# Simple API for Book Store


## Dependecy
- fastapi(0.79.0)
- fastapi_jwt_auth(0.5.0)
- pydantic(1.9.1)
- python-dotenv(0.20.0)
- python_bcrypt(0.3.2)
- SQLAlchemy(1.4.39)
- uvicorn(0.18.2)
- alembic(1.8.1)


## Install Requierement
```bash
# for install poetry using pip run
$ pip install poetry

# if you using poetry
$ poetry install

# or run on your venv or your local
$ pip install requirements.txt 
```

## Migration
```bash
$ cd book_store

$ poetry run alembic init alembic

$ poetry run alembic revision --autogenerate -m 'first migrations'

$ peotry run alembic upgrade head

```

## Run FastAPI

```bash
# if you using poetry
$ poetry run python prokons/app.py

# or run
$ python run prokons/app.py
```
