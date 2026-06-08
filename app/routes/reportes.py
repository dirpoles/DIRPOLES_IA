"""
Rutas (endpoints) para el módulo de análisis de reportes con IA.
Estas rutas quedan bajo el prefijo /api/v1/ (definido en main.py).
"""

from fastapi import APIRouter, HTTPException, Depends

from app.schemas.reportes import SolicitudReporteInput, AnalisisOutput, ErrorOutput
from app.services.analisis import analizar_reporte
from app.security import verificar_api_key

router = APIRouter()


# ============================================================
# ENDPOINT: Analizar un reporte con IA
# ============================================================

@router.post(
    "/analizar",
    response_model=AnalisisOutput,
    summary="Analizar un reporte con IA",
    dependencies=[Depends(verificar_api_key)],
    description="""
    Recibe el tipo de reporte y filtros opcionales.
    Python consulta la BD, procesa los datos y los envía a Gemini
    para generar un análisis narrativo completo.
    Requiere el header X-API-Key con la clave válida.
    """
)
def endpoint_analizar_reporte(solicitud: SolicitudReporteInput):
    """
    Endpoint principal para generar reportes con IA.
    El monolito PHP solo envía filtros, Python hace todo el trabajo pesado.
    """
    try:
        filtros = {
            "fecha_inicio": solicitud.fecha_inicio,
            "fecha_fin": solicitud.fecha_fin,
            "genero": solicitud.genero,
            "pnf": solicitud.pnf,
            "area": solicitud.area,
        }

        resultado = analizar_reporte(
            tipo_reporte=solicitud.tipo_reporte,
            filtros=filtros
        )
        return resultado

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail={"exito": False, "mensaje": str(e)}
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"exito": False, "mensaje": f"Error al analizar el reporte: {str(e)}"}
        )


# ============================================================
# ENDPOINT: Tipos de reportes disponibles
# ============================================================

@router.get(
    "/tipos-reportes",
    summary="Obtener tipos de reportes disponibles",
    description="Devuelve la lista de tipos de reportes que se pueden analizar."
)
def endpoint_tipos_reportes():
    """Lista los tipos de reportes soportados por el microservicio."""
    return {
        "exito": True,
        "tipos": [
            {"id": "general", "nombre": "Reporte General", "descripcion": "Análisis cruzado de todos los servicios", "disponible": True},
            {"id": "psicologia", "nombre": "Psicología", "descripcion": "Morbilidad y citas psicológicas", "disponible": False},
            {"id": "medicina", "nombre": "Medicina", "descripcion": "Consultas médicas e inventario", "disponible": False},
            {"id": "orientacion", "nombre": "Orientación", "descripcion": "Casos de orientación", "disponible": False},
            {"id": "becas", "nombre": "Becas", "descripcion": "Solicitudes y asignaciones de becas", "disponible": False},
            {"id": "discapacidad", "nombre": "Discapacidad", "descripcion": "Atenciones por discapacidad", "disponible": False},
            {"id": "transporte", "nombre": "Transporte", "descripcion": "Vehículos, rutas, proveedores", "disponible": False},
            {"id": "mobiliario", "nombre": "Mobiliario", "descripcion": "Inventario de mobiliario y equipos", "disponible": False},
            {"id": "jornadas", "nombre": "Jornadas Médicas", "descripcion": "Jornadas médicas realizadas", "disponible": False},
            {"id": "referencias", "nombre": "Referencias", "descripcion": "Referencias entre servicios", "disponible": False},
        ]
    }
