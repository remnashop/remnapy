from typing import Annotated, Any, Optional
from uuid import UUID

from pydantic import BaseModel, Field, StringConstraints


class NodeIntegrationDto(BaseModel):
    """An integration nodes can be attached to (panel 3.3.0+)."""

    uuid: UUID
    name: str
    description: Optional[str]
    config: dict[str, Any]


class GetNodeIntegrationsResponseDto(BaseModel):
    total: float
    node_integrations: list[NodeIntegrationDto] = Field(alias="nodeIntegrations")


class GetNodeIntegrationResponseDto(NodeIntegrationDto):
    pass


class CreateNodeIntegrationRequestDto(BaseModel):
    name: Annotated[str, StringConstraints(min_length=2, max_length=30)]
    description: Annotated[Optional[str], StringConstraints(max_length=255)] = None
    config: dict[str, Any]


class CreateNodeIntegrationResponseDto(NodeIntegrationDto):
    pass


class UpdateNodeIntegrationRequestDto(BaseModel):
    uuid: UUID
    name: Annotated[Optional[str], StringConstraints(min_length=2, max_length=30)] = (
        None
    )
    description: Annotated[Optional[str], StringConstraints(max_length=255)] = None
    config: Optional[dict[str, Any]] = None
    restart_nodes: Optional[bool] = Field(None, serialization_alias="restartNodes")


class UpdateNodeIntegrationResponseDto(NodeIntegrationDto):
    pass
