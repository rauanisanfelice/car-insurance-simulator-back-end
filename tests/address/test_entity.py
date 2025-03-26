import pytest

from app.insurance.entity import Address


class TestEntityClient:
    @pytest.mark.asyncio
    async def test_entity_return_client(self) -> None:
        address_create = {
            "contry": "BR",
            "zipcode": "88000-600",
            "state": "SC",
            "city": "Floripa",
            "neighborhood": "Carianos",
            "street": "Rua da magia",
            "address_number": "837B",
            "address_complement": None,
        }
        result = Address(**address_create)

        assert result is not None
        assert result.contry == "BR"
        assert result.zipcode == "88000-600"
        assert result.state == "SC"
        assert result.city == "Floripa"
        assert result.street == "Rua da magia"
        assert result.address_number == "837B"

    @pytest.mark.asyncio
    async def test_entity_return_error_code_invalid(self) -> None:
        address_create = {
            "contry": "BR",
            "zipcode": "88000600",
            "state": "SC",
            "city": "Floripa",
            "neighborhood": "Carianos",
            "street": "Rua da magia",
            "address_number": "837B",
            "address_complement": None,
        }
        with pytest.raises(ValueError) as ex:
            Address(**address_create)

        assert (
            "Address\nzipcode\n  Value error, Zipcode deve ter o seguinte padrão XXXXX-XXX"
            in str(
                ex.value,
            )
        )

    @pytest.mark.asyncio
    async def test_entity_return_error_country_invalid(self) -> None:
        address_create = {
            "contry": "BRRRRR",
            "zipcode": "88000-600",
            "state": "SC",
            "city": "Floripa",
            "neighborhood": "Carianos",
            "street": "Rua da magia",
            "address_number": "837B",
            "address_complement": None,
        }
        with pytest.raises(ValueError) as ex:
            Address(**address_create)

        assert "Address\ncontry\n  Invalid country alpha2 code" in str(ex.value)
