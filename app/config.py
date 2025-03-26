from decimal import Decimal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Environment
    ENVIRONMENT: str = "DEV"

    # Project
    PROJECT_NAME: str = "Car Insurance Simulator API Back-End"

    # Api
    API_NAME: str = "car-insurance-simulator-api-back-end"

    # API
    API_V1_STR: str = "/v1"
    API_ERROR_MORE_INFO: str = "https://github.com/AgroBrasil/test"

    # Logger
    LOG_LEVEL: int = 20  # INFO

    # Security
    ALLOWED_HOSTS: list[str] = ["*"]

    # Language Client
    CLIENT_LOCALE: str = "en_US"

    INSURANCE_BROKER_FEE: Decimal = Decimal("50.0")
    INSURANCE_COVERAGE_PERCENTAGE: Decimal = Decimal("1.0")
    INSURANCE_DEDUCTIBLE_PERCENTAGE: Decimal = Decimal("0.1")
    INSURANCE_RATE_PER_YEAR: Decimal = Decimal("0.005")
    INSURANCE_RATE_PER_VALUE: Decimal = Decimal("0.005")
    INSURANCE_FRACTIONAL_VALUE: Decimal = Decimal(10000)
    GIS_ADJUSTMENT_MIN: Decimal = Decimal("-0.02")
    GIS_ADJUSTMENT_MAX: Decimal = Decimal("0.02")

    if ENVIRONMENT == "DEV":
        SONAR_TOKEN: str = ""

        model_config = SettingsConfigDict(
            env_file=".env",
            env_file_encoding="utf-8",
        )


settings = Settings()
