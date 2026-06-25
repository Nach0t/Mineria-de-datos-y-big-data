import pandas as pd

df = pd.read_csv("alumnos.csv")
df = df.drop_duplicates()
df["Edad"] = pd.to_numeric(df["Edad"], errors="coerce")
df["Promedio"] = pd.to_numeric(df["Promedio"], errors="coerce")

columnas_texto = ["RUT", "Nombre", "Apellido_Paterno", "Apellido_Materno", "Sexo", "Ciudad"]
for col in columnas_texto:
    df[col] = df[col].astype(str).str.strip()
    df[col] = df[col].replace("nan", pd.NA)

df["Nombre_Completo"] = (
    df["Nombre"].fillna("") + " " +
    df["Apellido_Paterno"].fillna("") + " " +
    df["Apellido_Materno"].fillna("")
).str.replace(r"\s+", " ", regex=True).str.strip()

df["Promedio"] = df["Promedio"].interpolate()

alumnos_puerto_montt = df[(df["Edad"] > 20) & (df["Ciudad"].str.lower() == "puerto montt")]
alumnas = df[df["Sexo"].str.upper() == "F"]
cantidad_quellon = df[df["Ciudad"].str.lower() == "quellón"].shape[0]
alumnas_catalina_sara = df[
    (df["Sexo"].str.upper() == "F") &
    (df["Nombre"].str.lower().isin(["catalina", "sara"]))
]
ciudad_p = df[df["Ciudad"].str.upper().str.startswith("P", na=False)]

usuarios_completos = df.dropna()
usuarios_incompletos = df[df.isna().any(axis=1)]

print("\n==============================")
print("DATAFRAME LIMPIO")
print("==============================")
print(df)

print("\n==============================")
print("PREGUNTA A")
print("Alumnos mayores de 20 años de Puerto Montt")
print("==============================")
print(alumnos_puerto_montt[["RUT", "Nombre_Completo", "Edad", "Ciudad", "Promedio"]])

print("\n==============================")
print("PREGUNTA B")
print("Listado de alumnos de sexo femenino")
print("==============================")
print(alumnas[["RUT", "Nombre_Completo", "Sexo", "Ciudad", "Promedio"]])

print("\n==============================")
print("PREGUNTA C")
print("Cantidad de alumnos de Quellón")
print("==============================")
print("Cantidad:", cantidad_quellon)

print("\n==============================")
print("PREGUNTA D")
print("Promedios con interpolación aplicada")
print("==============================")
print(df[["RUT", "Nombre_Completo", "Promedio"]])

print("\n==============================")
print("PREGUNTA E")
print("Alumnas de nombre Catalina o Sara")
print("==============================")
print(alumnas_catalina_sara[["RUT", "Nombre_Completo", "Sexo", "Ciudad", "Promedio"]])

print("\n==============================")
print("PREGUNTA F")
print("Alumnos cuya ciudad comienza con la letra P")
print("==============================")
print(ciudad_p[["RUT", "Nombre_Completo", "Ciudad", "Promedio"]])

print("\n==============================")
print("REGISTROS COMPLETOS")
print("==============================")
print(usuarios_completos)

print("\n==============================")
print("REGISTROS INCOMPLETOS")
print("==============================")
print(usuarios_incompletos)

df[["RUT", "Nombre", "Apellido_Paterno", "Apellido_Materno", "Sexo", "Edad", "Ciudad", "Promedio"]].to_csv("alumnos_limpio.csv", index=False)
alumnos_puerto_montt[["RUT", "Nombre_Completo", "Edad", "Ciudad", "Promedio"]].to_csv("puerto_montt_mayores20.csv", index=False)
alumnas[["RUT", "Nombre_Completo", "Sexo", "Ciudad", "Promedio"]].to_csv("alumnas.csv", index=False)
df[["RUT", "Nombre_Completo", "Promedio"]].to_csv("promedios_interpolados.csv", index=False)
alumnas_catalina_sara[["RUT", "Nombre_Completo", "Sexo", "Ciudad", "Promedio"]].to_csv("catalina_sara.csv", index=False)
ciudad_p[["RUT", "Nombre_Completo", "Ciudad", "Promedio"]].to_csv("ciudad_p.csv", index=False)
usuarios_completos.to_csv("completos.csv", index=False)
usuarios_incompletos.to_csv("incompletos.csv", index=False)

print("\nArchivos generados correctamente:")
print("- alumnos_limpio.csv")
print("- puerto_montt_mayores20.csv")
print("- alumnas.csv")
print("- promedios_interpolados.csv")
print("- catalina_sara.csv")
print("- ciudad_p.csv")
print("- completos.csv")
print("- incompletos.csv")
print(f"- Cantidad de alumnos de Quellón: {cantidad_quellon}")
