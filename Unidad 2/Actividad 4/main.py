import numpy as np
import pandas as pd

# =========================================================
# ACTIVIDAD 4 UNIDAD 2 - CASO APLICADO
# TechSolutions SpA
# =========================================================

print("\n" + "=" * 70)
print("PARTE 1: PROCESAMIENTO NUMÉRICO (NUMPY)")
print("=" * 70)

# ---------------------------------------------------------
# Ejercicio 1: Estructura de datos
# ---------------------------------------------------------
print("\nEJERCICIO 1: Estructura de datos")

data = np.arange(10, 130, 10)
print("Arreglo original:")
print(data)

print("\nDimensión del arreglo:", data.ndim)
print("Shape del arreglo:", data.shape)
print("Tipo de dato:", data.dtype)

matriz = data.reshape(4, 3)
print("\nMatriz 4x3:")
print(matriz)

print("\nInterpretación posible de cada fila:")
print("- Fila 1: Equipo A")
print("- Fila 2: Equipo B")
print("- Fila 3: Equipo C")
print("- Fila 4: Equipo D")

# ---------------------------------------------------------
# Ejercicio 2: Análisis por equipo
# ---------------------------------------------------------
print("\n" + "-" * 70)
print("EJERCICIO 2: Análisis por equipo")

promedio_por_equipo = matriz.mean(axis=1)
promedio_general = matriz.mean()
mejor_equipo_idx = np.argmax(promedio_por_equipo)

print("Promedio por equipo:", promedio_por_equipo)
print("Promedio general:", promedio_general)
print(f"Equipo con mejor desempeño: Equipo {mejor_equipo_idx + 1} con promedio {promedio_por_equipo[mejor_equipo_idx]:.2f}")

# ---------------------------------------------------------
# Ejercicio 3: Filtrado de rendimiento
# ---------------------------------------------------------
print("\n" + "-" * 70)
print("EJERCICIO 3: Filtrado de rendimiento")

superiores_promedio = matriz[matriz > promedio_general]
print("Evaluaciones superiores al promedio general:")
print(superiores_promedio)

matriz_filtrada = matriz.copy()
afectados = np.sum(matriz_filtrada < 50)
matriz_filtrada[matriz_filtrada < 50] = 0

print("\nMatriz con valores inferiores a 50 reemplazados por 0:")
print(matriz_filtrada)
print("Cantidad de valores afectados:", afectados)

# ---------------------------------------------------------
# Ejercicio 4: Comparación entre periodos
# ---------------------------------------------------------
print("\n" + "-" * 70)
print("EJERCICIO 4: Comparación entre periodos")

np.random.seed(42)
nueva_matriz = np.random.randint(10, 121, size=matriz.shape)

print("Nueva matriz aleatoria:")
print(nueva_matriz)

diferencia = nueva_matriz - matriz
cambio_promedio = diferencia.mean()

print("\nDiferencia entre ambas matrices:")
print(diferencia)

if cambio_promedio > 0:
    estado = "Mejoró"
elif cambio_promedio < 0:
    estado = "Empeoró"
else:
    estado = "Se mantuvo igual"

print("Cambio promedio:", round(cambio_promedio, 2))
print("Interpretación del rendimiento:", estado)

# =========================================================
# PARTE 2: GESTIÓN DE DATOS (PANDAS)
# =========================================================

print("\n" + "=" * 70)
print("PARTE 2: GESTIÓN DE DATOS (PANDAS)")
print("=" * 70)

# ---------------------------------------------------------
# Ejercicio 5: Creación del DataFrame
# ---------------------------------------------------------
print("\nEJERCICIO 5: Creación del DataFrame")

df = pd.DataFrame({
    "ID": [1, 2, 3, 4, 5],
    "Nombre": ["Ana", "Luis", "Marta", "Juan", "Sofia"],
    "Departamento": ["TI", "Ventas", "TI", "RRHH", "Ventas"],
    "Edad": [29, 35, 28, 40, 30],
    "Salario": [1200, 1000, 1300, 900, 1100]
})

print("DataFrame inicial:")
print(df)

print("\nTipos de datos:")
print(df.dtypes)

print("\nEstadísticas básicas:")
print(df.describe(include="all"))

# ---------------------------------------------------------
# Ejercicio 6: Limpieza y transformación
# ---------------------------------------------------------
print("\n" + "-" * 70)
print("EJERCICIO 6: Limpieza y transformación")

nuevo_registro = pd.DataFrame({
    "ID": [6],
    "Nombre": ["Carlos"],
    "Departamento": ["TI"],
    "Edad": [np.nan],
    "Salario": [np.nan]
})

df = pd.concat([df, nuevo_registro], ignore_index=True)

print("DataFrame con registro nulo agregado:")
print(df)

df["Edad"] = df["Edad"].fillna(df["Edad"].mean())
df["Salario"] = df["Salario"].fillna(df["Salario"].mean())

print("\nDataFrame con nulos rellenados:")
print(df)

print("\n¿Existen nulos?")
print(df.isnull().sum())

# ---------------------------------------------------------
# Ejercicio 7: Análisis por departamento
# ---------------------------------------------------------
print("\n" + "-" * 70)
print("EJERCICIO 7: Análisis por departamento")

analisis_departamento = df.groupby("Departamento").agg(
    Salario_Promedio=("Salario", "mean"),
    Cantidad_Empleados=("ID", "count")
)

depto_mejor_salario = analisis_departamento["Salario_Promedio"].idxmax()

print("Análisis por departamento:")
print(analisis_departamento)

print("\nDepartamento con mayor salario promedio:", depto_mejor_salario)

# ---------------------------------------------------------
# Ejercicio 8: Segmentación de empleados
# ---------------------------------------------------------
print("\n" + "-" * 70)
print("EJERCICIO 8: Segmentación de empleados")

def clasificar_nivel_salario(salario):
    if salario < 1000:
        return "Bajo"
    elif 1000 <= salario <= 1200:
        return "Medio"
    else:
        return "Alto"

df["Nivel_Salarial"] = df["Salario"].apply(clasificar_nivel_salario)

conteo_niveles = df["Nivel_Salarial"].value_counts()

print("DataFrame con nivel salarial:")
print(df)

print("\nCantidad de empleados por nivel salarial:")
print(conteo_niveles)

# ---------------------------------------------------------
# Ejercicio 9: Incorporación de nuevos datos
# ---------------------------------------------------------
print("\n" + "-" * 70)
print("EJERCICIO 9: Incorporación de nuevos datos")

bonos = pd.DataFrame({
    "ID": [1, 2, 3, 5],
    "Bono": [200, 150, 300, 250]
})

df_bonos = pd.merge(df, bonos, on="ID", how="left")
df_bonos["Bono"] = df_bonos["Bono"].fillna(0)
df_bonos["Ingreso_Total"] = df_bonos["Salario"] + df_bonos["Bono"]

sin_bono = df_bonos[df_bonos["Bono"] == 0]

print("DataFrame combinado con bonos:")
print(df_bonos)

print("\nEmpleados sin bono:")
print(sin_bono[["ID", "Nombre", "Departamento", "Salario", "Bono"]])

# ---------------------------------------------------------
# Ejercicio 10: Análisis final
# ---------------------------------------------------------
print("\n" + "-" * 70)
print("EJERCICIO 10: Análisis final")

promedio_ingreso_depto = df_bonos.groupby("Departamento")["Ingreso_Total"].mean()
promedio_general_ingreso = df_bonos["Ingreso_Total"].mean()
sobre_promedio = df_bonos[df_bonos["Ingreso_Total"] > promedio_general_ingreso]

area_competitiva = promedio_ingreso_depto.idxmax()

print("Promedio de ingreso total por departamento:")
print(promedio_ingreso_depto)

print("\nPromedio general de ingreso total:", round(promedio_general_ingreso, 2))

print("\nEmpleados con ingreso total sobre el promedio general:")
print(sobre_promedio[["ID", "Nombre", "Departamento", "Ingreso_Total"]])

print("\nInterpretación:")
print(f"El área más competitiva parece ser {area_competitiva}, ya que tiene el mayor ingreso total promedio.")

# ---------------------------------------------------------
# EXPORTAR RESULTADOS
# ---------------------------------------------------------
df.to_csv("empleados_limpio.csv", index=False)
analisis_departamento.to_csv("analisis_departamento.csv")
df_bonos.to_csv("empleados_con_bonos.csv", index=False)
sobre_promedio.to_csv("empleados_sobre_promedio.csv", index=False)

print("\nArchivos generados correctamente:")
print("- empleados_limpio.csv")
print("- analisis_departamento.csv")
print("- empleados_con_bonos.csv")
print("- empleados_sobre_promedio.csv")
