# Taller 2
Para este proceso se entrega la configuración de un ambiente de desarrollo usando una imagen pre-construida de TensorFlow pero solo especificado en un ambiente comando de Docker.

```Docker
    sudo docker run -it --name tfx --rm -p 8888:8888 -p 6006:6006 -v $PWD:/tfx/src --entrypoint /run_jupyter.sh  tensorflow/tfx:1.12.0
```

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

Cree un archivo `docker-compose.yaml` que ejecute un contenedor de desarrollo basado en el comando de docker descrito anteriormente. Acceda a la interfaz gráfica de Jupyter que despliega este componente y ejecute los ejemplos vistos en clase [TFDV](Validacion_de_datos/TF/TFDV.ipynb) y [ML_Metadata](Transformacion_de_datos/ML_Metadata.ipynb).

Tenga en cuenta que es posible que necesite elementos nuevos en esta imagen, valide el funcionamiento y proponga como agregar los elementos faltantes.