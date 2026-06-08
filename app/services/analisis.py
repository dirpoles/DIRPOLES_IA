"""
<<<<<<< HEAD
Servicio de análisis de datos con IA.

Equivalente a la lógica que estaría en tu ReportesModel.php,
pero especializada en análisis inteligente.

NOTA: Esta primera versión usa análisis estadístico básico con Python puro.
Más adelante se puede integrar con OpenAI, scikit-learn, etc.
"""

from datetime import datetime
from typing import List, Optional
from collections import Counter


def analizar_reporte(tipo_reporte: str, datos: List[dict],
                     fecha_inicio: Optional[str] = None,
                     fecha_fin: Optional[str] = None) -> dict:
=======
Servicio de análisis de datos con IA utilizando Google AI Studio (Gemini).

Equivalente a la lógica que estaría en tu ReportesModel.php,
pero especializada en análisis inteligente.
"""

import os
import json
import urllib.request
import urllib.error
from datetime import datetime
from typing import List, Optional, Union
from collections import Counter
from app.config import GEMINI_API_KEY


def llamar_gemini(prompt: str, system_instruction: str = None) -> str:
    """
    Realiza una petición HTTP POST a la API de Gemini 3.5 Flash en Google AI Studio.
    """
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY no está configurada en las variables de entorno.")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash:generateContent?key={GEMINI_API_KEY}"
    
    # Preparar el cuerpo de la petición según la estructura oficial de Gemini API
    contents = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }
    
    if system_instruction:
        contents["systemInstruction"] = {
            "parts": [
                {"text": system_instruction}
            ]
        }

    # Forzar la respuesta en formato JSON
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
        with urllib.request.urlopen(req, timeout=25) as response:
            res_body = response.read().decode("utf-8")
            res_data = json.loads(res_body)
            # Extraer el texto de la respuesta de Gemini
            parts = res_data["candidates"][0]["content"]["parts"]
            texto = parts[0]["text"]
            return texto
    except urllib.error.HTTPError as e:
        error_content = e.read().decode("utf-8")
        raise RuntimeError(f"Error de la API de Gemini (HTTP {e.code}): {error_content}")
    except Exception as e:
        raise RuntimeError(f"Error al conectar con la API de Gemini: {str(e)}")


def analizar_reporte(tipo_reporte: str, datos: Union[List[dict], dict],
                      fecha_inicio: Optional[str] = None,
                      fecha_fin: Optional[str] = None) -> dict:
>>>>>>> 5e14c6e (Microservicio primera parte)
    """
    Analiza los datos de un reporte y genera un resumen inteligente.

    Parámetros:
        tipo_reporte: Tipo de reporte (general, psicologia, medicina, etc.)
<<<<<<< HEAD
        datos: Lista de registros del reporte (cada uno es un diccionario)
=======
        datos: Lista de registros del reporte u objeto con estadísticas resumidas
>>>>>>> 5e14c6e (Microservicio primera parte)
        fecha_inicio: Filtro opcional de fecha inicio
        fecha_fin: Filtro opcional de fecha fin

    Retorna:
<<<<<<< HEAD
        Diccionario con el análisis completo
    """

    # Si no hay datos, devolvemos un análisis vacío
    if not datos or len(datos) == 0:
        return {
            "exito": True,
            "tipo_reporte": tipo_reporte,
            "resumen": "No se encontraron datos para analizar en el período seleccionado.",
            "hallazgos": [],
            "estadisticas": {"total_registros": 0},
            "recomendaciones": ["Verifique los filtros de fecha seleccionados."],
            "fecha_analisis": datetime.now().isoformat()
        }

    total_registros = len(datos)
    hallazgos = []
    estadisticas = {"total_registros": total_registros}
    recomendaciones = []

    # ========================================
    # ANÁLISIS POR GÉNERO (si los datos tienen campo 'genero')
    # ========================================
    generos = [d.get("genero", "").upper() for d in datos if d.get("genero")]
    if generos:
        conteo_genero = Counter(generos)
        # Counter es una herramienta de Python que cuenta cuántas veces
        # aparece cada elemento. Ejemplo: Counter(["M","F","F","M","F"]) → {"F":3, "M":2}

        estadisticas["por_genero"] = dict(conteo_genero)

        total_con_genero = sum(conteo_genero.values())
        for genero, cantidad in conteo_genero.most_common():
            porcentaje = round((cantidad / total_con_genero) * 100, 1)
            nombre_genero = "Masculino" if genero == "M" else "Femenino" if genero == "F" else genero
            hallazgos.append(
                f"El {porcentaje}% de los registros corresponde al género {nombre_genero} "
                f"({cantidad} de {total_con_genero})."
            )

    # ========================================
    # ANÁLISIS POR PNF (si existe el campo 'nombre_pnf')
    # ========================================
    pnfs = [d.get("nombre_pnf", "") for d in datos if d.get("nombre_pnf")]
    if pnfs:
        conteo_pnf = Counter(pnfs)
        estadisticas["por_pnf"] = dict(conteo_pnf)

        # Top 3 PNF más frecuentes
        top_pnfs = conteo_pnf.most_common(3)
        if top_pnfs:
            top_nombres = [f"{nombre} ({cant})" for nombre, cant in top_pnfs]
            hallazgos.append(
                f"Los PNF con más registros son: {', '.join(top_nombres)}."
            )

        # PNF con menos atenciones (posible punto de atención)
        bottom_pnfs = conteo_pnf.most_common()[-3:]
        if bottom_pnfs and len(conteo_pnf) > 3:
            bottom_nombres = [f"{nombre} ({cant})" for nombre, cant in bottom_pnfs]
            recomendaciones.append(
                f"Los PNF con menos registros ({', '.join(bottom_nombres)}) "
                f"podrían necesitar mayor difusión o atención."
            )

    # ========================================
    # ANÁLISIS POR SERVICIO (si existe 'nombre_serv')
    # ========================================
    servicios = [d.get("nombre_serv", "") for d in datos if d.get("nombre_serv")]
    if servicios:
        conteo_servicio = Counter(servicios)
        estadisticas["por_servicio"] = dict(conteo_servicio)

        top_servicio = conteo_servicio.most_common(1)
        if top_servicio:
            hallazgos.append(
                f"El servicio más utilizado es '{top_servicio[0][0]}' "
                f"con {top_servicio[0][1]} atenciones."
            )

    # ========================================
    # ANÁLISIS TEMPORAL (si existe 'fecha_creacion')
    # ========================================
    fechas = []
    for d in datos:
        fecha_str = d.get("fecha_creacion") or d.get("fecha_referencia") or d.get("fecha")
        if fecha_str:
            try:
                # Intentar parsear la fecha (diferentes formatos posibles)
                if isinstance(fecha_str, str):
                    if "T" in fecha_str:
                        fecha = datetime.fromisoformat(fecha_str)
                    elif " " in fecha_str:
                        fecha = datetime.strptime(fecha_str, "%Y-%m-%d %H:%M:%S")
                    else:
                        fecha = datetime.strptime(fecha_str, "%Y-%m-%d")
                    fechas.append(fecha)
            except (ValueError, TypeError):
                pass  # Ignorar fechas que no se pueden parsear

    if fechas:
        # Agrupar por mes
        meses = Counter([f.strftime("%Y-%m") for f in fechas])
        estadisticas["por_mes"] = dict(sorted(meses.items()))

        # Encontrar el mes con más actividad
        mes_pico = meses.most_common(1)
        if mes_pico:
            hallazgos.append(
                f"El mes con mayor actividad fue {mes_pico[0][0]} "
                f"con {mes_pico[0][1]} registros."
            )

        # Tendencia: ¿está subiendo o bajando?
        meses_ordenados = sorted(meses.items())
        if len(meses_ordenados) >= 2:
            ultimo_mes = meses_ordenados[-1][1]
            penultimo_mes = meses_ordenados[-2][1]
            if ultimo_mes > penultimo_mes:
                diferencia = ultimo_mes - penultimo_mes
                hallazgos.append(
                    f"Se observa una tendencia CRECIENTE: el último mes registra "
                    f"{diferencia} atenciones más que el mes anterior."
                )
            elif ultimo_mes < penultimo_mes:
                diferencia = penultimo_mes - ultimo_mes
                hallazgos.append(
                    f"Se observa una tendencia DECRECIENTE: el último mes registra "
                    f"{diferencia} atenciones menos que el mes anterior."
                )
                recomendaciones.append(
                    "La tendencia decreciente podría indicar la necesidad de "
                    "revisar la captación de beneficiarios o la difusión de los servicios."
                )

    # ========================================
    # GENERAR RESUMEN
    # ========================================
    resumen_partes = [
        f"Se analizaron {total_registros} registros del reporte de '{tipo_reporte}'."
    ]

    if fecha_inicio and fecha_fin:
        resumen_partes.append(
            f"Período analizado: desde {fecha_inicio} hasta {fecha_fin}."
        )

    if hallazgos:
        resumen_partes.append(
            f"Se identificaron {len(hallazgos)} hallazgos relevantes."
        )

    resumen = " ".join(resumen_partes)
=======
        Diccionario con el análisis completo (resumen, hallazgos, estadísticas, recomendaciones)
    """

    # 1. Definición inicial de variables para fallback local
    total_registros = 0
    hallazgos = []
    recomendaciones = []
    estadisticas = {}

    # 2. Procesar datos según su estructura (lista de registros o resumen estadístico)
    if isinstance(datos, dict):
        # Datos ya resumidos por el backend PHP
        total_registros = datos.get("total_registros", 0)
        estadisticas = datos
        
        # Generar hallazgos offline básicos para fallback
        dist_genero = datos.get("distribucion_genero", {})
        if dist_genero:
            for gen, cant in dist_genero.items():
                porc = round((cant / total_registros) * 100, 1) if total_registros > 0 else 0
                hallazgos.append(f"El {porc}% de los registros corresponde al género {gen} ({cant} de {total_registros}).")
                
        dist_pnf = datos.get("distribucion_pnf", {})
        if dist_pnf:
            top_pnfs = sorted(dist_pnf.items(), key=lambda x: x[1], reverse=True)[:3]
            top_nombres = [f"{n} ({c})" for n, c in top_pnfs]
            if top_nombres:
                hallazgos.append(f"Los PNF con más registros son: {', '.join(top_nombres)}.")
                
        dist_serv = datos.get("distribucion_servicios", {})
        if dist_serv:
            top_serv = sorted(dist_serv.items(), key=lambda x: x[1], reverse=True)[:1]
            if top_serv:
                hallazgos.append(f"El servicio más utilizado es '{top_serv[0][0]}' con {top_serv[0][1]} atenciones.")
                
        resumen = f"Se analizaron {total_registros} registros del reporte de '{tipo_reporte}'."
        if fecha_inicio and fecha_fin:
            resumen += f" Período analizado: desde {fecha_inicio} hasta {fecha_fin}."
        
        recomendaciones.append("Revisar la distribución de solicitudes para equilibrar la carga de atención.")
    
    else:
        # Lista de registros crudos
        if not datos or len(datos) == 0:
            return {
                "exito": True,
                "tipo_reporte": tipo_reporte,
                "resumen": "No se encontraron datos para analizar en el período seleccionado.",
                "hallazgos": [],
                "estadisticas": {"total_registros": 0},
                "recomendaciones": ["Verifique los filtros de fecha seleccionados."],
                "fecha_analisis": datetime.now().isoformat()
            }
            
        total_registros = len(datos)
        estadisticas = {"total_registros": total_registros}
        
        # ANÁLISIS POR GÉNERO
        generos = [d.get("genero", "").upper() for d in datos if d.get("genero")]
        if generos:
            conteo_genero = Counter(generos)
            estadisticas["por_genero"] = dict(conteo_genero)
            total_con_genero = sum(conteo_genero.values())
            for genero, cantidad in conteo_genero.most_common():
                porcentaje = round((cantidad / total_con_genero) * 100, 1)
                nombre_genero = "Masculino" if genero == "M" else "Femenino" if genero == "F" else genero
                hallazgos.append(
                    f"El {porcentaje}% de los registros corresponde al género {nombre_genero} "
                    f"({cantidad} de {total_con_genero})."
                )

        # ANÁLISIS POR PNF
        pnfs = [d.get("nombre_pnf", "") for d in datos if d.get("nombre_pnf")]
        if pnfs:
            conteo_pnf = Counter(pnfs)
            estadisticas["por_pnf"] = dict(conteo_pnf)
            top_pnfs = conteo_pnf.most_common(3)
            if top_pnfs:
                top_nombres = [f"{nombre} ({cant})" for nombre, cant in top_pnfs]
                hallazgos.append(
                    f"Los PNF con más registros son: {', '.join(top_nombres)}."
                )
            bottom_pnfs = conteo_pnf.most_common()[-3:]
            if bottom_pnfs and len(conteo_pnf) > 3:
                bottom_nombres = [f"{nombre} ({cant})" for nombre, cant in bottom_pnfs]
                recomendaciones.append(
                    f"Los PNF con menos registros ({', '.join(bottom_nombres)}) "
                    f"podrían necesitar mayor difusión o atención."
                )

        # ANÁLISIS POR SERVICIO
        servicios = [d.get("nombre_serv", "") for d in datos if d.get("nombre_serv")]
        if servicios:
            conteo_servicio = Counter(servicios)
            estadisticas["por_servicio"] = dict(conteo_servicio)
            top_servicio = conteo_servicio.most_common(1)
            if top_servicio:
                hallazgos.append(
                    f"El servicio más utilizado es '{top_servicio[0][0]}' con {top_servicio[0][1]} atenciones."
                )

        # ANÁLISIS TEMPORAL
        fechas = []
        for d in datos:
            fecha_str = d.get("fecha_creacion") or d.get("fecha_referencia") or d.get("fecha")
            if fecha_str:
                try:
                    if isinstance(fecha_str, str):
                        if "T" in fecha_str:
                            fecha = datetime.fromisoformat(fecha_str)
                        elif " " in fecha_str:
                            fecha = datetime.strptime(fecha_str, "%Y-%m-%d %H:%M:%S")
                        else:
                            fecha = datetime.strptime(fecha_str, "%Y-%m-%d")
                        fechas.append(fecha)
                except (ValueError, TypeError):
                    pass

        if fechas:
            meses = Counter([f.strftime("%Y-%m") for f in fechas])
            estadisticas["por_mes"] = dict(sorted(meses.items()))
            mes_pico = meses.most_common(1)
            if mes_pico:
                hallazgos.append(
                    f"El mes con mayor actividad fue {mes_pico[0][0]} con {mes_pico[0][1]} registros."
                )
            meses_ordenados = sorted(meses.items())
            if len(meses_ordenados) >= 2:
                ultimo_mes = meses_ordenados[-1][1]
                penultimo_mes = meses_ordenados[-2][1]
                if ultimo_mes > penultimo_mes:
                    diferencia = ultimo_mes - penultimo_mes
                    hallazgos.append(
                        f"Se observa una tendencia CRECIENTE: el último mes registra {diferencia} atenciones más que el mes anterior."
                    )
                elif ultimo_mes < penultimo_mes:
                    diferencia = penultimo_mes - ultimo_mes
                    hallazgos.append(
                        f"Se observa una tendencia DECRECIENTE: el último mes registra {diferencia} atenciones menos que el mes anterior."
                    )
                    recomendaciones.append(
                        "La tendencia decreciente podría indicar la necesidad de revisar la captación de beneficiarios o la difusión de los servicios."
                    )

        resumen_partes = [f"Se analizaron {total_registros} registros del reporte de '{tipo_reporte}'."]
        if fecha_inicio and fecha_fin:
            resumen_partes.append(f"Período analizado: desde {fecha_inicio} hasta {fecha_fin}.")
        if hallazgos:
            resumen_partes.append(f"Se identificaron {len(hallazgos)} hallazgos relevantes.")
        resumen = " ".join(resumen_partes)

    # 3. Invocar a Gemini para análisis narrativo avanzado si hay API KEY
    if GEMINI_API_KEY:
        try:
            datos_str = json.dumps(datos, indent=2, ensure_ascii=False)
            prompt = f"""
            Analiza el siguiente reporte de tipo '{tipo_reporte}'.
            
            Filtros aplicados en la consulta:
            - Fecha de inicio: {fecha_inicio or 'No especificada'}
            - Fecha de fin: {fecha_fin or 'No especificada'}
            
            Datos del reporte (estadísticas o registros):
            {datos_str}
            
            Genera un resumen analítico narrativo, hallazgos clave y recomendaciones accionables basadas en los datos.
            Retorna ÚNICAMENTE el JSON estructurado según las instrucciones del sistema.
            """
            
            system_instruction = (
                "Eres un analista de datos experto del departamento de bienestar estudiantil y servicios médicos/sociales del instituto DIRPOLES.\n"
                "Tu tarea es analizar los datos estadísticos o registros del reporte de servicios/becas/atención médica proporcionados y generar un informe narrativo estructurado en formato JSON con la siguiente estructura exacta:\n"
                "{\n"
                "  \"resumen\": \"Un resumen analítico de alto nivel detallado en lenguaje natural y profesional sobre la actividad reportada, destacando lo más importante, tendencias e implicaciones para el bienestar estudiantil.\",\n"
                "  \"hallazgos\": [\"Hallazgo relevante 1 con porcentajes o números clave extraídos de los datos\", \"Hallazgo relevante 2...\"],\n"
                "  \"recomendaciones\": [\"Recomendación accionable 1 para mejorar la atención, asignar recursos o difundir servicios basada en la evidencia de los datos\", \"Recomendación 2...\"]\n"
                "}\n"
                "Asegúrate de que la respuesta sea estrictamente un objeto JSON válido con estas tres claves, sin bloques de código markdown ni texto adicional."
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
            
            resumen = ia_data.get("resumen", resumen)
            if "hallazgos" in ia_data and isinstance(ia_data["hallazgos"], list):
                hallazgos = ia_data["hallazgos"]
            if "recomendaciones" in ia_data and isinstance(ia_data["recomendaciones"], list):
                recomendaciones = ia_data["recomendaciones"]
                
        except Exception as e:
            # Fallback silencioso en producción, pero útil imprimir en desarrollo
            print(f"Error al generar reporte con Gemini (se usará fallback offline): {str(e)}")
>>>>>>> 5e14c6e (Microservicio primera parte)

    return {
        "exito": True,
        "tipo_reporte": tipo_reporte,
        "resumen": resumen,
        "hallazgos": hallazgos,
        "estadisticas": estadisticas,
        "recomendaciones": recomendaciones,
        "fecha_analisis": datetime.now().isoformat()
    }


<<<<<<< HEAD
def responder_pregunta(pregunta: str, tipo_reporte: str, datos: List[dict]) -> dict:
    """
    Responde una pregunta del usuario sobre los datos del reporte.

    En esta versión básica, analiza patrones en la pregunta y busca
    la respuesta en los datos. En el futuro, se puede conectar 
    con OpenAI/ChatGPT para respuestas más inteligentes.

    Parámetros:
        pregunta: Texto de la pregunta del usuario
        tipo_reporte: Tipo de reporte sobre el que se pregunta
        datos: Los datos del reporte para buscar la respuesta
    """

    pregunta_lower = pregunta.lower()
    total = len(datos)
=======
def responder_pregunta(pregunta: str, tipo_reporte: str, datos: Union[List[dict], dict]) -> dict:
    """
    Responde una pregunta del usuario sobre los datos del reporte.

    Parámetros:
        pregunta: Texto de la pregunta del usuario
        tipo_reporte: Tipo de reporte sobre el que se pregunta
        datos: Los datos del reporte para buscar la respuesta (crudos o resumidos)
    """

    if GEMINI_API_KEY:
        try:
            datos_str = json.dumps(datos, indent=2, ensure_ascii=False)
            prompt = f"""
            Tengo una pregunta sobre el reporte de tipo '{tipo_reporte}'.
            
            Pregunta del usuario: "{pregunta}"
            
            Datos del reporte:
            {datos_str}
            
            Responde la pregunta basándote estrictamente en los datos proporcionados.
            Genera una respuesta clara, concisa y profesional.
            También extrae o calcula si aplica algunos datos numéricos clave que soporten la respuesta y retórnalos en el campo 'datos_soporte'.
            
            Recuerda retornar ÚNICAMENTE el JSON estructurado según las instrucciones del sistema.
            """
            
            system_instruction = (
                "Eres un analista de datos experto del instituto DIRPOLES.\n"
                "Tu tarea es responder preguntas de los usuarios sobre los datos del reporte proporcionado.\n"
                "Debes retornar un JSON estructurado con el siguiente formato exacto:\n"
                "{\n"
                "  \"respuesta\": \"Respuesta detallada y clara en lenguaje natural basada únicamente en los datos.\",\n"
                "  \"datos_soporte\": {\"clave1\": valor1, \"clave2\": valor2} \n"
                "}\n"
                "Asegúrate de que la respuesta sea estrictamente un objeto JSON válido, sin bloques de código markdown ni texto adicional."
            )
            
            respuesta_texto = llamar_gemini(prompt, system_instruction)
            if respuesta_texto.strip().startswith("```"):
                lines = respuesta_texto.strip().split("\n")
                if lines[0].startswith("```"):
                    lines = lines[1:]
                if lines[-1].startswith("```"):
                    lines = lines[:-1]
                respuesta_texto = "\n".join(lines).strip()
                
            ia_data = json.loads(respuesta_texto)
            return {
                "exito": True,
                "pregunta": pregunta,
                "respuesta": ia_data.get("respuesta", "No se pudo generar una respuesta."),
                "datos_soporte": ia_data.get("datos_soporte")
            }
        except Exception as e:
            print(f"Error al responder pregunta con Gemini (se usará fallback offline): {str(e)}")

    # Fallback offline local
    pregunta_lower = pregunta.lower()
    
    if isinstance(datos, dict):
        total = datos.get("total_registros", 0)
        generos = datos.get("distribucion_genero", {})
        pnfs = datos.get("distribucion_pnf", {})
    else:
        total = len(datos)
        generos = Counter([d.get("genero", "").upper() for d in datos if d.get("genero")])
        pnfs = Counter([d.get("nombre_pnf", "") for d in datos if d.get("nombre_pnf")])
>>>>>>> 5e14c6e (Microservicio primera parte)

    # === Preguntas sobre cantidad/total ===
    if any(palabra in pregunta_lower for palabra in ["cuántos", "cuantos", "total", "cantidad"]):
        return {
            "exito": True,
            "pregunta": pregunta,
            "respuesta": f"El reporte de '{tipo_reporte}' contiene un total de {total} registros.",
            "datos_soporte": {"total": total}
        }

    # === Preguntas sobre género ===
    if any(palabra in pregunta_lower for palabra in ["género", "genero", "masculino", "femenino", "hombre", "mujer"]):
<<<<<<< HEAD
        generos = Counter([d.get("genero", "").upper() for d in datos if d.get("genero")])
        if generos:
            respuesta_partes = []
            for g, c in generos.most_common():
                nombre = "Masculino" if g == "M" else "Femenino" if g == "F" else g
                porcentaje = round((c / total) * 100, 1)
=======
        if generos:
            respuesta_partes = []
            for g, c in (generos.items() if isinstance(generos, dict) else generos.most_common()):
                nombre = "Masculino" if g in ["M", "Masculino"] else "Femenino" if g in ["F", "Femenino"] else g
                porcentaje = round((c / total) * 100, 1) if total > 0 else 0
>>>>>>> 5e14c6e (Microservicio primera parte)
                respuesta_partes.append(f"{nombre}: {c} ({porcentaje}%)")

            return {
                "exito": True,
                "pregunta": pregunta,
                "respuesta": f"Distribución por género en '{tipo_reporte}': " + ", ".join(respuesta_partes) + ".",
                "datos_soporte": dict(generos)
            }

    # === Preguntas sobre PNF ===
    if any(palabra in pregunta_lower for palabra in ["pnf", "carrera", "programa"]):
<<<<<<< HEAD
        pnfs = Counter([d.get("nombre_pnf", "") for d in datos if d.get("nombre_pnf")])
        if pnfs:
            top = pnfs.most_common(5)
            respuesta_partes = [f"{nombre}: {cant} registros" for nombre, cant in top]
=======
        if pnfs:
            items = sorted(pnfs.items(), key=lambda x: x[1], reverse=True)[:5] if isinstance(pnfs, dict) else pnfs.most_common(5)
            respuesta_partes = [f"{nombre}: {cant} registros" for nombre, cant in items]
>>>>>>> 5e14c6e (Microservicio primera parte)
            return {
                "exito": True,
                "pregunta": pregunta,
                "respuesta": f"Los PNF más frecuentes en '{tipo_reporte}' son: " + "; ".join(respuesta_partes) + ".",
<<<<<<< HEAD
                "datos_soporte": {"top_pnf": dict(top)}
=======
                "datos_soporte": {"top_pnf": dict(items)}
>>>>>>> 5e14c6e (Microservicio primera parte)
            }

    # === Pregunta genérica (no reconocida) ===
    return {
        "exito": True,
        "pregunta": pregunta,
        "respuesta": (
            f"Análisis sobre '{tipo_reporte}': Se encontraron {total} registros en total. "
            f"Puedo responder preguntas sobre cantidades, distribución por género, "
            f"distribución por PNF/carrera, y tendencias temporales. "
            f"Intenta ser más específico en tu pregunta."
        ),
        "datos_soporte": {"total_registros": total}
    }
