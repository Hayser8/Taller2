# Salidas de terminal

Estas salidas se obtuvieron ejecutando los comandos indicados en los ambientes
del proyecto. Son transcripciones textuales, no capturas de pantalla.

## Python `venv`

```text
$ python3 -m venv .venv
$ source .venv/bin/activate
(.venv) $ python --version
Python 3.14.7
(.venv) $ python -c 'import sys; print(sys.executable)'
/Users/julio/Documents/GitHub/Taller2/.venv/bin/python
(.venv) $ python -m taller2_ml.pipeline
Dataset: Iris (150 filas, 4 variables)
Exactitud en prueba: 0.921
Clases: setosa, versicolor, virginica
```

## Conda

```text
$ conda create --file environment.yml --yes
Platform: osx-arm64
environment location: /private/tmp/taller2-miniforge/envs/taller2-ml
To activate this environment, use: conda activate taller2-ml

$ conda activate taller2-ml
(taller2-ml) $ python --version
Python 3.12.14
(taller2-ml) $ python -c 'import sys; print(sys.executable)'
/private/tmp/taller2-miniforge/envs/taller2-ml/bin/python
(taller2-ml) $ python -m taller2_ml.pipeline
Dataset: Iris (150 filas, 4 variables)
Exactitud en prueba: 0.921
Clases: setosa, versicolor, virginica
(taller2-ml) $ conda env list
# conda environments:
#
# * -> active
base                     /private/tmp/taller2-miniforge
taller2-ml           *   /private/tmp/taller2-miniforge/envs/taller2-ml
```

La instalación temporal de Miniforge/Conda usada para esta comprobación se
retiró al terminar. El archivo `environment.yml` permite recrear el ambiente.

## Archivo de requisitos dentro del wheel

La construcción del wheel confirmó que setuptools incluyó el manifiesto
específico en la distribución binaria:

```text
$ python -m pip wheel --no-deps --wheel-dir /tmp/taller2-wheel .
Successfully built taller2-ml
$ unzip -l /tmp/taller2-wheel/taller2_ml-0.1.0-py3-none-any.whl
taller2_ml/requirements-pipeline.txt
```
