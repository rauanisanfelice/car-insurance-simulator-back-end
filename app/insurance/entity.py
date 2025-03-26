from decimal import Decimal

from pydantic import UUID4

from app.address.entity import Address
from app.car.entity import Car
from app.shared.models import EntityModel


class InsuranceInputDto(EntityModel):
    car: Car
    deductible_percentage: Decimal
    broker_fee: Decimal
    registration_location: Address | None = None


class InsuranceOutputDto(EntityModel):
    id: UUID4
    car: Car
    applied_rate: Decimal
    policy_limit: Decimal
    calculated_premium: Decimal
    deductible_value: Decimal
