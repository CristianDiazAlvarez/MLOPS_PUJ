# Introducción a los Contenedores y Docker
## ¿Qué es un contenedor?
- Un contenedor es una unidad ligera y portable que empaqueta una aplicación y sus dependencias para ejecutarse de manera consistente en cualquier entorno
- Comparado con máquinas virtuales, los contenedores comparten el kernel del sistema operativo y son más eficientes en el uso de recursos

## ¿Qué es Docker?
- Plataforma que permite crear, ejecutar y gestionar contenedores de manera sencilla
- Utiliza imágenes y contenedores para facilitar la portabilidad de aplicaciones

## Componentes Claves de Docker
- Imágenes: Plantillas inmutables que contienen el sistema base y las dependencias necesarias
- Contenedores: Instancias en ejecución de una imagen
- Dockerfile: Archivo con instrucciones para crear imágenes personalizadas
- Docker Hub: Repositorio en la nube para almacenar imágenes
- Docker Engine: Motor que permite ejecutar los contenedores

## Verificar si Docker está instalado

Ejecutar el siguiente comando en la terminal:
```bash
docker --version
```
Si Docker está instalado, mostrará la versión actual. En caso contrario, deberá instalarse desde la documentación oficial. [Docker Desktop](https://docs.docker.com/desktop/) o [Cómo instalar y usar Docker en Ubuntu 22.04](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-22-04)

## Probar que Docker funciona correctamente

```bash
docker run hello-world
```
Este comando descarga y ejecuta un contenedor de prueba.

## Ejemplo

[Ejemplo de un Dockerfile básico](basico/Dockerfile)
[Archivo de prueba](basico/archivo_prueba.txt)

Para construir la imagen, ejecutar el siguiente comando en la misma carpeta donde se encuentra el Dockerfile:

```bash
docker build -t mi_imagen_prueba .
````
- `-t mi_imagen_prueba`: Asigna un nombre a la imagen
- `.` : Indica que el contexto de construcción es la carpeta actual

Verificar que la imagen se creó correctamente

```bash
docker images
```
### Crear un Contenedor a partir de la Imagen
Una vez creada la imagen, podemos ejecutar un contenedor basado en ella.

```bash
docker run --name mi_contenedor -it mi_imagen_prueba
```
- `--name mi_contenedor`: Asigna un nombre al contenedor
- `-it`: Permite una sesión interactiva
- `mi_imagen_prueba`: Especifica la imagen a usar

Este comando ejecutará `ls -l /app`, mostrando los archivos dentro del directorio `/app`

### Validar los Archivos Copiados dentro del Contenedor
Para verificar que `archivo_prueba.txt` está dentro del contenedor, podemos acceder a la terminal del contenedor y listar su contenido.

Acceder al contenedor en ejecución
```bash
docker run --name mi_contenedor -it mi_imagen_prueba bash
```

Dentro del contenedor, ejecutar:
```bash
ls -l /app
cat /app/archivo_prueba.txt
```

Esto debería mostrar el archivo copiado y su contenido.

Salir del contenedor
Para salir de la sesión interactiva, escribir:
```bash
exit
```

### Detener y Eliminar Contenedores

Si un contenedor está en ejecución y queremos detenerlo:

```bash
docker stop mi_contenedor
```
Para eliminarlo completamente:

```bash

docker rm mi_contenedor
```

Para eliminar la imagen creada:

```bash
docker rmi mi_imagen_prueba
```

Para eliminar todos los contenedores detenidos:

```bash
docker container prune
```

### Descargar y Ejecutar Imágenes desde Docker Hub
Docker Hub permite acceder a imágenes oficiales y personalizadas.

Buscar una imagen en Docker Hub
```bash
docker search ubuntu
```

Descargar una imagen sin ejecutarla

```bash
docker pull ubuntu:latest
```

Ejecutar un contenedor desde una imagen descargada

```bash
docker run -it ubuntu bash
```

Esto inicia una sesión interactiva dentro de un contenedor Ubuntu.

## Ejercicio propuesto
1. Crear un Dockerfile personalizado que:

    - Use la imagen base alpine:latest.
    - Copie un archivo de texto en /data/.
    - Liste los archivos en /data/ al ejecutar el contenedor.
2. Construir la imagen y verificar que el archivo existe dentro del contenedor.