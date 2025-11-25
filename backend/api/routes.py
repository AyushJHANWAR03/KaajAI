"""FastAPI routes for loan analysis API."""
from fastapi import APIRouter, HTTPException, status
from typing import Dict
import logging

from api.schemas import (
    AnalyzeRequest,
    AnalysisResponse,
    ErrorResponse,
    HealthResponse
)
from agents.orchestrator import LoanAnalysisOrchestrator
from utils.config import settings

logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api", tags=["analysis"])

# Initialize orchestrator
orchestrator = LoanAnalysisOrchestrator(openai_api_key=settings.openai_api_key)


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint.

    Returns system status and loaded agents.
    """
    return {
        "status": "healthy",
        "version": "1.0.0",
        "agents_loaded": [
            "FinancialAnalyzerAgent",
            "RiskAssessorAgent",
            "MemoGeneratorAgent"
        ]
    }


@router.post(
    "/analyze",
    response_model=AnalysisResponse,
    responses={
        200: {"description": "Analysis completed successfully"},
        400: {"model": ErrorResponse, "description": "Invalid request data"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)
async def analyze_loan(request: AnalyzeRequest):
    """
    Analyze a loan package using multi-agent AI system.

    This endpoint orchestrates 3 AI agents:
    - Agent 3: Financial Analyzer - Calculates metrics
    - Agent 4: Risk Assessor - Identifies risks
    - Agent 5: Memo Generator - Creates credit memo

    Args:
        request: Loan application data including bank statements and business info

    Returns:
        Complete loan analysis with recommendation and credit memo
    """
    try:
        logger.info(f"Received analysis request for {request.business_name}")

        # Prepare extracted data
        extracted_data = {
            "bank_data": request.bank_data.model_dump(),
            "tax_data": request.tax_data.model_dump() if request.tax_data else {},
            "existing_debt": request.existing_debt
        }

        # Prepare business info
        business_info = {
            "business_name": request.business_name,
            "industry": request.industry,
            "loan_amount": request.loan_amount,
            "annual_interest_rate": request.annual_interest_rate,
            "term_months": request.term_months,
            "business_age_years": request.business_age_years
        }

        # Run orchestrator
        result = orchestrator.analyze_loan_package(extracted_data, business_info)

        if result.get("status") == "failed":
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result.get("error", "Analysis failed")
            )

        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in analyze_loan: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis failed: {str(e)}"
        )


@router.post("/quick-score")
async def quick_score_loan(request: AnalyzeRequest) -> Dict:
    """
    Quick scoring endpoint without full credit memo generation.

    Faster than full analysis - useful for batch processing.

    Args:
        request: Loan application data

    Returns:
        Underwriting score (0-100) only
    """
    try:
        extracted_data = {
            "bank_data": request.bank_data.model_dump(),
            "tax_data": request.tax_data.model_dump() if request.tax_data else {},
            "existing_debt": request.existing_debt
        }

        business_info = {
            "business_name": request.business_name,
            "industry": request.industry,
            "loan_amount": request.loan_amount,
            "annual_interest_rate": request.annual_interest_rate,
            "term_months": request.term_months,
            "business_age_years": request.business_age_years
        }

        score = orchestrator.quick_score(extracted_data, business_info)

        return {
            "business_name": request.business_name,
            "underwriting_score": score,
            "status": "completed"
        }

    except Exception as e:
        logger.error(f"Quick score failed: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Quick score failed: {str(e)}"
        )
