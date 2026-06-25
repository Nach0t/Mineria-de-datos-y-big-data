import numpy as np
import pandas as pd

# =========================================================
# PARTE 1: NUMPY
# =========================================================

print("\n" + "=" * 60)
print("PARTE 1: NUMPY")
print("=" * 60)

# ---------------------------------------------------------
# Ejercicio 1: Shape y transformación de arreglos
# ---------------------------------------------------------
print("\nEJERCICIO 1: Shape y transformación de arreglos")
arr1 = np.arange(1, 21)

print("Arreglo original:")
print(arr1)

print("Shape:", arr1.shape)
print("Dtype:", arr1.dtype)

matriz_4x5 = arr1.reshape(4, 5)
print("\nMatriz 4x5:")
print(matriz_4x5)

segunda_fila = matriz_4x5[1]
tercera_columna = matriz_4x5[:, 2]

print("\nSegunda fila:")
print(segunda_fila)

print("\nTercera columna:")
print(tercera_columna)


# ---------------------------------------------------------
# Ejercicio 2: Manipulación de datos
# ---------------------------------------------------------
print("\n" + "-" * 60)
print("EJERCICIO 2: Manipulación de datos")

arr2 = np.array([5, 10, 15, 20, 25, 30])
print("Arreglo original:", arr2)

multiplicado = arr2 * 3
print("Multiplicado por 3:", multiplicado)

reemplazado = np.where(multiplicado > 20, -1, multiplicado)
print("Valores > 20 reemplazados por -1:", reemplazado)

filtrados = reemplazado[reemplazado > 0]
print("Valores positivos resultantes:", filtrados)


# ---------------------------------------------------------
# Ejercicio 3: Matrices y operaciones
# ---------------------------------------------------------
print("\n" + "-" * 60)
print("EJERCICIO 3: Matrices y operaciones")

matriz_a = np.array([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
])

matriz_b = np.array([
    [9, 8, 7],
    [6, 5, 4],
    [3, 2, 1]
])

print("Matriz A:")
print(matriz_a)

print("\nMatriz B:")
print(matriz_b)

suma_matrices = matriz_a + matriz_b
producto_elemento = matriz_a * matriz_b
suma_total_a = matriz_a.sum()
suma_total_b = matriz_b.sum()

print("\nSuma entre matrices:")
print(suma_matrices)

print("\nMultiplicación elemento a elemento:")
print(producto_elemento)

print("\nSuma total matriz A:", suma_total_a)
print("Suma total matriz B:", suma_total_b)


# ---------------------------------------------------------
# Ejercicio 4: Estadística básica
# ---------------------------------------------------------
print("\n" + "-" * 60)
print("EJERCICIO 4: Estadística básica")

np.random.seed(42)  # para que siempre salga lo mismo
arr4 = np.random.randint(1, 50, size=10)

print("Arreglo aleatorio:")
print(arr4)

promedio_arr4 = arr4.mean()
max_arr4 = arr4.max()
min_arr4 = arr4.min()
ordenado_arr4 = np.sort(arr4)
mayores_promedio = np.sum(arr4 > promedio_arr4)

print("\nPromedio:", promedio_arr4)
print("Máximo:", max_arr4)
print("Mínimo:", min_arr4)
print("Ordenado de menor a mayor:", ordenado_arr4)
print("Cantidad de valores mayores al promedio:", mayores_promedio)


# ---------------------------------------------------------
# Ejercicio 5: Integración simple
# ---------------------------------------------------------
print("\n" + "-" * 60)
print("EJERCICIO 5: Integración simple")

matriz5 = np.random.randint(1, 101, size=(5, 4))
print("Matriz 5x4:")
print(matriz5)

promedios_fila = matriz5.mean(axis=1)
fila_mayor_promedio_idx = np.argmax(promedios_fila)
fila_mayor_promedio = matriz5[fila_mayor_promedio_idx]

print("\nPromedio por fila:")
print(promedios_fila)

print("\nÍndice de la fila con mayor promedio:", fila_mayor_promedio_idx)
print("Fila con mayor promedio:")
print(fila_mayor_promedio)


# =========================================================
# PARTE 2: PANDAS
# =========================================================

print("\n" + "=" * 60)
print("PARTE 2: PANDAS")
print("=" * 60)

# ---------------------------------------------------------
# Ejercicio 6: Creación y exploración
# ---------------------------------------------------------
print("\nEJERCICIO 6: Creación y exploración")

df = pd.DataFrame({
    "Nombre": ["Ana", "Luis", "Camila", "Pedro", "Sofía"],
    "Edad": [20, 22, 19, 23, 21],
    "Carrera": ["Informática", "Medicina", "Informática", "Derecho", "Medicina"]
})

print("DataFrame:")
print(df)

print("\nPrimeras filas:")
print(df.head())

print("\nTipos de datos:")
print(df.dtypes)

print("\nResumen estadístico:")
print(df.describe(include="all"))


# ---------------------------------------------------------
# Ejercicio 7: Agregar y modificar datos
# ---------------------------------------------------------
print("\n" + "-" * 60)
print("EJERCICIO 7: Agregar y modificar datos")

df["Promedio"] = [5.8, 4.2, 6.0, 3.9, 5.1]
df["Estado"] = np.where(df["Promedio"] >= 4, "Aprobado", "Reprobado")

aprobados = df[df["Estado"] == "Aprobado"]

print("DataFrame con Promedio y Estado:")
print(df)

print("\nSolo aprobados:")
print(aprobados)


# ---------------------------------------------------------
# Ejercicio 8: Agrupación y agregación
# ---------------------------------------------------------
print("\n" + "-" * 60)
print("EJERCICIO 8: Agrupación y agregación")

data = {
    "Carrera": ["Ing", "Ing", "Med", "Med", "Ing"],
    "Promedio": [5.0, 4.5, 6.0, 5.5, 3.8]
}

df8 = pd.DataFrame(data)
agrupado = df8.groupby("Carrera").agg(
    Promedio_Notas=("Promedio", "mean"),
    Cantidad_Estudiantes=("Promedio", "count")
)

print("DataFrame ejercicio 8:")
print(df8)

print("\nAgrupado por carrera:")
print(agrupado)


# ---------------------------------------------------------
# Ejercicio 9: Agregar filas y análisis
# ---------------------------------------------------------
print("\n" + "-" * 60)
print("EJERCICIO 9: Agregar filas y análisis")

nuevos_estudiantes = pd.DataFrame({
    "Nombre": ["Tomás", "Valentina"],
    "Edad": [24, 20],
    "Carrera": ["Informática", "Derecho"],
    "Promedio": [4.7, 6.3],
    "Estado": ["Aprobado", "Aprobado"]
})

df9 = pd.concat([df, nuevos_estudiantes], ignore_index=True)

promedio_general = df9["Promedio"].mean()
sobre_promedio = df9[df9["Promedio"] > promedio_general]

print("DataFrame con nuevos estudiantes:")
print(df9)

print("\nPromedio general:", promedio_general)

print("\nEstudiantes sobre el promedio general:")
print(sobre_promedio)


# ---------------------------------------------------------
# Ejercicio 10: Combinación de DataFrames
# ---------------------------------------------------------
print("\n" + "-" * 60)
print("EJERCICIO 10: Combinación de DataFrames")

df1 = pd.DataFrame({
    "ID": [1, 2, 3, 4],
    "Nombre": ["Ana", "Luis", "Camila", "Pedro"]
})

df2 = pd.DataFrame({
    "ID": [1, 2, 4, 5],
    "Carrera": ["Informática", "Medicina", "Derecho", "Arquitectura"]
})

merge_df = pd.merge(df1, df2, on="ID", how="outer", indicator=True)

sin_coincidencia = merge_df[merge_df["_merge"] != "both"]

print("DF1:")
print(df1)

print("\nDF2:")
print(df2)

print("\nMerge:")
print(merge_df)

print("\nIDs sin coincidencia:")
print(sin_coincidencia)
