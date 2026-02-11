from src.database.pg.model import session_maker
from src.database.pg.tables import Users, Profiles

from sqlalchemy import select, exists, insert, delete, update
from sqlalchemy.exc import IntegrityError
import asyncio
from fastapi import HTTPException
from src.utils.security.handler import hash_password
from pydantic import BaseModel
from typing import Type
from src.backend.enums.http import HTTPDetail

from src.backend.schemas import auth as auth_schema
from src.backend.schemas import profile as prof_schema
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
