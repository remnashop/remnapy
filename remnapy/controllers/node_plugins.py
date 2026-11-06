from typing import Annotated, Optional

from rapid_api_client import Path, PydanticBody, Query

from remnapy.models import (
    CloneNodePluginRequestDto,
    CloneNodePluginResponseDto,
    CreateNodePluginRequestDto,
    CreateNodePluginResponseDto,
    CreateSharedListRequestDto,
    CreateSharedListResponseDto,
    DeleteSharedListRequestDto,
    GetNodePluginResponseDto,
    GetNodePluginsResponseDto,
    GetSharedListResponseDto,
    GetSharedListsResponseDto,
    GetTagsResponseDto,
    GetTorrentBlockerReportsResponseDto,
    GetTorrentBlockerReportsStatsResponseDto,
    PluginExecutorRequestDto,
    ReorderNodePluginsRequestDto,
    ReorderNodePluginsResponseDto,
    SetTagsRequestDto,
    SetTagsResponseDto,
    SyncNodePluginRequestDto,
    SyncSharedListRequestDto,
    TableFilter,
    TableSort,
    UpdateNodePluginRequestDto,
    UpdateNodePluginResponseDto,
    UpdateSharedListRequestDto,
    UpdateSharedListResponseDto,
)
from remnapy.rapid import BaseController, delete, get, patch, post


class NodePluginsController(BaseController):
    @get(
        "/node-plugins/torrent-blocker",
        response_class=GetTorrentBlockerReportsResponseDto,
    )
    async def get_torrent_blocker_reports(
        self,
        size: Annotated[
            Optional[int], Query(default=None, ge=1, description="Page size")
        ] = None,
        start: Annotated[
            Optional[int], Query(default=None, ge=0, description="Offset")
        ] = None,
        filters: Annotated[
            Optional[list[TableFilter]],
            Query(default=None, description="Column filters"),
        ] = None,
        filter_modes: Annotated[
            Optional[dict[str, str]],
            Query(
                default=None, alias="filterModes", description="Per-column filter modes"
            ),
        ] = None,
        global_filter_mode: Annotated[
            Optional[str],
            Query(
                default=None, alias="globalFilterMode", description="Global filter mode"
            ),
        ] = None,
        sorting: Annotated[
            Optional[list[TableSort]],
            Query(default=None, description="Sort order"),
        ] = None,
    ) -> GetTorrentBlockerReportsResponseDto:
        """Get Torrent Blocker Reports"""
        ...

    @get(
        "/node-plugins/torrent-blocker/stats",
        response_class=GetTorrentBlockerReportsStatsResponseDto,
    )
    async def get_torrent_blocker_reports_stats(
        self,
    ) -> GetTorrentBlockerReportsStatsResponseDto:
        """Get Torrent Blocker Reports Stats"""
        ...

    @delete(
        "/node-plugins/torrent-blocker/truncate",
        response_class=None,
    )
    async def truncate_torrent_blocker_reports(
        self,
    ) -> None:
        """Truncate Torrent Blocker Reports"""
        ...

    @get("/node-plugins", response_class=GetNodePluginsResponseDto)
    async def get_all_node_plugins(self) -> GetNodePluginsResponseDto:
        """Get all Node Plugins"""
        ...

    @patch("/node-plugins", response_class=UpdateNodePluginResponseDto)
    async def update_node_plugin(
        self,
        body: Annotated[UpdateNodePluginRequestDto, PydanticBody()],
    ) -> UpdateNodePluginResponseDto:
        """Update Node Plugin"""
        ...

    @post("/node-plugins", response_class=CreateNodePluginResponseDto)
    async def create_node_plugin(
        self,
        body: Annotated[CreateNodePluginRequestDto, PydanticBody()],
    ) -> CreateNodePluginResponseDto:
        """Create Node Plugin"""
        ...

    @get("/node-plugins/{uuid}", response_class=GetNodePluginResponseDto)
    async def get_node_plugin_by_uuid(
        self,
        uuid: Annotated[str, Path(description="Node plugin UUID")],
    ) -> GetNodePluginResponseDto:
        """Get Node Plugin by uuid"""
        ...

    @delete("/node-plugins/{uuid}", response_class=None)
    async def delete_node_plugin(
        self,
        uuid: Annotated[str, Path(description="Node plugin UUID")],
    ) -> None:
        """Delete Node Plugin"""
        ...

    @post("/node-plugins/actions/reorder", response_class=ReorderNodePluginsResponseDto)
    async def reorder_node_plugins(
        self,
        body: Annotated[ReorderNodePluginsRequestDto, PydanticBody()],
    ) -> ReorderNodePluginsResponseDto:
        """Reorder Node Plugins"""
        ...

    @post("/node-plugins/actions/clone", response_class=CloneNodePluginResponseDto)
    async def clone_node_plugin(
        self,
        body: Annotated[CloneNodePluginRequestDto, PydanticBody()],
    ) -> CloneNodePluginResponseDto:
        """Clone Node Plugin"""
        ...

    @post("/node-plugins/executor", response_class=None)
    async def plugin_executor(
        self,
        body: Annotated[PluginExecutorRequestDto, PydanticBody()],
    ) -> None:
        """Execute command on node plugins"""
        ...

    @get("/node-plugins/tags", response_class=GetTagsResponseDto)
    async def get_tags(self) -> GetTagsResponseDto:
        """Get tags of Node Plugins (panel 3.4.0+)"""
        ...

    @patch("/node-plugins/tags", response_class=SetTagsResponseDto)
    async def set_tags(
        self,
        body: Annotated[SetTagsRequestDto, PydanticBody()],
    ) -> SetTagsResponseDto:
        """Set tags of a Node Plugin (panel 3.4.0+)"""
        ...

    @post("/node-plugins/actions/sync", response_class=None)
    async def sync_node_plugin(
        self,
        body: Annotated[SyncNodePluginRequestDto, PydanticBody()],
    ) -> None:
        """Sync Node Plugin to nodes (panel 3.3.0+)"""
        ...

    @get("/node-plugins/shared-lists", response_class=GetSharedListsResponseDto)
    async def get_shared_lists(self) -> GetSharedListsResponseDto:
        """Get Shared Lists, without their contents (panel 3.3.0+)"""
        ...

    @get("/node-plugins/shared-lists/by-name", response_class=GetSharedListResponseDto)
    async def get_shared_list_by_name(
        self,
        name: Annotated[str, Query(description="Shared list name")],
    ) -> GetSharedListResponseDto:
        """Get Shared List by name (panel 3.4.0+)"""
        ...

    @post("/node-plugins/shared-lists", response_class=CreateSharedListResponseDto)
    async def create_shared_list(
        self,
        body: Annotated[CreateSharedListRequestDto, PydanticBody()],
    ) -> CreateSharedListResponseDto:
        """Create Shared List (panel 3.3.0+)"""
        ...

    @patch("/node-plugins/shared-lists", response_class=UpdateSharedListResponseDto)
    async def update_shared_list(
        self,
        body: Annotated[UpdateSharedListRequestDto, PydanticBody()],
    ) -> UpdateSharedListResponseDto:
        """Update Shared List (panel 3.3.0+)"""
        ...

    @delete("/node-plugins/shared-lists", response_class=None)
    async def delete_shared_list(
        self,
        body: Annotated[DeleteSharedListRequestDto, PydanticBody()],
    ) -> None:
        """Delete Shared List by name (panel 3.4.0+)"""
        ...

    @post("/node-plugins/shared-lists/actions/sync", response_class=None)
    async def sync_shared_list(
        self,
        body: Annotated[SyncSharedListRequestDto, PydanticBody()],
    ) -> None:
        """Sync Shared List to nodes (panel 3.3.0+)"""
        ...
