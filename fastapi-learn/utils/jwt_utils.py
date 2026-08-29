from datetime import datetime, timedelta, timezone
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

# Configuration (In production, load these from environment variables)
SECRET_KEY = "your-highly-secure-secret-key-change-this"
ALGORITHM = "HS256"

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    
    
    current_time = datetime.now(timezone.utc)
    
    if expires_delta:
        expire = current_time + expires_delta
    else:
        expire = current_time + timedelta(minutes=30) 
        
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str) -> dict | None:
    print(token)
    try:
        # PyJWT automatically validates the 'exp' claim during decoding
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(payload)
        return payload
    except ExpiredSignatureError:
        print("Token verification failed: Token has expired.")
        return None
    except InvalidTokenError:
        print("Token verification failed: Token is invalid.")
        return None
