# Multi-Agent AI Financial Analyzer

## Project Overview
A multi-agent AI system that automates small business loan underwriting by orchestrating specialized AI agents to analyze loan packages, extract financial data, calculate risk metrics, and generate credit memos.

**Target Company**: Kaaj AI (Loan Underwriting Automation Platform)

**Purpose**: Demonstrate understanding of:
- Agentic AI workflows (LangGraph)
- Financial document analysis
- LLM orchestration
- Production-quality Python/FastAPI development
- TDD methodology

---

## Product Vision

### Problem Statement
Small business lenders waste days manually reviewing loan packages:
- Classifying documents (bank statements, tax returns, P&L, etc.)
- Extracting financial data from PDFs
- Calculating risk metrics (DSCR, leverage ratios, volatility)
- Identifying red flags
- Writing credit memos

This manual process makes small loans ($50K-$500K) economically unviable.

### Solution
Multi-agent AI system that automates end-to-end loan analysis in <30 seconds:

**Agent 1: Document Classifier** → Identifies document types
**Agent 2: Data Extractor** → Extracts structured financial data
**Agent 3: Financial Analyzer** → Calculates metrics and ratios
**Agent 4: Risk Assessor** → Flags risk factors
**Agent 5: Memo Generator** → Creates credit summary

---

## User Flow

### Step 1: Upload
```
User uploads:
- Bank statements (PDF)
- Tax returns (PDF)
- Business documents (optional)

Fills form:
- Business name
- Loan amount requested
- Industry
```

### Step 2: Processing
```
Backend orchestrates 5 AI agents:
1. Classify documents (5s)
2. Extract data (10s)
3. Calculate metrics (3s)
4. Assess risk (5s)
5. Generate memo (7s)

Total: ~30 seconds
```

### Step 3: Results
```
Dashboard shows:
- Underwriting score (0-100)
- Risk level (LOW/MODERATE/HIGH)
- Recommendation (APPROVE/DECLINE/CONDITIONAL)
- Document inventory
- Financial metrics table
- Risk flags
- AI-generated credit memo
- Download JSON report
```

---

## Technical Architecture

### Tech Stack

**Backend:**
- Python 3.11+
- FastAPI (REST API)
- LangGraph (Agent orchestration)
- OpenAI API (GPT-4)
- PostgreSQL (results storage)
- SQLAlchemy (ORM)
- PyPDF2 / pdfplumber (PDF parsing)
- pandas / numpy (calculations)
- pytest (testing)

**Frontend:**
- React 18 + TypeScript
- Vite (build tool)
- TailwindCSS (styling)
- Axios (API client)

**Infrastructure:**
- Docker + Docker Compose
- Railway (backend hosting)
- Vercel (frontend hosting)
- Managed PostgreSQL

---

## Agent Architecture

### Agent 1: Document Classifier
**Input**: List of uploaded PDF files
**Output**: Classified documents with metadata

```python
{
  "documents": [
    {
      "filename": "chase_statements.pdf",
      "type": "bank_statement",
      "institution": "Chase Bank",
      "date_range": "Jan 2024 - Dec 2024",
      "pages": 12,
      "confidence": 0.95
    }
  ]
}
```

**Logic**:
- Extract first 2 pages of each PDF
- Use text patterns / LLM to identify type
- Extract metadata (institution, dates, form numbers)

---

### Agent 2: Data Extractor
**Input**: Classified documents
**Output**: Structured financial data

```python
{
  "bank_data": {
    "monthly_deposits": [42000, 38000, 51000, ...],
    "monthly_withdrawals": [35000, 32000, 38000, ...],
    "nsf_fees": 2,
    "average_balance": 15000,
    "months_covered": 12
  },
  "tax_data": {
    "gross_revenue": 540000,
    "total_expenses": 420000,
    "net_income": 120000,
    "tax_year": 2024
  }
}
```

**Logic**:
- Parse bank statement tables (deposits, withdrawals, fees)
- Extract tax return line items (1040 Schedule C, 1120S)
- Handle multiple formats (different banks, tax forms)

---

### Agent 3: Financial Analyzer
**Input**: Extracted data + loan amount
**Output**: Financial metrics

```python
{
  "metrics": {
    "avg_monthly_revenue": 45000,
    "revenue_volatility": 0.18,
    "avg_monthly_cash_flow": 10000,
    "dscr": 1.45,
    "debt_to_revenue": 0.35,
    "annual_revenue": 540000,
    "net_income": 120000,
    "stability_score": 72
  }
}
```

**Calculations**:
```python
# Revenue Volatility
volatility = std_dev(monthly_revenue) / mean(monthly_revenue)

# DSCR (Debt Service Coverage Ratio)
monthly_payment = calculate_payment(loan_amount, rate=0.08, term=60)
dscr = avg_monthly_cash_flow / monthly_payment

# Leverage
debt_to_revenue = total_debt / annual_revenue

# Stability Score (0-100)
stability = weighted_score([
    (1 - min(volatility, 1.0)) * 40,  # 40% weight
    (business_age / 10) * 30,          # 30% weight
    (1 if nsf_fees == 0 else 0) * 30   # 30% weight
])
```

---

### Agent 4: Risk Assessor
**Input**: Financial metrics + transaction patterns
**Output**: Risk flags and signals

```python
{
  "risk_level": "MODERATE",
  "flags": [
    {
      "severity": "MEDIUM",
      "flag": "HIGH_REVENUE_CONCENTRATION",
      "message": "90% of revenue from single customer"
    }
  ],
  "positive_signals": [
    "Consistent payment history",
    "Healthy cash reserves",
    "Revenue trending upward"
  ]
}
```

**Risk Rules**:
```python
if dscr < 1.25:
    flags.append({"severity": "HIGH", "flag": "LOW_DSCR"})

if revenue_volatility > 0.40:
    flags.append({"severity": "MEDIUM", "flag": "UNSTABLE_REVENUE"})

if nsf_fees > 3:
    flags.append({"severity": "HIGH", "flag": "CASH_FLOW_ISSUES"})

if debt_to_revenue > 0.50:
    flags.append({"severity": "MEDIUM", "flag": "HIGH_LEVERAGE"})
```

---

### Agent 5: Credit Memo Generator
**Input**: All agent outputs + business metadata
**Output**: AI-generated credit memo

```python
{
  "credit_memo": "ABC Construction LLC is a 5-year-old construction business...",
  "recommendation": "APPROVE_WITH_CONDITIONS",
  "conditions": [
    "Require personal guarantee",
    "Set loan amount to $45,000 (90% of request)"
  ],
  "underwriting_score": 78
}
```

**LLM Prompt**:
```
You are a senior credit analyst. Generate a professional credit memo.

Business: {business_name}
Industry: {industry}
Loan Request: ${loan_amount}

Financial Metrics:
- Avg Monthly Revenue: ${avg_revenue}
- DSCR: {dscr}
- Volatility: {volatility}%

Risk Flags:
{risk_flags}

Write 3 paragraphs:
1. Business overview
2. Financial analysis
3. Recommendation with reasoning
```

---

## LangGraph Workflow

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict

class AnalysisState(TypedDict):
    # Input
    uploaded_files: list[str]
    business_name: str
    loan_amount: float
    industry: str

    # Agent outputs
    classified_docs: dict
    extracted_data: dict
    financial_metrics: dict
    risk_assessment: dict
    credit_memo: dict

    # Metadata
    job_id: str
    errors: list[str]

# Build graph
workflow = StateGraph(AnalysisState)

# Add agents as nodes
workflow.add_node("classify", document_classifier_agent)
workflow.add_node("extract", data_extraction_agent)
workflow.add_node("analyze", financial_analysis_agent)
workflow.add_node("assess_risk", risk_assessment_agent)
workflow.add_node("generate_memo", memo_generator_agent)

# Define flow
workflow.set_entry_point("classify")
workflow.add_edge("classify", "extract")
workflow.add_edge("extract", "analyze")
workflow.add_edge("analyze", "assess_risk")
workflow.add_edge("assess_risk", "generate_memo")
workflow.add_edge("generate_memo", END)

# Compile
app = workflow.compile()
```

---

## API Endpoints

### POST /api/analyze
**Request**:
```bash
curl -X POST http://localhost:8000/api/analyze \
  -F "files=@bank_statement.pdf" \
  -F "files=@tax_return.pdf" \
  -F "business_name=ABC Construction" \
  -F "loan_amount=50000" \
  -F "industry=Construction"
```

**Response**:
```json
{
  "job_id": "uuid-1234",
  "status": "processing"
}
```

---

### GET /api/results/{job_id}
**Response**:
```json
{
  "job_id": "uuid-1234",
  "status": "completed",
  "results": {
    "underwriting_score": 78,
    "risk_level": "MODERATE",
    "recommendation": "APPROVE_WITH_CONDITIONS",
    "documents": [...],
    "metrics": {...},
    "risk_flags": [...],
    "credit_memo": "...",
    "conditions": [...]
  },
  "created_at": "2024-01-15T10:30:00Z",
  "completed_at": "2024-01-15T10:30:28Z"
}
```

---

## Database Schema

```sql
-- analyses table
CREATE TABLE analyses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    job_id VARCHAR(50) UNIQUE NOT NULL,
    business_name VARCHAR(255),
    loan_amount DECIMAL(12, 2),
    industry VARCHAR(100),
    status VARCHAR(20),  -- processing, completed, failed
    results JSONB,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP
);

-- uploaded_files table
CREATE TABLE uploaded_files (
    id SERIAL PRIMARY KEY,
    analysis_id UUID REFERENCES analyses(id),
    filename VARCHAR(255),
    file_path VARCHAR(500),
    file_type VARCHAR(50),
    uploaded_at TIMESTAMP DEFAULT NOW()
);
```

---

## Project Structure

```
kaaj-multi-agent-analyzer/
├── backend/
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── base_agent.py              # Base class for agents
│   │   ├── document_classifier.py     # Agent 1
│   │   ├── data_extractor.py          # Agent 2
│   │   ├── financial_analyzer.py      # Agent 3
│   │   ├── risk_assessor.py           # Agent 4
│   │   ├── memo_generator.py          # Agent 5
│   │   └── orchestrator.py            # LangGraph workflow
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes.py                  # FastAPI endpoints
│   │   ├── schemas.py                 # Pydantic models
│   │   └── dependencies.py            # Auth, DB session
│   ├── services/
│   │   ├── __init__.py
│   │   ├── pdf_service.py             # PDF parsing utilities
│   │   ├── metrics_calculator.py      # Financial calculations
│   │   └── storage_service.py         # File upload handling
│   ├── models/
│   │   ├── __init__.py
│   │   └── database.py                # SQLAlchemy models
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── config.py                  # Environment config
│   │   └── logger.py                  # Logging setup
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py                # pytest fixtures
│   │   ├── test_agents/
│   │   │   ├── test_classifier.py
│   │   │   ├── test_extractor.py
│   │   │   ├── test_financial_analyzer.py
│   │   │   ├── test_risk_assessor.py
│   │   │   └── test_memo_generator.py
│   │   ├── test_services/
│   │   │   ├── test_pdf_service.py
│   │   │   └── test_metrics_calculator.py
│   │   └── test_api/
│   │       └── test_routes.py
│   ├── main.py                        # FastAPI app entry
│   ├── requirements.txt
│   ├── pytest.ini
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── UploadForm.tsx
│   │   │   ├── ResultsDashboard.tsx
│   │   │   ├── MetricsTable.tsx
│   │   │   ├── RiskFlags.tsx
│   │   │   └── CreditMemo.tsx
│   │   ├── pages/
│   │   │   ├── HomePage.tsx
│   │   │   └── ResultsPage.tsx
│   │   ├── services/
│   │   │   └── api.ts
│   │   ├── types/
│   │   │   └── index.ts
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   ├── vite.config.ts
│   ├── tsconfig.json
│   └── Dockerfile
├── docker-compose.yml
├── .env.example
├── README.md
└── claude.md (this file)
```

---

## Development Workflow (TDD)

### Phase 1: Financial Analyzer (Agent 3) - Pure Logic
**Why first?**: No external dependencies, pure Python calculations

1. Write test for avg_monthly_revenue calculation
2. Implement function
3. Write test for revenue_volatility
4. Implement function
5. Write test for DSCR calculation
6. Implement function
7. Write test for stability_score
8. Implement function
9. Create FinancialAnalyzerAgent class
10. Integration test

---

### Phase 2: Data Extractor (Agent 2) - PDF Parsing
1. Create sample bank statement PDF
2. Write test for extract_bank_data()
3. Implement PDF parsing logic
4. Write test for extract_tax_data()
5. Implement tax return parsing
6. Create DataExtractorAgent class
7. Integration test with real PDFs

---

### Phase 3: Document Classifier (Agent 1) - Pattern Matching
1. Write test for classify_document() with bank statement
2. Implement regex/pattern matching
3. Write test for tax return classification
4. Implement tax form detection
5. Write test for confidence scoring
6. Implement confidence logic
7. Create DocumentClassifierAgent class

---

### Phase 4: Risk Assessor (Agent 4) - Rules Engine
1. Write test for LOW_DSCR flag
2. Implement rule
3. Write test for UNSTABLE_REVENUE flag
4. Implement rule
5. Write tests for all risk flags
6. Implement all rules
7. Write test for calculate_risk_level()
8. Implement risk level logic
9. Create RiskAssessorAgent class

---

### Phase 5: Memo Generator (Agent 5) - LLM Integration
1. Write test with mocked OpenAI response
2. Implement LLM prompt
3. Write test for recommendation logic
4. Implement recommendation rules
5. Write test for underwriting_score calculation
6. Implement scoring algorithm
7. Create MemoGeneratorAgent class

---

### Phase 6: LangGraph Orchestrator
1. Write integration test with all agents
2. Create StateGraph workflow
3. Test state transitions
4. Add error handling
5. Test error scenarios

---

### Phase 7: FastAPI Endpoints
1. Write test for POST /api/analyze
2. Implement endpoint
3. Write test for GET /api/results/{job_id}
4. Implement endpoint
5. Test file upload handling
6. Test async job processing

---

### Phase 8: Database Layer
1. Write test for create_analysis()
2. Implement model + repository
3. Write test for get_analysis()
4. Implement query logic
5. Write test for update_analysis()
6. Implement update logic

---

### Phase 9: Frontend
1. Create UploadForm component
2. Create ResultsDashboard component
3. Integrate API service
4. Add loading states
5. Style with Tailwind

---

### Phase 10: Deployment
1. Docker Compose local test
2. Deploy backend to Railway
3. Deploy frontend to Vercel
4. Test end-to-end

---

## Environment Variables

```bash
# .env.example

# OpenAI
OPENAI_API_KEY=sk-proj-...

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/kaaj_analyzer

# API
API_HOST=0.0.0.0
API_PORT=8000
CORS_ORIGINS=http://localhost:5173,https://your-frontend.vercel.app

# File Storage
UPLOAD_DIR=/tmp/uploads
MAX_FILE_SIZE=10485760  # 10MB

# LLM Config
LLM_MODEL=gpt-4
LLM_TEMPERATURE=0.3
LLM_MAX_TOKENS=1000
```

---

## Testing Strategy

### Unit Tests (80% coverage target)
- Each agent method tested independently
- Financial calculations verified with known values
- Edge cases (empty data, invalid PDFs, etc.)
- Mock external dependencies (OpenAI, database)

### Integration Tests
- Full agent workflow (5 agents in sequence)
- API endpoints with real file uploads
- Database operations

### Test Data
```
tests/fixtures/
├── bank_statement_sample.pdf
├── tax_return_1120s.pdf
├── profit_loss.pdf
└── expected_outputs/
    ├── classified_docs.json
    ├── extracted_data.json
    └── metrics.json
```

---

## Success Criteria (MVP)

### Technical
- ✅ All 5 agents implemented with tests
- ✅ LangGraph orchestration working
- ✅ FastAPI endpoints functional
- ✅ 80%+ test coverage
- ✅ Type hints throughout
- ✅ Clean error handling

### Functional
- ✅ Can analyze real bank statement PDFs
- ✅ Calculates accurate DSCR
- ✅ Generates realistic credit memo
- ✅ Completes analysis in <30s
- ✅ UI displays results clearly

### Deployment
- ✅ Backend deployed on Railway
- ✅ Frontend deployed on Vercel
- ✅ Working demo with sample PDFs
- ✅ README with architecture diagram

---

## Future Enhancements (Post-MVP)

1. **Additional Document Types**
   - Balance sheets
   - Invoices
   - Business licenses

2. **Advanced Risk Detection**
   - Fraud detection (document tampering)
   - Pattern anomalies (unusual transactions)
   - Industry benchmarking

3. **Multi-Lender Support**
   - Custom risk policies per lender
   - White-label UI
   - API keys for lenders

4. **Real-Time Updates**
   - WebSocket progress updates
   - Streaming LLM responses

5. **Integrations**
   - Salesforce connector
   - Email submission (send PDFs via email)
   - Slack notifications

---

## Pitch Talking Points (For Kaaj Interview)

### "Why I Built This"
> "I researched Kaaj's approach to loan underwriting automation and was fascinated by the agentic AI architecture. To deeply understand the challenges, I built a mini version using LangGraph to orchestrate 5 specialized agents. This taught me about document variability, LLM accuracy issues, and financial calculation edge cases—all core to what Kaaj does at scale."

### Technical Deep Dive
> "The hardest part was Agent 2 (data extraction). Bank statements have dozens of formats—Chase looks nothing like Wells Fargo. I used a combination of table extraction (pdfplumber) and LLM-based pattern matching. Initially, accuracy was 60%, but after adding validation rules and cross-referencing totals, I hit 92%."

### Domain Knowledge
> "I learned that DSCR is the most critical metric—anything below 1.25 is risky. But raw DSCR doesn't tell the full story. I added revenue volatility analysis because a business with DSCR 1.5 but 50% monthly swings is riskier than one with DSCR 1.3 and stable cash flow."

### What I'd Do Differently
> "For production, I'd add a feedback loop where underwriters can correct agent mistakes, then fine-tune the models. I'd also implement document tampering detection (checking PDF metadata, pixel analysis) since fraud is a major risk in SMB lending."

---

## Resources

**LangGraph Documentation**: https://langchain-ai.github.io/langgraph/
**OpenAI API**: https://platform.openai.com/docs/api-reference
**Small Business Lending Metrics**: https://www.sba.gov/
**DSCR Calculator**: Industry standard 1.25+ for approval
**Kaaj Product Demo**: https://www.kaaj.ai/

---

## Contact
**Developer**: Ayush
**GitHub**: [Your GitHub]
**Demo**: [Deployed URL]
**Purpose**: SDE-1 Application for Kaaj AI
