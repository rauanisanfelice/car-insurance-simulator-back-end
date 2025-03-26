from decimal import Decimal

from app.shared.models import EntityModel


class Policy(EntityModel):
    deductible_value: Decimal
    policy_limit: Decimal
