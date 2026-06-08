"""
Repositorio para el reporte general.
Consulta la misma UNION ALL de 7 tablas que usaba ReportesIAModel.php
y aplica filtros opcionales en Python.
"""

from datetime import datetime
from app.database import ejecutar_consulta


def obtener_datos_reporte_general(
    fecha_inicio: str = None,
    fecha_fin: str = None,
    genero: str = None,
    pnf: str = None,
    area: str = None
) -> list:
    """
    Consulta todas las atenciones registradas en los 7 servicios del sistema
    y aplica los filtros opcionales.

    Retorna una lista de diccionarios con las columnas:
    nombres, apellidos, cedula, genero, nombre_pnf, nombre_serv, fecha_creacion
    """

    # La misma consulta UNION ALL que tenía ReportesIAModel.php
    query = """
        SELECT
            b.nombres, b.apellidos, b.cedula, b.genero,
            pnf.nombre_pnf, 
            'Becas' AS nombre_serv,
            bp.fecha_creacion
        FROM beneficiario b
        LEFT JOIN pnf ON b.id_pnf = pnf.id_pnf
        LEFT JOIN solicitud_de_servicio ss ON ss.id_beneficiario = b.id_beneficiario
        LEFT JOIN becas bp ON ss.id_solicitud_serv = bp.id_solicitud_serv
        WHERE bp.fecha_creacion IS NOT NULL

        UNION ALL

        SELECT
            b.nombres, b.apellidos, b.cedula, b.genero,
            pnf.nombre_pnf, 
            'Exoneración' AS nombre_serv,
            ep.fecha_creacion
        FROM beneficiario b
        LEFT JOIN pnf ON b.id_pnf = pnf.id_pnf
        LEFT JOIN solicitud_de_servicio ss ON ss.id_beneficiario = b.id_beneficiario
        LEFT JOIN exoneracion ep ON ss.id_solicitud_serv = ep.id_solicitud_serv
        WHERE ep.fecha_creacion IS NOT NULL

        UNION ALL

        SELECT
            b.nombres, b.apellidos, b.cedula, b.genero,
            pnf.nombre_pnf, 
            'FAMES' AS nombre_serv,
            fp.fecha_creacion
        FROM beneficiario b
        LEFT JOIN pnf ON b.id_pnf = pnf.id_pnf
        LEFT JOIN solicitud_de_servicio ss ON ss.id_beneficiario = b.id_beneficiario
        LEFT JOIN fames fp ON ss.id_solicitud_serv = fp.id_solicitud_serv
        WHERE fp.fecha_creacion IS NOT NULL

        UNION ALL

        SELECT
            b.nombres, b.apellidos, b.cedula, b.genero,
            pnf.nombre_pnf, 
            s.nombre_serv,
            mp.fecha_creacion
        FROM beneficiario b
        LEFT JOIN pnf ON b.id_pnf = pnf.id_pnf
        LEFT JOIN solicitud_de_servicio ss ON ss.id_beneficiario = b.id_beneficiario
        LEFT JOIN servicio s ON ss.id_servicios = s.id_servicios
        LEFT JOIN consulta_medica mp ON ss.id_solicitud_serv = mp.id_solicitud_serv
        WHERE mp.fecha_creacion IS NOT NULL

        UNION ALL

        SELECT
            b.nombres, b.apellidos, b.cedula, b.genero,
            pnf.nombre_pnf, 
            s.nombre_serv,
            op.fecha_creacion
        FROM beneficiario b
        LEFT JOIN pnf ON b.id_pnf = pnf.id_pnf
        LEFT JOIN solicitud_de_servicio ss ON ss.id_beneficiario = b.id_beneficiario
        LEFT JOIN servicio s ON ss.id_servicios = s.id_servicios
        LEFT JOIN orientacion op ON ss.id_solicitud_serv = op.id_solicitud_serv
        WHERE op.fecha_creacion IS NOT NULL

        UNION ALL

        SELECT
            b.nombres, b.apellidos, b.cedula, b.genero,
            pnf.nombre_pnf, 
            s.nombre_serv,
            dp.fecha_creacion
        FROM beneficiario b
        LEFT JOIN pnf ON b.id_pnf = pnf.id_pnf
        LEFT JOIN solicitud_de_servicio ss ON ss.id_beneficiario = b.id_beneficiario
        LEFT JOIN servicio s ON ss.id_servicios = s.id_servicios
        LEFT JOIN discapacidad dp ON ss.id_solicitud_serv = dp.id_solicitud_serv
        WHERE dp.fecha_creacion IS NOT NULL

        UNION ALL

        SELECT
            b.nombres, b.apellidos, b.cedula, b.genero,
            pnf.nombre_pnf, 
            s.nombre_serv,
            cp.fecha_creacion
        FROM beneficiario b
        LEFT JOIN pnf ON b.id_pnf = pnf.id_pnf
        LEFT JOIN solicitud_de_servicio ss ON ss.id_beneficiario = b.id_beneficiario
        LEFT JOIN servicio s ON ss.id_servicios = s.id_servicios
        LEFT JOIN consulta_psicologica cp ON ss.id_solicitud_serv = cp.id_solicitud_serv
        WHERE cp.fecha_creacion IS NOT NULL
    """

    filas = ejecutar_consulta(query, base="business")

    # Aplicar filtros en Python
    filtradas = []
    for fila in filas:
        # Filtro por fecha
        if fecha_inicio or fecha_fin:
            fecha_raw = fila.get("fecha_creacion")
            if fecha_raw:
                if isinstance(fecha_raw, datetime):
                    item_date = fecha_raw.strftime("%Y-%m-%d")
                else:
                    item_date = str(fecha_raw)[:10]

                if fecha_inicio and item_date < fecha_inicio:
                    continue
                if fecha_fin and item_date > fecha_fin:
                    continue
            else:
                continue  # Sin fecha, no pasa el filtro de fecha

        # Filtro por género
        if genero and fila.get("genero") != genero:
            continue

        # Filtro por PNF
        if pnf and fila.get("nombre_pnf") != pnf:
            continue

        # Filtro por área/servicio
        if area and fila.get("nombre_serv") != area:
            continue

        filtradas.append(fila)

    return filtradas
