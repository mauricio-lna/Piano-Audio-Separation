#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Procesador de CSV para eliminar registros duplicados

Este script lee un archivo CSV, elimina las filas duplicadas basándose en
la columna "archivo" y guarda los resultados únicos en un nuevo archivo CSV.
Está diseñado específicamente para procesar el archivo MedleyDBpiano.csv
que contiene registros de archivos YAML con la palabra "piano".
"""

import pandas as pd
import os
import sys
from datetime import datetime

def eliminar_duplicados(archivo_entrada, archivo_salida=None):
    """
    Lee un archivo CSV, elimina las filas con valores duplicados en la
    columna "archivo" y guarda los resultados en un nuevo archivo CSV.
    
    Args:
        archivo_entrada (str): Ruta al archivo CSV de entrada
        archivo_salida (str, optional): Ruta al archivo CSV de salida. 
                                        Si es None, se generará automáticamente.
    
    Returns:
        tuple: (archivo_salida, total_registros, registros_unicos, duplicados_eliminados)
    """
    try:
        # Verificar que el archivo de entrada existe
        if not os.path.isfile(archivo_entrada):
            print(f"Error: El archivo '{archivo_entrada}' no existe.")
            return None, 0, 0, 0
        
        # Leer el archivo CSV
        print(f"Leyendo el archivo: {archivo_entrada}")
        df = pd.read_csv(archivo_entrada)
        
        # Verificar que el CSV tiene la estructura esperada
        if "archivo" not in df.columns:
            print("Error: El archivo CSV no contiene la columna 'archivo'.")
            return None, 0, 0, 0
        
        # Obtener estadísticas antes de eliminar duplicados
        total_registros = len(df)
        print(f"Total de registros en el archivo original: {total_registros}")
        
        # Guardar los registros originales para posible referencia
        if archivo_salida is None:
            # Generar nombre automático con timestamp para evitar sobrescribir
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nombre_base = os.path.splitext(archivo_entrada)[0]
            archivo_salida = f"{nombre_base}_unicos_{timestamp}.csv"
        
        # Conservar el primer registro de cada archivo único
        df_sin_duplicados = df.drop_duplicates(subset=["archivo"])
        
        # Obtener estadísticas después de eliminar duplicados
        registros_unicos = len(df_sin_duplicados)
        duplicados_eliminados = total_registros - registros_unicos
        
        # Guardar el resultado en un nuevo archivo CSV
        df_sin_duplicados.to_csv(archivo_salida, index=False)
        print(f"Resultados guardados en: {archivo_salida}")
        
        return archivo_salida, total_registros, registros_unicos, duplicados_eliminados
    
    except Exception as e:
        print(f"Error al procesar el archivo: {str(e)}")
        return None, 0, 0, 0

def main():
    """Función principal del script."""
    # Determinar el archivo de entrada
    archivo_entrada = "MedleyDB-piano.csv"
    if not os.path.isfile(archivo_entrada):
        # Si no se encuentra en el directorio actual, solicitar al usuario
        print(f"No se encontró el archivo '{archivo_entrada}' en el directorio actual.")
        archivo_entrada = input("Introduce la ruta completa al archivo CSV: ").strip()
        if not archivo_entrada:
            print("No se proporcionó ningún archivo. Saliendo.")
            return
    
    # Determinar el archivo de salida
    archivo_salida = input(f"Introduce el nombre del archivo de salida (presiona Enter para generarlo automáticamente): ").strip()
    if not archivo_salida:
        archivo_salida = None
    
    # Procesar el archivo
    resultado, total, unicos, eliminados = eliminar_duplicados(archivo_entrada, archivo_salida)
    
    if resultado:
        # Mostrar resumen
        print("\n--- Resumen del procesamiento ---")
        print(f"Archivo de entrada: {archivo_entrada}")
        print(f"Archivo de salida: {resultado}")
        print(f"Total de registros originales: {total}")
        print(f"Registros únicos conservados: {unicos}")
        print(f"Registros duplicados eliminados: {eliminados}")
        print(f"Reducción: {(eliminados/total*100):.2f}%")
        
        # Verificar si hay duplicados
        if eliminados == 0:
            print("\nNo se encontraron archivos duplicados en el CSV.")
        else:
            print(f"\nSe eliminaron {eliminados} referencias duplicadas a archivos.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nOperación interrumpida por el usuario.")
    except Exception as e:
        print(f"\nError inesperado: {str(e)}")