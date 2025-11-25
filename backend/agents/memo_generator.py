"""Memo Generator Agent - Generates credit memos using LLM."""
from typing import Dict, List, Optional
from openai import OpenAI
import os


def determine_recommendation(
    risk_level: str,
    dscr: float,
    stability_score: int,
    flags: List[Dict]
) -> Dict:
    """
    Determine loan recommendation based on risk metrics.

    Logic:
        - HIGH risk + critical flags → DECLINE
        - HIGH risk but manageable → APPROVE_WITH_CONDITIONS
        - MODERATE risk → APPROVE_WITH_CONDITIONS
        - LOW risk + strong metrics → APPROVE

    Args:
        risk_level: "LOW", "MODERATE", or "HIGH"
        dscr: Debt Service Coverage Ratio
        stability_score: Business stability score (0-100)
        flags: List of risk flags

    Returns:
        Dict with decision, conditions/reasons
    """
    high_severity_flags = [f for f in flags if f.get("severity") == "HIGH"]

    # DECLINE cases
    if risk_level == "HIGH" and len(high_severity_flags) >= 2:
        return {
            "decision": "DECLINE",
            "reasons": [
                "Multiple critical risk factors identified",
                f"DSCR of {dscr:.2f} indicates insufficient debt service capacity" if dscr < 1.0 else None,
                "High volatility or cash flow concerns"
            ],
            "conditions": []
        }

    if dscr < 1.0:
        return {
            "decision": "DECLINE",
            "reasons": [
                f"DSCR of {dscr:.2f} is below 1.0 minimum threshold",
                "Insufficient cash flow to service debt"
            ],
            "conditions": []
        }

    # APPROVE WITH CONDITIONS cases
    if risk_level == "HIGH" or risk_level == "MODERATE":
        conditions = []

        if dscr < 1.35:
            conditions.append("Require personal guarantee from business owner")

        if stability_score < 70:
            conditions.append("Require quarterly financial reporting")

        if any(f.get("flag") == "UNSTABLE_REVENUE" for f in flags):
            conditions.append("Monitor cash flow closely for first 12 months")

        if any(f.get("flag") == "HIGH_LEVERAGE" for f in flags):
            conditions.append("Reduce loan amount to 80% of request")

        if any(f.get("flag") == "CASH_FLOW_ISSUES" for f in flags):
            conditions.append("Establish cash reserve requirement of 3 months expenses")

        if not conditions:
            conditions.append("Standard terms with enhanced monitoring")

        return {
            "decision": "APPROVE_WITH_CONDITIONS",
            "conditions": conditions,
            "reasons": []
        }

    # APPROVE cases (LOW risk)
    return {
        "decision": "APPROVE",
        "conditions": [],
        "reasons": []
    }


def calculate_underwriting_score(
    risk_level: str,
    dscr: float,
    stability_score: int,
    revenue_volatility: float
) -> int:
    """
    Calculate overall underwriting score (0-100).

    Components:
        - Risk level (40% weight)
        - DSCR (30% weight)
        - Stability score (20% weight)
        - Revenue volatility (10% weight)

    Args:
        risk_level: "LOW", "MODERATE", or "HIGH"
        dscr: Debt Service Coverage Ratio
        stability_score: Business stability (0-100)
        revenue_volatility: Revenue coefficient of variation

    Returns:
        Underwriting score from 0-100
    """
    # Risk level score (40 points)
    risk_scores = {"LOW": 40, "MODERATE": 25, "HIGH": 10}
    risk_score = risk_scores.get(risk_level, 10)

    # DSCR score (30 points)
    if dscr >= 1.75:
        dscr_score = 30
    elif dscr >= 1.50:
        dscr_score = 25
    elif dscr >= 1.25:
        dscr_score = 20
    elif dscr >= 1.0:
        dscr_score = 10
    else:
        dscr_score = 0

    # Stability score contribution (20 points)
    stability_contribution = (stability_score / 100) * 20

    # Volatility score (10 points, inverse)
    volatility_score = max(0, (1 - min(revenue_volatility, 1.0)) * 10)

    # Total
    total = risk_score + dscr_score + stability_contribution + volatility_score
    return int(max(0, min(100, total)))


def build_credit_memo_prompt(
    business_info: Dict,
    metrics: Dict,
    risk_assessment: Dict,
    recommendation: Dict
) -> str:
    """
    Build the prompt for LLM credit memo generation.

    Args:
        business_info: Business name, industry, loan amount
        metrics: Financial metrics
        risk_assessment: Risk flags and signals
        recommendation: Loan decision and conditions

    Returns:
        Formatted prompt string for GPT-4
    """
    business_name = business_info.get("business_name", "Unknown Business")
    industry = business_info.get("industry", "Unknown")
    loan_amount = business_info.get("loan_amount", 0)

    avg_revenue = metrics.get("avg_monthly_revenue", 0)
    dscr = metrics.get("dscr", 0)
    volatility = metrics.get("revenue_volatility", 0)
    stability = metrics.get("stability_score", 0)

    risk_level = risk_assessment.get("risk_level", "UNKNOWN")
    flags = risk_assessment.get("flags", [])
    positive_signals = risk_assessment.get("positive_signals", [])

    decision = recommendation.get("decision", "PENDING")
    conditions = recommendation.get("conditions", [])
    reasons = recommendation.get("reasons", [])

    prompt = f"""You are a senior credit analyst at a commercial lending institution. Generate a professional credit memo for the following small business loan application.

**BUSINESS INFORMATION:**
- Business Name: {business_name}
- Industry: {industry}
- Loan Amount Requested: ${loan_amount:,}

**FINANCIAL ANALYSIS:**
- Average Monthly Revenue: ${avg_revenue:,}
- Debt Service Coverage Ratio (DSCR): {dscr:.2f}
- Revenue Volatility: {volatility:.1%}
- Business Stability Score: {stability}/100

**RISK ASSESSMENT:**
- Overall Risk Level: {risk_level}

Risk Flags:
{chr(10).join([f"- [{f.get('severity')}] {f.get('message', '')}" for f in flags]) if flags else "- None identified"}

Positive Signals:
{chr(10).join([f"- {signal}" for signal in positive_signals]) if positive_signals else "- None identified"}

**RECOMMENDATION:**
- Decision: {decision}
{"- Conditions:" + chr(10) + chr(10).join([f"  * {c}" for c in conditions]) if conditions else ""}
{"- Reasons for Decline:" + chr(10) + chr(10).join([f"  * {r}" for r in reasons if r]) if reasons else ""}

**INSTRUCTIONS:**
Write a professional 3-paragraph credit memo:

1. **Business Overview** (2-3 sentences): Briefly describe the business, loan purpose, and key business characteristics.

2. **Financial Analysis** (3-4 sentences): Analyze the financial metrics. Discuss DSCR, revenue stability, cash flow, and any notable strengths or weaknesses. Be specific with numbers.

3. **Recommendation** (2-3 sentences): State your recommendation clearly (APPROVE, APPROVE WITH CONDITIONS, or DECLINE). Explain the reasoning. If conditional approval, list specific conditions. If decline, explain why.

Write in a professional, objective tone. Be concise but thorough. Use specific numbers from the analysis."""

    return prompt


class MemoGeneratorAgent:
    """
    Agent 5: Credit Memo Generator

    Uses LLM (GPT-4) to generate professional credit memos based on:
        - Business information
        - Financial metrics
        - Risk assessment
        - Recommendation logic
    """

    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o-mini"):
        """
        Initialize the Memo Generator Agent.

        Args:
            api_key: OpenAI API key (if None, will try env var)
            model: OpenAI model to use
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        self.client = None

        if self.api_key:
            try:
                self.client = OpenAI(api_key=self.api_key)
            except Exception as e:
                print(f"Warning: Failed to initialize OpenAI client: {e}")
                self.client = None

    def generate(
        self,
        business_info: Dict,
        financial_metrics: Dict,
        risk_assessment: Dict
    ) -> Dict:
        """
        Generate credit memo and recommendation.

        Args:
            business_info: {business_name, industry, loan_amount, ...}
            financial_metrics: Output from Financial Analyzer Agent
            risk_assessment: Output from Risk Assessor Agent

        Returns:
            Dict with "credit_memo_output" containing:
                - credit_memo: AI-generated memo text
                - recommendation: Decision (APPROVE/DECLINE/etc.)
                - underwriting_score: Score 0-100
                - conditions: List of conditions (if applicable)
                - reasons: List of decline reasons (if applicable)
        """
        # Extract metrics
        metrics = financial_metrics.get("metrics", {})
        assessment = risk_assessment.get("risk_assessment", {})

        risk_level = assessment.get("risk_level", "UNKNOWN")
        flags = assessment.get("flags", [])
        positive_signals = assessment.get("positive_signals", [])

        dscr = metrics.get("dscr", 0)
        stability_score = metrics.get("stability_score", 0)
        revenue_volatility = metrics.get("revenue_volatility", 0)

        # Determine recommendation
        recommendation = determine_recommendation(
            risk_level=risk_level,
            dscr=dscr,
            stability_score=stability_score,
            flags=flags
        )

        # Calculate underwriting score
        underwriting_score = calculate_underwriting_score(
            risk_level=risk_level,
            dscr=dscr,
            stability_score=stability_score,
            revenue_volatility=revenue_volatility
        )

        # Generate credit memo using LLM
        if self.client:
            try:
                prompt = build_credit_memo_prompt(
                    business_info, metrics, assessment, recommendation
                )

                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a senior credit analyst with 15+ years experience in small business lending."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.3,
                    max_tokens=1000
                )

                credit_memo = response.choices[0].message.content

            except Exception as e:
                # Fallback if OpenAI fails
                credit_memo = self._generate_fallback_memo(
                    business_info, metrics, assessment, recommendation
                )
                credit_memo += f"\n\n[Note: LLM generation failed: {str(e)}]"
        else:
            # No OpenAI client, use fallback
            credit_memo = self._generate_fallback_memo(
                business_info, metrics, assessment, recommendation
            )

        return {
            "credit_memo_output": {
                "credit_memo": credit_memo,
                "recommendation": recommendation["decision"],
                "underwriting_score": underwriting_score,
                "conditions": recommendation.get("conditions", []),
                "reasons": recommendation.get("reasons", [])
            }
        }

    def _generate_fallback_memo(
        self,
        business_info: Dict,
        metrics: Dict,
        assessment: Dict,
        recommendation: Dict
    ) -> str:
        """
        Generate a simple template-based memo when LLM is unavailable.

        Args:
            business_info: Business details
            metrics: Financial metrics
            assessment: Risk assessment
            recommendation: Loan recommendation

        Returns:
            Template-based credit memo
        """
        business_name = business_info.get("business_name", "Unknown Business")
        industry = business_info.get("industry", "Unknown")
        loan_amount = business_info.get("loan_amount", 0)

        avg_revenue = metrics.get("avg_monthly_revenue", 0)
        dscr = metrics.get("dscr", 0)
        risk_level = assessment.get("risk_level", "UNKNOWN")

        decision = recommendation.get("decision", "PENDING")

        memo = f"""CREDIT MEMO - {business_name}

BUSINESS OVERVIEW:
{business_name} operates in the {industry} sector and is requesting a loan of ${loan_amount:,}. Based on financial document analysis, the business demonstrates average monthly revenue of ${avg_revenue:,}.

FINANCIAL ANALYSIS:
The applicant's Debt Service Coverage Ratio (DSCR) of {dscr:.2f} {'meets' if dscr >= 1.25 else 'falls below'} industry standards for approval. Overall risk assessment indicates {risk_level} risk level. {'Positive indicators include strong financial metrics and stable operations.' if risk_level == 'LOW' else 'Some concerns identified that require attention.'}

RECOMMENDATION:
Based on the comprehensive analysis, the recommendation is to {decision.replace('_', ' ')}."""

        if recommendation.get("conditions"):
            memo += "\n\nCONDITIONS:\n" + "\n".join([f"- {c}" for c in recommendation["conditions"]])

        if recommendation.get("reasons"):
            memo += "\n\nREASONS:\n" + "\n".join([f"- {r}" for r in recommendation["reasons"] if r])

        return memo
