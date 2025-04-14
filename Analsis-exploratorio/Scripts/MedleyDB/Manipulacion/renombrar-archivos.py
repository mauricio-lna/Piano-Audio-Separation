import os
import re

def renombrar_archivos(ruta):
    # Verificar si la ruta existe
    if not os.path.exists(ruta):
        print(f"La ruta '{ruta}' no existe.")
        return
    
    # Obtener lista de archivos en la ruta
    archivos = os.listdir(ruta)
    
    # Contador para estadísticas
    archivos_renombrados = 0
    archivos_ignorados = 0
    
    # Patrón para identificar archivos con '_STEM'
    patron = re.compile(r'(.+?)_STEM.*')
    
    for archivo in archivos:
        # Verificar si el archivo contiene '_STEM'
        coincidencia = patron.match(archivo)
        
        if coincidencia:
            # Obtener el nuevo nombre (sin '_STEM' y lo que sigue)
            nuevo_nombre = coincidencia.group(1)
            
            # Rutas completas
            ruta_original = os.path.join(ruta, archivo)
            ruta_nueva = os.path.join(ruta, nuevo_nombre)
            
            # Extensión del archivo original (si tiene)
            _, extension = os.path.splitext(archivo)
            if extension:
                ruta_nueva += extension
            
            # Verificar si ya existe un archivo con el nuevo nombre
            if os.path.exists(ruta_nueva):
                print(f"Ignorando: '{archivo}' → '{os.path.basename(ruta_nueva)}' (ya existe)")
                archivos_ignorados += 1
            else:
                # Renombrar el archivo
                os.rename(ruta_original, ruta_nueva)
                print(f"Renombrado: '{archivo}' → '{os.path.basename(ruta_nueva)}'")
                archivos_renombrados += 1
    
    # Mostrar estadísticas finales
    print("\nEstadísticas:")
    print(f"Archivos procesados: {archivos_renombrados + archivos_ignorados}")
    print(f"Archivos renombrados: {archivos_renombrados}")
    print(f"Archivos ignorados: {archivos_ignorados}")

if __name__ == "__main__":
    # Solicitar la ruta al usuario
    ruta_archivos = input("Ingrese la ruta donde se encuentran los archivos: ")
    
    # Ejecutar la función principal
    renombrar_archivos(ruta_archivos)