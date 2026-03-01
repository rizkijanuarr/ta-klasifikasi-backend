from dataclasses import dataclass

@dataclass
class DetailDatasetResponseV1:
    id: int
    keyword: str
    title: str
    link: str
    description: str
    is_legal: int
    is_ilegal: int
