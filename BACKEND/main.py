from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config.database import Base, engine
from app.routes import auth_routes, user_routes

# Crear todas las tablas en la base de datos al iniciar
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API con Autenticación JWT",
    description="API REST con FastAPI, SQLAlchemy y autenticación JWT",
    version="1.0.0"
)

# ==========================================
# CORS — necesario para que el frontend (otro origen/puerto)
# pueda llamar a esta API desde el navegador
# ==========================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # en producción, reemplaza "*" por el dominio real del frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar las rutas
app.include_router(auth_routes.router)
app.include_router(user_routes.router)


@app.get("/", tags=["Inicio"])
def inicio():
    """Endpoint público de bienvenida"""
    return {"mensaje": "API funcionando correctamente"}