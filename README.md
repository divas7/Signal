# SIGNAL

**Institutional-Grade Trading Intelligence for the Retail Trader.**

[![Netlify Status](https://api.netlify.com/api/v1/badges/b5c7e0c7-1234-4567-8901-abcdef123456/deploy-status)](https://signalnb.netlify.app)

[**Live Demo: https://signalnb.netlify.app**](https://signalnb.netlify.app)

## 🌟 The Vision

Trading is hard. The markets are complex, volatile, and often stacked against the individual investor. To make matters worse, recent government regulations have imposed higher taxes on Futures & Options (F&O), squeezing margins and making profitability even harder to achieve.

We realized that most people simply don't have the tools to navigate this environment effectively. They rely on gut feelings, random tips, or overly complex charts that paralyze decision-making.

**This is why we created SIGNAL.**

Our goal was to build a system that cuts through the noise. We wanted to provide clear, data-driven intelligence that helps traders understand *what* is happening and *why*, empowering them to make better decisions in a challenging market.

---

## 🚀 Methodology

SIGNAL is built upon a robust analytical framework designed to process market data and output actionable intelligence:

### **1. Sentiment Analysis (Regime Detection)**
We start by understanding the "mood" of the market. Is it Bullish, Bearish, or Neutral? By analyzing broad market data, we determine the current regime, ensuring you never trade against the tide.

### **2. Technical Precision (Indicators)**
We process real-time price action using advanced technical indicators (EMA, RSI, MACD, Bollinger Bands) to identify precise entry and exit points. This removes guesswork and replaces it with mathematical probability.

### **3. Decision Engine (Action)**
Our expert system synthesizes Sentiment and Technicals into a clear, binary action: **BUY**, **SELL**, or **NEUTRAL**. It eliminates emotional decision-making, providing a confidence score for every signal.

### **4. Risk Management (Protection)**
Profitability isn't just about making money; it's about keeping it. We provide dynamic Support & Resistance levels ("Levels Ladder") and clear stop-loss guidelines to protect your capital.

---

## 🛠️ Technology Stack

We built SIGNAL using a modern, scalable stack designed for speed and reliability.

### **Frontend**
- **Framework**: [Next.js](https://nextjs.org/) (React) - For server-side rendering and static generation.
- **Language**: TypeScript - ensuring type safety and code quality.
- **Styling**: [Tailwind CSS](https://tailwindcss.com/) - utility-first CSS for rapid UI development.
- **Charting**: [Lightweight Charts](https://tradingview.github.io/lightweight-charts/) - high-performance financial charts.
- **Icons**: Lucide React - clean, consistent iconography.

### **Backend**
- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) - high-performance Python web framework.
- **Language**: Python 3.9+ - the standard for data science and financial analysis.
- **Data Analysis**: Pandas & NumPy - for efficient time-series processing.
- **Market Data**: `yfinance` - robust connector for fetching real-time market data.
- **Server**: Uvicorn - lightning-fast ASGI server.

### **Tools & DevOps**
- **Version Control**: Git & GitHub
- **Deployment**: Netlify (Frontend)
- **Containerization**: Docker (optional)

---

## ⚡ Quick Start (Local Development)

### Prerequisites
- Node.js (v18+)
- Python (v3.9+)

### 1. Clone the Repository
```bash
git clone https://github.com/divas7/Signal.git
cd Signal
```

### 2. Backend Setup
Navigate to the backend directory, create a virtual environment, and install dependencies.

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Run the backend server:
```bash
uvicorn app.main:app --reload
```
*The backend runs on http://localhost:8000*

### 3. Frontend Setup
Navigate to the frontend directory and install dependencies.

```bash
cd ../frontend
npm install
```

Run the development server:
```bash
npm run dev
```
*The frontend runs on http://localhost:3000*

---

## 🤝 Contributing

We welcome contributions! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
