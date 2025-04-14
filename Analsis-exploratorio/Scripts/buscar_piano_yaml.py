#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Buscador de palabras en archivos YAML

Este script analiza todos los archivos YAML en un directorio específico,
busca las palabras "piano" o "Piano" en cada uno, y guarda los resultados
en un archivo CSV.
"""

import os
import csv
import yaml
import sys
from pathlib import Path

def buscar_palabra_en_archivo(ruta_archivo, palabras_buscar):
    """
    Busca una serie de palabras en un archivo YAML.
    
    Args:
        ruta_archivo (str): Ruta al archivo YAML a analizar
        palabras_buscar (list): Lista de palabras a buscar
        
    Returns:
        tuple: (nombre_archivo, contiene_palabra, lineas_encontradas)
            - nombre_archivo: Nombre del archivo analizado
            - contiene_palabra: Boolean que indica si se encontró alguna palabra
            - lineas_encontradas: Lista de tuplas (número_linea, contenido) donde se encontró alguna palabra
    """
    nombre_archivo = os.path.basename(ruta_archivo)
    lineas_encontradas = []
    
    try:
        # Primero verificamos con una búsqueda rápida de texto
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            contenido = archivo.read()
            
            # Verificación rápida para evitar procesar archivos sin coincidencias
            if not any(palabra in contenido for palabra in palabras_buscar):
                return nombre_archivo, False, []
            
            # Si hay posibles coincidencias, analizamos línea por línea para más detalles
            lineas = contenido.split('\n')
            for num_linea, linea in enumerate(lineas, 1):
                if any(palabra in linea for palabra in palabras_buscar):
                    lineas_encontradas.append((num_linea, linea.strip()))
        
        # La validación YAML es opcional pero útil para asegurar que son archivos YAML válidos
        try:
            yaml.safe_load(contenido)
        except yaml.YAMLError:
            # Si hay error en el YAML, agregamos una nota
            lineas_encontradas.append((0, "⚠️ El archivo no es un YAML válido pero contiene la palabra buscada"))
                
        return nombre_archivo, True, lineas_encontradas
    
    except Exception as e:
        # Manejar errores de lectura de archivo
        return nombre_archivo, False, [(0, f"Error al leer el archivo: {str(e)}")]

def main():
    # Configuración
    directorio = input("Introduce la ruta del directorio a analizar (presiona Enter para usar el directorio actual): ").strip()
    if not directorio:
        directorio = os.getcwd()
    
    palabras_buscar = ["piano", "Piano"]  # Palabras a buscar (distingue entre mayúsculas y minúsculas)
    archivo_salida = "archivos_con_piano.csv"
    
    # Buscar archivos YAML en el directorio
    archivos_yaml = []
    extensiones_yaml = ['.yaml', '.yml']
    
    print(f"\nBuscando archivos YAML en: {directorio}")
    for extension in extensiones_yaml:
        archivos_yaml.extend(list(Path(directorio).glob(f"**/*{extension}")))
    
    total_archivos = len(archivos_yaml)
    if total_archivos == 0:
        print("No se encontraron archivos YAML en el directorio especificado.")
        return
    
    print(f"Se encontraron {total_archivos} archivos YAML para analizar.")
    
    # Analizar archivos y recopilar resultados
    resultados = []
    archivos_con_coincidencias = 0
    
    print("\nAnalizando archivos...")
    for i, archivo in enumerate(archivos_yaml, 1):
        nombre_archivo, contiene_palabra, lineas = buscar_palabra_en_archivo(str(archivo), palabras_buscar)
        
        if contiene_palabra:
            archivos_con_coincidencias += 1
            ruta_relativa = os.path.relpath(archivo, directorio)
            
            # Para cada línea encontrada, agregamos una entrada en los resultados
            for num_linea, contenido_linea in lineas:
                resultados.append({
                    'archivo': ruta_relativa,
                    'linea': num_linea,
                    'contenido': contenido_linea
                })
        
        # Mostrar progreso
        if i % 10 == 0 or i == total_archivos:
            print(f"Progreso: {i}/{total_archivos} archivos analizados")
    
    # Guardar resultados en CSV
    if resultados:
        try:
            with open(archivo_salida, 'w', newline='', encoding='utf-8') as csv_file:
                campos = ['archivo', 'linea', 'contenido']
                writer = csv.DictWriter(csv_file, fieldnames=campos)
                writer.writeheader()
                writer.writerows(resultados)
            
            print(f"\n✓ Se encontraron coincidencias en {archivos_con_coincidencias} archivos.")
            print(f"✓ Resultados guardados en: {os.path.abspath(archivo_salida)}")
        except Exception as e:
            print(f"\n❌ Error al guardar el archivo CSV: {str(e)}")
    else:
        print("\nNo se encontraron coincidencias de 'piano' o 'Piano' en ningún archivo YAML.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nBúsqueda interrumpida por el usuario.")
    except Exception as e:
        print(f"\nError inesperado: {str(e)}")