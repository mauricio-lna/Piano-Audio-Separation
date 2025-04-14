#!/usr/bin/env python3
import os
import yaml
import argparse
import matplotlib.pyplot as plt
from collections import Counter


def analyze_artists(yaml_path):
    """
    Analiza los archivos YAML en la ruta especificada y cuenta los artistas.
    
    Args:
        yaml_path (str): Ruta donde se encuentran los archivos YAML
        
    Returns:
        Counter: Contador con los artistas y sus ocurrencias
    """
    all_artists = []
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
                    
                    # Extraer artistas
                    if 'artist' in data and data['artist']:
                        # En algunos casos, 'artist' podría ser una lista o una cadena
                        if isinstance(data['artist'], list):
                            all_artists.extend([str(a).strip() for a in data['artist'] if a])
                        else:
                            artist = str(data['artist']).strip()
                            if artist:
                                all_artists.append(artist)
                
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
    all_artists = [artist for artist in all_artists if artist and artist.strip()]
    
    # Contar ocurrencias de artistas
    return Counter(all_artists)


def plot_pie_chart(artists_counter, output_file=None, max_artists=15):
    """
    Genera un gráfico circular con los artistas más comunes.
    
    Args:
        artists_counter (Counter): Contador con los artistas y sus ocurrencias
        output_file (str, optional): Ruta para guardar el gráfico. Si es None, se muestra en pantalla.
        max_artists (int, optional): Número máximo de artistas a mostrar individualmente en el gráfico.
    """
    if not artists_counter:
        print("No hay datos para generar el gráfico.")
        return
    
    # Ordenar por frecuencia (de mayor a menor)
    most_common = artists_counter.most_common()
    
    # Preparar datos para el gráfico
    if len(most_common) > max_artists:
        # Mostrar los max_artists más comunes y agrupar el resto como "Otros"
        labels = [item[0] for item in most_common[:max_artists]]
        values = [item[1] for item in most_common[:max_artists]]
        
        # Suma de "Otros"
        other_sum = sum(item[1] for item in most_common[max_artists:])
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
    
    # Crear un esquema de colores fríos y suaves
    colors = plt.cm.Blues([(0.3 + i*0.5/len(labels)) for i in range(len(labels))])
    
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
        title="Artistas", 
        loc="center left", 
        bbox_to_anchor=(1, 0, 0.5, 1),
        fontsize=10
    )
    
    # Añadir título
    plt.title('Distribución de Artistas', fontsize=14, color='#334455', pad=20)
    
    # Ajustar el diseño
    plt.tight_layout()
    
    # Guardar o mostrar
    if output_file:
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"Gráfico guardado en: {output_file}")
    else:
        plt.show()


def plot_bar_chart(artists_counter, output_file=None, max_artists=20):
    """
    Genera un gráfico de barras horizontal con los artistas más comunes.
    
    Args:
        artists_counter (Counter): Contador con los artistas y sus ocurrencias
        output_file (str, optional): Ruta para guardar el gráfico. Si es None, se muestra en pantalla.
        max_artists (int, optional): Número máximo de artistas a mostrar en el gráfico.
    """
    if not artists_counter:
        print("No hay datos para generar el gráfico.")
        return
    
    # Ordenar por frecuencia y limitar el número de artistas
    sorted_artists = artists_counter.most_common(max_artists)
    artists = [item[0] for item in sorted_artists]
    counts = [item[1] for item in sorted_artists]
    
    # Invertir listas para que el más común aparezca arriba
    artists.reverse()
    counts.reverse()
    
    # Crear figura con tamaño adaptable y fondo suave
    plt.figure(figsize=(12, max(8, min(len(artists) * 0.4, 18))))
    fig = plt.gcf()
    fig.patch.set_facecolor('#f8f9fa')
    ax = plt.gca()
    ax.set_facecolor('#f0f3f5')
    
    # Generar gráfico de barras horizontal con colores fríos
    bars = plt.barh(artists, counts, color='#6b93b0', alpha=0.8, edgecolor='#5a7d98', linewidth=0.5)
    
    # Añadir etiquetas con valores
    for bar in bars:
        width = bar.get_width()
        plt.text(width + 0.5, bar.get_y() + bar.get_height()/2, f"{width}", 
                ha='left', va='center', color='#445566')
    
    # Configurar el gráfico
    plt.xlabel('Ocurrencias', fontsize=11, color='#445566')
    plt.ylabel('Artistas', fontsize=11, color='#445566')
    plt.title('Frecuencia de Artistas en Archivos YAML', 
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
    parser = argparse.ArgumentParser(description='Analizar artistas en archivos YAML')
    parser.add_argument('yaml_path', type=str, help='Ruta donde se encuentran los archivos YAML')
    parser.add_argument('--output', '-o', type=str, help='Prefijo para guardar los gráficos (opcional)')
    parser.add_argument('--limit', '-l', type=int, default=20, help='Número máximo de artistas a mostrar (default: 20)')
    parser.add_argument('--csv', '-c', type=str, help='Ruta para guardar los resultados en CSV (opcional)')
    parser.add_argument('--pie', '-p', action='store_true', help='Generar gráfico circular en lugar de barras')
    
    args = parser.parse_args()
    
    # Ejecutar análisis
    artists_counter = analyze_artists(args.yaml_path)
    
    # Mostrar resultados en consola
    if artists_counter:
        print(f"\nTotal de artistas únicos: {len(artists_counter)}")
        print(f"Total de ocurrencias: {sum(artists_counter.values())}")
        
        # Mostrar artistas más comunes
        print("\nArtistas más comunes:")
        for artist, count in artists_counter.most_common(20):  # Mostrar solo los 20 más comunes en consola
            print(f"- {artist}: {count}")
        
        if len(artists_counter) > 20:
            print(f"... y {len(artists_counter) - 20} artistas más")
        
        # Guardar resultados en CSV si se especificó
        if args.csv:
            try:
                import csv
                with open(args.csv, 'w', newline='', encoding='utf-8') as csvfile:
                    csv_writer = csv.writer(csvfile)
                    csv_writer.writerow(['Artista', 'Ocurrencias'])
                    for artist, count in artists_counter.most_common():
                        csv_writer.writerow([artist, count])
                print(f"Resultados guardados en CSV: {args.csv}")
            except Exception as e:
                print(f"Error al guardar el CSV: {e}")
        
        # Generar gráficos
        if args.pie:
            # Gráfico circular
            pie_output = f"{args.output}_pie.png" if args.output else None
            plot_pie_chart(artists_counter, pie_output, args.limit)
        else:
            # Gráfico de barras horizontal (predeterminado)
            bar_output = f"{args.output}_bar.png" if args.output else None
            plot_bar_chart(artists_counter, bar_output, args.limit)
    else:
        print("No se encontraron artistas para analizar.")


if __name__ == "__main__":
    main()