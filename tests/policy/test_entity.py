from decimal import Decimal

from app.policy.entity import Policy


class TestPolicyEntity:
    def test_policy_entity_creation_success(self) -> None:
        policy_data = {
            "deductible_value": Decimal("500.00"),
            "policy_limit": Decimal("100000.00"),
        }
        policy = Policy(**policy_data)

        assert policy is not None
        assert policy.deductible_value == Decimal("500.00")
        assert policy.policy_limit == Decimal("100000.00")
