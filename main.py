from fastapi import FastAPI
from config.database import engine, Base

from midlewares.error_handler import ErrorHandler
from routers.movie_router import movie_router
from routers.user import user_router


app = FastAPI()
app.title = "My API"
app.description = "This is a fantastic API"
app.version = "1.0.0"

app.add_middleware(ErrorHandler)

Base.metadata.create_all(bind=engine)
app.include_router(user_router)
app.include_router(movie_router)

@app.get("/", tags=["Root"])
def read_root():
    return {"Hello": "World"}
