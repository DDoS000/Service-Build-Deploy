from pydantic import BaseModel
from pydantic.types import Json
from datetime import datetime
from typing import Optional


class Template(BaseModel):
    id: int
