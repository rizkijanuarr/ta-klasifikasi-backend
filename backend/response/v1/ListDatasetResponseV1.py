from dataclasses import dataclass

@dataclass
class ListDatasetResponseV1:
    id: int
    keyword: str
    title: str
    link: str
    description: str
    is_legal: int
    is_ilegal: int
