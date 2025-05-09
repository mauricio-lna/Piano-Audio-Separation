import os
import re
from datetime import datetime

def renombrar_archivos(ruta):
    if not os.path.exists(ruta):
        print(f"La ruta '{ruta}' no existe.")
        return

    archivos_renombrados = 0
    archivos_ignorados = 0

    patron = re.compile(r'(.+?)_STEM.*')

    log_path = os.path.join(os.getcwd(), 'log_renombrado.txt')
    with open(log_path, 'w', encoding='utf-8') as log:
        log.write(f"LOG DE RENOMBRAMIENTO - {datetime.now()}\n")
        log.write(f"Ruta procesada: {ruta}\n\n")

        for carpeta_actual, _, archivos in os.walk(ruta):
            for archivo in archivos:
                coincidencia = patron.match(archivo)

                if coincidencia:
                    nuevo_nombre = coincidencia.group(1)
                    ruta_original = os.path.join(carpeta_actual, archivo)
                    ruta_nueva = os.path.join(carpeta_actual, nuevo_nombre)

                    _, extension = os.path.splitext(archivo)
                    if extension:
                        ruta_nueva += extension

                    if os.path.exists(ruta_nueva):
                        mensaje = f"Ignorado: '{archivo}' → '{os.path.basename(ruta_nueva)}' (ya existe)\n"
                        archivos_ignorados += 1
                    else:
                        os.rename(ruta_original, ruta_nueva)
                        mensaje = f"Renombrado: '{archivo}' → '{os.path.basename(ruta_nueva)}'\n"
                        archivos_renombrados += 1

                    print(mensaje.strip())
                    log.write(mensaje)

        log.write("\nResumen:\n")
        log.write(f"Archivos procesados: {archivos_renombrados + archivos_ignorados}\n")
        log.write(f"Archivos renombrados: {archivos_renombrados}\n")
        log.write(f"Archivos ignorados: {archivos_ignorados}\n")

    print(f"\nLog guardado en: {log_path}")

if __name__ == "__main__":
    ruta_archivos = input("Ingrese la ruta donde se encuentran los archivos: ")
    renombrar_archivos(ruta_archivos)
