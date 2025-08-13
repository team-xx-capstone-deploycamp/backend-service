import secrets
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from app.core.config import settings

security = HTTPBasic()

def verify_basic_auth(credentials: HTTPBasicCredentials = Depends(security)) -> str:
    user_ok = secrets.compare_digest(credentials.username, settings.basic_auth_username)
    pass_ok = secrets.compare_digest(credentials.password, settings.basic_auth_password)
    if not (user_ok and pass_ok):
        # Ensure clients see a 401 and are prompted for Basic credentials
        raise HTTPException(status_code=401, detail="Unauthorized", headers={"WWW-Authenticate": "Basic"})
    return credentials.username
