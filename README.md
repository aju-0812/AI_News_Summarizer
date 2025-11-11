# ⚡ AI News Summarizer (Neon Black Edition)

A smart and fast **AI-powered news summarization web app** that helps you stay informed without spending time reading long articles.  
Just **paste a news URL**, and the system instantly provides:

- A **concise summary**
- **Sentiment analysis** (Happy / Sad / Neutral)
- **Fake news credibility score**
- **Breaking news feed**
- **Trending topics**
- **Global market dashboard**
- **Interactive market analysis charts (Price + RSI)**

---

## 🎯 Project Goal
To simplify news consumption and avoid information overload by providing **quick insights**, **credibility checks**, and **market context** — all in one elegant dashboard.

---

## 🧠 Features

| Feature | Description |
|--------|-------------|
| 📝 **AI Article Summarizer** | Extracts and summarizes article content automatically |
| 😊 **Sentiment Analysis** | Detects emotional tone of the news |
| ❗ **Fake News Detection** | Scores credibility using domain + text heuristics |
| 🔥 **Breaking News Feed** | Real-time news headlines with context |
| 📈 **Market Dashboard** | NIFTY 50, SENSEX, NASDAQ, S&P 500, Gold, Crude Oil, Bitcoin |
| 📊 **Advanced Financial Analysis** | Price trend graphs + **RSI(14)** indicator |
| 📡 **Trending Topics** | Google Trends or automatic keyword extraction |
| 🖥 **Neon Cyber UI** | Dark aesthetic with glowing accents (Gen Z + Tech vibes) |

---

## 🛠 Tech Stack

| Layer | Technology |
|------|------------|
| **Frontend** | HTML, CSS (Neon UI), Plotly.js |
| **Backend** | Flask (Python) |
| **News Parsing** | Newspaper3k, Requests |
| **NLP** | NLTK (punkt), TextBlob |
| **Fake News Logic** | Custom heuristic scoring |
| **Trends Data** | Google Trends API (pytrends) *(optional fallback included)* |
| **Finance Data** | Yahoo Finance API (yfinance) |

---

## 🔄 Workflow

1. User enters or pastes a news article URL in the website.

2. The system verifies whether the URL is valid and the article can be accessed.

3. The article content is downloaded and parsed using Newspaper3k.

4. NLP processing is performed:
      - Text is tokenized and summarized.
      - Sentiment (positive / negative / neutral) is detected.
      - Fake news credibility score is calculated based on domain and text patterns.

5. The summarized output is displayed to the user along with:
      - Sentiment result
      - Fake news credibility score
      - Author and publication details

6. Meanwhile, the homepage also fetches:
      - Breaking news (Google News RSS)
      - Trending search topics (PyTrends / fallback keyword extraction)
      - Global market snapshot (Yahoo Finance API)

7. When a user selects a market index:
      - Historical data is retrieved.
      - Price Chart and RSI (Relative Strength Index) are plotted using Plotly.js.

8. Final UI shows:
      → Summary + Sentiment
      → Breaking News Feed
      → Trending Topics
      → Market Dashboard + Financial Graphs


---

## 📂 Project Structure

AI-News-Summarizer/
│
├── app.py                     # Main Flask backend and routing logic
│
├── templates/                 # Frontend HTML Templates (Jinja2)
│   ├── base.html              # Main layout / navigation
│   ├── index.html             # Homepage + Summarizer UI
│   ├── news.html              # Category-wise news display page
│   ├── markets.html           # Global market dashboard interface
│   └── analysis.html          # Price + RSI interactive chart page
│
├── static/                    # Static frontend assets
│   └── neon.css               # Dark theme + glowing neon UI styling
│
├── requirements.txt           # Python dependencies
│
└── README.md                  # Documentation


## ⚙️ Setup & Installation

```bash
git clone <your-repo-url>
cd AI-News-Summarizer

# Create virtual environment
python -m venv .venv
source .venv/bin/activate   # (Windows: .venv\Scripts\activate)

# Install requirements
pip install -r requirements.txt

# Run server
python app.py
Then open:

cpp
Copy code
http://127.0.0.1:5000
🚀 Future Enhancements
Deep Learning-based summarization (T5 / BART)

More advanced fake news classifiers (BERT-based)

Multi-language summarization

User profiles + bookmark history

Mobile App (React Native / Flutter)

🙌 Credits
Developed by Ajendra
Neon UI + Market Visualization + Real-Time Intelligence Engine


