"""
Configuración central del microservicio DIRPOLES IA.
Lee las variables del archivo .env y las expone como constantes.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# --- Base de Datos Principal (dirpoles_business) ---
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_NAME = os.getenv("DB_NAME", "dirpoles_business")
DB_USER = os.getenv("DB_USER", "root")
DB_PASS = os.getenv("DB_PASS", "")

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# --- Base de Datos de Seguridad (dirpoles_security) ---
DB_SECURITY_NAME = os.getenv("DB_SECURITY_NAME", "dirpoles_security")
DATABASE_SECURITY_URL = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_SECURITY_NAME}"

# --- Servidor ---
SERVER_HOST = os.getenv("SERVER_HOST", "0.0.0.0")
SERVER_PORT = int(os.getenv("SERVER_PORT", "8000"))

# --- Seguridad (API Key compartida con el monolito PHP) ---
IA_API_KEY = os.getenv("IA_API_KEY", "")

# --- IA (Google AI Studio / Gemini) ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# --- CORS ---
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost").split(",")
