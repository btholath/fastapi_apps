
(.venv) C:\github\fastapi_apps\06_redis_warehouse_store>uvicorn microservice_warehouse.main:app --reload
INFO:     Will watch for changes in these directories: ['C:\\github\\fastapi_apps\\06_redis_warehouse_store']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [18016] using StatReload
INFO:     Started server process [27828]
INFO:     Waiting for application startup.
INFO:     Application startup complete.




For microservices_warehouse
http://127.0.0.1:8000/docs#/


-- microservice_store
(.venv) PS C:\github\fastapi_apps\06_redis_warehouse_store> uvicorn microservice_store.main:app --reload --port 8001
INFO:     Will watch for changes in these directories: ['C:\\github\\fastapi_apps\\06_redis_warehouse_store']
INFO:     Uvicorn running on http://127.0.0.1:8001 (Press CTRL+C to quit)
INFO:     Started reloader process [14232] using StatReload
INFO:     Started server process [17560]
INFO:     Waiting for application startup.
INFO:     Application startup complete.

http://127.0.0.1:8001/docs#/





(.venv) C:\github\fastapi_apps\06_redis_warehouse_store\web-ui>npx create-react-app .
Need to install the following packages:
create-react-app@5.1.0
Ok to proceed? (y) y

npm warn deprecated inflight@1.0.6: This module is not supported, and leaks memory. Do not use it. Check out lru-cache if you want a good and tested way to coalesce async requests by a key value, which is much more comprehensive and powerful.
npm warn deprecated fstream-ignore@1.0.5: This package is no longer supported.
npm warn deprecated uid-number@0.0.6: This package is no longer supported.
npm warn deprecated glob@7.2.3: Glob versions prior to v9 are no longer supported
npm warn deprecated rimraf@2.7.1: Rimraf versions prior to v4 are no longer supported
npm warn deprecated fstream@1.0.12: This package is no longer supported.
npm warn deprecated tar@2.2.2: This version of tar is no longer supported, and will not receive security updates. Please upgrade asap.
create-react-app is deprecated.

You can find a list of up-to-date React frameworks on react.dev
For more info see:https://react.dev/link/cra

This error message will only be shown once per install.

Creating a new React app in C:\github\fastapi_apps\06_redis_warehouse_store\web-ui.

Installing packages. This might take a couple of minutes.
Installing react, react-dom, and react-scripts with cra-template...

