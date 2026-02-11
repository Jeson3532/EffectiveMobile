from pydantic import BaseModel, Field, ConfigDict
from typing import Union


class UserProfileResponse(BaseModel):
    age: str = Field(...)
    date_of_birth: str = Field(...)
    phone_number: str = Field(...)
    bio: str = Field(...)


class InputEditProfileModel(BaseModel):
    section_name: str = Field(...)
    new_value: str = Field(...)

    model_config = ConfigDict(from_attributes=True)


class EditProfileModel(BaseModel):
    user_id: str | None = Field(default=None)
    section_name: str = Field(...)
    new_value: str = Field(...)
