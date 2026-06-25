import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# =========================================================
# ACTIVIDAD 6 UNIDAD 2 - CASO PRÁCTICO INTEGRADOR
# TechRetail SpA
# =========================================================

# =========================================================
# PARTE 1: NUMPY - DESEMPEÑO
# =========================================================
print("\n" + "=" * 70)
print("PARTE 1: PROCESAMIENTO NUMÉRICO (NUMPY)")
print("=" * 70)

desempeno = np.array([
    80, 90, 75, 85,
    60, 70, 65, 75,
    95, 85, 90, 100
])

matriz_desempeno = desempeno.reshape(3, 4)

print("\nMatriz de desempeño (3 equipos x 4 meses):")
print(matriz_desempeno)

promedio_equipo = matriz_desempeno.mean(axis=1)
promedio_mes = matriz_desempeno.mean(axis=0)
promedio_general = matriz_desempeno.mean()

equipo_mejor = np.argmax(promedio_equipo)
mes_peor = np.argmin(promedio_mes)

valores_sobre_promedio = matriz_desempeno[matriz_desempeno > promedio_general]

matriz_filtrada = matriz_desempeno.copy()
matriz_filtrada[matriz_filtrada < 70] = 0

print("\nPromedio por equipo:", promedio_equipo)
print("Promedio por mes:", promedio_mes)
print("Promedio general:", promedio_general)

print(f"\nEquipo con mejor desempeño: Equipo {equipo_mejor + 1}")
print(f"Mes con menor desempeño: Mes {mes_peor + 1}")

print("\nValores sobre el promedio general:")
print(valores_sobre_promedio)

print("\nMatriz con valores bajo 70 reemplazados por 0:")
print(matriz_filtrada)

# =========================================================
# PARTE 2: PANDAS - VENTAS
# =========================================================
print("\n" + "=" * 70)
print("PARTE 2: GESTIÓN DE DATOS (PANDAS)")
print("=" * 70)

df = pd.DataFrame({
    "ID": [1, 2, 3, 4, 5, 6],
    "Producto": ["Laptop", "Mouse", "Teclado", "Monitor", "Silla", "Escritorio"],
    "Categoria": ["Tecnología", "Tecnología", "Tecnología", "Tecnología", "Hogar", "Hogar"],
    "Precio": [800, 20, 50, 300, 120, 250],
    "Cantidad": [5, 50, 30, 10, 15, 8],
    "Sucursal": ["Norte", "Sur", "Centro", "Norte", "Sur", "Centro"]
})

df["Ingreso"] = df["Precio"] * df["Cantidad"]

print("\nDataFrame con columna Ingreso:")
print(df)

ingreso_categoria = df.groupby("Categoria")["Ingreso"].sum()
ingreso_sucursal = df.groupby("Sucursal")["Ingreso"].sum()

promedio_ingreso_producto = df.groupby("Producto")["Ingreso"].mean()
cantidad_categoria = df.groupby("Categoria")["Cantidad"].sum()

def clasificar_nivel_venta(ingreso):
    if ingreso < 1000:
        return "Bajo"
    elif 1000 <= ingreso <= 3000:
        return "Medio"
    else:
        return "Alto"

df["Nivel_Venta"] = df["Ingreso"].apply(clasificar_nivel_venta)

promedio_ingreso = df["Ingreso"].mean()
productos_sobre_promedio = df[df["Ingreso"] > promedio_ingreso]

print("\nIngreso total por categoría:")
print(ingreso_categoria)

print("\nIngreso total por sucursal:")
print(ingreso_sucursal)

print("\nPromedio de ingreso por producto:")
print(promedio_ingreso_producto)

print("\nCantidad total vendida por categoría:")
print(cantidad_categoria)

print("\nDataFrame con Nivel_Venta:")
print(df)

print("\nProductos con ingresos superiores al promedio:")
print(productos_sobre_promedio)

# =========================================================
# PARTE 3: INTEGRACIÓN DEL ANÁLISIS
# =========================================================
print("\n" + "=" * 70)
print("PARTE 3: INTEGRACIÓN DEL ANÁLISIS")
print("=" * 70)

sucursal_mas_fuerte = ingreso_sucursal.idxmax()
categoria_dominante = ingreso_categoria.idxmax()

print(f"\nSucursal más fuerte: {sucursal_mas_fuerte}")
print(f"Categoría dominante: {categoria_dominante}")

print("\nRelación desempeño vs ventas:")
print("- El equipo con mejor desempeño podría asociarse a una mejor gestión comercial.")
print("- Las sucursales con mayores ingresos podrían estar respaldadas por equipos más eficientes.")
print("- Sin embargo, con estos datos no existe una relación directa uno a uno entre equipo y sucursal, por lo que la conclusión es referencial.")

decisiones = [
    "1. Reforzar la sucursal con menor ingreso con estrategias de venta y capacitación del equipo.",
    "2. Potenciar la categoría dominante con más stock, promociones y seguimiento de productos de alto ingreso."
]

print("\nDecisiones recomendadas:")
for d in decisiones:
    print(d)

# =========================================================
# PARTE 4: CONCLUSIONES ESCRITAS
# =========================================================
print("\n" + "=" * 70)
print("PARTE 4: CONCLUSIONES")
print("=" * 70)

conclusiones = f"""
1. ¿Qué área de la empresa tiene mejor rendimiento?
   El mejor rendimiento en desempeño lo presenta el Equipo {equipo_mejor + 1}, ya que obtuvo el promedio más alto.
   En ventas, la categoría con mejor rendimiento es {categoria_dominante} por su mayor ingreso acumulado.

2. ¿Qué sucursal presenta mayor desempeño comercial?
   La sucursal con mayor desempeño comercial es {sucursal_mas_fuerte}, ya que concentra el mayor ingreso total.

3. ¿Existe relación entre desempeño y ventas?
   Se puede plantear una relación indirecta: mejores equipos suelen favorecer mejores resultados comerciales.
   Sin embargo, con los datos entregados no existe un vínculo explícito entre cada equipo y cada sucursal, por lo que la relación es solo inferencial.

4. ¿Qué decisiones recomendarías a la gerencia?
   - Reforzar la sucursal con menor ingreso mediante capacitación, promociones y seguimiento comercial.
   - Fortalecer la categoría dominante, ya que es la que más aporta al negocio.
"""

print(conclusiones)

# Guardar conclusiones en txt
with open("conclusiones.txt", "w", encoding="utf-8") as f:
    f.write(conclusiones)

# =========================================================
# VISUALIZACIONES
# =========================================================
print("\n" + "=" * 70)
print("GENERANDO GRÁFICOS...")
print("=" * 70)

# Gráfico 1: Promedio por equipo
plt.figure(figsize=(8, 5))
plt.bar(["Equipo 1", "Equipo 2", "Equipo 3"], promedio_equipo)
plt.title("Promedio de Desempeño por Equipo")
plt.xlabel("Equipo")
plt.ylabel("Promedio")
plt.tight_layout()
plt.savefig("grafico_desempeno_equipos.png")
plt.close()

# Gráfico 2: Ingreso por sucursal
plt.figure(figsize=(8, 5))
ingreso_sucursal.plot(kind="bar")
plt.title("Ingreso Total por Sucursal")
plt.xlabel("Sucursal")
plt.ylabel("Ingreso")
plt.tight_layout()
plt.savefig("grafico_ingreso_sucursal.png")
plt.close()

# Gráfico 3: Ingreso por categoría
plt.figure(figsize=(8, 5))
ingreso_categoria.plot(kind="bar")
plt.title("Ingreso Total por Categoría")
plt.xlabel("Categoría")
plt.ylabel("Ingreso")
plt.tight_layout()
plt.savefig("grafico_ingreso_categoria.png")
plt.close()

# =========================================================
# EXPORTAR CSV
# =========================================================
df.to_csv("ventas_techretail.csv", index=False)
productos_sobre_promedio.to_csv("productos_sobre_promedio.csv", index=False)

resumen_categoria = ingreso_categoria.reset_index()
resumen_categoria.columns = ["Categoria", "Ingreso_Total"]
resumen_categoria.to_csv("resumen_categoria.csv", index=False)

resumen_sucursal = ingreso_sucursal.reset_index()
resumen_sucursal.columns = ["Sucursal", "Ingreso_Total"]
resumen_sucursal.to_csv("resumen_sucursal.csv", index=False)

print("\nArchivos generados correctamente:")
print("- ventas_techretail.csv")
print("- productos_sobre_promedio.csv")
print("- resumen_categoria.csv")
print("- resumen_sucursal.csv")
print("- conclusiones.txt")
print("- grafico_desempeno_equipos.png")
print("- grafico_ingreso_sucursal.png")
print("- grafico_ingreso_categoria.png")
