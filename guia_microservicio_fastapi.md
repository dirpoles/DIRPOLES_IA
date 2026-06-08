# 🐍 Guía Completa: Implementación de un Microservicio con Python y FastAPI para DIRPOLES_4

> **¿Para quién es esta guía?** Para el equipo de desarrollo de DIRPOLES_4 que necesita crear un módulo de Inteligencia Artificial como un servicio independiente. No se asume conocimiento previo de Python, FastAPI ni arquitectura de microservicios.

---

## 📚 Tabla de Contenidos

1. [Conceptos Fundamentales](#1-conceptos-fundamentales)
2. [¿Por qué un Microservicio y no agregarlo al PHP?](#2-por-qué-un-microservicio-y-no-agregarlo-al-php)
3. [¿Por qué Python y FastAPI?](#3-por-qué-python-y-fastapi)
4. [Mapa General de la Arquitectura](#4-mapa-general-de-la-arquitectura)
5. [Prerequisitos: Instalar Python en Windows](#5-prerequisitos-instalar-python-en-windows)
6. [Paso 1: Crear la Carpeta del Microservicio](#6-paso-1-crear-la-carpeta-del-microservicio)
7. [Paso 2: Crear un Entorno Virtual de Python](#7-paso-2-crear-un-entorno-virtual-de-python)
8. [Paso 3: Instalar las Dependencias (librerías)](#8-paso-3-instalar-las-dependencias-librerías)
9. [Paso 4: Estructura de Carpetas del Microservicio](#9-paso-4-estructura-de-carpetas-del-microservicio)
10. [Paso 5: Archivo de Configuración (.env)](#10-paso-5-archivo-de-configuración-env)
11. [Paso 6: Configuración Central (config.py)](#11-paso-6-configuración-central-configpy)
12. [Paso 7: Conexión a la Base de Datos MySQL](#12-paso-7-conexión-a-la-base-de-datos-mysql)
13. [Paso 8: Crear el Archivo Principal (main.py)](#13-paso-8-crear-el-archivo-principal-mainpy)
14. [Paso 9: Crear los Schemas (Modelos de Datos)](#14-paso-9-crear-los-schemas-modelos-de-datos)
15. [Paso 10: Crear los Servicios (Lógica de Negocio)](#15-paso-10-crear-los-servicios-lógica-de-negocio)
16. [Paso 11: Crear las Rutas (Endpoints de la API)](#16-paso-11-crear-las-rutas-endpoints-de-la-api)
17. [Paso 12: Arrancar el Microservicio](#17-paso-12-arrancar-el-microservicio)
18. [Paso 13: Probar el Microservicio](#18-paso-13-probar-el-microservicio)
19. [Paso 14: Conectar DIRPOLES_4 (PHP/JS) con el Microservicio](#19-paso-14-conectar-dirpoles_4-phpjs-con-el-microservicio)
20. [Paso 15: Seguridad - Proteger el Microservicio](#20-paso-15-seguridad---proteger-el-microservicio)
21. [Paso 16: Futuro - Integrar IA Real](#21-paso-16-futuro---integrar-ia-real)
22. [Resumen de Comandos Rápidos](#22-resumen-de-comandos-rápidos)
23. [Errores Comunes y Soluciones](#23-errores-comunes-y-soluciones)
24. [Diagrama de Flujo Completo](#24-diagrama-de-flujo-completo)

---

## 1. Conceptos Fundamentales

Antes de escribir una sola línea de código, necesitas entender **qué estamos haciendo y por qué**. Voy explicando cada término como si fuera la primera vez que lo escuchas.

### 1.1 ¿Qué es una API?

**API** significa *Application Programming Interface* (Interfaz de Programación de Aplicaciones). Es un **contrato** que permite que dos programas hablen entre sí.

**Analogía del mundo real:** Piensa en un restaurante. Tú (el cliente) no vas a la cocina a cocinar tu comida. En su lugar, le dices al mesero (la API) lo que quieres, y el mesero le lleva tu pedido a la cocina (el servidor). La cocina prepara tu comida y el mesero te la trae de vuelta.

En tu sistema DIRPOLES_4, **ya usas APIs sin saberlo**. Cuando tu JavaScript hace un `fetch()` a una ruta como `reportes_general_data`, está llamando a una API. El PHP recibe la petición, consulta la base de datos, y devuelve los datos en formato JSON. Eso es una API.

```
[Tu navegador / JavaScript]  --->  petición HTTP  --->  [Servidor PHP (Apache/XAMPP)]
                              <---  respuesta JSON <---
```

### 1.2 ¿Qué es una API REST?

**REST** (*Representational State Transfer*) es una **convención** (un conjunto de reglas) sobre cómo construir APIs. Define cómo se organizan las URLs y qué tipo de operación hace cada una.

Las reglas principales son:

| Método HTTP | Propósito | Ejemplo |
|---|---|---|
| `GET` | **Leer** datos (sin modificar nada) | Obtener lista de beneficiarios |
| `POST` | **Crear** algo nuevo | Registrar un nuevo beneficiario |
| `PUT` | **Actualizar** algo existente completamente | Actualizar todos los datos de un beneficiario |
| `PATCH` | **Actualizar parcialmente** | Cambiar solo el teléfono de un beneficiario |
| `DELETE` | **Eliminar** algo | Eliminar un registro |

Tu sistema DIRPOLES_4 usa parcialmente REST (usa `GET` y `POST`), pero no sigue la convención completa. Eso está bien, no necesita cambiar.

### 1.3 ¿Qué es un Microservicio?

Un **microservicio** es una **aplicación pequeña e independiente** que hace **una sola cosa** y la hace bien.

**¿Qué significa "independiente"?** Significa que:
- Tiene su **propio servidor** (no corre dentro de Apache/XAMPP)
- Tiene su **propio código fuente** (carpeta separada)
- Puede estar escrito en un **lenguaje diferente** (en tu caso, Python en vez de PHP)
- Se puede **encender y apagar** sin afectar al sistema principal
- Se comunica con el sistema principal **a través de la red** (HTTP), no compartiendo archivos

**Analogía:** Imagina que DIRPOLES_4 es un edificio de oficinas. Actualmente, toda la empresa (beneficiarios, medicina, psicología, transporte, reportes) trabaja en el mismo edificio. Un microservicio sería como contratar a una empresa **externa** especializada en inteligencia artificial, que trabaja en **su propia oficina**, y a la que le envías datos por correo (HTTP) y te devuelve respuestas por correo.

```
┌─────────────────────────────────────────────┐
│         TU SISTEMA ACTUAL (Monolito)        │
│                                             │
│  DIRPOLES_4 (PHP + Apache en XAMPP)         │
│  Puerto: 80                                 │
│                                             │
│  ┌─────────┐ ┌────────┐ ┌───────────────┐  │
│  │Benefici.│ │Medicina│ │  Reportes     │  │
│  └─────────┘ └────────┘ └──────┬────────┘  │
│                                │            │
│                     Necesita análisis IA    │
│                                │            │
└────────────────────────────────┼────────────┘
                                 │
                    Petición HTTP (red local)
                                 │
                                 ▼
┌─────────────────────────────────────────────┐
│     MICROSERVICIO NUEVO (separado)          │
│                                             │
│  Python + FastAPI                           │
│  Puerto: 8000                               │
│                                             │
│  ┌──────────────────────────────────────┐   │
│  │  Módulo de Inteligencia Artificial   │   │
│  │  - Análisis de reportes              │   │
│  │  - Generación de respuestas          │   │
│  │  - Predicciones estadísticas         │   │
│  └──────────────────────────────────────┘   │
│                                             │
└─────────────────────────────────────────────┘
```

### 1.4 ¿Qué es un Puerto?

Un **puerto** es como una **puerta numerada** en tu computadora. Cada programa que responde peticiones de red necesita su propia puerta.

- XAMPP (Apache) usa el **puerto 80** (o 443 para HTTPS). Cuando abres `http://localhost/DIRPOLES_4/`, estás tocando la puerta 80.
- MySQL usa el **puerto 3306**. Cuando PHP se conecta a la base de datos, toca la puerta 3306.
- El microservicio de FastAPI usará el **puerto 8000**. Cuando PHP le quiera preguntar algo a la IA, tocará la puerta 8000.

Todos en la misma computadora (`localhost`), pero cada uno en su propia puerta.

### 1.5 ¿Qué es JSON?

**JSON** (*JavaScript Object Notation*) es un formato de texto para intercambiar datos. Ya lo usas en DIRPOLES_4 cuando tu PHP hace `json_encode()` y tu JavaScript hace `response.json()`.

```json
{
    "exito": true,
    "mensaje": "Datos obtenidos correctamente",
    "datos": [
        {"nombre": "Juan", "cedula": "V-12345678"},
        {"nombre": "María", "cedula": "V-87654321"}
    ]
}
```

Los microservicios se comunican usando JSON. Tu sistema PHP enviará datos en JSON al microservicio Python, y Python responderá en JSON.

---

## 2. ¿Por qué un Microservicio y no agregarlo al PHP?

Podrías preguntarte: *"¿Por qué no simplemente agregar el módulo de IA dentro del PHP como un controlador más?"*

Razones técnicas:

| Factor | Dentro de PHP | Como Microservicio (Python) |
|---|---|---|
| **Librerías de IA** | Muy pocas y limitadas | Miles de opciones maduras (TensorFlow, scikit-learn, pandas, OpenAI) |
| **Rendimiento** | PHP no es óptimo para cálculos pesados | Python está optimizado para ciencia de datos |
| **Si la IA falla** | Podría tumbar todo DIRPOLES_4 | Solo se cae el microservicio, DIRPOLES_4 sigue funcionando |
| **Escalabilidad** | Difícil de escalar una parte sin la otra | Puedes poner el microservicio en otro servidor más potente |
| **Equipo** | Necesitas saber PHP para todo | El equipo de IA puede trabajar en Python sin tocar PHP |

> [!IMPORTANT]
> **La razón principal:** El ecosistema de Inteligencia Artificial vive en Python. No existe un equivalente real en PHP. Por eso les dijeron que usaran Python.

---

## 3. ¿Por qué Python y FastAPI?

### 3.1 ¿Por qué Python?

**Python** es un lenguaje de programación de propósito general, pero es el **rey indiscutible** de la inteligencia artificial, ciencia de datos y machine learning. Todas las librerías importantes de IA están en Python:

- **pandas**: Para manipular y analizar tablas de datos (similar a Excel pero en código)
- **scikit-learn**: Para machine learning (predicciones, clasificaciones)
- **OpenAI / LangChain**: Para conectar con modelos de lenguaje como ChatGPT
- **matplotlib / plotly**: Para generar gráficas

### 3.2 ¿Qué es FastAPI?

**FastAPI** es un **framework** (un conjunto de herramientas pre-construidas) para crear APIs en Python. Es como lo que es tu `Router.php` para DIRPOLES_4, pero para Python y mucho más poderoso.

**¿Por qué FastAPI y no otro?** Existen otros frameworks en Python (como Flask o Django), pero FastAPI tiene ventajas:

| Característica | FastAPI | Flask | Django |
|---|---|---|---|
| Velocidad de ejecución | ⭐⭐⭐⭐⭐ (el más rápido) | ⭐⭐⭐ | ⭐⭐⭐ |
| Documentación automática | ✅ Sí (Swagger/OpenAPI) | ❌ Manual | ❌ Manual |
| Validación de datos automática | ✅ Sí (con Pydantic) | ❌ Manual | Parcial |
| Fácil de aprender | ✅ Muy intuitivo | ✅ Simple | ❌ Complejo |
| Async (procesos simultáneos) | ✅ Nativo | ❌ No | ❌ No nativo |

> [!TIP]
> **La documentación automática** significa que FastAPI genera una página web donde puedes ver y probar TODAS las rutas de tu API sin escribir documentación. Es como tener un Postman integrado gratis.

### 3.3 ¿Qué es un Framework?

Si no sabes qué es un framework: es un **esqueleto pre-construido** que te ahorra escribir código repetitivo. En vez de escribir tú mismo el código para recibir peticiones HTTP, parsear JSON, validar datos, manejar errores, etc., el framework lo hace por ti. Tú solo escribes la **lógica de tu negocio** (la parte importante).

Es similar a cómo en DIRPOLES_4 tu `Router.php` te permite escribir `Router::get('ruta', función)` en vez de tener que parsear manualmente la URL, verificar el método HTTP, etc.

---

## 4. Mapa General de la Arquitectura

```mermaid
graph TB
    subgraph "Navegador del Usuario"
        A[JavaScript / Frontend DIRPOLES_4]
    end

    subgraph "Servidor XAMPP - Puerto 80"
        B[Apache]
        C[PHP - DIRPOLES_4]
        C --> D[ReportesController.php]
        C --> E[Otros Controllers]
    end

    subgraph "Servidor FastAPI - Puerto 8000"
        F[Python - FastAPI]
        F --> G[Endpoint /api/v1/analizar]
        F --> H[Endpoint /api/v1/predecir]
        F --> I[Módulo IA / ML]
    end

    subgraph "Base de Datos - Puerto 3306"
        J[(MySQL - dirpoles_business)]
        K[(MySQL - dirpoles_security)]
    end

    A -->|1. Usuario pide análisis IA| B
    B --> C
    D -->|2. PHP recopila datos de reportes| J
    D -->|3. PHP envía datos al microservicio| F
    G -->|4. FastAPI procesa con IA| I
    F -->|5. FastAPI puede consultar BD directamente también| J
    F -->|6. Respuesta JSON con análisis| D
    D -->|7. PHP devuelve resultado al navegador| A

    style F fill:#4CAF50,color:white
    style C fill:#777BB4,color:white
    style J fill:#F29111,color:white
```

### Flujo paso a paso (cómo funciona en la práctica):

1. El usuario está en la vista de reportes de DIRPOLES_4 y hace clic en un botón **"Analizar con IA"**
2. El JavaScript del frontend hace un `fetch()` al PHP (como ya hace normalmente)
3. El PHP (controller) recopila los datos del reporte desde MySQL
4. El PHP hace una petición HTTP **interna** al microservicio FastAPI (como si fuera un `fetch()` pero desde el backend)
5. FastAPI recibe los datos, los procesa con inteligencia artificial
6. FastAPI devuelve el resultado (análisis, predicciones, resúmenes) en JSON
7. El PHP recibe la respuesta y se la envía al navegador del usuario
8. El JavaScript muestra el resultado al usuario

**Alternativa simplificada:** El JavaScript del frontend también puede llamar directamente al microservicio FastAPI sin pasar por PHP. Esto es más simple pero menos seguro (explicado más adelante).

---

## 5. Prerequisitos: Instalar Python en Windows

### 5.1 Verificar si ya tienes Python

Abre PowerShell (o CMD) y escribe:

```powershell
python --version
```

Si ves algo como `Python 3.11.x` o `Python 3.12.x`, ya lo tienes instalado. **Salta al Paso 1.**

Si ves un error como `'python' no se reconoce como un comando...`, necesitas instalarlo.

### 5.2 Descargar Python

1. Ve a [https://www.python.org/downloads/](https://www.python.org/downloads/)
2. Descarga la versión más reciente (3.11 o 3.12, **no uses 3.13** porque algunas librerías de IA aún no son compatibles)
3. **MUY IMPORTANTE:** Al instalar, marca la casilla **☑ "Add Python to PATH"** en la primera pantalla del instalador. Si no marcas esto, el comando `python` no funcionará desde la terminal.
4. Haz clic en "Install Now"

### 5.3 Verificar que pip funciona

**pip** es el gestor de paquetes de Python. Es como lo que es `composer` para PHP o `npm` para JavaScript. Te permite instalar librerías (paquetes) que otras personas han creado.

```powershell
pip --version
```

Deberías ver algo como: `pip 23.x from c:\users\...`. Si no funciona, reinicia la terminal.

### 5.4 Herramienta adicional: Instalar `virtualenv`

```powershell
pip install virtualenv
```

**¿Qué es `virtualenv`?** Es una herramienta para crear **entornos virtuales**. Un entorno virtual es como una "burbuja" o "caja aislada" donde instalas las librerías de tu proyecto sin afectar al Python global del sistema. Así evitas conflictos si tienes varios proyectos Python con diferentes versiones de librerías.

Es similar a cómo `node_modules` aísla las dependencias de un proyecto Node.js, o cómo `vendor` aísla las de un proyecto PHP con Composer.

---

## 6. Paso 1: Crear la Carpeta del Microservicio

> [!IMPORTANT]
> **"Aislado"** significa que el microservicio vive en su **propia carpeta**, completamente separada de `DIRPOLES_4`. No va dentro de la carpeta del proyecto PHP. Tiene su propio repositorio Git si lo deseas.

### 6.1 ¿Dónde creamos la carpeta?

Tienes dos opciones:

**Opción A (Recomendada para desarrollo):** Al mismo nivel que DIRPOLES_4:
```
c:\xampp\htdocs\
├── DIRPOLES_4\          ← Tu sistema PHP actual
└── dirpoles_ia\         ← El nuevo microservicio Python (AQUÍ)
```

**Opción B (Para producción futura):** En cualquier otra ubicación, incluso en otro servidor:
```
c:\proyectos\dirpoles_ia\    ← Podría estar en cualquier lado
```

Usaremos la **Opción A** porque es más práctica durante el desarrollo.

### 6.2 Crear la carpeta

Abre PowerShell y ejecuta:

```powershell
mkdir c:\xampp\htdocs\dirpoles_ia
```

> [!NOTE]
> Esta carpeta **no** será servida por Apache/XAMPP. Aunque esté dentro de `htdocs`, el microservicio tiene su propio servidor (Uvicorn, que veremos más adelante). Apache solo sirve archivos PHP.

---

## 7. Paso 2: Crear un Entorno Virtual de Python

Un **entorno virtual** es como crear una "copia privada" de Python solo para este proyecto. Todas las librerías que instales (FastAPI, etc.) se guardarán dentro de esta carpeta, sin afectar tu instalación global de Python.

### 7.1 Crear el entorno virtual

```powershell
# Navega a la carpeta del microservicio
cd c:\xampp\htdocs\dirpoles_ia

# Crea un entorno virtual llamado "venv"
python -m venv venv
```

Esto creará una carpeta `venv` dentro de `dirpoles_ia` con una copia aislada de Python.

### 7.2 Activar el entorno virtual

**Cada vez que abras una terminal nueva** para trabajar en el microservicio, debes activar el entorno virtual:

```powershell
# En PowerShell:
.\venv\Scripts\Activate.ps1
```

> [!WARNING]
> **Si ves un error sobre "políticas de ejecución"**, ejecuta esto primero (una sola vez como administrador):
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

Sabrás que está activado porque verás `(venv)` al inicio de la línea de tu terminal:

```
(venv) PS C:\xampp\htdocs\dirpoles_ia>
```

### 7.3 Para desactivar el entorno virtual (cuando termines de trabajar)

```powershell
deactivate
```

> [!IMPORTANT]
> **Regla de oro:** Siempre que trabajes en el microservicio, primero activa el entorno virtual. Si no lo activas, `pip install` instalará las librerías en tu Python global, no en el proyecto.

---

## 8. Paso 3: Instalar las Dependencias (librerías)

Con el entorno virtual **activado** (debes ver `(venv)` en tu terminal), instala las librerías necesarias:

```powershell
pip install fastapi uvicorn python-dotenv pymysql sqlalchemy pydantic
```

### ¿Qué hace cada una?

| Librería | ¿Qué es? | ¿Para qué la usamos? |
|---|---|---|
| `fastapi` | El framework para crear la API | Es el esqueleto de nuestro microservicio |
| `uvicorn` | Servidor ASGI para Python | Es el "Apache" de Python. Ejecuta el servidor que escucha peticiones. Sin esto, FastAPI no puede correr |
| `python-dotenv` | Lector de archivos `.env` | Para leer variables de entorno (contraseñas, configuración), igual que tu PHP usa `Dotenv\Dotenv` |
| `pymysql` | Driver de MySQL para Python | Permite que Python se conecte a MySQL, igual que PDO en PHP |
| `sqlalchemy` | ORM para bases de datos | Permite hacer consultas SQL de forma segura. Es como PDO pero más poderoso |
| `pydantic` | Validador de datos | Valida automáticamente que los datos recibidos tienen el formato correcto. Se instala con FastAPI pero lo mencionamos explícitamente |

### 8.1 Guardar las dependencias en un archivo

Esto es como tu `composer.json` o `package.json` pero para Python:

```powershell
pip freeze > requirements.txt
```

Este comando crea un archivo `requirements.txt` que lista TODAS las librerías instaladas con sus versiones exactas. Cuando otro miembro del equipo clone el proyecto, solo necesita ejecutar:

```powershell
pip install -r requirements.txt
```

Y tendrá exactamente las mismas librerías.

---

## 9. Paso 4: Estructura de Carpetas del Microservicio

Crea la siguiente estructura dentro de `c:\xampp\htdocs\dirpoles_ia\`:

```
dirpoles_ia/
│
├── venv/                    ← Entorno virtual (ya lo creamos, NO tocar)
│
├── app/                     ← Código fuente del microservicio
│   ├── __init__.py          ← Archivo vacío que le dice a Python "esto es un paquete"
│   ├── main.py              ← Punto de entrada (como tu index.php)
│   ├── config.py            ← Configuración (como tu config.php)
│   ├── database.py          ← Conexión a BD (como tu Database.php)
│   │
│   ├── routes/              ← Rutas/endpoints (como tu carpeta app/routes/)
│   │   ├── __init__.py
│   │   └── reportes.py      ← Endpoints de análisis de reportes
│   │
│   ├── schemas/             ← Modelos de datos de entrada/salida
│   │   ├── __init__.py
│   │   └── reportes.py      ← Definición de qué datos se esperan y se devuelven
│   │
│   └── services/            ← Lógica de negocio / IA
│       ├── __init__.py
│       └── analisis.py      ← La lógica de inteligencia artificial
│
├── .env                     ← Variables de entorno (contraseñas, config)
├── .gitignore               ← Archivos que Git debe ignorar
├── requirements.txt         ← Lista de dependencias (ya lo creamos)
└── README.md                ← Documentación del proyecto
```

### 9.1 ¿Qué son los archivos `__init__.py`?

En Python, una carpeta con un archivo `__init__.py` se convierte en un **paquete** (package). Un paquete es simplemente una forma de organizar el código en módulos. El archivo puede estar **completamente vacío**, solo necesita existir.

Es similar a los `namespace` en PHP. Cuando en tu PHP escribes `namespace App\Models;`, le dices a PHP que ese archivo pertenece al paquete `App\Models`. En Python, la estructura de carpetas con `__init__.py` logra lo mismo.

### 9.2 Crear los archivos

Ejecuta estos comandos en PowerShell:

```powershell
cd c:\xampp\htdocs\dirpoles_ia

# Crear carpetas
mkdir app
mkdir app\routes
mkdir app\schemas
mkdir app\services

# Crear archivos __init__.py (vacíos)
New-Item -Path app\__init__.py -ItemType File
New-Item -Path app\routes\__init__.py -ItemType File
New-Item -Path app\schemas\__init__.py -ItemType File
New-Item -Path app\services\__init__.py -ItemType File

# Crear archivos principales (vacíos por ahora, los llenaremos después)
New-Item -Path app\main.py -ItemType File
New-Item -Path app\config.py -ItemType File
New-Item -Path app\database.py -ItemType File
New-Item -Path app\routes\reportes.py -ItemType File
New-Item -Path app\schemas\reportes.py -ItemType File
New-Item -Path app\services\analisis.py -ItemType File

# Crear archivos raíz
New-Item -Path .env -ItemType File
New-Item -Path .gitignore -ItemType File
New-Item -Path README.md -ItemType File
```

### 9.3 Crear el `.gitignore`

Si vas a usar Git (recomendado), crea el archivo `.gitignore` con este contenido:

```gitignore
# Entorno virtual - NUNCA subir a Git (es como node_modules)
venv/

# Variables de entorno con contraseñas
.env

# Archivos compilados de Python (se generan automáticamente)
__pycache__/
*.py[cod]

# IDE
.vscode/
.idea/
```

---

## 10. Paso 5: Archivo de Configuración (.env)

El archivo `.env` guarda la configuración sensible (contraseñas, secretos) **fuera del código**. Tu DIRPOLES_4 ya usa uno para el JWT, este es el mismo concepto.

### 10.1 Contenido del `.env`

Edita `c:\xampp\htdocs\dirpoles_ia\.env`:

```env
# ========================================
# Configuración del Microservicio DIRPOLES IA
# ========================================

# --- Base de Datos (misma que usa DIRPOLES_4) ---
DB_HOST=localhost
DB_PORT=3306
DB_NAME=dirpoles_business
DB_USER=root
DB_PASS=

# Base de datos de seguridad (si la necesitas)
DB_SECURITY_NAME=dirpoles_security
DB_SECURITY_USER=root
DB_SECURITY_PASS=

# --- Configuración del Servidor ---
# El puerto donde correrá el microservicio
# (diferente al 80 de Apache)
SERVER_HOST=0.0.0.0
SERVER_PORT=8000

# --- Seguridad ---
# Clave secreta para validar que las peticiones vienen de DIRPOLES_4
# Debe ser un string largo y aleatorio
API_SECRET_KEY=mi-clave-secreta-para-el-microservicio-2026

# Orígenes permitidos (CORS) - explicado más adelante
# Este es el dominio desde donde DIRPOLES_4 hace las peticiones
ALLOWED_ORIGINS=http://localhost,http://localhost:80,http://127.0.0.1

# --- IA (para el futuro) ---
# OPENAI_API_KEY=sk-tu-clave-de-openai-aqui
```

> [!CAUTION]
> **NUNCA subas el archivo `.env` a Git** (por eso está en `.gitignore`). Contiene contraseñas. Cada desarrollador debe crear su propio `.env` basado en un `.env.example`.

---

## 11. Paso 6: Configuración Central (config.py)

Este archivo lee las variables del `.env` y las pone disponibles para todo el proyecto. Es el equivalente a tu `app/Config/config.php`.

### 11.1 Contenido de `app/config.py`

```python
"""
Configuración central del microservicio.
Lee las variables del archivo .env y las expone como constantes.

Equivalente a: DIRPOLES_4/app/Config/config.php
"""

import os
from dotenv import load_dotenv

# Cargar las variables del archivo .env
# Esto es equivalente a lo que hace tu PHP:
#   $dotenv = \Dotenv\Dotenv::createImmutable(BASE_PATH);
#   $dotenv->load();
load_dotenv()

# --- Base de Datos ---
# os.getenv("NOMBRE", "valor_por_defecto") lee una variable de entorno
# Si no existe, usa el valor por defecto

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_NAME = os.getenv("DB_NAME", "dirpoles_business")
DB_USER = os.getenv("DB_USER", "root")
DB_PASS = os.getenv("DB_PASS", "")

DB_SECURITY_NAME = os.getenv("DB_SECURITY_NAME", "dirpoles_security")

# Cadena de conexión para SQLAlchemy (formato estándar)
# pymysql es el driver que instalamos para conectar Python con MySQL
# Formato: mysql+pymysql://usuario:contraseña@host:puerto/base_de_datos
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# --- Servidor ---
SERVER_HOST = os.getenv("SERVER_HOST", "0.0.0.0")
SERVER_PORT = int(os.getenv("SERVER_PORT", "8000"))

# --- Seguridad ---
API_SECRET_KEY = os.getenv("API_SECRET_KEY", "default-secret-key")

# Orígenes permitidos para CORS (explicado más adelante)
# .split(",") convierte el string "a,b,c" en una lista ["a", "b", "c"]
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost").split(",")
```

### Nota sobre la sintaxis de Python vs PHP

Si vienes de PHP, aquí hay una tabla de equivalencias que te ayudará:

| Concepto | PHP | Python |
|---|---|---|
| Variable | `$nombre = "Juan";` | `nombre = "Juan"` (sin `$`, sin `;`) |
| Constante | `const PI = 3.14;` | `PI = 3.14` (por convención en MAYÚSCULAS) |
| String con variables | `"Hola {$nombre}"` | `f"Hola {nombre}"` (nota la `f` al inicio) |
| Comentario una línea | `// comentario` | `# comentario` |
| Comentario multi-línea | `/* ... */` | `""" ... """` (triple comillas) |
| Importar archivo | `require_once 'archivo.php';` | `from modulo import algo` |
| Array/Lista | `$arr = [1, 2, 3];` | `arr = [1, 2, 3]` |
| Array asociativo / Diccionario | `$arr = ['clave' => 'valor'];` | `dic = {'clave': 'valor'}` |
| Función | `function nombre() { }` | `def nombre():` (usa indentación, no llaves) |
| Null | `null` | `None` |
| True/False | `true / false` | `True / False` (con mayúscula) |

---

## 12. Paso 7: Conexión a la Base de Datos MySQL

Este archivo configura la conexión a la misma base de datos MySQL que usa DIRPOLES_4. Es el equivalente a tu `app/Core/Database.php`.

### 12.1 Contenido de `app/database.py`

```python
"""
Conexión a la base de datos MySQL.
Usa SQLAlchemy para crear una conexión reutilizable.

Equivalente a: DIRPOLES_4/app/Core/Database.php
"""

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.config import DATABASE_URL

# Crear el "motor" de conexión
# pool_recycle=3600: reconecta automáticamente después de 1 hora
#   (evita que MySQL cierre conexiones inactivas)
# echo=False: no imprime las consultas SQL en la terminal (cámbialo a True para debug)
engine = create_engine(
    DATABASE_URL,
    pool_recycle=3600,
    echo=False
)

# Crear una "fábrica" de sesiones (conexiones a la BD)
# Cada sesión es como hacer: new PDO(...) en tu PHP
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_db():
    """
    Función generadora que crea una sesión de base de datos
    y la cierra automáticamente al terminar.

    En PHP, tú creas la conexión en el constructor de Database.php
    y la cierras manualmente (o PHP la cierra al terminar el script).

    En FastAPI, usamos esta función como "dependencia" que se inyecta
    automáticamente en cada endpoint que necesite la base de datos.

    Uso en un endpoint:
        @router.get("/datos")
        def obtener_datos(db: Session = Depends(get_db)):
            resultado = db.execute(text("SELECT * FROM beneficiario"))
            return resultado.fetchall()
    """
    db = SessionLocal()
    try:
        yield db  # "yield" pausa aquí y entrega la sesión al endpoint
    finally:
        db.close()  # Cuando el endpoint termina, se cierra la conexión


def ejecutar_consulta(consulta_sql: str, parametros: dict = None):
    """
    Función de utilidad para ejecutar consultas SQL directamente.
    Similar a como tu PHP usa $stmt = $this->conn->prepare($query);

    Parámetros:
        consulta_sql: La consulta SQL como string
        parametros: Diccionario con los parámetros (para consultas preparadas)

    Retorna:
        Lista de diccionarios con los resultados

    Ejemplo de uso:
        datos = ejecutar_consulta(
            "SELECT * FROM beneficiario WHERE cedula = :cedula",
            {"cedula": "V-12345678"}
        )
    """
    db = SessionLocal()
    try:
        resultado = db.execute(text(consulta_sql), parametros or {})
        # .mappings() convierte cada fila en un diccionario {columna: valor}
        filas = resultado.mappings().all()
        # Convertir a lista de diccionarios normales
        return [dict(fila) for fila in filas]
    except Exception as e:
        raise e
    finally:
        db.close()
```

---

## 13. Paso 8: Crear el Archivo Principal (main.py)

Este es el **punto de entrada** del microservicio. Es equivalente a tu `index.php`. Aquí se configura FastAPI, se registran las rutas y se configura CORS.

### 13.1 ¿Qué es CORS?

**CORS** (*Cross-Origin Resource Sharing*) es una **protección de seguridad** de los navegadores web.

**El problema:** Cuando tu página web está en `http://localhost/DIRPOLES_4/` (origen A) y quiere hacer un `fetch()` a `http://localhost:8000/api/analizar` (origen B), el navegador lo **bloquea por seguridad**. Piensa que es un ataque porque estás intentando acceder a un servidor diferente.

**La solución:** El servidor del microservicio (FastAPI) debe decirle al navegador: *"Tranquilo, yo autorizo que peticiones desde `http://localhost` me lleguen"*. Eso es CORS.

Si no configuras CORS, verás este error en la consola del navegador:
```
Access to fetch at 'http://localhost:8000/...' from origin 'http://localhost' 
has been blocked by CORS policy
```

### 13.2 Contenido de `app/main.py`

```python
"""
Punto de entrada del microservicio DIRPOLES IA.
Equivalente a: DIRPOLES_4/index.php

Aquí se:
1. Crea la aplicación FastAPI
2. Configura CORS (para que el navegador permita las peticiones)
3. Registra las rutas (endpoints)
4. Define el endpoint de salud (health check)
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import ALLOWED_ORIGINS, SERVER_HOST, SERVER_PORT

# ============================================================
# 1. CREAR LA APLICACIÓN
# ============================================================
# Esto es como crear tu Router en PHP, pero FastAPI hace mucho más.

app = FastAPI(
    title="DIRPOLES IA - Microservicio de Inteligencia Artificial",
    description="""
    Microservicio que provee análisis con inteligencia artificial
    para los reportes estadísticos del sistema DIRPOLES_4.
    
    Este servicio es independiente del sistema PHP principal 
    y se comunica con él a través de peticiones HTTP (API REST).
    """,
    version="1.0.0",
    # Prefijo de la documentación automática
    docs_url="/docs",       # Swagger UI: http://localhost:8000/docs
    redoc_url="/redoc",     # ReDoc: http://localhost:8000/redoc
)

# ============================================================
# 2. CONFIGURAR CORS
# ============================================================
# Esto permite que DIRPOLES_4 (corriendo en localhost:80) 
# haga peticiones a este microservicio (corriendo en localhost:8000)

app.add_middleware(
    CORSMiddleware,
    # Orígenes permitidos (de dónde pueden venir las peticiones)
    allow_origins=ALLOWED_ORIGINS,
    # Permitir envío de cookies/credenciales
    allow_credentials=True,
    # Métodos HTTP permitidos
    allow_methods=["GET", "POST"],
    # Headers permitidos en las peticiones
    allow_headers=["*"],
)

# ============================================================
# 3. REGISTRAR RUTAS
# ============================================================
# Importamos y registramos las rutas desde los archivos del directorio routes/
# Es equivalente a tu archivo routes.php que hace:
#   foreach (glob(BASE_PATH . 'app/routes/*.php') as $rutaArchivo) {
#       require_once $rutaArchivo;
#   }

from app.routes import reportes as rutas_reportes

# "prefix" agrega un prefijo a todas las rutas del módulo
# "tags" agrupa las rutas en la documentación automática
app.include_router(
    rutas_reportes.router,
    prefix="/api/v1",
    tags=["Reportes IA"]
)

# ============================================================
# 4. ENDPOINT DE SALUD (Health Check)
# ============================================================
# Es una ruta simple que sirve para verificar que el microservicio
# está vivo y respondiendo. Es una práctica estándar en microservicios.

@app.get("/")
def health_check():
    """
    Verificar que el microservicio está activo.
    
    Equivalente a visitar http://localhost:8000/ en el navegador.
    Si ves este JSON, el servicio está funcionando.
    """
    return {
        "estado": "activo",
        "servicio": "DIRPOLES IA",
        "version": "1.0.0",
        "mensaje": "El microservicio de Inteligencia Artificial está funcionando correctamente."
    }


@app.get("/health")
def health_detailed():
    """
    Verificación detallada del estado del servicio.
    Incluye verificación de conexión a la base de datos.
    """
    # Intentamos conectar a la BD para verificar
    from app.database import ejecutar_consulta
    try:
        ejecutar_consulta("SELECT 1")
        db_status = "conectada"
    except Exception as e:
        db_status = f"error: {str(e)}"

    return {
        "estado": "activo",
        "base_de_datos": db_status,
        "servicio": "DIRPOLES IA",
        "version": "1.0.0"
    }


# ============================================================
# 5. ARRANQUE DEL SERVIDOR (solo si se ejecuta directamente)
# ============================================================
# Este bloque solo se ejecuta cuando corres: python -m app.main
# En producción, usarías: uvicorn app.main:app --host 0.0.0.0 --port 8000

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=SERVER_HOST,
        port=SERVER_PORT,
        reload=True  # Recarga automática al cambiar código (solo para desarrollo)
    )
```

### 13.3 Explicación de `@app.get("/")`

Si no has visto la sintaxis `@algo` antes, se llama **decorador**. Es una forma de Python para "decorar" o "modificar" una función.

```python
@app.get("/ruta")
def mi_funcion():
    return {"dato": "valor"}
```

Esto es equivalente a esto en tu PHP:

```php
Router::get('ruta', function() {
    echo json_encode(["dato" => "valor"]);
});
```

El decorador `@app.get("/")` le dice a FastAPI: *"Cuando alguien haga una petición GET a la ruta `/`, ejecuta la función que está debajo"*.

---

## 14. Paso 9: Crear los Schemas (Modelos de Datos)

Los **schemas** definen la **forma** (estructura) de los datos que entran y salen de tu API. Son como un contrato: "Para usar este endpoint, debes enviarme datos con esta forma exacta".

### 14.1 ¿Qué es Pydantic?

**Pydantic** es una librería que valida datos automáticamente. Tú defines una "plantilla" y Pydantic se asegura de que los datos recibidos cumplan con ella. Si no cumplen, devuelve un error automáticamente al cliente.

En tu PHP, haces esto manualmente:
```php
// En tu ReportesModel.php
case 'id_tipo_empleado':
    if (!filter_var($valor, FILTER_VALIDATE_INT, ['options' => ['min_range' => 1]])) {
        throw new InvalidArgumentException("El ID debe ser un número entero positivo.");
    }
```

Con Pydantic, es automático:
```python
class MiModelo(BaseModel):
    id_tipo_empleado: int  # Pydantic valida automáticamente que sea un entero
```

### 14.2 Contenido de `app/schemas/reportes.py`

```python
"""
Schemas (modelos de datos) para los endpoints de reportes.

Definen QUÉ datos se esperan recibir y QUÉ datos se van a devolver.
Es como definir un "contrato" o "formulario" para cada endpoint.

En tu PHP, las validaciones están dispersas en los Models.
Aquí se centralizan en un solo lugar.
"""

from pydantic import BaseModel, Field
from typing import Optional, List
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

    # 'datos' es una Lista de diccionarios (cada elemento es un registro del reporte)
    # List[dict] = lista de diccionarios
    datos: List[dict] = Field(
        ...,
        description="Array con los datos del reporte a analizar"
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

    datos: List[dict] = Field(
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
```

---

## 15. Paso 10: Crear los Servicios (Lógica de Negocio)

Los **servicios** contienen la lógica real: el procesamiento de datos, los análisis, las predicciones. Aquí es donde eventualmente irá la inteligencia artificial.

### 15.1 Contenido de `app/services/analisis.py`

```python
"""
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
    """
    Analiza los datos de un reporte y genera un resumen inteligente.

    Parámetros:
        tipo_reporte: Tipo de reporte (general, psicologia, medicina, etc.)
        datos: Lista de registros del reporte (cada uno es un diccionario)
        fecha_inicio: Filtro opcional de fecha inicio
        fecha_fin: Filtro opcional de fecha fin

    Retorna:
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

    return {
        "exito": True,
        "tipo_reporte": tipo_reporte,
        "resumen": resumen,
        "hallazgos": hallazgos,
        "estadisticas": estadisticas,
        "recomendaciones": recomendaciones,
        "fecha_analisis": datetime.now().isoformat()
    }


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
        generos = Counter([d.get("genero", "").upper() for d in datos if d.get("genero")])
        if generos:
            respuesta_partes = []
            for g, c in generos.most_common():
                nombre = "Masculino" if g == "M" else "Femenino" if g == "F" else g
                porcentaje = round((c / total) * 100, 1)
                respuesta_partes.append(f"{nombre}: {c} ({porcentaje}%)")

            return {
                "exito": True,
                "pregunta": pregunta,
                "respuesta": f"Distribución por género en '{tipo_reporte}': " + ", ".join(respuesta_partes) + ".",
                "datos_soporte": dict(generos)
            }

    # === Preguntas sobre PNF ===
    if any(palabra in pregunta_lower for palabra in ["pnf", "carrera", "programa"]):
        pnfs = Counter([d.get("nombre_pnf", "") for d in datos if d.get("nombre_pnf")])
        if pnfs:
            top = pnfs.most_common(5)
            respuesta_partes = [f"{nombre}: {cant} registros" for nombre, cant in top]
            return {
                "exito": True,
                "pregunta": pregunta,
                "respuesta": f"Los PNF más frecuentes en '{tipo_reporte}' son: " + "; ".join(respuesta_partes) + ".",
                "datos_soporte": {"top_pnf": dict(top)}
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
```

---

## 16. Paso 11: Crear las Rutas (Endpoints de la API)

Las rutas definen **qué URLs están disponibles** en el microservicio y **qué hacen**. Es equivalente a tus archivos en `app/routes/` de DIRPOLES_4.

### 16.1 Contenido de `app/routes/reportes.py`

```python
"""
Rutas (endpoints) para el módulo de análisis de reportes con IA.

Equivalente a: DIRPOLES_4/app/routes/reportes.php
Pero solo para las funcionalidades de IA.

Estas rutas quedarán bajo el prefijo /api/v1/ (definido en main.py)
Ejemplo: POST http://localhost:8000/api/v1/analizar
"""

from fastapi import APIRouter, HTTPException

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

# Crear el router (agrupador de rutas)
# Es como crear un grupo de rutas en tu PHP
router = APIRouter()


# ============================================================
# ENDPOINT 1: Analizar un reporte
# ============================================================
# Decorador: cuando alguien haga POST a /api/v1/analizar, ejecuta esta función
# response_model indica qué forma tiene la respuesta (para la documentación)

@router.post(
    "/analizar",
    response_model=AnalisisOutput,
    summary="Analizar un reporte con IA",
    description="""
    Recibe los datos de un reporte estadístico y devuelve un análisis 
    inteligente que incluye: resumen, hallazgos, estadísticas y recomendaciones.
    
    Los datos deben enviarse en el cuerpo de la petición como JSON.
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
    description="""
    Envía una pregunta en lenguaje natural junto con los datos de un reporte,
    y la IA intentará responderla basándose en los datos proporcionados.
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
```

---

## 17. Paso 12: Arrancar el Microservicio

### 17.1 Correr el servidor en modo desarrollo

Abre PowerShell, activa el entorno virtual y ejecuta:

```powershell
cd c:\xampp\htdocs\dirpoles_ia
.\venv\Scripts\Activate.ps1

# Opción 1: Correr con uvicorn directamente (RECOMENDADO)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Opción 2: Correr con Python
python -m app.main
```

### 17.2 ¿Qué significa cada parámetro?

| Parámetro | Significado |
|---|---|
| `app.main:app` | "En el archivo `app/main.py`, busca el objeto llamado `app`" |
| `--reload` | Reinicia automáticamente cuando modificas un archivo (solo para desarrollo) |
| `--host 0.0.0.0` | Escuchar en todas las interfaces de red (necesario para que PHP pueda acceder) |
| `--port 8000` | Usar el puerto 8000 |

### 17.3 Verificar que funciona

Si todo está bien, verás en la terminal:

```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345]
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

> [!IMPORTANT]
> **El microservicio debe estar corriendo en su propia terminal**. No cierres esa terminal mientras quieras usarlo. Es como mantener XAMPP abierto para que Apache funcione. Cada uno en su propia ventana.

---

## 18. Paso 13: Probar el Microservicio

### 18.1 Desde el navegador

Abre tu navegador y visita:

- **Health check:** [http://localhost:8000/](http://localhost:8000/) → Deberías ver el JSON de estado
- **Documentación Swagger:** [http://localhost:8000/docs](http://localhost:8000/docs) → Página interactiva donde puedes probar todos los endpoints
- **Documentación ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc) → Documentación en formato más formal

### 18.2 Desde Swagger UI (la forma más fácil)

1. Ve a [http://localhost:8000/docs](http://localhost:8000/docs)
2. Verás todos tus endpoints listados
3. Haz clic en **POST /api/v1/analizar**
4. Haz clic en **"Try it out"** (botón a la derecha)
5. Pega este JSON de prueba en el campo del body:

```json
{
    "tipo_reporte": "general",
    "datos": [
        {"nombres": "Juan", "apellidos": "Pérez", "cedula": "V-12345678", "genero": "M", "nombre_pnf": "Ingeniería", "nombre_serv": "Becas", "fecha_creacion": "2026-01-15"},
        {"nombres": "María", "apellidos": "García", "cedula": "V-87654321", "genero": "F", "nombre_pnf": "Medicina", "nombre_serv": "FAMES", "fecha_creacion": "2026-02-20"},
        {"nombres": "Carlos", "apellidos": "López", "cedula": "V-11111111", "genero": "M", "nombre_pnf": "Ingeniería", "nombre_serv": "Becas", "fecha_creacion": "2026-02-22"},
        {"nombres": "Ana", "apellidos": "Martínez", "cedula": "V-22222222", "genero": "F", "nombre_pnf": "Derecho", "nombre_serv": "Exoneración", "fecha_creacion": "2026-03-01"},
        {"nombres": "Pedro", "apellidos": "Rodríguez", "cedula": "V-33333333", "genero": "M", "nombre_pnf": "Ingeniería", "nombre_serv": "Becas", "fecha_creacion": "2026-03-15"}
    ],
    "fecha_inicio": "2026-01-01",
    "fecha_fin": "2026-03-31"
}
```

6. Haz clic en **"Execute"**
7. Verás la respuesta JSON con el análisis

### 18.3 Desde la terminal (con curl)

```powershell
# Health check
curl http://localhost:8000/

# Analizar un reporte (con datos de prueba)
curl -X POST http://localhost:8000/api/v1/analizar `
  -H "Content-Type: application/json" `
  -d '{"tipo_reporte": "general", "datos": [{"genero": "M"}, {"genero": "F"}, {"genero": "F"}]}'
```

---

## 19. Paso 14: Conectar DIRPOLES_4 (PHP/JS) con el Microservicio

Ahora viene la parte crucial: hacer que tu sistema PHP existente se comunique con el microservicio Python.

### Hay dos formas de hacerlo:

### 19.1 Opción A: Desde JavaScript (Frontend directo → Microservicio)

**Ventaja:** Más simple de implementar.
**Desventaja:** El token de seguridad queda expuesto en el navegador.

Ejemplo en tu archivo JavaScript de la vista de reportes:

```javascript
/**
 * Llama al microservicio de IA para analizar los datos de un reporte.
 * 
 * @param {string} tipoReporte - Tipo de reporte (general, psicologia, etc.)
 * @param {Array} datos - Array con los datos del reporte
 * @returns {Object} Resultado del análisis
 */
async function analizarConIA(tipoReporte, datos) {
    try {
        // URL del microservicio (corre en otro puerto)
        const MICROSERVICIO_URL = 'http://localhost:8000/api/v1';
        
        const response = await fetch(`${MICROSERVICIO_URL}/analizar`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                tipo_reporte: tipoReporte,
                datos: datos
            })
        });

        if (!response.ok) {
            throw new Error(`Error HTTP: ${response.status}`);
        }

        const resultado = await response.json();
        return resultado;

    } catch (error) {
        console.error('Error al conectar con el microservicio de IA:', error);
        return {
            exito: false,
            mensaje: 'No se pudo conectar con el servicio de análisis. Verifique que esté activo.'
        };
    }
}

// ============================================================
// EJEMPLO DE USO: en tu vista de reportes, después de cargar los datos
// ============================================================

// Supongamos que ya tienes los datos del reporte (del fetch al PHP)
// Por ejemplo, después de llamar a reportes_general_data:
async function cargarReporteConAnalisis() {
    // 1. Primero, obtener los datos del reporte desde PHP (como ya lo haces)
    const respuestaReporte = await fetch(BASE_URL + 'reportes_general_data');
    const datosReporte = await respuestaReporte.json();

    // 2. Luego, enviar esos datos al microservicio de IA para análisis
    const analisisIA = await analizarConIA('general', datosReporte);

    // 3. Mostrar el resultado en la interfaz
    if (analisisIA.exito) {
        // Mostrar resumen
        document.getElementById('resumenIA').textContent = analisisIA.resumen;

        // Mostrar hallazgos
        const listaHallazgos = document.getElementById('hallazgosIA');
        analisisIA.hallazgos.forEach(h => {
            const li = document.createElement('li');
            li.textContent = h;
            listaHallazgos.appendChild(li);
        });

        // Mostrar recomendaciones
        const listaRecom = document.getElementById('recomendacionesIA');
        analisisIA.recomendaciones.forEach(r => {
            const li = document.createElement('li');
            li.textContent = r;
            listaRecom.appendChild(li);
        });
    }
}
```

### 19.2 Opción B: Desde PHP (Frontend → PHP → Microservicio) — RECOMENDADA

**Ventaja:** Más seguro. El frontend nunca sabe que existe el microservicio. El PHP actúa como intermediario.
**Desventaja:** Requiere que PHP haga peticiones HTTP (necesita curl).

Crea una función helper reutilizable en tu PHP:

```php
<?php
/**
 * Helper para comunicarse con el microservicio de IA.
 * Colocar en: DIRPOLES_4/app/Core/MicroservicioIA.php
 *
 * Uso:
 *   $ia = new MicroservicioIA();
 *   $resultado = $ia->analizar('general', $datosDelReporte);
 */

namespace App\Core;

class MicroservicioIA
{
    // URL base del microservicio Python
    private $baseUrl;
    
    public function __construct()
    {
        // En producción, esto vendría del .env
        $this->baseUrl = 'http://localhost:8000/api/v1';
    }
    
    /**
     * Envía datos de un reporte al microservicio para análisis.
     *
     * @param string $tipoReporte Tipo de reporte
     * @param array  $datos       Datos del reporte
     * @param string $fechaInicio Fecha inicio (opcional)
     * @param string $fechaFin    Fecha fin (opcional)
     * @return array Resultado del análisis
     */
    public function analizar(string $tipoReporte, array $datos, 
                             string $fechaInicio = null, string $fechaFin = null): array
    {
        $payload = [
            'tipo_reporte' => $tipoReporte,
            'datos' => $datos,
            'fecha_inicio' => $fechaInicio,
            'fecha_fin' => $fechaFin
        ];
        
        return $this->hacerPeticion('POST', '/analizar', $payload);
    }
    
    /**
     * Envía una pregunta sobre los datos al microservicio.
     */
    public function preguntar(string $pregunta, string $tipoReporte, array $datos): array
    {
        $payload = [
            'pregunta' => $pregunta,
            'tipo_reporte' => $tipoReporte,
            'datos' => $datos
        ];
        
        return $this->hacerPeticion('POST', '/preguntar', $payload);
    }
    
    /**
     * Verifica si el microservicio está activo.
     */
    public function estaActivo(): bool
    {
        try {
            $resultado = $this->hacerPeticion('GET', '/../health');
            return isset($resultado['estado']) && $resultado['estado'] === 'activo';
        } catch (\Exception $e) {
            return false;
        }
    }
    
    /**
     * Método privado que realiza la petición HTTP al microservicio.
     * Usa cURL (librería incluida con PHP/XAMPP).
     */
    private function hacerPeticion(string $metodo, string $endpoint, array $datos = null): array
    {
        $url = $this->baseUrl . $endpoint;
        
        // Inicializar cURL
        // cURL es una herramienta de PHP para hacer peticiones HTTP
        // (como un fetch() pero desde el backend)
        $ch = curl_init();
        
        // Configurar la petición
        curl_setopt($ch, CURLOPT_URL, $url);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true); // Devolver la respuesta como string
        curl_setopt($ch, CURLOPT_TIMEOUT, 30); // Timeout de 30 segundos
        curl_setopt($ch, CURLOPT_HTTPHEADER, [
            'Content-Type: application/json',
            'Accept: application/json'
        ]);
        
        if ($metodo === 'POST' && $datos !== null) {
            curl_setopt($ch, CURLOPT_POST, true);
            curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($datos));
        }
        
        // Ejecutar la petición
        $respuesta = curl_exec($ch);
        $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        $error = curl_error($ch);
        curl_close($ch);
        
        // Verificar errores de conexión
        if ($error) {
            throw new \RuntimeException(
                "No se pudo conectar con el microservicio de IA. " .
                "Verifique que esté corriendo en {$this->baseUrl}. Error: {$error}"
            );
        }
        
        // Decodificar la respuesta JSON
        $resultado = json_decode($respuesta, true);
        
        if ($httpCode >= 400) {
            throw new \RuntimeException(
                "El microservicio devolvió un error (HTTP {$httpCode}): " .
                ($resultado['detail']['mensaje'] ?? $respuesta)
            );
        }
        
        return $resultado;
    }
}
```

**Uso en tu `reportesController.php`:**

```php
// Dentro de una nueva función, por ejemplo:
function reportes_analisis_ia()
{
    $permisos = new PermisosModel();
    $modelo = new ReportesModel();
    $modulo = 'Reportes';

    try {
        // 1. Verificar permisos (como siempre)
        $verificar = ['Modulo' => $modulo, 'Permiso' => 'Leer', 'Rol' => $_SESSION['id_tipo_empleado']];
        foreach ($verificar as $atributo => $valor) {
            $permisos->__set($atributo, $valor);
        }
        if (!$permisos->manejarAccion('Verificar')) {
            throw new Exception('No tienes permiso para realizar esta acción');
        }

        // 2. Obtener los datos del reporte desde la BD
        $tipoReporte = $_GET['tipo'] ?? 'general';
        $datosReporte = $modelo->manejarAccion('reporteGeneral');

        // 3. Enviar los datos al microservicio de IA
        require_once BASE_PATH . 'app/Core/MicroservicioIA.php';
        $ia = new \App\Core\MicroservicioIA();
        $analisis = $ia->analizar($tipoReporte, $datosReporte);

        // 4. Devolver el análisis al frontend
        header('Content-Type: application/json');
        echo json_encode($analisis);

    } catch (Throwable $e) {
        http_response_code(500);
        header('Content-Type: application/json');
        echo json_encode([
            'exito' => false,
            'mensaje' => $e->getMessage()
        ]);
        exit();
    }
}
```

---

## 20. Paso 15: Seguridad - Proteger el Microservicio

> [!WARNING]
> Sin seguridad, **cualquier persona** que conozca la URL `http://localhost:8000` podría acceder al microservicio y consultar datos. Debemos protegerlo.

### 20.1 Opción simple: API Key

El microservicio valida que cada petición traiga una clave secreta en el header.

Agrega esto a tu `app/main.py` (o crea un archivo `app/security.py`):

```python
"""
Agregar en app/security.py
"""

from fastapi import Header, HTTPException
from app.config import API_SECRET_KEY


async def verificar_api_key(x_api_key: str = Header(...)):
    """
    Dependencia de seguridad que verifica que la petición 
    incluya un header 'X-API-Key' con la clave correcta.
    
    Uso en un endpoint:
        @router.post("/analizar")
        def analizar(datos: ..., _: str = Depends(verificar_api_key)):
            ...
    """
    if x_api_key != API_SECRET_KEY:
        raise HTTPException(
            status_code=403,
            detail={
                "exito": False,
                "mensaje": "Clave de API inválida. Acceso denegado."
            }
        )
    return x_api_key
```

Luego, en tus endpoints de `app/routes/reportes.py`, agregas la dependencia:

```python
from fastapi import Depends
from app.security import verificar_api_key

@router.post("/analizar", dependencies=[Depends(verificar_api_key)])
def endpoint_analizar_reporte(datos_entrada: DatosReporteInput):
    # ... solo se ejecuta si el X-API-Key es válido
```

Y en tu PHP, agregas el header:

```php
curl_setopt($ch, CURLOPT_HTTPHEADER, [
    'Content-Type: application/json',
    'X-API-Key: mi-clave-secreta-para-el-microservicio-2026'
]);
```

---

## 21. Paso 16: Futuro - Integrar IA Real

Cuando quieras ir más allá del análisis estadístico básico y usar IA real:

### 21.1 Opción 1: OpenAI (ChatGPT)

```powershell
pip install openai
```

```python
# En app/services/analisis.py
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analizar_con_gpt(datos, pregunta):
    respuesta = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Eres un analista de datos del sistema DIRPOLES."},
            {"role": "user", "content": f"Analiza estos datos: {datos}\n\nPregunta: {pregunta}"}
        ]
    )
    return respuesta.choices[0].message.content
```

### 21.2 Opción 2: Modelos locales (sin costo, sin internet)

```powershell
pip install scikit-learn pandas
```

Ideal para predicciones numéricas sobre tus propios datos históricos.

### 21.3 Opción 3: Ollama (IA local tipo ChatGPT)

Puedes correr modelos de lenguaje **localmente** sin costo usando [Ollama](https://ollama.ai/). Esto es útil si no puedes/deben usar servicios externos.

---

## 22. Resumen de Comandos Rápidos

### Primera vez (configuración inicial):

```powershell
# 1. Crear carpeta
mkdir c:\xampp\htdocs\dirpoles_ia
cd c:\xampp\htdocs\dirpoles_ia

# 2. Crear entorno virtual
python -m venv venv

# 3. Activar entorno virtual
.\venv\Scripts\Activate.ps1

# 4. Instalar dependencias
pip install fastapi uvicorn python-dotenv pymysql sqlalchemy pydantic

# 5. Guardar dependencias
pip freeze > requirements.txt

# 6. Crear estructura de carpetas y archivos (ver Paso 4)
```

### Cada vez que vayas a trabajar:

```powershell
# 1. Navegar al proyecto
cd c:\xampp\htdocs\dirpoles_ia

# 2. Activar entorno virtual
.\venv\Scripts\Activate.ps1

# 3. Arrancar el servidor
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Cuando otro miembro del equipo clone el proyecto:

```powershell
# 1. Clonar o copiar el proyecto
cd c:\xampp\htdocs\dirpoles_ia

# 2. Crear su propio entorno virtual
python -m venv venv

# 3. Activar
.\venv\Scripts\Activate.ps1

# 4. Instalar dependencias desde el archivo
pip install -r requirements.txt

# 5. Crear su propio .env (copiar del .env.example)
# 6. Arrancar
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## 23. Errores Comunes y Soluciones

| Error | Causa | Solución |
|---|---|---|
| `'python' no se reconoce como un comando` | Python no está en el PATH | Reinstalar Python marcando "Add to PATH" |
| `Activate.ps1 cannot be loaded because running scripts is disabled` | Política de ejecución de PowerShell | Ejecutar: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` |
| `ModuleNotFoundError: No module named 'fastapi'` | Entorno virtual no activado, o no instalaste las dependencias | Activar `.\venv\Scripts\Activate.ps1` y luego `pip install -r requirements.txt` |
| `CORS error` en el navegador | No configuraste CORS o el origen no está en la lista | Verificar `ALLOWED_ORIGINS` en `.env` |
| `Connection refused` al conectar PHP → FastAPI | El microservicio no está corriendo | Verificar que la terminal con `uvicorn` está activa |
| `Access denied for user 'root'@'localhost'` | Credenciales de MySQL incorrectas | Verificar `DB_USER` y `DB_PASS` en `.env` |
| `Address already in use (port 8000)` | Otro proceso ya usa el puerto 8000 | Cambiar `SERVER_PORT=8001` en `.env` o cerrar el otro proceso |
| `Can't connect to MySQL server` | MySQL no está corriendo | Iniciar MySQL desde el panel de XAMPP |

---

## 24. Diagrama de Flujo Completo

```mermaid
sequenceDiagram
    participant U as 👤 Usuario
    participant JS as 🌐 JavaScript (Frontend)
    participant PHP as 🐘 PHP/Apache (Puerto 80)
    participant DB as 🗄️ MySQL (Puerto 3306)
    participant PY as 🐍 FastAPI (Puerto 8000)

    U->>JS: 1. Clic en "Analizar con IA"
    JS->>PHP: 2. fetch('reportes_analisis_ia?tipo=general')
    PHP->>PHP: 3. Verificar sesión + JWT + permisos
    PHP->>DB: 4. SELECT datos del reporte
    DB-->>PHP: 5. Datos del reporte (array)
    PHP->>PY: 6. POST /api/v1/analizar (con cURL)
    Note over PY: 7. Procesar datos con IA
    PY-->>PHP: 8. JSON con análisis y hallazgos
    PHP-->>JS: 9. JSON con análisis
    JS->>U: 10. Mostrar resumen + hallazgos + recomendaciones
```

---

> [!TIP]
> ## 📋 Checklist de Implementación
> 
> Usa esta lista para rastrear tu progreso:
> 
> - [ ] Instalar Python 3.11+ en Windows
> - [ ] Crear carpeta `c:\xampp\htdocs\dirpoles_ia`
> - [ ] Crear entorno virtual (`python -m venv venv`)
> - [ ] Instalar dependencias (`pip install fastapi uvicorn ...`)
> - [ ] Crear estructura de carpetas y archivos `__init__.py`
> - [ ] Escribir `.env` con credenciales de BD
> - [ ] Escribir `app/config.py`
> - [ ] Escribir `app/database.py`
> - [ ] Escribir `app/main.py` con CORS
> - [ ] Escribir `app/schemas/reportes.py`
> - [ ] Escribir `app/services/analisis.py`
> - [ ] Escribir `app/routes/reportes.py`
> - [ ] Arrancar con `uvicorn app.main:app --reload`
> - [ ] Probar en `http://localhost:8000/docs`
> - [ ] Crear `app/Core/MicroservicioIA.php` en DIRPOLES_4
> - [ ] Crear función en `reportesController.php` para conectar con IA
> - [ ] Agregar ruta en `app/routes/reportes.php` de DIRPOLES_4
> - [ ] Probar flujo completo desde el navegador
> - [ ] Implementar seguridad (API Key)
> - [ ] (Futuro) Integrar IA real (OpenAI, scikit-learn, etc.)
