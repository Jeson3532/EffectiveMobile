from enum import Enum


class HTTPDetail(str, Enum):
    DETAIL_401_UNAUTHORIZED = """Вы ввели неверный логин или пароль, проверьте правильность введенных данных"""
    DETAIL_403_FORBIDDEN = """У Вас недостаточно прав для выполнения этой операции"""
    DETAIL_404_NOT_FOUND_USER = """Пользователь не найден"""
    DETAIL_404_NOT_FOUND_PROFILE = """Профиль не найден"""
    DETAIL_404_NOT_FOUND = """Запрашиваемый ресурс не найден в системе"""
