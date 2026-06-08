"""
Schemas (modelos de datos) para los endpoints de reportes.
Definen el contrato de entrada y salida de cada endpoint.
"""

from pydantic import BaseModel, Field
from typing import Optional, List


# ============================================================
# MODELO DE ENTRADA
# ============================================================

class SolicitudReporteInput(BaseModel):
    """
    Datos que envía el monolito PHP para solicitar un análisis IA.
    Python se encarga de consultar la BD y procesar los datos.

    Ejemplo de JSON:
    {
        "tipo_reporte": "general",
        "fecha_inicio": "2026-01-01",
        "fecha_fin": "2026-06-01",
        "genero": "F",
        "pnf": "Ingeniería",
        "area": "Becas"
    }
    """

    tipo_reporte: str = Field(
        ...,
        description="Tipo de reporte a analizar: general, psicologia, medicina, etc.",
        examples=["general", "psicologia", "medicina", "orientacion", "becas"]
    )

    fecha_inicio: Optional[str] = Field(
        None,
        description="Fecha de inicio para filtrar (formato: YYYY-MM-DD)"
    )

    fecha_fin: Optional[str] = Field(
        None,
        description="Fecha de fin para filtrar (formato: YYYY-MM-DD)"
    )

    genero: Optional[str] = Field(
        None,
        description="Filtro por género: M o F"
    )

    pnf: Optional[str] = Field(
        None,
        description="Filtro por nombre del PNF"
    )

    area: Optional[str] = Field(
        None,
        description="Filtro por área/servicio"
    )


# ============================================================
# MODELOS DE SALIDA
# ============================================================

class AnalisisOutput(BaseModel):
    """
    Respuesta con el análisis generado por la IA.

    Ejemplo de respuesta:
    {
        "exito": true,
        "tipo_reporte": "general",
        "total_registros": 150,
        "resumen": "Se analizaron 150 registros...",
        "hallazgos": ["El 60% de los beneficiarios son mujeres", ...],
        "estadisticas": {"por_genero": {"M": 60, "F": 90}},
        "recomendaciones": ["Revisar la distribución...", ...],
        "fecha_analisis": "2026-06-08T18:30:00"
    }
    """

    exito: bool = Field(..., description="Indica si el análisis fue exitoso")
    tipo_reporte: str = Field(..., description="Tipo de reporte analizado")
    total_registros: int = Field(default=0, description="Total de registros analizados")
    resumen: str = Field(..., description="Resumen narrativo del análisis")
    hallazgos: List[str] = Field(default=[], description="Hallazgos importantes")
    estadisticas: dict = Field(default={}, description="Estadísticas calculadas")
    recomendaciones: List[str] = Field(default=[], description="Recomendaciones basadas en el análisis")
    fecha_analisis: str = Field(..., description="Fecha y hora del análisis")


class ErrorOutput(BaseModel):
    """Respuesta estándar de error."""
    exito: bool = False
    mensaje: str
