#!/usr/bin/env python3
import os
import csv
import yaml
import glob
import argparse

def process_yaml_file(file_path):
    """
    Procesa un archivo YAML y extrae la información de stems e instrumentos.
    
    Args:
        file_path (str): Ruta al archivo YAML
        
    Returns:
        list: Lista de filas para el CSV con [nombre_archivo, instrumento, stem, posible_archivo_stem]
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)
            
        # Obtener el nombre base del archivo
        file_name = os.path.basename(file_path)
        # Remover "_METADATA.yaml" del nombre
        if file_name.endswith("_METADATA.yaml"):
            file_name = file_name.replace("_METADATA.yaml", "")
        
        rows = []
        
        # Solo procesamos la sección 'stems'
        if 'stems' in data:
            for stem_id, stem_info in data['stems'].items():
                if 'instrument' in stem_info:
                    # Extraer el número de stem sin la 'S'
                    stem_number = stem_id[1:].zfill(2)  # Elimina la 'S' y asegura que tenga 2 dígitos
                    
                    # Crear el posible nombre de archivo stem
                    posible_stem = f"{file_name}_STEM_{stem_number}.wav"
                    
                    rows.append([
                        file_name,
                        stem_info['instrument'],
                        stem_id,
                        posible_stem
                    ])
        
        return rows
    except Exception as e:
        print(f"Error al procesar {file_path}: {e}")
        return []

def main():
    parser = argparse.ArgumentParser(description='Convierte archivos YAML a CSV extrayendo información de stems e instrumentos')
    parser.add_argument('input_dir', help='Directorio que contiene los archivos YAML')
    parser.add_argument('output_file', help='Archivo CSV de salida')
    
    args = parser.parse_args()
    
    # Verificar que el directorio existe
    if not os.path.isdir(args.input_dir):
        print(f"Error: El directorio '{args.input_dir}' no existe")
        return
    
    # Obtener todos los archivos YAML en el directorio
    yaml_files = glob.glob(os.path.join(args.input_dir, "*.yaml"))
    yaml_files.extend(glob.glob(os.path.join(args.input_dir, "*.yml")))
    
    if not yaml_files:
        print(f"No se encontraron archivos YAML en '{args.input_dir}'")
        return
    
    # Preparar el CSV
    with open(args.output_file, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        # Escribir encabezados
        csv_writer.writerow(['Nombre de la carpeta', 'Instrument', 'Stem', 'Posible archivo stem'])
        
        # Procesar cada archivo YAML
        total_rows = 0
        for yaml_file in yaml_files:
            rows = process_yaml_file(yaml_file)
            for row in rows:
                csv_writer.writerow(row)
                total_rows += 1
    
    print(f"Proceso completado. Se procesaron {len(yaml_files)} archivos YAML y se escribieron {total_rows} filas en '{args.output_file}'")

if __name__ == "__main__":
    main()