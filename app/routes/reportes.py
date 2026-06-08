"""
Rutas (endpoints) para el módulo de análisis de reportes con IA.

Equivalente a: DIRPOLES_4/app/routes/reportes.php
Pero solo para las funcionalidades de IA.

Estas rutas quedarán bajo el prefijo /api/v1/ (definido en main.py)
Ejemplo: POST http://localhost:8000/api/v1/analizar
"""

from fastapi import APIRouter, HTTPException, Depends

# Importar los schemas (modelos de datos de entrada/salida)
from app.schemas.reportes import (
    DatosReporteInput,
    PreguntaReporteInput,
    AnalisisOutput,
    RespuestaIA,
    ErrorOutput
)

# Importar los servicios (lógica de negocio)
from app.services.analisis import analizar_reporte, responder_pregunta

<<<<<<< HEAD
# Importar la verificación de seguridad (API Key)
from app.security import verificar_api_key
=======
# Importar la verificación de seguridad (Autenticación por X-API-Key)
from app.security import autenticar_peticion
>>>>>>> 5e14c6e (Microservicio primera parte)

# Crear el router (agrupador de rutas)
# Es como crear un grupo de rutas en tu PHP
router = APIRouter()


# ============================================================
# ENDPOINT 1: Analizar un reporte
# ============================================================
# Decorador: cuando alguien haga POST a /api/v1/analizar, ejecuta esta función
# response_model indica qué forma tiene la respuesta (para la documentación)
# dependencies=[Depends(verificar_api_key)] = requiere el header X-API-Key válido

@router.post(
    "/analizar",
    response_model=AnalisisOutput,
    summary="Analizar un reporte con IA",
<<<<<<< HEAD
    dependencies=[Depends(verificar_api_key)],
=======
    dependencies=[Depends(autenticar_peticion)],
>>>>>>> 5e14c6e (Microservicio primera parte)
    description="""
    Recibe los datos de un reporte estadístico y devuelve un análisis 
    inteligente que incluye: resumen, hallazgos, estadísticas y recomendaciones.
    
    Los datos deben enviarse en el cuerpo de la petición como JSON.
    Requiere el header X-API-Key con la clave secreta válida.
    """
)
def endpoint_analizar_reporte(datos_entrada: DatosReporteInput):
    """
    Endpoint para analizar datos de reportes.

    Parámetros (automáticos desde el JSON del body):
        datos_entrada: Objeto que contiene tipo_reporte, datos, fecha_inicio, fecha_fin

    FastAPI automáticamente:
    1. Lee el body de la petición como JSON
    2. Valida que cumple con el schema DatosReporteInput
    3. Si no cumple, devuelve un error 422 automáticamente
    4. Si cumple, llama a esta función con el objeto ya validado
    """
    try:
        resultado = analizar_reporte(
            tipo_reporte=datos_entrada.tipo_reporte,
            datos=datos_entrada.datos,
            fecha_inicio=datos_entrada.fecha_inicio,
            fecha_fin=datos_entrada.fecha_fin
        )
        return resultado

    except Exception as e:
        # Si algo sale mal, devolvemos un error 500
        # HTTPException es la forma de FastAPI de devolver errores HTTP
        raise HTTPException(
            status_code=500,
            detail={
                "exito": False,
                "mensaje": f"Error al analizar el reporte: {str(e)}"
            }
        )


# ============================================================
# ENDPOINT 2: Hacer una pregunta sobre un reporte
# ============================================================

@router.post(
    "/preguntar",
    response_model=RespuestaIA,
    summary="Hacer una pregunta sobre los datos",
<<<<<<< HEAD
    dependencies=[Depends(verificar_api_key)],
=======
    dependencies=[Depends(autenticar_peticion)],
>>>>>>> 5e14c6e (Microservicio primera parte)
    description="""
    Envía una pregunta en lenguaje natural junto con los datos de un reporte,
    y la IA intentará responderla basándose en los datos proporcionados.
    Requiere el header X-API-Key con la clave secreta válida.
    """
)
def endpoint_preguntar(datos_entrada: PreguntaReporteInput):
    """
    Endpoint para responder preguntas sobre reportes.
    """
    try:
        resultado = responder_pregunta(
            pregunta=datos_entrada.pregunta,
            tipo_reporte=datos_entrada.tipo_reporte,
            datos=datos_entrada.datos
        )
        return resultado

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "exito": False,
                "mensaje": f"Error al procesar la pregunta: {str(e)}"
            }
        )


# ============================================================
# ENDPOINT 3: Obtener tipos de reportes disponibles
# ============================================================

@router.get(
    "/tipos-reportes",
    summary="Obtener tipos de reportes disponibles",
    description="Devuelve la lista de tipos de reportes que se pueden analizar."
)
def endpoint_tipos_reportes():
    """
    Endpoint informativo que lista los tipos de reportes soportados.
    Esto ayuda al frontend a saber qué opciones mostrar al usuario.
    """
    return {
        "exito": True,
        "tipos": [
            {
                "id": "general",
                "nombre": "Reporte General",
                "descripcion": "Análisis cruzado de todos los servicios"
            },
            {
                "id": "psicologia",
                "nombre": "Psicología",
                "descripcion": "Morbilidad y citas psicológicas"
            },
            {
                "id": "medicina",
                "nombre": "Medicina",
                "descripcion": "Consultas médicas e inventario"
            },
            {
                "id": "orientacion",
                "nombre": "Orientación",
                "descripcion": "Casos de orientación"
            },
            {
                "id": "becas",
                "nombre": "Becas",
                "descripcion": "Solicitudes y asignaciones de becas"
            },
            {
                "id": "discapacidad",
                "nombre": "Discapacidad",
                "descripcion": "Atenciones por discapacidad"
            },
            {
                "id": "transporte",
                "nombre": "Transporte",
                "descripcion": "Vehículos, rutas, proveedores"
            },
            {
                "id": "mobiliario",
                "nombre": "Mobiliario",
                "descripcion": "Inventario de mobiliario y equipos"
            },
            {
                "id": "jornadas",
                "nombre": "Jornadas Médicas",
                "descripcion": "Jornadas médicas realizadas"
            },
            {
                "id": "referencias",
                "nombre": "Referencias",
                "descripcion": "Referencias entre servicios"
            }
        ]
    }
