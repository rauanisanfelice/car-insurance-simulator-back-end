from decimal import Decimal

import pytest

from app.address.entity import Address
from app.car.entity import Car


@pytest.fixture
def car() -> Car:
    return Car(
        make="Toyota",
        model="Camry",
        year=2020,
        value=Decimal("25000.00"),
    )


@pytest.fixture
def address() -> Address:
    return Address(
        street="1234 Main St",
        city="Springfield",
        state="IL",
        zipcode="12345-678",
        neighborhood="Downtown",
        address_number="1234",
        address_complement="Apt 1",
    )
