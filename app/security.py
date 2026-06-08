"""
<<<<<<< HEAD
Agregar en app/security.py
"""

from fastapi import Header, HTTPException
from app.config import API_SECRET_KEY


async def verificar_api_key(x_api_key: str = Header(...)):
    """
    Dependencia de seguridad que verifica que la petición 
    incluya un header 'X-API-Key' con la clave correcta.
    
    Uso en un endpoint:
        @router.post("/analizar")
        def analizar(datos: ..., _: str = Depends(verificar_api_key)):
            ...
    """
    if x_api_key != API_SECRET_KEY:
        raise HTTPException(
            status_code=403,
            detail={
                "exito": False,
                "mensaje": "Clave de API inválida. Acceso denegado."
            }
        )
    return x_api_key
=======
Módulo de seguridad para la autenticación de peticiones en el microservicio.
Implementa validación simétrica de tokens con X-API-Key para la conexión backend-to-backend.
"""

from fastapi import HTTPException, Header, status
from app.config import API_KEY

async def autenticar_peticion(x_api_key: str = Header(None, alias="X-API-Key")) -> dict:
    """
    Dependencia de seguridad que valida que la llave X-API-Key enviada por el backend
    coincida con la llave configurada en el archivo .env del microservicio.
    """
    header_key = x_api_key.strip() if x_api_key else None
    config_key = API_KEY.strip() if API_KEY else None

    if not header_key or header_key != config_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "exito": False,
                "mensaje": "Clave de API (X-API-Key) inválida o ausente. Acceso denegado."
            }
        )

    return {
        "autenticado_por": "x_api_key"
    }


>>>>>>> 5e14c6e (Microservicio primera parte)
