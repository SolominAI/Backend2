from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def func():
    return 'Hello World'



# E:\YandexDisk\4 0 Projects\lua_dashbord\import_export\export_stream\1726034697.1.1.txt