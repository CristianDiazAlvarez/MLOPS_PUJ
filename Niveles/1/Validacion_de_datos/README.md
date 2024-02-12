# Data Validation


## Tensor Flow Data Validation

---

La instalación de TFX puede ser un proceso complejo, por eso Docker es una herramienta útil. Además cada framework importante genera una imagen para usar sus herramientas, este es el caso de TFX. Hay un ejemplo para usar este contenedor usando un volumen para mantener los datos guardados en la máquina host. Además, el contenedor expone una instancia de JupyterLab lista para funcionar.


---
```Docker
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


El cuaderno TFDV muestra un ejemplo sobre datos de diabetes sobre cómo usar TFDV según el ejemplo de TF.




---
## pycaret


Construir imágenes propias es una práctica común, en este caso, el archivo **Dockerfile** nos permite crear una imagen lista para usar en la biblioteca pycaret expuesta en un Jupyter Lab. Consulte requierements.txt y Dockerfile.

---
```Docker
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

El cuaderno **pycaret** muestra un ejemplo sobre datos de diabetes sobre cómo usar **pycaret** según el ejemplo de Docs.
