# Instalacion

## Anaconda

### Crear Entorno

conda env create -f environment.yml

### Activar Entorno

conda activate audio_env

### Desactivar Entorno

conda deactivate

### Eliminar Entorno

conda env remove --name audio_env

### Ver Entornos

conda env list

## NUSSL

Instrucciones para instalar NUSSL

1. desde el entorno audio_env moverse a la carpeta nussl
   cd nussl-1.1.3

2. ejectuar pip install
   pip install .

3. Ejecutar el siguiente commando e ir a la direccion que muestra audio-env
   conda info --envs
   cd C:\Users\wallc\.conda\envs\audio_env\Lib\site-packages\

4. ir a a la carpeta stempeg
   cd C:\Users\wallc\.conda\envs\audio_env\Lib\site-packages\stempeg

## Jupyter

1.  Ir a la ruta
    C:\Users\wallc\.conda\envs\audio_env\Lib\site-packages\numpy

2.  Activar entorno
    conda activate audio_env

3.  Abrir jupyter
    jupyter notebook

## Version de librerias a instalar

- NumPY 1.26.4
- SciPy v1.15.1
- scaper1.6.4
- pyloudnorm
