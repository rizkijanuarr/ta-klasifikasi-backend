from dataclasses import dataclass
from typing import Optional

@dataclass
class ScrapeSerperRequestV1:
    """
    Request DTO untuk Serper API
    Sesuai dengan dokumentasi: https://serper.dev/
    """
    query: str  # Keyword pencarian (wajib)
    location: Optional[str] = "Indonesia"  # Lokasi pencarian
    gl: Optional[str] = "id"  # Country code
    hl: Optional[str] = "id"  # Language code
    total_pages: Optional[int] = 1  # Total halaman yang akan di-crawl (1 page = 10 hasil)

    def __post_init__(self):
        """Validasi field wajib"""
        if not self.query:
            raise ValueError("query is required and cannot be empty")
        if self.total_pages and self.total_pages > 100:
            raise ValueError("total_pages maximum is 100 (1000 results)")
