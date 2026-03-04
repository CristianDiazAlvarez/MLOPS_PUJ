# MinIO + Notebook (Docker Compose)

Este ejemplo muestra como entrenar un modelo simple desde un notebook y guardar artefactos en MinIO usando un stack Docker Compose. Incluye red dedicada entre servicios y volumenes administrados por Docker.

## Objetivo
- Entender como un servicio de almacenamiento tipo S3 (MinIO) se consume desde un notebook.
- Practicar configuracion de red entre contenedores (DNS interno por nombre de servicio).
- Ver el uso de volumenes Docker para persistir datos de MinIO.

## Arquitectura
Servicios:
- `minio`: servidor S3 compatible para almacenar modelos y metricas.
- `jupyter`: notebook para entrenamiento y carga de artefactos a MinIO.

Red:
- `minio-net`: red bridge dedicada para resolver `minio` por nombre dentro del compose.

Volumenes:
- `minio_data`: volumen persistente para el almacenamiento del servidor MinIO.
- `./notebooks`: volumen bind para editar notebooks en tu editor local.

## Pasos

1) Levantar los servicios:

```bash
cd Niveles/2/MinIO
docker compose up -d
```

2) Abrir Jupyter Lab:

```bash
docker compose logs -f jupyter
```

Abrir:
```
http://127.0.0.1:8888/lab?token=minio123
```

3) Abrir el notebook `notebooks/train_minio_model.ipynb` y ejecuta todas las celdas.

4) Verifica en la consola de MinIO:
- URL: http://localhost:9001
- Usuario: `admin`
- Password: `supersecret`
