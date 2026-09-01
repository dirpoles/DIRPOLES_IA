# AGENT.md — Contexto del Proyecto DIRPOLES_IA

> Este archivo es la fuente de verdad para cualquier agente de código que trabaje en este repositorio.
> Léelo completo antes de hacer cambios.

---

## ¿Qué es este proyecto?

**DIRPOLES_IA** es un microservicio en **Python + FastAPI** que provee análisis con inteligencia artificial (Google AI Studio / Gemini) para los reportes estadísticos del sistema **DIRPOLES_4** (monolito PHP).

**Arquitectura:**
```
DIRPOLES_4 (PHP/Apache :80) ──HTTP/JSON──► DIRPOLES_IA (Python/Uvicorn :8000)
         │                                            │
         └────────────► MySQL (dirpoles_business) ◄───┘
```

- El monolito PHP **solo envía filtros** (fechas, género, PNF, área).
- Python **consulta la BD directamente**, procesa datos, y los envía a Gemini para generar el informe narrativo.
- Autenticación mutua via `X-API-Key` en header HTTP.

---

## Stack tecnológico

| Componente | Tecnología | Versión |
|---|---|---|
| Framework web | FastAPI | 0.115.3 |
| Servidor ASGI | Uvicorn | 0.44.0 |
| ORM/BD | SQLAlchemy | 2.0.49 |
| Driver MySQL | PyMySQL | 1.1.2 |
| Validación | Pydantic | 2.13.0 |
| IA | Google AI Studio (Gemini 2.0 Flash) | API REST |
| Autenticación | API Key (X-API-Key header) | hmac.compare_digest |

---

## Estructura del proyecto

```
DIRPOLES_IA/
├── .env.example              # Template de variables de entorno
├── .gitignore
├── requirements.txt          # Dependencias Python
├── AGENT.md                  # ← Este archivo (contexto para agentes)
├── README.md                 # Portada del repositorio
└── app/
    ├── __init__.py
    ├── main.py               # Entry point: FastAPI app, CORS, rutas, health checks
    ├── config.py             # Lee .env, expone constantes (DB_HOST, GEMINI_API_KEY, etc.)
    ├── database.py           # Conexiones SQLAlchemy a dirpoles_business y dirpoles_security
    ├── security.py           # Verificación de API Key (verificar_api_key dependency)
    ├── repositories/
    │   ├── __init__.py
    │   └── reporte_general.py  # ✅ ÚNICO repositorio implementado
    ├── routes/
    │   ├── __init__.py
    │   └── reportes.py         # Rutas: POST /analizar, GET /tipos-reportes
    ├── schemas/
    │   ├── __init__.py
    │   └── reportes.py         # SolicitudReporteInput, AnalisisOutput, ErrorOutput
    └── services/
        ├── __init__.py
        └── analisis.py         # Core: procesar_datos_crudos, analizar_reporte, llamar_gemini
```

---

## Estado actual — Lo que está HECHO ✅

1. **Arquitectura completa**: FastAPI, CORS, config, database, security — todo funcional.
2. **Endpoint `POST /api/v1/analizar`**: Recibe filtros, consulta BD, envía a Gemini, devuelve análisis JSON.
3. **Endpoint `GET /api/v1/tipos-reportes`**: Lista los tipos de reporte disponibles.
4. **Health checks**: `GET /`, `GET /health`, `GET /api/health`, `GET /api/v1/health`.
5. **Repositorio `general`**: Consulta UNION ALL de 7 tablas (becas, exoneración, FAMES, consulta médica, orientación, discapacidad, consulta psicológica).
6. **Integración Gemini**: Llamada directa a la API REST con `urllib.request`, sin SDK externo. Formato JSON forzado.
7. **Fallback offline**: Si Gemini falla o no hay API key, genera resumen/hallazgos básicos con lógica interna.
8. **Schemas Pydantic**: Contratos de entrada/salida bien definidos.
9. **Seguridad**: API Key con comparación en tiempo constante (hmac).

---

## Estado actual — Lo que FALTA ⚠️

### CRÍTICO (funcionalidad principal)

1. **9 repositorios faltantes** — Solo existe `reporte_general.py`. Faltan:
   - `repositories/reporte_psicologia.py` → tabla `consulta_psicologica`
   - `repositories/reporte_medicina.py` → tabla `consulta_medica`
   - `repositories/reporte_orientacion.py` → tabla `orientacion`
   - `repositories/reporte_becas.py` → tabla `becas`
   - `repositories/reporte_discapacidad.py` → tabla `discapacidad`
   - `repositories/reporte_transporte.py` → (consultar estructura de tablas)
   - `repositories/reporte_mobiliario.py` → (consultar estructura de tablas)
   - `repositories/reporte_jornadas.py` → (consultar estructura de tablas)
   - `repositories/reporte_referencias.py` → (consultar estructura de tablas)

2. **Endpoint `POST /api/v1/preguntar`** — Mencionado en el README pero NO implementado. Debería recibir preguntas en lenguaje natural y responder con datos de la BD + Gemini.

3. **Actualizar `services/analisis.py`** — La función `_obtener_datos()` solo despacha `"general"`. Cada nuevo repo debe agregarse ahí con su `elif`.

4. **Actualizar `routes/reportes.py`** — Marcar todos los tipos como `"disponible": True` en el endpoint `/tipos-reportes`.

### MEJORAS (no crítico)

5. **Tests unitarios** — No existe ninguno. Necesarios para:
   - Validar que los repos devuelven datos con la estructura correcta.
   - Mockear Gemini y probar el fallback.
   - Verificar autenticación API Key.

6. **Logging** — Actualmente usa `print()`. Debería usar `logging` de Python para niveles (INFO, WARNING, ERROR).

7. **Rate limiting** — No hay protección contra abuso de la API de Gemini.

8. **BD de seguridad** (`dirpoles_security`) — Está configurada en `config.py` y `database.py` pero **nunca se usa**. Está pendiente para futuras funcionalidades (autenticación de usuarios, roles, etc.).

9. **Límites de tokens** — El prompt a Gemini puede crecer mucho si hay miles de registros. Considerar paginación o resumen previo.

---

## Base de datos — Tablas conocidas (dirpoles_business)

Estas son las tablas que ya se usan en la consulta UNION ALL del reporte general:

| Tabla | Servicio | Columnas clave |
|---|---|---|
| `beneficiario` | — (tabla base) | `id_beneficiario`, `nombres`, `apellidos`, `cedula`, `genero`, `id_pnf` |
| `pnf` | — (catálogo) | `id_pnf`, `nombre_pnf` |
| `solicitud_de_servicio` | — (tabla puente) | `id_solicitud_serv`, `id_beneficiario`, `id_servicios` |
| `servicio` | — (catálogo) | `id_servicios`, `nombre_serv` |
| `becas` | Becas | `id_solicitud_serv`, `fecha_creacion` |
| `exoneracion` | Exoneración | `id_solicitud_serv`, `fecha_creacion` |
| `fames` | FAMES | `id_solicitud_serv`, `fecha_creacion` |
| `consulta_medica` | Medicina | `id_solicitud_serv`, `fecha_creacion` |
| `orientacion` | Orientación | `id_solicitud_serv`, `fecha_creacion` |
| `discapacidad` | Discapacidad | `id_solicitud_serv`, `fecha_creacion` |
| `consulta_psicologica` | Psicología | `id_solicitud_serv`, `fecha_creacion` |

> **IMPORTANTE**: Las tablas de transporte, mobiliario, jornadas y referencias **no están en la consulta UNION ALL actual**. Es posible que tengan una estructura diferente. Consultar el esquema de BD antes de implementar esos repos.

---

## Patrón para crear un nuevo repositorio

Cada repositorio sigue el mismo patrón que `reporte_general.py`:

```python
# app/repositories/reporte_X.py
from datetime import datetime
from app.database import ejecutar_consulta

def obtener_datos_reporte_X(
    fecha_inicio: str = None,
    fecha_fin: str = None,
    genero: str = None,
    pnf: str = None,
    area: str = None
) -> list:
    """
    Consulta la tabla X y aplica filtros opcionales.
    Retorna lista de diccionarios con las columnas:
    nombres, apellidos, cedula, genero, nombre_pnf, nombre_serv, fecha_creacion
    """
    query = """SELECT ... FROM ... WHERE ..."""
    filas = ejecutar_consulta(query, base="business")
    # Aplicar filtros en Python (mismo patrón que reporte_general)
    filtradas = []
    for fila in filas:
        # Filtros por fecha, género, PNF, área
        ...
        filtradas.append(fila)
    return filtradas
```

Luego registrar en `services/analisis.py` → `_obtener_datos()`:
```python
elif tipo_reporte == "X":
    from app.repositories.reporte_X import obtener_datos_reporte_X
    return obtener_datos_reporte_X(...)
```

---

## Variables de entorno requeridas

| Variable | Descripción |
|---|---|
| `DB_HOST` | Host MySQL (default: localhost) |
| `DB_PORT` | Puerto MySQL (default: 3306) |
| `DB_NAME` | BD principal: `dirpoles_business` |
| `DB_USER` | Usuario MySQL |
| `DB_PASS` | Contraseña MySQL |
| `IA_API_KEY` | Clave API para autenticación con el monolito PHP |
| `GEMINI_API_KEY` | API Key de Google AI Studio |
| `SERVER_HOST` | IP de escucha (default: 0.0.0.0) |
| `SERVER_PORT` | Puerto del servidor (default: 8000) |
| `ALLOWED_ORIGINS` | Orígenes CORS, separados por coma |

---

## Cómo ejecutar

```bash
# 1. Crear entorno virtual
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar variables de entorno
cp .env.example .env
# Editar .env con tus valores reales

# 4. Ejecutar
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Documentación interactiva: `http://localhost:8000/docs`

---

## Notas para el agente

- **NO usar `npm` ni `npx`** — Este es un proyecto Python puro.
- **NO instalar dependencias globalmente** — Siempre usar el venv.
- **Verificar la BD antes de crear queries** — Usar `SHOW TABLES` y `DESCRIBE tabla` para confirmar estructura.
- **No subir `.env`** — Solo `.env.example` va al repo.
- **Formato del requirements.txt** — Debe ser UTF-8 plano (sin BOM, sin UTF-16).
- **El remote ya está configurado**: `origin → https://github.com/dirpoles/DIRPOLES_IA.git`
- **Rama principal**: `main`
