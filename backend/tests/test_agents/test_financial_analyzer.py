"""Tests for Financial Analyzer Agent."""
import pytest
from typing import Dict, List


class TestFinancialMetrics:
    """Test financial metric calculations."""

    def test_calculate_avg_monthly_revenue(self):
        """Test average monthly revenue calculation."""
        from agents.financial_analyzer import calculate_avg_monthly_revenue

        monthly_deposits = [40000, 45000, 38000, 42000, 50000, 48000]
        result = calculate_avg_monthly_revenue(monthly_deposits)

        assert result == 43833.33  # rounded to 2 decimals
        assert isinstance(result, float)

    def test_calculate_avg_monthly_revenue_empty_list(self):
        """Test with empty list returns 0."""
        from agents.financial_analyzer import calculate_avg_monthly_revenue

        result = calculate_avg_monthly_revenue([])
        assert result == 0.0

    def test_calculate_revenue_volatility(self):
        """Test revenue volatility calculation (coefficient of variation)."""
        from agents.financial_analyzer import calculate_revenue_volatility

        # Low volatility example
        stable_revenue = [40000, 41000, 40500, 40200, 40800]
        low_volatility = calculate_revenue_volatility(stable_revenue)
        assert low_volatility < 0.05  # Less than 5% volatility

        # High volatility example
        unstable_revenue = [20000, 50000, 15000, 60000, 25000]
        high_volatility = calculate_revenue_volatility(unstable_revenue)
        assert high_volatility > 0.40  # More than 40% volatility

    def test_calculate_revenue_volatility_single_value(self):
        """Test volatility with single value returns 0."""
        from agents.financial_analyzer import calculate_revenue_volatility

        result = calculate_revenue_volatility([50000])
        assert result == 0.0

    def test_calculate_dscr(self):
        """Test Debt Service Coverage Ratio calculation."""
        from agents.financial_analyzer import calculate_dscr

        monthly_cash_flow = 10000
        loan_amount = 100000
        annual_interest_rate = 0.08  # 8%
        term_months = 60  # 5 years

        dscr = calculate_dscr(
            monthly_cash_flow=monthly_cash_flow,
            loan_amount=loan_amount,
            annual_interest_rate=annual_interest_rate,
            term_months=term_months,
        )

        # Expected monthly payment ~$2,027
        # DSCR = 10000 / 2027 = ~4.93
        assert 4.5 < dscr < 5.5
        assert isinstance(dscr, float)

    def test_calculate_dscr_zero_payment(self):
        """Test DSCR when payment is zero (no debt)."""
        from agents.financial_analyzer import calculate_dscr

        result = calculate_dscr(
            monthly_cash_flow=10000,
            loan_amount=0,
            annual_interest_rate=0.08,
            term_months=60,
        )

        assert result == 0.0

    def test_calculate_monthly_payment(self):
        """Test monthly payment calculation."""
        from agents.financial_analyzer import calculate_monthly_payment

        loan_amount = 100000
        annual_interest_rate = 0.08
        term_months = 60

        payment = calculate_monthly_payment(
            loan_amount, annual_interest_rate, term_months
        )

        # Standard loan formula result
        assert 2000 < payment < 2100
        assert isinstance(payment, float)

    def test_calculate_monthly_payment_zero_interest(self):
        """Test monthly payment with 0% interest."""
        from agents.financial_analyzer import calculate_monthly_payment

        payment = calculate_monthly_payment(
            loan_amount=60000, annual_interest_rate=0.0, term_months=60
        )

        assert payment == 1000.0  # Simply loan_amount / term_months

    def test_calculate_debt_to_revenue_ratio(self):
        """Test debt-to-revenue ratio calculation."""
        from agents.financial_analyzer import calculate_debt_to_revenue_ratio

        total_debt = 120000
        annual_revenue = 400000

        ratio = calculate_debt_to_revenue_ratio(total_debt, annual_revenue)

        assert ratio == 0.30  # 30%
        assert isinstance(ratio, float)

    def test_calculate_debt_to_revenue_ratio_zero_revenue(self):
        """Test ratio with zero revenue returns 0."""
        from agents.financial_analyzer import calculate_debt_to_revenue_ratio

        ratio = calculate_debt_to_revenue_ratio(100000, 0)
        assert ratio == 0.0

    def test_calculate_stability_score(self):
        """Test business stability score calculation."""
        from agents.financial_analyzer import calculate_stability_score

        # Strong stability
        high_score = calculate_stability_score(
            revenue_volatility=0.10,  # Low volatility
            business_age_years=8,  # Established
            nsf_fees_count=0,  # No NSF fees
            revenue_trend=0.15,  # Growing 15%
        )

        assert 80 <= high_score <= 100

        # Weak stability
        low_score = calculate_stability_score(
            revenue_volatility=0.60,  # High volatility
            business_age_years=1,  # New business
            nsf_fees_count=5,  # Multiple NSF fees
            revenue_trend=-0.20,  # Declining 20%
        )

        assert 0 <= low_score <= 40

    def test_calculate_stability_score_bounds(self):
        """Test stability score is always between 0-100."""
        from agents.financial_analyzer import calculate_stability_score

        # Extreme bad case
        score = calculate_stability_score(
            revenue_volatility=2.0, business_age_years=0, nsf_fees_count=20, revenue_trend=-0.90
        )
        assert 0 <= score <= 100

        # Extreme good case
        score = calculate_stability_score(
            revenue_volatility=0.0, business_age_years=50, nsf_fees_count=0, revenue_trend=1.0
        )
        assert 0 <= score <= 100


class TestFinancialAnalyzerAgent:
    """Test FinancialAnalyzerAgent class."""

    @pytest.fixture
    def sample_extracted_data(self) -> Dict:
        """Sample data from Data Extractor Agent."""
        return {
            "bank_data": {
                "monthly_deposits": [42000, 38000, 51000, 45000, 43000, 47000, 46000, 44000, 49000, 45000, 44000, 46000],
                "monthly_withdrawals": [35000, 32000, 38000, 36000, 34000, 37000, 36000, 35000, 38000, 36000, 35000, 37000],
                "nsf_fees": 1,
                "average_balance": 15000,
                "months_covered": 12,
            },
            "tax_data": {
                "gross_revenue": 540000,
                "total_expenses": 420000,
                "net_income": 120000,
                "tax_year": 2024,
            },
            "existing_debt": 80000,
        }

    @pytest.fixture
    def loan_request(self) -> Dict:
        """Sample loan request."""
        return {
            "loan_amount": 50000,
            "annual_interest_rate": 0.08,
            "term_months": 60,
            "business_age_years": 5,
        }

    def test_agent_analyze_returns_metrics(self, sample_extracted_data, loan_request):
        """Test that agent returns all required metrics."""
        from agents.financial_analyzer import FinancialAnalyzerAgent

        agent = FinancialAnalyzerAgent()
        result = agent.analyze(sample_extracted_data, loan_request)

        # Check structure
        assert "metrics" in result
        metrics = result["metrics"]

        # Check all required fields
        assert "avg_monthly_revenue" in metrics
        assert "revenue_volatility" in metrics
        assert "avg_monthly_cash_flow" in metrics
        assert "dscr" in metrics
        assert "debt_to_revenue" in metrics
        assert "annual_revenue" in metrics
        assert "net_income" in metrics
        assert "stability_score" in metrics

        # Check types
        assert isinstance(metrics["avg_monthly_revenue"], float)
        assert isinstance(metrics["dscr"], float)
        assert isinstance(metrics["stability_score"], (int, float))

    def test_agent_analyze_correct_calculations(self, sample_extracted_data, loan_request):
        """Test that agent calculations are correct."""
        from agents.financial_analyzer import FinancialAnalyzerAgent

        agent = FinancialAnalyzerAgent()
        result = agent.analyze(sample_extracted_data, loan_request)
        metrics = result["metrics"]

        # Verify avg monthly revenue
        expected_avg = sum(sample_extracted_data["bank_data"]["monthly_deposits"]) / 12
        assert abs(metrics["avg_monthly_revenue"] - expected_avg) < 1.0

        # Verify annual revenue from tax data
        assert metrics["annual_revenue"] == 540000

        # Verify net income
        assert metrics["net_income"] == 120000

        # Verify DSCR is positive
        assert metrics["dscr"] > 0

    def test_agent_handles_missing_data(self):
        """Test agent handles incomplete data gracefully."""
        from agents.financial_analyzer import FinancialAnalyzerAgent

        agent = FinancialAnalyzerAgent()

        incomplete_data = {
            "bank_data": {
                "monthly_deposits": [40000, 42000],
                "monthly_withdrawals": [35000, 36000],
                "nsf_fees": 0,
            }
            # Missing tax_data
        }

        loan_request = {"loan_amount": 50000, "annual_interest_rate": 0.08, "term_months": 60}

        result = agent.analyze(incomplete_data, loan_request)

        # Should still return metrics, using available data
        assert "metrics" in result
        assert result["metrics"]["avg_monthly_revenue"] > 0

    def test_agent_state_format(self, sample_extracted_data, loan_request):
        """Test that agent output conforms to LangGraph state format."""
        from agents.financial_analyzer import FinancialAnalyzerAgent

        agent = FinancialAnalyzerAgent()
        result = agent.analyze(sample_extracted_data, loan_request)

        # Should be a dict that can be added to state
        assert isinstance(result, dict)
        assert "metrics" in result
