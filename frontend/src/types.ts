export interface BankData {
  monthly_deposits: number[];
  monthly_withdrawals: number[];
  nsf_fees: number;
  average_balance?: number;
  months_covered?: number;
}

export interface TaxData {
  gross_revenue: number;
  total_expenses: number;
  net_income: number;
  tax_year: number;
}

export interface AnalyzeRequest {
  business_name: string;
  industry: string;
  loan_amount: number;
  business_age_years: number;
  annual_interest_rate: number;
  term_months: number;
  bank_data: BankData;
  tax_data?: TaxData;
  existing_debt: number;
}

export interface FinancialMetrics {
  avg_monthly_revenue: number;
  revenue_volatility: number;
  avg_monthly_cash_flow: number;
  dscr: number;
  debt_to_revenue: number;
  annual_revenue: number;
  net_income: number;
  stability_score: number;
  total_debt: number;
  revenue_trend: number;
}

export interface RiskFlag {
  severity: string;
  flag: string;
  message: string;
}

export interface RiskAssessment {
  risk_level: 'LOW' | 'MODERATE' | 'HIGH';
  flags: RiskFlag[];
  positive_signals: string[];
}

export interface AnalysisResponse {
  status: string;
  business_info: {
    business_name: string;
    industry: string;
    loan_amount: number;
    annual_interest_rate: number;
    term_months: number;
    business_age_years: number;
  };
  financial_metrics: FinancialMetrics;
  risk_assessment: RiskAssessment;
  credit_memo: string;
  recommendation: 'APPROVE' | 'APPROVE_WITH_CONDITIONS' | 'DECLINE';
  underwriting_score: number;
  conditions: string[];
  decline_reasons: string[];
}
