#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para organizar archivos STEM por instrumento.
Este script lee un archivo CSV con información sobre stems y los copia
a un nuevo directorio organizado por instrumentos.
"""

import os
import csv
import shutil
import argparse
from datetime import datetime


def normalize_name(instrument_name):
    """Normaliza el nombre del instrumento para usarlo como nombre de carpeta."""
    # Eliminar caracteres no válidos para nombres de carpeta
    name = instrument_name.replace('[', '').replace(']', '').replace('\'', '')
    name = name.replace(',', '_').replace('/', '_').strip()
    # Reemplazar espacios con guiones bajos
    return name.replace(' ', '_')


def main():
    parser = argparse.ArgumentParser(description='Organiza archivos STEM por instrumento.')
    parser.add_argument('csv_file', help='Archivo CSV con información de stems')
    parser.add_argument('ruta_origen', help='Ruta donde se encuentran las carpetas de origen')
    parser.add_argument('destino', help='Directorio donde se copiarán los archivos organizados')
    args = parser.parse_args()

    # Crear directorio de destino si no existe
    if not os.path.exists(args.destino):
        os.makedirs(args.destino)

    # Crear archivo de log
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(args.destino, f"log_organizar_stems_{timestamp}.txt")
    
    # Contadores para el informe final
    total_archivos = 0
    archivos_copiados = 0
    errores = 0

    with open(log_file, 'w', encoding='utf-8') as log:
        log.write(f"Log de organización de stems: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        log.write(f"Ruta de origen: {args.ruta_origen}\n")
        log.write(f"Ruta de destino: {args.destino}\n\n")
        
        # Leer el archivo CSV
        try:
            with open(args.csv_file, 'r', encoding='utf-8') as csv_file:
                reader = csv.DictReader(csv_file)
                
                for row in reader:
                    total_archivos += 1
                    carpeta = row['Nombre de la carpeta']
                    instrumento = row['Instrument']
                    stem_file = row['Posible archivo stem']
                    
                    # Normalizar nombre de instrumento para crear carpeta
                    instrumento_normalizado = normalize_name(instrumento)
                    
                    # Crear directorio para el instrumento si no existe
                    instrumento_dir = os.path.join(args.destino, instrumento_normalizado)
                    if not os.path.exists(instrumento_dir):
                        os.makedirs(instrumento_dir)
                    
                    # Construir ruta al archivo stem de origen
                    # Estructura: carpeta/carpeta_STEMS/archivo_stem.wav
                    origen_path = os.path.join(
                        args.ruta_origen,
                        carpeta,
                        f"{carpeta}_STEMS",
                        stem_file
                    )
                    
                    # Ruta de destino
                    destino_path = os.path.join(instrumento_dir, stem_file)
                    
                    # Copiar el archivo
                    try:
                        if os.path.exists(origen_path):
                            shutil.copy2(origen_path, destino_path)
                            log.write(f"COPIADO: {origen_path} -> {destino_path}\n")
                            archivos_copiados += 1
                        else:
                            log.write(f"ERROR: Archivo no encontrado: {origen_path}\n")
                            errores += 1
                    except Exception as e:
                        log.write(f"ERROR al copiar {origen_path}: {str(e)}\n")
                        errores += 1
        
        except Exception as e:
            log.write(f"ERROR al leer el archivo CSV: {str(e)}\n")
            print(f"ERROR: No se pudo leer el archivo CSV: {str(e)}")
            return
        
        # Escribir resumen en el log
        log.write("\n--- RESUMEN ---\n")
        log.write(f"Total de archivos procesados: {total_archivos}\n")
        log.write(f"Archivos copiados exitosamente: {archivos_copiados}\n")
        log.write(f"Errores encontrados: {errores}\n")
    
    print(f"Proceso completado. Se copiaron {archivos_copiados} de {total_archivos} archivos.")
    print(f"Se encontraron {errores} errores. Consulte el archivo de log para detalles: {log_file}")


if __name__ == "__main__":
    main()