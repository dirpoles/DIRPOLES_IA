<div align="center">

# 🤖 DIRPOLES_IA

### Microservicio de Análisis Inteligente

**Motor de IA que genera informes estadísticos automatizados para el ecosistema DIRPOLES_4**

![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=flat&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=flat&logo=fastapi&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?style=flat&logo=mysql&logoColor=white)
![Gemini](https://img.shields.io/badge/Gemini-2.0-4285F4?style=flat&logo=google&logoColor=white)
![License](https://img.shields.io/badge/License-Proprietary-red)

<br>

```
DIRPOLES_4 (PHP) ──HTTP/JSON──► DIRPOLES_IA (Python) ──► MySQL + Gemini AI
```

</div>

---

## 🧠 ¿Qué es?

DIRPOLES_IA es un microservicio independiente que funciona como **motor de análisis** para la plataforma DIRPOLES_4. Desde el monolito PHP solo se envían filtros de búsqueda; el microservicio se encarga de:

1. 📊 **Consultar la base de datos** directamente (UNION ALL de 7+ tablas de servicios)
2. 📈 **Calcular estadísticas** (distribución por género, PNF, servicio, tendencias temporales)
3. 🤖 **Enviar los datos a Gemini** (Google AI Studio) para generar un informe narrativo profesional
4. 📋 **Devolver un JSON estructurado** con resumen, hallazgos y recomendaciones

---

## 🏗️ Arquitectura

```
┌──────────────────────────┐        HTTP/JSON         ┌──────────────────────────┐
│     DIRPOLES_4 (PHP)     │ ◄──────────────────────► │    DIRPOLES_IA (Python)  │
│   Apache · Puerto 80     │       X-API-Key Auth      │   Uvicorn · Puerto 8000  │
│   Frontend + Backend     │                           │   Motor de Análisis IA   │
└──────────┬───────────────┘                           └────────────┬─────────────┘
           │                                                         │
           │                    ┌──────────────────┐                 │
           └───────────────────►│  MySQL (compartida)◄───────────────┘
                                │ dirpoles_business  │
                                └────────────────────┘
```

---

## 📡 API Endpoints

| Método | Ruta | Descripción | Auth |
|--------|------|-------------|:----:|
| `GET` | `/` | Health check básico | ❌ |
| `GET` | `/health` | Health check detallado (incluye estado de BD) | ❌ |
| `GET` | `/api/v1/tipos-reportes` | Lista de tipos de reporte disponibles | ❌ |
| `POST` | `/api/v1/analizar` | Genera un análisis IA completo | ✅ |

> 📖 **Documentación interactiva** disponible en `/docs` (Swagger) y `/redoc` (ReDoc)

### Ejemplo de solicitud

```bash
curl -X POST http://localhost:8000/api/v1/analizar \
  -H "Content-Type: application/json" \
  -H "X-API-Key: tu-clave-secreta" \
  -d '{
    "tipo_reporte": "general",
    "fecha_inicio": "2026-01-01",
    "fecha_fin": "2026-06-01",
    "genero": null,
    "pnf": null,
    "area": null
  }'
```

### Respuesta

```json
{
  "exito": true,
  "tipo_reporte": "general",
  "total_registros": 150,
  "resumen": "Se analizaron 150 registros del período enero-junio 2026...",
  "hallazgos": [
    "El 60% de los beneficiarios son mujeres",
    "El PNF más frecuente es Ingeniería Informática (32 registros)",
    "El servicio de Psicología concentró el mayor volumen de atenciones"
  ],
  "estadisticas": {
    "total_registros": 150,
    "distribucion_genero": {"Femenino": 90, "Masculino": 60},
    "distribucion_pnf": {"Ing. Informática": 32, "Ing. Electricidad": 28},
    "distribucion_servicios": {"Psicología": 45, "Medicina": 38},
    "distribucion_mensual": {"2026-01": 20, "2026-02": 25}
  },
  "recomendaciones": [
    "Mantener la cobertura de Psicología que lidera la demanda",
    "Evaluar la carga de trabajo en servicios con menor atención"
  ],
  "fecha_analisis": "2026-06-08T18:30:00"
}
```

---

## 📋 Tipos de Reporte

| Tipo | Estado | Descripción |
|------|:------:|-------------|
| `general` | ✅ | Análisis cruzado de todos los servicios (Becas, Medicina, Psicología, Orientación, Discapacidad, FAMES, Exoneración) |
| `psicologia` | 🔨 | Morbilidad y citas psicológicas |
| `medicina` | 🔨 | Consultas médicas e inventario |
| `orientacion` | 🔨 | Casos de asesoría |
| `becas` | 🔨 | Solicitudes y asignaciones de becas |
| `discapacidad` | 🔨 | Atenciones por discapacidad |
| `transporte` | 🔨 | Vehículos, rutas y proveedores |
| `mobiliario` | 🔨 | Inventario de equipos y mobiliario |
| `jornadas` | 🔨 | Jornadas médicas especiales |
| `referencias` | 🔨 | Derivaciones entre servicios |

> ✅ = Implementado · 🔨 = En desarrollo

---

## ⚙️ Configuración

### Variables de entorno

Copia `.env.example` como `.env` y completa los valores:

```bash
cp .env.example .env
```

| Variable | Default | Descripción |
|----------|---------|-------------|
| `DB_HOST` | `localhost` | Host de MySQL |
| `DB_PORT` | `3306` | Puerto de MySQL |
| `DB_NAME` | `dirpoles_business` | Base de datos principal |
| `DB_USER` | `root` | Usuario MySQL |
| `DB_PASS` | *(vacío)* | Contraseña MySQL |
| `IA_API_KEY` | *(vacío)* | Clave API para autenticación con DIRPOLES_4 |
| `GEMINI_API_KEY` | *(vacío)* | API Key de Google AI Studio |
| `SERVER_HOST` | `0.0.0.0` | IP de escucha |
| `SERVER_PORT` | `8000` | Puerto del servidor |
| `ALLOWED_ORIGINS` | `http://localhost` | Orígenes CORS (separados por coma) |

---

## 🚀 Instalación y Ejecución

```bash
# 1. Clonar
git clone https://github.com/dirpoles/DIRPOLES_IA.git
cd DIRPOLES_IA

# 2. Entorno virtual
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 3. Dependencias
pip install -r requirements.txt

# 4. Configurar entorno
cp .env.example .env
# Editar .env con tus credenciales reales

# 5. Ejecutar
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

El servicio estará disponible en `http://localhost:8000`

---

## 🔌 Integración con DIRPOLES_4 (PHP)

```php
<?php
$ch = curl_init('http://localhost:8000/api/v1/analizar');
curl_setopt_array($ch, [
    CURLOPT_POST => true,
    CURLOPT_HTTPHEADER => [
        'Content-Type: application/json',
        'X-API-Key: tu-clave-secreta'
    ],
    CURLOPT_POSTFIELDS => json_encode([
        'tipo_reporte' => 'general',
        'fecha_inicio' => '2026-01-01',
        'fecha_fin' => '2026-06-30',
    ]),
    CURLOPT_RETURNTRANSFER => true,
]);

$respuesta = json_decode(curl_exec($ch), true);
curl_close($ch);

// $respuesta['resumen']   → Texto narrativo del informe
// $respuesta['hallazgos'] → Array de hallazgos clave
// $respuesta['estadisticas'] → Datos numéricos procesados
```

---

## 🛠️ Tecnologías

| Componente | Tecnología | Propósito |
|---|---|---|
| Framework | [FastAPI](https://fastapi.tiangolo.com/) | API web ASGI de alto rendimiento |
| Servidor | [Uvicorn](https://www.uvicorn.org/) | Servidor ASGI asíncrono |
| ORM | [SQLAlchemy](https://www.sqlalchemy.org/) | Conexión y consultas a MySQL |
| Driver | [PyMySQL](https://pypi.org/project/PyMySQL/) | Conector MySQL puro en Python |
| Validación | [Pydantic](https://docs.pydantic.dev/) | Modelos de datos y validación |
| IA | [Google AI Studio](https://aistudio.google.com/) | Gemini 2.0 Flash para análisis narrativo |
| Config | [python-dotenv](https://github.com/theskumar/python-dotenv) | Variables de entorno desde `.env` |

---

## 📁 Estructura

```
DIRPOLES_IA/
├── .env.example              # Template de variables de entorno
├── .gitignore
├── AGENT.md                  # Contexto para agentes de código (Freebuff)
├── README.md                 # ← Este archivo
├── requirements.txt          # Dependencias Python
└── app/
    ├── main.py               # Entry point: FastAPI, CORS, rutas, health checks
    ├── config.py             # Configuración desde variables de entorno
    ├── database.py           # Conexiones SQLAlchemy (business + security)
    ├── security.py           # Autenticación por API Key
    ├── repositories/
    │   └── reporte_general.py  # Consulta SQL del reporte general
    ├── routes/
    │   └── reportes.py         # Endpoints de la API
    ├── schemas/
    │   └── reportes.py         # Modelos Pydantic (entrada/salida)
    └── services/
        └── analisis.py         # Motor de análisis + integración Gemini
```

---

## 📄 Licencia

Proyecto privado — Parte del ecosistema **DIRPOLES**. Todos los derechos reservados.
