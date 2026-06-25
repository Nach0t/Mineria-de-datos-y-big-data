-- =========================================
-- ACTIVIDAD DATA WAREHOUSE - CADENA DE CINES
-- Versión SQLite3
-- =========================================

PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS Hechos_Ventas;
DROP TABLE IF EXISTS Dim_Pelicula;
DROP TABLE IF EXISTS Dim_Sucursal;
DROP TABLE IF EXISTS Dim_Tiempo;

CREATE TABLE Dim_Pelicula (
    ID_Pelicula INTEGER PRIMARY KEY,
    Titulo TEXT NOT NULL,
    Genero TEXT NOT NULL,
    Clasificacion TEXT
);

CREATE TABLE Dim_Sucursal (
    ID_Sucursal INTEGER PRIMARY KEY,
    Nombre_Cine TEXT NOT NULL,
    Ciudad TEXT NOT NULL,
    Pais TEXT NOT NULL
);

CREATE TABLE Dim_Tiempo (
    ID_Tiempo INTEGER PRIMARY KEY,
    Fecha TEXT NOT NULL,
    Dia INTEGER NOT NULL,
    Mes INTEGER NOT NULL,
    Anio INTEGER NOT NULL,
    Trimestre INTEGER NOT NULL
);

CREATE TABLE Hechos_Ventas (
    ID_Venta INTEGER PRIMARY KEY,
    FK_Pelicula INTEGER NOT NULL,
    FK_Sucursal INTEGER NOT NULL,
    FK_Tiempo INTEGER NOT NULL,
    Cantidad_Tickets INTEGER NOT NULL,
    Monto_Total REAL NOT NULL,

    FOREIGN KEY (FK_Pelicula) REFERENCES Dim_Pelicula(ID_Pelicula),
    FOREIGN KEY (FK_Sucursal) REFERENCES Dim_Sucursal(ID_Sucursal),
    FOREIGN KEY (FK_Tiempo) REFERENCES Dim_Tiempo(ID_Tiempo)
);

INSERT INTO Dim_Pelicula (ID_Pelicula, Titulo, Genero, Clasificacion) VALUES
(1, 'The Batman', 'Accion', 'R'),
(2, 'Avengers: Endgame', 'Accion', 'PG-13'),
(3, 'Toy Story 4', 'Animacion', 'G'),
(4, 'Interstellar', 'Ciencia Ficcion', 'PG-13');

INSERT INTO Dim_Sucursal (ID_Sucursal, Nombre_Cine, Ciudad, Pais) VALUES
(1, 'Cinepolis Central', 'Punta Arenas', 'Chile'),
(2, 'Cinemark Costanera', 'Santiago', 'Chile'),
(3, 'Cineplanet Mall', 'Puerto Montt', 'Chile');

INSERT INTO Dim_Tiempo (ID_Tiempo, Fecha, Dia, Mes, Anio, Trimestre) VALUES
(1, '2025-05-15', 15, 5, 2025, 2),
(2, '2025-06-10', 10, 6, 2025, 2),
(3, '2025-07-01', 1, 7, 2025, 3),
(4, '2025-07-20', 20, 7, 2025, 3);

INSERT INTO Hechos_Ventas (ID_Venta, FK_Pelicula, FK_Sucursal, FK_Tiempo, Cantidad_Tickets, Monto_Total) VALUES
(1001, 1, 1, 1, 2, 7500),
(1002, 2, 2, 2, 3, 15000),
(1003, 3, 3, 3, 4, 12000),
(1004, 1, 2, 4, 1, 4000),
(1005, 4, 1, 3, 2, 9000);

-- Consulta principal
SELECT
    P.Genero,
    S.Ciudad,
    SUM(V.Monto_Total) AS Ingresos_Totales
FROM Hechos_Ventas V
JOIN Dim_Pelicula P ON V.FK_Pelicula = P.ID_Pelicula
JOIN Dim_Sucursal S ON V.FK_Sucursal = S.ID_Sucursal
GROUP BY P.Genero, S.Ciudad
ORDER BY S.Ciudad, P.Genero;

-- Consulta extra 1: Total vendido por película
SELECT
    P.Titulo,
    SUM(V.Cantidad_Tickets) AS Total_Tickets,
    SUM(V.Monto_Total) AS Total_Recaudado
FROM Hechos_Ventas V
JOIN Dim_Pelicula P ON V.FK_Pelicula = P.ID_Pelicula
GROUP BY P.Titulo
ORDER BY Total_Recaudado DESC;

-- Consulta extra 2: Total vendido por sucursal
SELECT
    S.Nombre_Cine,
    S.Ciudad,
    SUM(V.Monto_Total) AS Total_Recaudado
FROM Hechos_Ventas V
JOIN Dim_Sucursal S ON V.FK_Sucursal = S.ID_Sucursal
GROUP BY S.Nombre_Cine, S.Ciudad
ORDER BY Total_Recaudado DESC;

-- Consulta extra 3: Total vendido por trimestre
SELECT
    T.Anio,
    T.Trimestre,
    SUM(V.Monto_Total) AS Total_Recaudado
FROM Hechos_Ventas V
JOIN Dim_Tiempo T ON V.FK_Tiempo = T.ID_Tiempo
GROUP BY T.Anio, T.Trimestre
ORDER BY T.Anio, T.Trimestre;
