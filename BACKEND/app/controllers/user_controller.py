from sqlalchemy import text
from sqlalchemy.orm import Session

from app.schemas.user_schema import UserSchema
from app.utils.response import api_response


# ==========================================
# GET ALL USERS
# ==========================================
def get_users(db: Session):

    query = text("""
        SELECT
            id,
            nombre,
            correo,
            created_at
        FROM usuarios
        ORDER BY id
    """)

    result = db.execute(query)

    users = [
        {
            "id": row.id,
            "nombre": row.nombre,
            "correo": row.correo,
            "created_at": row.created_at
        }
        for row in result
    ]

    return api_response(
        success=True,
        message="Lista de usuarios",
        data=users
    )


# ==========================================
# GET USER BY ID
# ==========================================
def get_user(
    id: int,
    db: Session
):

    query = text("""
        SELECT
            id,
            nombre,
            correo,
            created_at
        FROM usuarios
        WHERE id = :id
    """)

    result = db.execute(
        query,
        {"id": id}
    )

    user = result.fetchone()

    if not user:
        return api_response(
            success=False,
            message="Usuario no encontrado"
        )

    return api_response(
        success=True,
        message="Usuario encontrado",
        data={
            "id": user.id,
            "nombre": user.nombre,
            "correo": user.correo,
            "created_at": user.created_at
        }
    )


# ==========================================
# CREATE USER
# ==========================================
def create_user(
    user: UserSchema,
    db: Session
):

    # Verificar si el correo ya existe
    query_exists = text("""
        SELECT id
        FROM usuarios
        WHERE correo = :correo
    """)

    exists = db.execute(
        query_exists,
        {"correo": user.correo}
    ).fetchone()

    if exists:
        return api_response(
            success=False,
            message="El correo ya está registrado"
        )

    query = text("""
        INSERT INTO usuarios (
            nombre,
            correo,
            password
        )
        VALUES (
            :nombre,
            :correo,
            :password
        )
    """)

    db.execute(
        query,
        {
            "nombre": user.nombre,
            "correo": user.correo,
            "password": user.password
        }
    )

    db.commit()

    return api_response(
        success=True,
        message="Usuario creado correctamente"
    )


# ==========================================
# UPDATE USER
# ==========================================
def update_user(
    id: int,
    user: UserSchema,
    db: Session
):

    query = text("""
        UPDATE usuarios
        SET
            nombre = :nombre,
            correo = :correo,
            password = :password
        WHERE id = :id
    """)

    result = db.execute(
        query,
        {
            "id": id,
            "nombre": user.nombre,
            "correo": user.correo,
            "password": user.password
        }
    )

    db.commit()

    if result.rowcount == 0:
        return api_response(
            success=False,
            message="Usuario no encontrado"
        )

    return api_response(
        success=True,
        message="Usuario actualizado correctamente"
    )


# ==========================================
# DELETE USER
# ==========================================
def delete_user(
    id: int,
    db: Session
):

    query = text("""
        DELETE FROM usuarios
        WHERE id = :id
    """)

    result = db.execute(
        query,
        {"id": id}
    )

    db.commit()

    if result.rowcount == 0:
        return api_response(
            success=False,
            message="Usuario no encontrado"
        )

    return api_response(
        success=True,
        message="Usuario eliminado correctamente"
    )