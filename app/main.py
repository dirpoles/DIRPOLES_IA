"""
Punto de entrada del microservicio DIRPOLES IA.

Aquí se:
1. Crea la aplicación FastAPI
2. Configura CORS
3. Registra las rutas (endpoints)
4. Define el endpoint de salud (health check)
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import ALLOWED_ORIGINS, SERVER_HOST, SERVER_PORT

# ============================================================
# 1. CREAR LA APLICACIÓN
# ============================================================

app = FastAPI(
    title="DIRPOLES IA - Microservicio de Inteligencia Artificial",
    description="""
    Microservicio que provee análisis con inteligencia artificial
    para los reportes estadísticos del sistema DIRPOLES_4.
    
    Se comunica con el monolito PHP a través de API REST,
    autenticado por API Key (X-API-Key).
    """,
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ============================================================
# 2. CONFIGURAR CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# ============================================================
# 3. REGISTRAR RUTAS
# ============================================================

from app.routes import reportes as rutas_reportes

app.include_router(
    rutas_reportes.router,
    prefix="/api/v1",
    tags=["Reportes IA"]
)

# ============================================================
# 4. HEALTH CHECK
# ============================================================

@app.get("/")
def health_check():
    """Verificar que el microservicio está activo."""
    return {
        "estado": "activo",
        "servicio": "DIRPOLES IA",
        "version": "2.0.0",
        "mensaje": "El microservicio de Inteligencia Artificial está funcionando correctamente"
    }


@app.get("/health")
@app.get("/api/health")
@app.get("/api/v1/health")
def health_detailed():
    """Verificación detallada: incluye estado de la BD."""
    from app.database import ejecutar_consulta
    try:
        ejecutar_consulta("SELECT 1")
        db_status = "conectada"
    except Exception as e:
        db_status = f"error: {str(e)}"

    return {
        "estado": "activo",
        "base_de_datos": db_status,
        "servicio": "DIRPOLES IA",
        "version": "2.0.0"
    }


# ============================================================
# 5. ARRANQUE DEL SERVIDOR
# ============================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=SERVER_HOST,
        port=SERVER_PORT,
        reload=True
    )
