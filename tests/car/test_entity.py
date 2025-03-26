from datetime import datetime, timezone
from decimal import Decimal

import pytest

from app.car.entity import Car
from app.locale.messages import APPLICATION_YEAR_VALIDATION_ERROR


class TestCarEntity:
    def test_car_entity_creation_success(self) -> None:
        car_data = {
            "make": "Toyota",
            "model": "Corolla",
            "year": 2020,
            "value": Decimal("1250000.00"),
        }
        car = Car(**car_data)

        assert car is not None
        assert car.make == "Toyota"
        assert car.model == "Corolla"
        assert car.year == 2020
        assert car.value == Decimal("1250000.00")

    def test_car_entity_invalid_year_too_old(self) -> None:
        car_data = {
            "make": "Ford",
            "model": "Model T",
            "year": 1800,
            "value": Decimal("10000.00"),
        }
        with pytest.raises(ValueError) as ex:
            Car(**car_data)

        assert APPLICATION_YEAR_VALIDATION_ERROR in str(ex.value)

    def test_car_entity_invalid_year_in_future(self) -> None:
        future_year = datetime.now(tz=timezone.utc).year + 1
        car_data = {
            "make": "Tesla",
            "model": "Model S",
            "year": future_year,
            "value": Decimal("80000.00"),
        }
        with pytest.raises(ValueError) as ex:
            Car(**car_data)

        assert APPLICATION_YEAR_VALIDATION_ERROR in str(ex.value)

    def test_car_entity_invalid_value_negative(self) -> None:
        car_data = {
            "make": "Honda",
            "model": "Civic",
            "year": 2015,
            "value": Decimal("-5000.00"),
        }
        with pytest.raises(ValueError):
            Car(**car_data)

    def test_car_entity_invalid_value_zero(self) -> None:
        car_data = {
            "make": "Chevrolet",
            "model": "Camaro",
            "year": 2018,
            "value": Decimal("0.00"),
        }
        with pytest.raises(ValueError):
            Car(**car_data)
