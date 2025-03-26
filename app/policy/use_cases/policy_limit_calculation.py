from abc import ABC, abstractmethod
from decimal import Decimal

from app.car.entity import Car
from app.infrastructure.services.logging import logger
from app.policy.entity import Policy


class PolicyCalculationInterface(ABC):
    @abstractmethod
    def get_base_policy_limit(self, car: Car) -> Decimal:
        raise NotImplementedError

    @abstractmethod
    def get_deductible_value(self, base_policy_limit: Decimal) -> Decimal:
        raise NotImplementedError

    @abstractmethod
    def get_final_policy_limit(
        self, base_policy_limit: Decimal, deductible_value: Decimal
    ) -> Decimal:
        raise NotImplementedError

    @abstractmethod
    def execute(self, car: Car) -> Policy:
        raise NotImplementedError


class PolicyCalculation(PolicyCalculationInterface):
    def __init__(
        self,
        coverage_percentage: Decimal,
        deductible_percentage: Decimal,
    ):
        self.coverage_percentage = coverage_percentage
        self.deductible_percentage = deductible_percentage

    def get_base_policy_limit(
        self,
        car: Car,
    ) -> Decimal:
        base_policy_limit = car.value * self.coverage_percentage
        logger.debug("Base policy limit %s", base_policy_limit)
        return base_policy_limit

    def get_deductible_value(
        self,
        base_policy_limit: Decimal,
    ) -> Decimal:
        deductible_value = base_policy_limit * self.deductible_percentage
        logger.debug("Deductible value %s", deductible_value)
        return deductible_value

    def get_final_policy_limit(
        self,
        base_policy_limit: Decimal,
        deductible_value: Decimal,
    ) -> Decimal:
        final_policy_limit = base_policy_limit - deductible_value
        logger.debug("Final policy limit %s", final_policy_limit)
        return final_policy_limit

    def execute(
        self,
        car: Car,
    ) -> Policy:
        logger.info("Calculating policy")
        base_policy_limit = self.get_base_policy_limit(
            car=car,
        )
        deductible_value = self.get_deductible_value(
            base_policy_limit=base_policy_limit,
        )
        final_policy_limit = self.get_final_policy_limit(
            base_policy_limit=base_policy_limit,
            deductible_value=deductible_value,
        )
        return Policy(
            deductible_value=deductible_value,
            policy_limit=final_policy_limit,
        )
