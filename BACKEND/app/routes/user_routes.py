from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.controllers.user_controller import (
    get_users,
    get_user,
    create_user,
    update_user,
    delete_user
)
from app.schemas.user_schema import UserSchema
from app.utils.auth_middleware import obtener_usuario_actual  # 🔒 NUEVO

# ==========================================
# ROUTER
# ==========================================
router = APIRouter(tags=["Usuarios"])


# ==========================================
# GET ALL USERS — 🔒 PROTEGIDO
# ==========================================
@router.get("/users")
def users(
    db: Session = Depends(get_db),
    usuario_actual = Depends(obtener_usuario_actual)   # <-- requiere JWT
):
    return get_users(db)


# ==========================================
# GET USER BY ID — 🔒 PROTEGIDO
# ==========================================
@router.get("/users/{id}")
def user(
    id: int,
    db: Session = Depends(get_db),
    usuario_actual = Depends(obtener_usuario_actual)   # <-- requiere JWT
):
    return get_user(id, db)


# ==========================================
# CREATE USER — 🌐 PÚBLICO
# (cualquiera puede crear cuenta)
# ==========================================
@router.post("/users")
def store_user(
    user: UserSchema,
    db: Session = Depends(get_db)
):
    return create_user(user, db)


# ==========================================
# UPDATE USER — 🔒 PROTEGIDO
# ==========================================
@router.put("/users/{id}")
def edit_user(
    id: int,
    user: UserSchema,
    db: Session = Depends(get_db),
    usuario_actual = Depends(obtener_usuario_actual)   # <-- requiere JWT
):
    return update_user(id, user, db)


# ==========================================
# DELETE USER — 🔒 PROTEGIDO
# ==========================================
@router.delete("/users/{id}")
def destroy_user(
    id: int,
    db: Session = Depends(get_db),
    usuario_actual = Depends(obtener_usuario_actual)   # <-- requiere JWT
):
    return delete_user(id, db)
