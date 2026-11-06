from typing import Annotated, Union
from uuid import UUID

from rapid_api_client import Path, PydanticBody

from remnapy.models import (
    CreateNodeIntegrationRequestDto,
    CreateNodeIntegrationResponseDto,
    GetNodeIntegrationResponseDto,
    GetNodeIntegrationsResponseDto,
    UpdateNodeIntegrationRequestDto,
    UpdateNodeIntegrationResponseDto,
)
from remnapy.rapid import BaseController, delete, get, patch, post


class NodeIntegrationsController(BaseController):
    """Node integrations (panel 3.3.0+)"""

    @get("/node-integrations", response_class=GetNodeIntegrationsResponseDto)
    async def get_all_node_integrations(self) -> GetNodeIntegrationsResponseDto:
        """Get all Node Integrations"""
        ...

    @post("/node-integrations", response_class=CreateNodeIntegrationResponseDto)
    async def create_node_integration(
        self,
        body: Annotated[CreateNodeIntegrationRequestDto, PydanticBody()],
    ) -> CreateNodeIntegrationResponseDto:
        """Create Node Integration"""
        ...

    @patch("/node-integrations", response_class=UpdateNodeIntegrationResponseDto)
    async def update_node_integration(
        self,
        body: Annotated[UpdateNodeIntegrationRequestDto, PydanticBody()],
    ) -> UpdateNodeIntegrationResponseDto:
        """Update Node Integration"""
        ...

    @get("/node-integrations/{uuid}", response_class=GetNodeIntegrationResponseDto)
    async def get_node_integration_by_uuid(
        self,
        uuid: Annotated[Union[str, UUID], Path(description="Node integration UUID")],
    ) -> GetNodeIntegrationResponseDto:
        """Get Node Integration by uuid"""
        ...

    @delete("/node-integrations/{uuid}", response_class=None)
    async def delete_node_integration(
        self,
        uuid: Annotated[Union[str, UUID], Path(description="Node integration UUID")],
    ) -> None:
        """Delete Node Integration"""
        ...
