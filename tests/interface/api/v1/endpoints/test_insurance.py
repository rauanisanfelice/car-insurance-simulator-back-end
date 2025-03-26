import json
from unittest.mock import AsyncMock, patch

import pytest
from fastapi import status

from app.interface.api.error_schema import ApiError


class TestEndpointsInsurance:
    @pytest.mark.asyncio
    async def test_calculate_insurance_success(
        self, client_test_default, mock_insurance_input_dto, mock_insurance_output_dto
    ):
        with patch(
            "app.insurance.use_cases.get_car_insurance.GetInsurance.execute",
            new_callable=AsyncMock,
        ) as mock_execute:
            mock_execute.return_value = mock_insurance_output_dto

            response = client_test_default.post(
                url="/v1/insurance", data=mock_insurance_input_dto.json()
            )

            assert response.status_code == status.HTTP_200_OK, response.content
            assert response.json() == json.loads(
                mock_insurance_output_dto.model_dump_json()
            )
            mock_execute.assert_called_once_with(input_dto=mock_insurance_input_dto)

    @pytest.mark.asyncio
    async def test_calculate_insurance_expected_500_error(
        self, client_test_default, mock_insurance_input_dto
    ):
        mock_error_message = "Some error occurred"

        with patch(
            "app.insurance.use_cases.get_car_insurance.GetInsurance.execute",
            new_callable=AsyncMock,
        ) as mock_execute:
            mock_execute.side_effect = Exception(mock_error_message)

            response = client_test_default.post(
                url="/v1/insurance", data=mock_insurance_input_dto.json()
            )

            assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
            assert (
                response.json()
                == ApiError(
                    developer_message=f"Error - {mock_error_message}", error_code=0
                ).model_dump()
            )
            mock_execute.assert_called_once_with(input_dto=mock_insurance_input_dto)

    @pytest.mark.asyncio
    async def test_calculate_insurance_expected_422_error(
        self, client_test_default, mock_insurance_input_dto
    ):
        mock_error_message = "Some error occurred"

        with patch(
            "app.insurance.use_cases.get_car_insurance.GetInsurance.execute",
            new_callable=AsyncMock,
        ) as mock_execute:
            mock_execute.side_effect = Exception(mock_error_message)

            response = client_test_default.post(
                url="/v1/insurance", data=mock_insurance_input_dto.dict()
            )

            assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
            result = json.loads(response.content.decode("utf-8"))
            assert result["error_code"] == 1000
