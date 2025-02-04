# FastAPI

FastAPI es una herramienta poderosa para construir APIs en Python de manera rápida y eficiente.

## ¿Qué es una API?

Una API (Application Programming Interface) es un conjunto de reglas que permite que diferentes aplicaciones se comuniquen entre sí. Existen diferentes tipos de APIs, pero en esta clase nos enfocaremos en las APIs REST, que utilizan HTTP para la comunicación.

## Beneficios de las APIs
- Facilitan la integración entre sistemas
- Permiten la separación de frontend y backend
- Son reutilizables y escalables
- Se pueden consumir desde aplicaciones web, móviles y otros servicios


FastAPI es un framework para construir APIs en Python, basado en Starlette y Pydantic, con las siguientes ventajas:

- Es rápido y eficiente
- Soporta validación automática de datos con Pydantic
- Genera automáticamente documentación interactiva con Swagger UI y ReDoc
- Usa tipado estático de Python para definir estructuras de datos
- Tiene soporte asíncrono (async/await) para mejorar el rendimiento


## 📌 Instalación

Para usar FastAPI, primero instalamos los paquetes necesarios:

```python
pip install fastapi uvicorn
```

`fastapi`: El framework para definir y manejar la API

`uvicorn`: Un servidor ASGI para ejecutar la API

## Creación de un archivo

[1_main](1_main.py)

## Ejecutación

Para ejecutar la API con Uvicorn, usamos:

```bash
uvicorn 1_main:app --reload
```
- `main`: Nombre del archivo sin la extensión .py

- `app`: Nombre de la instancia de FastAPI

- `--reload`: Habilita la recarga automática en desarrollo


Una vez corriendo, puedes acceder a la API en http://127.0.0.1:8000

### Swagger UI

FastAPI genera automáticamente la documentación de la API en http://127.0.0.1:8000/docs.


### ReDoc

También puedes ver la documentación en http://127.0.0.1:8000/redoc.

## Rutas y Métodos HTTP en FastAPI

FastAPI soporta diferentes métodos HTTP:

- `GET`: Obtener información.
- `POST`: Enviar datos al servidor.
- `PUT`: Actualizar un recurso existente.
- `DELETE`: Eliminar un recurso.

[2_metodos](2_metodos.py)

## Modelo de Datos con Pydantic

FastAPI usa Pydantic para validar datos de entrada, lo que permite definir estructuras de datos claras y seguras. Si se intenta enviar un objeto sin los campos correctos, FastAPI responderá con un error.

[3_modelo_de_datos](3_modelo_de_datos.py)

## Manejo de Respuestas y Estados HTTP

FastAPI permite personalizar las respuestas y los códigos de estado.

[4_respuestas_y_estados](4_respuestas_y_estados.py)
