
from fastapi import Depends, HTTPException, APIRouter, status
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer


from model import User
from utils import create_token, decode_token

user_router = APIRouter()
http_bearer = HTTPBearer()

@user_router.post('/login', tags=['users'])
def login(user: User):
    if user.email == "admin@gmail.com" and user.password == "admin":
        token: str = create_token({"sub": user.email})
        return JSONResponse(status_code=200, content={"access_token": token, "token_type": "bearer"})
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email o contraseña incorrectos")

@user_router.get("/users/me", tags=["users"])
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
