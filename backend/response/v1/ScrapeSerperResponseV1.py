from dataclasses import dataclass
from typing import Optional, List

@dataclass
class SerperOrganicItem:
    """
    Single item dari hasil organic search Serper
    """
    title: str
    link: str
    snippet: str
    position: int
    rating: Optional[float] = None
    ratingCount: Optional[int] = None

@dataclass
class ScrapeSerperResponseV1:
    """
    Response DTO untuk Serper API
    Berisi list hasil crawling yang akan disimpan ke CSV
    """
    query: str  # Keyword yang dicari
    total_results: int  # Jumlah hasil
    organic: List[SerperOrganicItem]  # List hasil organic search
    csv_path: str  # Path file CSV yang disimpan
    message: str  # Status message
