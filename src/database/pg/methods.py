from src.database.pg.model import session_maker
from src.database.pg.tables import Users, Profiles, Roles, Permissions, RolePermissions

from sqlalchemy import select, exists, insert, delete, update
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError
import asyncio
from fastapi import HTTPException
from src.utils.security.handler import hash_password
from pydantic import BaseModel
from typing import Type
from src.backend.enums.http import HTTPDetail

from src.backend.schemas import auth as auth_schema
from src.backend.schemas import profile as prof_schema
from src.backend.schemas import role as role_schema
from src.backend.schemas import permission as perm_schema
from src.utils.log import logger

ALLOWED_EDIT_SECTIONS = list(prof_schema.UserProfileResponse.model_fields.keys())


class AuthMethods:
    @classmethod
    async def get_user(cls, username: str, model: Type[BaseModel] = None):
        async with session_maker() as session:
            try:
                query = select(Users).where(Users.username == username)
                st = await session.execute(query)
                result = st.scalar_one_or_none()
                if not result:
                    raise HTTPException(status_code=404, detail=HTTPDetail.DETAIL_404_NOT_FOUND_USER)
                if model:
                    validate_user = model.model_validate(result)
                    return validate_user
                return result
            except HTTPException:
                await session.rollback()
                raise
            except Exception as e:
                await session.rollback()
                logger.error(f"Произошла ошибка в get_user: {e}")
                raise HTTPException(status_code=500,
                                    detail="Произошла ошибка при выполнении операции")

    @classmethod
    async def get_user_by_id(cls, user_id: int, model: Type[BaseModel] = None):
        async with session_maker() as session:
            try:
                query = select(Users).where(Users.id == user_id)
                st = await session.execute(query)
                result = st.scalar_one_or_none()
                if not result:
                    raise HTTPException(status_code=404, detail=HTTPDetail.DETAIL_404_NOT_FOUND_USER)
                if model:
                    validate_user = model.model_validate(result)
                    return validate_user
                return result
            except HTTPException:
                await session.rollback()
                raise
            except Exception as e:
                await session.rollback()
                logger.error(f"Произошла ошибка в get_user_by_id: {e}")
                raise HTTPException(status_code=500,
                                    detail="Произошла ошибка при выполнении операции")

    @classmethod
    async def get_user_by_email(cls, email: str, model: Type[BaseModel] = None):
        async with session_maker() as session:
            try:
                query = select(Users).where(Users.email == email)
                st = await session.execute(query)
                result = st.scalar_one_or_none()
                if not result:
                    raise HTTPException(status_code=404, detail=HTTPDetail.DETAIL_404_NOT_FOUND_USER)
                if model:
                    validate_user = model.model_validate(result)
                    return validate_user
                return result
            except HTTPException:
                await session.rollback()
                raise
            except Exception as e:
                await session.rollback()
                logger.error(f"Произошла ошибка в get_user: {e}")
                raise HTTPException(status_code=500,
                                    detail="Произошла ошибка при выполнении операции")

    @classmethod
    async def register_user(cls, user: auth_schema.UserRegModel):
        async with session_maker() as session:
            try:
                dumped_user = user.model_dump(exclude={"repeat_password"})
                dumped_user['password'] = hash_password(dumped_user['password'])

                new_user = Users(**dumped_user)
                new_user.profile = Profiles()  # Создание профиля
                session.add(new_user)
                await session.commit()
                return user
            except IntegrityError:
                await session.rollback()
                raise HTTPException(status_code=409, detail="Данный пользователь уже существует в системе")
            except Exception as e:
                logger.error(f"Произошла ошибка в register_user: {e}")
                await session.rollback()
                raise HTTPException(status_code=500, detail="Произошла ошибка при регистрации")


class ProfileMethods:
    @classmethod
    async def get_profile(cls, user_id: int, model: Type[BaseModel] = None):
        async with session_maker() as session:
            try:
                query = select(Profiles).where(Profiles.user_id == user_id)
                st = await session.execute(query)
                result = st.scalar_one_or_none()
                if not result:
                    raise HTTPException(status_code=404, detail=HTTPDetail.DETAIL_404_NOT_FOUND_PROFILE)
                if model:
                    validate_profile = model.model_validate(result)
                    return validate_profile
                return result
            except HTTPException:
                await session.rollback()
                raise
            except Exception as e:
                logger.error(f"Произошла ошибка в get_profile: {e}")
                await session.rollback()
                raise HTTPException(status_code=500, detail="Произошла ошибка при запросе профиля")

    @classmethod
    async def edit_section(cls, edit_form: prof_schema.EditProfileModel):
        async with session_maker() as session:
            try:
                dumped_form = edit_form.model_dump()

                user_id = dumped_form.get("user_id")
                section_name = dumped_form.get("section_name")
                new_value = dumped_form.get("new_value")

                query = select(Profiles).where(Profiles.user_id == user_id)
                st = await session.execute(query)
                profile = st.scalar_one_or_none()
                if not profile:
                    raise HTTPException(status_code=404, detail=HTTPDetail.DETAIL_404_NOT_FOUND_PROFILE)

                if hasattr(profile, section_name):
                    if section_name not in ALLOWED_EDIT_SECTIONS:
                        raise HTTPException(status_code=400, detail="Вы не можете редактировать эту секцию")
                    setattr(profile, section_name, new_value)
                else:
                    raise HTTPException(status_code=404, detail=f"Секции {section_name} не существует")
                await session.commit()
                await session.refresh(profile)
                return profile
            except HTTPException:
                await session.rollback()
                raise
            except Exception as e:
                logger.error(f"Произошла ошибка в edit_section: {e}")
                await session.rollback()
                raise HTTPException(status_code=500,
                                    detail="Произошла ошибка при попытке редактировать профиль, попробуйте позже")


class AccountMethods:
    @classmethod
    async def account_is_active(cls, user_id) -> bool:
        async with session_maker() as session:
            try:
                query = select(Users.is_active).where(Users.id == user_id)
                st = await session.execute(query)
                is_active = st.scalar_one_or_none()
                if not is_active:
                    raise HTTPException(status_code=404, detail=HTTPDetail.DETAIL_404_NOT_FOUND_USER)
                return is_active
            except HTTPException:
                await session.rollback()
                raise
            except Exception as e:
                await session.rollback()
                logger.error(f"Произошла ошибка в account_is_active: {e}")
                raise HTTPException(status_code=500,
                                    detail="Произошла ошибка при выполнении операции")

    @classmethod
    async def delete_account(cls, user_id: int):
        async with session_maker() as session:
            try:
                query = select(Users).where(Users.id == user_id)
                st = await session.execute(query)
                user = st.scalar_one_or_none()
                if not user:
                    raise HTTPException(status_code=404, detail=HTTPDetail.DETAIL_404_NOT_FOUND_USER)
                if hasattr(user, 'is_active'):
                    if not user.is_active:
                        raise HTTPException(status_code=404, detail="Аккаунт не найден")
                    setattr(user, 'is_active', False)
                else:
                    logger.error(f"Нет секции is_active у юзера {user}")
                    raise HTTPException(status_code=500,
                                        detail="Произошла ошибка при попытке удаления аккаунта, попробуйте позже")
                await session.commit()
                return {"success": True}
            except HTTPException:
                await session.rollback()
                raise
            except Exception as e:
                await session.rollback()
                logger.error(f"Произошла ошибка в delete_account: {e}")
                raise HTTPException(status_code=500,
                                    detail="Произошла ошибка при выполнении операции")


class RoleMethods:
    @classmethod
    async def create_role(cls, form: role_schema.CreateRoleModel):
        async with session_maker() as session:
            try:
                new_role = Roles(role_name=form.role_name)
                permissions = form.permissions
                session.add(new_role)
                await session.flush()

                query = select(Permissions.id).where(Permissions.permission_name.in_(permissions))
                result = await session.execute(query)
                perm_ids = result.scalars().all()

                if len(perm_ids) != len(permissions):
                    raise HTTPException(status_code=400, detail=f"Некоторых указанных прав нет в системе")
                for id_ in perm_ids:
                    new_perm = RolePermissions(
                        role_id=new_role.id,
                        permission_id=id_
                    )
                    session.add(new_perm)
                await session.commit()
                await session.refresh(new_role)
                return role_schema.RoleResponse(id=new_role.id, role_name=new_role.role_name, permissions=permissions)
            except IntegrityError:
                await session.rollback()
                raise HTTPException(status_code=409, detail="Данная роль уже существует в системе")
            except HTTPException:
                await session.rollback()
                raise
            except Exception as e:
                await session.rollback()
                logger.error(f"Произошла ошибка в create_role: {e}")
                raise HTTPException(status_code=500,
                                    detail="Произошла ошибка при выполнении операции")

    @classmethod
    async def get_roles(cls):
        async with session_maker() as session:
            try:
                query = select(Roles).options(
                    selectinload(Roles.roleperm).selectinload(RolePermissions.perm)
                )
                st = await session.execute(query)
                result = st.scalars().unique().all()
                return [
                    {
                        "role_name": role.role_name,
                        "permissions": [role_perm.perm.permission_name for role_perm in role.roleperm]
                    }
                    for role in result
                ]
            except HTTPException:
                await session.rollback()
                raise
            except Exception as e:
                await session.rollback()
                logger.error(f"Произошла ошибка в get_roles: {e}")
                raise HTTPException(status_code=500,
                                    detail="Произошла ошибка при выполнении операции")

    @classmethod
    async def update_role(cls, form: role_schema.UpdateRoleModel):
        async with session_maker() as session:
            try:
                # Айди роли
                query = select(Roles.id).where(Roles.role_name == form.role_name)
                result = await session.execute(query)
                role_id = result.scalar_one_or_none()
                if not role_id:
                    raise HTTPException(status_code=404, detail=f"Роли {form.role_name} не существует")
                # Айди права
                query = select(Permissions.id).where(Permissions.permission_name == form.permission)
                result = await session.execute(query)
                perm_id = result.scalar_one_or_none()
                if not perm_id:
                    raise HTTPException(status_code=404, detail=f"Права {form.permission} не существует")

                query_link = select(RolePermissions).where(
                    RolePermissions.role_id == role_id,
                    RolePermissions.permission_id == perm_id)
                result = await session.execute(query_link)
                row = result.scalar_one_or_none()
                if row:
                    await session.delete(row)
                    await session.commit()
                    return f'Право "{form.permission}" у роли "{form.role_name}" отобрано'
                new_perm = RolePermissions(role_id=role_id, permission_id=perm_id)
                session.add(new_perm)
                await session.commit()
                await session.refresh(new_perm)
                return f'Право "{form.permission}" добавлено к роли "{form.role_name}"'
            except HTTPException:
                await session.rollback()
                raise
            except Exception as e:
                await session.rollback()
                logger.error(f"Произошла ошибка в update_role: {e}")
                raise HTTPException(status_code=500,
                                    detail="Произошла ошибка при выполнении операции")

    @classmethod
    async def delete_role(cls, form: role_schema.DeleteRoleModel):
        async with session_maker() as session:
            try:
                query = delete(Roles).where(Roles.role_name == form.role_name)
                result = await session.execute(query)
                await session.commit()
                if result.rowcount == 0:
                    raise HTTPException(status_code=404, detail=f'Роли "{form.role_name}" не существует в системе')
                return {"success": True}
            except HTTPException:
                await session.rollback()
                raise
            except Exception as e:
                await session.rollback()
                logger.error(f"Произошла ошибка в delete_role: {e}")
                raise HTTPException(status_code=500,
                                    detail="Произошла ошибка при выполнении операции")

    @classmethod
    async def delete_role_by_id(cls, form: role_schema.DeleteRoleByIDModel):
        async with session_maker() as session:
            try:
                query = delete(Roles).where(Roles.id == form.role_id)
                result = await session.execute(query)
                await session.commit()
                if result.rowcount == 0:
                    raise HTTPException(status_code=404, detail=f'Роли с айди "{form.role_id}" не существует в системе')
                return {"success": True}
            except HTTPException:
                await session.rollback()
                raise
            except Exception as e:
                await session.rollback()
                logger.error(f"Произошла ошибка в delete_role_by_id: {e}")
                raise HTTPException(status_code=500,
                                    detail="Произошла ошибка при выполнении операции")

    @classmethod
    async def get_role_permissions(cls, role_name: str):
        async with session_maker() as session:
            try:
                # Поиск айди
                query = select(Roles.id).where(Roles.role_name == role_name)
                st = await session.execute(query)
                role_id = st.scalar_one_or_none()
                if not role_id:
                    raise HTTPException(status_code=404, detail=f'Роль "{role_name}" не найдена')
                # Получение айди прав
                query = select(RolePermissions.permission_id).where(RolePermissions.role_id == role_id)
                st = await session.execute(query)
                perm_ids = st.scalars().all()

                if not perm_ids:
                    return []
                # Получение названий по айди
                query = select(Permissions.permission_name).where(Permissions.id.in_(perm_ids))
                st = await session.execute(query)
                perm_names = st.scalars().all()
                return {"role_name": role_name, "permissions": perm_names}
            except HTTPException:
                await session.rollback()
                raise
            except Exception as e:
                await session.rollback()
                logger.error(f"Произошла ошибка в get_role_permissions: {e}")
                raise HTTPException(status_code=500,
                                    detail="Произошла ошибка при выполнении операции")


class PermissionMethods:
    @classmethod
    async def create_permission(cls, form: perm_schema.CreatePermissionModel):
        async with session_maker() as session:
            try:
                dumped_form = form.model_dump()
                new_perm = Permissions(**dumped_form)
                session.add(new_perm)
                await session.commit()
                await session.refresh(new_perm)
                return new_perm
            except HTTPException:
                await session.rollback()
                raise
            except IntegrityError:
                await session.rollback()
                raise HTTPException(status_code=409, detail="Данное право уже существует в системе")
            except Exception as e:
                await session.rollback()
                logger.error(f"Произошла ошибка в create_permission: {e}")
                raise HTTPException(status_code=500,
                                    detail="Произошла ошибка при выполнении операции")

    @classmethod
    async def get_permissions(cls):
        async with session_maker() as session:
            try:
                query = select(Permissions.permission_name)
                result = await session.execute(query)
                perms = result.scalars().all()
                if not perms:
                    raise HTTPException(status_code=404, detail="Прав в системе не найдено")
                return {"permissions": perms}
            except HTTPException:
                await session.rollback()
                raise
            except Exception as e:
                await session.rollback()
                logger.error(f"Произошла ошибка в create_permission: {e}")
                raise HTTPException(status_code=500,
                                    detail="Произошла ошибка при выполнении операции")

    @classmethod
    async def delete_permission(cls, form: perm_schema.DeletePermissionModel):
        async with session_maker() as session:
            try:
                permission_name = form.permission_name
                query = delete(Roles).where(Permissions.permission_name == permission_name)
                result = await session.execute(query)
                await session.commit()
                if result.rowcount == 0:
                    raise HTTPException(status_code=404, detail=f'Права "{permission_name}" не существует в системе')
                return {"success": True}
            except HTTPException:
                await session.rollback()
                raise
            except Exception as e:
                await session.rollback()
                logger.error(f"Произошла ошибка в delete_permission: {e}")
                raise HTTPException(status_code=500,
                                    detail="Произошла ошибка при выполнении операции")

    @classmethod
    async def delete_permission_by_id(cls, form: perm_schema.DeletePermissionByIDModel):
        async with session_maker() as session:
            try:
                permission_id = form.permission_id
                query = delete(Roles).where(Permissions.id == permission_id)
                result = await session.execute(query)
                await session.commit()
                if result.rowcount == 0:
                    raise HTTPException(status_code=404,
                                        detail=f'Права с айди "{permission_id}" не существует в системе')
                return {"success": True}
            except HTTPException:
                await session.rollback()
                raise
            except Exception as e:
                await session.rollback()
                logger.error(f"Произошла ошибка в delete_permission_by_id: {e}")
                raise HTTPException(status_code=500,
                                    detail="Произошла ошибка при выполнении операции")
