from decimal import Decimal

import pytest

from app.policy.entity import Policy
from app.policy.use_cases.policy_limit_calculation import PolicyCalculation


@pytest.fixture
def policy_calculation():
    return PolicyCalculation(
        coverage_percentage=Decimal("0.8"),
        deductible_percentage=Decimal("0.1"),
    )


class TestPolicyCalculation:
    def test_get_base_policy_limit(self, policy_calculation, car):
        base_policy_limit = policy_calculation.get_base_policy_limit(car)
        assert base_policy_limit == Decimal(
            20000
        ), "Base policy limit calculation is incorrect"

    def test_get_deductible_value(self, policy_calculation):
        base_policy_limit = Decimal(16000)
        deductible_value = policy_calculation.get_deductible_value(base_policy_limit)
        assert deductible_value == Decimal(
            1600
        ), "Deductible value calculation is incorrect"

    def test_get_final_policy_limit(self, policy_calculation):
        base_policy_limit = Decimal(16000)
        deductible_value = Decimal(1600)
        final_policy_limit = policy_calculation.get_final_policy_limit(
            base_policy_limit, deductible_value
        )
        assert final_policy_limit == Decimal(
            14400
        ), "Final policy limit calculation is incorrect"

    def test_execute(self, policy_calculation, car):
        policy = policy_calculation.execute(car)
        assert isinstance(policy, Policy), "Result should be an instance of Policy"
        assert policy.deductible_value == Decimal(
            2000
        ), "Deductible value in Policy is incorrect"
        assert policy.policy_limit == Decimal(
            18000
        ), "Policy limit in Policy is incorrect"
