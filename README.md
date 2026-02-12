## Effective Mobile Backend App
- Система авторизации OAuth 2.0 с ролевой логикой и выдачей прав.

#### Версия разработки: Python 3.12
#### Инструменты разработки: FastAPI, sqlalchemy (ORM, +asyncpg), alembic, Redis, PyJWT
#### CI/CD стек: Docker, git


## Инструкция по запуску проекта:
1. **Скопируйте репозиторий на локальную машину:**
    - ```git clone https://github.com/Jeson3532/EffectiveMobile.git```
2. **Создайте и активируйте виртуальное окружение:**
    - ```python -m venv .venv``` | ```python3 -m venv .venv```
    - ```source .venv/bin/activate (Linux)``` | ```./.venv/Scripts/activate (PS)```
3. **Установите все зависимости на локальную машину:**
    - ```pip install -r requirements.txt```
4. **Установите PYTHONPATH на корень проекта:**
    - PS: ```$env:PYTHONPATH='.'```
    - CMD: ```set PYTHONPATH=.```
    - Linux & macOS: ```export PYTHONPATH=.```
5. **Создайте файл .env и добавьте следующее содержимое:**
```env
# Security
SECRET_KEY=YOUR_SECRET_KEY
# Database
POSTGRES_USER=admin
POSTGRES_PASSWORD=admin
POSTGRES_DB=efmobile
POSTGRES_PORT=5432
# Redis
REDIS_HOST=redis_db
REDIS_PORT=6379 

```
6. **Установите и запустите Docker:**
    - Windows: установите Docker Desktop и активируйте компонент WSL на компьютере, после запустите его.
    - macOS: установите Docker Desktop и запустите его.
    - Linix: Установите Docker Engine через официальный репозиторий и запустите процесс.
7. **Забилдите и запустите контейнеры:**
    - ```docker compose up -d --build``` 
8. **Загрузите дамп базы:**  
  .sql: ```cat db_backup.sql | docker exec -i effective-mobile-postgres_db-1 psql -U admin -d efmobile```
9. **Загрузите все миграции (опционально, но для масштабирования потребуется):**  
   - ```docker exec -it effective-mobile-backend-1 alembic stamp head```
10. **Подключитесь по адресу localhost:8000/docs (Swagger) либо localhost:8000/redoc (ReDoc) для тестирования функционала.**  
**Вы можете воспользоваться кнопкой 'Authorize' справа сверху  и войти в аккаунт с root-правами:**
    - ```username: root@gmail.com```
    -  ```password: 12345678```
