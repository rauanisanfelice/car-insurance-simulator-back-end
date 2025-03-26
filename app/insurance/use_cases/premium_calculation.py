from abc import ABC, abstractmethod
from decimal import Decimal

from app.car.entity import Car
from app.infrastructure.services.logging import logger


class PremiumCalculationInterface(ABC):
    @abstractmethod
    def get_base_premium(self, car: Car, applied_rate: Decimal) -> Decimal:
        raise NotImplementedError

    @abstractmethod
    def get_deductible_discount(self, base_premium: Decimal) -> Decimal:
        raise NotImplementedError

    @abstractmethod
    def get_final_premium(
        self, base_premium: Decimal, deductible_discount: Decimal
    ) -> Decimal:
        raise NotImplementedError

    @abstractmethod
    def execute(self, car: Car, applied_rate: Decimal) -> Decimal:
        raise NotImplementedError


class PremiumCalculation(PremiumCalculationInterface):
    def __init__(
        self,
        coverage_percentage: Decimal,
        deductible_percentage: Decimal,
        brooker_fee: Decimal,
    ):
        self.coverage_percentage = coverage_percentage
        self.deductible_percentage = deductible_percentage
        self.brooker_fee = brooker_fee

    def get_base_premium(
        self,
        car: Car,
        applied_rate: Decimal,
    ) -> Decimal:
        base_premium = car.value * applied_rate
        logger.debug("Base premium %s", base_premium)
        return base_premium

    def get_deductible_discount(
        self,
        base_premium: Decimal,
    ) -> Decimal:
        deductible_discount = base_premium * self.deductible_percentage
        logger.debug("Deductible discount %s", deductible_discount)
        return deductible_discount

    def get_final_premium(
        self,
        base_premium: Decimal,
        deductible_discount: Decimal,
    ) -> Decimal:
        final_premium = base_premium - deductible_discount + self.brooker_fee
        logger.debug("Final premium %s", final_premium)
        return final_premium

    def execute(
        self,
        car: Car,
        applied_rate: Decimal,
    ) -> Decimal:
        logger.info("Calculating premium rate")
        base_premium = self.get_base_premium(
            car=car,
            applied_rate=applied_rate,
        )
        deductible_discount = self.get_deductible_discount(
            base_premium=base_premium,
        )

        return self.get_final_premium(
            base_premium=base_premium,
            deductible_discount=deductible_discount,
        )
