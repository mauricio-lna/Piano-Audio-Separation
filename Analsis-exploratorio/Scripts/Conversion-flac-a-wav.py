from pydub import AudioSegment
import os

def convert_flac_to_wav(input_path, output_path=None):
    if not input_path.lower().endswith('.flac'):
        raise ValueError("El archivo de entrada debe ser un archivo .flac")

    # Establecer el nombre del archivo de salida si no se proporciona
    if output_path is None:
        output_path = os.path.splitext(input_path)[0] + '.wav'

    try:
        # Cargar el archivo FLAC
        audio = AudioSegment.from_file(input_path, format="flac")
        # Exportar como WAV
        audio.export(output_path, format="wav")
        print(f"Conversión completada: {output_path}")
    except Exception as e:
        print(f"Ocurrió un error durante la conversión: {e}")

# Ejemplo de uso
if __name__ == "__main__":
    input_file = "D:\\src\\Piano-Audio-Separation\\Analsis-exploratorio\\Scripts\\Slakh2100\\Atributos\\output\\combined_audio_20250407_235259.flac"  # Cambia esto por la ruta a tu archivo FLAC
    convert_flac_to_wav(input_file)
