from pydantic import BaseModel
from typing import List, Optional

class DesignSpec(BaseModel):
    type: str
    material: List[str]
    dimensions: Optional[str] = None
    extras: Optional[str] = None
