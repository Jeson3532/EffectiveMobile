from fastapi import APIRouter, Depends, Cookie
from src.utils.auth.methods import get_user
from src.database.pg.methods import ProfileMethods, AccountMethods
from src.backend.schemas.profile import UserProfileResponse, EditProfileModel, InputEditProfileModel
from src.backend.schemas.auth import TokenData

router = APIRouter(prefix="/account", tags=['Аккаунт', 'Account'])


@router.get("/profile", description="Получить свой профиль", response_model=UserProfileResponse)
async def get_profile(user: TokenData = Depends(get_user)):
    profile = await ProfileMethods.get_profile(user.user_id)
    return profile


@router.patch("/profile/edit", response_model=UserProfileResponse, description="Изменить секцию из своего профиля")
async def edit_profile(input_form: InputEditProfileModel, user: TokenData = Depends(get_user)):
    edit_form = EditProfileModel(**input_form.model_dump())
    edit_form = edit_form.model_copy(update={"user_id": user.user_id})
    return await ProfileMethods.edit_section(edit_form)


@router.delete("/delete")
async def delete_account(user: TokenData = Depends(get_user)):
    return await AccountMethods.delete_account(user.user_id)
