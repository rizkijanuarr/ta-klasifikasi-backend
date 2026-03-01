from dataclasses import dataclass
from typing import Optional

@dataclass
class GetDatasetByLinkRequestV1:
    link: str

    def __post_init__(self):
        # Validate link
        if not self.link or not self.link.strip():
            raise ValueError("link is required and cannot be empty")

        # Basic URL validation
        if not (self.link.startswith('http://') or self.link.startswith('https://')):
            raise ValueError("link must be a valid URL (http:// or https://)")
