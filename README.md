# 🤖 Kaaj AI - Multi-Agent Loan Analyzer

**Automated Small Business Loan Underwriting with AI Agents**

A production-ready multi-agent AI system that automates loan underwriting using specialized AI agents for financial analysis, risk assessment, and credit memo generation.

[![Deploy Backend](https://img.shields.io/badge/Deploy-Render-46E3B7?style=for-the-badge&logo=render)](https://render.com)
[![Deploy Frontend](https://img.shields.io/badge/Deploy-Netlify-00C7B7?style=for-the-badge&logo=netlify)](https://netlify.com)

---

## 🎯 The Problem We Solved

**Before:** DSCR was calculated using ONLY the new loan payment, ignoring existing debt. This made risky borrowers appear safe.

**Example - Main Street Restaurant:**
- ❌ **Wrong:** DSCR 4.08, Score 92/100, APPROVE
- ✅ **Fixed:** DSCR 1.17, Score 40/100, CONDITIONS/DECLINE

**Impact:** Proper risk assessment that matches industry lending standards.

---

## ⚡ Features

- **Multi-Agent Architecture**: 5 specialized AI agents working together
- **Industry-Standard DSCR**: Includes total debt service (existing + new)
- **Risk Assessment**: 6 risk flags with severity levels
- **Credit Memo Generation**: AI-written professional credit memos
- **Beautiful UI**: Step-by-step wizard with real-time progress
- **8 Test Scenarios**: Pre-configured realistic loan applications
- **No Database Required**: Uses SQLite for simplicity

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│                  User Interface                     │
│            (React + TypeScript + Vite)              │
└─────────────────────────────────────────────────────┘
                        ↓ HTTP
┌─────────────────────────────────────────────────────┐
│                FastAPI Backend                      │
│                                                     │
│  ┌──────────────────────────────────────────────┐  │
│  │    Agent Orchestrator (LangGraph-style)     │  │
│  └──────────────────────────────────────────────┘  │
│                        ↓                            │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────┐  │
│  │   Agent 3:   │→ │   Agent 4:   │→ │ Agent 5:│  │
│  │  Financial   │  │     Risk     │  │  Memo   │  │
│  │   Analyzer   │  │   Assessor   │  │Generator│  │
│  └──────────────┘  └──────────────┘  └─────────┘  │
│                                                     │
│  Calculates:         Identifies:      Generates:   │
│  • DSCR (fixed!)     • 6 Risk Flags   • Credit     │
│  • Volatility        • Risk Level     • Memo       │
│  • Stability         • Positive       • Score      │
│  • Debt Ratios       • Signals        • Decision   │
└─────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- Python 3.11+
- OpenAI API key

### Local Development

1. **Clone the repo:**
```bash
git clone https://github.com/AyushJHANWAR03/KaajAI.git
cd KaajAI
```

2. **Backend Setup:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Create .env file
echo "OPENAI_API_KEY=your-key-here" > .env

# Run backend
uvicorn main:app --reload --port 8000
```

3. **Frontend Setup:**
```bash
cd frontend
npm install
npm run dev
```

4. **Open:** http://localhost:5173

---

## 📊 Test Scenarios

The app includes 8 pre-configured test scenarios in `TEST_SCENARIOS.md`:

| Scenario | Business | Expected | DSCR | Score |
|----------|----------|----------|------|-------|
| 1 | ABC Construction | APPROVE | 3.51 | 93 |
| 2 | Main Street Restaurant | CONDITIONS | 1.17 | 40 |
| 3 | Quick Cash Payday | DECLINE | -0.04 | 19 |
| 4 | TechParts Manufacturing | APPROVE | 4.42 | 97 |
| 5 | Ski Shop (Seasonal) | CONDITIONS | 1.66 | 65 |
| 6 | Family Dental | DECLINE | 0.02 | 29 |
| 7 | CloudSync Tech | APPROVE | 2.75 | 88 |
| 8 | Metro Courier | DECLINE | -0.31 | 26 |

---

## 🎥 Video Demo Script

### 1. Show the Bug Fix (1 min)
- Explain: "DSCR was only counting new loan, not total debt"
- Show Main Street Restaurant
- **Before:** DSCR 4.08, Score 92, APPROVE ❌
- **After:** DSCR 1.17, Score 40, CONDITIONS ✅

### 2. Live Demo (3 min)
- Walk through 5-step form
- Submit Main Street Restaurant
- Show 30-second analysis
- Highlight:
  - DSCR calculation (includes existing debt)
  - Risk flags (LOW DSCR, 3 NSF fees)
  - Credit memo generation

### 3. Different Outcomes (1 min)
- ABC Construction: Score 93, APPROVE
- Quick Cash: Score 19, DECLINE (negative DSCR!)

### 4. Technical Highlights (1 min)
- Multi-agent architecture
- LangGraph-style orchestration
- Industry-standard calculations
- Beautiful UI

---

## 🌐 Deployment

See `DEPLOYMENT.md` for detailed instructions.

**TL;DR:**
1. Push to GitHub
2. Deploy backend to Render (free tier)
3. Deploy frontend to Netlify (free tier)
4. Add `OPENAI_API_KEY` to Render
5. Add `VITE_API_URL` to Netlify

**Cost:** $0/month (OpenAI API usage not included)

---

## 📁 Project Structure

```
kaaj-multi-agent-analyzer/
├── backend/
│   ├── agents/              # AI agent implementations
│   │   ├── financial_analyzer.py   # Calculates DSCR, volatility
│   │   ├── risk_assessor.py        # Identifies risk flags
│   │   └── memo_generator.py       # Generates credit memo
│   ├── api/                 # FastAPI routes
│   ├── tests/              # Unit & integration tests
│   ├── main.py             # FastAPI app
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── App.tsx         # Main wizard component
│   │   ├── components/     # Reusable components
│   │   └── types.ts        # TypeScript types
│   ├── package.json
│   └── netlify.toml
│
├── TEST_SCENARIOS.md       # 8 pre-configured scenarios
├── FIXES_SUMMARY.md        # Detailed bug fix explanation
├── DEPLOYMENT.md           # Step-by-step deployment guide
└── README.md               # This file
```

---

## 🧪 Testing

```bash
cd backend
pytest tests/ -v --cov=agents --cov-report=html
```

**Coverage:** 97% for financial_analyzer.py

---

## 🔑 Key Calculations

### DSCR (Debt Service Coverage Ratio)
```python
# CORRECT METHOD (includes total debt)
total_payment = new_loan_payment + existing_debt_payment
DSCR = monthly_cash_flow / total_payment

# Industry Standard: DSCR >= 1.25 for approval
```

### Underwriting Score (0-100)
- Risk Level (40%): LOW=40pts, MODERATE=25pts, HIGH=10pts
- DSCR (30%): ≥1.75=30pts, ≥1.50=25pts, ≥1.25=20pts
- Stability (20%): Volatility, age, NSF fees
- Volatility (10%): Revenue consistency

### Risk Flags
1. **LOW DSCR** (HIGH): < 1.25
2. **CASH FLOW ISSUES** (HIGH): > 3 NSF fees
3. **NEGATIVE CASH FLOW** (HIGH): Losing money
4. **UNSTABLE REVENUE** (MEDIUM): > 40% volatility
5. **HIGH LEVERAGE** (MEDIUM): > 50% debt-to-revenue
6. **DECLINING REVENUE** (MEDIUM): < -10% trend

---

## 🤝 Contributing

This is a demonstration project for the Kaaj AI SDE-1 interview.

---

## 📝 License

MIT License - see LICENSE file

---

## 👤 Author

**Ayush Jhanwar**
- GitHub: [@AyushJHANWAR03](https://github.com/AyushJHANWAR03)
- Built for: Kaaj AI Interview

---

## 🎯 Why This Matters

Small business loans ($50K-$500K) are often economically unviable due to manual underwriting costs. This system:

- ✅ Reduces underwriting time from days to **30 seconds**
- ✅ Provides **consistent, bias-free** risk assessment
- ✅ Uses **industry-standard** financial calculations
- ✅ Generates **professional credit memos** automatically
- ✅ Makes small loans **economically viable**

---

**Built with:** FastAPI • React • TypeScript • OpenAI GPT-4 • LangGraph Architecture

**Deployed on:** Render (Backend) • Netlify (Frontend)

---

⭐ **Star this repo if you found it useful!**
