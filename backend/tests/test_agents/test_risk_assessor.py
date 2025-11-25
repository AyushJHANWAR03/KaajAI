"""Tests for Risk Assessor Agent."""
import pytest
from typing import Dict


class TestRiskRules:
    """Test individual risk detection rules."""

    def test_low_dscr_flag(self):
        """Test LOW_DSCR flag when DSCR < 1.25."""
        from agents.risk_assessor import check_low_dscr

        # Below threshold
        flag = check_low_dscr(1.0)
        assert flag is not None
        assert flag["severity"] == "HIGH"
        assert flag["flag"] == "LOW_DSCR"

        # At threshold
        flag = check_low_dscr(1.25)
        assert flag is None

        # Above threshold
        flag = check_low_dscr(1.5)
        assert flag is None

    def test_unstable_revenue_flag(self):
        """Test UNSTABLE_REVENUE flag when volatility > 0.40."""
        from agents.risk_assessor import check_unstable_revenue

        # High volatility
        flag = check_unstable_revenue(0.50)
        assert flag is not None
        assert flag["severity"] == "MEDIUM"
        assert flag["flag"] == "UNSTABLE_REVENUE"

        # At threshold
        flag = check_unstable_revenue(0.40)
        assert flag is None

        # Low volatility
        flag = check_unstable_revenue(0.15)
        assert flag is None

    def test_cash_flow_issues_flag(self):
        """Test CASH_FLOW_ISSUES flag when NSF fees > 3."""
        from agents.risk_assessor import check_cash_flow_issues

        # Many NSF fees
        flag = check_cash_flow_issues(5)
        assert flag is not None
        assert flag["severity"] == "HIGH"
        assert flag["flag"] == "CASH_FLOW_ISSUES"

        # At threshold
        flag = check_cash_flow_issues(3)
        assert flag is None

        # No NSF fees
        flag = check_cash_flow_issues(0)
        assert flag is None

    def test_high_leverage_flag(self):
        """Test HIGH_LEVERAGE flag when debt-to-revenue > 0.50."""
        from agents.risk_assessor import check_high_leverage

        # High leverage
        flag = check_high_leverage(0.60)
        assert flag is not None
        assert flag["severity"] == "MEDIUM"
        assert flag["flag"] == "HIGH_LEVERAGE"

        # At threshold
        flag = check_high_leverage(0.50)
        assert flag is None

        # Low leverage
        flag = check_high_leverage(0.30)
        assert flag is None

    def test_negative_cash_flow_flag(self):
        """Test NEGATIVE_CASH_FLOW flag."""
        from agents.risk_assessor import check_negative_cash_flow

        # Negative
        flag = check_negative_cash_flow(-5000)
        assert flag is not None
        assert flag["severity"] == "HIGH"
        assert flag["flag"] == "NEGATIVE_CASH_FLOW"

        # Zero
        flag = check_negative_cash_flow(0)
        assert flag is None

        # Positive
        flag = check_negative_cash_flow(10000)
        assert flag is None

    def test_declining_revenue_flag(self):
        """Test DECLINING_REVENUE flag when revenue trend < -0.10."""
        from agents.risk_assessor import check_declining_revenue

        # Declining
        flag = check_declining_revenue(-0.20)
        assert flag is not None
        assert flag["severity"] == "MEDIUM"
        assert flag["flag"] == "DECLINING_REVENUE"

        # At threshold
        flag = check_declining_revenue(-0.10)
        assert flag is None

        # Growing
        flag = check_declining_revenue(0.15)
        assert flag is None


class TestRiskLevel:
    """Test risk level calculation."""

    def test_calculate_risk_level_low(self):
        """Test LOW risk level with no flags."""
        from agents.risk_assessor import calculate_risk_level

        flags = []
        risk_level = calculate_risk_level(flags)
        assert risk_level == "LOW"

    def test_calculate_risk_level_moderate_single_medium(self):
        """Test MODERATE risk with single medium flag."""
        from agents.risk_assessor import calculate_risk_level

        flags = [{"severity": "MEDIUM", "flag": "UNSTABLE_REVENUE"}]
        risk_level = calculate_risk_level(flags)
        assert risk_level == "MODERATE"

    def test_calculate_risk_level_high_single_high(self):
        """Test HIGH risk with single high flag."""
        from agents.risk_assessor import calculate_risk_level

        flags = [{"severity": "HIGH", "flag": "LOW_DSCR"}]
        risk_level = calculate_risk_level(flags)
        assert risk_level == "HIGH"

    def test_calculate_risk_level_high_multiple_medium(self):
        """Test HIGH risk with multiple medium flags."""
        from agents.risk_assessor import calculate_risk_level

        flags = [
            {"severity": "MEDIUM", "flag": "UNSTABLE_REVENUE"},
            {"severity": "MEDIUM", "flag": "HIGH_LEVERAGE"},
            {"severity": "MEDIUM", "flag": "DECLINING_REVENUE"},
        ]
        risk_level = calculate_risk_level(flags)
        assert risk_level == "HIGH"


class TestPositiveSignals:
    """Test positive signal detection."""

    def test_detect_positive_signals_strong_cash_flow(self):
        """Test detection of strong cash flow."""
        from agents.risk_assessor import detect_positive_signals

        metrics = {
            "avg_monthly_cash_flow": 15000,
            "dscr": 1.8,
            "revenue_volatility": 0.12,
            "stability_score": 85,
            "revenue_trend": 0.20,
        }

        signals = detect_positive_signals(metrics, nsf_fees=0)

        assert "Strong cash flow reserves" in signals
        assert "Excellent DSCR" in signals
        assert "Low revenue volatility" in signals
        assert "High business stability" in signals
        assert "Strong revenue growth" in signals  # 0.20 > 0.15 gives "Strong"
        assert "Clean payment history" in signals

    def test_detect_positive_signals_minimal(self):
        """Test with minimal positive signals."""
        from agents.risk_assessor import detect_positive_signals

        metrics = {
            "avg_monthly_cash_flow": 3000,
            "dscr": 1.2,
            "revenue_volatility": 0.35,
            "stability_score": 60,
            "revenue_trend": -0.05,
        }

        signals = detect_positive_signals(metrics, nsf_fees=2)

        # Should have very few signals
        assert len(signals) <= 2


class TestRiskAssessorAgent:
    """Test RiskAssessorAgent class."""

    @pytest.fixture
    def sample_metrics_good(self) -> Dict:
        """Sample metrics from a strong borrower."""
        return {
            "metrics": {
                "avg_monthly_revenue": 45000,
                "revenue_volatility": 0.15,
                "avg_monthly_cash_flow": 12000,
                "dscr": 1.50,
                "debt_to_revenue": 0.35,
                "stability_score": 80,
                "revenue_trend": 0.10,
            }
        }

    @pytest.fixture
    def sample_metrics_risky(self) -> Dict:
        """Sample metrics from a risky borrower."""
        return {
            "metrics": {
                "avg_monthly_revenue": 25000,
                "revenue_volatility": 0.50,
                "avg_monthly_cash_flow": 2000,
                "dscr": 1.10,
                "debt_to_revenue": 0.60,
                "stability_score": 40,
                "revenue_trend": -0.15,
            }
        }

    @pytest.fixture
    def sample_extracted_data(self) -> Dict:
        """Sample extracted data with NSF fees."""
        return {"bank_data": {"nsf_fees": 0}}

    @pytest.fixture
    def sample_extracted_data_with_issues(self) -> Dict:
        """Sample extracted data with cash flow issues."""
        return {"bank_data": {"nsf_fees": 5}}

    def test_agent_assess_good_borrower(
        self, sample_metrics_good, sample_extracted_data
    ):
        """Test assessment of strong borrower."""
        from agents.risk_assessor import RiskAssessorAgent

        agent = RiskAssessorAgent()
        result = agent.assess(sample_metrics_good, sample_extracted_data)

        assert "risk_assessment" in result
        assessment = result["risk_assessment"]

        assert assessment["risk_level"] == "LOW"
        assert len(assessment["flags"]) == 0
        assert len(assessment["positive_signals"]) > 3

    def test_agent_assess_risky_borrower(
        self, sample_metrics_risky, sample_extracted_data_with_issues
    ):
        """Test assessment of risky borrower."""
        from agents.risk_assessor import RiskAssessorAgent

        agent = RiskAssessorAgent()
        result = agent.assess(sample_metrics_risky, sample_extracted_data_with_issues)

        assert "risk_assessment" in result
        assessment = result["risk_assessment"]

        assert assessment["risk_level"] in ["MODERATE", "HIGH"]
        assert len(assessment["flags"]) >= 3

        # Check for expected flags
        flag_types = [f["flag"] for f in assessment["flags"]]
        assert "LOW_DSCR" in flag_types
        assert "UNSTABLE_REVENUE" in flag_types
        assert "CASH_FLOW_ISSUES" in flag_types

    def test_agent_output_structure(self, sample_metrics_good, sample_extracted_data):
        """Test that agent output has correct structure."""
        from agents.risk_assessor import RiskAssessorAgent

        agent = RiskAssessorAgent()
        result = agent.assess(sample_metrics_good, sample_extracted_data)

        # Check top-level structure
        assert isinstance(result, dict)
        assert "risk_assessment" in result

        # Check risk_assessment structure
        assessment = result["risk_assessment"]
        assert "risk_level" in assessment
        assert "flags" in assessment
        assert "positive_signals" in assessment

        # Check risk_level is valid
        assert assessment["risk_level"] in ["LOW", "MODERATE", "HIGH"]

        # Check flags structure
        assert isinstance(assessment["flags"], list)
        if assessment["flags"]:
            for flag in assessment["flags"]:
                assert "severity" in flag
                assert "flag" in flag
                assert "message" in flag

        # Check positive signals
        assert isinstance(assessment["positive_signals"], list)
