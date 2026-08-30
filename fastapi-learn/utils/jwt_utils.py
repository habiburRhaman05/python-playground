from datetime import datetime, timedelta, timezone
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

# Configuration (Ensure this is identical for encoding and decoding)
SECRET_KEY = "your-highly-secure-secret-key-change-this"
ALGORITHM = "HS256"

# 3. CORE TOKEN FUNCTIONS
def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    current_time = datetime.now(timezone.utc)
    
    if expires_delta:
        expire = current_time + expires_delta
    else:
        expire = current_time + timedelta(minutes=30) 
        
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_access_token(token: str) -> dict | None:
    try:
        print("verofy-iput",token)
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        print("DEBUG decoded payload:", payload)

        return payload

    except (ExpiredSignatureError, InvalidTokenError) as e:
        print("🔥 JWT ERROR:", type(e).__name__, str(e))
        return None