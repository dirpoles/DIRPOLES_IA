"""
Conexión a las bases de datos MySQL.
Soporta dos bases de datos: dirpoles_business y dirpoles_security.
"""

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.config import DATABASE_URL, DATABASE_SECURITY_URL

# ============================================================
# Motor y sesión para dirpoles_business (BD principal)
# ============================================================
engine = create_engine(DATABASE_URL, pool_recycle=3600, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ============================================================
# Motor y sesión para dirpoles_security
# ============================================================
engine_security = create_engine(DATABASE_SECURITY_URL, pool_recycle=3600, echo=False)
SessionSecurity = sessionmaker(autocommit=False, autoflush=False, bind=engine_security)


def get_db():
    """Genera una sesión de dirpoles_business y la cierra al terminar."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_db_security():
    """Genera una sesión de dirpoles_security y la cierra al terminar."""
    db = SessionSecurity()
    try:
        yield db
    finally:
        db.close()


def ejecutar_consulta(consulta_sql: str, parametros: dict = None, base="business"):
    """
    Ejecuta una consulta SQL y retorna una lista de diccionarios.

    Parámetros:
        consulta_sql: La consulta SQL como string
        parametros: Diccionario con los parámetros (para consultas preparadas)
        base: "business" para dirpoles_business, "security" para dirpoles_security
    """
    Session = SessionLocal if base == "business" else SessionSecurity
    db = Session()
    try:
        resultado = db.execute(text(consulta_sql), parametros or {})
        filas = resultado.mappings().all()
        return [dict(fila) for fila in filas]
    except Exception as e:
        raise e
    finally:
        db.close()
