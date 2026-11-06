from datetime import datetime
from enum import StrEnum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field

from .subscriptions_settings import CustomRemarksDto, HwidSettingsDto


class TemplateType(StrEnum):
    """Template type enum"""

    XRAY_JSON = "XRAY_JSON"
    XRAY_BASE64 = "XRAY_BASE64"
    MIHOMO = "MIHOMO"
    STASH = "STASH"
    CLASH = "CLASH"
    SINGBOX = "SINGBOX"


class ExternalSquadInfoDto(BaseModel):
    """External squad info"""

    members_count: float = Field(alias="membersCount")


class ExternalSquadTemplateDto(BaseModel):
    """External squad template"""

    template_uuid: UUID = Field(alias="templateUuid")
    template_type: TemplateType = Field(alias="templateType")


class ExternalSquadSubscriptionSettingsDto(BaseModel):
    """External squad subscription settings"""

    serve_json_at_base_subscription: Optional[bool] = Field(
        None, alias="serveJsonAtBaseSubscription"
    )
    is_show_custom_remarks: Optional[bool] = Field(None, alias="isShowCustomRemarks")
    randomize_hosts: Optional[bool] = Field(None, alias="randomizeHosts")


class ExternalSquadHostOverridesDto(BaseModel):
    """External squad host overrides"""

    server_description: Optional[str] = Field(
        None, alias="serverDescription", max_length=30
    )
    vless_route_id: Optional[int] = Field(None, alias="vlessRouteId", ge=0, le=65535)


class ExternalSquadDto(BaseModel):
    """External squad data model"""

    uuid: UUID
    view_position: int = Field(alias="viewPosition")
    tags: list[str] = Field(default_factory=list, description="Panel 3.4.0+.")
    name: str
    info: ExternalSquadInfoDto
    templates: list[ExternalSquadTemplateDto]
    subscription_settings: Optional[ExternalSquadSubscriptionSettingsDto] = Field(
        None, alias="subscriptionSettings"
    )
    host_overrides: Optional[ExternalSquadHostOverridesDto] = Field(
        None, alias="hostOverrides"
    )
    response_headers_add: Optional[dict[str, str]] = Field(
        None, alias="responseHeadersAdd"
    )
    response_headers_remove: Optional[list[str]] = Field(
        None, alias="responseHeadersRemove"
    )
    hwid_settings: Optional[HwidSettingsDto] = Field(None, alias="hwidSettings")
    custom_remarks: Optional[CustomRemarksDto] = Field(None, alias="customRemarks")
    subpage_config_uuid: Optional[UUID] = Field(None, alias="subpageConfigUuid")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


# Request/Response models
class GetExternalSquadsResponseDto(BaseModel):
    """Response with all external squads"""

    total: float = Field(alias="total")
    external_squads: list[ExternalSquadDto] = Field(alias="externalSquads")


class GetExternalSquadByUuidResponseDto(ExternalSquadDto):
    """Response with external squad by UUID"""

    pass


class CreateExternalSquadRequestDto(BaseModel):
    """Request to create external squad"""

    name: str = Field(min_length=2, max_length=30, pattern=r"^[A-Za-z0-9_\s-]+$")


class CreateExternalSquadResponseDto(ExternalSquadDto):
    """Response after creating external squad"""

    pass


class UpdateExternalSquadRequestDto(BaseModel):
    """Request to update external squad"""

    uuid: UUID
    name: Optional[str] = Field(
        None, min_length=2, max_length=30, pattern=r"^[A-Za-z0-9_\s-]+$"
    )
    templates: Optional[list[ExternalSquadTemplateDto]] = None
    subscription_settings: Optional[ExternalSquadSubscriptionSettingsDto] = Field(
        None, serialization_alias="subscriptionSettings"
    )
    host_overrides: Optional[ExternalSquadHostOverridesDto] = Field(
        None, serialization_alias="hostOverrides"
    )
    hwid_settings: Optional[HwidSettingsDto] = Field(None, alias="hwidSettings")
    custom_remarks: Optional[CustomRemarksDto] = Field(None, alias="customRemarks")
    response_headers_add: Optional[dict[str, str]] = Field(
        None, serialization_alias="responseHeadersAdd"
    )
    response_headers_remove: Optional[list[str]] = Field(
        None, serialization_alias="responseHeadersRemove"
    )
    subpage_config_uuid: Optional[UUID] = Field(
        None, serialization_alias="subpageConfigUuid"
    )


class UpdateExternalSquadResponseDto(ExternalSquadDto):
    """Response after updating external squad"""

    pass


class ReorderExternalSquadItem(BaseModel):
    view_position: int = Field(serialization_alias="viewPosition")
    uuid: UUID


class ReorderExternalSquadsRequestDto(BaseModel):
    items: list[ReorderExternalSquadItem]


class ReorderExternalSquadsResponseDto(BaseModel):
    """Response after reordering external squads"""

    total: float = Field(alias="total")
    external_squads: list[ExternalSquadDto] = Field(alias="externalSquads")
