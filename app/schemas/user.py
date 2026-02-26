from calendar import monthrange
from pydantic import (
    BaseModel,
    Field,
    EmailStr,
    model_validator,
    field_validator,
    ConfigDict,
)
from datetime import date


class UserBase(BaseModel):
    first_name: str = Field(min_length=2, alias="firstName")
    last_name: str = Field(min_length=1, alias="lastName")
    age: int
    gender: str
    email: EmailStr
    phone: str
    user_name: str = Field(alias="username")
    birth_date: date = Field(alias="birthDate")
    image: str
    role: str

    model_config = ConfigDict(
        from_attributes=True, extra="ignore", populate_by_name=True
    )

    @field_validator("birth_date", mode="before")
    @classmethod
    def parse_birth_date(cls, v: str) -> date:
        # handles "1997-9-3"
        year, month, day = list(map(int, v.split("-")))
        return date(year, month, day)


class UserResponse(UserBase):
    id: int
