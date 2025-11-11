from flask import Flask, request, render_template, flash, redirect, url_for
import os
import time
from datetime import datetime, timedelta
from urllib.parse import urlparse

import nltk
from textblob import TextBlob
from newspaper import Article
import validators
import requests
import feedparser
import yfinance as yf

try:
    from pytrends.request import TrendReq
    PYTRENDS_AVAILABLE = True
except Exception:
    PYTRENDS_AVAILABLE = False

nltk.download('punkt', quiet=True)

app = Flask(__name__)
app.secret_key = os.environ.get('APP_SECRET_KEY', 'your_secret_key')

# -----------------------------
# Simple TTL cache to avoid hammering APIs
# -----------------------------
_cache = {}

def cached(key, ttl_seconds, loader):
    now = time.time()
    if key in _cache:
        val, ts = _cache[key]
        if now - ts < ttl_seconds:
            return val
    val = loader()
    _cache[key] = (val, now)
    return val

# -----------------------------
# Utilities
# -----------------------------

def get_website_name(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    if domain.startswith("www."):
        domain = domain[4:]
    return domain

# Basic credibility list (toy). You can extend this.
TRUSTED_DOMAINS = {
    'bbc.com', 'reuters.com', 'apnews.com', 'thehindu.com', 'hindustantimes.com',
    'indianexpress.com', 'ndtv.com', 'aljazeera.com', 'nytimes.com', 'theguardian.com',
    'wsj.com', 'bloomberg.com', 'economictimes.indiatimes.com'
}

CLICKBAIT = {
    'shocking', 'you won\'t believe', 'miracle', 'secret revealed', 'exposed', 'what happens next',
    'jaw-dropping', 'unbelievable', 'this is why', 'number #', 'insane', 'must see'
}


def fake_news_score(url, text):
    """Return (score 0-100, label). 0=very reliable, 100=very fake-y
    Heuristic based: domain credibility + clickbait + punctuation + ALL CAPS ratio.
    """
    domain = get_website_name(url)
    base = 30 if domain not in TRUSTED_DOMAINS else 5

    t = text or ''
    lower = t.lower()

    # Clickbait words
    bait = sum(1 for w in CLICKBAIT if w in lower)

    # Too many exclamations / question marks
    punct_bloat = min(20, (t.count('!') + t.count('?')) * 2)

    # ALL CAPS ratio for words length >= 4
    words = [w for w in t.split() if len(w) >= 4]
    caps = sum(1 for w in words if w.isupper())
    caps_ratio = (caps / max(1, len(words))) * 30  # up to 30 points

    score = min(100, base + bait * 10 + punct_bloat + caps_ratio)
    label = 'Likely Real ✅' if score < 30 else ('Uncertain ⚠️' if score < 55 else 'Likely Fake ❌')
    return round(score, 1), label

# -----------------------------
# News & Markets helpers
# -----------------------------

MARKET_TICKERS = {
    'NIFTY 50': '^NSEI',
    'SENSEX': '^BSESN',
    'NASDAQ': '^IXIC',
    'S&P 500': '^GSPC',
    'Crude Oil': 'CL=F',
    'Gold': 'GC=F',
    'Bitcoin': 'BTC-USD'
}

NAME_BY_TICKER = {v: k for k, v in MARKET_TICKERS.items()}

def get_breaking_news(limit=12):
    def loader():
        feed_url = 'https://news.google.com/rss?hl=en-IN&gl=IN&ceid=IN:en'
        feed = feedparser.parse(feed_url)
        out = []
        for e in feed.entries[:limit]:
            img = None
            # try RSS thumbnail
            if hasattr(e, 'media_thumbnail') and e.media_thumbnail:
                img = e.media_thumbnail[0].get('url')
            summary = None
            try:
                art = Article(e.link); art.download(); art.parse(); art.nlp()
                if not img:
                    img = art.top_image
                # take first 1-2 sentences of summary
                s = art.summary.split('.')
                summary = '. '.join(s[:2]).strip() + '.' if len(s) > 1 else art.summary
            except Exception:
                pass
            out.append({
                'title': e.title,
                'link': e.link,
                'image': img,
                'summary': summary,
                'published': getattr(e, 'published', ''),
            })
        return out
    return cached('breaking_news', 300, loader)  # 5 minutes


def get_category_news(topic, limit=20):
    topic_q = requests.utils.quote(topic)
    feed_url = f'https://news.google.com/rss/search?q={topic_q}&hl=en-IN&gl=IN&ceid=IN:en'
    feed = feedparser.parse(feed_url)
    return [{
        'title': e.title,
        'link': e.link,
        'published': getattr(e, 'published', ''),
    } for e in feed.entries[:limit]]


def get_trends_top(n=10, geo='IN'):
    """Return trending topics.
    If pytrends isn't available or fails, fall back to extracting frequent keywords from breaking news titles."""
    def fallback_from_breaking():
        import re
        stop = {
            'the','a','an','and','or','but','with','from','for','that','this','these','those','into','over','under',
            'after','before','about','amid','as','to','in','on','at','of','by','is','are','was','were','be','being','been',
            'will','can','could','would','should','has','have','had','it','its','they','them','their','you','we','our'
        }
        titles = [x['title'] for x in get_breaking_news(limit=50)]
        freq = {}
        for t in titles:
            for w in re.findall(r"[A-Za-z][A-Za-z\-']{2,}", t):
                lw = w.lower()
                if lw in stop or len(lw) < 4:
                    continue
                freq[lw] = freq.get(lw, 0) + 1
        return [k for k,_ in sorted(freq.items(), key=lambda kv: kv[1], reverse=True)[:n]]

    if not PYTRENDS_AVAILABLE:
        return fallback_from_breaking()

    def loader():
        try:
            pytrend = TrendReq(hl='en-US', tz=330)
            df = pytrend.trending_searches(pn='india' if geo == 'IN' else 'united_states')
            items = [str(x) for x in df[0].head(n).values]
            if items:
                return items
            return fallback_from_breaking()
        except Exception:
            return fallback_from_breaking()

    return cached('trends_top', 1800, loader)  # 30 min cache


def get_market_snapshot():
    def loader():
        data = {}
        for name, t in MARKET_TICKERS.items():
            try:
                hist = yf.Ticker(t).history(period='7d')
                if hist.empty:
                    data[name] = {'price': None, 'chg': None, 'pct': None, 'hist': []}
                    continue
                closes = list(hist['Close'].tail(7))
                close = float(closes[-1])
                prev = float(closes[-2]) if len(closes) > 1 else close
                chg = close - prev
                pct = (chg / prev * 100.0) if prev else 0.0
                data[name] = {'price': close, 'chg': chg, 'pct': pct, 'hist': closes, 'ticker': t}
            except Exception:
                data[name] = {'price': None, 'chg': None, 'pct': None, 'hist': [], 'ticker': t}
        return data
    return cached('market_snapshot', 600, loader)  # 10 minutes

def compute_rsi(series, period: int = 14):
    import numpy as np
    if len(series) < period + 1:
        return [None] * len(series)
    deltas = np.diff(series)
    ups = np.where(deltas > 0, deltas, 0.0)
    downs = np.where(deltas < 0, -deltas, 0.0)
    roll_up = np.convolve(ups, np.ones(period), 'full')[:len(ups)] / period
    roll_down = np.convolve(downs, np.ones(period), 'full')[:len(downs)] / period
    rs = np.divide(roll_up, roll_down, out=np.zeros_like(roll_up), where=roll_down!=0)
    rsi = 100.0 - (100.0 / (1.0 + rs))
    rsi = [None] + list(rsi)  # align lengths
    # pad if needed
    if len(rsi) < len(series):
        rsi = [None] * (len(series) - len(rsi)) + rsi
    return rsi


def get_history_with_indicators(ticker: str, period: str = '6mo', interval: str = '1d'):
    hist = yf.Ticker(ticker).history(period=period, interval=interval)
    if hist.empty:
        return [], [], [], []
    dates = [d.strftime('%Y-%m-%d') for d in hist.index.to_pydatetime()]
    closes = [float(x) for x in hist['Close'].tolist()]
    volume = [int(x) for x in hist['Volume'].fillna(0).tolist()]
    rsi = compute_rsi(closes, period=14)
    return dates, closes, volume, rsi

# -----------------------------
# Routes
# -----------------------------

@app.route('/', methods=['GET', 'POST'])
def index():
    breaking = get_breaking_news()
    trends = get_trends_top()
    market = get_market_snapshot()

    if request.method == 'POST':
        url = request.form.get('url', '').strip()

        if not validators.url(url):
            flash('Please enter a valid URL.')
            return redirect(url_for('index'))

        try:
            response = requests.get(url, timeout=15)
            response.raise_for_status()
        except requests.RequestException:
            flash('Failed to download the content of the URL.')
            return redirect(url_for('index'))

        article = Article(url)
        article.download()
        article.parse()
        try:
            article.nlp()
        except Exception:
            pass

        title = article.title
        authors = ', '.join(article.authors) or get_website_name(url)
        publish_date = article.publish_date.strftime('%B %d, %Y') if article.publish_date else "N/A"

        article_text = article.text or ''
        sentences = [s.strip() for s in article_text.split('.') if s.strip()]
        max_summarized_sentences = 5
        summary = '. '.join(sentences[:max_summarized_sentences]) + ('.' if sentences else '')

        top_image = article.top_image

        analysis = TextBlob(article_text)
        polarity = analysis.sentiment.polarity
        if polarity > 0:
            sentiment = 'happy 😊'
        elif polarity < 0:
            sentiment = 'sad 😟'
        else:
            sentiment = 'neutral 😐'

        if summary == "":
            flash('Sorry, that link did not produce a readable article. Try another URL.')
            return redirect(url_for('index'))

        score, fake_label = fake_news_score(url, article_text)

        return render_template(
            'index.html',
            title=title,
            authors=authors,
            publish_date=publish_date,
            summary=summary,
            top_image=top_image,
            sentiment=sentiment,
            fake_label=fake_label,
            fake_score=score,
            breaking_news=breaking,
            trends=trends,
            market=market
        )

    return render_template('index.html', breaking_news=breaking, trends=trends, market=market)


@app.route('/news/<topic>')
def news_topic(topic):
    articles = get_category_news(topic)
    return render_template('news.html', topic=topic.title(), articles=articles)


@app.route('/markets')
def markets():
    snapshot = get_market_snapshot()
    return render_template('markets.html', market=snapshot)


@app.route('/markets/analysis/<path:ticker>')
def market_analysis(ticker):
    name = NAME_BY_TICKER.get(ticker, ticker)
    dates, closes, volume, rsi = get_history_with_indicators(ticker)
    return render_template('analysis.html', name=name, ticker=ticker, dates=dates, closes=closes, volume=volume, rsi=rsi)
if __name__ == '__main__':
    app.run(debug=True)

