from pydantic import BaseModel, Field, EmailStr, model_validator
from pydantic.networks import email_validator


class UserBase(BaseModel):
    email: EmailStr
    first_name: str = Field(min_length=2)
    last_name: str = Field(min_length=1)

    class Config:
        from_attributes = True


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
