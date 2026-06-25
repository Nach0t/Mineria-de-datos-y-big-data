import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from mlxtend.frequent_patterns import apriori, association_rules

# =========================================================
# ACTIVIDAD 7 UNIDAD 2
# Dataset: ventas.csv
# Si ventas.csv no existe, se genera automáticamente.
# =========================================================

def generar_csv_ventas(nombre_archivo="ventas.csv", n=1000):
    np.random.seed(42)

    data = {
        "ID": range(1, n + 1),
        "Edad": np.random.randint(18, 66, n),
        "Ciudad": np.random.choice(["Santiago", "Valparaíso", "Concepción", "Puerto Montt"], n),
        "Producto": np.random.choice(["Laptop", "Smartphone", "Tablet", "Accesorio"], n),
        "Precio": np.random.randint(50, 2001, n),
        "Cantidad": np.random.randint(1, 6, n),
        "FechaCompra": pd.date_range("2022-01-01", "2024-12-31").to_series().sample(n, replace=True).values,
        "MétodoPago": np.random.choice(["Tarjeta", "Transferencia", "Efectivo"], n)
    }

    df = pd.DataFrame(data)
    df.to_csv(nombre_archivo, index=False)
    print(f"Archivo {nombre_archivo} generado correctamente.")
    return df

def cargar_o_generar_ventas(nombre_archivo="ventas.csv"):
    try:
        df = pd.read_csv(nombre_archivo)
        print(f"Archivo {nombre_archivo} cargado correctamente.")
    except FileNotFoundError:
        print(f"No se encontró {nombre_archivo}. Se generará automáticamente.")
        df = generar_csv_ventas(nombre_archivo)
    return df

def exploracion_inicial(df):
    print("\n===== EXPLORACIÓN INICIAL =====")
    print(df.head(10))
    print("\nRegistros por ciudad:")
    print(df["Ciudad"].value_counts())

def estadisticas_descriptivas(df):
    print("\n===== ESTADÍSTICAS DESCRIPTIVAS =====")
    print("\nPromedio de precios por producto:")
    print(df.groupby("Producto")["Precio"].mean())

    print("\nDesviación estándar de las edades:")
    print(df["Edad"].std())

    producto_mas_vendido = df.groupby("Producto")["Cantidad"].sum().idxmax()
    print("\nProducto más vendido en cantidad:")
    print(producto_mas_vendido)

def visualizaciones(df):
    print("\n===== GENERANDO GRÁFICOS =====")

    plt.figure(figsize=(8, 5))
    plt.hist(df["Precio"], bins=20)
    plt.title("Histograma de precios")
    plt.xlabel("Precio")
    plt.ylabel("Frecuencia")
    plt.tight_layout()
    plt.savefig("histograma_precios.png")
    plt.close()

    ventas_ciudad = df.groupby("Ciudad")["Cantidad"].sum()
    plt.figure(figsize=(8, 5))
    ventas_ciudad.plot(kind="bar")
    plt.title("Ventas por ciudad")
    plt.xlabel("Ciudad")
    plt.ylabel("Cantidad vendida")
    plt.tight_layout()
    plt.savefig("barras_ventas_ciudad.png")
    plt.close()

    plt.figure(figsize=(8, 5))
    plt.scatter(df["Precio"], df["Cantidad"])
    plt.title("Precio vs Cantidad")
    plt.xlabel("Precio")
    plt.ylabel("Cantidad")
    plt.tight_layout()
    plt.savefig("scatter_precio_cantidad.png")
    plt.close()

def uso_numpy(df):
    print("\n===== NUMPY =====")
    precios = df["Precio"].to_numpy()

    precios_normalizados = (precios - precios.min()) / (precios.max() - precios.min())
    percentiles = np.percentile(precios, [25, 50, 75])

    print("Primeros 10 precios como array NumPy:")
    print(precios[:10])

    print("\nPrimeros 10 precios normalizados:")
    print(precios_normalizados[:10])

    print("\nPercentiles 25, 50, 75:")
    print(percentiles)

def ejecutar_apriori(df):
    print("\n===== APRIORI =====")
    # Matriz binaria por ticket (ID) y producto
    transacciones = pd.crosstab(df["ID"], df["Producto"])
    transacciones = (transacciones > 0).astype(int)

    frecuentes = apriori(transacciones, min_support=0.05, use_colnames=True)
    reglas = association_rules(frecuentes, metric="confidence", min_threshold=0.6)
    reglas = reglas[["antecedents", "consequents", "support", "confidence", "lift"]]

    print("\nItemsets frecuentes:")
    print(frecuentes.head(20))

    print("\nReglas de asociación (support > 0.05, confidence > 0.6):")
    print(reglas.head(20))

    frecuentes.to_csv("itemsets_frecuentes_ventas.csv", index=False)
    reglas.to_csv("reglas_asociacion_ventas.csv", index=False)

def ejecutar_kmeans(df):
    print("\n===== KMEANS =====")
    X = df[["Edad", "Precio", "Cantidad"]]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    df["Cluster"] = kmeans.fit_predict(X_scaled)

    print(df[["ID", "Edad", "Precio", "Cantidad", "Cluster"]].head(20))

    plt.figure(figsize=(8, 5))
    plt.scatter(df["Edad"], df["Precio"], c=df["Cluster"], s=20)
    plt.title("Clusters de clientes (Edad vs Precio)")
    plt.xlabel("Edad")
    plt.ylabel("Precio")
    plt.tight_layout()
    plt.savefig("clusters_ventas.png")
    plt.close()

    df.to_csv("ventas_clusterizadas.csv", index=False)

    print("\nInterpretación de clusters:")
    resumen = df.groupby("Cluster")[["Edad", "Precio", "Cantidad"]].mean()
    print(resumen)

def main():
    df = cargar_o_generar_ventas("ventas.csv")
    exploracion_inicial(df)
    estadisticas_descriptivas(df)
    visualizaciones(df)
    uso_numpy(df)
    ejecutar_apriori(df)
    ejecutar_kmeans(df)
    print("\nActividad 7 completada.")

if __name__ == "__main__":
    main()
