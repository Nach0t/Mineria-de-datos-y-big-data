-- =========================================
-- ACTIVIDAD 2A - DATA WAREHOUSE TIENDA DE ELECTRÓNICA
-- SQLITE3
-- =========================================

PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS Hecho_Ventas;
DROP TABLE IF EXISTS Dim_producto;
DROP TABLE IF EXISTS Dim_tiempo;

CREATE TABLE Dim_producto (
    Producto_Key INTEGER PRIMARY KEY,
    Nombre TEXT NOT NULL,
    Categoria TEXT NOT NULL,
    PrecioUnitario REAL NOT NULL
);

CREATE TABLE Dim_tiempo (
    Tiempo_Key INTEGER PRIMARY KEY,
    Fecha TEXT NOT NULL,
    Anio INTEGER NOT NULL,
    Mes TEXT NOT NULL,
    Trimestre INTEGER NOT NULL,
    Semestre INTEGER NOT NULL
);

CREATE TABLE Hecho_Ventas (
    VentaId INTEGER PRIMARY KEY,
    Producto_Key INTEGER NOT NULL,
    Tiempo_Key INTEGER NOT NULL,
    Cantidad INTEGER NOT NULL,
    TotalVenta REAL NOT NULL,
    FOREIGN KEY (Producto_Key) REFERENCES Dim_producto(Producto_Key),
    FOREIGN KEY (Tiempo_Key) REFERENCES Dim_tiempo(Tiempo_Key)
);

INSERT INTO Dim_producto (Producto_Key, Nombre, Categoria, PrecioUnitario) VALUES
(1, 'iPhone 15', 'Telefonia', 900.00),
(2, 'Samsung Galaxy S24', 'Telefonia', 850.00),
(3, 'MacBook Air M2', 'Computacion', 1100.00),
(4, 'Dell XPS 13', 'Computacion', 1000.00),
(5, 'Monitor LG 27"', 'Accesorios', 300.00),
(6, 'Teclado Mecanico RGB', 'Accesorios', 80.00);

INSERT INTO Dim_tiempo (Tiempo_Key, Fecha, Anio, Mes, Trimestre, Semestre) VALUES
(20240115, '2024-01-15', 2024, 'Enero', 1, 1),
(20240210, '2024-02-10', 2024, 'Febrero', 1, 1),
(20240320, '2024-03-20', 2024, 'Marzo', 1, 1),
(20240405, '2024-04-05', 2024, 'Abril', 2, 1),
(20240518, '2024-05-18', 2024, 'Mayo', 2, 1),
(20240622, '2024-06-22', 2024, 'Junio', 2, 1);

INSERT INTO Hecho_Ventas (VentaId, Producto_Key, Tiempo_Key, Cantidad, TotalVenta) VALUES
(1, 1, 20240115, 1, 900.00),
(2, 3, 20240115, 2, 2200.00),
(3, 5, 20240210, 5, 1500.00),
(4, 2, 20240210, 1, 850.00),
(5, 6, 20240320, 10, 800.00),
(6, 4, 20240320, 1, 1000.00),
(7, 1, 20240405, 2, 1800.00),
(8, 5, 20240405, 3, 900.00),
(9, 2, 20240518, 2, 1700.00),
(10, 3, 20240622, 1, 1100.00);
