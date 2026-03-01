from dataclasses import dataclass, field
from typing import List, TypeVar, Generic, Optional

T = TypeVar('T')

@dataclass
class ErrorResponse:
    code: str
    title: str
    message: str

@dataclass
class SliceResponseParameter(Generic[T]):
    """
    Response parameter for paginated/sliced data with metadata
    """
    data: List[T]
    success: bool = True
    message: Optional[str] = None
    is_first: bool = False
    is_last: bool = False
    has_next: bool = False
    total_data: Optional[int] = None
    current_page: Optional[int] = None
    errors: Optional[List[ErrorResponse]] = field(default_factory=list)
