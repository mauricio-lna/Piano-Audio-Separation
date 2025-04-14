#!/usr/bin/env python3
import os
import shutil
import re

def copy_metadata_files(source_dir, target_dir):
    """
    Copia los archivos metadata.yaml de cada subdirectorio 'Track' a un nuevo directorio
    y los renombra según el nombre de su carpeta de origen.
    
    Args:
        source_dir (str): Directorio que contiene las carpetas Track
        target_dir (str): Directorio donde se copiarán los archivos metadata.yaml
    """
    # Crear el directorio de destino si no existe
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
        print(f"Directorio creado: {target_dir}")
    
    # Patrón para identificar las carpetas "Track"
    track_pattern = re.compile(r'Track\d+')
    
    # Contar archivos copiados
    copied_files = 0
    
    # Recorrer todos los subdirectorios en el directorio fuente
    for item in os.listdir(source_dir):
        item_path = os.path.join(source_dir, item)
        
        # Verificar si es un directorio y coincide con el patrón "TrackXXXXX"
        if os.path.isdir(item_path) and track_pattern.match(item):
            # Ruta al archivo metadata.yaml dentro del directorio Track
            metadata_path = os.path.join(item_path, "metadata.yaml")
            
            # Verificar si existe el archivo metadata.yaml
            if os.path.exists(metadata_path):
                # Nombre del nuevo archivo (nombre del directorio Track + .yaml)
                new_filename = f"{item}.yaml"
                target_path = os.path.join(target_dir, new_filename)
                
                # Copiar el archivo
                shutil.copy2(metadata_path, target_path)
                copied_files += 1
                print(f"Copiado: {metadata_path} -> {target_path}")
    
    print(f"\nProceso completado. Se copiaron {copied_files} archivos.")

if __name__ == "__main__":
    # Directorio que contiene las carpetas Track
    source_directory = input("Ingresa la ruta del directorio fuente: ")
    
    # Directorio donde se copiarán los archivos metadata.yaml
    target_directory = input("Ingresa la ruta del directorio destino: ")
    
    copy_metadata_files(source_directory, target_directory)