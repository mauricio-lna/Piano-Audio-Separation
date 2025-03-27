import os
import yaml
import csv
import argparse
import glob

def find_piano_in_yaml(yaml_file_path):
    """
    Analiza un archivo YAML y encuentra los stems que contienen la palabra 'piano'
    en el nombre del programa MIDI, la clase de instrumento o el campo 'instrument'.
    
    Compatible con dos formatos diferentes de archivos YAML:
    1. Formato con campos UUID, inst_class, midi_program_name (metadata_X.yaml)
    2. Formato con campos artist, title e instrument (ArtistName_SongTitle_METADATA.yaml)
    
    Args:
        yaml_file_path (str): Ruta al archivo YAML
        
    Returns:
        list: Lista de diccionarios con información de pianos encontrados
    """
    try:
        with open(yaml_file_path, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)
            
        track_name = os.path.basename(os.path.dirname(yaml_file_path))
        # Intentar obtener información del track según el formato del archivo
        track_uuid = data.get('UUID', 'N/A')
        artist = data.get('artist', 'Desconocido')
        title = data.get('title', 'Desconocido')
        
        results = []
        
        # Detectar el tipo de formato del archivo YAML
        format_type = 1  # Por defecto, asumimos formato tipo 1 (metadata_X.yaml)
        if 'artist' in data and 'title' in data and any(stem.get('instrument') for stem_id, stem in data.get('stems', {}).items()):
            format_type = 2  # Formato tipo 2 (ArtistName_SongTitle_METADATA.yaml)
        
        # Recorrer todos los stems en el archivo
        for stem_id, stem_info in data.get('stems', {}).items():
            found_piano = False
            
            if format_type == 1:
                # Formato 1: Buscar en midi_program_name o inst_class
                midi_program = stem_info.get('midi_program_name', '').lower() if isinstance(stem_info.get('midi_program_name', ''), str) else ''
                inst_class = stem_info.get('inst_class', '').lower() if isinstance(stem_info.get('inst_class', ''), str) else ''
                
                if 'piano' in midi_program or 'piano' in inst_class:
                    found_piano = True
                    
                    results.append({
                        'archivo': os.path.basename(yaml_file_path),
                        'directorio': os.path.dirname(yaml_file_path),
                        'track_name': track_name,
                        'artist': 'N/A',
                        'title': 'N/A',
                        'uuid': track_uuid,
                        'stem_id': stem_id,
                        'instrumento': stem_info.get('midi_program_name', 'Desconocido'),
                        'clase': stem_info.get('inst_class', 'Desconocido'),
                        'plugin': stem_info.get('plugin_name', 'Desconocido'),
                        'programa': stem_info.get('program_num', 'Desconocido')
                    })
            
            elif format_type == 2:
                # Formato 2: Buscar en instrument
                instrument = stem_info.get('instrument', '')
                
                # El instrument puede ser una lista o un string
                if isinstance(instrument, list):
                    instruments_text = ' '.join([str(i).lower() for i in instrument])
                else:
                    instruments_text = str(instrument).lower()
                
                if 'piano' in instruments_text:
                    found_piano = True
                    
                    # También buscar en los RAW para obtener más detalles
                    raw_details = []
                    for raw_id, raw_info in stem_info.get('raw', {}).items():
                        raw_inst = raw_info.get('instrument', '')
                        if isinstance(raw_inst, list):
                            raw_inst = ', '.join(raw_inst)
                        raw_details.append(f"{raw_id}: {raw_inst}")
                    
                    results.append({
                        'archivo': os.path.basename(yaml_file_path),
                        'directorio': os.path.dirname(yaml_file_path),
                        'track_name': track_name,
                        'artist': artist,
                        'title': title,
                        'uuid': track_uuid,
                        'stem_id': stem_id,
                        'instrumento': instrument if isinstance(instrument, str) else ', '.join(instrument),
                        'clase': stem_info.get('component', 'N/A'),
                        'plugin': 'N/A',
                        'programa': 'N/A',
                        'filename': stem_info.get('filename', 'N/A'),
                        'raw_details': '; '.join(raw_details) if raw_details else 'N/A'
                    })
                
        return results
    
    except Exception as e:
        print(f"Error al procesar el archivo {yaml_file_path}: {str(e)}")
        return []

def main():
    parser = argparse.ArgumentParser(description='Buscar pianos en archivos YAML')
    parser.add_argument('--dir', type=str, default='.', help='Directorio donde buscar archivos YAML')
    parser.add_argument('--output', type=str, default='pianos_encontrados.csv', help='Archivo CSV de salida')
    parser.add_argument('--format', type=int, choices=[0, 1, 2], default=0, 
                       help='Formato: 0=Auto-detectar, 1=metadata_X.yaml, 2=ArtistName_SongTitle_METADATA.yaml')
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
        # Determinar los campos del CSV basados en los resultados
        # (pueden variar dependiendo del formato de los archivos procesados)
        all_fields = set()
        for result in all_results:
            all_fields.update(result.keys())
        
        fieldnames = ['archivo', 'directorio', 'track_name', 'artist', 'title', 'uuid', 'stem_id', 
                     'instrumento', 'clase', 'plugin', 'programa', 'filename']
        
        # Asegurarse de que todos los campos necesarios están incluidos
        for field in all_fields:
            if field not in fieldnames:
                fieldnames.append(field)
        
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for result in all_results:
            # Asegurarse de que todos los campos existen en cada resultado
            for field in fieldnames:
                if field not in result:
                    result[field] = 'N/A'
            writer.writerow(result)
    
    print(f"Se encontraron {len(all_results)} pianos en {len(set(r['archivo'] for r in all_results))} archivos")
    print(f"Resultados guardados en {args.output}")

if __name__ == "__main__":
    main()