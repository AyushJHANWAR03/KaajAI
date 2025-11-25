"""Financial Analyzer Agent - Calculates key financial metrics."""
import math
from typing import Dict, List, Optional
import numpy as np


def calculate_avg_monthly_revenue(monthly_deposits: List[float]) -> float:
    """
    Calculate average monthly revenue from deposits.

    Args:
        monthly_deposits: List of monthly deposit amounts

    Returns:
        Average monthly revenue rounded to 2 decimals
    """
    if not monthly_deposits:
        return 0.0

    avg = sum(monthly_deposits) / len(monthly_deposits)
    return round(avg, 2)


def calculate_revenue_volatility(monthly_revenue: List[float]) -> float:
    """
    Calculate revenue volatility using coefficient of variation.

    Volatility = Standard Deviation / Mean

    Args:
        monthly_revenue: List of monthly revenue amounts

    Returns:
        Volatility as a decimal (e.g., 0.25 = 25% volatility)
    """
    if not monthly_revenue or len(monthly_revenue) <= 1:
        return 0.0

    mean = np.mean(monthly_revenue)
    if mean == 0:
        return 0.0

    std_dev = np.std(monthly_revenue, ddof=1)  # Sample std dev
    volatility = std_dev / mean

    return round(volatility, 4)


def calculate_monthly_payment(
    loan_amount: float, annual_interest_rate: float, term_months: int
) -> float:
    """
    Calculate monthly loan payment using amortization formula.

    Formula: M = P * [r(1+r)^n] / [(1+r)^n - 1]
    Where:
        M = Monthly payment
        P = Principal (loan amount)
        r = Monthly interest rate
        n = Number of payments

    Args:
        loan_amount: Principal amount
        annual_interest_rate: Annual interest rate as decimal (0.08 = 8%)
        term_months: Loan term in months

    Returns:
        Monthly payment amount
    """
    if loan_amount == 0 or term_months == 0:
        return 0.0

    if annual_interest_rate == 0:
        # No interest, simple division
        return round(loan_amount / term_months, 2)

    monthly_rate = annual_interest_rate / 12
    numerator = monthly_rate * math.pow(1 + monthly_rate, term_months)
    denominator = math.pow(1 + monthly_rate, term_months) - 1

    payment = loan_amount * (numerator / denominator)
    return round(payment, 2)


def calculate_dscr(
    monthly_cash_flow: float,
    loan_amount: float,
    annual_interest_rate: float,
    term_months: int,
) -> float:
    """
    Calculate Debt Service Coverage Ratio (DSCR).

    DSCR = Monthly Cash Flow / Monthly Debt Payment

    Industry standard:
        DSCR >= 1.25: Good (approved)
        DSCR 1.0-1.25: Marginal
        DSCR < 1.0: Risky (likely declined)

    Args:
        monthly_cash_flow: Average monthly cash flow
        loan_amount: Requested loan amount
        annual_interest_rate: Annual interest rate
        term_months: Loan term in months

    Returns:
        DSCR ratio
    """
    monthly_payment = calculate_monthly_payment(
        loan_amount, annual_interest_rate, term_months
    )

    if monthly_payment == 0:
        return 0.0

    dscr = monthly_cash_flow / monthly_payment
    return round(dscr, 2)


def calculate_debt_to_revenue_ratio(total_debt: float, annual_revenue: float) -> float:
    """
    Calculate debt-to-revenue ratio.

    Ratio = Total Debt / Annual Revenue

    Industry standard:
        < 0.30: Low leverage (good)
        0.30-0.50: Moderate leverage
        > 0.50: High leverage (risky)

    Args:
        total_debt: Total existing debt + new loan
        annual_revenue: Annual gross revenue

    Returns:
        Debt-to-revenue ratio as decimal (0.30 = 30%)
    """
    if annual_revenue == 0:
        return 0.0

    ratio = total_debt / annual_revenue
    return round(ratio, 2)


def calculate_stability_score(
    revenue_volatility: float,
    business_age_years: int,
    nsf_fees_count: int,
    revenue_trend: float = 0.0,
) -> int:
    """
    Calculate business stability score (0-100).

    Components:
        - Revenue volatility (40% weight): Lower is better
        - Business age (30% weight): Older is better
        - NSF fees (30% weight): Fewer is better
        - Revenue trend (bonus): Positive growth adds points

    Args:
        revenue_volatility: Coefficient of variation (0.0-1.0+)
        business_age_years: Age of business in years
        nsf_fees_count: Number of NSF fees in past 12 months
        revenue_trend: YoY revenue growth rate (-1.0 to 1.0+)

    Returns:
        Stability score from 0-100
    """
    # Volatility component (40 points max)
    # Inverse relationship: higher volatility = lower score
    volatility_score = max(0, (1 - min(revenue_volatility, 1.0)) * 40)

    # Age component (30 points max)
    # Caps at 10 years
    age_score = min(business_age_years, 10) / 10 * 30

    # NSF component (30 points max)
    # Penalize NSF fees
    if nsf_fees_count == 0:
        nsf_score = 30
    elif nsf_fees_count <= 2:
        nsf_score = 20
    elif nsf_fees_count <= 5:
        nsf_score = 10
    else:
        nsf_score = 0

    # Base score
    base_score = volatility_score + age_score + nsf_score

    # Revenue trend bonus (up to +10 or -10)
    trend_bonus = revenue_trend * 10

    # Final score with bounds
    final_score = base_score + trend_bonus
    return int(max(0, min(100, final_score)))


class FinancialAnalyzerAgent:
    """
    Agent 3: Financial Analyzer

    Calculates key financial metrics from extracted data:
        - Average monthly revenue
        - Revenue volatility
        - Cash flow metrics
        - DSCR (Debt Service Coverage Ratio)
        - Leverage ratios
        - Business stability score
    """

    def __init__(self):
        """Initialize the Financial Analyzer Agent."""
        pass

    def analyze(self, extracted_data: Dict, loan_request: Dict) -> Dict:
        """
        Analyze financial data and calculate metrics.

        Args:
            extracted_data: Output from Data Extractor Agent containing:
                - bank_data: {monthly_deposits, monthly_withdrawals, nsf_fees, ...}
                - tax_data: {gross_revenue, total_expenses, net_income, ...}
                - existing_debt: Total existing debt
            loan_request: {
                loan_amount,
                annual_interest_rate,
                term_months,
                business_age_years
            }

        Returns:
            Dict with "metrics" key containing all calculated metrics
        """
        # Extract bank data
        bank_data = extracted_data.get("bank_data", {})
        monthly_deposits = bank_data.get("monthly_deposits", [])
        monthly_withdrawals = bank_data.get("monthly_withdrawals", [])
        nsf_fees = bank_data.get("nsf_fees", 0)

        # Extract tax data
        tax_data = extracted_data.get("tax_data", {})
        annual_revenue = tax_data.get("gross_revenue", 0)
        net_income = tax_data.get("net_income", 0)

        # Extract loan request details
        loan_amount = loan_request.get("loan_amount", 0)
        annual_interest_rate = loan_request.get("annual_interest_rate", 0.08)
        term_months = loan_request.get("term_months", 60)
        business_age_years = loan_request.get("business_age_years", 0)
        existing_debt = extracted_data.get("existing_debt", 0)

        # Calculate metrics
        avg_monthly_revenue = calculate_avg_monthly_revenue(monthly_deposits)

        revenue_volatility = calculate_revenue_volatility(monthly_deposits)

        # Calculate avg monthly cash flow
        if monthly_deposits and monthly_withdrawals:
            deposits_avg = sum(monthly_deposits) / len(monthly_deposits)
            withdrawals_avg = sum(monthly_withdrawals) / len(monthly_withdrawals)
            avg_monthly_cash_flow = deposits_avg - withdrawals_avg
        else:
            avg_monthly_cash_flow = 0.0

        # Calculate DSCR using TOTAL debt service (existing + new loan)
        # New loan payment
        new_loan_payment = calculate_monthly_payment(
            loan_amount=loan_amount,
            annual_interest_rate=annual_interest_rate,
            term_months=term_months,
        )

        # Existing debt payment (assume same rate/term for conservative estimate)
        existing_debt_payment = calculate_monthly_payment(
            loan_amount=existing_debt,
            annual_interest_rate=annual_interest_rate,
            term_months=term_months,
        )

        # Total monthly debt service
        total_monthly_payment = new_loan_payment + existing_debt_payment

        # Calculate DSCR
        if total_monthly_payment == 0:
            dscr = 0.0
        else:
            dscr = round(avg_monthly_cash_flow / total_monthly_payment, 2)

        # Calculate total debt (existing + new loan)
        total_debt = existing_debt + loan_amount

        # Calculate debt-to-revenue ratio
        # Use bank data for annual revenue if tax data missing
        revenue_for_ratio = annual_revenue if annual_revenue > 0 else avg_monthly_revenue * 12
        debt_to_revenue = calculate_debt_to_revenue_ratio(total_debt, revenue_for_ratio)

        # Calculate revenue trend (simple: compare first 6 months to last 6 months)
        revenue_trend = 0.0
        if len(monthly_deposits) >= 12:
            first_half = sum(monthly_deposits[:6]) / 6
            second_half = sum(monthly_deposits[6:12]) / 6
            if first_half > 0:
                revenue_trend = (second_half - first_half) / first_half

        # Calculate stability score
        stability_score = calculate_stability_score(
            revenue_volatility=revenue_volatility,
            business_age_years=business_age_years,
            nsf_fees_count=nsf_fees,
            revenue_trend=revenue_trend,
        )

        # Compile metrics
        metrics = {
            "avg_monthly_revenue": round(avg_monthly_revenue, 2),
            "revenue_volatility": revenue_volatility,
            "avg_monthly_cash_flow": round(avg_monthly_cash_flow, 2),
            "dscr": dscr,
            "debt_to_revenue": debt_to_revenue,
            "annual_revenue": revenue_for_ratio,
            "net_income": net_income,
            "stability_score": stability_score,
            "total_debt": total_debt,
            "revenue_trend": round(revenue_trend, 4),
        }

        return {"metrics": metrics}
