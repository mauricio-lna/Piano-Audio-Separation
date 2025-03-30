#!/usr/bin/env python3
import os
import shutil
import glob
import sys
import argparse
import yaml

carpetaTracks = "D:\\src\\Tesis (DEV)\\Datasets\\slakh2100_flac_redux\\validation"
carpetaPiano = "D:\\src\\Tesis (DEV)\\Datasets\\Manipulacion-slakh2100\\validation\Piano"

def main():
    # Configurar el análisis de argumentos
    parser = argparse.ArgumentParser(description='Copia archivos de stems de Bright Acoustic Piano de carpetas Track* a un directorio destino')
    parser.add_argument('--source', '-s', default=carpetaTracks, help='Directorio que contiene las carpetas Track* (por defecto: directorio actual)')
    parser.add_argument('--destination', '-d', default=carpetaPiano, help='Directorio de destino donde se copiarán los archivos (por defecto: "./piano_stems")')
    
    # Analizar los argumentos
    args = parser.parse_args()
    
    source_dir = args.source
    dest_dir = args.destination
    
    # Verificar que el directorio fuente existe
    if not os.path.exists(source_dir):
        print(f"Error: El directorio fuente '{source_dir}' no existe.")
        return 1
        
    # Verificar si la carpeta destino existe, si no, crearla
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
        print(f"Carpeta '{dest_dir}' creada.")
    
    # Obtener la ruta absoluta del directorio fuente
    abs_source_dir = os.path.abspath(source_dir)
    
    # Obtener la ruta absoluta del directorio destino
    abs_dest_dir = os.path.abspath(dest_dir)
    
    # Cambiar al directorio fuente para la búsqueda
    original_dir = os.getcwd()
    os.chdir(abs_source_dir)
    
    # Buscar todas las carpetas que empiezan con "Track"
    track_folders = sorted(glob.glob("Track*"))
    
    # Filtrar solo los directorios
    track_folders = [folder for folder in track_folders if os.path.isdir(folder)]
    
    if not track_folders:
        print(f"Advertencia: No se encontraron carpetas 'Track*' en '{abs_source_dir}'")
        os.chdir(original_dir)
        return 0
    
    # Procesar cada carpeta de Track
    count = 0
    for track_folder in track_folders:
        print(f"Procesando {track_folder}...")
        
        # Verificar que existe el archivo metadata.yaml
        yaml_path = os.path.join(track_folder, "metadata.yaml")
        if not os.path.isfile(yaml_path):
            print(f"  Advertencia: No se encontró el archivo 'metadata.yaml' en {track_folder}")
            continue
        
        # Leer el archivo YAML
        try:
            with open(yaml_path, 'r') as yaml_file:
                metadata = yaml.safe_load(yaml_file)
        except Exception as e:
            print(f"  Error al leer el archivo YAML en {track_folder}: {e}")
            continue
        
        # Verificar que existe la sección stems
        if 'stems' not in metadata:
            print(f"  Advertencia: No se encontró la sección 'stems' en el YAML de {track_folder}")
            continue
        
        # Buscar los stems con midi_program_name = "Bright Acoustic Piano"
        piano_stems = []
        for stem_id, stem_data in metadata['stems'].items():
            if 'midi_program_name' in stem_data and stem_data['midi_program_name'] == 'Bright Acoustic Piano':
                piano_stems.append(stem_id)
        
        if not piano_stems:
            print(f"  No se encontraron stems de 'Bright Acoustic Piano' en {track_folder}")
            continue
        
        print(f"  Stems de Bright Acoustic Piano encontrados: {', '.join(piano_stems)}")
        
        # Verificar que existe la carpeta stems
        stems_dir = os.path.join(track_folder, "stems")
        if not os.path.isdir(stems_dir):
            print(f"  Advertencia: No se encontró la carpeta 'stems' en {track_folder}")
            continue
        
        # Copiar cada archivo de stem de piano
        for stem_id in piano_stems:
            stem_file = os.path.join(stems_dir, f"{stem_id}.flac")
            
            # Verificar que existe el archivo del stem
            if not os.path.isfile(stem_file):
                print(f"  Advertencia: No se encontró el archivo '{stem_id}.flac' en {stems_dir}")
                continue
            
            # Nombre del archivo de destino será: TrackXXXXX_SXX.flac
            dest_filename = f"{track_folder}_{stem_id}.flac"
            dest_path = os.path.join(abs_dest_dir, dest_filename)
            
            # Copiar el archivo
            try:
                shutil.copy2(stem_file, dest_path)
                print(f"  Copiado: {stem_file} -> {dest_path}")
                count += 1
            except Exception as e:
                print(f"  Error al copiar {stem_file}: {e}")
    
    # Volver al directorio original
    os.chdir(original_dir)
    
    print(f"Proceso completado. {count} archivos de stems de 'Bright Acoustic Piano' han sido copiados a la carpeta '{abs_dest_dir}'.")
    return 0

if __name__ == "__main__":
    sys.exit(main())