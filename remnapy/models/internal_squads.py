from datetime import datetime
from typing import Annotated, Optional
from uuid import UUID

from pydantic import BaseModel, Field, StringConstraints


class InboundsDto(BaseModel):
    uuid: UUID
    profile_uuid: UUID = Field(alias="profileUuid")
    tag: str
    type: str
    network: Optional[str] = None
    security: Optional[str] = None
    port: Optional[float] = None
    raw_inbound: Optional[dict] = Field(None, alias="rawInbound")


class InfoDto(BaseModel):
    members_count: float = Field(alias="membersCount")
    inbounds_count: float = Field(alias="inboundsCount")


class InternalSquadDto(BaseModel):
    uuid: UUID
    view_position: int = Field(alias="viewPosition")
    tags: list[str] = Field(default_factory=list, description="Panel 3.4.0+.")
    name: str
    info: Optional[InfoDto] = Field(default=None)
    inbounds: list[InboundsDto] = Field(default_factory=list)
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class CreateInternalSquadRequestDto(BaseModel):
    name: Annotated[
        str,
        StringConstraints(min_length=2, max_length=30, pattern=r"^[A-Za-z0-9_\s-]+$"),
    ]
    inbounds: list[UUID] = Field(default_factory=list)


class CreateInternalSquadResponseDto(InternalSquadDto):
    pass


class UpdateInternalSquadRequestDto(BaseModel):
    uuid: UUID
    inbounds: list[UUID] = Field(default_factory=list)
    name: Optional[
        Annotated[
            str,
            StringConstraints(
                min_length=2, max_length=30, pattern=r"^[A-Za-z0-9_\s-]+$"
            ),
        ]
    ] = None


class UpdateInternalSquadResponseDto(InternalSquadDto):
    pass


class GetAllInternalSquadsResponse(BaseModel):
    total: float
    internal_squads: list[InternalSquadDto] = Field(alias="internalSquads")


class GetAllInternalSquadsResponseDto(GetAllInternalSquadsResponse):
    pass


class GetInternalSquadByUuidResponseDto(InternalSquadDto):
    pass


class AddUsersToInternalSquadRequestDto(BaseModel):
    user_uuids: list[UUID] = Field(alias="userUuids")


class DeleteUsersFromInternalSquadRequestDto(BaseModel):
    user_uuids: list[UUID] = Field(alias="userUuids")


class AccessibleNodeDto(BaseModel):
    uuid: UUID
    name: str = Field(alias="nodeName")
    country_code: Optional[str] = Field(default=None, alias="countryCode")
    config_profile_uuid: Optional[UUID] = Field(default=None, alias="configProfileUuid")
    config_profile_name: Optional[str] = Field(default=None, alias="configProfileName")
    active_inbounds: list[str] = Field(default_factory=list, alias="activeInbounds")


class GetInternalSquadAccessibleNodesResponseDto(BaseModel):
    squad_uuid: UUID = Field(alias="squadUuid")
    accessible_nodes: list[AccessibleNodeDto] = Field(alias="accessibleNodes")


class ReorderInternalSquadItem(BaseModel):
    view_position: int = Field(serialization_alias="viewPosition")
    uuid: UUID


class ReorderInternalSquadsRequestDto(BaseModel):
    items: list[ReorderInternalSquadItem]


class ReorderInternalSquadsResponseDto(GetAllInternalSquadsResponse):
    pass


class InternalSquadUsageUser(BaseModel):
    """Traffic usage of a single user in the squad"""

    id: int
    total_bytes: float = Field(alias="totalBytes")


class GetInternalSquadUsageResponseDto(BaseModel):
    """Response for GET /api/internal-squads/{uuid}/usage"""

    squad_uuid: UUID = Field(alias="squadUuid")
    users: list[InternalSquadUsageUser]
    next_cursor: Optional[str] = Field(None, alias="nextCursor")
    has_more: bool = Field(alias="hasMore")


class AddManyUsersToInternalSquadRequestDto(BaseModel):
    """Request body for POST /api/internal-squads/{uuid}/bulk-actions/add-many-users"""

    user_ids: list[int] = Field(
        ..., serialization_alias="userIds", description="List of user IDs"
    )


class DeleteManyUsersFromInternalSquadRequestDto(BaseModel):
    """Request body for DELETE /api/internal-squads/{uuid}/bulk-actions/remove-many-users"""

    user_ids: list[int] = Field(
        ..., serialization_alias="userIds", description="List of user IDs"
    )
