from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 配置 CORS，允许前端访问
origins = [
    "http://localhost:5173",  # Vue 默认端口
    "http://localhost:8080",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI backend!"}

@app.get("/api/info")
def get_info():
    return {
        "forum_name": "My Tech Forum",
        "version": "1.0.0",
        "status": "running"
    }
