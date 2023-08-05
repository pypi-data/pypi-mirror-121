from pydantic import BaseModel


class MLSourceConfiguration(BaseModel):
    token: str
