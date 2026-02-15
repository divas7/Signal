# SIGNAL

**Institutional-Grade Trading Intelligence for the Retail Trader.**

![Signal Dashboard](frontend/public/signal_logo_v3.png)

## 🌟 Why SIGNAL?

Most people don't know how to trade effectively. The markets are complex, volatile, and often stacked against the individual investor. To make matters worse, recent government regulations have imposed higher taxes on Futures & Options (F&O), squeezing margins and making profitability even harder to achieve.

We created **SIGNAL** to level the playing field. 

It provides clear, actionable intelligence without the noise, designed to give you a **better understanding** of market dynamics and improve your **profitability** in this challenging environment.

---

## 🚀 The S.T.A.R. Methodology

SIGNAL is built upon our proprietary **S.T.A.R.** methodology, a comprehensive framework for market analysis:

### **S - Sentiment (Regime)**
Understanding the "mood" of the market is the first step. Is the market Bullish, Bearish, or Neutral? We analyze broad market data to determine the current regime, ensuring you never trade against the tide.

### **T - Technicals (Indicators)**
We process real-time data using advanced technical indicators (EMA, RSI, MACD, Bollinger Bands) to identify precise entry and exit points. No more guessing—just data-driven signals.

### **A - Action (Decision Engine)**
Our expert system synthesizes Sentiment and Technicals into a clear, binary action: **BUY**, **SELL**, or **NEUTRAL**. It eliminates emotional decision-making, providing a confidence score for every signal.

### **R - Risk (Management)**
Profitability isn't just about making money; it's about not losing it. We provide dynamic Support & Resistance levels ("Levels Ladder") and clear stop-loss guidelines to protect your capital.

---

## ✨ Key Features

- **Real-Time Signals**: Live BUY/SELL actionable insights with confidence scores.
- **Expert Playbook**: automated commentary that explains *why* a signal was generated, in plain English.
- **NIFTY & Bitcoin Support**: Track India's premier index and the world's leading cryptocurrency.
- **Levels Ladder**: Dynamic support and resistance visualization.
- **Market Status**: Instantly know if the market is Open, Closed, or in Pre-market.

## 🛠️ Installation & Setup

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
