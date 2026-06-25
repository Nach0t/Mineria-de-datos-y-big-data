-- =========================================
-- ACTIVIDAD 3A - DATA WAREHOUSE HOSPITAL
-- SQLITE3
-- =========================================

PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS Hechos_Hospitalizaciones;
DROP TABLE IF EXISTS Dim_Paciente;
DROP TABLE IF EXISTS Dim_Doctor;
DROP TABLE IF EXISTS Dim_Diagnostico;
DROP TABLE IF EXISTS Dim_Tiempo;

-- =========================================
-- 1) TABLAS DE DIMENSIONES
-- =========================================

CREATE TABLE Dim_Paciente (
    Paciente_Key INTEGER PRIMARY KEY,
    Nombre TEXT NOT NULL,
    Edad INTEGER NOT NULL,
    Genero TEXT NOT NULL,
    Ciudad TEXT NOT NULL,
    TipoSeguro TEXT NOT NULL
);

CREATE TABLE Dim_Doctor (
    Doctor_Key INTEGER PRIMARY KEY,
    Nombre TEXT NOT NULL,
    Especialidad TEXT NOT NULL
);

CREATE TABLE Dim_Diagnostico (
    Diagnostico_Key INTEGER PRIMARY KEY,
    CodigoEnfermedad TEXT NOT NULL,
    Descripcion TEXT NOT NULL,
    Gravedad INTEGER NOT NULL -- 1 = grave, 0 = no grave
);

CREATE TABLE Dim_Tiempo (
    Tiempo_Key INTEGER PRIMARY KEY, -- formato YYYYMMDD
    Fecha TEXT NOT NULL,
    Mes INTEGER NOT NULL,
    Anio INTEGER NOT NULL
);

-- =========================================
-- 2) TABLA DE HECHOS
-- =========================================

CREATE TABLE Hechos_Hospitalizaciones (
    Hospitalizacion_Key INTEGER PRIMARY KEY,
    Paciente_Key INTEGER NOT NULL,
    Doctor_Key INTEGER NOT NULL,
    Diagnostico_Key INTEGER NOT NULL,
    Tiempo_Key INTEGER NOT NULL,
    DiasEstancia INTEGER NOT NULL,
    CostoTratamiento REAL NOT NULL,
    FOREIGN KEY (Paciente_Key) REFERENCES Dim_Paciente(Paciente_Key),
    FOREIGN KEY (Doctor_Key) REFERENCES Dim_Doctor(Doctor_Key),
    FOREIGN KEY (Diagnostico_Key) REFERENCES Dim_Diagnostico(Diagnostico_Key),
    FOREIGN KEY (Tiempo_Key) REFERENCES Dim_Tiempo(Tiempo_Key)
);

-- =========================================
-- 3) CARGA DE DATOS
-- =========================================

INSERT INTO Dim_Paciente (Paciente_Key, Nombre, Edad, Genero, Ciudad, TipoSeguro) VALUES
(1, 'Ana Torres', 12, 'Femenino', 'Santiago', 'Fonasa'),
(2, 'Luis Perez', 68, 'Masculino', 'Valparaiso', 'Isapre'),
(3, 'Camila Soto', 35, 'Femenino', 'Concepcion', 'Fonasa'),
(4, 'Diego Rojas', 72, 'Masculino', 'Santiago', 'Particular'),
(5, 'Valentina Diaz', 8, 'Femenino', 'Puerto Montt', 'Fonasa'),
(6, 'Martin Silva', 29, 'Masculino', 'Temuco', 'Isapre');

INSERT INTO Dim_Doctor (Doctor_Key, Nombre, Especialidad) VALUES
(1, 'Dra. Martinez', 'Pediatria'),
(2, 'Dr. Gonzalez', 'Cardiologia'),
(3, 'Dra. Herrera', 'Medicina Interna'),
(4, 'Dr. Fuentes', 'Neurologia'),
(5, 'Dra. Lopez', 'Geriatria');

INSERT INTO Dim_Diagnostico (Diagnostico_Key, CodigoEnfermedad, Descripcion, Gravedad) VALUES
(1, 'J10', 'Influenza', 0),
(2, 'I21', 'Infarto Agudo al Miocardio', 1),
(3, 'E11', 'Diabetes Mellitus Tipo 2', 0),
(4, 'J18', 'Neumonia', 1),
(5, 'G40', 'Epilepsia', 1),
(6, 'K29', 'Gastritis', 0);

INSERT INTO Dim_Tiempo (Tiempo_Key, Fecha, Mes, Anio) VALUES
(20240110, '2024-01-10', 1, 2024),
(20240215, '2024-02-15', 2, 2024),
(20240320, '2024-03-20', 3, 2024),
(20240418, '2024-04-18', 4, 2024),
(20240512, '2024-05-12', 5, 2024),
(20240625, '2024-06-25', 6, 2024),
(20240714, '2024-07-14', 7, 2024),
(20240822, '2024-08-22', 8, 2024),
(20240909, '2024-09-09', 9, 2024),
(20241030, '2024-10-30', 10, 2024),
(20241111, '2024-11-11', 11, 2024),
(20241205, '2024-12-05', 12, 2024);

INSERT INTO Hechos_Hospitalizaciones
(Hospitalizacion_Key, Paciente_Key, Doctor_Key, Diagnostico_Key, Tiempo_Key, DiasEstancia, CostoTratamiento)
VALUES
(1, 1, 1, 1, 20240110, 2, 180000),
(2, 2, 2, 2, 20240215, 8, 2500000),
(3, 3, 3, 6, 20240320, 3, 320000),
(4, 4, 5, 3, 20240418, 5, 600000),
(5, 5, 1, 4, 20240512, 6, 950000),
(6, 6, 4, 5, 20240625, 4, 1100000),
(7, 2, 5, 4, 20240714, 7, 1250000),
(8, 1, 1, 1, 20240822, 1, 120000),
(9, 4, 2, 2, 20240909, 9, 2750000),
(10, 3, 3, 3, 20241030, 2, 280000),
(11, 5, 1, 1, 20241111, 3, 210000),
(12, 6, 4, 5, 20241205, 5, 1350000);

-- =========================================
-- 4) CONSULTAS PEDIDAS EN LA ACTIVIDAD
-- =========================================

-- A. Especialidad más costosa y con más días de estancia
SELECT
    d.Especialidad,
    SUM(h.CostoTratamiento) AS CostoTotal,
    SUM(h.DiasEstancia) AS DiasTotales
FROM Hechos_Hospitalizaciones h
JOIN Dim_Doctor d ON h.Doctor_Key = d.Doctor_Key
GROUP BY d.Especialidad
ORDER BY CostoTotal DESC, DiasTotales DESC;

-- B. Qué se está atendiendo más: niños o adultos mayores
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

-- C. Qué doctor realiza más atenciones mensualmente
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

-- D. Qué género es el más atendido por gravedad
SELECT
    dg.Gravedad,
    p.Genero,
    COUNT(*) AS TotalAtenciones
FROM Hechos_Hospitalizaciones h
JOIN Dim_Paciente p ON h.Paciente_Key = p.Paciente_Key
JOIN Dim_Diagnostico dg ON h.Diagnostico_Key = dg.Diagnostico_Key
GROUP BY dg.Gravedad, p.Genero
ORDER BY dg.Gravedad DESC, TotalAtenciones DESC;

-- E. Qué enfermedad es la que más se atiende los primeros 6 meses
SELECT
    dg.Descripcion,
    COUNT(*) AS TotalAtenciones
FROM Hechos_Hospitalizaciones h
JOIN Dim_Diagnostico dg ON h.Diagnostico_Key = dg.Diagnostico_Key
JOIN Dim_Tiempo t ON h.Tiempo_Key = t.Tiempo_Key
WHERE t.Mes BETWEEN 1 AND 6
GROUP BY dg.Descripcion
ORDER BY TotalAtenciones DESC;

-- F. Costo total facturado por mes en el último año
SELECT
    t.Anio,
    t.Mes,
    SUM(h.CostoTratamiento) AS CostoTotalFacturado
FROM Hechos_Hospitalizaciones h
JOIN Dim_Tiempo t ON h.Tiempo_Key = t.Tiempo_Key
GROUP BY t.Anio, t.Mes
ORDER BY t.Anio, t.Mes;

-- G. Promedio de estancia por especialidad médica
SELECT
    d.Especialidad,
    AVG(h.DiasEstancia) AS PromedioDiasEstancia
FROM Hechos_Hospitalizaciones h
JOIN Dim_Doctor d ON h.Doctor_Key = d.Doctor_Key
GROUP BY d.Especialidad
ORDER BY PromedioDiasEstancia DESC;

-- H. Los 5 diagnósticos más comunes
SELECT
    dg.Descripcion,
    COUNT(*) AS TotalCasos
FROM Hechos_Hospitalizaciones h
JOIN Dim_Diagnostico dg ON h.Diagnostico_Key = dg.Diagnostico_Key
GROUP BY dg.Descripcion
ORDER BY TotalCasos DESC
LIMIT 5;
