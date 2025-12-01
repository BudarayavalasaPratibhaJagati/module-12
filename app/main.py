from fastapi import FastAPI

from app.routers import users, calculations
from app import models
from app.database import engine

app = FastAPI()

# Include routers
app.include_router(users.router)
app.include_router(calculations.router)

# Make sure tables exist
models.Base.metadata.create_all(bind=engine)
