from datetime import datetime
from typing import Annotated, Any, Optional
from uuid import UUID

from pydantic import BaseModel, Field, StringConstraints


class InboundDto(BaseModel):
    uuid: UUID
    profile_uuid: UUID = Field(alias="profileUuid")
    tag: str
    type: str
    network: Optional[str] = None
    security: Optional[str] = None
    port: Optional[float] = None
    raw_inbound: Optional[Any] = Field(None, alias="rawInbound")


class NodesProfileDto(BaseModel):
    uuid: UUID
    name: str
    country_code: str = Field(alias="countryCode")


class ConfigProfileDto(BaseModel):
    uuid: UUID
    name: str
    view_position: int = Field(alias="viewPosition")
    tags: list[str] = Field(default_factory=list, description="Panel 3.4.0+.")
    config: dict[str, Any]
    inbounds: list[InboundDto]
    nodes: list[NodesProfileDto] = []
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class CreateConfigProfileRequestDto(BaseModel):
    name: Annotated[
        str,
        StringConstraints(min_length=2, max_length=30, pattern=r"^[A-Za-z0-9_\s-]+$"),
    ]
    config: dict[str, Any]


class CreateConfigProfileResponseDto(ConfigProfileDto):
    pass


class UpdateConfigProfileRequestDto(BaseModel):
    uuid: UUID
    name: Optional[
        Annotated[
            str,
            StringConstraints(
                min_length=2, max_length=30, pattern=r"^[A-Za-z0-9_\s-]+$"
            ),
        ]
    ] = None
    config: Optional[dict[str, Any]] = None


class UpdateConfigProfileResponseDto(ConfigProfileDto):
    pass


class GetAllConfigProfilesResponsePaginated(BaseModel):
    total: float
    config_profiles: list[ConfigProfileDto] = Field(alias="configProfiles")


class GetAllConfigProfilesResponseDto(GetAllConfigProfilesResponsePaginated):
    pass


class GetConfigProfileByUuidResponseDto(ConfigProfileDto):
    pass


class GetAllInboundsResponseDto(list[InboundDto]):
    pass


class GetInboundsByProfileUuidResponseDto(list[InboundDto]):
    pass


class ReorderConfigProfileItem(BaseModel):
    view_position: int = Field(serialization_alias="viewPosition")
    uuid: UUID


class ReorderConfigProfilesRequestDto(BaseModel):
    items: list[ReorderConfigProfileItem]


class ReorderConfigProfilesResponseDto(GetAllConfigProfilesResponsePaginated):
    pass
