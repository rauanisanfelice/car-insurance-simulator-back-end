from decimal import Decimal

import pytest

from app.insurance.use_cases.premium_calculation import PremiumCalculation


@pytest.fixture
def premium_calculation():
    return PremiumCalculation(
        coverage_percentage=Decimal("0.8"),
        deductible_percentage=Decimal("0.1"),
        brooker_fee=Decimal("50.00"),
    )


class TestPremiumCalculation:
    def test_get_base_premium(self, premium_calculation, car):
        applied_rate = Decimal("0.05")
        base_premium = premium_calculation.get_base_premium(car, applied_rate)
        assert base_premium == Decimal("1250.0000")

    def test_get_deductible_discount(self, premium_calculation):
        base_premium = Decimal("1000.00")
        deductible_discount = premium_calculation.get_deductible_discount(base_premium)
        assert deductible_discount == Decimal("100.00")

    def test_get_final_premium(self, premium_calculation):
        base_premium = Decimal("1000.00")
        deductible_discount = Decimal("100.00")
        final_premium = premium_calculation.get_final_premium(
            base_premium, deductible_discount
        )
        assert final_premium == Decimal("950.00")

    def test_execute(self, premium_calculation, car):
        applied_rate = Decimal("0.05")
        final_premium = premium_calculation.execute(car, applied_rate)
        assert final_premium == Decimal("1175.00000")
