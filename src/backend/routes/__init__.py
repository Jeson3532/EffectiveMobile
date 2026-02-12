from src.backend.routes.auth import router as auth_router
from src.backend.routes.account import router as profile_router
from src.backend.routes.testing import router as test_router
from src.backend.routes.rights import router as role_router
from fastapi import APIRouter

routers = []
for k, v in list(globals().items()):
    cond1 = '_router' in k
    cond2 = isinstance(v, APIRouter)
    if cond1 and cond2:
        routers.append(v)
