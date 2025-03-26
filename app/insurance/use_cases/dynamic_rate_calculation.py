from abc import ABC, abstractmethod
from datetime import datetime, timezone
from decimal import Decimal

from app.car.entity import Car
from app.infrastructure.services.logging import logger


class DynamicRateCalculationInterface(ABC):
    @abstractmethod
    def calculate_rate_per_year(self, car: Car) -> Decimal:
        raise NotImplementedError

    @abstractmethod
    def calculate_rate_per_value(self, car: Car) -> Decimal:
        raise NotImplementedError

    @abstractmethod
    def calculate_rate(
        self,
        rate_per_year: Decimal,
        rate_per_value: Decimal,
    ) -> Decimal:
        raise NotImplementedError

    @abstractmethod
    def execute(self, car: Car) -> Decimal:
        raise NotImplementedError


class DynamicRateCalculation(DynamicRateCalculationInterface):
    def __init__(
        self,
        rate_per_year: Decimal,
        fractional_value: Decimal,
        rate_per_value: Decimal,
    ):
        self.rate_per_year = rate_per_year
        self.fractional_value = fractional_value
        self.rate_per_value = rate_per_value

    def _get_car_years(self, year: int) -> int:
        today = datetime.now(timezone.utc)
        return today.year - year

    def calculate_rate_per_year(self, car: Car) -> Decimal:
        rate_per_year = self._get_car_years(year=car.year) * self.rate_per_year
        logger.debug("Rate per year %s", rate_per_year)
        return rate_per_year

    def _get_fractional_value(self, value: Decimal) -> int:
        return int(value / self.fractional_value)

    def calculate_rate_per_value(self, car: Car) -> Decimal:
        rate_per_value = (
            self._get_fractional_value(value=car.value) * self.rate_per_value
        )
        logger.debug("Rate per value %s", rate_per_value)
        return rate_per_value

    def calculate_rate(
        self,
        rate_per_year: Decimal,
        rate_per_value: Decimal,
    ) -> Decimal:
        rate = rate_per_year + rate_per_value
        logger.debug("Rate calculated %s", rate)
        return rate

    def execute(self, car: Car) -> Decimal:
        logger.info("Calculating rate")
        rate_per_year = self.calculate_rate_per_year(car)
        rate_per_value = self.calculate_rate_per_value(car)

        return self.calculate_rate(
            rate_per_year=rate_per_year,
            rate_per_value=rate_per_value,
        )
