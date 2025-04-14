import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Datos proporcionados
instrumentos = ['Guitarra', 'Piano', 'Cuerdas contiguas', 'Bajo', 'Batería', 'Metales', 
                'Pad sintetizador', 'Caña', 'Órgano', 'Flauta', 'Sintetizador líder', 
                'Percusión cromática', 'Cuerdas', 'Efectos de sonido', 'Etnico', 'Percusivo']

ocurrencias = [3343, 2130, 2098, 1548, 1289, 681, 572, 490, 446, 432, 383, 295, 272, 386, 96, 68]

porcentajes = [23.01, 14.66, 14.44, 10.65, 8.87, 4.69, 3.94, 3.37, 3.07, 2.97, 2.64, 2.03, 1.87, 2.66, 1.17, 0.47]

# Crear un DataFrame para facilitar el manejo de datos
df = pd.DataFrame({
    'Instrumentos': instrumentos,
    'Ocurrencias': ocurrencias,
    'Porcentaje': porcentajes
})

# Ordenar por número de ocurrencias (de mayor a menor)
df = df.sort_values('Ocurrencias', ascending=False)

# Crear figura con tamaño personalizado
plt.figure(figsize=(14, 8))

# Crear el gráfico de barras (histograma)
bars = plt.bar(df['Instrumentos'], df['Ocurrencias'], color='skyblue', edgecolor='navy')

# Añadir etiquetas y título
plt.xlabel('Instrumentos', fontsize=12)
plt.ylabel('Ocurrencias', fontsize=12)
plt.title('Histograma de Frecuencia de Instrumentos Musicales', fontsize=16, pad=20)

# Rotar las etiquetas del eje x para mejor visualización
plt.xticks(rotation=45, ha='right', fontsize=10)

# Añadir los valores de ocurrencias encima de cada barra
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height + 50,
             f'{height}',
             ha='center', va='bottom', fontsize=9)

# Añadir porcentajes en las barras
for i, bar in enumerate(bars):
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height/2,
             f'{df["Porcentaje"].iloc[i]}%',
             ha='center', va='center', fontsize=9, color='white', fontweight='bold')

# Ajustar layout
plt.tight_layout()

# Añadir grid horizontal para facilitar la lectura
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Mostrar el gráfico
plt.show()