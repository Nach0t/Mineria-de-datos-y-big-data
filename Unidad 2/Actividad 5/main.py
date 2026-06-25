import numpy as np
import pandas as pd

# =========================================================
# ACTIVIDAD 5 UNIDAD 2 - CASO APLICADO 2
# RetailData Ltda.
# =========================================================

print("\n" + "=" * 70)
print("PARTE 1: PROCESAMIENTO NUMÉRICO (NUMPY)")
print("=" * 70)

# ---------------------------------------------------------
# Ejercicio 1: Estructura de ventas
# ---------------------------------------------------------
print("\nEJERCICIO 1: Estructura de ventas")

ventas = np.array([120, 150, 90, 200, 80, 110, 140, 170, 100, 130, 160, 180])

print("Arreglo original:")
print(ventas)

print("\nDimensión del arreglo:", ventas.ndim)
print("Shape del arreglo:", ventas.shape)
print("Tipo de dato:", ventas.dtype)

matriz_ventas = ventas.reshape(3, 4)
print("\nMatriz de ventas (3 sucursales x 4 meses):")
print(matriz_ventas)

print("\nInterpretación:")
print("- Cada fila representa una sucursal")
print("- Cada columna representa un mes")
print("  Fila 1 = Sucursal Norte")
print("  Fila 2 = Sucursal Sur")
print("  Fila 3 = Sucursal Centro")

# ---------------------------------------------------------
# Ejercicio 2: Análisis de ventas
# ---------------------------------------------------------
print("\n" + "-" * 70)
print("EJERCICIO 2: Análisis de ventas")

ventas_totales_sucursal = matriz_ventas.sum(axis=1)
ventas_promedio_mes = matriz_ventas.mean(axis=0)

sucursal_mejor = np.argmax(ventas_totales_sucursal)
mes_mejor = np.argmax(ventas_promedio_mes)

print("Ventas totales por sucursal:", ventas_totales_sucursal)
print("Ventas promedio por mes:", ventas_promedio_mes)

print(f"Sucursal con mayores ventas totales: Sucursal {sucursal_mejor + 1}")
print(f"Mes con mayores ventas promedio: Mes {mes_mejor + 1}")

# ---------------------------------------------------------
# Ejercicio 3: Evaluación de desempeño
# ---------------------------------------------------------
print("\n" + "-" * 70)
print("EJERCICIO 3: Evaluación de desempeño")

promedio_general = matriz_ventas.mean()
ventas_superiores = matriz_ventas[matriz_ventas > promedio_general]

matriz_bajo_rendimiento = matriz_ventas.copy()
matriz_bajo_rendimiento[matriz_bajo_rendimiento < 100] = 0

print("Promedio general de ventas:", promedio_general)
print("\nVentas superiores al promedio:")
print(ventas_superiores)

print("\nMatriz con ventas menores a 100 reemplazadas por 0:")
print(matriz_bajo_rendimiento)

# ---------------------------------------------------------
# Ejercicio 4: Comparación de escenarios
# ---------------------------------------------------------
print("\n" + "-" * 70)
print("EJERCICIO 4: Comparación de escenarios")

np.random.seed(42)
variacion = np.random.randint(-30, 31, size=matriz_ventas.shape)
nuevo_periodo = matriz_ventas + variacion

diferencia = nuevo_periodo - matriz_ventas
cambio_promedio = diferencia.mean()

print("Nuevo período simulado:")
print(nuevo_periodo)

print("\nDiferencia entre períodos:")
print(diferencia)

if cambio_promedio > 0:
    estado = "Aumentaron"
elif cambio_promedio < 0:
    estado = "Disminuyeron"
else:
    estado = "Se mantuvieron"

print("Cambio promedio:", round(cambio_promedio, 2))
print("Interpretación:", estado)

# =========================================================
# PARTE 2: GESTIÓN DE DATOS (PANDAS)
# =========================================================

print("\n" + "=" * 70)
print("PARTE 2: GESTIÓN DE DATOS (PANDAS)")
print("=" * 70)

# ---------------------------------------------------------
# Ejercicio 5: Creación de DataFrame
# ---------------------------------------------------------
print("\nEJERCICIO 5: Creación de DataFrame")

df = pd.DataFrame({
    "ID": [1, 2, 3, 4, 5],
    "Producto": ["Laptop", "Mouse", "Silla", "Escritorio", "Audífonos"],
    "Categoria": ["Tecnología", "Tecnología", "Hogar", "Hogar", "Tecnología"],
    "Precio": [800, 20, 100, 200, 50],
    "Cantidad": [5, 50, 10, 7, 20]
})

df["Ingreso"] = df["Precio"] * df["Cantidad"]

print("DataFrame inicial:")
print(df)

# ---------------------------------------------------------
# Ejercicio 6: Análisis por categoría
# ---------------------------------------------------------
print("\n" + "-" * 70)
print("EJERCICIO 6: Análisis por categoría")

analisis_categoria = df.groupby("Categoria").agg(
    Ingreso_Total=("Ingreso", "sum"),
    Cantidad_Total=("Cantidad", "sum")
)

categoria_mas_rentable = analisis_categoria["Ingreso_Total"].idxmax()

print("Análisis por categoría:")
print(analisis_categoria)

print("\nCategoría más rentable:", categoria_mas_rentable)

# ---------------------------------------------------------
# Ejercicio 7: Segmentación de productos
# ---------------------------------------------------------
print("\n" + "-" * 70)
print("EJERCICIO 7: Segmentación de productos")

def clasificar_nivel_venta(ingreso):
    if ingreso < 500:
        return "Bajo"
    elif 500 <= ingreso <= 2000:
        return "Medio"
    else:
        return "Alto"

df["Nivel_Venta"] = df["Ingreso"].apply(clasificar_nivel_venta)

conteo_niveles = df["Nivel_Venta"].value_counts()

print("DataFrame con nivel de venta:")
print(df)

print("\nCantidad de productos por nivel:")
print(conteo_niveles)

# ---------------------------------------------------------
# Ejercicio 8: Agregación y filtrado
# ---------------------------------------------------------
print("\n" + "-" * 70)
print("EJERCICIO 8: Agregación y filtrado")

ingreso_promedio = df["Ingreso"].mean()
productos_sobre_promedio = df[df["Ingreso"] > ingreso_promedio].sort_values(
    by="Ingreso", ascending=False
)

print("Ingreso promedio:", ingreso_promedio)

print("\nProductos con ingreso superior al promedio:")
print(productos_sobre_promedio)

# ---------------------------------------------------------
# Ejercicio 9: Combinación de datos
# ---------------------------------------------------------
print("\n" + "-" * 70)
print("EJERCICIO 9: Combinación de datos")

sucursales = pd.DataFrame({
    "ID": [1, 2, 3, 4, 5],
    "Sucursal": ["Norte", "Sur", "Centro", "Norte", "Sur"]
})

df_merge = pd.merge(df, sucursales, on="ID", how="left")

ingreso_por_sucursal = df_merge.groupby("Sucursal")["Ingreso"].sum()

print("DataFrame combinado:")
print(df_merge)

print("\nIngreso total por sucursal:")
print(ingreso_por_sucursal)

# ---------------------------------------------------------
# Ejercicio 10: Análisis final
# ---------------------------------------------------------
print("\n" + "-" * 70)
print("EJERCICIO 10: Análisis final")

mejor_sucursal = ingreso_por_sucursal.idxmax()

categoria_por_sucursal = (
    df_merge.groupby(["Sucursal", "Categoria"])["Ingreso"]
    .sum()
    .reset_index()
    .sort_values(["Sucursal", "Ingreso"], ascending=[True, False])
)

productos_mejor_sucursal = df_merge[
    (df_merge["Sucursal"] == mejor_sucursal) &
    (df_merge["Nivel_Venta"] == "Alto")
]

print("Sucursal con mayor ingreso:", mejor_sucursal)

print("\nCategoría dominante por sucursal:")
print(categoria_por_sucursal)

print(f"\nProductos de alto rendimiento en la mejor sucursal ({mejor_sucursal}):")
print(productos_mejor_sucursal)

# ---------------------------------------------------------
# EXPORTAR RESULTADOS
# ---------------------------------------------------------
df.to_csv("productos_con_ingreso.csv", index=False)
analisis_categoria.to_csv("analisis_categoria.csv")
df_merge.to_csv("productos_sucursales.csv", index=False)
productos_sobre_promedio.to_csv("productos_sobre_promedio.csv", index=False)
productos_mejor_sucursal.to_csv("mejor_sucursal_alto_rendimiento.csv", index=False)

print("\nArchivos generados correctamente:")
print("- productos_con_ingreso.csv")
print("- analisis_categoria.csv")
print("- productos_sucursales.csv")
print("- productos_sobre_promedio.csv")
print("- mejor_sucursal_alto_rendimiento.csv")
