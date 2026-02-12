from fastapi import APIRouter, Body, HTTPException, Response, Depends
from src.backend.schemas import role as role_schema
from src.backend.schemas import permission as perm_schema
from src.utils.auth.methods import get_user
from src.database.pg.methods import AuthMethods, RoleMethods, PermissionMethods
from src.backend.schemas.auth import TokenData
from src.utils.auth.permissions import RightsChecker

router = APIRouter(prefix="/roles", tags=['Управление правами', 'Rights management'])


@router.post("/createRole")
async def create_role(form: role_schema.CreateRoleModel,
                      user: TokenData = Depends(RightsChecker("role.create"))):
    return await RoleMethods.create_role(form)


@router.patch("/updateRole", description="Выдать либо отнять право у роли")
async def update_role(form: role_schema.UpdateRoleModel,
                      user: TokenData = Depends(RightsChecker("role.update"))):
    return await RoleMethods.update_role(form)


@router.post("/getRoles", description="Получить все роли в системе (с правами)")
async def get_roles(user: TokenData = Depends(RightsChecker("role.getAll"))):
    return await RoleMethods.get_roles()


@router.delete("/deleteRole")
async def delete_role(form: role_schema.DeleteRoleModel,
                      user: TokenData = Depends(RightsChecker("role.delete"))):
    return await RoleMethods.delete_role(form)


@router.delete("/deleteRole/{id}")
async def delete_role_by_id(id: int,
                            user: TokenData = Depends(RightsChecker("role.delete"))):
    role_form = role_schema.DeleteRoleByIDModel(role_id=id)
    return await RoleMethods.delete_role_by_id(role_form)


@router.post("/createPermission")
async def create_permission(form: perm_schema.CreatePermissionModel,
                            user: TokenData = Depends(RightsChecker("permission.create"))):
    return await PermissionMethods.create_permission(form)


@router.delete("/deletePermision")
async def delete_permission(form: perm_schema.DeletePermissionModel,
                            user: TokenData = Depends(RightsChecker("permission.delete"))):
    return await PermissionMethods.delete_permission(form)


@router.delete("/deletePermision/{id}")
async def delete_permission_by_id(id: int,
                                  user: TokenData = Depends(RightsChecker("permission.delete"))):
    perm_form = perm_schema.DeletePermissionByIDModel(permission_id=id)
    return await PermissionMethods.delete_permission_by_id(perm_form)


@router.get("/getRolePermissions/{role_name}")
async def _(role_name: str,
            user: TokenData = Depends(RightsChecker("role.permissions"))):
    return await RoleMethods.get_role_permissions(role_name)


@router.get("/getPermissions", description="Получение всех прав в системе")
async def _(user: TokenData = Depends(RightsChecker("permission.getAll"))):
    return await PermissionMethods.get_permissions()
