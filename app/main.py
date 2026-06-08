"""
Punto de entrada del microservicio DIRPOLES IA.
Equivalente a: DIRPOLES_4/index.php

Aquí se:
1. Crea la aplicación FastAPI
2. Configura CORS (para que el navegador permita las peticiones)
3. Registra las rutas (endpoints)
4. Define el endpoint de salud (health check)
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import ALLOWED_ORIGINS, SERVER_HOST, SERVER_PORT

# ============================================================
# 1. CREAR LA APLICACIÓN
# ============================================================
# Esto es como crear tu Router en PHP, pero FastAPI hace mucho más.

app = FastAPI(
    title="DIRPOLES IA - Microservicio de Inteligencia Artificial",
    description="""
    Microservicio que provee análisis con inteligencia artificial
    para los reportes estadísticos del sistema DIRPOLES_4.
    
    Este servicio es independiente del sistema PHP principal 
    y se comunica con él a través de peticiones HTTP (API REST).
    """,
    version="1.0.0",
    # Prefijo de la documentación automática
    docs_url="/docs",       # Swagger UI: http://localhost:8000/docs
    redoc_url="/redoc",     # ReDoc: http://localhost:8000/redoc
)

# ============================================================
# 2. CONFIGURAR CORS
# ============================================================
# Esto permite que DIRPOLES_4 (corriendo en localhost:80) 
# haga peticiones a este microservicio (corriendo en localhost:8000)

app.add_middleware(
    CORSMiddleware,
    # Orígenes permitidos (de dónde pueden venir las peticiones)
    allow_origins=ALLOWED_ORIGINS,
    # Permitir envío de cookies/credenciales
    allow_credentials=True,
    # Métodos HTTP permitidos
    allow_methods=["GET", "POST"],
    # Headers permitidos en las peticiones
    allow_headers=["*"],
)

# ============================================================
# 3. REGISTRAR RUTAS
# ============================================================
# Importamos y registramos las rutas desde los archivos del directorio routes/
# Es equivalente a tu archivo routes.php que hace:
#   foreach (glob(BASE_PATH . 'app/routes/*.php') as $rutaArchivo) {
#       require_once $rutaArchivo;
#   }

from app.routes import reportes as rutas_reportes

# "prefix" agrega un prefijo a todas las rutas del módulo
# "tags" agrupa las rutas en la documentación automática
app.include_router(
    rutas_reportes.router,
    prefix="/api/v1",
    tags=["Reportes IA"]
)

# ============================================================
# 4. ENDPOINT DE SALUD (Health Check)
# ============================================================
# Es una ruta simple que sirve para verificar que el microservicio
# está vivo y respondiendo. Es una práctica estándar en microservicios.

@app.get("/")
def health_check():
    """
    Verificar que el microservicio está activo.
    
    Equivalente a visitar http://localhost:8000/ en el navegador.
    Si ves este JSON, el servicio está funcionando.
    """
    return {
        "estado": "activo",
        "servicio": "DIRPOLES IA",
        "version": "1.0.0",
        "mensaje": "El microservicio de Inteligencia Artificial está funcionando correctamente"
    }


@app.get("/health")
<<<<<<< HEAD
=======
@app.get("/api/health")
@app.get("/api/v1/health")
>>>>>>> 5e14c6e (Microservicio primera parte)
def health_detailed():
    """
    Verificación detallada del estado del servicio.
    Incluye verificación de conexión a la base de datos.
    """
    # Intentamos conectar a la BD para verificar
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
        "version": "1.0.0"
    }


# ============================================================
# 5. ARRANQUE DEL SERVIDOR (solo si se ejecuta directamente)
# ============================================================
# Este bloque solo se ejecuta cuando corres: python -m app.main
# En producción, usarías: uvicorn app.main:app --host 0.0.0.0 --port 8000

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=SERVER_HOST,
        port=SERVER_PORT,
        reload=True  # Recarga automática al cambiar código (solo para desarrollo)
    )
