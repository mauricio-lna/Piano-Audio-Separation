import os
import sys
import glob

def renombrar_archivos(carpeta):
    """
    Renombra archivos FLAC eliminando el guion bajo y todo lo que le sigue.
    Ejemplo: Track00001_S02.flac -> Track00001.flac
    
    Args:
        carpeta (str): Ruta a la carpeta que contiene los archivos FLAC
    """
    # Verificar que la carpeta existe
    if not os.path.isdir(carpeta):
        print(f"Error: La carpeta '{carpeta}' no existe.")
        return
    
    # Buscar todos los archivos FLAC en la carpeta
    archivos_flac = glob.glob(os.path.join(carpeta, "*.flac"))
    
    if not archivos_flac:
        print(f"No se encontraron archivos FLAC en la carpeta '{carpeta}'.")
        return
    
    contador = 0
    
    for archivo in archivos_flac:
        # Obtener el nombre del archivo sin la ruta
        nombre_archivo = os.path.basename(archivo)
        
        # Verificar si el archivo contiene guion bajo
        if "_" in nombre_archivo:
            # Obtener el nuevo nombre (todo antes del guion bajo)
            nuevo_nombre = nombre_archivo.split("_")[0] + ".flac"
            
            # Ruta completa del nuevo archivo
            nueva_ruta = os.path.join(carpeta, nuevo_nombre)
            
            # Renombrar el archivo
            try:
                os.rename(archivo, nueva_ruta)
                print(f"Renombrado: {nombre_archivo} -> {nuevo_nombre}")
                contador += 1
            except Exception as e:
                print(f"Error al renombrar {nombre_archivo}: {e}")
    
    print(f"\nProceso completado. Se renombraron {contador} archivos.")

if __name__ == "__main__":
    # Verificar si se proporcionó una carpeta como argumento
    if len(sys.argv) > 1:
        carpeta = sys.argv[1]
        renombrar_archivos(carpeta)
    else:
        # Si no se proporciona argumento, usar la carpeta actual
        carpeta = input("Ingrese la ruta de la carpeta (o presione Enter para usar la carpeta actual): ")
        if not carpeta:
            carpeta = "."
        renombrar_archivos(carpeta)