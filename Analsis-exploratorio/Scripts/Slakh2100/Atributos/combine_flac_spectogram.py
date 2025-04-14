#!/usr/bin/env python3
"""
Script para combinar múltiples archivos FLAC en uno solo y generar un espectrograma
del audio resultante.

Requisitos:
    - Python 3.6+
    - librosa
    - matplotlib
    - numpy
    - pydub
    - soundfile

Instalación de dependencias:
    pip install librosa matplotlib numpy pydub soundfile

    Ruta
    D:\src\Datasets\Datasets\Manipulacion-slakh2100\train\Piano
"""

import os
import argparse
import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf
from pydub import AudioSegment
import librosa
import librosa.display
import tempfile
import time
import shutil
from datetime import datetime

def list_flac_files(directory):
    """
    Lista todos los archivos FLAC en un directorio.
    
    Args:
        directory (str): Ruta al directorio
        
    Returns:
        list: Lista de rutas completas a los archivos FLAC
    """
    flac_files = []
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.flac'):
                flac_files.append(os.path.join(root, file))
    
    return sorted(flac_files)

def combine_flac_files(flac_files, output_file):
    """
    Combina múltiples archivos FLAC en uno solo.
    
    Args:
        flac_files (list): Lista de rutas a los archivos FLAC
        output_file (str): Ruta al archivo de salida
        
    Returns:
        str: Ruta al archivo combinado
    """
    if not flac_files:
        raise ValueError("No se encontraron archivos FLAC para combinar")
    
    print(f"Combinando {len(flac_files)} archivos FLAC...")
    
    # Inicializar con el primer archivo
    combined = AudioSegment.from_file(flac_files[0], format="flac")
    print(f"  [1/{len(flac_files)}] Añadido: {os.path.basename(flac_files[0])}")
    
    # Añadir el resto de archivos
    for i, flac_file in enumerate(flac_files[1:], 2):
        try:
            audio = AudioSegment.from_file(flac_file, format="flac")
            combined += audio
            print(f"  [{i}/{len(flac_files)}] Añadido: {os.path.basename(flac_file)}")
        except Exception as e:
            print(f"  Error al procesar {flac_file}: {e}")
    
    # Guardar el archivo combinado
    print(f"Guardando archivo combinado en: {output_file}")
    combined.export(output_file, format="flac")
    
    return output_file

def generate_spectrogram(audio_file, output_file, n_fft=2048, hop_length=512, y_axis='log', cmap='viridis'):
    """
    Genera un espectrograma a partir de un archivo de audio.
    
    Args:
        audio_file (str): Ruta al archivo de audio
        output_file (str): Ruta donde guardar el espectrograma
        n_fft (int): Tamaño de la ventana FFT
        hop_length (int): Número de muestras entre frames
        y_axis (str): Escala del eje Y ('linear' o 'log')
        cmap (str): Mapa de colores
        
    Returns:
        str: Ruta al archivo de espectrograma
    """
    print(f"Generando espectrograma para: {audio_file}")
    print("  Cargando audio (esto puede tardar un poco para archivos grandes)...")
    
    # Cargar el archivo de audio
    y, sr = librosa.load(audio_file, sr=None)
    
    # Configurar el tamaño de la figura según la duración del audio
    duration = len(y) / sr
    fig_width = max(10, min(20, duration / 60))  # Anchura basada en la duración en minutos
    
    print(f"  Duración del audio: {duration:.2f} segundos")
    print(f"  Frecuencia de muestreo: {sr} Hz")
    print(f"  Generando espectrograma con n_fft={n_fft}, hop_length={hop_length}, escala={y_axis}...")
    
    # Crear la figura
    plt.figure(figsize=(fig_width, 8))
    
    # Calcular el espectrograma
    D = librosa.amplitude_to_db(np.abs(librosa.stft(y, n_fft=n_fft, hop_length=hop_length)), ref=np.max)
    
    # Mostrar el espectrograma
    librosa.display.specshow(D, sr=sr, hop_length=hop_length, x_axis='time', y_axis=y_axis, cmap=cmap)
    
    # Añadir barra de color y etiquetas
    plt.colorbar(format='%+2.0f dB')
    plt.title(f'Espectrograma - {os.path.basename(audio_file)}')
    plt.xlabel('Tiempo')
    plt.ylabel('Frecuencia (Hz)')
    
    # Guardar la figura
    plt.tight_layout()
    plt.savefig(output_file, dpi=300)
    plt.close()
    
    print(f"Espectrograma guardado en: {output_file}")
    
    return output_file

def main():
    """Función principal del script"""
    parser = argparse.ArgumentParser(description='Combina archivos FLAC y genera un espectrograma')
    parser.add_argument('directory', help='Directorio que contiene los archivos FLAC')
    parser.add_argument('--output-dir', '-o', default='output', help='Directorio de salida')
    parser.add_argument('--n-fft', type=int, default=2048, help='Tamaño de la ventana FFT')
    parser.add_argument('--hop-length', type=int, default=512, help='Número de muestras entre frames')
    parser.add_argument('--y-axis', choices=['linear', 'log'], default='log', help='Escala del eje Y')
    parser.add_argument('--cmap', default='viridis', help='Mapa de colores para el espectrograma')
    parser.add_argument('--keep-combined', action='store_true', help='Mantener el archivo de audio combinado')
    
    args = parser.parse_args()
    
    # Crear directorio de salida si no existe
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)
    
    # Crear un identificador único para esta ejecución
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Rutas de salida
    combined_audio_file = os.path.join(args.output_dir, f"combined_audio_{timestamp}.flac")
    spectrogram_file = os.path.join(args.output_dir, f"spectrogram_{timestamp}.png")
    
    try:
        # Listar archivos FLAC
        flac_files = list_flac_files(args.directory)
        
        if not flac_files:
            print(f"No se encontraron archivos FLAC en el directorio: {args.directory}")
            return
        
        print(f"Se encontraron {len(flac_files)} archivos FLAC")
        
        # Combinar archivos
        combined_file = combine_flac_files(flac_files, combined_audio_file)
        
        # Generar espectrograma
        generate_spectrogram(
            combined_file, 
            spectrogram_file,
            n_fft=args.n_fft,
            hop_length=args.hop_length,
            y_axis=args.y_axis,
            cmap=args.cmap
        )
        
        # Eliminar archivo combinado si no se especificó mantenerlo
        if not args.keep_combined:
            print("Eliminando archivo de audio combinado...")
            os.remove(combined_file)
        
        print("\nProceso completado con éxito!")
        print(f"Espectrograma guardado en: {spectrogram_file}")
        if args.keep_combined:
            print(f"Audio combinado guardado en: {combined_file}")
            
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    main()