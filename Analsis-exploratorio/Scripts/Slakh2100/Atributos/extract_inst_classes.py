#!/usr/bin/env python3
"""
Script para analizar archivos YAML y extraer los diferentes tipos de inst_class.
Este script recorre un directorio y sus subdirectorios buscando archivos YAML
y lista las diferentes clases de instrumentos encontradas.
"""
import os
import sys
import yaml
import argparse
from collections import Counter

def extract_inst_classes(yaml_file_path):
    """
    Extrae los inst_class de un archivo YAML.
    
    Args:
        yaml_file_path (str): Ruta al archivo YAML a analizar
        
    Returns:
        list: Lista de inst_class encontrados
    """
    try:
        with open(yaml_file_path, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)
            
        inst_classes = []
        
        # Verifica si el archivo tiene una estructura esperada con 'stems'
        if 'stems' in data and isinstance(data['stems'], dict):
            for stem_id, stem_data in data['stems'].items():
                if 'inst_class' in stem_data:
                    inst_classes.append(stem_data['inst_class'])
        
        return inst_classes
    
    except Exception as e:
        print(f"Error al procesar {yaml_file_path}: {e}")
        return []

def analyze_directory(directory_path):
    """
    Analiza todos los archivos YAML en un directorio y sus subdirectorios.
    
    Args:
        directory_path (str): Ruta al directorio que contiene los archivos YAML
        
    Returns:
        dict: Diccionario con estadísticas sobre los inst_class encontrados
    """
    if not os.path.isdir(directory_path):
        print(f"Error: '{directory_path}' no es un directorio válido.")
        sys.exit(1)
    
    all_inst_classes = []
    processed_files = 0
    yaml_files = 0
    
    print(f"Analizando archivos YAML en: {directory_path}")
    print("-" * 60)
    
    # Recorrer el directorio y sus subdirectorios
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.lower().endswith(('.yaml', '.yml')):
                yaml_files += 1
                file_path = os.path.join(root, file)
                
                print(f"Procesando: {file_path}")
                inst_classes = extract_inst_classes(file_path)
                
                if inst_classes:
                    all_inst_classes.extend(inst_classes)
                    processed_files += 1
    
    print("-" * 60)
    
    # Contar las ocurrencias de cada inst_class
    inst_counter = Counter(all_inst_classes)
    
    # Ordenar por frecuencia (de mayor a menor)
    sorted_insts = inst_counter.most_common()
    
    return {
        'unique_insts': sorted_insts,
        'total_occurrences': len(all_inst_classes),
        'processed_files': processed_files,
        'yaml_files': yaml_files
    }

def display_results(results):
    """
    Muestra los resultados del análisis.
    
    Args:
        results (dict): Resultados del análisis
    """
    unique_insts = results['unique_insts']
    total = results['total_occurrences']
    processed = results['processed_files']
    yaml_files = results['yaml_files']
    
    print(f"\nResumen del análisis:")
    print(f"  Archivos YAML encontrados: {yaml_files}")
    print(f"  Archivos YAML procesados: {processed}")
    print(f"  Total de inst_class encontrados: {total}")
    print(f"  Tipos únicos de inst_class: {len(unique_insts)}")
    
    if unique_insts:
        print("\nLista de inst_class encontrados (ordenados por frecuencia):")
        print("-" * 60)
        print(f"{'Instrument Class':<40} | {'Ocurrencias':<10} | {'Porcentaje':<10}")
        print("-" * 60)
        
        for inst, count in unique_insts:
            percentage = (count / total) * 100 if total > 0 else 0
            print(f"{inst:<40} | {count:<10} | {percentage:.2f}%")
    else:
        print("\nNo se encontraron inst_class en los archivos YAML procesados.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Analiza archivos YAML para identificar tipos de inst_class')
    parser.add_argument('directory', help='Directorio que contiene los archivos YAML a analizar')
    parser.add_argument('--output', '-o', help='Archivo para guardar resultados (opcional)')
    
    args = parser.parse_args()
    
    results = analyze_directory(args.directory)
    display_results(results)
    
    # Guardar resultados en archivo si se especificó
    if args.output:
        try:
            with open(args.output, 'w', encoding='utf-8') as outfile:
                outfile.write("Tipos de inst_class encontrados:\n\n")
                
                for inst, count in results['unique_insts']:
                    percentage = (count / results['total_occurrences']) * 100 if results['total_occurrences'] > 0 else 0
                    outfile.write(f"{inst}: {count} ({percentage:.2f}%)\n")
                
                outfile.write(f"\nTotal de inst_class: {results['total_occurrences']}\n")
                outfile.write(f"Archivos YAML procesados: {results['processed_files']}/{results['yaml_files']}\n")
            
            print(f"\nResultados guardados en: {args.output}")
        except Exception as e:
            print(f"Error al guardar los resultados: {e}")