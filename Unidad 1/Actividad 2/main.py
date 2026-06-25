import sqlite3


DB_NAME = "tienda_dw.db"


def conectar_db(db_name=DB_NAME):
    """Abre la conexión a la base de datos SQLite."""
    return sqlite3.connect(db_name)


def pregunta_a(con):
    """
    A) ¿Cuánto dinero ganamos por categoría de producto en el primer trimestre?
    """
    query = """
    SELECT
        p.Categoria,
        SUM(h.TotalVenta) AS IngresosTotales,
        SUM(h.Cantidad) AS UnidadesVendidas
    FROM Hecho_Ventas h
    JOIN Dim_producto p ON h.Producto_Key = p.Producto_Key
    JOIN Dim_tiempo t ON h.Tiempo_Key = t.Tiempo_Key
    WHERE t.Trimestre = 1
    GROUP BY p.Categoria
    ORDER BY IngresosTotales DESC;
    """
    cur = con.cursor()
    cur.execute(query)
    return cur.fetchall()


def pregunta_b(con):
    """
    B) Ranking de Ventas por Categoría
    """
    query = """
    SELECT
        p.Categoria,
        SUM(h.TotalVenta) AS GranTotal,
        COUNT(h.VentaId) AS NumeroDeTransacciones
    FROM Hecho_Ventas h
    JOIN Dim_producto p ON h.Producto_Key = p.Producto_Key
    GROUP BY p.Categoria
    ORDER BY GranTotal DESC;
    """
    cur = con.cursor()
    cur.execute(query)
    return cur.fetchall()


def pregunta_c(con):
    """
    C) Ventas por Mes
    """
    query = """
    SELECT
        t.Anio,
        t.Mes,
        SUM(h.TotalVenta) AS VentaMensual
    FROM Hecho_Ventas h
    JOIN Dim_tiempo t ON h.Tiempo_Key = t.Tiempo_Key
    GROUP BY t.Anio, t.Mes
    ORDER BY t.Anio, MIN(t.Tiempo_Key);
    """
    cur = con.cursor()
    cur.execute(query)
    return cur.fetchall()


def pregunta_d(con):
    """
    D) Saber qué productos son los "estrellas" y cuáles no se están moviendo
    """
    query = """
    SELECT
        p.Nombre AS Producto,
        p.Categoria,
        SUM(h.Cantidad) AS UnidadesVendidas,
        SUM(h.TotalVenta) AS IngresosTotales,
        AVG(p.PrecioUnitario) AS PrecioPromedio
    FROM Hecho_Ventas h
    JOIN Dim_producto p ON h.Producto_Key = p.Producto_Key
    GROUP BY p.Nombre, p.Categoria
    ORDER BY UnidadesVendidas DESC, IngresosTotales DESC;
    """
    cur = con.cursor()
    cur.execute(query)
    return cur.fetchall()


def pregunta_e(con):
    """
    E) Ventas por periodo: año, trimestre y mes
    """
    query = """
    SELECT
        t.Anio,
        t.Trimestre,
        t.Mes,
        SUM(h.TotalVenta) AS TotalVendido,
        COUNT(h.VentaId) AS TotalTransacciones
    FROM Hecho_Ventas h
    JOIN Dim_tiempo t ON h.Tiempo_Key = t.Tiempo_Key
    GROUP BY t.Anio, t.Trimestre, t.Mes
    ORDER BY t.Anio, t.Trimestre, MIN(t.Tiempo_Key);
    """
    cur = con.cursor()
    cur.execute(query)
    return cur.fetchall()


def imprimir_resultados(titulo, filas, encabezados):
    print(f"\n{titulo}")
    print("-" * len(titulo))
    print(" | ".join(encabezados))
    print("-" * 80)
    for fila in filas:
        print(" | ".join(str(x) for x in fila))


def main():
    con = conectar_db()

    try:
        res_a = pregunta_a(con)
        res_b = pregunta_b(con)
        res_c = pregunta_c(con)
        res_d = pregunta_d(con)
        res_e = pregunta_e(con)

        imprimir_resultados(
            "Pregunta A: Ingresos por categoría en el primer trimestre",
            res_a,
            ["Categoria", "IngresosTotales", "UnidadesVendidas"]
        )

        imprimir_resultados(
            "Pregunta B: Ranking de ventas por categoría",
            res_b,
            ["Categoria", "GranTotal", "NumeroDeTransacciones"]
        )

        imprimir_resultados(
            "Pregunta C: Ventas por mes",
            res_c,
            ["Anio", "Mes", "VentaMensual"]
        )

        imprimir_resultados(
            "Pregunta D: Productos estrella / menor movimiento",
            res_d,
            ["Producto", "Categoria", "UnidadesVendidas", "IngresosTotales", "PrecioPromedio"]
        )

        imprimir_resultados(
            "Pregunta E: Ventas por periodo",
            res_e,
            ["Anio", "Trimestre", "Mes", "TotalVendido", "TotalTransacciones"]
        )

    finally:
        con.close()


if __name__ == "__main__":
    main()
