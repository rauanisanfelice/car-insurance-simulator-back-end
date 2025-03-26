import re

from pydantic import Field, field_validator
from pydantic_extra_types.country import CountryAlpha2

from app.shared.models import EntityModel


class Address(EntityModel):
    contry: CountryAlpha2 = Field(default="BR", examples=["BR"])
    zipcode: str = Field(max_length=9, examples=["12345-678"])
    state: str = Field(max_length=2)
    city: str
    street: str
    neighborhood: str
    address_number: str = Field(max_length=10)
    address_complement: str | None

    @field_validator("zipcode")
    @classmethod
    def validate_code(cls, value: str) -> str:
        re_code = r"^\d{5}-\d{3}$"
        if not re.match(re_code, value):
            msg = "Zipcode deve ter o seguinte padrão XXXXX-XXX"
            raise ValueError(msg)

        return value
