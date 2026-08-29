from fastapi.security import OAuth2PasswordBearer

# Define it once here. The tokenUrl should match your actual login route path.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")