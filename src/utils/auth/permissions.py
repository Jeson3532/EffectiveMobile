from src.utils.auth.methods import get_user
from fastapi import Depends, HTTPException
from src.backend.schemas.auth import TokenData
from src.database.pg.methods import RoleMethods


class RightsChecker:
    def __init__(self, req_permission: str):
        self.req_permission = req_permission

    async def __call__(self, user: TokenData = Depends(get_user)):
        user_role = user.role
        result: dict = await RoleMethods.get_role_permissions(user_role)
        permissions = result.get("permissions", [])
        if 'root' in permissions:
            return user

        if self.req_permission not in permissions:
            raise HTTPException(status_code=403, detail="У Вас нет прав на выполнение данной операции")
        return user
