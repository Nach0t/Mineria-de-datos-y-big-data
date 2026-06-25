import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from mlxtend.frequent_patterns import apriori, association_rules

# =========================================================
# ACTIVIDAD 8 UNIDAD 2
# Dataset: estudiantes.csv
# Si estudiantes.csv no existe, se genera automáticamente.
# =========================================================

def generar_csv_estudiantes(nombre_archivo="estudiantes.csv", n=1000):
    np.random.seed(12)

    data = {
        "ID": range(1, n + 1),
        "Carrera": np.random.choice(["Informática", "Ingeniería", "Medicina", "Derecho", "Arquitectura"], n),
        "Edad": np.random.randint(18, 31, n),
        "PromedioNotas": np.round(np.random.uniform(3.5, 7.0, n), 2),
        "HorasEstudioSemanal": np.random.randint(0, 41, n),
        "Asistencia": np.random.randint(50, 101, n),
        "Ciudad": np.random.choice(["Santiago", "Valparaíso", "Concepción", "Puerto Montt"], n),
        "Beca": np.random.choice(["Sí", "No"], n, p=[0.3, 0.7])
    }

    df = pd.DataFrame(data)
    df.to_csv(nombre_archivo, index=False)
    print(f"Archivo {nombre_archivo} generado correctamente.")
    return df

def cargar_o_generar_estudiantes(nombre_archivo="estudiantes.csv"):
    try:
        df = pd.read_csv(nombre_archivo)
        print(f"Archivo {nombre_archivo} cargado correctamente.")
    except FileNotFoundError:
        print(f"No se encontró {nombre_archivo}. Se generará automáticamente.")
        df = generar_csv_estudiantes(nombre_archivo)
    return df

def exploracion_inicial(df):
    print("\n===== EXPLORACIÓN INICIAL =====")
    print(df.head())
    print("\nCantidad de estudiantes por carrera:")
    print(df["Carrera"].value_counts())

def estadisticas(df):
    print("\n===== ESTADÍSTICAS =====")
    print("\nPromedio de notas por carrera:")
    print(df.groupby("Carrera")["PromedioNotas"].mean())

    print("\nMedia de horas de estudio semanal:")
    print(df["HorasEstudioSemanal"].mean())

    porcentaje_beca = (df["Beca"].value_counts(normalize=True) * 100).round(2)
    print("\nPorcentaje de estudiantes con beca:")
    print(porcentaje_beca)

    print("\nCantidad de alumnos por ciudad:")
    print(df["Ciudad"].value_counts())

def visualizaciones(df):
    print("\n===== GENERANDO GRÁFICOS =====")

    plt.figure(figsize=(8, 5))
    plt.hist(df["HorasEstudioSemanal"], bins=15)
    plt.title("Histograma de horas de estudio")
    plt.xlabel("Horas de estudio semanal")
    plt.ylabel("Frecuencia")
    plt.tight_layout()
    plt.savefig("histograma_horas_estudio.png")
    plt.close()

    promedio_ciudad = df.groupby("Ciudad")["PromedioNotas"].mean()
    plt.figure(figsize=(8, 5))
    promedio_ciudad.plot(kind="bar")
    plt.title("Promedio de notas por ciudad")
    plt.xlabel("Ciudad")
    plt.ylabel("Promedio de notas")
    plt.tight_layout()
    plt.savefig("barras_promedio_ciudad.png")
    plt.close()

    plt.figure(figsize=(8, 5))
    plt.scatter(df["HorasEstudioSemanal"], df["PromedioNotas"])
    plt.title("Horas de estudio vs Promedio de notas")
    plt.xlabel("Horas de estudio semanal")
    plt.ylabel("Promedio de notas")
    plt.tight_layout()
    plt.savefig("scatter_horas_promedio.png")
    plt.close()

def uso_numpy(df):
    print("\n===== NUMPY =====")
    asistencia = df["Asistencia"].to_numpy()
    horas = df["HorasEstudioSemanal"].to_numpy()

    percentiles_asistencia = np.percentile(asistencia, [25, 50, 75])
    horas_normalizadas = (horas - horas.min()) / (horas.max() - horas.min())

    print("Percentiles de asistencia (25, 50, 75):")
    print(percentiles_asistencia)

    print("\nPrimeras 10 horas de estudio normalizadas:")
    print(horas_normalizadas[:10])

def ejecutar_apriori(df):
    print("\n===== APRIORI =====")
    # Reglas entre Carrera y Beca
    transacciones = pd.get_dummies(df[["Carrera", "Beca"]].astype(str))
    frecuentes = apriori(transacciones, min_support=0.05, use_colnames=True)
    reglas = association_rules(frecuentes, metric="confidence", min_threshold=0.3)
    reglas = reglas[["antecedents", "consequents", "support", "confidence", "lift"]]

    print("\nItemsets frecuentes:")
    print(frecuentes.head(20))

    print("\nReglas de asociación entre carrera y beca:")
    print(reglas.head(20))

    frecuentes.to_csv("itemsets_frecuentes_estudiantes.csv", index=False)
    reglas.to_csv("reglas_asociacion_estudiantes.csv", index=False)

def ejecutar_kmeans(df):
    print("\n===== KMEANS =====")
    X = df[["Edad", "PromedioNotas", "HorasEstudioSemanal"]]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    df["Cluster"] = kmeans.fit_predict(X_scaled)

    print(df[["ID", "Edad", "PromedioNotas", "HorasEstudioSemanal", "Cluster"]].head(20))

    plt.figure(figsize=(8, 5))
    plt.scatter(df["HorasEstudioSemanal"], df["PromedioNotas"], c=df["Cluster"], s=20)
    plt.title("Clusters de estudiantes")
    plt.xlabel("Horas de estudio semanal")
    plt.ylabel("Promedio de notas")
    plt.tight_layout()
    plt.savefig("clusters_estudiantes.png")
    plt.close()

    df.to_csv("estudiantes_clusterizados.csv", index=False)

    print("\nInterpretación de clusters:")
    resumen = df.groupby("Cluster")[["Edad", "PromedioNotas", "HorasEstudioSemanal"]].mean()
    print(resumen)

def main():
    df = cargar_o_generar_estudiantes("estudiantes.csv")
    exploracion_inicial(df)
    estadisticas(df)
    visualizaciones(df)
    uso_numpy(df)
    ejecutar_apriori(df)
    ejecutar_kmeans(df)
    print("\nActividad 8 completada.")

if __name__ == "__main__":
    main()
