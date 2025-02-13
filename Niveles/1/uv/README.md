# UV

Es un gestor de paquetes y proyectos para Python escrito en Rust, que ofrece una alternativa rápida y eficiente a herramientas tradicionales como `pip` y `poetry`.

## 🚀 Instalación de uv

Puedes instalar uv utilizando el instalador independiente proporcionado por los desarrolladores:

### Para 💻 macOS y 🐧 Linux

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Para ⚙️ Windows

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Para 🔩 pip

Alternativamente, uv está disponible en PyPI y puede ser instalado usando pip:

```bash
pip install uv
```

Para más detalles sobre la instalación, puedes consultar la [documentación oficial](https://docs.astral.sh/uv/).

## 📌 Creación de un Proyecto con uv

Inicializar el Proyecto: Para comenzar un nuevo proyecto, utiliza el comando uv init seguido del nombre del proyecto.

```bash
uv init mi_proyecto
```

Este comando crea una nueva carpeta llamada `mi_proyecto` con la estructura básica de un proyecto, incluyendo un archivo `pyproject.toml`.

Seleccionar la Versión de Python: uv permite gestionar diferentes versiones de Python. Para instalar y utilizar una versión específica, ejecuta:

```bash
uv python install 3.10.9
```

Luego, dentro del directorio del proyecto, puedes fijar la versión de Python deseada:

```bash
cd mi_proyecto
uv python pin 3.10.9
```

Esto asegura que el proyecto utilice la versión de Python especificada.

## 🔗 Gestionar Dependencias

Agregar Dependencias: Para añadir paquetes al proyecto, utiliza el comando `uv add` seguido del nombre del paquete. Por ejemplo, para agregar `numpy` y `pandas`:

```bash
uv add numpy pandas
```

Este comando resuelve e instala las dependencias, y las añade al archivo pyproject.toml.

**Grupos de Dependencias:** uv permite crear grupos de dependencias, lo cual es útil para separar dependencias de desarrollo y de producción. Para agregar una dependencia al grupo de desarrollo:

```bash
uv add --group dev pytest
```

Esto añade `pytest` al grupo de dependencias de desarrollo en el archivo `pyproject.toml`.

**Ejecutar Comandos:** Para ejecutar comandos dentro del entorno del proyecto, utiliza `uv run`. Por ejemplo, para iniciar una sesión interactiva de Python:

```bash
uv run python
```

O para ejecutar un script específico:

```bash
uv run python script.py
```

Esto asegura que los comandos se ejecuten dentro del entorno virtual del proyecto, con las dependencias y la versión de Python especificadas.

## Ejemplo de Uso de **uv**

En este ejemplo, exploraremos cómo utilizar **uv** para gestionar dependencias en un proyecto de FastAPI con un modelo de Machine Learning. Mostraremos dos casos de uso:

1. **Creación de un Proyecto desde Cero**
2. **Uso de un Proyecto Existente sin Tener Nada Instalado**

## 🚀 1. Creación de un Proyecto desde Cero

### Paso 1: Instalación de **uv**

Si no tienes **uv** instalado:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

O usando `pip`:

```bash
pip install uv
```

### Paso 2: Inicialización del Proyecto

```bash
uv init fastapi-ml-project
cd fastapi-ml-project
```

Esto creará un archivo `pyproject.toml` que gestionará las dependencias.

### Paso 3: Agregar Dependencias

Agregamos las librerías necesarias:

```bash
uv add numpy pandas scikit-learn fastapi uvicorn
```

Esto actualizará el `pyproject.toml` y creará un archivo `uv.lock`.

### Paso 4: Crear el Archivo `main.py`

```python
from fastapi import FastAPI
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier

app = FastAPI()

# Modelo simple de ejemplo
data = load_iris()
model = RandomForestClassifier()
model.fit(data.data, data.target)

@app.get("/predict")
def predict(sepal_length: float, sepal_width: float, petal_length: float, petal_width: float):
    prediction = model.predict([[sepal_length, sepal_width, petal_length, petal_width]])
    return {"prediction": int(prediction[0])}
```

### Paso 5: Ejecutar la Aplicación

```bash
uv run uvicorn main:app --reload
```

Accede a la API en [http://localhost:8000/docs](http://localhost:8000/docs).

---

## 🔄 2. Uso de un Proyecto Existente

Si ya tienes el proyecto con los archivos `pyproject.toml` y `uv.lock`, pero no tienes nada instalado:

### Paso 1: Instalar **uv**

Si no está instalado:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Paso 2: Sincronizar Dependencias

```bash
uv sync
```

Esto instalará automáticamente todas las dependencias definidas en `pyproject.toml` y `uv.lock`.

### Paso 3: Ejecutar la Aplicación

```bash
uv run uvicorn main:app --reload
```

### Prueba de la API

```bash
curl "http://localhost:8000/predict?sepal_length=5.1&sepal_width=3.5&petal_length=1.4&petal_width=0.2"
```

Respuesta esperada:

```json
{"prediction": 0}
```

---
