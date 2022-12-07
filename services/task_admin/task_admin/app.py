from fastapi import FastAPI
from task_admin import tasks

app = FastAPI()
app.include_router(tasks.views.router)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
