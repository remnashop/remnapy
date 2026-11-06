from typing import Annotated, Union
from uuid import UUID

from rapid_api_client import Path
from rapid_api_client.annotations import PydanticBody

from remnapy.models import (
    CreateExternalSquadRequestDto,
    CreateExternalSquadResponseDto,
    GetExternalSquadByUuidResponseDto,
    GetExternalSquadsResponseDto,
    GetTagsResponseDto,
    ReorderExternalSquadsRequestDto,
    ReorderExternalSquadsResponseDto,
    SetTagsRequestDto,
    SetTagsResponseDto,
    UpdateExternalSquadRequestDto,
    UpdateExternalSquadResponseDto,
)
from remnapy.rapid import BaseController, delete, get, patch, post


class ExternalSquadsController(BaseController):
    @get("/external-squads", response_class=GetExternalSquadsResponseDto)
    async def get_external_squads(
        self,
    ) -> GetExternalSquadsResponseDto:
        """Get all external squads"""
        ...

    @post("/external-squads", response_class=CreateExternalSquadResponseDto)
    async def create_external_squad(
        self,
        body: Annotated[CreateExternalSquadRequestDto, PydanticBody()],
    ) -> CreateExternalSquadResponseDto:
        """Create external squad"""
        ...

    @patch("/external-squads", response_class=UpdateExternalSquadResponseDto)
    async def update_external_squad(
        self,
        body: Annotated[UpdateExternalSquadRequestDto, PydanticBody()],
    ) -> UpdateExternalSquadResponseDto:
        """Update external squad"""
        ...

    @get("/external-squads/{uuid}", response_class=GetExternalSquadByUuidResponseDto)
    async def get_external_squad_by_uuid(
        self,
        uuid: Annotated[
            Union[str, UUID], Path(description="UUID of the external squad")
        ],
    ) -> GetExternalSquadByUuidResponseDto: ...

    @delete("/external-squads/{uuid}", response_class=None)
    async def delete_external_squad(
        self,
        uuid: Annotated[
            Union[str, UUID], Path(description="UUID of the external squad")
        ],
    ) -> None: ...

    @post(
        "/external-squads/{uuid}/bulk-actions/add-users",
        response_class=None,
    )
    async def add_users_to_external_squad(
        self,
        uuid: Annotated[
            Union[str, UUID], Path(description="UUID of the external squad")
        ],
    ) -> None: ...

    @delete(
        "/external-squads/{uuid}/bulk-actions/remove-users",
        response_class=None,
    )
    async def remove_users_from_external_squad(
        self,
        uuid: Annotated[
            Union[str, UUID], Path(description="UUID of the external squad")
        ],
    ) -> None: ...

    @post(
        "/external-squads/actions/reorder",
        response_class=ReorderExternalSquadsResponseDto,
    )
    async def reorder_external_squads(
        self,
        body: Annotated[ReorderExternalSquadsRequestDto, PydanticBody()],
    ) -> ReorderExternalSquadsResponseDto:
        """Reorder external squads"""
        ...

    @get("/external-squads/tags", response_class=GetTagsResponseDto)
    async def get_tags(self) -> GetTagsResponseDto:
        """Get tags of External Squads (panel 3.4.0+)"""
        ...

    @patch("/external-squads/tags", response_class=SetTagsResponseDto)
    async def set_tags(
        self,
        body: Annotated[SetTagsRequestDto, PydanticBody()],
    ) -> SetTagsResponseDto:
        """Set tags of a External Squad (panel 3.4.0+)"""
        ...
