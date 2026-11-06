from datetime import datetime
from typing import Annotated, Any, Literal, Optional, Union
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, StringConstraints


class TorrentBlockerUserDto(BaseModel):
    username: str


class TorrentBlockerNodeDto(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    uuid: UUID
    name: str
    country_code: str = Field(alias="countryCode")


class TorrentBlockerActionReportDto(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    blocked: bool
    ip: str
    block_duration: float = Field(alias="blockDuration")
    will_unblock_at: datetime = Field(alias="willUnblockAt")
    user_id: str = Field(alias="userId")
    processed_at: datetime = Field(alias="processedAt")


class TorrentBlockerXrayReportDto(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    email: Optional[str] = None
    level: Optional[float] = None
    protocol: Optional[str] = None
    network: str
    source: Optional[str] = None
    destination: str
    route_target: Optional[str] = Field(default=None, alias="routeTarget")
    original_target: Optional[str] = Field(default=None, alias="originalTarget")
    inbound_tag: Optional[str] = Field(default=None, alias="inboundTag")
    inbound_name: Optional[str] = Field(default=None, alias="inboundName")
    inbound_local: Optional[str] = Field(default=None, alias="inboundLocal")
    outbound_tag: Optional[str] = Field(default=None, alias="outboundTag")
    ts: float


class TorrentBlockerReportPayloadDto(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    action_report: TorrentBlockerActionReportDto = Field(alias="actionReport")
    xray_report: TorrentBlockerXrayReportDto = Field(alias="xrayReport")


class TorrentBlockerReportRecordDto(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: float
    user_id: int = Field(alias="userId")
    node_id: float = Field(alias="nodeId")
    user: TorrentBlockerUserDto
    node: TorrentBlockerNodeDto
    report: TorrentBlockerReportPayloadDto
    created_at: datetime = Field(alias="createdAt")


class TorrentBlockerReportsData(BaseModel):
    records: list[TorrentBlockerReportRecordDto]
    total: float


class GetTorrentBlockerReportsResponseDto(TorrentBlockerReportsData):
    pass


class TorrentBlockerStatsDto(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    distinct_nodes: float = Field(alias="distinctNodes")
    distinct_users: float = Field(alias="distinctUsers")
    total_reports: float = Field(alias="totalReports")
    reports_last_24_hours: float = Field(alias="reportsLast24Hours")


class TorrentBlockerTopUserDto(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    user_id: int = Field(alias="userId")
    color: str
    username: str
    total: float


class TorrentBlockerTopNodeDto(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    uuid: UUID
    country_code: str = Field(alias="countryCode")
    color: str
    name: str
    total: float


class GetTorrentBlockerReportsStatsResponseDto(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    stats: TorrentBlockerStatsDto
    top_users: list[TorrentBlockerTopUserDto] = Field(alias="topUsers")
    top_nodes: list[TorrentBlockerTopNodeDto] = Field(alias="topNodes")


class NodePluginDto(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    uuid: UUID
    view_position: int = Field(alias="viewPosition")
    tags: list[str] = Field(default_factory=list, description="Panel 3.4.0+.")
    name: str
    plugin_config: Any | None = Field(alias="pluginConfig")


class GetNodePluginsResponseDto(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    total: float
    node_plugins: list[NodePluginDto] = Field(alias="nodePlugins")


class GetNodePluginResponseDto(NodePluginDto):
    pass


class UpdateNodePluginRequestDto(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    uuid: UUID
    name: Optional[
        Annotated[
            str,
            StringConstraints(
                min_length=2, max_length=30, pattern=r"^[A-Za-z0-9_\s-]+$"
            ),
        ]
    ] = None
    plugin_config: Optional[Any] = Field(default=None, alias="pluginConfig")


class UpdateNodePluginResponseDto(NodePluginDto):
    pass


class CreateNodePluginRequestDto(BaseModel):
    name: Annotated[
        str,
        StringConstraints(min_length=2, max_length=30, pattern=r"^[A-Za-z0-9_\s-]+$"),
    ]


class CreateNodePluginResponseDto(NodePluginDto):
    pass


class ReorderNodePluginItem(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    view_position: int = Field(alias="viewPosition")
    uuid: UUID


class ReorderNodePluginsRequestDto(BaseModel):
    items: list[ReorderNodePluginItem]


class ReorderNodePluginsResponseDto(GetNodePluginsResponseDto):
    pass


class CloneNodePluginRequestDto(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    clone_from_uuid: UUID = Field(alias="cloneFromUuid")


class CloneNodePluginResponseDto(NodePluginDto):
    pass


class BlockIpItemDto(BaseModel):
    ip: str
    timeout: float


class BlockIpsCommandDto(BaseModel):
    command: Literal["blockIps"]
    ips: list[BlockIpItemDto]


class UnblockIpsCommandDto(BaseModel):
    command: Literal["unblockIps"]
    ips: list[str]


class RecreateTablesCommandDto(BaseModel):
    command: Literal["recreateTables"]


PluginCommandDto = Union[
    BlockIpsCommandDto, UnblockIpsCommandDto, RecreateTablesCommandDto
]


class TargetAllNodesDto(BaseModel):
    target: Literal["allNodes"]


class TargetSpecificNodesDto(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    target: Literal["specificNodes"]
    node_uuids: list[UUID] = Field(alias="nodeUuids")


PluginTargetNodesDto = Union[TargetAllNodesDto, TargetSpecificNodesDto]


class PluginExecutorRequestDto(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    command: PluginCommandDto
    target_nodes: PluginTargetNodesDto = Field(alias="targetNodes")


SharedListName = Annotated[
    str,
    StringConstraints(
        min_length=2, max_length=255, pattern=r"^[A-Za-z0-9_-]+(/[A-Za-z0-9_-]+)*$"
    ),
]


class SyncNodePluginRequestDto(BaseModel):
    """Pushes a node plugin to its nodes (panel 3.3.0+)."""

    uuid: UUID


class SharedListDto(BaseModel):
    """A list node plugins share, e.g. of IPs or domains (panel 3.3.0+)."""

    name: str
    config: dict[str, Any]


class SharedListPreviewDto(BaseModel):
    name: str
    type: str
    items_count: float = Field(alias="itemsCount")


class GetSharedListsResponseDto(BaseModel):
    total: float
    shared_lists: list[SharedListPreviewDto] = Field(alias="sharedLists")


class GetSharedListResponseDto(SharedListDto):
    pass


class CreateSharedListRequestDto(BaseModel):
    name: SharedListName
    config: dict[str, Any]


class CreateSharedListResponseDto(SharedListDto):
    pass


class UpdateSharedListRequestDto(BaseModel):
    name: SharedListName
    config: dict[str, Any]


class UpdateSharedListResponseDto(SharedListDto):
    pass


class DeleteSharedListRequestDto(BaseModel):
    name: SharedListName


class SyncSharedListRequestDto(BaseModel):
    name: SharedListName
