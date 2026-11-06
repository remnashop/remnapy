from typing import Annotated, Union
from uuid import UUID

from rapid_api_client.annotations import Path, PydanticBody

from remnapy.models import (
    CloneSubscriptionPageConfigRequestDto,
    CloneSubscriptionPageConfigResponseDto,
    CreateSubscriptionPageConfigRequestDto,
    CreateSubscriptionPageConfigResponseDto,
    GetSubscriptionPageConfigResponseDto,
    GetSubscriptionPageConfigsResponseDto,
    GetTagsResponseDto,
    ReorderSubscriptionPageConfigsRequestDto,
    ReorderSubscriptionPageConfigsResponseDto,
    SetTagsRequestDto,
    SetTagsResponseDto,
    UpdateSubscriptionPageConfigRequestDto,
    UpdateSubscriptionPageConfigResponseDto,
)
from remnapy.rapid import BaseController, delete, get, patch, post


class SubscriptionPageConfigController(BaseController):
    @get(
        "/subscription-page-configs",
        response_class=GetSubscriptionPageConfigsResponseDto,
    )
    async def get_all_configs(self) -> GetSubscriptionPageConfigsResponseDto:
        """Get all subscription page configs"""
        ...

    @post(
        "/subscription-page-configs",
        response_class=CreateSubscriptionPageConfigResponseDto,
    )
    async def create_config(
        self,
        body: Annotated[CreateSubscriptionPageConfigRequestDto, PydanticBody()],
    ) -> CreateSubscriptionPageConfigResponseDto:
        """Create subscription page config"""
        ...

    @patch(
        "/subscription-page-configs",
        response_class=UpdateSubscriptionPageConfigResponseDto,
    )
    async def update_config(
        self,
        body: Annotated[UpdateSubscriptionPageConfigRequestDto, PydanticBody()],
    ) -> UpdateSubscriptionPageConfigResponseDto:
        """Update subscription page config"""
        ...

    @get(
        "/subscription-page-configs/{uuid}",
        response_class=GetSubscriptionPageConfigResponseDto,
    )
    async def get_config_by_uuid(
        self,
        uuid: Annotated[
            Union[str, UUID], Path(description="Subscription page config UUID")
        ],
    ) -> GetSubscriptionPageConfigResponseDto:
        """Get subscription page config by uuid"""
        ...

    @delete(
        "/subscription-page-configs/{uuid}",
        response_class=None,
    )
    async def delete_config(
        self,
        uuid: Annotated[
            Union[str, UUID], Path(description="Subscription page config UUID")
        ],
    ) -> None:
        """Delete subscription page config"""
        ...

    @post(
        "/subscription-page-configs/actions/reorder",
        response_class=ReorderSubscriptionPageConfigsResponseDto,
    )
    async def reorder_configs(
        self,
        body: Annotated[ReorderSubscriptionPageConfigsRequestDto, PydanticBody()],
    ) -> ReorderSubscriptionPageConfigsResponseDto:
        """Reorder subscription page configs"""
        ...

    @post(
        "/subscription-page-configs/actions/clone",
        response_class=CloneSubscriptionPageConfigResponseDto,
    )
    async def clone_config(
        self,
        body: Annotated[CloneSubscriptionPageConfigRequestDto, PydanticBody()],
    ) -> CloneSubscriptionPageConfigResponseDto:
        """Clone subscription page config"""
        ...

    @get("/subscription-page-configs/tags", response_class=GetTagsResponseDto)
    async def get_tags(self) -> GetTagsResponseDto:
        """Get tags of Subpage Configs (panel 3.4.0+)"""
        ...

    @patch("/subscription-page-configs/tags", response_class=SetTagsResponseDto)
    async def set_tags(
        self,
        body: Annotated[SetTagsRequestDto, PydanticBody()],
    ) -> SetTagsResponseDto:
        """Set tags of a Subpage Config (panel 3.4.0+)"""
        ...
