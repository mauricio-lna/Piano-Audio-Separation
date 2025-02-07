import os
import shutil

def copiar_archivos_yaml_recursivo(origen, destino):
    """
    Copia todos los archivos YAML de manera recursiva de la carpeta origen a la carpeta destino,
    manejando nombres duplicados.

    :param origen: Ruta de la carpeta origen
    :param destino: Ruta de la carpeta destino
    """
    if not os.path.exists(origen):
        print(f"La carpeta origen '{origen}' no existe.")
        return

    if not os.path.exists(destino):
        os.makedirs(destino)

    for root, _, files in os.walk(origen):
        for file in files:
            if file.endswith('.yaml'):
                ruta_origen = os.path.join(root, file)

                # Manejar nombres duplicados
                ruta_destino = os.path.join(destino, file)
                contador = 1
                while os.path.exists(ruta_destino):
                    nombre, extension = os.path.splitext(file)
                    ruta_destino = os.path.join(destino, f"{nombre}_{contador}{extension}")
                    contador += 1

                shutil.copy2(ruta_origen, ruta_destino)
                print(f"Archivo copiado: {ruta_origen} -> {ruta_destino}")

    print(f"Copia completada de archivos YAML desde '{origen}' hacia '{destino}'.")

# Ejemplo de uso
if __name__ == "__main__":
    ruta_origen = input("Ingresa la ruta de la carpeta origen: ")
    ruta_destino = input("Ingresa la ruta de la carpeta destino: ")

    copiar_archivos_yaml_recursivo(ruta_origen, ruta_destino)