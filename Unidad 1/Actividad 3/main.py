import sqlite3

DB_NAME = "retail_dw.db"


def conectar_db(db_name=DB_NAME):
    return sqlite3.connect(db_name)


def ranking_ventas_categoria(con):
    query = """
    SELECT
        p.Categoria,
        SUM(h.TotalVenta) AS TotalVendido,
        SUM(h.Cantidad) AS UnidadesVendidas
    FROM Hecho_Ventas h
    JOIN Dim_producto p ON h.Producto_Key = p.Producto_Key
    GROUP BY p.Categoria
    ORDER BY TotalVendido DESC;
    """
    cur = con.cursor()
    cur.execute(query)
    return cur.fetchall()


def ventas_por_mes(con):
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


def ventas_por_periodo(con):
    query = """
    SELECT
        t.Anio,
        t.Mes,
        COUNT(h.VentaId) AS TotalTransacciones,
        SUM(h.TotalVenta) AS TotalVendido
    FROM Hecho_Ventas h
    JOIN Dim_tiempo t ON h.Tiempo_Key = t.Tiempo_Key
    GROUP BY t.Anio, t.Mes
    ORDER BY t.Anio, MIN(t.Tiempo_Key);
    """
    cur = con.cursor()
    cur.execute(query)
    return cur.fetchall()


def ranking_ciudad_genero(con):
    query = """
    SELECT
        c.Ciudad,
        c.Genero,
        SUM(h.TotalVenta) AS TotalVendido,
        COUNT(h.VentaId) AS TotalTransacciones
    FROM Hecho_Ventas h
    JOIN Dim_cliente c ON h.Cliente_Key = c.Cliente_Key
    GROUP BY c.Ciudad, c.Genero
    ORDER BY TotalVendido DESC;
    """
    cur = con.cursor()
    cur.execute(query)
    return cur.fetchall()


def mejor_cliente(con):
    query = """
    SELECT
        c.NombreCompleto,
        c.Ciudad,
        c.Segmento,
        SUM(h.TotalVenta) AS TotalComprado,
        SUM(h.Cantidad) AS TotalUnidades
    FROM Hecho_Ventas h
    JOIN Dim_cliente c ON h.Cliente_Key = c.Cliente_Key
    GROUP BY c.Cliente_Key, c.NombreCompleto, c.Ciudad, c.Segmento
    ORDER BY TotalComprado DESC
    LIMIT 1;
    """
    cur = con.cursor()
    cur.execute(query)
    return cur.fetchall()


def imprimir_resultados(titulo, filas, encabezados):
    print(f"\n{titulo}")
    print("-" * len(titulo))
    print(" | ".join(encabezados))
    print("-" * 90)
    for fila in filas:
        print(" | ".join(str(x) for x in fila))


def main():
    con = conectar_db()
    try:
        res_a = ranking_ventas_categoria(con)
        res_b = ventas_por_mes(con)
        res_c = ventas_por_periodo(con)
        res_d = ranking_ciudad_genero(con)
        res_e = mejor_cliente(con)

        imprimir_resultados(
            "A) Ranking de ventas por categoría de producto",
            res_a,
            ["Categoria", "TotalVendido", "UnidadesVendidas"]
        )

        imprimir_resultados(
            "B) Ventas por mes",
            res_b,
            ["Anio", "Mes", "VentaMensual"]
        )

        imprimir_resultados(
            "C) Ventas por periodo (anio y mes)",
            res_c,
            ["Anio", "Mes", "TotalTransacciones", "TotalVendido"]
        )

        imprimir_resultados(
            "D) Ranking de ventas totales por ciudad y genero",
            res_d,
            ["Ciudad", "Genero", "TotalVendido", "TotalTransacciones"]
        )

        imprimir_resultados(
            "E) Mejor cliente",
            res_e,
            ["NombreCompleto", "Ciudad", "Segmento", "TotalComprado", "TotalUnidades"]
        )
    finally:
        con.close()


if __name__ == "__main__":
    main()
