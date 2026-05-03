# DuckMusic

## Sumary
- [Requeriments](#requiriments)
- [Runing / install](#runing)
- [Project Structure](#project-structure)
- [contributors](#contributors)
- [changes historic](#changes-historic)
- [lincense](#lincense)
- [how to contribe](#how-to-contribe)

## Requiriments
- python (3.11)
- postgressql , mysql or another relational database
- git and github
- uv

## Runing

1- clone repository
``` bash
# clone repository
git clone https://github.com/PedroLopes30/DuckMusic/
# or
git clone https://github.com/Jose-GuilhermeG/DuckMusic/ 

cd duckMusic
```

2- install dependicies
```bash
    cd ./src/api/
    uv venv
    uv sync
```

3 - Runing
```bash
    #with fastapi dev
    uv run fastapi dev main.py
    #or with uvicorn
    PYTHONPATH=../../src/ uv run uvicorn --port 8000 main:app --reload
 
``` 

## Project Structure
```
└── 📁duckMusic
    └── 📁docs
        ├── routes.md
    └── 📁src
        └── 📁api
            └── 📁admin
                ├── autenticate.py
                ├── auth_admin.py
            └── 📁configs
                ├── __init__.py
                ├── db.py
                ├── settings.py
            └── 📁core
                ├── __init__.py
                ├── constants.py
                ├── models.py
                ├── utils.py
            └── 📁depends
                ├── __init__.py
                ├── auth_dep.py
                ├── db_dep.py
            └── 📁interfaces
                ├── __init__.py
                ├── access_service.py
                ├── hash.py
                ├── repository.py
            └── 📁middlewares
                ├── __init__.py
                ├── database_middleware.py
            └── 📁models
                ├── __init__.py
                ├── auth.py
            └── 📁routes
                ├── __init__.py
                ├── auth.py
            └── 📁shemas
                └── 📁input
                    ├── __init__.py
                    ├── auth_input.py
                └── 📁output
                    ├── __init__.py
                    ├── auth_output.py
                    ├── general_output.py
            ├── __init__.py
            ├── .python-version
            ├── main.py
            ├── pyproject.toml
            ├── repository.py
            ├── uv.lock
    ├── .editorconfig
    ├── .gitignore
    ├── CONTRIBUTING.md
    ├── license
    └── README.md
```

## Contributors

- [José Guilherme](https://github.com/Jose-GuilhermeG)
- [Pedro lopes](https://github.com/PedroLopes30)

## changes historic
- [changelog](./docs/CHANGELOG.md)

## lincense
- [lincense](./license)

## How to contribe
- [contribe](./CONTRIBUTING.md)