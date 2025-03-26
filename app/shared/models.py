from pydantic import AliasGenerator, BaseModel, ConfigDict
from pydantic.alias_generators import to_snake


class EntityModel(BaseModel):
    """Base class for all models."""

    model_config = ConfigDict(
        extra="ignore",
        populate_by_name=True,
        use_enum_values=True,
        validate_assignment=True,
        alias_generator=AliasGenerator(
            validation_alias=to_snake,
            serialization_alias=to_snake,
        ),
    )
