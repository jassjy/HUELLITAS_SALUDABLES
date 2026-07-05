from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.schemas.user_schema import UserSchema
from app.controllers.auth_controller import register, login

router = APIRouter(prefix="/auth", tags=["Autenticación"])


class LoginSchema(BaseModel):
    correo:   str
    password: str


@router.post("/registro")
def registro(user: UserSchema, db: Session = Depends(get_db)):
    return register(user, db)


@router.post("/login")
def iniciar_sesion(datos: LoginSchema, db: Session = Depends(get_db)):
    return login(datos.correo, datos.password, db)