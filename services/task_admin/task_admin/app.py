from fastapi import FastAPI
from task_admin import tasks, auth
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.include_router(tasks.views.router)
app.include_router(auth.views.router)

origins = [
    "http://localhost:8080",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api")
async def root():
    return {"message": "Hello Bigger Applications!"}