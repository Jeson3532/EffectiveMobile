from pydantic import BaseModel, Field, ConfigDict


class CreatePermissionModel(BaseModel):
    permission_name: str = Field(...)

    model_config = ConfigDict(from_attributes=True)


class DeletePermissionModel(BaseModel):
    permission_name: str = Field(...)


class DeletePermissionByIDModel(BaseModel):
    permission_id: int = Field(...)
