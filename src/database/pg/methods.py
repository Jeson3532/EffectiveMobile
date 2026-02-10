from src.database.pg.model import session_maker
from sqlalchemy import select, exists, insert, delete
from src.database.pg.tables import Users
import asyncio


class AuthMethods:
    @classmethod
    async def get_user(cls, username: str):
        async with session_maker() as session:
            query = select(Users).where(Users.username == username)
            st = await session.execute(query)
            result_ = st.scalars().all()
            return result_


result = asyncio.run(AuthMethods().get_user("admin"))
print({k: v for k, v in result[0].__dict__.items() if not k.startswith("_")})
