import pandas as pd

# =========================
# 1. CARGAR CSV BASE
# =========================
df = pd.read_csv("trabajadores.csv")

# =========================
# 2. LIMPIEZA / PREPARACIÓN DE DATOS
# =========================

# Eliminar duplicados exactos
df = df.drop_duplicates()

# Limpiar columna sueldo:
# "$1.200.000" -> 1200000
df["Sueldo"] = (
    df["Sueldo"]
    .astype(str)
    .str.replace("$", "", regex=False)
    .str.replace(".", "", regex=False)
    .str.strip()
)

# Convertir sueldo a numérico
df["Sueldo"] = pd.to_numeric(df["Sueldo"], errors="coerce")

# Convertir edad a numérico por seguridad
df["Edad"] = pd.to_numeric(df["Edad"], errors="coerce")

# Limpiar espacios en columnas de texto
columnas_texto = ["RUT", "Nombre", "Apellido_Paterno", "Apellido_Materno"]
for col in columnas_texto:
    df[col] = df[col].astype(str).str.strip()
    df[col] = df[col].replace("nan", pd.NA)

# =========================
# 3. CREAR NOMBRE COMPLETO
#    (Pregunta b)
# =========================
df["Nombre_Completo"] = (
    df["Nombre"].fillna("") + " " +
    df["Apellido_Paterno"].fillna("") + " " +
    df["Apellido_Materno"].fillna("")
).str.replace(r"\s+", " ", regex=True).str.strip()

# =========================
# 4. CALCULAR BONO 25%
#    (Pregunta c)
# =========================
df["Bono"] = (df["Sueldo"] * 0.25).round(0)

# =========================
# 5. PREGUNTA A
#    Personas mayores de 40 años
#    con sueldo mayor a $1.500.000
# =========================
sueldos_mayores = df[(df["Edad"] > 40) & (df["Sueldo"] > 1500000)]

# =========================
# 6. DATOS COMPLETOS / INCOMPLETOS
#    (parte de preparación de datos)
# =========================
usuarios_completos = df.dropna()
usuarios_incompletos = df[df.isna().any(axis=1)]

# =========================
# 7. MOSTRAR RESPUESTAS EN CONSOLA
# =========================

print("\n==============================")
print("DATAFRAME LIMPIO")
print("==============================")
print(df)

print("\n==============================")
print("PREGUNTA A")
print("Personas mayores de 40 años con sueldo > $1.500.000")
print("==============================")
print(sueldos_mayores[["RUT", "Nombre_Completo", "Edad", "Sueldo"]])

print("\n==============================")
print("PREGUNTA B")
print("Listado del nombre completo de los trabajadores")
print("==============================")
print(df[["RUT", "Nombre_Completo"]])

print("\n==============================")
print("PREGUNTA C")
print("Bono del 25% para cada trabajador")
print("==============================")
print(df[["RUT", "Nombre_Completo", "Sueldo", "Bono"]])

print("\n==============================")
print("REGISTROS COMPLETOS")
print("==============================")
print(usuarios_completos)

print("\n==============================")
print("REGISTROS INCOMPLETOS")
print("==============================")
print(usuarios_incompletos)

# =========================
# 8. EXPORTAR CSV
# =========================

# CSV limpio general
df[[
    "RUT",
    "Nombre",
    "Apellido_Paterno",
    "Apellido_Materno",
    "Edad",
    "Sueldo"
]].to_csv("trabajadores_limpio.csv", index=False)

# Pregunta A
sueldos_mayores[[
    "RUT",
    "Nombre_Completo",
    "Edad",
    "Sueldo"
]].to_csv("sueldomayor.csv", index=False)

# Pregunta B
df[[
    "RUT",
    "Nombre_Completo"
]].to_csv("nombres_completos.csv", index=False)

# Pregunta C
df[[
    "RUT",
    "Nombre_Completo",
    "Sueldo",
    "Bono"
]].to_csv("bono.csv", index=False)

# Registros completos e incompletos
usuarios_completos.to_csv("completos.csv", index=False)
usuarios_incompletos.to_csv("incompletos.csv", index=False)

print("\nArchivos generados correctamente:")
print("- trabajadores_limpio.csv")
print("- sueldomayor.csv")
print("- nombres_completos.csv")
print("- bono.csv")
print("- completos.csv")
print("- incompletos.csv")