from pydantic import BaseModel
from typing import List
class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None
    scopes: List[str] = None
