from dataclasses import dataclass
from typing import TypeVar, Generic, Optional, List
from backend.response.advices.ErrorResponse import ErrorResponse

T = TypeVar('T')

@dataclass
class PageResponseParameter(Generic[T]):
    data: Optional[List[T]] = None
    message: Optional[str] = None
    success: bool = True
    current_page: Optional[int] = None
    total_page: Optional[int] = None
    total_data: Optional[int] = None
    page_size: Optional[int] = None
    errors: Optional[List[ErrorResponse]] = None