#!/usr/bin/env python3
import os
import sys
from mutagen.flac import FLAC
from datetime import timedelta

def calcular_duracion_media(directorio):
    """
    Calcula la duración media de todos los archivos FLAC en el directorio especificado.
    
    Args:
        directorio (str): Ruta al directorio que contiene los archivos FLAC
    
    Returns:
        tuple: (duracion_media, lista_de_archivos_con_duracion)
    """
    if not os.path.isdir(directorio):
        print(f"Error: '{directorio}' no es un directorio válido.")
        sys.exit(1)
        
    archivos_flac = []
    duracion_total = 0
    contador = 0
    
    print(f"Analizando archivos FLAC en: {directorio}")
    print("-" * 60)
    
    # Recorrer todos los archivos en el directorio
    for archivo in os.listdir(directorio):
        ruta_completa = os.path.join(directorio, archivo)
        
        # Verificar si es un archivo y tiene extensión .flac
        if os.path.isfile(ruta_completa) and archivo.lower().endswith('.flac'):
            try:
                # Leer metadatos del archivo FLAC
                audio = FLAC(ruta_completa)
                duracion = audio.info.length  # duración en segundos
                
                # Formatear la duración para mostrarla
                duracion_formateada = str(timedelta(seconds=int(duracion)))
                
                # Guardar información del archivo
                info_archivo = {
                    'nombre': archivo,
                    'duracion_segundos': duracion,
                    'duracion_formateada': duracion_formateada
                }
                
                archivos_flac.append(info_archivo)
                duracion_total += duracion
                contador += 1
                
                # Mostrar información del archivo actual
                print(f"Archivo {contador}: {archivo}")
                print(f"  Duración: {duracion_formateada}")
                
            except Exception as e:
                print(f"Error al procesar el archivo {archivo}: {e}")
    
    print("-" * 60)
    
    # Calcular la duración media si hay archivos
    if contador > 0:
        duracion_media = duracion_total / contador
        duracion_media_formateada = str(timedelta(seconds=int(duracion_media)))
        
        print(f"Total de archivos FLAC analizados: {contador}")
        print(f"Duración total: {str(timedelta(seconds=int(duracion_total)))}")
        print(f"Duración media: {duracion_media_formateada} ({duracion_media:.2f} segundos)")
    else:
        print("No se encontraron archivos FLAC en el directorio especificado.")
        duracion_media = 0
    
    return duracion_media, archivos_flac

if __name__ == "__main__":
    # Verificar si se proporcionó un directorio como argumento
    if len(sys.argv) != 2:
        print("Uso: python calcular_duracion_flac.py <directorio>")
        sys.exit(1)
    
    directorio = sys.argv[1]
    calcular_duracion_media(directorio)