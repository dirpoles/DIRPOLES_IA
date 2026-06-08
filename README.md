# 🤖 DIRPOLES_IA — Microservicio de Análisis Inteligente

**Versión:** 1.0.0  
**Stack:** Python + FastAPI + MySQL  
**Propósito:** Proporcionar análisis estadístico e inteligencia artificial a los reportes del sistema **DIRPOLES_4**.

---

## 🧠 ¿Qué es DIRPOLES_IA?

Es un microservicio independiente desarrollado en **Python con FastAPI** que funciona como un **motor de análisis** para la plataforma **DIRPOLES_4** (PHP). Recibe datos de reportes vía HTTP, los procesa con lógica estadística y devuelve hallazgos, resúmenes, estadísticas y recomendaciones en formato JSON.

Está diseñado para ejecutarse en **paralelo al servidor Apache** de DIRPOLES_4, sin interferir con su funcionamiento.

---

## 🏗️ Arquitectura

```
┌──────────────────────┐       HTTP/JSON        ┌──────────────────────┐
│   DIRPOLES_4 (PHP)   │ ◄─────────────────────► │   DIRPOLES_IA (Py)   │
│   Apache :80         │       X-API-Key Auth     │   Uvicorn :8000      │
│   Frontend + Backend │                          │   Motor de Análisis  │
└──────┬───────────────┘                          └──────────┬───────────┘
       │                                                      │
       │                  ┌────────────────────┐              │
       └──────────────────►   MySQL (compartida)◄─────────────┘
                          │   dirpoles_business │
                          └────────────────────┘
```

### Flujo de comunicación

1. El usuario solicita un análisis desde la interfaz de DIRPOLES_4.
2. DIRPOLES_4 compila los datos del reporte desde la base de datos compartida.
3. DIRPOLES_4 envía una petición HTTP POST a `http://localhost:8000/api/v1/analizar` con los datos y la clave API.
4. El microservicio procesa los datos, calcula estadísticas y devuelve un análisis en JSON.
5. DIRPOLES_4 recibe la respuesta y la presenta al usuario.

---

## 📡 Endpoints disponibles

| Método | Ruta | Descripción | Auth |
|--------|------|-------------|------|
| `GET` | `/` | Health check básico | ❌ |
| `GET` | `/health` | Health check detallado (incluye BD) | ❌ |
| `GET` | `/api/v1/tipos-reportes` | Lista los tipos de reporte soportados | ❌ |
| `POST` | `/api/v1/analizar` | Analiza un reporte y genera hallazgos | ✅ |
| `POST` | `/api/v1/preguntar` | Responde preguntas en lenguaje natural sobre los datos | ✅ |

> La documentación interactiva está disponible en `/docs` (Swagger UI) y `/redoc` (ReDoc).

---

## 📋 Tipos de reporte soportados

| Tipo | Descripción |
|------|-------------|
| `general` | Reporte General — Análisis cruzado de todos los servicios |
| `psicologia` | Psicología — Morbilidad y citas psicológicas |
| `medicina` | Medicina — Consultas médicas e inventario |
| `orientacion` | Orientación — Casos de asesoría |
| `becas` | Becas — Solicitudes y asignaciones |
| `discapacidad` | Discapacidad — Servicios relacionados |
| `transporte` | Transporte — Vehículos, rutas y proveedores |
| `mobiliario` | Mobiliario — Inventario de equipos y mobiliario |
| `jornadas` | Jornadas Médicas — Eventos médicos especiales |
| `referencias` | Referencias — Derivaciones entre servicios |

---

## 🔐 Autenticación

El microservicio utiliza **API Key** mediante el encabezado HTTP:

```
X-API-Key: <tu-clave-secreta>
```

La clave se configura en la variable de entorno `API_SECRET_KEY`. Los endpoints `POST /api/v1/analizar` y `POST /api/v1/preguntar` están protegidos.

---

## ⚙️ Variables de entorno (`.env`)

| Variable | Valor por defecto | Descripción |
|----------|-------------------|-------------|
| `DB_HOST` | `localhost` | Host de la base de datos MySQL |
| `DB_PORT` | `3306` | Puerto de la base de datos |
| `DB_NAME` | `dirpoles_business` | Nombre de la base de datos compartida |
| `DB_USER` | `root` | Usuario de la base de datos |
| `DB_PASS` | *(vacío)* | Contraseña de la base de datos |
| `SERVER_HOST` | `0.0.0.0` | IP de escucha del servidor |
| `SERVER_PORT` | `8000` | Puerto del servidor |
| `API_SECRET_KEY` | `default-secret-key` | Clave secreta para autenticación |
| `ALLOWED_ORIGINS` | `http://localhost` | Orígenes permitidos por CORS |

---

## 🚀 Instalación y ejecución

### 1. Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd DIRPOLES_IA
```

### 2. Crear y activar el entorno virtual

```bash
python -m venv venv
.\venv\Scripts\activate   # Windows
source venv/bin/activate  # Linux/Mac
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Copiar `.env` con los valores de tu entorno:

```
DB_HOST=localhost
DB_PORT=3306
DB_NAME=dirpoles_business
DB_USER=root
DB_PASS=tu_contraseña
API_SECRET_KEY=mi-clave-secreta
SERVER_HOST=0.0.0.0
SERVER_PORT=8000
ALLOWED_ORIGINS=http://localhost,http://localhost:80
```

### 5. Ejecutar el servidor

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

O directamente:

```bash
python -m app.main
```

El servicio estará disponible en `http://localhost:8000`.

---

## 🧪 Capacidades de análisis

Actualmente el motor incluye:

- **Conteo total de registros** y distribución por género.
- **Top 3 PNF** (Programas Nacionales de Formación) más frecuentes.
- **Bottom 3 PNF** con recomendaciones si requieren atención.
- **Identificación del servicio más usado** dentro del reporte.
- **Análisis temporal mensual**: mes pico y tendencia (creciente/decreciente).
- **Resumen ejecutivo** en lenguaje natural.
- **Recomendaciones automáticas** basadas en los datos.
- **Respuesta a preguntas** en lenguaje natural mediante coincidencia de patrones.

> En versiones futuras se integrará con **OpenAI**, **scikit-learn** y otras herramientas de IA/ML.

---

## 🛠️ Tecnologías utilizadas

| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| [FastAPI](https://fastapi.tiangolo.com/) | 0.135.3 | Framework web ASGI |
| [Uvicorn](https://www.uvicorn.org/) | 0.44.0 | Servidor ASGI |
| [SQLAlchemy](https://www.sqlalchemy.org/) | 2.0.49 | ORM para base de datos |
| [PyMySQL](https://pypi.org/project/PyMySQL/) | 1.1.2 | Driver MySQL |
| [Pydantic](https://docs.pydantic.dev/) | 2.13.0 | Validación de datos |
| [python-dotenv](https://github.com/theskumar/python-dotenv) | 1.2.2 | Gestión de variables de entorno |

---

## 📁 Estructura del proyecto

```
DIRPOLES_IA/
├── .env                          # Variables de entorno
├── .gitignore                    # Archivos ignorados por Git
├── requirements.txt              # Dependencias de Python
├── README.md                     # Este documento
├── guia_microservicio_fastapi.md # Guía de uso para desarrolladores
├── venv/                         # Entorno virtual
└── app/
    ├── __init__.py
    ├── main.py                   # Punto de entrada de la aplicación
    ├── config.py                 # Configuración desde variables de entorno
    ├── database.py               # Conexión a MySQL con SQLAlchemy
    ├── security.py               # Autenticación por API Key
    ├── routes/
    │   ├── __init__.py
    │   └── reportes.py           # Rutas de la API
    ├── schemas/
    │   ├── __init__.py
    │   └── reportes.py           # Modelos Pydantic (entrada/salida)
    └── services/
        ├── __init__.py
        └── analisis.py           # Lógica de análisis estadístico
```

---

## 🔄 Conexión con DIRPOLES_4

DIRPOLES_4 se comunica con este microservicio a través de **peticiones HTTP** desde PHP usando `curl` o `file_get_contents`. Ejemplo:

```php
$ch = curl_init('http://localhost:8000/api/v1/analizar');
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_HTTPHEADER, [
    'Content-Type: application/json',
    'X-API-Key: mi-clave-secreta'
]);
curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode([
    'tipo_reporte' => 'psicologia',
    'datos' => $datosDelReporte
]));
$respuesta = curl_exec($ch);
curl_close($ch);
```

---

## 📄 Licencia

Este proyecto es parte del ecosistema **DIRPOLES**. Todos los derechos reservados.
