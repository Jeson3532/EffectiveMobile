from src.database.pg.model import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import text, TEXT, ForeignKey


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    middle_name: Mapped[str] = mapped_column(comment="Отчество (при наличии)", nullable=True)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False, comment="Хеш пароля")
    role: Mapped[str] = mapped_column(nullable=False, default="user", server_default=text("user"))
    is_active: Mapped[bool] = mapped_column(default=True, server_default=text("true"))

    profile: Mapped['Profiles'] = relationship(back_populates='user', uselist=False)


class Profiles(Base):
    __tablename__ = "profiles"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    age: Mapped[str] = mapped_column(default="Не указано", server_default="Не указано")
    date_of_birth: Mapped[str] = mapped_column(default="Не указано", server_default="Не указано")
    phone_number: Mapped[str] = mapped_column(default="Не указано", server_default="Не указано")
    bio: Mapped[str] = mapped_column(TEXT, default="...", server_default="...")

    user: Mapped['Users'] = relationship(back_populates='profile')


class Roles(Base):
    __tablename__ = 'roles'

    id: Mapped[int] = mapped_column(primary_key=True)
    role_name: Mapped[str] = mapped_column(unique=True, nullable=False)

    roleperm: Mapped[list['RolePermissions']] = relationship(back_populates="role")


class Permissions(Base):
    __tablename__ = 'permissions'

    id: Mapped[int] = mapped_column(primary_key=True)
    permission_name: Mapped[str] = mapped_column(unique=True, nullable=False)

    roleperm: Mapped[list['RolePermissions']] = relationship(back_populates="perm")


class RolePermissions(Base):
    __tablename__ = 'role_permissions'

    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True)
    permission_id: Mapped[int] = mapped_column(ForeignKey("permissions.id", ondelete="CASCADE"), primary_key=True)

    role: Mapped['Roles'] = relationship(back_populates="roleperm")
    perm: Mapped['Permissions'] = relationship(back_populates="roleperm")
