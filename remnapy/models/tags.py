from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, Field, StringConstraints

Tag = Annotated[str, StringConstraints(max_length=36, pattern=r"^[A-Z0-9_:]+$")]


class GetTagsResponseDto(BaseModel):
    """Tags in use across one kind of entity (panel 3.4.0+)."""

    tags: list[str]


class SetTagsRequestDto(BaseModel):
    """Replaces the tags of one entity (panel 3.4.0+)."""

    uuid: UUID
    tags: Annotated[list[Tag], Field(max_length=10)]


class SetTagsResponseDto(BaseModel):
    uuid: UUID
    tags: list[str]
