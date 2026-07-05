from datetime import datetime, timedelta
from jose import JWTError, jwt
import bcrypt as _bcrypt
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY                  = os.getenv("SECRET_KEY", "clave_secreta_cambiar")
ALGORITHM                   = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))


def encriptar_password(password: str) -> str:
    return _bcrypt.hashpw(password[:72].encode(), _bcrypt.gensalt()).decode()

def verificar_password(password_plano: str, password_hash: str) -> bool:
    return _bcrypt.checkpw(password_plano[:72].encode(), password_hash.encode())

def crear_token(data: dict) -> str:
    datos = data.copy()
    expira = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    datos.update({"exp": expira})
    return jwt.encode(datos, SECRET_KEY, algorithm=ALGORITHM)

def verificar_token(token: str) -> str | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None