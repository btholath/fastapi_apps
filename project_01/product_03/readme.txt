
http://127.0.0.1:8000/redoc#tag/product

http://127.0.0.1:8000/docs#tag/product

http://127.0.0.1:8000/documentation



--create a secret key for JWT
$ openssl rand -hex 32
ed383250ab5e129d78b449d4856cbb096e96dd3f4eb775ec760b25f5a9fffe33

(.venv) C:\github\fastapi_apps\project_01\product>uvicorn main:app --reload
