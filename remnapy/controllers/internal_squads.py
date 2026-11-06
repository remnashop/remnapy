from typing import Annotated, Optional, Union
from uuid import UUID

from rapid_api_client import Path, Query
from rapid_api_client.annotations import PydanticBody

from remnapy.models import (
    AddManyUsersToInternalSquadRequestDto,
    CreateInternalSquadRequestDto,
    CreateInternalSquadResponseDto,
    DeleteManyUsersFromInternalSquadRequestDto,
    GetAllInternalSquadsResponseDto,
    GetInternalSquadAccessibleNodesResponseDto,
    GetInternalSquadByUuidResponseDto,
    GetInternalSquadUsageResponseDto,
    GetTagsResponseDto,
    ReorderInternalSquadsRequestDto,
    ReorderInternalSquadsResponseDto,
    SetTagsRequestDto,
    SetTagsResponseDto,
    UpdateInternalSquadRequestDto,
    UpdateInternalSquadResponseDto,
)
from remnapy.rapid import BaseController, delete, get, patch, post


class InternalSquadsController(BaseController):
    @get("/internal-squads", response_class=GetAllInternalSquadsResponseDto)
    async def get_internal_squads(self) -> GetAllInternalSquadsResponseDto:
        """Get all internal squads"""
        ...

    @post("/internal-squads", response_class=CreateInternalSquadResponseDto)
    async def create_internal_squad(
        self,
        body: Annotated[CreateInternalSquadRequestDto, PydanticBody()],
    ) -> CreateInternalSquadResponseDto:
        """Create internal squad"""
        ...

    @patch("/internal-squads", response_class=UpdateInternalSquadResponseDto)
    async def update_internal_squad(
        self,
        body: Annotated[UpdateInternalSquadRequestDto, PydanticBody()],
    ) -> UpdateInternalSquadResponseDto:
        """Update internal squad"""
        ...

    @get("/internal-squads/{uuid}", response_class=GetInternalSquadByUuidResponseDto)
    async def get_internal_squad_by_uuid(
        self,
        uuid: Annotated[
            Union[str, UUID], Path(description="UUID of the internal squad")
        ],
    ) -> GetInternalSquadByUuidResponseDto:
        """Get internal squad by uuid"""
        ...

    @delete("/internal-squads/{uuid}", response_class=None)
    async def delete_internal_squad(
        self,
        uuid: Annotated[
            Union[str, UUID], Path(description="UUID of the internal squad")
        ],
    ) -> None:
        """Delete internal squad"""
        ...

    @post(
        "/internal-squads/{uuid}/bulk-actions/add-users",
        response_class=None,
    )
    async def add_users_to_internal_squad(
        self,
        uuid: Annotated[
            Union[str, UUID], Path(description="UUID of the internal squad")
        ],
    ) -> None:
        """Add users to internal squad"""
        ...

    @delete(
        "/internal-squads/{uuid}/bulk-actions/remove-users",
        response_class=None,
    )
    async def remove_users_from_internal_squad(
        self,
        uuid: Annotated[
            Union[str, UUID], Path(description="UUID of the internal squad")
        ],
    ) -> None:
        """Delete users from internal squad"""
        ...

    @get(
        "/internal-squads/{uuid}/accessible-nodes",
        response_class=GetInternalSquadAccessibleNodesResponseDto,
    )
    async def get_accessible_nodes(
        self,
        uuid: Annotated[
            Union[str, UUID], Path(description="UUID of the internal squad")
        ],
    ) -> GetInternalSquadAccessibleNodesResponseDto:
        """Get accessible nodes for internal squad"""
        ...

    @post(
        "/internal-squads/actions/reorder",
        response_class=ReorderInternalSquadsResponseDto,
    )
    async def reorder_internal_squads(
        self,
        body: Annotated[ReorderInternalSquadsRequestDto, PydanticBody()],
    ) -> ReorderInternalSquadsResponseDto:
        """Reorder internal squads"""
        ...

    @get(
        "/internal-squads/{uuid}/usage",
        response_class=GetInternalSquadUsageResponseDto,
    )
    async def get_internal_squad_usage(
        self,
        uuid: Annotated[
            Union[str, UUID], Path(description="UUID of the internal squad")
        ],
        start: Annotated[str, Query(description="Start date")],
        end: Annotated[str, Query(description="End date")],
        min_total_bytes: Annotated[
            int,
            Query(
                default=0, ge=0, alias="minTotalBytes", description="Minimum total bytes"
            ),
        ] = 0,
        limit: Annotated[
            int,
            Query(
                default=250, ge=1, le=1000, description="Number of users to return"
            ),
        ] = 250,
        cursor: Annotated[
            Optional[int],
            Query(
                default=None,
                description=(
                    "Pagination cursor; pass the previous response's nextCursor "
                    "converted to an integer"
                ),
            ),
        ] = None,
    ) -> GetInternalSquadUsageResponseDto:
        """Get internal squad usage"""
        ...

    @post(
        "/internal-squads/{uuid}/bulk-actions/add-many-users",
        response_class=None,
    )
    async def add_many_users_to_internal_squad(
        self,
        uuid: Annotated[
            Union[str, UUID], Path(description="UUID of the internal squad")
        ],
        body: Annotated[AddManyUsersToInternalSquadRequestDto, PydanticBody()],
    ) -> None:
        """Add many users to internal squad"""
        ...

    @delete(
        "/internal-squads/{uuid}/bulk-actions/remove-many-users",
        response_class=None,
    )
    async def remove_many_users_from_internal_squad(
        self,
        uuid: Annotated[
            Union[str, UUID], Path(description="UUID of the internal squad")
        ],
        body: Annotated[DeleteManyUsersFromInternalSquadRequestDto, PydanticBody()],
    ) -> None:
        """Remove many users from internal squad"""
        ...

    @get("/internal-squads/tags", response_class=GetTagsResponseDto)
    async def get_tags(self) -> GetTagsResponseDto:
        """Get tags of Internal Squads (panel 3.4.0+)"""
        ...

    @patch("/internal-squads/tags", response_class=SetTagsResponseDto)
    async def set_tags(
        self,
        body: Annotated[SetTagsRequestDto, PydanticBody()],
    ) -> SetTagsResponseDto:
        """Set tags of a Internal Squad (panel 3.4.0+)"""
        ...
