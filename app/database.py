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
