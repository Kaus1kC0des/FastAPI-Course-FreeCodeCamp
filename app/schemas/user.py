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
    id: int
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


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=16)
    confirm_password: str = Field(min_length=8, max_length=16)

    @model_validator(mode="after")
    def check_passwords_match(self):
        if self.password != self.confirm_password:
            raise ValueError(f"Passwords don't match!")
        return self


class UserResponse(UserBase):
    pass


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserPayment(BaseModel):
    card_expiry: date = Field(alias="cardExpire")
    card_number: str = Field(alias="cardNumber")
    card_type: str = Field(alias="cardType")
    currency: str
    iban: str

    @field_validator("card_expiry", mode="before")
    @classmethod
    def validate_expiry(cls, expiry: str):
        month, year = expiry.split("/")
        year = 2000 + int(year)
        month = int(month)
        last_day = monthrange(year, month)[1]
        return date(year, month, last_day)
