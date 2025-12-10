import os
from fastapi import HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
path_to_token = ROOT_DIR / 'sql' /'data' / 'secret' / 'token.env'

load_dotenv(path_to_token)
API_TOKEN = os.getenv('API_TOKEN')

security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    if credentials.scheme.lower() != "bearer":
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "Invalid authentication scheme.")
    
    if credentials.credentials != API_TOKEN:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "Invalid token.")
    
    return True