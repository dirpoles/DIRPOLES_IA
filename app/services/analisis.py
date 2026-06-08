"""
Servicio de análisis de datos con IA utilizando Google AI Studio (Gemini).
Consulta la BD, procesa los datos y los envía a Gemini para generar el reporte.
"""

import json
import urllib.request
import urllib.error
from datetime import datetime
from collections import Counter
from app.config import GEMINI_API_KEY


# ============================================================
# Función para llamar a la API de Gemini
# ============================================================

def llamar_gemini(prompt: str, system_instruction: str = None) -> str:
    """
    Realiza una petición HTTP POST a la API de Gemini en Google AI Studio.
    Retorna el texto de la respuesta.
    """
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY no está configurada en las variables de entorno.")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

    contents = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }

    if system_instruction:
        contents["systemInstruction"] = {
            "parts": [{"text": system_instruction}]
        }

    # Forzar respuesta en formato JSON
    contents["generationConfig"] = {
        "responseMimeType": "application/json"
    }

    data_bytes = json.dumps(contents).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=data_bytes,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            res_body = response.read().decode("utf-8")
            res_data = json.loads(res_body)
            parts = res_data["candidates"][0]["content"]["parts"]
            return parts[0]["text"]
    except urllib.error.HTTPError as e:
        error_content = e.read().decode("utf-8")
        raise RuntimeError(f"Error de la API de Gemini (HTTP {e.code}): {error_content}")
    except Exception as e:
        raise RuntimeError(f"Error al conectar con la API de Gemini: {str(e)}")


# ============================================================
# Procesamiento de datos crudos para generar estadísticas
# ============================================================

def procesar_datos_crudos(filas: list) -> dict:
    """
    Toma las filas crudas de la BD y genera estadísticas resumidas
    para enviar a Gemini (reduce el tamaño del payload).
    """
    total = len(filas)
    conteo_pnf = {}
    conteo_genero = {}
    conteo_servicio = {}
    conteo_mes = {}

    for fila in filas:
        # PNF
        pnf_nombre = fila.get("nombre_pnf") or "No especificado"
        conteo_pnf[pnf_nombre] = conteo_pnf.get(pnf_nombre, 0) + 1

        # Género
        gen_raw = fila.get("genero", "")
        if gen_raw == "M":
            gen = "Masculino"
        elif gen_raw == "F":
            gen = "Femenino"
        else:
            gen = "No especificado"
        conteo_genero[gen] = conteo_genero.get(gen, 0) + 1

        # Servicio
        serv = fila.get("nombre_serv") or "No especificado"
        conteo_servicio[serv] = conteo_servicio.get(serv, 0) + 1

        # Mes (para tendencias)
        fecha_raw = fila.get("fecha_creacion")
        if fecha_raw:
            try:
                if isinstance(fecha_raw, datetime):
                    mes_key = fecha_raw.strftime("%Y-%m")
                else:
                    mes_key = str(fecha_raw)[:7]  # "2026-01"
                conteo_mes[mes_key] = conteo_mes.get(mes_key, 0) + 1
            except Exception:
                pass

    return {
        "total_registros": total,
        "distribucion_pnf": conteo_pnf,
        "distribucion_genero": conteo_genero,
        "distribucion_servicios": conteo_servicio,
        "distribucion_mensual": dict(sorted(conteo_mes.items()))
    }


# ============================================================
# Función principal de análisis
# ============================================================

def analizar_reporte(tipo_reporte: str, filtros: dict) -> dict:
    """
    Flujo completo:
    1. Obtiene los datos crudos de la BD según el tipo de reporte
    2. Procesa y resume las estadísticas
    3. Envía a Gemini para generar el análisis narrativo
    4. Retorna el resultado estructurado

    Parámetros:
        tipo_reporte: Tipo de reporte (general, psicologia, etc.)
        filtros: dict con fecha_inicio, fecha_fin, genero, pnf, area
    """

    # 1. Obtener datos crudos de la BD
    filas = _obtener_datos(tipo_reporte, filtros)

    if not filas:
        return {
            "exito": True,
            "tipo_reporte": tipo_reporte,
            "total_registros": 0,
            "resumen": "No se encontraron registros que coincidan con los filtros seleccionados.",
            "hallazgos": [],
            "estadisticas": {},
            "recomendaciones": ["Verifique los filtros seleccionados o amplíe el rango de fechas."],
            "fecha_analisis": datetime.now().isoformat()
        }

    # 2. Procesar estadísticas
    estadisticas = procesar_datos_crudos(filas)

    # 3. Generar análisis con Gemini
    resumen, hallazgos, recomendaciones = _generar_analisis_ia(
        tipo_reporte, estadisticas, filtros
    )

    return {
        "exito": True,
        "tipo_reporte": tipo_reporte,
        "total_registros": estadisticas["total_registros"],
        "resumen": resumen,
        "hallazgos": hallazgos,
        "estadisticas": estadisticas,
        "recomendaciones": recomendaciones,
        "fecha_analisis": datetime.now().isoformat()
    }


def _obtener_datos(tipo_reporte: str, filtros: dict) -> list:
    """
    Importa y ejecuta el repositorio correspondiente al tipo de reporte.
    Cada tipo de reporte tendrá su propio archivo en app/repositories/.
    """
    if tipo_reporte == "general":
        from app.repositories.reporte_general import obtener_datos_reporte_general
        return obtener_datos_reporte_general(
            fecha_inicio=filtros.get("fecha_inicio"),
            fecha_fin=filtros.get("fecha_fin"),
            genero=filtros.get("genero"),
            pnf=filtros.get("pnf"),
            area=filtros.get("area")
        )
    else:
        raise ValueError(f"Tipo de reporte '{tipo_reporte}' no implementado aún.")


def _generar_analisis_ia(tipo_reporte: str, estadisticas: dict, filtros: dict) -> tuple:
    """
    Envía las estadísticas a Gemini y retorna (resumen, hallazgos, recomendaciones).
    Si Gemini falla, usa un fallback offline.
    """
    # Fallback por defecto
    resumen_fallback = _generar_resumen_offline(tipo_reporte, estadisticas, filtros)
    hallazgos_fallback = _generar_hallazgos_offline(estadisticas)
    recomendaciones_fallback = ["Revisar la distribución de atenciones entre servicios y PNF para equilibrar la carga."]

    if not GEMINI_API_KEY:
        return resumen_fallback, hallazgos_fallback, recomendaciones_fallback

    try:
        datos_str = json.dumps(estadisticas, indent=2, ensure_ascii=False)

        filtros_texto = (
            f"- Fecha inicio: {filtros.get('fecha_inicio') or 'No especificada'}\n"
            f"- Fecha fin: {filtros.get('fecha_fin') or 'No especificada'}\n"
            f"- Género: {filtros.get('genero') or 'Todos'}\n"
            f"- PNF: {filtros.get('pnf') or 'Todos'}\n"
            f"- Área: {filtros.get('area') or 'Todos'}"
        )

        prompt = (
            f"Analiza el siguiente reporte de tipo '{tipo_reporte}' del sistema DIRPOLES.\n\n"
            f"Filtros aplicados:\n{filtros_texto}\n\n"
            f"Estadísticas del reporte:\n{datos_str}\n\n"
            f"Genera un análisis completo basado en estos datos.\n"
            f"Retorna ÚNICAMENTE el JSON estructurado según las instrucciones del sistema."
        )

        system_instruction = (
            "Eres un analista de datos experto del departamento de bienestar estudiantil "
            "y servicios médicos/sociales del instituto DIRPOLES.\n"
            "Tu tarea es analizar las estadísticas del reporte proporcionado y generar "
            "un informe narrativo estructurado en formato JSON con la siguiente estructura exacta:\n"
            "{\n"
            '  "resumen": "Un resumen analítico detallado en lenguaje natural y profesional '
            'sobre la actividad reportada, destacando lo más importante, tendencias e implicaciones.",\n'
            '  "hallazgos": ["Hallazgo 1 con porcentajes o números clave", "Hallazgo 2..."],\n'
            '  "recomendaciones": ["Recomendación accionable 1", "Recomendación 2..."]\n'
            "}\n"
            "Asegúrate de que la respuesta sea estrictamente un objeto JSON válido con esas tres claves."
        )

        respuesta_texto = llamar_gemini(prompt, system_instruction)

        # Limpiar posibles bloques de código markdown
        if respuesta_texto.strip().startswith("```"):
            lines = respuesta_texto.strip().split("\n")
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines[-1].startswith("```"):
                lines = lines[:-1]
            respuesta_texto = "\n".join(lines).strip()

        ia_data = json.loads(respuesta_texto)

        resumen = ia_data.get("resumen", resumen_fallback)
        hallazgos = ia_data.get("hallazgos", hallazgos_fallback)
        recomendaciones = ia_data.get("recomendaciones", recomendaciones_fallback)

        return resumen, hallazgos, recomendaciones

    except Exception as e:
        print(f"[Fallback] Error con Gemini: {str(e)}")
        return resumen_fallback, hallazgos_fallback, recomendaciones_fallback


# ============================================================
# Funciones de fallback offline
# ============================================================

def _generar_resumen_offline(tipo_reporte: str, estadisticas: dict, filtros: dict) -> str:
    """Genera un resumen básico sin IA."""
    total = estadisticas.get("total_registros", 0)
    partes = [f"Se analizaron {total} registros del reporte de '{tipo_reporte}'."]

    fecha_inicio = filtros.get("fecha_inicio")
    fecha_fin = filtros.get("fecha_fin")
    if fecha_inicio and fecha_fin:
        partes.append(f"Período: desde {fecha_inicio} hasta {fecha_fin}.")

    return " ".join(partes)


def _generar_hallazgos_offline(estadisticas: dict) -> list:
    """Genera hallazgos básicos sin IA."""
    hallazgos = []
    total = estadisticas.get("total_registros", 0)

    # Género
    dist_genero = estadisticas.get("distribucion_genero", {})
    for gen, cant in dist_genero.items():
        porc = round((cant / total) * 100, 1) if total > 0 else 0
        hallazgos.append(f"El {porc}% corresponde a género {gen} ({cant} de {total}).")

    # Top PNF
    dist_pnf = estadisticas.get("distribucion_pnf", {})
    if dist_pnf:
        top = sorted(dist_pnf.items(), key=lambda x: x[1], reverse=True)[:3]
        nombres = [f"{n} ({c})" for n, c in top]
        hallazgos.append(f"PNF más frecuentes: {', '.join(nombres)}.")

    # Top servicio
    dist_serv = estadisticas.get("distribucion_servicios", {})
    if dist_serv:
        top = sorted(dist_serv.items(), key=lambda x: x[1], reverse=True)[:1]
        if top:
            hallazgos.append(f"Servicio más utilizado: '{top[0][0]}' con {top[0][1]} atenciones.")

    return hallazgos
