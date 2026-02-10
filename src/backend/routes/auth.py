from fastapi import APIRouter, Body, HTTPException, Response
from src.backend.schemas import auth as auth_schema
from src.utils.auth import methods as auth_methods
from src.backend.enums.exc import HTTPDetail
router = APIRouter(prefix="/auth", tags=['Аутентификация'])


@router.post("/register")
async def _():
    ...


@router.post("", response_model=auth_schema.TokenResponse)
async def _(response: Response, auth_form: auth_schema.UserAuthModel = Body(...)):
    tokens = auth_methods.verify_user(auth_form.login, auth_form.password)
    response.set_cookie("refresh_token", tokens.get("refresh_token"),
                        httponly=True,
                        max_age=4320 * 60)
    return tokens

