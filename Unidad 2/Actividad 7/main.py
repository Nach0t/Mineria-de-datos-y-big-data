import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# =========================================================
# ACTIVIDAD K-MEANS - CLIENTES
# Usa el archivo clientes.csv entregado
# =========================================================

# 1) Cargar el CSV
df = pd.read_csv("clientes.csv")

print("\n==============================")
print("DATOS CARGADOS")
print("==============================")
print(df)

# 2) Explorar los datos
print("\n==============================")
print("EXPLORACIÓN")
print("==============================")
print("\nPrimeras filas:")
print(df.head())

print("\nInformación del DataFrame:")
df.info()

print("\nResumen estadístico:")
print(df.describe())

# 3) Seleccionar variables numéricas para clustering
X = df[["Edad", "Gasto_Mensual"]]

# 4) Normalizar variables
scaler = StandardScaler()
X_normalizado = scaler.fit_transform(X)

# 5) Aplicar K-Means con k = 3
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
clusters = kmeans.fit_predict(X_normalizado)

# 6) Asignar cluster a cada cliente
df["Cluster"] = clusters

print("\n==============================")
print("CLIENTES CON CLUSTER ASIGNADO")
print("==============================")
print(df)

# 7) Obtener centroides en escala original
centroides = scaler.inverse_transform(kmeans.cluster_centers_)

print("\n==============================")
print("CENTROIDES")
print("==============================")
for i, c in enumerate(centroides):
    print(f"Cluster {i}: Edad promedio = {c[0]:.2f}, Gasto promedio = {c[1]:.2f}")

# 8) Interpretación simple de clusters
print("\n==============================")
print("INTERPRETACIÓN")
print("==============================")
for i, c in enumerate(centroides):
    edad = c[0]
    gasto = c[1]

    if edad < 30 and gasto < 300:
        perfil = "clientes jóvenes con gasto bajo/medio"
    elif 30 <= edad < 50 and gasto < 700:
        perfil = "clientes adultos con gasto medio"
    else:
        perfil = "clientes mayores o de alto gasto"

    print(f"Cluster {i}: {perfil}")

# 9) Exportar resultados
df.to_csv("clientes_clusterizados.csv", index=False)

centroides_df = pd.DataFrame(
    centroides,
    columns=["Edad_Promedio", "Gasto_Mensual_Promedio"]
)
centroides_df.insert(0, "Cluster", range(len(centroides_df)))
centroides_df.to_csv("centroides.csv", index=False)

# 10) Visualización
plt.figure(figsize=(8, 5))
plt.scatter(df["Edad"], df["Gasto_Mensual"], c=df["Cluster"], s=100)
plt.scatter(
    centroides[:, 0],
    centroides[:, 1],
    marker="X",
    s=250
)
plt.xlabel("Edad")
plt.ylabel("Gasto_Mensual")
plt.title("Segmentación de clientes con K-Means")
plt.tight_layout()
plt.savefig("grafico_kmeans_clientes.png", dpi=300, bbox_inches="tight")
plt.close()

print("\nArchivos generados correctamente:")
print("- clientes_clusterizados.csv")
print("- centroides.csv")
print("- grafico_kmeans_clientes.png")
