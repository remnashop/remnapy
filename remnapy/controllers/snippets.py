from typing import Annotated

from rapid_api_client.annotations import PydanticBody

from remnapy.models import (
    CreateSnippetRequestDto,
    CreateSnippetResponseDto,
    DeleteSnippetRequestDto,
    GetSnippetsResponseDto,
    SyncSnippetRequestDto,
    UpdateSnippetRequestDto,
    UpdateSnippetResponseDto,
)
from remnapy.rapid import BaseController, delete, get, patch, post


class SnippetsController(BaseController):
    @get("/snippets", response_class=GetSnippetsResponseDto)
    async def get_snippets(self) -> GetSnippetsResponseDto:
        """Get snippets"""
        ...

    @post("/snippets", response_class=CreateSnippetResponseDto)
    async def create_snippet(
        self,
        body: Annotated[CreateSnippetRequestDto, PydanticBody()],
    ) -> CreateSnippetResponseDto:
        """Create snippet"""
        ...

    @patch("/snippets", response_class=UpdateSnippetResponseDto)
    async def update_snippet(
        self,
        body: Annotated[UpdateSnippetRequestDto, PydanticBody()],
    ) -> UpdateSnippetResponseDto:
        """Update snippet"""
        ...

    @delete("/snippets", response_class=None)
    async def delete_snippet_by_name(
        self,
        body: Annotated[DeleteSnippetRequestDto, PydanticBody()],
    ) -> None:
        """Delete snippet"""
        ...

    @post("/snippets/actions/sync", response_class=None)
    async def sync_snippet(
        self,
        body: Annotated[SyncSnippetRequestDto, PydanticBody()],
    ) -> None:
        """Sync snippet to the config profiles using it (panel 3.2.3+)"""
        ...
