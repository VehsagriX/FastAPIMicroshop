from typing import Annotated
from annotated_types import MaxLen, MinLen
from pydantic import BaseModel, EmailStr, Field


class CreateUser(BaseModel):
    # username: str = Field(..., min_length=8, max_length=20)
    username: Annotated[str, MinLen(8), MaxLen(20)]
    email: EmailStr
