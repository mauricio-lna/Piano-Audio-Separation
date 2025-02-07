import yaml
import csv
import sys
import os

def get_yaml_files_from_directory(directory):
    """Obtiene una lista de archivos YAML desde una carpeta especificada."""
    return [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.yaml') or f.endswith('.yml')]

def yaml_to_csv(yaml_files, csv_file):
    try:
        # Crear una lista para almacenar todos los datos
        all_data = []

        # Leer y combinar los datos de todos los archivos YAML
        for yaml_file in yaml_files:
            with open(yaml_file, 'r') as yf:
                data = yaml.safe_load(yf)

                # Asegurarse de que los datos sean una lista de diccionarios
                if not isinstance(data, list):
                    print(f"Error: El archivo YAML {yaml_file} debe contener una lista de objetos.")
                    return

                all_data.extend(data)

        # Obtener las claves del primer diccionario como encabezados del CSV
        if not all_data:
            print("Error: No se encontraron datos para escribir en el archivo CSV.")
            return

        keys = all_data[0].keys()

        # Escribir los datos en el archivo CSV
        with open(csv_file, 'w', newline='') as cf:
            writer = csv.DictWriter(cf, fieldnames=keys)
            writer.writeheader()
            writer.writerows(all_data)

        print(f"Archivo CSV generado exitosamente: {csv_file}")

    except FileNotFoundError as e:
        print(f"Error: No se encontró el archivo {e.filename}.")
    except yaml.YAMLError as e:
        print(f"Error al leer el archivo YAML: {e}")
    except Exception as e:
        print(f"Ocurrió un error: {e}")

# Ejemplo de uso
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python YAML-to-CSV.py <directorio_yaml> <archivo_csv>")
    else:
        yaml_directory = sys.argv[1]
        csv_file = sys.argv[2]

        # Obtener archivos YAML desde la carpeta especificada
        yaml_files = get_yaml_files_from_directory(yaml_directory)

        if not yaml_files:
            print(f"Error: No se encontraron archivos YAML en el directorio {yaml_directory}.")
        else:
            yaml_to_csv(yaml_files, csv_file)
