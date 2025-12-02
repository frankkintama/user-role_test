from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from api.routers.user_router import router
from api.configs.db import engine, Base
from api.routers.user_router import router as user_router
from api.routers.auth_router import router as auth_router
from api.routers.role_router import router as role_router
from src.models.blacklist_model import TokenBlacklist


# Tạo tables khi khởi động
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="User Management API",
    description="Sync FastAPI with PostgreSQL",
    version="1.0.0"
)

app.include_router(auth_router, prefix="/api", tags=["Auth"])
app.include_router(user_router, prefix="/api", tags=["Users"])
app.include_router(role_router, prefix="/api", tags=["Roles"])


@app.get("/")
def root():
    return {
        "message": "User Management API",
        "docs": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)