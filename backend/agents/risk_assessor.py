"""Risk Assessor Agent - Identifies risk flags and signals."""
from typing import Dict, List, Optional


def check_low_dscr(dscr: float) -> Optional[Dict]:
    """
    Check if DSCR is below safe threshold.

    Industry standard: DSCR >= 1.25 for approval

    Args:
        dscr: Debt Service Coverage Ratio

    Returns:
        Risk flag dict if DSCR < 1.25, None otherwise
    """
    if dscr < 1.25:
        return {
            "severity": "HIGH",
            "flag": "LOW_DSCR",
            "message": f"DSCR of {dscr:.2f} is below 1.25 minimum threshold"
        }
    return None


def check_unstable_revenue(volatility: float) -> Optional[Dict]:
    """
    Check if revenue volatility is too high.

    Args:
        volatility: Revenue coefficient of variation

    Returns:
        Risk flag dict if volatility > 0.40, None otherwise
    """
    if volatility > 0.40:
        return {
            "severity": "MEDIUM",
            "flag": "UNSTABLE_REVENUE",
            "message": f"Revenue volatility of {volatility:.1%} indicates unstable cash flow"
        }
    return None


def check_cash_flow_issues(nsf_fees: int) -> Optional[Dict]:
    """
    Check for cash flow issues based on NSF fees.

    Args:
        nsf_fees: Number of NSF (Non-Sufficient Funds) fees in past 12 months

    Returns:
        Risk flag dict if nsf_fees > 3, None otherwise
    """
    if nsf_fees > 3:
        return {
            "severity": "HIGH",
            "flag": "CASH_FLOW_ISSUES",
            "message": f"{nsf_fees} NSF fees indicate recurring cash flow problems"
        }
    return None


def check_high_leverage(debt_to_revenue: float) -> Optional[Dict]:
    """
    Check if debt-to-revenue ratio is too high.

    Args:
        debt_to_revenue: Total debt / Annual revenue

    Returns:
        Risk flag dict if ratio > 0.50, None otherwise
    """
    if debt_to_revenue > 0.50:
        return {
            "severity": "MEDIUM",
            "flag": "HIGH_LEVERAGE",
            "message": f"Debt-to-revenue ratio of {debt_to_revenue:.1%} exceeds 50% threshold"
        }
    return None


def check_negative_cash_flow(avg_monthly_cash_flow: float) -> Optional[Dict]:
    """
    Check for negative cash flow.

    Args:
        avg_monthly_cash_flow: Average monthly cash flow

    Returns:
        Risk flag dict if cash flow is negative, None otherwise
    """
    if avg_monthly_cash_flow < 0:
        return {
            "severity": "HIGH",
            "flag": "NEGATIVE_CASH_FLOW",
            "message": f"Negative average monthly cash flow of ${avg_monthly_cash_flow:,.2f}"
        }
    return None


def check_declining_revenue(revenue_trend: float) -> Optional[Dict]:
    """
    Check if revenue is declining.

    Args:
        revenue_trend: Revenue growth rate (negative = decline)

    Returns:
        Risk flag dict if trend < -0.10, None otherwise
    """
    if revenue_trend < -0.10:
        return {
            "severity": "MEDIUM",
            "flag": "DECLINING_REVENUE",
            "message": f"Revenue declining by {abs(revenue_trend):.1%}"
        }
    return None


def calculate_risk_level(flags: List[Dict]) -> str:
    """
    Calculate overall risk level based on flags.

    Logic:
        - Any HIGH severity flag → HIGH risk
        - 3+ MEDIUM severity flags → HIGH risk
        - 1-2 MEDIUM severity flags → MODERATE risk
        - No flags → LOW risk

    Args:
        flags: List of risk flag dicts

    Returns:
        Risk level: "LOW", "MODERATE", or "HIGH"
    """
    if not flags:
        return "LOW"

    high_count = sum(1 for f in flags if f["severity"] == "HIGH")
    medium_count = sum(1 for f in flags if f["severity"] == "MEDIUM")

    if high_count > 0:
        return "HIGH"
    elif medium_count >= 3:
        return "HIGH"
    elif medium_count >= 1:
        return "MODERATE"
    else:
        return "LOW"


def detect_positive_signals(metrics: Dict, nsf_fees: int) -> List[str]:
    """
    Detect positive signals in the metrics.

    Args:
        metrics: Financial metrics dict
        nsf_fees: Number of NSF fees

    Returns:
        List of positive signal messages
    """
    signals = []

    # Strong cash flow
    if metrics.get("avg_monthly_cash_flow", 0) > 10000:
        signals.append("Strong cash flow reserves")

    # Excellent DSCR
    if metrics.get("dscr", 0) >= 1.75:
        signals.append("Excellent DSCR")
    elif metrics.get("dscr", 0) >= 1.5:
        signals.append("Strong DSCR")
    elif metrics.get("dscr", 0) >= 1.25:
        signals.append("Adequate DSCR")

    # Low volatility
    if metrics.get("revenue_volatility", 1.0) < 0.20:
        signals.append("Low revenue volatility")

    # High stability
    if metrics.get("stability_score", 0) >= 80:
        signals.append("High business stability")
    elif metrics.get("stability_score", 0) >= 70:
        signals.append("Good business stability")

    # Growing revenue
    if metrics.get("revenue_trend", 0) > 0.15:
        signals.append("Strong revenue growth")
    elif metrics.get("revenue_trend", 0) > 0:
        signals.append("Growing revenue")

    # Clean payment history
    if nsf_fees == 0:
        signals.append("Clean payment history")

    # Low leverage
    if metrics.get("debt_to_revenue", 1.0) < 0.30:
        signals.append("Low financial leverage")

    return signals


class RiskAssessorAgent:
    """
    Agent 4: Risk Assessor

    Analyzes financial metrics and identifies:
        - Risk flags (negative signals)
        - Positive signals (strengths)
        - Overall risk level (LOW/MODERATE/HIGH)
    """

    def __init__(self):
        """Initialize the Risk Assessor Agent."""
        pass

    def assess(self, financial_metrics: Dict, extracted_data: Dict) -> Dict:
        """
        Assess risks based on financial metrics.

        Args:
            financial_metrics: Output from Financial Analyzer Agent
            extracted_data: Output from Data Extractor Agent (for NSF fees)

        Returns:
            Dict with "risk_assessment" key containing:
                - risk_level: "LOW", "MODERATE", or "HIGH"
                - flags: List of risk flag dicts
                - positive_signals: List of positive signal strings
        """
        # Extract metrics
        metrics = financial_metrics.get("metrics", {})

        # Extract NSF fees
        bank_data = extracted_data.get("bank_data", {})
        nsf_fees = bank_data.get("nsf_fees", 0)

        # Run all risk checks
        flags = []

        # DSCR check
        dscr = metrics.get("dscr", 0)
        flag = check_low_dscr(dscr)
        if flag:
            flags.append(flag)

        # Revenue volatility check
        volatility = metrics.get("revenue_volatility", 0)
        flag = check_unstable_revenue(volatility)
        if flag:
            flags.append(flag)

        # NSF fees check
        flag = check_cash_flow_issues(nsf_fees)
        if flag:
            flags.append(flag)

        # Leverage check
        debt_to_revenue = metrics.get("debt_to_revenue", 0)
        flag = check_high_leverage(debt_to_revenue)
        if flag:
            flags.append(flag)

        # Cash flow check
        cash_flow = metrics.get("avg_monthly_cash_flow", 0)
        flag = check_negative_cash_flow(cash_flow)
        if flag:
            flags.append(flag)

        # Revenue trend check
        revenue_trend = metrics.get("revenue_trend", 0)
        flag = check_declining_revenue(revenue_trend)
        if flag:
            flags.append(flag)

        # Calculate overall risk level
        risk_level = calculate_risk_level(flags)

        # Detect positive signals
        positive_signals = detect_positive_signals(metrics, nsf_fees)

        return {
            "risk_assessment": {
                "risk_level": risk_level,
                "flags": flags,
                "positive_signals": positive_signals,
            }
        }
