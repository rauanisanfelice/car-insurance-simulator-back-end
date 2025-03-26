from datetime import datetime, timezone
from decimal import Decimal

from pydantic import Field, field_validator

from app.locale.messages import APPLICATION_YEAR_VALIDATION_ERROR
from app.shared.models import EntityModel


class Car(EntityModel):
    make: str
    model: str
    year: int
    value: Decimal = Field(
        max_digits=6,
        decimal_places=2,
        gt=0,
    )

    @field_validator("year")
    @classmethod
    def year_must_be_valid(cls, date: int) -> int:
        minimum_year: int = 1900
        if date < minimum_year or date > datetime.now(tz=timezone.utc).year:
            raise ValueError(APPLICATION_YEAR_VALIDATION_ERROR)
        return date
