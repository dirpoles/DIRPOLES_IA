"""
Schemas (modelos de datos) para los endpoints de reportes.

Definen QUÉ datos se esperan recibir y QUÉ datos se van a devolver.
Es como definir un "contrato" o "formulario" para cada endpoint.

En tu PHP, las validaciones están dispersas en los Models.
Aquí se centralizan en un solo lugar.
"""

from pydantic import BaseModel, Field
<<<<<<< HEAD
from typing import Optional, List
=======
from typing import Optional, List, Union
>>>>>>> 5e14c6e (Microservicio primera parte)
from datetime import datetime


# ============================================================
# MODELOS DE ENTRADA (lo que el frontend envía al microservicio)
# ============================================================

class DatosReporteInput(BaseModel):
    """
    Datos que envía el frontend para solicitar un análisis IA.

    'BaseModel' es la clase padre de Pydantic que activa la
    validación automática. Todas las clases de datos heredan de ella.

    Ejemplo de JSON que debe enviar el frontend:
    {
        "tipo_reporte": "general",
        "datos": [
            {"nombre": "Juan", "cedula": "V-12345678", ...},
            {"nombre": "María", "cedula": "V-87654321", ...}
        ],
        "fecha_inicio": "2026-01-01",
        "fecha_fin": "2026-03-31"
    }
    """

    # 'tipo_reporte' debe ser un string (texto)
    # Field(...) significa que es OBLIGATORIO (no puede faltar)
    # description es una descripción que aparece en la documentación automática
    tipo_reporte: str = Field(
        ...,
        description="Tipo de reporte a analizar: general, psicologia, medicina, etc.",
        examples=["general", "psicologia", "medicina", "orientacion", "becas"]
    )

<<<<<<< HEAD
    # 'datos' es una Lista de diccionarios (cada elemento es un registro del reporte)
    # List[dict] = lista de diccionarios
    datos: List[dict] = Field(
        ...,
        description="Array con los datos del reporte a analizar"
=======
    # 'datos' es una Lista de diccionarios o un diccionario con el resumen
    datos: Union[List[dict], dict] = Field(
        ...,
        description="Array o diccionario con los datos del reporte a analizar"
>>>>>>> 5e14c6e (Microservicio primera parte)
    )

    # Filtros opcionales
    # Optional[str] = puede ser un string O puede ser None (no enviado)
    # El valor por defecto es None (no obligatorio)
    fecha_inicio: Optional[str] = Field(
        None,
        description="Fecha de inicio para filtrar (formato: YYYY-MM-DD)"
    )

    fecha_fin: Optional[str] = Field(
        None,
        description="Fecha de fin para filtrar (formato: YYYY-MM-DD)"
    )


class PreguntaReporteInput(BaseModel):
    """
    Para cuando el usuario hace una pregunta sobre los datos.

    Ejemplo de JSON:
    {
        "pregunta": "¿Cuál es el PNF con más beneficiarios atendidos?",
        "tipo_reporte": "general",
        "datos": [...]
    }
    """

    pregunta: str = Field(
        ...,
        description="La pregunta del usuario sobre los datos del reporte",
        min_length=5,
        max_length=500
    )

    tipo_reporte: str = Field(
        ...,
        description="Tipo de reporte sobre el que se pregunta"
    )

<<<<<<< HEAD
    datos: List[dict] = Field(
=======
    datos: Union[List[dict], dict] = Field(
>>>>>>> 5e14c6e (Microservicio primera parte)
        ...,
        description="Los datos del reporte para contexto"
    )


# ============================================================
# MODELOS DE SALIDA (lo que el microservicio devuelve al frontend)
# ============================================================

class AnalisisOutput(BaseModel):
    """
    Respuesta con el análisis generado por la IA.

    Ejemplo de JSON de respuesta:
    {
        "exito": true,
        "tipo_reporte": "general",
        "resumen": "Se analizaron 150 registros. El servicio más utilizado...",
        "hallazgos": [
            "El 60% de los beneficiarios son mujeres",
            "El PNF más atendido es Ingeniería"
        ],
        "estadisticas": {
            "total_registros": 150,
            "por_genero": {"M": 60, "F": 90}
        },
        "fecha_analisis": "2026-04-11T10:30:00"
    }
    """

    exito: bool = Field(
        ...,
        description="Indica si el análisis fue exitoso"
    )

    tipo_reporte: str = Field(
        ...,
        description="Tipo de reporte que fue analizado"
    )

    resumen: str = Field(
        ...,
        description="Resumen en lenguaje natural del análisis"
    )

    hallazgos: List[str] = Field(
        default=[],
        description="Lista de hallazgos importantes encontrados"
    )

    estadisticas: dict = Field(
        default={},
        description="Diccionario con estadísticas calculadas"
    )

    recomendaciones: List[str] = Field(
        default=[],
        description="Sugerencias basadas en el análisis"
    )

    fecha_analisis: str = Field(
        ...,
        description="Fecha y hora del análisis"
    )


class RespuestaIA(BaseModel):
    """
    Respuesta a una pregunta del usuario sobre los datos.
    """

    exito: bool
    pregunta: str
    respuesta: str = Field(
        ...,
        description="Respuesta generada por la IA en lenguaje natural"
    )
    datos_soporte: Optional[dict] = Field(
        None,
        description="Datos numéricos que soportan la respuesta"
    )


class ErrorOutput(BaseModel):
    """
    Respuesta estándar de error.
    Similar a tu formato: {"exito": false, "mensaje": "..."}
    """

    exito: bool = False
    mensaje: str
