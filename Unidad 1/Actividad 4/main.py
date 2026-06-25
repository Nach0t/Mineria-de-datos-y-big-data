import sqlite3

DB_NAME = "hospital_dwh.db"


def conectar_db(db_name=DB_NAME):
    return sqlite3.connect(db_name)


def pregunta_a(con):
    query = """
    SELECT
        d.Especialidad,
        SUM(h.CostoTratamiento) AS CostoTotal,
        SUM(h.DiasEstancia) AS DiasTotales
    FROM Hechos_Hospitalizaciones h
    JOIN Dim_Doctor d ON h.Doctor_Key = d.Doctor_Key
    GROUP BY d.Especialidad
    ORDER BY CostoTotal DESC, DiasTotales DESC;
    """
    cur = con.cursor()
    cur.execute(query)
    return cur.fetchall()


def pregunta_b(con):
    query = """
    SELECT
        CASE
            WHEN p.Edad < 18 THEN 'Ninos'
            WHEN p.Edad >= 65 THEN 'Adultos Mayores'
            ELSE 'Otros'
        END AS GrupoEdad,
        COUNT(*) AS Atenciones,
        SUM(h.CostoTratamiento) AS CostoTotal
    FROM Hechos_Hospitalizaciones h
    JOIN Dim_Paciente p ON h.Paciente_Key = p.Paciente_Key
    GROUP BY GrupoEdad
    ORDER BY Atenciones DESC;
    """
    cur = con.cursor()
    cur.execute(query)
    return cur.fetchall()


def pregunta_c(con):
    query = """
    SELECT
        t.Anio,
        t.Mes,
        d.Nombre AS Doctor,
        COUNT(*) AS TotalAtenciones
    FROM Hechos_Hospitalizaciones h
    JOIN Dim_Doctor d ON h.Doctor_Key = d.Doctor_Key
    JOIN Dim_Tiempo t ON h.Tiempo_Key = t.Tiempo_Key
    GROUP BY t.Anio, t.Mes, d.Nombre
    ORDER BY t.Anio, t.Mes, TotalAtenciones DESC;
    """
    cur = con.cursor()
    cur.execute(query)
    return cur.fetchall()


def pregunta_d(con):
    query = """
    SELECT
        dg.Gravedad,
        p.Genero,
        COUNT(*) AS TotalAtenciones
    FROM Hechos_Hospitalizaciones h
    JOIN Dim_Paciente p ON h.Paciente_Key = p.Paciente_Key
    JOIN Dim_Diagnostico dg ON h.Diagnostico_Key = dg.Diagnostico_Key
    GROUP BY dg.Gravedad, p.Genero
    ORDER BY dg.Gravedad DESC, TotalAtenciones DESC;
    """
    cur = con.cursor()
    cur.execute(query)
    return cur.fetchall()


def pregunta_e(con):
    query = """
    SELECT
        dg.Descripcion,
        COUNT(*) AS TotalAtenciones
    FROM Hechos_Hospitalizaciones h
    JOIN Dim_Diagnostico dg ON h.Diagnostico_Key = dg.Diagnostico_Key
    JOIN Dim_Tiempo t ON h.Tiempo_Key = t.Tiempo_Key
    WHERE t.Mes BETWEEN 1 AND 6
    GROUP BY dg.Descripcion
    ORDER BY TotalAtenciones DESC;
    """
    cur = con.cursor()
    cur.execute(query)
    return cur.fetchall()


def pregunta_f(con):
    query = """
    SELECT
        t.Anio,
        t.Mes,
        SUM(h.CostoTratamiento) AS CostoTotalFacturado
    FROM Hechos_Hospitalizaciones h
    JOIN Dim_Tiempo t ON h.Tiempo_Key = t.Tiempo_Key
    GROUP BY t.Anio, t.Mes
    ORDER BY t.Anio, t.Mes;
    """
    cur = con.cursor()
    cur.execute(query)
    return cur.fetchall()


def pregunta_g(con):
    query = """
    SELECT
        d.Especialidad,
        AVG(h.DiasEstancia) AS PromedioDiasEstancia
    FROM Hechos_Hospitalizaciones h
    JOIN Dim_Doctor d ON h.Doctor_Key = d.Doctor_Key
    GROUP BY d.Especialidad
    ORDER BY PromedioDiasEstancia DESC;
    """
    cur = con.cursor()
    cur.execute(query)
    return cur.fetchall()


def pregunta_h(con):
    query = """
    SELECT
        dg.Descripcion,
        COUNT(*) AS TotalCasos
    FROM Hechos_Hospitalizaciones h
    JOIN Dim_Diagnostico dg ON h.Diagnostico_Key = dg.Diagnostico_Key
    GROUP BY dg.Descripcion
    ORDER BY TotalCasos DESC
    LIMIT 5;
    """
    cur = con.cursor()
    cur.execute(query)
    return cur.fetchall()


def imprimir_resultados(titulo, filas, encabezados):
    print(f"\n{titulo}")
    print("-" * len(titulo))
    print(" | ".join(encabezados))
    print("-" * 100)
    for fila in filas:
        print(" | ".join(str(x) for x in fila))


def main():
    con = conectar_db()
    try:
        imprimir_resultados(
            "A) Especialidad más costosa y con más días de estancia",
            pregunta_a(con),
            ["Especialidad", "CostoTotal", "DiasTotales"]
        )

        imprimir_resultados(
            "B) Qué se atiende más: niños o adultos mayores",
            pregunta_b(con),
            ["GrupoEdad", "Atenciones", "CostoTotal"]
        )

        imprimir_resultados(
            "C) Doctor con más atenciones mensualmente",
            pregunta_c(con),
            ["Anio", "Mes", "Doctor", "TotalAtenciones"]
        )

        imprimir_resultados(
            "D) Género más atendido por gravedad",
            pregunta_d(con),
            ["Gravedad", "Genero", "TotalAtenciones"]
        )

        imprimir_resultados(
            "E) Enfermedad más atendida en los primeros 6 meses",
            pregunta_e(con),
            ["Descripcion", "TotalAtenciones"]
        )

        imprimir_resultados(
            "F) Costo total facturado por mes",
            pregunta_f(con),
            ["Anio", "Mes", "CostoTotalFacturado"]
        )

        imprimir_resultados(
            "G) Promedio de estancia por especialidad médica",
            pregunta_g(con),
            ["Especialidad", "PromedioDiasEstancia"]
        )

        imprimir_resultados(
            "H) 5 diagnósticos más comunes",
            pregunta_h(con),
            ["Descripcion", "TotalCasos"]
        )
    finally:
        con.close()


if __name__ == "__main__":
    main()
