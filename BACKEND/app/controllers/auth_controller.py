from sqlalchemy import text
from sqlalchemy.orm import Session

from app.schemas.user_schema import UserSchema
from app.utils.response import api_response
from app.utils.jwt_utils import encriptar_password, verificar_password, crear_token


def register(user: UserSchema, db: Session):
    exists = db.execute(
        text("SELECT id FROM usuarios WHERE correo = :correo"),
        {"correo": user.correo}
    ).fetchone()

    if exists:
        return api_response(success=False, message="El correo ya está registrado")

    db.execute(
        text("INSERT INTO usuarios (nombre, correo, password) VALUES (:nombre, :correo, :password)"),
        {
            "nombre":   user.nombre,
            "correo":   user.correo,
            "password": encriptar_password(user.password)
        }
    )
    db.commit()

    return api_response(success=True, message="Usuario registrado correctamente")


def login(correo: str, password: str, db: Session):
    usuario = db.execute(
        text("SELECT id, nombre, correo, password FROM usuarios WHERE correo = :correo"),
        {"correo": correo}
    ).fetchone()

    if not usuario or not verificar_password(password, usuario.password):
        return api_response(success=False, message="Correo o contraseña incorrectos")

    token = crear_token({"sub": usuario.correo})

    return api_response(
        success=True,
        message="Login exitoso",
        data={"access_token": token, "token_type": "bearer"}
    )