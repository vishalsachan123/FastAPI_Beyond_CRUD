from fastapi import FastAPI

app = FastAPI(title='simaple app')


@app.get('/')
async def index():
    return {"msg": "Hello"}

