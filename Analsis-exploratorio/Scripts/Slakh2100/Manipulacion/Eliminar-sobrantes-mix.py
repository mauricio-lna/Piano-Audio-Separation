import os
import sys
import glob
import re

def obtener_archivos_base(carpeta_piano):
    """
    Obtiene los nombres base de los archivos en la carpeta Piano,
    ignorando el sufijo '_S##' si existe.
    
    Args:
        carpeta_piano (str): Ruta a la carpeta Piano
    
    Returns:
        set: Conjunto con los nombres base de los archivos
    """
    if not os.path.isdir(carpeta_piano):
        print(f"Error: La carpeta '{carpeta_piano}' no existe.")
        return set()
    
    archivos_piano = glob.glob(os.path.join(carpeta_piano, "*.flac"))
    nombres_base = set()
    
    for archivo in archivos_piano:
        nombre = os.path.basename(archivo)
        # Eliminar la extensión
        nombre_sin_extension = os.path.splitext(nombre)[0]
        
        # Si tiene el formato Track#####_S##, extraer solo la parte Track#####
        if "_S" in nombre_sin_extension:
            nombre_base = nombre_sin_extension.split("_S")[0]
        else:
            nombre_base = nombre_sin_extension
            
        nombres_base.add(nombre_base)
    
    return nombres_base

def eliminar_archivos_no_coincidentes(carpeta_principal, carpeta_piano):
    """
    Elimina los archivos FLAC en la carpeta principal que no coincidan
    con los nombres base de los archivos en la carpeta Piano.
    Ignora cualquier sufijo que comience con "_" en ambas carpetas.
    
    Args:
        carpeta_principal (str): Ruta a la carpeta principal
        carpeta_piano (str): Ruta a la carpeta Piano
    """
    # Verificar que la carpeta principal existe
    if not os.path.isdir(carpeta_principal):
        print(f"Error: La carpeta principal '{carpeta_principal}' no existe.")
        return
    
    # Obtener los nombres base de los archivos en Piano
    nombres_piano = obtener_archivos_base(carpeta_piano)
    
    if not nombres_piano:
        print("No se encontraron archivos FLAC válidos en la carpeta Piano.")
        return
    
    print(f"Archivos encontrados en Piano: {len(nombres_piano)}")
    
    # Buscar todos los archivos FLAC en la carpeta principal
    archivos_principal = glob.glob(os.path.join(carpeta_principal, "*.flac"))
    
    if not archivos_principal:
        print("No se encontraron archivos FLAC en la carpeta principal.")
        return
    
    contador_eliminados = 0
    
    for archivo in archivos_principal:
        nombre = os.path.basename(archivo)
        nombre_sin_extension = os.path.splitext(nombre)[0]
        
        # Extraer el nombre base ignorando cualquier sufijo con "_"
        if "_" in nombre_sin_extension:
            nombre_base = nombre_sin_extension.split("_")[0]
        else:
            nombre_base = nombre_sin_extension
        
        # Verificar si este archivo está en la lista de los que debemos conservar
        if nombre_base not in nombres_piano:
            try:
                os.remove(archivo)
                print(f"Eliminado: {nombre}")
                contador_eliminados += 1
            except Exception as e:
                print(f"Error al eliminar {nombre}: {e}")
    
    print(f"\nProceso completado. Se eliminaron {contador_eliminados} archivos.")

if __name__ == "__main__":
    # Verificar si se proporcionó una carpeta como argumento
    if len(sys.argv) > 1:
        carpeta_principal = sys.argv[1]
    else:
        # Si no se proporciona argumento, usar la carpeta actual
        carpeta_principal = input("Ingrese la ruta de la carpeta principal (o presione Enter para usar la carpeta actual): ")
        if not carpeta_principal:
            carpeta_principal = "."
    
    # Construir la ruta a la carpeta Piano
    carpeta_piano = os.path.join(carpeta_principal, "Piano")
    
    # Confirmar la eliminación
    print(f"ADVERTENCIA: Este script eliminará archivos FLAC de '{carpeta_principal}'")
    print(f"que no coincidan con los nombres base de los archivos en '{carpeta_piano}'.")
    confirmacion = input("¿Desea continuar? (s/n): ")
    
    if confirmacion.lower() == 's':
        eliminar_archivos_no_coincidentes(carpeta_principal, carpeta_piano)
    else:
        print("Operación cancelada.")