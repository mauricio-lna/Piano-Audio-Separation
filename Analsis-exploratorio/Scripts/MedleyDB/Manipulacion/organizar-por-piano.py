import os
import shutil
import re

# Solicitar rutas al usuario
medley_dir = input("Ruta a 'Manipulacion-MedleyDB': ").strip()
dataset_dir = input("Ruta a 'dataset-final': ").strip()
instrumento_objetivo = input("Nombre del instrumento objetivo (ej. piano): ").strip()

# Ruta a los archivos de referencia
referencia_dir = os.path.join(dataset_dir, instrumento_objetivo)

# Verificar que exista la carpeta de referencia
if not os.path.isdir(referencia_dir):
    print(f"ERROR: No se encontró la carpeta: {referencia_dir}")
    exit(1)

# Función para normalizar nombres (quita _STEM y lo que sigue, conserva extensión)
def normalizar_nombre(nombre):
    return re.sub(r'_STEM.*(?=\.wav)', '', nombre)

# Crear conjunto de nombres de referencia normalizados
archivos_referencia = {
    normalizar_nombre(f) for f in os.listdir(referencia_dir) if f.endswith('.wav')
}

# Recorrer recursivamente Manipulacion-MedleyDB
for root, dirs, files in os.walk(medley_dir):
    for file in files:
        if not file.endswith('.wav'):
            continue

        nombre_normalizado = normalizar_nombre(file)

        if nombre_normalizado in archivos_referencia:
            ruta_origen = os.path.join(root, file)

            # Extraer el nombre de la subcarpeta (instrumento)
            instrumento = os.path.basename(os.path.dirname(ruta_origen))

            # Crear carpeta de destino si no existe
            destino_dir = os.path.join(dataset_dir, instrumento)
            os.makedirs(destino_dir, exist_ok=True)

            # Ruta destino con el nombre original
            ruta_destino = os.path.join(destino_dir, file)

            # Copiar si no existe
            if not os.path.exists(ruta_destino):
                shutil.copy2(ruta_origen, ruta_destino)
                print(f'Copiado: {ruta_origen} -> {ruta_destino}')
            else:
                print(f'Omitido (ya existe): {ruta_destino}')
