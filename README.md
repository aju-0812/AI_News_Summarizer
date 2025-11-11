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

User pastes news URL
↓
Article is downloaded + parsed
↓
Summary + Sentiment generated
↓
Credibility score calculated
↓
UI displays:
• Summary
• Sentiment
• Fake/Real Label
• Breaking News
• Trends
• Market Dashboard
• Market Analysis Charts

yaml
Copy code

---

## 📂 Project Structure

AI-News-Summarizer/
│
├── app.py # Main Flask app
├── templates/ # HTML templates
│ ├── index.html # Homepage + summarizer
│ ├── news.html # Category news
│ ├── markets.html # Market dashboard
│ └── analysis.html # Price & RSI chart page
│
├── static/
│ └── neon.css # UI styling
│
├── requirements.txt # Python dependencies
└── README.md # Documentation

yaml
Copy code

---

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

