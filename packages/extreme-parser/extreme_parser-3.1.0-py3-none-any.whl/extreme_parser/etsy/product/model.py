from typing import Optional

from pydantic import BaseModel


class Product(BaseModel):
    title: Optional[str]
