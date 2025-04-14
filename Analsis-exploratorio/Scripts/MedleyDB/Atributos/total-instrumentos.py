import os
import yaml
import argparse
import matplotlib.pyplot as plt
from collections import Counter


def flatten_and_stringify(item):
    """
    Aplanar y convertir a string cualquier estructura de datos anidada.
    
    Args:
        item: Cualquier tipo de dato (string, lista, diccionario, etc.)
        
    Returns:
        list: Lista de strings
    """
    if item is None:
        return []
    
    if isinstance(item, (str, int, float, bool)):
        return [str(item)]
    
    if isinstance(item, list):
        result = []
        for subitem in item:
            result.extend(flatten_and_stringify(subitem))
        return result
    
    if isinstance(item, dict):
        result = []
        for value in item.values():
            result.extend(flatten_and_stringify(value))
        return result
    
    # Para cualquier otro tipo, convertirlo a string
    return [str(item)]


def analyze_instruments(yaml_path):
    """
    Analiza los archivos YAML en la ruta especificada y cuenta los instrumentos.
    Solo analiza los instrumentos en el nivel de 'stems' e ignora los de 'raw'.
    
    Args:
        yaml_path (str): Ruta donde se encuentran los archivos YAML
        
    Returns:
        Counter: Contador con los instrumentos y sus ocurrencias
    """
    all_instruments = []
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
        instruments_in_file = []
        
        try:
            with open(full_path, 'r', encoding='utf-8') as file:
                try:
                    data = yaml.safe_load(file)
                    
                    # Si no hay datos o no es un diccionario, continuar con el siguiente archivo
                    if not data or not isinstance(data, dict) or 'stems' not in data:
                        skipped_files += 1
                        continue
                    
                    # Extraer SOLO los instrumentos de 'stems' (ignorar los de 'raw')
                    if data['stems']:
                        for stem_key, stem_data in data['stems'].items():
                            if isinstance(stem_data, dict) and 'instrument' in stem_data:
                                instrument_values = flatten_and_stringify(stem_data['instrument'])
                                if instrument_values:
                                    instruments_in_file.extend(instrument_values)
                except yaml.YAMLError as e:
                    print(f"Error al parsear YAML {yaml_file}: {e}")
                    skipped_files += 1
                    continue
        except Exception as e:
            print(f"Error al abrir el archivo {yaml_file}: {e}")
            skipped_files += 1
            continue
        
        # Agregar instrumentos encontrados en este archivo a la lista general
        all_instruments.extend(instruments_in_file)
    
    # Informar archivos omitidos
    if skipped_files > 0:
        print(f"Se omitieron {skipped_files} archivos debido a errores o formato inválido.")
    
    # Filtrar valores vacíos y convertir todo a cadenas de texto
    all_instruments = [instr for instr in all_instruments if instr and instr.strip()]
    
    # Contar ocurrencias de instrumentos
    return Counter(all_instruments)


def plot_histogram(instruments_counter, output_file=None, max_instruments=30):
    """
    Genera un histograma con las ocurrencias de los instrumentos.
    
    Args:
        instruments_counter (Counter): Contador con los instrumentos y sus ocurrencias
        output_file (str, optional): Ruta para guardar el histograma. Si es None, se muestra en pantalla.
        max_instruments (int, optional): Número máximo de instrumentos a mostrar en el histograma.
    """
    if not instruments_counter:
        print("No hay datos para generar el histograma.")
        return
    
    # Ordenar por frecuencia (de mayor a menor) y limitar el número de instrumentos si hay muchos
    sorted_instruments = instruments_counter.most_common(max_instruments)
    instruments = [item[0] for item in sorted_instruments]
    counts = [item[1] for item in sorted_instruments]
    
    # Crear figura con tamaño adaptable y fondo suave
    plt.figure(figsize=(12, max(8, min(len(instruments) * 0.3, 20))))
    fig = plt.gcf()
    fig.patch.set_facecolor('#f8f9fa')
    ax = plt.gca()
    ax.set_facecolor('#f0f3f5')
    
    # Generar gráfico de barras horizontal con color más frío y menos intenso
    bars = plt.barh(instruments, counts, color='#6b93b0', alpha=0.8, edgecolor='#5a7d98', linewidth=0.5)
    
    # Añadir etiquetas con valores en un color más suave
    for bar in bars:
        width = bar.get_width()
        plt.text(width + 0.5, bar.get_y() + bar.get_height()/2, f"{width}", 
                ha='left', va='center', color='#445566')
    
    # Configurar el gráfico con colores más suaves
    plt.xlabel('Ocurrencias', fontsize=11, color='#445566')
    plt.ylabel('Instrumentos', fontsize=11, color='#445566')
    plt.title('Frecuencia de Instrumentos en Archivos YAML (solo nivel stems)', 
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
        print(f"Histograma guardado en: {output_file}")
    else:
        plt.show()


def main():
    # Configurar parser de argumentos
    parser = argparse.ArgumentParser(description='Analizar instrumentos en archivos YAML (solo nivel stems)')
    parser.add_argument('yaml_path', type=str, help='Ruta donde se encuentran los archivos YAML')
    parser.add_argument('--output', '-o', type=str, help='Ruta para guardar el histograma (opcional)')
    parser.add_argument('--limit', '-l', type=int, default=30, help='Número máximo de instrumentos a mostrar en el histograma (default: 30)')
    parser.add_argument('--csv', '-c', type=str, help='Ruta para guardar los resultados en CSV (opcional)')
    parser.add_argument('--debug', '-d', action='store_true', help='Habilitar modo de depuración')
    
    args = parser.parse_args()
    
    # Ejecutar análisis
    instruments_counter = analyze_instruments(args.yaml_path)
    
    # Mostrar resultados en consola
    if instruments_counter:
        print(f"\nTotal de instrumentos únicos (solo nivel stems): {len(instruments_counter)}")
        print(f"Total de ocurrencias: {sum(instruments_counter.values())}")
        
        # Mostrar instrumentos más comunes
        print("\nInstrumentos más comunes:")
        for instrument, count in instruments_counter.most_common(20):  # Mostrar solo los 20 más comunes en consola
            print(f"- {instrument}: {count}")
        
        if len(instruments_counter) > 20:
            print(f"... y {len(instruments_counter) - 20} instrumentos más")
        
        # Guardar resultados en CSV si se especificó
        if args.csv:
            try:
                import csv
                with open(args.csv, 'w', newline='', encoding='utf-8') as csvfile:
                    csv_writer = csv.writer(csvfile)
                    csv_writer.writerow(['Instrumento', 'Ocurrencias'])
                    for instrument, count in instruments_counter.most_common():
                        csv_writer.writerow([instrument, count])
                print(f"Resultados guardados en CSV: {args.csv}")
            except Exception as e:
                print(f"Error al guardar el CSV: {e}")
        
        # Generar histograma
        plot_histogram(instruments_counter, args.output, args.limit)
    else:
        print("No se encontraron instrumentos para analizar.")


if __name__ == "__main__":
    main()