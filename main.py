from fastapi import Depends, FastAPI, HTTPException, Path, Query, status
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, Field
from typing import List, Optional
from config.database import engine, Base, get_db
from sqlalchemy.orm import Session


from midlewares.error_handler import ErrorHandler
from model import User
from utils import create_token, decode_token
from routers.movie import movie_router

app = FastAPI()
app.title = "My API"
app.description = "This is a fantastic API"
app.version = "1.0.0"

app.add_middleware(ErrorHandler)
http_bearer = HTTPBearer()

Base.metadata.create_all(bind=engine)
app.include_router(movie_router)

@app.get("/", tags=["Root"])
def read_root():
    return {"Hello": "World"}


@app.post('/login', tags=['auth'])
def login(user: User):
    if user.email == "admin@gmail.com" and user.password == "admin":
        token: str = create_token({"sub": user.email})
        return JSONResponse(status_code=200, content={"access_token": token, "token_type": "bearer"})
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email o contraseña incorrectos")

@app.get("/users/me", tags=["users"])
def read_users_me(credentials: HTTPAuthorizationCredentials = Depends(http_bearer)):
    token = credentials.credentials
    decoded_token = decode_token(token)
    if decoded_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"email": decoded_token["sub"]}
