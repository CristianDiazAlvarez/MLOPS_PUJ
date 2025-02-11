# Validación de datos

El proceso de validación de datos es un paso fundamental en cualquier proyecto de ciencia de datos o machine learning, ya que garantiza la calidad, integridad y coherencia de los datos antes de su análisis o uso en el entrenamiento de modelos. La validación de datos consiste en aplicar un conjunto de verificaciones para identificar errores, anomalías, valores nulos, duplicados o inconsistencias que puedan afectar el rendimiento del modelo o llevar a conclusiones erróneas.

Este proceso no solo ayuda a detectar problemas evidentes en los datos, sino que también permite asegurar que cumplen con las reglas de negocio, las expectativas del dominio y los estándares de calidad definidos para el proyecto. La validación de datos puede realizarse en diferentes etapas del ciclo de vida del dato, desde su recolección hasta su procesamiento final, e incluye técnicas como la verificación de tipos de datos, la detección de valores atípicos, la comprobación de rangos válidos y la consistencia entre diferentes fuentes de información.

Implementar un proceso de validación de datos efectivo contribuye a la confiabilidad del modelo, reduce el riesgo de errores en producción y mejora la capacidad de tomar decisiones basadas en datos precisos y de alta calidad.


## Tensor Flow Data Validation

TensorFlow Data Validation (TFDV) es una herramienta que facilita la exploración y validación de datos en proyectos de machine learning. Permite detectar automáticamente anomalías, valores atípicos e inconsistencias en los datos, comparando diferentes conjuntos (como entrenamiento y prueba) para garantizar su calidad. Además, ayuda a generar estadísticas descriptivas y esquemas de datos, lo que mejora la confiabilidad y reproducibilidad de los modelos.

### Instalación de TFDV
---

La instalación de TFX puede ser un proceso complejo, por eso Docker es una herramienta útil. Además cada framework importante genera una imagen para usar sus herramientas, este es el caso de TFX. Hay un ejemplo para usar este contenedor usando un volumen para mantener los datos guardados en la máquina host. Además, el contenedor expone una instancia de JupyterLab lista para funcionar.

---
```bash
    sudo docker run -it --name tfx --rm -p 8888:8888 -p 6006:6006 -v $PWD:/tfx/src --entrypoint /run_jupyter.sh  tensorflow/tfx:1.12.0
```

---

Entendiendo el comando de Docker:

- **`-it`** permite un modo interactivo
- **`--name tf`x** establece un nombre específico para la instancia del contenedor, en este caso 'tfx'
- **`--rm`** Al detener la ejecución de este contenedor lo elimina
- **`-p`** publicar o exponer el puerto puerto_maquina_anfitriona:puerto_del_contenedor
- **`-v`** montar el volumen de enlace como archivo o carpeta. carpeta_host: carpeta_docker
    - **`$PWD`** selecciona la carpeta actual de ejecución como punto de montaje del volumen
    - **`/tfx/src`** Establece cual es la carpeta dentro del contenedor que
- **`--entrypoint`** comando de establecimiento para ejecutar y establecer la vida útil del contenedor como este comando
- **`tensorflow/tfx`** define la imagen de docker, primero como búsqueda predeterminada local y luego en DockerHub (o cualquier registro de artefactos indicado)
---


El [notebook TFDV](TF/TFDV.ipynb) muestra un ejemplo sobre datos de diabetes sobre cómo usar TFDV según el ejemplo de TF.

---
## Pycaret

PyCaret es una biblioteca de machine learning de bajo código que simplifica el proceso de validación de datos al automatizar la detección de anomalías, el manejo de valores nulos y la verificación de la consistencia de las variables. Facilita la exploración de datos mediante análisis estadísticos rápidos, identificación de desequilibrios en las clases y generación de informes de calidad, lo que permite preparar conjuntos de datos más robustos para el modelado.

Construir imágenes propias es una práctica común, en este caso, el archivo **[Dockerfile](PYCARET/Dockerfile)** nos permite crear una imagen lista para usar en la biblioteca pycaret expuesta en un Jupyter Lab. Consulte [requierements.txt](PYCARET/requirements.txt) y Dockerfile.

---
```bash
    docker build -t pycaret .
    docker run -it --name pycaret --rm -e TZ=America/Bogota -p 8888:8888 -v $PWD:/work pycaret:latest
```

---

Entendiendo el comando de Docker:

- **`-it`** permite un modo interactivo
- **`--name pycaret`x** establece un nombre específico para la instancia del contenedor, en este caso 'pycaret'
- **`-e TZ=America/Bogota`** Establece la variable env en el contenedor, esto modifica la zona horaria
- **`--rm`** Al detener la ejecución de este contenedor lo elimina
- **`-p`** publicar o exponer el puerto puerto_maquina_anfitriona:puerto_del_contenedor
- **`-v`** montar el volumen de enlace como archivo o carpeta. carpeta_host: carpeta_docker
    - **`$PWD`** selecciona la carpeta actual de ejecución como punto de montaje del volumen
    - **`/work`** Establece cual es la carpeta dentro del contenedor que
- **`--entrypoint`** comando de establecimiento para ejecutar y establecer la vida útil del contenedor como este comando
- **`pycaret:latest`** define la imagen de docker, primero como búsqueda predeterminada local y luego en DockerHub (o cualquier registro de artefactos indicado)
---

El [Notebook **pycaret**](PYCARET/pycaret.ipynb) muestra un ejemplo sobre datos de diabetes sobre cómo usar **pycaret** según el ejemplo de Docs.
