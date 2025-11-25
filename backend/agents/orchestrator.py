"""Orchestrator - Coordinates all AI agents in sequence."""
from typing import Dict, Optional
import logging

from agents.financial_analyzer import FinancialAnalyzerAgent
from agents.risk_assessor import RiskAssessorAgent
from agents.memo_generator import MemoGeneratorAgent

logger = logging.getLogger(__name__)


class LoanAnalysisOrchestrator:
    """
    Orchestrates the multi-agent loan analysis workflow.

    Agent Flow:
        Input Data
        ↓
        Agent 3: Financial Analyzer → Calculate metrics
        ↓
        Agent 4: Risk Assessor → Identify risks
        ↓
        Agent 5: Memo Generator → Generate memo
        ↓
        Final Output
    """

    def __init__(self, openai_api_key: Optional[str] = None):
        """
        Initialize orchestrator with all agents.

        Args:
            openai_api_key: OpenAI API key for memo generation
        """
        self.financial_analyzer = FinancialAnalyzerAgent()
        self.risk_assessor = RiskAssessorAgent()
        self.memo_generator = MemoGeneratorAgent(api_key=openai_api_key)

        logger.info("Loan Analysis Orchestrator initialized")

    def analyze_loan_package(
        self,
        extracted_data: Dict,
        business_info: Dict
    ) -> Dict:
        """
        Run complete loan analysis through all agents.

        Args:
            extracted_data: {
                "bank_data": {
                    "monthly_deposits": [...],
                    "monthly_withdrawals": [...],
                    "nsf_fees": int,
                    ...
                },
                "tax_data": {
                    "gross_revenue": float,
                    "total_expenses": float,
                    "net_income": float,
                    ...
                },
                "existing_debt": float
            }
            business_info: {
                "business_name": str,
                "industry": str,
                "loan_amount": float,
                "annual_interest_rate": float (default 0.08),
                "term_months": int (default 60),
                "business_age_years": int
            }

        Returns:
            Complete analysis result with all agent outputs
        """
        logger.info(f"Starting analysis for {business_info.get('business_name')}")

        try:
            # Prepare loan request data
            loan_request = {
                "loan_amount": business_info.get("loan_amount", 0),
                "annual_interest_rate": business_info.get("annual_interest_rate", 0.08),
                "term_months": business_info.get("term_months", 60),
                "business_age_years": business_info.get("business_age_years", 0),
            }

            # Agent 3: Financial Analysis
            logger.info("Running Agent 3: Financial Analyzer...")
            financial_metrics = self.financial_analyzer.analyze(
                extracted_data, loan_request
            )
            logger.info("✓ Financial metrics calculated")

            # Agent 4: Risk Assessment
            logger.info("Running Agent 4: Risk Assessor...")
            risk_assessment = self.risk_assessor.assess(
                financial_metrics, extracted_data
            )
            logger.info("✓ Risk assessment completed")

            # Agent 5: Memo Generation
            logger.info("Running Agent 5: Memo Generator...")
            memo_output = self.memo_generator.generate(
                business_info, financial_metrics, risk_assessment
            )
            logger.info("✓ Credit memo generated")

            # Compile final output
            result = {
                "status": "completed",
                "business_info": business_info,
                "financial_metrics": financial_metrics["metrics"],
                "risk_assessment": risk_assessment["risk_assessment"],
                "credit_memo": memo_output["credit_memo_output"]["credit_memo"],
                "recommendation": memo_output["credit_memo_output"]["recommendation"],
                "underwriting_score": memo_output["credit_memo_output"]["underwriting_score"],
                "conditions": memo_output["credit_memo_output"].get("conditions", []),
                "decline_reasons": memo_output["credit_memo_output"].get("reasons", []),
            }

            logger.info(f"Analysis complete - Score: {result['underwriting_score']}, Decision: {result['recommendation']}")
            return result

        except Exception as e:
            logger.error(f"Analysis failed: {str(e)}", exc_info=True)
            return {
                "status": "failed",
                "error": str(e),
                "business_info": business_info
            }

    def quick_score(self, extracted_data: Dict, business_info: Dict) -> int:
        """
        Quick scoring without full memo generation (faster).

        Useful for batch processing or pre-screening.

        Args:
            extracted_data: Bank and tax data
            business_info: Business metadata

        Returns:
            Underwriting score (0-100)
        """
        try:
            loan_request = {
                "loan_amount": business_info.get("loan_amount", 0),
                "annual_interest_rate": business_info.get("annual_interest_rate", 0.08),
                "term_months": business_info.get("term_months", 60),
                "business_age_years": business_info.get("business_age_years", 0),
            }

            # Run agents 3 & 4 only
            financial_metrics = self.financial_analyzer.analyze(extracted_data, loan_request)
            risk_assessment = self.risk_assessor.assess(financial_metrics, extracted_data)

            # Calculate score without LLM
            from agents.memo_generator import calculate_underwriting_score

            metrics = financial_metrics["metrics"]
            assessment = risk_assessment["risk_assessment"]

            score = calculate_underwriting_score(
                risk_level=assessment["risk_level"],
                dscr=metrics["dscr"],
                stability_score=metrics["stability_score"],
                revenue_volatility=metrics["revenue_volatility"]
            )

            return score

        except Exception as e:
            logger.error(f"Quick score failed: {str(e)}")
            return 0
