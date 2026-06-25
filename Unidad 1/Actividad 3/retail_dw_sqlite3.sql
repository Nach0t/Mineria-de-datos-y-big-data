-- =========================================
-- ACTIVIDAD 3 - DATA WAREHOUSE RETAIL
-- SQLITE3
-- =========================================

PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS Hecho_Ventas;
DROP TABLE IF EXISTS Dim_cliente;
DROP TABLE IF EXISTS Dim_producto;
DROP TABLE IF EXISTS Dim_tiempo;

-- =========================================
-- 1) TABLAS DE DIMENSIONES
-- =========================================

CREATE TABLE Dim_producto (
    Producto_Key INTEGER PRIMARY KEY,
    Nombre TEXT NOT NULL,
    Categoria TEXT NOT NULL,
    Precio REAL NOT NULL
);

CREATE TABLE Dim_tiempo (
    Tiempo_Key INTEGER PRIMARY KEY,   -- formato YYYYMMDD
    Fecha TEXT NOT NULL,
    Anio INTEGER NOT NULL,
    Mes TEXT NOT NULL,
    Trimestre INTEGER NOT NULL
);

CREATE TABLE Dim_cliente (
    Cliente_Key INTEGER PRIMARY KEY,
    NombreCompleto TEXT NOT NULL,
    Genero TEXT NOT NULL,
    Ciudad TEXT NOT NULL,
    Segmento TEXT NOT NULL
);

-- =========================================
-- 2) TABLA DE HECHOS
--    Ya viene modificada para incluir cliente
-- =========================================

CREATE TABLE Hecho_Ventas (
    VentaId INTEGER PRIMARY KEY,
    Producto_Key INTEGER NOT NULL,
    Tiempo_Key INTEGER NOT NULL,
    Cliente_Key INTEGER NOT NULL,
    Cantidad INTEGER NOT NULL,
    TotalVenta REAL NOT NULL,
    FOREIGN KEY (Producto_Key) REFERENCES Dim_producto(Producto_Key),
    FOREIGN KEY (Tiempo_Key) REFERENCES Dim_tiempo(Tiempo_Key),
    FOREIGN KEY (Cliente_Key) REFERENCES Dim_cliente(Cliente_Key)
);

-- =========================================
-- 3) CARGA DE DATOS
--    5+ registros en dimensiones y 10+ en hechos
-- =========================================

INSERT INTO Dim_producto (Producto_Key, Nombre, Categoria, Precio) VALUES
(1, 'Arroz 1kg', 'Alimentos', 1.80),
(2, 'Leche Entera 1L', 'Lacteos', 1.20),
(3, 'Detergente 3L', 'Limpieza', 6.50),
(4, 'Pan Integral', 'Panaderia', 2.10),
(5, 'Cereal Choco', 'Desayuno', 4.80),
(6, 'Aceite 1L', 'Despensa', 3.90);

INSERT INTO Dim_tiempo (Tiempo_Key, Fecha, Anio, Mes, Trimestre) VALUES
(20240105, '2024-01-05', 2024, 'Enero', 1),
(20240212, '2024-02-12', 2024, 'Febrero', 1),
(20240308, '2024-03-08', 2024, 'Marzo', 1),
(20240410, '2024-04-10', 2024, 'Abril', 2),
(20240518, '2024-05-18', 2024, 'Mayo', 2),
(20240622, '2024-06-22', 2024, 'Junio', 2);

INSERT INTO Dim_cliente (Cliente_Key, NombreCompleto, Genero, Ciudad, Segmento) VALUES
(1, 'Ana Torres', 'Femenino', 'Santiago', 'Premium'),
(2, 'Luis Perez', 'Masculino', 'Valparaiso', 'Regular'),
(3, 'Camila Soto', 'Femenino', 'Concepcion', 'Nuevo'),
(4, 'Diego Rojas', 'Masculino', 'Santiago', 'Premium'),
(5, 'Valentina Diaz', 'Femenino', 'Puerto Montt', 'Regular'),
(6, 'Martin Silva', 'Masculino', 'Temuco', 'Nuevo');

INSERT INTO Hecho_Ventas (VentaId, Producto_Key, Tiempo_Key, Cliente_Key, Cantidad, TotalVenta) VALUES
(1, 1, 20240105, 1, 5, 9.00),
(2, 2, 20240105, 2, 3, 3.60),
(3, 3, 20240212, 1, 2, 13.00),
(4, 4, 20240212, 3, 4, 8.40),
(5, 5, 20240308, 4, 2, 9.60),
(6, 6, 20240308, 5, 3, 11.70),
(7, 1, 20240410, 6, 10, 18.00),
(8, 3, 20240410, 2, 1, 6.50),
(9, 5, 20240518, 4, 5, 24.00),
(10, 2, 20240518, 1, 6, 7.20),
(11, 6, 20240622, 5, 2, 7.80),
(12, 4, 20240622, 3, 3, 6.30);

-- =========================================
-- 4) CONSULTAS PEDIDAS EN LA ACTIVIDAD
-- =========================================

-- A) Ranking de ventas por categoría de producto
SELECT
    p.Categoria,
    SUM(h.TotalVenta) AS TotalVendido,
    SUM(h.Cantidad) AS UnidadesVendidas
FROM Hecho_Ventas h
JOIN Dim_producto p ON h.Producto_Key = p.Producto_Key
GROUP BY p.Categoria
ORDER BY TotalVendido DESC;

-- B) Ventas por mes
SELECT
    t.Anio,
    t.Mes,
    SUM(h.TotalVenta) AS VentaMensual
FROM Hecho_Ventas h
JOIN Dim_tiempo t ON h.Tiempo_Key = t.Tiempo_Key
GROUP BY t.Anio, t.Mes
ORDER BY t.Anio, MIN(t.Tiempo_Key);

-- C) Ventas por periodo: año y mes
SELECT
    t.Anio,
    t.Mes,
    COUNT(h.VentaId) AS TotalTransacciones,
    SUM(h.TotalVenta) AS TotalVendido
FROM Hecho_Ventas h
JOIN Dim_tiempo t ON h.Tiempo_Key = t.Tiempo_Key
GROUP BY t.Anio, t.Mes
ORDER BY t.Anio, MIN(t.Tiempo_Key);

-- D) Ranking de ventas totales por ciudad y género
SELECT
    c.Ciudad,
    c.Genero,
    SUM(h.TotalVenta) AS TotalVendido,
    COUNT(h.VentaId) AS TotalTransacciones
FROM Hecho_Ventas h
JOIN Dim_cliente c ON h.Cliente_Key = c.Cliente_Key
GROUP BY c.Ciudad, c.Genero
ORDER BY TotalVendido DESC;

-- E) ¿Quién es mi mejor cliente?
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
