from dataclasses import dataclass
from typing import Optional

@dataclass
class ErrorResponse:
    code: Optional[int] = None
    title: Optional[str] = None
    message: Optional[str] = None