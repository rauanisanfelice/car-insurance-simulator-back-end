from datetime import datetime, timezone
from decimal import Decimal
from unittest.mock import patch

import pytest

from app.insurance.use_cases.dynamic_rate_calculation import DynamicRateCalculation


@pytest.fixture
def dynamic_rate_calculation():
    return DynamicRateCalculation(
        rate_per_year=Decimal(100),
        fractional_value=Decimal(1000),
        rate_per_value=Decimal(10),
    )


class TestDynamicRateCalculation:
    def test_get_car_years(self, dynamic_rate_calculation):
        with patch(
            "app.insurance.use_cases.dynamic_rate_calculation.datetime"
        ) as mock_datetime:
            mock_datetime.now.return_value = datetime(2023, 1, 1, tzinfo=timezone.utc)
            car_years = dynamic_rate_calculation._get_car_years(2015)
            assert car_years == 8

    def test_calculate_rate_per_year(self, dynamic_rate_calculation, car):
        with patch(
            "app.insurance.use_cases.dynamic_rate_calculation.datetime"
        ) as mock_datetime:
            mock_datetime.now.return_value = datetime(2023, 1, 1, tzinfo=timezone.utc)
            rate_per_year = dynamic_rate_calculation.calculate_rate_per_year(car)
            assert rate_per_year == Decimal(300)

    def test_get_fractional_value(self, dynamic_rate_calculation):
        fractional_value = dynamic_rate_calculation._get_fractional_value(
            Decimal(20000)
        )
        assert fractional_value == 20

    def test_calculate_rate_per_value(self, dynamic_rate_calculation, car):
        rate_per_value = dynamic_rate_calculation.calculate_rate_per_value(car)
        assert rate_per_value == Decimal(250)

    def test_calculate_rate(self, dynamic_rate_calculation):
        rate = dynamic_rate_calculation.calculate_rate(
            rate_per_year=Decimal(800),
            rate_per_value=Decimal(200),
        )
        assert rate == Decimal(1000)

    def test_execute(self, dynamic_rate_calculation, car):
        with (
            patch(
                "app.insurance.use_cases.dynamic_rate_calculation.logger"
            ) as mock_logger,  # noqa: F841
            patch(
                "app.insurance.use_cases.dynamic_rate_calculation.datetime"
            ) as mock_datetime,
        ):
            mock_datetime.now.return_value = datetime(2023, 1, 1, tzinfo=timezone.utc)
            rate = dynamic_rate_calculation.execute(car)
            assert rate == Decimal(550)
