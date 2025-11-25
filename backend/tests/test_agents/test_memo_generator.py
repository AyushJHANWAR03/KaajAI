"""Tests for Memo Generator Agent."""
import pytest
from typing import Dict
from unittest.mock import Mock, patch


class TestRecommendationLogic:
    """Test recommendation determination logic."""

    def test_determine_recommendation_approve(self):
        """Test APPROVE recommendation for strong application."""
        from agents.memo_generator import determine_recommendation

        # Strong metrics, low risk
        recommendation = determine_recommendation(
            risk_level="LOW",
            dscr=1.50,
            stability_score=85,
            flags=[]
        )

        assert recommendation["decision"] == "APPROVE"
        assert recommendation["conditions"] == []

    def test_determine_recommendation_approve_with_conditions(self):
        """Test APPROVE_WITH_CONDITIONS for moderate risk."""
        from agents.memo_generator import determine_recommendation

        # Moderate risk with some flags
        recommendation = determine_recommendation(
            risk_level="MODERATE",
            dscr=1.35,
            stability_score=70,
            flags=[{"severity": "MEDIUM", "flag": "UNSTABLE_REVENUE"}]
        )

        assert recommendation["decision"] == "APPROVE_WITH_CONDITIONS"
        assert len(recommendation["conditions"]) > 0
        assert isinstance(recommendation["conditions"], list)

    def test_determine_recommendation_decline(self):
        """Test DECLINE recommendation for high risk."""
        from agents.memo_generator import determine_recommendation

        # High risk with critical flags
        recommendation = determine_recommendation(
            risk_level="HIGH",
            dscr=0.90,
            stability_score=35,
            flags=[
                {"severity": "HIGH", "flag": "LOW_DSCR"},
                {"severity": "HIGH", "flag": "CASH_FLOW_ISSUES"}
            ]
        )

        assert recommendation["decision"] == "DECLINE"
        assert len(recommendation["reasons"]) > 0

    def test_determine_recommendation_edge_case_borderline(self):
        """Test borderline case."""
        from agents.memo_generator import determine_recommendation

        recommendation = determine_recommendation(
            risk_level="MODERATE",
            dscr=1.25,  # Exactly at threshold
            stability_score=65,
            flags=[{"severity": "MEDIUM", "flag": "HIGH_LEVERAGE"}]
        )

        assert recommendation["decision"] in ["APPROVE_WITH_CONDITIONS", "CONDITIONAL_APPROVAL"]


class TestUnderwritingScore:
    """Test underwriting score calculation."""

    def test_calculate_underwriting_score_excellent(self):
        """Test score for excellent application."""
        from agents.memo_generator import calculate_underwriting_score

        score = calculate_underwriting_score(
            risk_level="LOW",
            dscr=1.75,
            stability_score=90,
            revenue_volatility=0.10
        )

        assert 85 <= score <= 100
        assert isinstance(score, int)

    def test_calculate_underwriting_score_poor(self):
        """Test score for poor application."""
        from agents.memo_generator import calculate_underwriting_score

        score = calculate_underwriting_score(
            risk_level="HIGH",
            dscr=0.95,
            stability_score=30,
            revenue_volatility=0.60
        )

        assert 0 <= score <= 40
        assert isinstance(score, int)

    def test_calculate_underwriting_score_moderate(self):
        """Test score for moderate application."""
        from agents.memo_generator import calculate_underwriting_score

        score = calculate_underwriting_score(
            risk_level="MODERATE",
            dscr=1.30,
            stability_score=65,
            revenue_volatility=0.30
        )

        assert 50 <= score <= 75
        assert isinstance(score, int)

    def test_calculate_underwriting_score_bounds(self):
        """Test score is always 0-100."""
        from agents.memo_generator import calculate_underwriting_score

        # Extreme bad
        score = calculate_underwriting_score("HIGH", 0.5, 0, 2.0)
        assert 0 <= score <= 100

        # Extreme good
        score = calculate_underwriting_score("LOW", 3.0, 100, 0.0)
        assert 0 <= score <= 100


class TestCreditMemoPrompt:
    """Test credit memo prompt generation."""

    def test_build_credit_memo_prompt(self):
        """Test prompt building for LLM."""
        from agents.memo_generator import build_credit_memo_prompt

        business_info = {
            "business_name": "ABC Construction LLC",
            "industry": "Construction",
            "loan_amount": 50000,
        }

        metrics = {
            "avg_monthly_revenue": 45000,
            "dscr": 1.45,
            "revenue_volatility": 0.18,
        }

        risk_assessment = {
            "risk_level": "LOW",
            "flags": [],
            "positive_signals": ["Strong DSCR", "Low volatility"]
        }

        recommendation = {
            "decision": "APPROVE",
            "conditions": []
        }

        prompt = build_credit_memo_prompt(
            business_info, metrics, risk_assessment, recommendation
        )

        # Check prompt includes key information
        assert "ABC Construction LLC" in prompt
        assert "Construction" in prompt
        assert "$50,000" in prompt or "50000" in prompt
        assert "1.45" in prompt or "DSCR" in prompt
        assert "APPROVE" in prompt

    def test_build_credit_memo_prompt_with_conditions(self):
        """Test prompt with conditional approval."""
        from agents.memo_generator import build_credit_memo_prompt

        business_info = {
            "business_name": "XYZ Manufacturing",
            "industry": "Manufacturing",
            "loan_amount": 75000,
        }

        metrics = {"avg_monthly_revenue": 35000, "dscr": 1.28}

        risk_assessment = {
            "risk_level": "MODERATE",
            "flags": [{"severity": "MEDIUM", "flag": "UNSTABLE_REVENUE"}],
            "positive_signals": []
        }

        recommendation = {
            "decision": "APPROVE_WITH_CONDITIONS",
            "conditions": ["Require personal guarantee", "Quarterly reporting"]
        }

        prompt = build_credit_memo_prompt(
            business_info, metrics, risk_assessment, recommendation
        )

        assert "XYZ Manufacturing" in prompt
        assert "APPROVE_WITH_CONDITIONS" in prompt or "conditional" in prompt.lower()
        assert "personal guarantee" in prompt.lower() or "conditions" in prompt.lower()


class TestMemoGeneratorAgent:
    """Test MemoGeneratorAgent class."""

    @pytest.fixture
    def sample_business_info(self) -> Dict:
        """Sample business information."""
        return {
            "business_name": "ABC Construction LLC",
            "industry": "Construction",
            "loan_amount": 50000,
            "business_age_years": 5,
        }

    @pytest.fixture
    def sample_financial_metrics(self) -> Dict:
        """Sample financial metrics."""
        return {
            "metrics": {
                "avg_monthly_revenue": 45000,
                "revenue_volatility": 0.18,
                "avg_monthly_cash_flow": 10000,
                "dscr": 1.45,
                "debt_to_revenue": 0.35,
                "annual_revenue": 540000,
                "net_income": 120000,
                "stability_score": 72,
                "revenue_trend": 0.10,
            }
        }

    @pytest.fixture
    def sample_risk_assessment(self) -> Dict:
        """Sample risk assessment."""
        return {
            "risk_assessment": {
                "risk_level": "LOW",
                "flags": [],
                "positive_signals": [
                    "Strong DSCR",
                    "Low revenue volatility",
                    "Clean payment history"
                ],
            }
        }

    @patch("agents.memo_generator.OpenAI")
    def test_agent_generate_memo_structure(
        self,
        mock_openai,
        sample_business_info,
        sample_financial_metrics,
        sample_risk_assessment
    ):
        """Test that agent returns correct structure."""
        # Mock OpenAI response
        mock_client = Mock()
        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content="This is a test credit memo."))]
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client

        from agents.memo_generator import MemoGeneratorAgent

        agent = MemoGeneratorAgent(api_key="test-key")
        result = agent.generate(
            sample_business_info,
            sample_financial_metrics,
            sample_risk_assessment
        )

        # Check structure
        assert "credit_memo_output" in result
        output = result["credit_memo_output"]

        assert "credit_memo" in output
        assert "recommendation" in output
        assert "underwriting_score" in output
        assert "conditions" in output or "reasons" in output

    @patch("agents.memo_generator.OpenAI")
    def test_agent_calls_openai_with_correct_params(
        self,
        mock_openai,
        sample_business_info,
        sample_financial_metrics,
        sample_risk_assessment
    ):
        """Test that OpenAI is called with correct parameters."""
        # Mock OpenAI response
        mock_client = Mock()
        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content="Credit memo content"))]
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client

        from agents.memo_generator import MemoGeneratorAgent

        agent = MemoGeneratorAgent(api_key="test-key")
        agent.generate(
            sample_business_info,
            sample_financial_metrics,
            sample_risk_assessment
        )

        # Verify OpenAI was called
        mock_client.chat.completions.create.assert_called_once()
        call_args = mock_client.chat.completions.create.call_args

        # Check parameters
        assert call_args.kwargs["model"] == "gpt-4o-mini"
        assert "messages" in call_args.kwargs
        assert len(call_args.kwargs["messages"]) > 0

    @patch("agents.memo_generator.OpenAI")
    def test_agent_handles_openai_error(
        self,
        mock_openai,
        sample_business_info,
        sample_financial_metrics,
        sample_risk_assessment
    ):
        """Test agent handles OpenAI API errors gracefully."""
        # Mock OpenAI error
        mock_client = Mock()
        mock_client.chat.completions.create.side_effect = Exception("API Error")
        mock_openai.return_value = mock_client

        from agents.memo_generator import MemoGeneratorAgent

        agent = MemoGeneratorAgent(api_key="test-key")
        result = agent.generate(
            sample_business_info,
            sample_financial_metrics,
            sample_risk_assessment
        )

        # Should still return structure with fallback content
        assert "credit_memo_output" in result
        output = result["credit_memo_output"]

        # Should have fallback memo
        assert "credit_memo" in output
        assert "error" in output["credit_memo"].lower() or "unable" in output["credit_memo"].lower()

    def test_agent_without_openai_key(
        self,
        sample_business_info,
        sample_financial_metrics,
        sample_risk_assessment
    ):
        """Test agent can work without OpenAI key (fallback mode)."""
        from agents.memo_generator import MemoGeneratorAgent

        agent = MemoGeneratorAgent(api_key=None)
        result = agent.generate(
            sample_business_info,
            sample_financial_metrics,
            sample_risk_assessment
        )

        # Should return structured output even without LLM
        assert "credit_memo_output" in result
        output = result["credit_memo_output"]

        assert "credit_memo" in output
        assert "recommendation" in output
        assert "underwriting_score" in output
