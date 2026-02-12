from pydantic import BaseModel, Field, ConfigDict


class RoleModel(BaseModel):
    role_name: str = Field(...)


class CreateRoleModel(RoleModel):
    permissions: list = Field(...)

    model_config = ConfigDict(from_attributes=True)


class DeleteRoleModel(RoleModel):
    role_name: str = Field(...)


class DeleteRoleByIDModel(BaseModel):
    role_id: int = Field(...)


class RoleResponse(BaseModel):
    id: int = Field(...)
    role_name: str = Field(...)
    permissions: list = Field(...)


class UpdateRoleModel(BaseModel):
    role_name: str = Field(...)
    permission: str = Field(...)
