from fastapi import FastAPI
from app.api.routes.repositories import router
from app.core.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="GitHub Tracker API")

app.include_router(router)
