"""
Autenticación del microservicio por API Key.
Cada petición del monolito PHP debe incluir el header: X-API-Key
"""

import hmac
from fastapi import HTTPException, Header, status
from app.config import IA_API_KEY


async def verificar_api_key(x_api_key: str = Header(..., alias="X-API-Key")) -> bool:
    """
    Verifica que el header X-API-Key coincida con la clave configurada en el .env.
    Usa hmac.compare_digest para comparación en tiempo constante (evita timing attacks).
    """
    if not IA_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"exito": False, "mensaje": "IA_API_KEY no configurada en el servidor."}
        )

    if not hmac.compare_digest(x_api_key, IA_API_KEY):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"exito": False, "mensaje": "API Key inválida."}
        )

    return True
