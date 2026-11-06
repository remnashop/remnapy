from typing import Annotated, Any

from pydantic import BaseModel, StringConstraints

# panel 3.4.0+ also allows slashes, which group snippets into folders
SNIPPET_NAME_PATTERN = r"^[A-Za-z0-9_ -]+(/[A-Za-z0-9_ -]+)*$"


class SnippetItem(BaseModel):
    """Individual snippet item"""

    name: str
    snippet: Any  # Can be any JSON object or array


class SnippetsData(BaseModel):
    """Snippets response data"""

    total: int
    snippets: list[SnippetItem]


# The API returns the data directly, without a wrapper
class GetSnippetsResponseDto(SnippetsData):
    """Get all snippets response - extends SnippetsData directly"""

    pass


class CreateSnippetResponseDto(SnippetsData):
    """Create snippet response - extends SnippetsData directly"""

    pass


class UpdateSnippetResponseDto(SnippetsData):
    """Update snippet response - extends SnippetsData directly"""

    pass


class CreateSnippetRequestDto(BaseModel):
    """Create snippet request"""

    name: Annotated[
        str,
        StringConstraints(min_length=2, max_length=255, pattern=SNIPPET_NAME_PATTERN),
    ]
    snippet: list[dict]  # Array of objects


class UpdateSnippetRequestDto(BaseModel):
    """Update snippet request"""

    name: Annotated[
        str,
        StringConstraints(min_length=2, max_length=255, pattern=SNIPPET_NAME_PATTERN),
    ]
    snippet: list[dict]  # Array of objects


class DeleteSnippetRequestDto(BaseModel):
    """Delete snippet request"""

    name: Annotated[
        str,
        StringConstraints(min_length=2, max_length=255, pattern=SNIPPET_NAME_PATTERN),
    ]


class SyncSnippetRequestDto(BaseModel):
    """Re-applies a snippet to the config profiles using it (panel 3.2.3+)."""

    name: Annotated[
        str,
        StringConstraints(min_length=2, max_length=255, pattern=SNIPPET_NAME_PATTERN),
    ]
