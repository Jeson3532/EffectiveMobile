from pydantic import BaseModel, Field, ConfigDict, model_validator
from typing import Union
from fastapi import HTTPException


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

    @model_validator(mode='after')
    def section_type(self):
        if self.section_name == 'age':
            if not self.new_value.isdigit():
                raise HTTPException(status_code=400, detail="Неверный формат возраста")
        return self
