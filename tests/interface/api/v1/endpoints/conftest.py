import uuid

import pytest

from app.car.entity import Car
from app.insurance.entity import InsuranceInputDto, InsuranceOutputDto


@pytest.fixture
def mock_insurance_input_dto(car: Car) -> InsuranceInputDto:
    return InsuranceInputDto(
        car=car,
        deductible_percentage=0.1,
        broker_fee=0.1,
        registration_location=None,
    )


@pytest.fixture
def mock_insurance_output_dto(car: Car) -> InsuranceOutputDto:
    return InsuranceOutputDto(
        id=uuid.uuid4(),
        car=car,
        applied_rate=0.1,
        policy_limit=1000,
        calculated_premium=100,
        deductible_value=100,
    )
