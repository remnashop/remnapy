from datetime import datetime
from typing import Annotated, Literal, Optional, Union
from uuid import UUID

from pydantic import BaseModel, Field, RootModel, StringConstraints

from remnapy.models.internal_squads import InboundsDto
from remnapy.models.webhook import NodeIpDto, NodeSystemDto, NodeVersionsDto


class ExcludedInbounds(BaseModel):
    uuid: UUID
    tag: str
    type: str
    network: Optional[str] = None
    security: Optional[str] = None


class DeleteResponse(BaseModel):
    is_deleted: bool = Field(alias="isDeleted")


class ReorderNodeItem(BaseModel):
    view_position: int = Field(serialization_alias="viewPosition")
    uuid: UUID


class GetAllNodesTagsResponseDto(BaseModel):
    """Response with all nodes tags"""

    tags: list[str]


class NodeProviderDto(BaseModel):
    """Node provider information"""

    uuid: UUID
    name: str
    favicon_link: Optional[str] = Field(None, alias="faviconLink")
    login_url: Optional[str] = Field(None, alias="loginUrl")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class NodeConfigProfileDto(BaseModel):
    active_config_profile_uuid: Optional[UUID] = Field(alias="activeConfigProfileUuid")
    active_inbounds: list[InboundsDto] = Field(alias="activeInbounds")


class NodeConfigProfileRequestDto(BaseModel):
    active_config_profile_uuid: UUID = Field(alias="activeConfigProfileUuid")
    active_inbounds: list[UUID] = Field(alias="activeInbounds")


class CreateNodeRequestDto(BaseModel):
    name: Annotated[str, StringConstraints(min_length=3, max_length=30)]
    address: Annotated[str, StringConstraints(min_length=2)]
    port: Optional[int] = Field(None, ge=1, le=65535)
    proxy_url: Optional[str] = Field(None, serialization_alias="proxyUrl")
    is_traffic_tracking_active: Optional[bool] = Field(
        False,
        serialization_alias="isTrafficTrackingActive",
    )
    traffic_limit_bytes: Optional[int] = Field(
        None, serialization_alias="trafficLimitBytes", ge=0
    )
    notify_percent: Optional[int] = Field(
        None, serialization_alias="notifyPercent", ge=0, le=100
    )
    traffic_reset_day: Optional[int] = Field(
        None, serialization_alias="trafficResetDay", ge=1, le=31
    )
    country_code: Annotated[Optional[str], StringConstraints(max_length=2)] = Field(
        "XX", serialization_alias="countryCode"
    )
    consumption_multiplier: Optional[float] = Field(
        None, serialization_alias="consumptionMultiplier", ge=0.1
    )
    node_consumption_multiplier: Optional[float] = Field(
        None, serialization_alias="nodeConsumptionMultiplier", ge=0, le=100
    )
    config_profile: NodeConfigProfileRequestDto = Field(
        serialization_alias="configProfile"
    )
    provider_uuid: Optional[UUID] = Field(None, serialization_alias="providerUuid")
    note: Annotated[Optional[str], StringConstraints(max_length=255)] = None
    tags: Optional[
        list[Annotated[str, StringConstraints(max_length=36, pattern=r"^[A-Z0-9_:]+$")]]
    ] = Field(None, serialization_alias="tags", max_length=10)
    active_plugin_uuid: Optional[UUID] = Field(
        None, serialization_alias="activePluginUuid"
    )
    integration_uuids: Optional[list[UUID]] = Field(
        None, serialization_alias="integrationUuids", max_length=20, description="Panel 3.3.0+."
    )
    ips: Optional[list[NodeIpDto]] = Field(None, max_length=64, description="Panel 3.2.2+.")


class UpdateNodeRequestDto(BaseModel):
    uuid: UUID
    name: Annotated[Optional[str], StringConstraints(min_length=3, max_length=30)] = (
        None
    )
    address: Annotated[Optional[str], StringConstraints(min_length=2)] = None
    port: Optional[float] = Field(None, ge=1, le=65535)
    proxy_url: Optional[str] = Field(None, serialization_alias="proxyUrl")
    is_traffic_tracking_active: Optional[bool] = Field(
        None, serialization_alias="isTrafficTrackingActive"
    )
    traffic_limit_bytes: Optional[float] = Field(
        None, serialization_alias="trafficLimitBytes", ge=0
    )
    notify_percent: Optional[float] = Field(
        None, serialization_alias="notifyPercent", ge=0, le=100
    )
    traffic_reset_day: Optional[float] = Field(
        None, serialization_alias="trafficResetDay", ge=1, le=31
    )
    country_code: Annotated[Optional[str], StringConstraints(max_length=2)] = Field(
        None, serialization_alias="countryCode"
    )
    consumption_multiplier: Optional[float] = Field(
        None, serialization_alias="consumptionMultiplier", ge=0.1
    )
    node_consumption_multiplier: Optional[float] = Field(
        None, serialization_alias="nodeConsumptionMultiplier", ge=0, le=100
    )
    config_profile: Optional[NodeConfigProfileRequestDto] = Field(
        None, serialization_alias="configProfile"
    )
    provider_uuid: Optional[UUID] = Field(None, serialization_alias="providerUuid")
    note: Annotated[Optional[str], StringConstraints(max_length=255)] = None
    tags: Optional[
        list[Annotated[str, StringConstraints(max_length=36, pattern=r"^[A-Z0-9_:]+$")]]
    ] = Field(None, serialization_alias="tags", max_length=10)
    active_plugin_uuid: Optional[UUID] = Field(
        None, serialization_alias="activePluginUuid"
    )
    integration_uuids: Optional[list[UUID]] = Field(
        None, serialization_alias="integrationUuids", max_length=20, description="Panel 3.3.0+."
    )
    ips: Optional[list[NodeIpDto]] = Field(None, max_length=64, description="Panel 3.2.2+.")


class ReorderNodeRequestDto(BaseModel):
    nodes: list[ReorderNodeItem]


class NodeResponseDto(BaseModel):
    uuid: UUID
    id: Optional[int] = Field(None, description="Panel 3.1.0+.")
    name: str
    address: str
    port: Optional[int] = None
    proxy_url: Optional[str] = Field(None, alias="proxyUrl")
    is_connected: bool = Field(alias="isConnected")
    is_disabled: bool = Field(alias="isDisabled")
    is_connecting: bool = Field(alias="isConnecting")
    last_status_change: Optional[datetime] = Field(None, alias="lastStatusChange")
    last_status_message: Optional[str] = Field(None, alias="lastStatusMessage")
    xray_uptime: float = Field(0, alias="xrayUptime")
    is_traffic_tracking_active: bool = Field(alias="isTrafficTrackingActive")
    traffic_reset_day: Optional[int] = Field(None, alias="trafficResetDay")
    traffic_limit_bytes: Optional[float] = Field(None, alias="trafficLimitBytes")
    traffic_used_bytes: Optional[float] = Field(None, alias="trafficUsedBytes")
    notify_percent: Optional[int] = Field(None, alias="notifyPercent")
    users_online: Optional[int] = Field(None, alias="usersOnline")
    view_position: int = Field(alias="viewPosition")
    country_code: str = Field(alias="countryCode")
    consumption_multiplier: float = Field(alias="consumptionMultiplier")
    node_consumption_multiplier: Optional[float] = Field(
        None, alias="nodeConsumptionMultiplier"
    )
    system: Optional[NodeSystemDto] = None
    versions: Optional[NodeVersionsDto] = None
    note: Optional[str] = None
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config_profile: NodeConfigProfileDto = Field(alias="configProfile")
    provider_uuid: Optional[UUID] = Field(None, alias="providerUuid")
    provider: Optional[NodeProviderDto] = None
    tags: list[str] = Field(default_factory=list, alias="tags")
    active_plugin_uuid: Optional[UUID] = Field(None, alias="activePluginUuid")
    integration_uuids: list[UUID] = Field(
        default_factory=list, alias="integrationUuids", description="Panel 3.3.0+."
    )
    ips: list[NodeIpDto] = Field(default_factory=list, description="Panel 3.2.2+.")


class CreateNodeResponseDto(NodeResponseDto):
    pass


class UpdateNodeResponseDto(NodeResponseDto):
    pass


class GetOneNodeResponseDto(NodeResponseDto):
    pass


class GetAllNodesResponseDto(RootModel[list[NodeResponseDto]]):
    root: list[NodeResponseDto]

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]

    def __bool__(self):
        """Return True if list is not empty"""
        return bool(self.root)

    def __len__(self):
        """Return length of list"""
        return len(self.root)


class EnableNodeResponseDto(NodeResponseDto):
    pass


class DisableNodeResponseDto(NodeResponseDto):
    pass


class ReorderNodeResponseDto(RootModel[list[NodeResponseDto]]):
    root: list[NodeResponseDto]

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]

    def __bool__(self):
        """Return True if list is not empty"""
        return bool(self.root)

    def __len__(self):
        """Return length of list"""
        return len(self.root)


class RestartNodeRequestBodyDto(BaseModel):
    force_restart: bool = Field(default=False, serialization_alias="forceRestart")


class RestartAllNodesRequestBodyDto(BaseModel):
    force_restart: bool = Field(default=False, alias="forceRestart")


class ResetNodeTrafficRequestDto(BaseModel):
    uuid: Union[str, UUID] = Field(alias="uuid")


class ConfigProfileData(BaseModel):
    """Config profile data for modification"""

    active_config_profile_uuid: str = Field(alias="activeConfigProfileUuid")
    active_inbounds: list[str] = Field(alias="activeInbounds", min_length=1)


class ProfileModificationRequestDto(BaseModel):
    """Request to modify profiles for multiple nodes"""

    uuids: list[str] = Field(min_length=1)
    config_profile: ConfigProfileData = Field(alias="configProfile")


class ProfileModificationResponseData(BaseModel):
    """Profile modification response data"""

    event_sent: bool = Field(alias="eventSent")


# Legacy aliases
RestartAllNodesRequestDto = RestartAllNodesRequestBodyDto
NodesResponseDto = NodeResponseDto


NodeBulkActionType = Literal["ENABLE", "DISABLE", "RESTART", "RESET_TRAFFIC"]


class NodesBulkActionsRequestDto(BaseModel):
    """Request for performing bulk actions on nodes"""

    uuids: list[UUID] = Field(min_length=1)
    action: NodeBulkActionType = Field(description="Action to perform on nodes")


class NodesUpdateFieldsDto(BaseModel):
    """Fields to update for many nodes at once"""

    country_code: Annotated[Optional[str], StringConstraints(max_length=2)] = Field(
        None, serialization_alias="countryCode"
    )
    consumption_multiplier: Optional[float] = Field(
        None, serialization_alias="consumptionMultiplier", ge=0.1
    )
    node_consumption_multiplier: Optional[float] = Field(
        None, serialization_alias="nodeConsumptionMultiplier", ge=0, le=100
    )
    provider_uuid: Optional[UUID] = Field(None, serialization_alias="providerUuid")
    tags: Optional[
        list[Annotated[str, StringConstraints(max_length=36, pattern=r"^[A-Z0-9_:]+$")]]
    ] = Field(None, serialization_alias="tags", max_length=10)
    active_plugin_uuid: Optional[UUID] = Field(
        None, serialization_alias="activePluginUuid"
    )
    integration_uuids: Optional[list[UUID]] = Field(
        None, serialization_alias="integrationUuids", max_length=20, description="Panel 3.3.0+."
    )
    note: Annotated[Optional[str], StringConstraints(max_length=255)] = None


class BulkNodesUpdateRequestDto(BaseModel):
    """Request to update many nodes at once"""

    uuids: list[UUID] = Field(min_length=1)
    fields: NodesUpdateFieldsDto
