#!/usr/bin/env python3
import os
import yaml
import matplotlib.pyplot as plt
from collections import Counter
import argparse

def analyze_bleed_status(directory):
    """
    Analiza todos los archivos YAML en un directorio para contar los valores de 'has_bleed'
    
    Args:
        directory (str): Ruta al directorio que contiene los archivos YAML
        
    Returns:
        Counter: Contador con los valores de 'has_bleed' y sus frecuencias
    """
    bleed_counter = Counter()
    yaml_files = []
    
    # Buscar todos los archivos YAML en el directorio
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(('.yaml', '.yml')):
                yaml_files.append(os.path.join(root, file))
    
    print(f"Se encontraron {len(yaml_files)} archivos YAML")
    
    # Analizar cada archivo YAML
    for yaml_file in yaml_files:
        try:
            with open(yaml_file, 'r', encoding='utf-8') as file:
                data = yaml.safe_load(file)
                
                # Verificar si el archivo tiene la clave 'has_bleed'
                if 'has_bleed' in data:
                    bleed_status = data['has_bleed']
                    bleed_counter[bleed_status] += 1
                else:
                    bleed_counter['no especificado'] += 1
        except Exception as e:
            print(f"Error al procesar {yaml_file}: {e}")
            bleed_counter['error'] += 1
    
    return bleed_counter

def create_histogram(counter):
    """
    Crea un diagrama circular basado en los resultados del contador
    
    Args:
        counter (Counter): Contador con valores y frecuencias
    """
    labels = list(counter.keys())
    values = list(counter.values())
    
    # Configurar un estilo más suave
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Establecer un fondo suave
    fig.patch.set_facecolor('#f8f9fa')
    
    # Asignar colores más fríos y menos intensos
    colors = []
    for label in labels:
        if label == 'yes':
            colors.append('#8da0cb')  # Azul suave
        elif label == 'no':
            colors.append('#66c2a5')  # Verde menta suave
        else:
            colors.append('#d9d9d9')  # Gris claro
    
    # Crear el gráfico circular
    wedges, texts, autotexts = ax.pie(
        values, 
        labels=None,  # No mostramos etiquetas en el gráfico para evitar sobrecarga
        autopct='%1.1f%%',  # Mostrar porcentajes con un decimal
        startangle=90,      # Comenzar desde arriba
        colors=colors,
        wedgeprops={'edgecolor': 'white', 'linewidth': 1.5},  # Bordes blancos para separar segmentos
        textprops={'fontsize': 12, 'color': '#333333'},       # Propiedades del texto
        shadow=False,
        explode=[0.05 if label == 'yes' else 0 for label in labels]  # Destacar ligeramente 'yes'
    )
    
    # Añadir título con estilo más suave
    ax.set_title('Distribución de sangrado', 
                fontsize=14, color='#444444', pad=20)
    
    # Crear leyenda personalizada
    legend_labels = [f"{label} ({value} archivos)" for label, value in zip(labels, values)]
    ax.legend(wedges, legend_labels, title="Valores", 
              loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
    
    # Ajustar el diseño para que haya espacio para la leyenda
    plt.tight_layout()
    
    # Guardar el gráfico
    plt.savefig('has_bleed_chart.png', bbox_inches='tight')
    print("Gráfico circular guardado como 'has_bleed_chart.png'")
    
    # Mostrar el gráfico
    plt.show()

def main():
    parser = argparse.ArgumentParser(description='Analiza la opción "has_bleed" en archivos YAML')
    parser.add_argument('directory', help='Directorio que contiene los archivos YAML')
    args = parser.parse_args()
    
    if not os.path.isdir(args.directory):
        print(f"Error: '{args.directory}' no es un directorio válido")
        return
    
    bleed_counter = analyze_bleed_status(args.directory)
    
    print("\nResultados del análisis:")
    for status, count in bleed_counter.items():
        print(f"  has_bleed: '{status}' - {count} archivos")
    
    create_histogram(bleed_counter)

if __name__ == "__main__":
    main()