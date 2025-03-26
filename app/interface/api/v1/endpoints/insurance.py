from fastapi import APIRouter
from fastapi import status as status_code
from starlette.responses import JSONResponse

from app.config import settings
from app.insurance.entity import (
    InsuranceInputDto,
    InsuranceOutputDto,
)
from app.insurance.use_cases.dynamic_rate_calculation import (
    DynamicRateCalculation,
)
from app.insurance.use_cases.get_car_insurance import GetInsurance
from app.insurance.use_cases.premium_calculation import PremiumCalculation
from app.interface.api.error_schema import ApiError
from app.policy.use_cases.policy_limit_calculation import PolicyCalculation

router = APIRouter()


@router.post(
    "",
    response_model=InsuranceOutputDto,
    status_code=status_code.HTTP_200_OK,
)
async def calculate_insurance(
    payload: InsuranceInputDto,
) -> InsuranceOutputDto | JSONResponse:
    try:
        dynamic_rate_calculation = DynamicRateCalculation(
            rate_per_year=settings.INSURANCE_RATE_PER_YEAR,
            rate_per_value=settings.INSURANCE_RATE_PER_VALUE,
            fractional_value=settings.INSURANCE_FRACTIONAL_VALUE,
        )
        premium_calculation = PremiumCalculation(
            coverage_percentage=settings.INSURANCE_COVERAGE_PERCENTAGE,
            deductible_percentage=settings.INSURANCE_DEDUCTIBLE_PERCENTAGE,
            brooker_fee=settings.INSURANCE_BROKER_FEE,
        )
        policy_calculation = PolicyCalculation(
            coverage_percentage=settings.INSURANCE_COVERAGE_PERCENTAGE,
            deductible_percentage=settings.INSURANCE_DEDUCTIBLE_PERCENTAGE,
        )
        get_insurance_uc = GetInsurance(
            dynamic_rate_calculation=dynamic_rate_calculation,
            premium_calculation=premium_calculation,
            policy_calculation=policy_calculation,
        )
        return await get_insurance_uc.execute(
            input_dto=payload,
        )

    except Exception as ex:  # noqa: BLE001
        api_error = ApiError(developer_message=f"Error - {ex!s}", error_code=0)
        return JSONResponse(
            status_code=status_code.HTTP_500_INTERNAL_SERVER_ERROR,
            content=api_error.model_dump(),
        )
