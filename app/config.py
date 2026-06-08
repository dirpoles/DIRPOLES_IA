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
<<<<<<< HEAD
API_SECRET_KEY = os.getenv("API_SECRET_KEY", "default-secret-key")
=======
API_KEY = os.getenv("X-API-KEY") or os.getenv("X_API_KEY") or os.getenv("API_SECRET_KEY", "default-secret-key")

# --- IA (Google AI Studio / Gemini) ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# --- Seguridad RSA / JWT (Obsoleto, se prefiere cifrado simétrico) ---
# Directorio raíz del proyecto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JWT_PUBLIC_KEY_PATH = os.path.join(BASE_DIR, os.getenv("JWT_PUBLIC_KEY_PATH", "certs/jwt_public.pem"))
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "RS256")
# Inyección directa por variable de entorno (opcional)
JWT_PUBLIC_KEY_PEM = os.getenv("JWT_PUBLIC_KEY_PEM", None)
>>>>>>> 5e14c6e (Microservicio primera parte)

# Orígenes permitidos para CORS (explicado más adelante)
# .split(",") convierte el string "a,b,c" en una lista ["a", "b", "c"]
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost").split(",")
