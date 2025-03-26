from decimal import Decimal
from unittest.mock import Mock

import pytest

from app.insurance.entity import InsuranceInputDto, InsuranceOutputDto
from app.insurance.use_cases.get_car_insurance import GetInsurance
from app.policy.entity import Policy


class TestGetInsurance:
    @pytest.mark.asyncio
    async def test_get_insurance_execute(self, car):
        dynamic_rate_calculation = Mock()
        premium_calculation = Mock()
        policy_calculation = Mock()

        dynamic_rate_calculation.execute.return_value = Decimal("0.05")
        premium_calculation.execute.return_value = Decimal("500.00")
        policy_calculation.execute.return_value = Policy(
            policy_limit=Decimal("10000.00"),
            deductible_value=Decimal("1000.00"),
        )

        get_insurance = GetInsurance(
            dynamic_rate_calculation=dynamic_rate_calculation,
            premium_calculation=premium_calculation,
            policy_calculation=policy_calculation,
        )

        input_dto = InsuranceInputDto(
            car=car,
            deductible_percentage=10,
            broker_fee=30,
            registration_location=None,
        )

        result = await get_insurance.execute(input_dto)

        assert isinstance(result, InsuranceOutputDto)
        assert result.applied_rate == Decimal("0.05")
        assert result.calculated_premium == Decimal("500.00")
        assert result.policy_limit == Decimal("10000.00")
        assert result.deductible_value == Decimal("1000.00")

        dynamic_rate_calculation.execute.assert_called_once_with(car=car)
        premium_calculation.execute.assert_called_once_with(
            car=car, applied_rate=Decimal("0.05")
        )
        policy_calculation.execute.assert_called_once_with(car=car)
