from typing import Optional

from pydantic import BaseModel
from tracardi.domain.entity import Entity


class Configuration(BaseModel):
    source: Entity
    language: str = 'en'
    model: str = 'social'
    title: Optional[str] = None
    text: str

    def has_title(self) -> bool:
        return self.title is not None
