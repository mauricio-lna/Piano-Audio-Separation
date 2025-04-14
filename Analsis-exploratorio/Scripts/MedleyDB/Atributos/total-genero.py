#!/usr/bin/env python3
import os
import yaml
import argparse
import matplotlib.pyplot as plt
from collections import Counter


def analyze_genres(yaml_path):
    """
    Analiza los archivos YAML en la ruta especificada y cuenta los géneros musicales.
    
    Args:
        yaml_path (str): Ruta donde se encuentran los archivos YAML
        
    Returns:
        Counter: Contador con los géneros y sus ocurrencias
    """
    all_genres = []
    skipped_files = 0
    
    # Verificar que el directorio exista
    if not os.path.exists(yaml_path):
        print(f"Error: La ruta {yaml_path} no existe.")
        return Counter()
    
    # Obtener todos los archivos YAML en la ruta
    yaml_files = [f for f in os.listdir(yaml_path) if f.endswith(('.yaml', '.yml'))]
    
    if not yaml_files:
        print(f"No se encontraron archivos YAML en {yaml_path}")
        return Counter()
    
    print(f"Analizando {len(yaml_files)} archivos YAML en {yaml_path}")
    
    # Procesar cada archivo YAML
    for yaml_file in yaml_files:
        full_path = os.path.join(yaml_path, yaml_file)
        
        try:
            with open(full_path, 'r', encoding='utf-8') as file:
                try:
                    data = yaml.safe_load(file)
                    
                    # Si no hay datos o no es un diccionario, continuar con el siguiente archivo
                    if not data or not isinstance(data, dict):
                        skipped_files += 1
                        continue
                    
                    # Extraer géneros
                    if 'genre' in data and data['genre']:
                        # En algunos casos, 'genre' podría ser una lista o una cadena
                        if isinstance(data['genre'], list):
                            all_genres.extend([str(g).strip() for g in data['genre'] if g])
                        else:
                            genre = str(data['genre']).strip()
                            if genre:
                                all_genres.append(genre)
                
                except yaml.YAMLError as e:
                    print(f"Error al parsear YAML {yaml_file}: {e}")
                    skipped_files += 1
                    continue
        except Exception as e:
            print(f"Error al abrir el archivo {yaml_file}: {e}")
            skipped_files += 1
            continue
    
    # Informar archivos omitidos
    if skipped_files > 0:
        print(f"Se omitieron {skipped_files} archivos debido a errores o formato inválido.")
    
    # Filtrar valores vacíos
    all_genres = [genre for genre in all_genres if genre and genre.strip()]
    
    # Contar ocurrencias de géneros
    return Counter(all_genres)


def plot_pie_chart(genres_counter, output_file=None, max_genres=15):
    """
    Genera un gráfico circular con los géneros más comunes.
    
    Args:
        genres_counter (Counter): Contador con los géneros y sus ocurrencias
        output_file (str, optional): Ruta para guardar el gráfico. Si es None, se muestra en pantalla.
        max_genres (int, optional): Número máximo de géneros a mostrar individualmente en el gráfico.
    """
    if not genres_counter:
        print("No hay datos para generar el gráfico.")
        return
    
    # Ordenar por frecuencia (de mayor a menor)
    most_common = genres_counter.most_common()
    
    # Preparar datos para el gráfico
    if len(most_common) > max_genres:
        # Mostrar los max_genres más comunes y agrupar el resto como "Otros"
        labels = [item[0] for item in most_common[:max_genres]]
        values = [item[1] for item in most_common[:max_genres]]
        
        # Suma de "Otros"
        other_sum = sum(item[1] for item in most_common[max_genres:])
        if other_sum > 0:
            labels.append('Otros')
            values.append(other_sum)
    else:
        labels = [item[0] for item in most_common]
        values = [item[1] for item in most_common]
    
    # Crear figura con fondo suave
    plt.figure(figsize=(12, 10))
    fig = plt.gcf()
    fig.patch.set_facecolor('#f8f9fa')
    
    # Crear un esquema de colores fríos y suaves - usando tonos verdes/azulados
    colors = plt.cm.GnBu([(0.3 + i*0.5/len(labels)) for i in range(len(labels))])
    
    # Resaltar ligeramente las porciones más grandes
    explode = [0.05 if i < 3 else 0 for i in range(len(labels))]
    
    # Crear gráfico circular
    wedges, texts, autotexts = plt.pie(
        values, 
        labels=None,  # No mostrar etiquetas en el gráfico para evitar superposición
        autopct='%1.1f%%',
        startangle=90,
        explode=explode,
        colors=colors,
        wedgeprops={'edgecolor': 'white', 'linewidth': 1},
        textprops={'fontsize': 11, 'color': '#445566'},
        shadow=False
    )
    
    # Añadir leyenda
    legend_labels = [f"{label} ({value})" for label, value in zip(labels, values)]
    plt.legend(
        wedges, 
        legend_labels, 
        title="Géneros", 
        loc="center left", 
        bbox_to_anchor=(1, 0, 0.5, 1),
        fontsize=10
    )
    
    # Añadir título
    plt.title('Distribución de Géneros Musicales', fontsize=14, color='#334455', pad=20)
    
    # Ajustar el diseño
    plt.tight_layout()
    
    # Guardar o mostrar
    if output_file:
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"Gráfico guardado en: {output_file}")
    else:
        plt.show()


def plot_bar_chart(genres_counter, output_file=None, max_genres=20):
    """
    Genera un gráfico de barras horizontal con los géneros más comunes.
    
    Args:
        genres_counter (Counter): Contador con los géneros y sus ocurrencias
        output_file (str, optional): Ruta para guardar el gráfico. Si es None, se muestra en pantalla.
        max_genres (int, optional): Número máximo de géneros a mostrar en el gráfico.
    """
    if not genres_counter:
        print("No hay datos para generar el gráfico.")
        return
    
    # Ordenar por frecuencia y limitar el número de géneros
    sorted_genres = genres_counter.most_common(max_genres)
    genres = [item[0] for item in sorted_genres]
    counts = [item[1] for item in sorted_genres]
    
    # Invertir listas para que el más común aparezca arriba
    genres.reverse()
    counts.reverse()
    
    # Crear figura con tamaño adaptable y fondo suave
    plt.figure(figsize=(12, max(8, min(len(genres) * 0.4, 18))))
    fig = plt.gcf()
    fig.patch.set_facecolor('#f8f9fa')
    ax = plt.gca()
    ax.set_facecolor('#f0f3f5')
    
    # Generar gráfico de barras horizontal con colores fríos - tonos verdosos
    bars = plt.barh(genres, counts, color='#66a182', alpha=0.8, edgecolor='#558c70', linewidth=0.5)
    
    # Añadir etiquetas con valores
    for bar in bars:
        width = bar.get_width()
        plt.text(width + 0.5, bar.get_y() + bar.get_height()/2, f"{width}", 
                ha='left', va='center', color='#445566')
    
    # Configurar el gráfico
    plt.xlabel('Ocurrencias', fontsize=11, color='#445566')
    plt.ylabel('Géneros', fontsize=11, color='#445566')
    plt.title('Frecuencia de Géneros Musicales en Archivos YAML', 
             fontsize=13, color='#334455', pad=15)
    
    # Grid más sutil
    plt.grid(axis='x', linestyle='--', alpha=0.4, color='#cccccc')
    
    # Estilo para los ejes
    ax.tick_params(axis='both', colors='#445566')
    for spine in ax.spines.values():
        spine.set_color('#bbbbbb')
    
    # Ajustar márgenes
    plt.tight_layout()
    
    # Guardar o mostrar
    if output_file:
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"Gráfico guardado en: {output_file}")
    else:
        plt.show()


def main():
    # Configurar parser de argumentos
    parser = argparse.ArgumentParser(description='Analizar géneros musicales en archivos YAML')
    parser.add_argument('yaml_path', type=str, help='Ruta donde se encuentran los archivos YAML')
    parser.add_argument('--output', '-o', type=str, help='Prefijo para guardar los gráficos (opcional)')
    parser.add_argument('--limit', '-l', type=int, default=20, help='Número máximo de géneros a mostrar (default: 20)')
    parser.add_argument('--csv', '-c', type=str, help='Ruta para guardar los resultados en CSV (opcional)')
    parser.add_argument('--pie', '-p', action='store_true', help='Generar gráfico circular en lugar de barras')
    
    args = parser.parse_args()
    
    # Ejecutar análisis
    genres_counter = analyze_genres(args.yaml_path)
    
    # Mostrar resultados en consola
    if genres_counter:
        print(f"\nTotal de géneros únicos: {len(genres_counter)}")
        print(f"Total de ocurrencias: {sum(genres_counter.values())}")
        
        # Mostrar géneros más comunes
        print("\nGéneros más comunes:")
        for genre, count in genres_counter.most_common(20):  # Mostrar solo los 20 más comunes en consola
            print(f"- {genre}: {count}")
        
        if len(genres_counter) > 20:
            print(f"... y {len(genres_counter) - 20} géneros más")
        
        # Guardar resultados en CSV si se especificó
        if args.csv:
            try:
                import csv
                with open(args.csv, 'w', newline='', encoding='utf-8') as csvfile:
                    csv_writer = csv.writer(csvfile)
                    csv_writer.writerow(['Género', 'Ocurrencias'])
                    for genre, count in genres_counter.most_common():
                        csv_writer.writerow([genre, count])
                print(f"Resultados guardados en CSV: {args.csv}")
            except Exception as e:
                print(f"Error al guardar el CSV: {e}")
        
        # Generar gráficos
        if args.pie:
            # Gráfico circular
            pie_output = f"{args.output}_pie.png" if args.output else None
            plot_pie_chart(genres_counter, pie_output, args.limit)
        else:
            # Gráfico de barras horizontal (predeterminado)
            bar_output = f"{args.output}_bar.png" if args.output else None
            plot_bar_chart(genres_counter, bar_output, args.limit)
    else:
        print("No se encontraron géneros para analizar.")


if __name__ == "__main__":
    main()