import os
import yaml
import csv
import argparse
import glob

def find_piano_in_yaml(yaml_file_path):
    """
    Analiza un archivo YAML y encuentra los stems que contienen la palabra 'piano'
    en el nombre del programa MIDI o en la clase de instrumento.
    
    Args:
        yaml_file_path (str): Ruta al archivo YAML
        
    Returns:
        list: Lista de diccionarios con información de pianos encontrados
    """
    try:
        with open(yaml_file_path, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)
            
        track_name = os.path.basename(os.path.dirname(yaml_file_path))
        track_uuid = data.get('UUID', 'Desconocido')
        results = []
        
        # Recorrer todos los stems en el archivo
        for stem_id, stem_info in data.get('stems', {}).items():
            # Buscar la palabra "piano" en el nombre del programa MIDI o en la clase de instrumento
            midi_program = stem_info.get('midi_program_name', '').lower()
            inst_class = stem_info.get('inst_class', '').lower()
            
            if 'piano' in midi_program or 'piano' in inst_class:
                results.append({
                    'archivo': os.path.basename(yaml_file_path),
                    'directorio': os.path.dirname(yaml_file_path),
                    'track_name': track_name,
                    'uuid': track_uuid,
                    'stem_id': stem_id,
                    'instrumento': stem_info.get('midi_program_name', 'Desconocido'),
                    'clase': stem_info.get('inst_class', 'Desconocido'),
                    'plugin': stem_info.get('plugin_name', 'Desconocido'),
                    'programa': stem_info.get('program_num', 'Desconocido')
                })
                
        return results
    
    except Exception as e:
        print(f"Error al procesar el archivo {yaml_file_path}: {str(e)}")
        return []

def main():
    parser = argparse.ArgumentParser(description='Buscar pianos en archivos YAML')
    parser.add_argument('--dir', type=str, default='.', help='Directorio donde buscar archivos YAML')
    parser.add_argument('--output', type=str, default='pianos_encontrados.csv', help='Archivo CSV de salida')
    args = parser.parse_args()
    
    # Buscar todos los archivos YAML en el directorio especificado (incluyendo subdirectorios)
    yaml_files = glob.glob(os.path.join(args.dir, '**', '*.yaml'), recursive=True)
    yaml_files.extend(glob.glob(os.path.join(args.dir, '**', '*.yml'), recursive=True))
    
    if not yaml_files:
        print(f"No se encontraron archivos YAML en {args.dir}")
        return
    
    all_results = []
    for yaml_file in yaml_files:
        results = find_piano_in_yaml(yaml_file)
        all_results.extend(results)
    
    if not all_results:
        print("No se encontraron pianos en ningún archivo YAML")
        return
    
    # Escribir resultados en el archivo CSV
    with open(args.output, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['archivo', 'directorio', 'track_name', 'uuid', 'stem_id', 
                     'instrumento', 'clase', 'plugin', 'programa']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for result in all_results:
            writer.writerow(result)
    
    print(f"Se encontraron {len(all_results)} pianos en {len(set(r['archivo'] for r in all_results))} archivos")
    print(f"Resultados guardados en {args.output}")

if __name__ == "__main__":
    main()