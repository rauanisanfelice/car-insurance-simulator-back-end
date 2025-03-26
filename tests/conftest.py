from decimal import Decimal

import pytest

from app.car.entity import Car


@pytest.fixture
def car() -> Car:
    return Car(
        make="Toyota",
        model="Camry",
        year=2020,
        value=Decimal("25000.00"),
    )
