
#!/usr/bin/env python3
import os
import shutil
import glob
import sys
import argparse

carpetaTracks = 'D:\\src\\Tesis (DEV)\\Datasets\\slakh2100_flac_redux\\validation'
carpetaResultado = 'D:\src\Tesis (DEV)\Datasets\Manipulacion-slakh2100\\validation'

def main():
    # Configurar el análisis de argumentos
    parser = argparse.ArgumentParser(description='Copia archivos "mix.flac" de carpetas Track* a una carpeta "train"')
    parser.add_argument('--source', '-s', default=carpetaTracks, help='Directorio que contiene las carpetas Track* (por defecto: directorio actual)')
    parser.add_argument('--destination', '-d', default=carpetaResultado, help='Directorio de destino donde se copiarán los archivos (por defecto: "./train")')
    
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
    track_folders = glob.glob("Track*")
    
    # Filtrar solo los directorios
    track_folders = [folder for folder in track_folders if os.path.isdir(folder)]
    
    if not track_folders:
        print(f"Advertencia: No se encontraron carpetas 'Track*' en '{abs_source_dir}'")
        os.chdir(original_dir)
        return 0
    
    # Procesar cada carpeta
    count = 0
    for folder in track_folders:
        mix_file = os.path.join(folder, "mix.flac")
        
        # Verificar que exista el archivo mix.flac dentro de la carpeta
        if os.path.isfile(mix_file):
            # Nombre del archivo de destino será el nombre de la carpeta con extensión .flac
            dest_filename = f"{folder}.flac"
            # Copiar el archivo mix.flac a la carpeta destino con el nombre de la carpeta
            shutil.copy2(mix_file, os.path.join(abs_dest_dir, dest_filename))
            print(f"Copiado: {mix_file} -> {os.path.join(abs_dest_dir, dest_filename)}")
            count += 1
        else:
            print(f"Advertencia: No se encontró el archivo 'mix.flac' en {folder}")
    
    # Volver al directorio original
    os.chdir(original_dir)
    
    print(f"Proceso completado. {count} archivos han sido copiados a la carpeta '{abs_dest_dir}'.")
    return 0

if __name__ == "__main__":
    sys.exit(main())