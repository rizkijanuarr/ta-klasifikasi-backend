from dataclasses import dataclass
from typing import TypeVar, Generic, Optional, List
from backend.response.advices.ErrorResponse import ErrorResponse

T = TypeVar('T')

@dataclass
class DataResponseParameter(Generic[T]):
    data: Optional[T] = None
    message: Optional[str] = None
    success: bool = True
    errors: Optional[List[ErrorResponse]] = None