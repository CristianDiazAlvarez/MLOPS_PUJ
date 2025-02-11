# Transformación de Datos

El proceso de transformación de datos es una etapa crucial en el ciclo de vida de los proyectos de ciencia de datos y machine learning. Consiste en convertir, modificar o estructurar los datos brutos para que sean adecuados para el análisis y el entrenamiento de modelos. Este proceso mejora la calidad de los datos, optimiza el rendimiento de los algoritmos y garantiza que la información sea coherente y relevante para los objetivos del proyecto.

Las transformaciones pueden incluir tareas como la normalización o escalado de variables numéricas, la codificación de variables categóricas, la generación de nuevas características (feature engineering), la agregación de datos, y la eliminación o imputación de valores nulos. Estas operaciones permiten adaptar los datos a los requisitos específicos de los modelos, mejorando su capacidad para aprender patrones significativos.

Un proceso de transformación de datos bien diseñado no solo mejora la precisión y eficiencia del modelo, sino que también facilita la interpretabilidad de los resultados y la reproducibilidad del análisis. Por ello, es fundamental comprender las técnicas de transformación y su impacto en el rendimiento de los modelos de machine learning.

## TensorFlow Transform
TensorFlow Transform (TFT) es una herramienta que permite realizar transformaciones de datos a gran escala de manera eficiente y coherente tanto durante el entrenamiento de modelos de machine learning como en su despliegue en producción. Facilita tareas como la normalización, generación de variables derivadas y manejo de valores faltantes, asegurando que las transformaciones aplicadas en la fase de entrenamiento se reproduzcan exactamente en el entorno de inferencia, lo que mejora la consistencia y el rendimiento del modelo.

```bash
docker rmi $(docker images --filter "dangling=true" -q --no-trunc)
```
- `docker` rmi: Comando para eliminar imágenes de Docker.
- `$(...)`: Permite ejecutar un comando dentro de otro. En este caso, se listan las imágenes colgantes y se pasan como argumento para eliminarlas.
- `docker images`: Lista las imágenes almacenadas localmente en Docker.
- `--filter "dangling=true"`: Filtra las imágenes que están colgantes, es decir, aquellas que no están asociadas a ningún contenedor y que generalmente son restos de compilaciones anteriores.
- `-q`: Muestra solo los IDs de las imágenes, lo que es útil para operaciones automáticas como esta.
- `--no-trunc`: Muestra los IDs completos de las imágenes sin truncarlos (aunque con -q esto suele ser redundante).

```bash
docker build -t tfx_custom .
```

- `docker build`: Comando para construir una imagen de Docker a partir de un Dockerfile.
- `-t tfx_custom`: La opción -t (o --tag) asigna un nombre a la imagen resultante, en este caso tfx_custom. Esto facilita su referencia en futuros comandos sin necesidad de usar el ID de la imagen.
- `.:` Indica el contexto de construcción, es decir, la carpeta actual donde está ubicado el Dockerfile y otros archivos necesarios.

```bash
    docker run -it --name tfx_custom -e TZ=America/Bogota --rm -p 8888:8888  -v $PWD:/work tfx_custom
```

- `docker run`: Comando para crear y ejecutar un nuevo contenedor basado en una imagen.
- `-it`: Combina dos opciones:
    - `-i (interactivo)`: Mantiene la entrada estándar abierta.
    - `-t (pseudo-TTY)`: Asigna una terminal interactiva, permitiendo la interacción directa con el contenedor.
- `--name tfx_custom`: Asigna un nombre personalizado al contenedor (tfx_custom), lo que facilita su gestión en lugar de usar el ID generado automáticamente.
- `-e TZ=America/Bogota`: Establece una variable de entorno (TZ) dentro del contenedor, configurando la zona horaria a America/Bogota.
- `--rm`: Indica que el contenedor se eliminará automáticamente después de detenerse, evitando la acumulación de contenedores inactivos.
- `-p 8888:8888`: Publica el puerto 8888 del contenedor en el puerto 8888 del host. Esto permite, por ejemplo, acceder a aplicaciones web como Jupyter Notebook ejecutándose dentro del contenedor a través del navegador.
- `-v $PWD:/work`: Monta un volumen, vinculando el directorio actual del host ($PWD) al directorio /work dentro del contenedor. Esto permite compartir archivos entre el host y el contenedor de manera persistente.
- `tfx_custom`: Especifica la imagen que se usará para crear el contenedor, en este caso, la imagen tfx_custom construida anteriormente.