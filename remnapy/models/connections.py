from datetime import datetime
from typing import Annotated, Literal, Optional, Union
from uuid import UUID

from pydantic import BaseModel, Field, model_validator

# ─────────────────────────────────────────────────────────────────────────────
# Job start
# ─────────────────────────────────────────────────────────────────────────────


class ConnectionsJobData(BaseModel):
    """Returned job ID after requesting a connections fetch"""

    job_id: str = Field(alias="jobId")


class ConnectionsByNodeResponseDto(ConnectionsJobData):
    """Response for POST /api/connections/by-node/{nodeUuid}"""

    pass


class ConnectionsByUserResponseDto(ConnectionsJobData):
    """Response for POST /api/connections/by-user/{userId}"""

    pass


# ─────────────────────────────────────────────────────────────────────────────
# Job result – by node
# ─────────────────────────────────────────────────────────────────────────────


class ConnectionIp(BaseModel):
    """IP entry with last seen timestamp"""

    ip: str
    last_seen: datetime = Field(alias="lastSeen")


class ConnectionsByNodeUser(BaseModel):
    """Per-user IP list on a node"""

    user_id: int = Field(alias="userId")
    ips: list[ConnectionIp]


class ConnectionsByNodeResult(BaseModel):
    """Full result payload when the by-node job is completed"""

    success: bool
    node_uuid: UUID = Field(alias="nodeUuid")
    users: list[ConnectionsByNodeUser]


class ConnectionsByNodeResultResponseDto(BaseModel):
    """Response for GET /api/connections/by-node/{jobId}"""

    is_completed: bool = Field(alias="isCompleted")
    is_failed: bool = Field(alias="isFailed")
    result: Optional[ConnectionsByNodeResult] = None


# ─────────────────────────────────────────────────────────────────────────────
# Job result – by user
# ─────────────────────────────────────────────────────────────────────────────


class ConnectionsProgress(BaseModel):
    """Progress information for a by-user connections job"""

    total: float
    completed: float
    percent: float


class ConnectionsByUserNode(BaseModel):
    """Per-node IP list for a user"""

    node_uuid: UUID = Field(alias="nodeUuid")
    node_name: str = Field(alias="nodeName")
    country_code: str = Field(alias="countryCode")
    ips: list[ConnectionIp]


class ConnectionsByUserResult(BaseModel):
    """Full result payload when the by-user job is completed"""

    success: bool
    user_id: int = Field(alias="userId")
    nodes: list[ConnectionsByUserNode]


class ConnectionsByUserResultResponseDto(BaseModel):
    """Response for GET /api/connections/by-user/{jobId}"""

    is_completed: bool = Field(alias="isCompleted")
    is_failed: bool = Field(alias="isFailed")
    progress: ConnectionsProgress
    result: Optional[ConnectionsByUserResult] = None


# ─────────────────────────────────────────────────────────────────────────────
# Drop connections – discriminated unions for dropBy / targetNodes
# ─────────────────────────────────────────────────────────────────────────────


class DropByUserIds(BaseModel):
    """Drop connections for specific user IDs"""

    by: Literal["userIds"] = "userIds"
    user_ids: list[int] = Field(
        ...,
        serialization_alias="userIds",
        min_length=1,
        description="List of user IDs whose connections should be dropped",
    )

    @model_validator(mode="after")
    def _keep_discriminator(self):
        # ``by`` has a default, so it is "unset" unless passed explicitly.
        # The client serializes bodies with ``exclude_unset=True``, which would
        # strip the discriminator and make the API ignore the drop event.
        self.__pydantic_fields_set__.add("by")
        return self


class DropByIpAddresses(BaseModel):
    """Drop connections from specific IP addresses"""

    by: Literal["ipAddresses"] = "ipAddresses"
    ip_addresses: list[str] = Field(
        ...,
        serialization_alias="ipAddresses",
        min_length=1,
        description="List of IP addresses to disconnect",
    )

    @model_validator(mode="after")
    def _keep_discriminator(self):
        self.__pydantic_fields_set__.add("by")
        return self


DropBy = Annotated[
    Union[DropByUserIds, DropByIpAddresses],
    Field(discriminator="by"),
]


class TargetAllNodes(BaseModel):
    """Send the drop-connections event to all connected nodes"""

    target: Literal["allNodes"] = "allNodes"

    @model_validator(mode="after")
    def _keep_discriminator(self):
        self.__pydantic_fields_set__.add("target")
        return self


class TargetSpecificNodes(BaseModel):
    """Send the drop-connections event to specific nodes only"""

    target: Literal["specificNodes"] = "specificNodes"
    node_uuids: list[UUID] = Field(
        ...,
        serialization_alias="nodeUuids",
        min_length=1,
        description="List of node UUIDs to target",
    )

    @model_validator(mode="after")
    def _keep_discriminator(self):
        self.__pydantic_fields_set__.add("target")
        return self


TargetNodes = Annotated[
    Union[TargetAllNodes, TargetSpecificNodes],
    Field(discriminator="target"),
]


class DropConnectionsRequestDto(BaseModel):
    """Request body for POST /api/connections/drop"""

    drop_by: DropBy = Field(
        ...,
        serialization_alias="dropBy",
        description="Selector for whose connections to drop",
    )
    target_nodes: TargetNodes = Field(
        ...,
        serialization_alias="targetNodes",
        description="Selector for which nodes to send the drop event to",
    )


# ─────────────────────────────────────────────────────────────────────────────
# Geocheck (panel 3.3.0+)
# ─────────────────────────────────────────────────────────────────────────────


class GeocheckByNodeRequestDto(BaseModel):
    """Where the node checks from: an IP or a network interface, not both"""

    ip: Optional[str] = None
    interface: Optional[str] = None


class GeocheckByNodeResponseDto(ConnectionsJobData):
    """Response for POST /api/connections/geocheck/{nodeUuid}"""

    pass


class GeocheckImageDto(BaseModel):
    format: Literal["svg"]
    media_type: Literal["image/svg+xml"]
    encoding: Literal["base64"]
    data: str


class GeocheckResultDto(BaseModel):
    success: bool
    node_uuid: UUID = Field(alias="nodeUuid")
    image: Optional[GeocheckImageDto]
    raw_report: Optional[dict] = Field(alias="rawReport")
    message: Optional[str]


class GeocheckByNodeResultResponseDto(BaseModel):
    """Response for GET /api/connections/geocheck/{jobId}"""

    is_completed: bool = Field(alias="isCompleted")
    is_failed: bool = Field(alias="isFailed")
    result: Optional[GeocheckResultDto]
