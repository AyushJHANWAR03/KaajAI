"""Pydantic schemas for API request/response validation."""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum


class IndustryEnum(str, Enum):
    """Supported industries."""
    CONSTRUCTION = "Construction"
    MANUFACTURING = "Manufacturing"
    RETAIL = "Retail"
    RESTAURANT = "Restaurant"
    HEALTHCARE = "Healthcare"
    PROFESSIONAL_SERVICES = "Professional Services"
    TECHNOLOGY = "Technology"
    TRANSPORTATION = "Transportation"
    WHOLESALE = "Wholesale"
    OTHER = "Other"


class RiskLevelEnum(str, Enum):
    """Risk levels."""
    LOW = "LOW"
    MODERATE = "MODERATE"
    HIGH = "HIGH"


class RecommendationEnum(str, Enum):
    """Loan recommendations."""
    APPROVE = "APPROVE"
    APPROVE_WITH_CONDITIONS = "APPROVE_WITH_CONDITIONS"
    CONDITIONAL_APPROVAL = "CONDITIONAL_APPROVAL"
    DECLINE = "DECLINE"


# Request Schemas

class BankData(BaseModel):
    """Bank statement data."""
    monthly_deposits: List[float] = Field(..., description="List of monthly deposit amounts")
    monthly_withdrawals: List[float] = Field(..., description="List of monthly withdrawal amounts")
    nsf_fees: int = Field(default=0, description="Number of NSF fees")
    average_balance: Optional[float] = Field(default=None, description="Average account balance")
    months_covered: Optional[int] = Field(default=None, description="Number of months covered")


class TaxData(BaseModel):
    """Tax return data."""
    gross_revenue: float = Field(..., description="Annual gross revenue")
    total_expenses: float = Field(..., description="Annual total expenses")
    net_income: float = Field(..., description="Annual net income")
    tax_year: int = Field(..., description="Tax year")


class AnalyzeRequest(BaseModel):
    """Request schema for loan analysis."""
    business_name: str = Field(..., description="Business legal name")
    industry: str = Field(..., description="Business industry")
    loan_amount: float = Field(..., gt=0, description="Requested loan amount")
    business_age_years: int = Field(default=0, ge=0, description="Business age in years")
    annual_interest_rate: float = Field(default=0.08, gt=0, le=0.30, description="Annual interest rate")
    term_months: int = Field(default=60, gt=0, description="Loan term in months")

    # Financial data
    bank_data: BankData
    tax_data: Optional[TaxData] = None
    existing_debt: float = Field(default=0, ge=0, description="Existing debt amount")

    class Config:
        json_schema_extra = {
            "example": {
                "business_name": "ABC Construction LLC",
                "industry": "Construction",
                "loan_amount": 50000,
                "business_age_years": 5,
                "annual_interest_rate": 0.08,
                "term_months": 60,
                "bank_data": {
                    "monthly_deposits": [42000, 38000, 51000, 45000, 43000, 47000, 46000, 44000, 49000, 45000, 44000, 46000],
                    "monthly_withdrawals": [35000, 32000, 38000, 36000, 34000, 37000, 36000, 35000, 38000, 36000, 35000, 37000],
                    "nsf_fees": 1,
                    "average_balance": 15000,
                    "months_covered": 12
                },
                "tax_data": {
                    "gross_revenue": 540000,
                    "total_expenses": 420000,
                    "net_income": 120000,
                    "tax_year": 2024
                },
                "existing_debt": 80000
            }
        }


# Response Schemas

class FinancialMetrics(BaseModel):
    """Financial metrics calculated by Agent 3."""
    avg_monthly_revenue: float
    revenue_volatility: float
    avg_monthly_cash_flow: float
    dscr: float
    debt_to_revenue: float
    annual_revenue: float
    net_income: float
    stability_score: int
    total_debt: float
    revenue_trend: float


class RiskFlag(BaseModel):
    """Individual risk flag."""
    severity: str
    flag: str
    message: str


class RiskAssessment(BaseModel):
    """Risk assessment from Agent 4."""
    risk_level: RiskLevelEnum
    flags: List[RiskFlag]
    positive_signals: List[str]


class AnalysisResponse(BaseModel):
    """Complete analysis response."""
    status: str
    business_info: Dict[str, Any]
    financial_metrics: FinancialMetrics
    risk_assessment: RiskAssessment
    credit_memo: str
    recommendation: RecommendationEnum
    underwriting_score: int = Field(..., ge=0, le=100)
    conditions: List[str]
    decline_reasons: List[str]


class ErrorResponse(BaseModel):
    """Error response schema."""
    status: str = "failed"
    error: str
    business_info: Optional[Dict[str, Any]] = None


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    version: str = "1.0.0"
    agents_loaded: List[str]
