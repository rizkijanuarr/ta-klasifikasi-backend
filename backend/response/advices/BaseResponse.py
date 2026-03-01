from dataclasses import dataclass
from typing import Any, Optional, List
from backend.response.advices.ErrorResponse import ErrorResponse

@dataclass
class BaseResponse:
    success: bool = True
    message: Optional[str] = None
    data: Optional[Any] = None
    is_first: Optional[bool] = None
    is_last: Optional[bool] = None
    has_next: Optional[bool] = None
    current_page: Optional[int] = None
    total_page: Optional[int] = None
    total_data: Optional[int] = None
    page_size: Optional[int] = None
    errors: Optional[List[ErrorResponse]] = None