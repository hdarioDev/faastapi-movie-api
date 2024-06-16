from datetime import datetime, timedelta
from jose import JWTError, jwt
from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

def create_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    print(f"Token expires at: {int(expire.timestamp())} (timestamp) -> {expire} UTC")
    return encoded_jwt

def decode_token(token: str) -> dict:
    try:
        decoded_jwt = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        current_timestamp = datetime.utcnow().timestamp()
        current_time = datetime.utcfromtimestamp(current_timestamp)
        if decoded_jwt["exp"] >= current_timestamp:
            return decoded_jwt
        print("Token has expired")
        return None
    except JWTError as e:
        print(f"JWTError: {e}")
        return None


