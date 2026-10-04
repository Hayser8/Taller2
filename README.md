# Machine Learning Engineering — Taller 2

Este repositorio muestra cómo aislar dependencias de Python para un proyecto de
Machine Learning, cómo documentar el entorno y cómo distribuir un pipeline de
scikit-learn como paquete.

## Estructura

```text
.
├── environment.yml                 # Entorno reproducible con Conda
├── Makefile                        # Atajos para instalar y ejecutar el pipeline
├── pyproject.toml                  # Metadatos y dependencias del paquete
├── requirements.txt                # Punto de entrada convencional para pip
├── requirements-ml.txt             # Herramientas generales de ML y análisis
├── src/taller2_ml/
│   ├── __init__.py
│   ├── pipeline.py                 # Pipeline de clasificación con Iris
│   └── requirements-pipeline.txt   # Dependencias del pipeline, incluidas en el paquete
└── docs/
    ├── evidence/terminal-results.md # Salidas verificadas de los ambientes
    └── screenshots/                # Lugar para las capturas PNG
```

## 1. Ambiente virtual de Python (`venv`)

La biblioteca estándar `venv` crea un directorio aislado para el intérprete y
los paquetes del proyecto. La convención más extendida para declarar paquetes
instalables con `pip` es un archivo llamado `requirements.txt`. Aquí funciona
como punto de entrada y delega la lista de análisis/ML en `requirements-ml.txt`;
las dependencias específicas del pipeline se separan dentro del paquete.

En macOS/Linux, desde la raíz del repositorio:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install -e .
taller2-pipeline
```

El último comando es el *entrypoint* de consola que se define en
`pyproject.toml`. También se puede ejecutar el módulo directamente con
`python -m taller2_ml.pipeline`.

En Windows PowerShell, la activación es `.\.venv\Scripts\Activate.ps1` y se
mantiene el resto de los comandos `python -m pip ...`.

`requirements-ml.txt` agrupa NumPy, pandas, scikit-learn, Matplotlib, Seaborn y
JupyterLab, herramientas comunes para preparar datos, entrenar modelos y
explorar resultados. Los rangos expresan compatibilidad prevista; para
reproducir exactamente una instalación se debe guardar además un archivo con
versiones resueltas (por ejemplo, `pip freeze > requirements-lock.txt`).

## 2. Dependencias del pipeline y empaquetado

El ejemplo de `src/taller2_ml/pipeline.py` carga Iris desde scikit-learn,
divide los datos, estandariza las variables y entrena una regresión logística.
No necesita un archivo de datos externo. Sus dependencias directas están en
`src/taller2_ml/requirements-pipeline.txt` y también en los metadatos de
`pyproject.toml`.

El archivo de requisitos está dentro del paquete y `pyproject.toml` lo declara
como dato del paquete mediante `package-data`. Por eso acompaña al módulo tanto
en el wheel como en la distribución fuente; se puede consultar desde una
instalación con `importlib.resources`. Esto permite instalar solo el pipeline
con:

```bash
python -m pip install -r src/taller2_ml/requirements-pipeline.txt
python -m pip install -e .
```

## 3. Ambiente Conda

Conda administra entornos nombrados, dependencias Python y bibliotecas binarias.
Es útil en ciencia de datos cuando hay componentes compilados o se requiere una
versión de Python concreta. El archivo `environment.yml` define el entorno
completo y puede combinar paquetes del canal Conda con dependencias instaladas
por `pip`.

```bash
conda create --file environment.yml
conda activate taller2-ml
taller2-pipeline
conda env list
```

El reto de Conda tiene su propia variación: el manifiesto convencional es
`environment.yml` (YAML), no `requirements.txt`. No es solo una lista de pip:
también puede indicar el nombre del ambiente, canales, versión de Python y una
sección separada para paquetes de pip. Para actualizarlo, se modifica el YAML y
se ejecuta `conda env update -f environment.yml --prune`.

## 4. Comparación: `venv` + `pip` y uv

La comparación toma como referencia el tutorial de [DataCamp sobre uv](https://www.datacamp.com/tutorial/python-uv)
y la [documentación de uv](https://docs.astral.sh/uv/).

| Criterio | `venv` + `pip` (flujo de este taller) | uv |
|---|---|---|
| Enfoque | Herramientas estándar separadas: `venv` crea el entorno y `pip` instala paquetes. | Herramienta unificada para proyectos, entornos, resolución e instalación de paquetes y versiones de Python. |
| Declaración común | `requirements.txt`, normalmente junto a `pyproject.toml` para metadatos/paquete. | Recomienda `pyproject.toml`; también puede compilar `requirements.in` o `pyproject.toml` a `requirements.txt`. |
| Entorno | Se crea explícitamente con `python -m venv .venv`. | En proyectos crea/usa `.venv` automáticamente al correr `uv sync` o `uv run`. |
| Versiones reproducibles | Un archivo de requisitos con rangos no fija toda la resolución; se puede fijar con `pip freeze` o herramientas de lock. | `uv.lock` conserva las versiones resueltas del proyecto; `uv pip compile` puede producir requisitos fijados. |
| Instalación y uso | Activar el entorno e invocar `python -m pip install ...`. | `uv add`, `uv sync` y `uv run`; también ofrece comandos compatibles con el flujo pip. |
| Ventaja práctica | Viene con Python, enseña explícitamente el aislamiento y funciona bien en ejercicios sencillos. | Reduce pasos y acelera la resolución e instalación; gestiona varios aspectos del flujo de trabajo con un solo ejecutable. |
| Consideración | Se coordinan varias herramientas y un `requirements.txt` básico no equivale por sí solo a un lock completo. | Requiere instalar uv y aprender su flujo; su `uv.lock` es específico de proyecto y conviene mantenerlo en control de versiones. |

## 5. Comparación: `venv` + `pip` y Poetry

La comparación toma como referencia el tutorial de [DataCamp sobre Poetry](https://www.datacamp.com/tutorial/python-poetry)
y la [documentación oficial de Poetry](https://python-poetry.org/docs/).

| Criterio | `venv` + `pip` (flujo de este taller) | Poetry |
|---|---|---|
| Enfoque | Aislamiento y descarga de paquetes son pasos explícitos con herramientas estándar. | Administrador de proyectos y dependencias; también crea/gestiona entornos virtuales y puede construir/publicar paquetes. |
| Declaración común | `requirements.txt` para instalación y `pyproject.toml` para metadatos cuando se empaqueta. | `pyproject.toml` como manifiesto central del proyecto. |
| Entorno | El equipo crea y activa el entorno de forma explícita. | `poetry install` administra el entorno del proyecto; `poetry env use` permite elegir el intérprete. |
| Versiones reproducibles | Requiere generar y compartir una resolución fijada adicional si se busca reproducibilidad estricta. | `poetry.lock` registra la resolución exacta y se comparte con el proyecto. |
| Grupos de dependencias | Se suelen separar archivos, por ejemplo `requirements-ml.txt` y `requirements-dev.txt`. | Permite grupos y extras definidos en el proyecto e instalarlos selectivamente. |
| Empaquetado | Hay que configurar explícitamente el backend y los archivos incluidos, como hace este ejercicio con setuptools. | Incluye construcción y publicación en su flujo integrado. |
| Ventaja práctica | Es simple, está disponible con Python y deja visibles los pasos fundamentales. | Centraliza dependencias, lock, entornos y tareas de empaquetado para proyectos compartidos. |
| Consideración | Más configuración manual a medida que crece el proyecto. | Añade una herramienta y convenciones propias; el equipo debe adoptar Poetry para operar con el manifiesto y lock. |

## 6. Entrypoint de Python y Makefile

En `pyproject.toml`, la tabla `[project.scripts]` registra el comando
`taller2-pipeline` y lo conecta con `taller2_ml.pipeline:main`. El instalador
crea el ejecutable de consola al instalar el paquete; por eso se puede llamar
al pipeline por su nombre sin escribir una ruta al archivo Python.

```toml
[project.scripts]
taller2-pipeline = "taller2_ml.pipeline:main"
```

Con el ambiente del proyecto activado, el Makefile ofrece dos objetivos para
repetir los pasos comunes:

```bash
make install
make run
```

`install` instala el proyecto en modo editable dentro del Python activo. `run`
invoca el mismo comando de consola que se puede llamar directamente. En uv se
puede usar `uv sync` y luego `uv run taller2-pipeline`; en Poetry,
`poetry install` y luego `poetry run taller2-pipeline`. El `environment.yml` de
este proyecto instala el paquete editable con pip dentro del ambiente Conda,
así que tras activarlo también queda disponible el comando. Para distribuir un
paquete nativo de Conda, `conda-build` admite declarar entradas de consola en
`build.entry_points` dentro de la receta.

Un Makefile organiza comandos bajo objetivos y puede servir como interfaz
uniforme para desarrollo local o CI. No crea ni registra el entrypoint: lo
invoca después de que el ambiente instala el paquete.

## 7. Conclusiones

Un ambiente virtual evita que las dependencias de un proyecto alteren las de
otro. En Machine Learning esto es especialmente útil porque versiones de
NumPy, scikit-learn y bibliotecas con componentes nativos pueden afectar tanto
la ejecución como los resultados. Un manifiesto compartido facilita que otra
persona instale el mismo conjunto de herramientas y entienda qué requiere el
código.

`venv` y `pip` son adecuados para aprender el aislamiento y mantener ejemplos
pequeños con pocos pasos. UV ofrece un flujo integrado y lock del proyecto;
Poetry añade metadatos, grupos de dependencias y empaquetado; Conda también
puede resolver paquetes binarios y versiones de Python mediante canales. Para
un proyecto de equipo conviene elegir una herramienta por entorno de trabajo,
mantener su manifiesto y archivo de resolución bajo control de versiones y
evitar mezclar gestores en el mismo ambiente.

## Fuentes

- [Python: `venv` — creación de ambientes virtuales](https://docs.python.org/3/library/venv.html)
- [VS Code: ambientes virtuales de Python](https://code.visualstudio.com/docs/python/environments)
- [Conda: administración de ambientes](https://docs.conda.io/projects/conda/en/stable/user-guide/tasks/manage-environments.html)
- [DataCamp: Python UV](https://www.datacamp.com/tutorial/python-uv)
- [uv: proyectos y dependencias](https://docs.astral.sh/uv/guides/projects/)
- [DataCamp: Python Poetry](https://www.datacamp.com/tutorial/python-poetry)
- [Poetry: documentación](https://python-poetry.org/docs/)
- [PyPA: especificación de entry points](https://packaging.python.org/en/latest/specifications/entry-points/)
- [PyPA: metadatos de `pyproject.toml`](https://packaging.python.org/en/latest/specifications/pyproject-toml/)
- [DataCamp: Makefile y GitHub Actions](https://www.datacamp.com/tutorial/makefile-github-actions-tutorial)

## Entregables

- Código del pipeline y archivos de requisitos en este repositorio.
- Configuración Conda en `environment.yml`.
- Salidas verificadas de terminal en `docs/evidence/terminal-results.md`.
- Las capturas PNG solicitadas están pendientes; ver `docs/screenshots/README.md`.
- Repositorio del taller: [Hayser8/Taller2](https://github.com/Hayser8/Taller2).
