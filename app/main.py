from fastapi import FastAPI
from api import auth, anime, favorites, history
from models.database import Base, engine

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(anime.router)
app.include_router(favorites.router)
app.include_router(history.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to SparkyRoll API!"}