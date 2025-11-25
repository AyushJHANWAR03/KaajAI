# 🤖 Kaaj AI - Multi-Agent Loan Analyzer

**Automated Small Business Loan Underwriting System powered by AI Agents**

A production-ready multi-agent AI system that automates loan underwriting by analyzing financial documents, calculating risk metrics, and generating professional credit memos in under 30 seconds.

[![Live Demo](https://img.shields.io/badge/Live%20Demo-kaajai.netlify.app-success?style=for-the-badge)](https://kaajai.netlify.app/)
[![Backend API](https://img.shields.io/badge/API-kaajai.onrender.com-blue?style=for-the-badge)](https://kaajai.onrender.com/docs)

**🔗 Live Application:** [https://kaajai.netlify.app/](https://kaajai.netlify.app/)  
**🔗 Backend API:** [https://kaajai.onrender.com](https://kaajai.onrender.com)  
**📚 API Documentation:** [https://kaajai.onrender.com/docs](https://kaajai.onrender.com/docs)

---

## 📹 Video Walkthrough

**[Watch Demo Video Here]** *(Recording in progress)*

> *A complete walkthrough showing the problem statement, solution architecture, live demo, and technical implementation details.*

---

## 🎯 Problem Statement

Small business loans ($50K-$500K) are often economically unviable for lenders due to high manual underwriting costs. The traditional process involves:

- **Days of manual work** reviewing financial documents
- **High error rates** from manual data entry and calculations
- **Inconsistent decisions** based on analyst experience
- **Expensive overhead** making small loans unprofitable
- **Risk assessment gaps** from incomplete debt service analysis

### Critical Bug Discovered

During development, I identified a **critical flaw in DSCR (Debt Service Coverage Ratio) calculation** commonly made in automated systems:

**The Problem:**  
Many systems calculate DSCR using ONLY the new loan payment, completely ignoring existing debt obligations. This creates dangerously optimistic risk assessments.

**Real Example - Main Street Restaurant:**
```
❌ WRONG CALCULATION (New Loan Only):
   Monthly Cash Flow: $3,583
   New Loan Payment: $1,664
   DSCR = 3,583 / 1,664 = 4.08  ← Looks safe!
   Result: Score 92/100, APPROVE

✅ CORRECT CALCULATION (Total Debt Service):
   Monthly Cash Flow: $3,583
   New Loan Payment: $1,664
   Existing Debt Payment: $1,408
   Total Payment: $3,072
   DSCR = 3,583 / 3,072 = 1.17  ← Below 1.25 threshold!
   Result: Score 40/100, HIGH RISK
```

**Impact:** A borrower with barely enough cash flow to cover total obligations was being approved as "excellent" risk. This is how lenders lose money.

---

## 💡 Solution

I built a **multi-agent AI system** that automates end-to-end loan underwriting while implementing industry-standard financial calculations correctly.

### Key Innovations

1. **Accurate DSCR Calculation**  
   Properly calculates debt service coverage using total monthly obligations (existing + new debt), matching real lending standards.

2. **Multi-Agent Architecture**  
   Three specialized AI agents work together:
   - **Financial Analyzer**: Extracts and calculates key metrics (DSCR, volatility, leverage ratios)
   - **Risk Assessor**: Identifies 6 risk flags across different severity levels
   - **Memo Generator**: Creates professional credit memos with AI-written analysis

3. **Industry-Standard Risk Assessment**  
   - DSCR threshold: 1.25 (industry standard)
   - 6 risk flags with HIGH/MEDIUM severity classification
   - Holistic evaluation combining quantitative metrics and qualitative patterns

4. **Professional Output**  
   Generates complete credit memos with:
   - Underwriting score (0-100)
   - Risk level classification
   - Specific recommendations (APPROVE/CONDITIONS/DECLINE)
   - Detailed conditions when applicable
   - Professional business analysis

---

## ⚡ Features

### Core Capabilities
- ✅ **30-Second Analysis**: Complete underwriting in under 30 seconds
- ✅ **Multi-Agent Processing**: Three specialized AI agents working in sequence
- ✅ **Industry-Standard Calculations**: DSCR, volatility, leverage ratios, stability scoring
- ✅ **Risk Flag Detection**: 6 automated risk checks with severity classification
- ✅ **Credit Memo Generation**: AI-written professional credit analysis
- ✅ **Beautiful UI**: Step-by-step wizard with real-time progress tracking

### Technical Features
- ✅ **No Database Required**: Uses SQLite for simplicity
- ✅ **RESTful API**: FastAPI backend with auto-generated documentation
- ✅ **Type Safety**: Full TypeScript frontend
- ✅ **Production Ready**: Deployed on Render + Netlify with zero cost
- ✅ **Comprehensive Testing**: 97% code coverage on financial calculations
- ✅ **8 Test Scenarios**: Pre-configured realistic loan applications

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────┐
│             User Interface (React + TS)             │
│          https://kaajai.netlify.app/                │
└────────────────────────┬────────────────────────────┘
                         │ HTTPS
                         ▼
┌─────────────────────────────────────────────────────┐
│           FastAPI Backend (Python 3.11)             │
│         https://kaajai.onrender.com                 │
│                                                      │
│  ┌───────────────────────────────────────────────┐ │
│  │   Multi-Agent Orchestrator                    │ │
│  │   (LangGraph-inspired workflow)               │ │
│  └───────────────────────────────────────────────┘ │
│                         │                            │
│         ┌───────────────┼───────────────┐           │
│         ▼               ▼               ▼           │
│  ┌──────────┐    ┌──────────┐   ┌──────────┐      │
│  │ Agent 1: │───▶│ Agent 2: │──▶│ Agent 3: │      │
│  │Financial │    │   Risk   │   │   Memo   │      │
│  │ Analyzer │    │ Assessor │   │Generator │      │
│  └──────────┘    └──────────┘   └──────────┘      │
│                                                      │
│  Calculates:     Identifies:     Generates:        │
│  • DSCR*         • 6 Risk Flags  • Credit Memo    │
│  • Volatility    • Risk Level    • Score 0-100    │
│  • Stability     • Positive      • Recommendation │
│  • Debt Ratios   • Signals       • Conditions     │
│                                                      │
│  *Correctly includes existing debt + new loan      │
└─────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────┐
│              SQLite Database (Local)                 │
│              Analysis history & results              │
└─────────────────────────────────────────────────────┘
```

---

## 📊 Sample Results

The system has been tested with 8 realistic business loan scenarios:

| Business | Industry | Loan | DSCR | Score | Decision |
|----------|----------|------|------|-------|----------|
| ABC Construction | Construction | $50K | 3.51 | 93 | ✅ APPROVE |
| Main Street Restaurant | Restaurant | $65K | 1.17 | 40 | ⚠️ CONDITIONS |
| Quick Cash Payday | Services | $100K | -0.04 | 19 | ❌ DECLINE |
| TechParts Mfg | Manufacturing | $75K | 4.42 | 97 | ✅ APPROVE |
| Ski Shop | Retail | $40K | 1.66 | 65 | ⚠️ CONDITIONS |
| Family Dental | Healthcare | $120K | 0.02 | 29 | ❌ DECLINE |
| CloudSync Tech | Technology | $60K | 2.75 | 88 | ✅ APPROVE |
| Metro Courier | Transportation | $80K | -0.31 | 26 | ❌ DECLINE |

*Note: DSCR values correctly include both existing and new debt payments*

---

## 🔑 Key Calculations Explained

### DSCR (Debt Service Coverage Ratio)
The most critical metric for loan approval decisions.

```python
# CORRECT METHOD
new_loan_payment = calculate_payment(new_loan, rate, term)
existing_debt_payment = calculate_payment(existing_debt, rate, term)
total_monthly_payment = new_loan_payment + existing_debt_payment

DSCR = monthly_cash_flow / total_monthly_payment

# Industry Standard
DSCR >= 1.25  → Approve
DSCR 1.0-1.25 → Conditional approval with safeguards
DSCR < 1.0    → Decline (insufficient cash flow)
```

### Underwriting Score (0-100)
Weighted composite score across four factors:

- **Risk Level (40%)**: LOW=40pts, MODERATE=25pts, HIGH=10pts
- **DSCR (30%)**: ≥1.75=30pts, ≥1.50=25pts, ≥1.25=20pts, ≥1.0=10pts
- **Stability (20%)**: Based on volatility, business age, NSF fees
- **Volatility (10%)**: Revenue consistency measure

### Risk Flags
Six automated checks with severity classification:

| Flag | Severity | Trigger |
|------|----------|---------|
| Low DSCR | HIGH | < 1.25 |
| Cash Flow Issues | HIGH | > 3 NSF fees |
| Negative Cash Flow | HIGH | Monthly loss |
| Unstable Revenue | MEDIUM | > 40% volatility |
| High Leverage | MEDIUM | > 50% debt-to-revenue |
| Declining Revenue | MEDIUM | < -10% trend |

---

## 🚀 Try It Yourself

### Live Demo
Visit [https://kaajai.netlify.app/](https://kaajai.netlify.app/) and try the **Main Street Restaurant** scenario:

1. Enter business details:
   - Name: Main Street Restaurant
   - Industry: Restaurant
   - Age: 3 years

2. Enter loan request:
   - Amount: $65,000
   - Rate: 10.5%
   - Term: 48 months
   - Existing Debt: $55,000

3. Paste bank statement data:
   ```
   Deposits: 28000, 32000, 25000, 31000, 27000, 33000, 29000, 26000, 34000, 30000, 28000, 31000
   Withdrawals: 24000, 27000, 23000, 26000, 25000, 28000, 26000, 24000, 29000, 27000, 25000, 27000
   NSF Fees: 3
   ```

4. Add optional tax data (recommended):
   ```
   Revenue: $350,000
   Expenses: $320,000
   Net Income: $30,000
   ```

5. Review and submit for analysis

**Expected Result:**  
DSCR: 1.17, Score: ~40, Risk: HIGH, Decision: DECLINE or APPROVE_WITH_CONDITIONS

---

## 💻 Technology Stack

**Backend:**
- Python 3.11 (FastAPI framework)
- OpenAI GPT-4o-mini for AI analysis
- Pydantic for data validation
- NumPy/Pandas for financial calculations
- SQLite for data persistence
- Pytest with 97% coverage

**Frontend:**
- React 18 + TypeScript
- Vite (build tool)
- TailwindCSS (styling)
- Axios (API client)

**Infrastructure:**
- Render (backend hosting - free tier)
- Netlify (frontend hosting - free tier)
- Total cost: $0/month (+ OpenAI API usage)

---

## 📁 Project Structure

```
kaaj-multi-agent-analyzer/
├── backend/
│   ├── agents/                      # Multi-agent implementation
│   │   ├── financial_analyzer.py    # Calculates DSCR, metrics
│   │   ├── risk_assessor.py         # Identifies risk flags
│   │   └── memo_generator.py        # Generates credit memos
│   ├── api/                         # FastAPI routes & schemas
│   ├── tests/                       # Comprehensive test suite
│   ├── main.py                      # Application entry point
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── App.tsx                  # Main wizard component
│   │   ├── components/              # Reusable UI components
│   │   └── types.ts                 # TypeScript definitions
│   └── package.json
│
├── TEST_SCENARIOS.md                # 8 pre-configured test cases
├── DEPLOYMENT.md                    # Deployment instructions
└── README.md                        # This file
```

---

## 🎯 Business Impact

### Problem Solved
Small business loans are often unprofitable due to high underwriting costs. Manual review of a $50K loan can cost $500-1000, making the economics unfavorable.

### Solution Impact
- ⏱️ **Time**: Days → 30 seconds (99.9% reduction)
- 💰 **Cost**: $500-1000 → ~$0.50 in API costs (99.9% reduction)
- 🎯 **Accuracy**: Consistent, bias-free risk assessment
- 📈 **Scale**: Can process thousands of applications daily
- ✅ **Quality**: Professional credit memos for every application

### Makes Possible
- Small loans ($10K-$100K) become economically viable
- Instant preliminary decisions for applicants
- Reduced bias in lending decisions
- Scalable underwriting without linear cost growth

---

## 🧪 Testing & Validation

### Test Coverage
```bash
cd backend
pytest tests/ -v --cov=agents --cov-report=html
```

**Results:**
- 97% coverage on financial_analyzer.py
- All 16 unit tests passing
- End-to-end integration tests validated

### Test Scenarios
8 realistic loan scenarios in `TEST_SCENARIOS.md`:
- 3 APPROVE cases (strong businesses)
- 3 DECLINE cases (high risk/over-leveraged)
- 2 APPROVE_WITH_CONDITIONS (borderline cases)

Each scenario includes:
- Complete business profile
- 12 months of bank statement data
- Tax return information
- Expected DSCR, score, and recommendation

---

## 🔐 Security & Privacy

- ✅ No sensitive data stored permanently
- ✅ SQLite used only for analysis history (optional)
- ✅ HTTPS encryption for all API communication
- ✅ CORS properly configured
- ✅ No PII collected or retained
- ✅ OpenAI API calls are stateless

---

## 🚀 Local Development

### Prerequisites
- Node.js 18+
- Python 3.11+
- OpenAI API key

### Setup

1. **Clone repository:**
```bash
git clone https://github.com/AyushJHANWAR03/KaajAI.git
cd KaajAI
```

2. **Backend setup:**
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
echo "OPENAI_API_KEY=your-key-here" > .env
uvicorn main:app --reload --port 8000
```

3. **Frontend setup:**
```bash
cd frontend
npm install
npm run dev
```

4. **Open:** http://localhost:5173

---

## 📈 Future Enhancements

Potential areas for expansion:

1. **Additional Document Types**
   - Balance sheets
   - Profit & loss statements
   - Business licenses

2. **Advanced Analytics**
   - Industry benchmarking
   - Trend analysis
   - Fraud detection

3. **Workflow Features**
   - Multi-borrower support
   - Approval workflows
   - Document versioning

4. **Integration Capabilities**
   - CRM systems
   - Banking APIs
   - Credit bureau integration

---

## 👤 About

**Developer:** Ayush Jhanwar  
**GitHub:** [@AyushJHANWAR03](https://github.com/AyushJHANWAR03)  
**Built For:** Demonstrating multi-agent AI architecture for financial analysis  

---

## 📄 License

MIT License - See LICENSE file for details

---

## 🤝 Acknowledgments

- Built with FastAPI, React, and OpenAI GPT-4
- Deployed on Render and Netlify free tiers
- Inspired by real-world loan underwriting challenges

---

**⭐ Star this repository if you found it useful!**

**🔗 Try the live demo:** [https://kaajai.netlify.app/](https://kaajai.netlify.app/)
