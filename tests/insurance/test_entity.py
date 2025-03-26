from decimal import Decimal
from uuid import uuid4

import pytest
from pydantic import ValidationError

from app.insurance.entity import InsuranceInputDto, InsuranceOutputDto


class TestInsuranceInputDto:
    def test_insurance_input_dto_creation_success(self, car, address) -> None:
        insurance_input = InsuranceInputDto(
            car=car,
            deductible_percentage=Decimal("0.10"),
            broker_fee=Decimal("500.00"),
            registration_location=address,
        )

        assert insurance_input.car == car
        assert insurance_input.deductible_percentage == Decimal("0.10")
        assert insurance_input.broker_fee == Decimal("500.00")
        assert insurance_input.registration_location == address

    def test_insurance_input_dto_creation_without_optional_field(self, car) -> None:
        insurance_input = InsuranceInputDto(
            car=car,
            deductible_percentage=Decimal("0.10"),
            broker_fee=Decimal("500.00"),
        )

        assert insurance_input.car == car
        assert insurance_input.deductible_percentage == Decimal("0.10")
        assert insurance_input.broker_fee == Decimal("500.00")
        assert insurance_input.registration_location is None

    def test_insurance_input_dto_invalid_data(self) -> None:
        with pytest.raises(ValidationError):
            InsuranceInputDto(
                car=None,
                deductible_percentage="invalid_decimal",
                broker_fee="invalid_decimal",
            )


class TestInsuranceOutputDto:
    def test_insurance_output_dto_creation_success(self, car) -> None:
        insurance_output = InsuranceOutputDto(
            id=uuid4(),
            car=car,
            applied_rate=Decimal("0.05"),
            policy_limit=Decimal("100000.00"),
            calculated_premium=Decimal("5000.00"),
            deductible_value=Decimal("500.00"),
        )

        assert insurance_output.car == car
        assert insurance_output.applied_rate == Decimal("0.05")
        assert insurance_output.policy_limit == Decimal("100000.00")
        assert insurance_output.calculated_premium == Decimal("5000.00")
        assert insurance_output.deductible_value == Decimal("500.00")

    def test_insurance_output_dto_invalid_data(self) -> None:
        with pytest.raises(ValidationError):
            InsuranceOutputDto(
                id="invalid_uuid",
                car=None,
                applied_rate="invalid_decimal",
                policy_limit="invalid_decimal",
                calculated_premium="invalid_decimal",
                deductible_value="invalid_decimal",
            )
