# Recursos

La idea es entender cómo limitar los recursos físicos que puede consumir un contenedor (CPU, RAM) y cómo estas restricciones afectan el comportamiento de las aplicaciones. Esto es fundamental cuando se desea empujar un sistema al límite, por ejemplo durante pruebas de rendimiento o despliegues en producción.

Docker, por defecto, permite a los contenedores usar todos los recursos disponibles del host (CPU, memoria). Esto puede generar problemas como:

- Contenedores que acaparan recursos y afectan a otros servicios.

- Uso descontrolado de memoria que lleva al Out of Memory (OOM) del sistema.

- Falta de realismo en pruebas de carga (si se hacen sin restricciones)

Al ejecutar docker compose puede ser las estadísticas de los contenedores usando:

```bash
docker stats
```

Ajuste los parámetros de memoria y cpu, ¿que sucede?
