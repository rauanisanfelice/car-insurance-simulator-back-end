import uuid
from decimal import Decimal
from typing import TYPE_CHECKING

from app.insurance.entity import InsuranceInputDto, InsuranceOutputDto
from app.insurance.use_cases.dynamic_rate_calculation import (
    DynamicRateCalculationInterface,
)
from app.insurance.use_cases.premium_calculation import PremiumCalculationInterface
from app.policy.use_cases.policy_limit_calculation import PolicyCalculationInterface

if TYPE_CHECKING:
    from app.policy.entity import Policy


class GetInsurance:
    def __init__(
        self,
        dynamic_rate_calculation: DynamicRateCalculationInterface,
        premium_calculation: PremiumCalculationInterface,
        policy_calculation: PolicyCalculationInterface,
    ) -> None:
        self.dynamic_rate_calculation = dynamic_rate_calculation
        self.premium_calculation = premium_calculation
        self.policy_calculation = policy_calculation

    def build_entity(
        self,
        input_dto: InsuranceInputDto,
        applied_rate: Decimal,
        policy_limit: Decimal,
        calculated_premium: Decimal,
        deductible_value: Decimal,
    ) -> InsuranceOutputDto:
        return InsuranceOutputDto(
            id=uuid.uuid4(),
            applied_rate=applied_rate,
            policy_limit=policy_limit,
            calculated_premium=calculated_premium,
            deductible_value=deductible_value,
            **input_dto.model_dump(),
        )

    async def execute(self, input_dto: InsuranceInputDto) -> InsuranceOutputDto:
        applied_rate: Decimal = self.dynamic_rate_calculation.execute(
            car=input_dto.car,
        )
        calculated_premium: Decimal = self.premium_calculation.execute(
            car=input_dto.car,
            applied_rate=applied_rate,
        )
        policy: Policy = self.policy_calculation.execute(
            car=input_dto.car,
        )

        return self.build_entity(
            input_dto=input_dto,
            applied_rate=applied_rate,
            policy_limit=policy.policy_limit,
            calculated_premium=calculated_premium,
            deductible_value=policy.deductible_value,
        )
