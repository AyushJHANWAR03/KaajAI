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

> *A complete walkthrough showing the inspiration, problem statement, solution architecture, live demo, and technical implementation details.*

---

## 💡 Inspiration - Kaaj AI

This project is inspired by [Kaaj AI](https://kaaj.ai), a company building AI-powered loan underwriting automation for small business lenders. After researching their approach to automating financial document analysis and risk assessment, I wanted to deeply understand the challenges in this space by building a working prototype.

### Why This Problem Matters

Kaaj AI addresses a critical inefficiency in lending: **small business loans ($50K-$500K) are often economically unviable** due to high manual underwriting costs. Traditional underwriters spend days reviewing documents, entering data, and making subjective decisions - making each loan review cost $500-1000. This overhead makes small loans unprofitable, leaving small businesses underserved.

---

## 🎯 Problem Statement

After studying the loan underwriting process, I identified several critical challenges:

### 1. **Economic Inefficiency**
- Manual review takes **3-5 days** per application
- Underwriter costs: **$500-1000** per loan review
- Makes loans under $100K **unprofitable**
- Limits access to capital for small businesses

### 2. **Quality & Consistency Issues**
- High error rates from manual data entry
- Inconsistent decisions based on analyst experience
- Subjective risk assessment
- No standardized documentation

### 3. **Scalability Limitations**
- Linear cost growth with volume
- Limited by human capacity
- Can't serve high-volume, low-ticket loans
- Bottleneck in the lending process

### 4. **Technical Complexity**
- Multiple document types (bank statements, tax returns, P&L)
- Complex financial calculations (DSCR, leverage ratios, volatility)
- Risk assessment requires domain expertise
- Professional memo writing is time-consuming

---

## 💡 My Solution

I built a **multi-agent AI system** that automates the entire underwriting workflow, reducing the process from days to 30 seconds while maintaining accuracy and generating professional outputs.

### Core Architecture

Three specialized AI agents work in sequence, each handling a specific aspect of underwriting:

**Agent 1: Financial Analyzer**
- Extracts data from bank statements and tax returns
- Calculates key metrics: DSCR, revenue volatility, cash flow stability
- Computes leverage ratios and business stability scores
- Uses NumPy/Pandas for accurate financial mathematics

**Agent 2: Risk Assessor**
- Evaluates 6 different risk dimensions
- Classifies risk flags by severity (HIGH/MEDIUM)
- Identifies positive business signals
- Assigns overall risk level (LOW/MODERATE/HIGH)

**Agent 3: Credit Memo Generator**
- Uses GPT-4o-mini to write professional credit analysis
- Generates underwriting scores (0-100)
- Makes clear recommendations (APPROVE/CONDITIONS/DECLINE)
- Lists specific conditions when applicable

### Key Features

✅ **Speed**: 30-second complete analysis (99.9% faster than manual)  
✅ **Cost**: ~$0.50 in API costs per analysis (99.9% cheaper)  
✅ **Accuracy**: Industry-standard calculations with 97% test coverage  
✅ **Consistency**: Same methodology applied to every application  
✅ **Scalability**: Can process thousands daily with zero marginal cost  
✅ **Quality**: Professional credit memos for every decision  

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
│  • DSCR          • 6 Risk Flags  • Credit Memo    │
│  • Volatility    • Risk Level    • Score 0-100    │
│  • Stability     • Positive      • Recommendation │
│  • Debt Ratios   • Signals       • Conditions     │
└─────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────┐
│              SQLite Database (Local)                 │
│              Analysis history & results              │
└─────────────────────────────────────────────────────┘
```

---

## 🎯 Business Impact

### Problem Solved
Small business loans are economically unviable due to $500-1000 manual underwriting costs. This system makes them profitable by automating 99.9% of the work.

### Impact Metrics
- ⏱️ **Time**: 3-5 days → 30 seconds
- 💰 **Cost**: $500-1000 → $0.50
- 🎯 **Accuracy**: Industry-standard calculations
- 📈 **Scale**: Unlimited parallel processing
- ✅ **Quality**: Professional memos every time

### Enables New Business Models
- Makes $10K-$100K loans profitable
- Instant preliminary decisions
- High-volume lending programs
- Reduced bias in lending
- Scalable growth without linear costs

---

## 📊 Sample Results

Tested with 8 realistic business scenarios across different industries:

| Business | Industry | Loan | DSCR | Score | Decision |
|----------|----------|------|------|-------|----------|
| ABC Construction | Construction | $50K | 3.51 | 93 | ✅ APPROVE |
| Main Street Restaurant | Restaurant | $65K | 1.17 | 40 | ⚠️ CONDITIONS |
| Quick Cash Payday | Services | $100K | -0.04 | 19 | ❌ DECLINE |
| TechParts Mfg | Manufacturing | $75K | 4.42 | 97 | ✅ APPROVE |
| Ski Shop (Seasonal) | Retail | $40K | 1.66 | 65 | ⚠️ CONDITIONS |
| Family Dental | Healthcare | $120K | 0.02 | 29 | ❌ DECLINE |
| CloudSync Tech | Technology | $60K | 2.75 | 88 | ✅ APPROVE |
| Metro Courier | Transportation | $80K | -0.31 | 26 | ❌ DECLINE |

*All scenarios validated against industry lending standards*

---

## 🚀 Try It Yourself

### Live Demo
Visit [https://kaajai.netlify.app/](https://kaajai.netlify.app/) and try the **Main Street Restaurant** scenario:

1. **Business Details:**
   - Name: Main Street Restaurant
   - Industry: Restaurant
   - Age: 3 years

2. **Loan Request:**
   - Amount: $65,000
   - Rate: 10.5%
   - Term: 48 months
   - Existing Debt: $55,000

3. **Bank Statement Data:**
   ```
   Deposits: 28000, 32000, 25000, 31000, 27000, 33000, 29000, 26000, 34000, 30000, 28000, 31000
   Withdrawals: 24000, 27000, 23000, 26000, 25000, 28000, 26000, 24000, 29000, 27000, 25000, 27000
   NSF Fees: 3
   ```

4. **Tax Data (Optional but recommended):**
   ```
   Revenue: $350,000
   Expenses: $320,000
   Net Income: $30,000
   ```

5. **Submit for Analysis**

**Expected Result:**  
DSCR: 1.17, Score: ~40, Risk: HIGH, Decision: APPROVE_WITH_CONDITIONS

---

## 🔑 Technical Deep Dive

### DSCR (Debt Service Coverage Ratio)
The most critical metric for loan approval. Measures ability to service debt obligations.

```python
# Industry-standard calculation
new_loan_payment = calculate_payment(new_loan, rate, term)
existing_debt_payment = calculate_payment(existing_debt, rate, term)
total_monthly_payment = new_loan_payment + existing_debt_payment

DSCR = monthly_cash_flow / total_monthly_payment

# Decision thresholds
DSCR >= 1.25  → Approve
DSCR 1.0-1.25 → Conditional (safeguards required)
DSCR < 1.0    → Decline (insufficient cash flow)
```

### Underwriting Score Algorithm
Weighted composite score (0-100) across four factors:

| Factor | Weight | Calculation |
|--------|--------|-------------|
| Risk Level | 40% | LOW=40pts, MODERATE=25pts, HIGH=10pts |
| DSCR | 30% | Tiered: ≥1.75=30pts, ≥1.50=25pts, ≥1.25=20pts |
| Stability | 20% | Volatility + Age + NSF fees |
| Volatility | 10% | Revenue consistency measure |

### Risk Assessment Framework
Six automated risk checks with severity classification:

| Risk Flag | Severity | Trigger Condition |
|-----------|----------|-------------------|
| Low DSCR | HIGH | < 1.25 |
| Cash Flow Issues | HIGH | > 3 NSF fees |
| Negative Cash Flow | HIGH | Monthly loss |
| Unstable Revenue | MEDIUM | > 40% volatility |
| High Leverage | MEDIUM | > 50% debt-to-revenue |
| Declining Revenue | MEDIUM | < -10% trend |

---

## 🔍 Critical Bug Discovered & Fixed

During development, I discovered a **critical flaw** that exists in many automated underwriting systems:

### The Problem
Many systems calculate DSCR using **ONLY the new loan payment**, completely ignoring existing debt obligations. This creates dangerously optimistic risk assessments.

### Real Example - Main Street Restaurant

**❌ WRONG CALCULATION (New Loan Only):**
```
Monthly Cash Flow: $3,583
New Loan Payment: $1,664
DSCR = $3,583 / $1,664 = 2.15

Result: Looks safe, would likely be approved
```

**✅ CORRECT CALCULATION (Total Debt Service):**
```
Monthly Cash Flow: $3,583
New Loan Payment: $1,664
Existing Debt Payment: $1,408
Total Payment: $3,072

DSCR = $3,583 / $3,072 = 1.17

Result: Below 1.25 threshold, HIGH RISK
```

### Impact
A borrower with barely enough cash flow to cover all obligations would be approved as "safe" using the wrong calculation. The correct method shows they're at risk of default. **This is how lenders lose money.**

### My Solution
My system correctly calculates DSCR using total debt service (existing + new), matching real lending industry standards. This is validated in all 8 test scenarios.

---

## 💻 Technology Stack

**Backend:**
- Python 3.11 with FastAPI
- OpenAI GPT-4o-mini for AI analysis
- Pydantic for data validation
- NumPy/Pandas for financial calculations
- SQLite for data persistence
- Pytest with 97% test coverage

**Frontend:**
- React 18 + TypeScript
- Vite (modern build tool)
- TailwindCSS (utility-first styling)
- Axios (HTTP client)

**Infrastructure:**
- Render (backend - free tier)
- Netlify (frontend - free tier)
- GitHub (version control)
- Total hosting cost: $0/month

---

## 📁 Project Structure

```
kaaj-multi-agent-analyzer/
├── backend/
│   ├── agents/                      # Multi-agent implementation
│   │   ├── financial_analyzer.py    # DSCR, metrics calculation
│   │   ├── risk_assessor.py         # Risk flag identification
│   │   └── memo_generator.py        # Credit memo generation
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
├── TEST_SCENARIOS.md                # 8 validated test cases
├── DEPLOYMENT.md                    # Deployment instructions
└── README.md                        # This file
```

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
- End-to-end integration validated

### Test Scenarios
8 realistic scenarios in `TEST_SCENARIOS.md`:
- 3 APPROVE (strong businesses)
- 3 DECLINE (high risk/over-leveraged)
- 2 APPROVE_WITH_CONDITIONS (borderline)

Each includes complete financial data and expected outcomes.

---

## 🔐 Security & Privacy

- ✅ No sensitive data stored permanently
- ✅ SQLite for optional analysis history only
- ✅ HTTPS encryption end-to-end
- ✅ CORS properly configured
- ✅ No PII retention
- ✅ Stateless OpenAI API calls

---

## 🚀 Local Development

### Prerequisites
- Node.js 18+
- Python 3.11+
- OpenAI API key

### Quick Start

```bash
# Clone repository
git clone https://github.com/AyushJHANWAR03/KaajAI.git
cd KaajAI

# Backend setup
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
echo "OPENAI_API_KEY=your-key" > .env
uvicorn main:app --reload --port 8000

# Frontend setup (new terminal)
cd frontend
npm install
npm run dev
```

Open http://localhost:5173

---

## 📈 Future Enhancements

Potential expansion areas:

1. **Document Processing**
   - OCR for scanned documents
   - Balance sheet analysis
   - Profit & loss statements

2. **Advanced Features**
   - Industry benchmarking
   - Fraud detection
   - Trend forecasting

3. **Integration**
   - Banking APIs
   - Credit bureaus
   - CRM systems

4. **Workflow**
   - Multi-borrower support
   - Approval chains
   - Document versioning

---

## 👤 About

**Developer:** Ayush Jhanwar  
**GitHub:** [@AyushJHANWAR03](https://github.com/AyushJHANWAR03)  
**Inspiration:** [Kaaj AI](https://kaaj.ai) - AI-powered loan underwriting automation  

---

## 📄 License

MIT License - See LICENSE file

---

## 🙏 Acknowledgments

- Inspired by Kaaj AI's approach to loan underwriting automation
- Built with FastAPI, React, and OpenAI GPT-4
- Deployed on Render and Netlify free tiers
- Guided by real-world lending industry standards

---

**⭐ Star this repository if you found it useful!**

**🔗 Try the live demo:** [https://kaajai.netlify.app/](https://kaajai.netlify.app/)
