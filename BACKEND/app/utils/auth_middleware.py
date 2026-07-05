from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.utils.jwt_utils import verificar_token

security = HTTPBearer()


def obtener_usuario_actual(
    credenciales: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token  = credenciales.credentials
    correo = verificar_token(token)

    if correo is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )

    usuario = db.execute(
        text("SELECT id, nombre, correo FROM usuarios WHERE correo = :correo"),
        {"correo": correo}
    ).fetchone()

    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado",
        )

    return {"id": usuario.id, "nombre": usuario.nombre, "correo": usuario.correo}