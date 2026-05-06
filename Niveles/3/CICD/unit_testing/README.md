# Unit Testing con Pytest

Este módulo presenta lo mínimo necesario para que los estudiantes entiendan pruebas unitarias en Python y las ejecuten en contenedor.

## ¿Qué es una prueba unitaria?

Una prueba unitaria valida una función pequeña y aislada, con entradas conocidas y salidas esperadas.

Objetivos en este curso:
- verificar lógica de negocio antes de desplegar,
- detectar regresiones temprano,
- integrar pruebas automáticas en CI/CD.

## Estructura del demo

```text
unit_testing/
  demo_app/
    app.py
    tests/test_app.py
    requirements.txt
    Dockerfile
```

## Ejecutar local (sin contenedor)

Desde `Niveles/3/CICD/unit_testing/demo_app`:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -q
```

## Ejecutar en contenedor

Desde `Niveles/3/CICD/unit_testing/demo_app`:

```bash
docker build -t unit-testing-demo:0.0.1 .
docker run --rm unit-testing-demo:0.0.1
```

## Actividad propuesta

Construya una mini API o script Python para preprocesamiento con al menos 3 funciones, por ejemplo:
1. limpieza de texto,
2. validación de rangos numéricos,
3. transformación de features.

Requisitos de la actividad:
1. crear archivo `app.py` (o módulo equivalente),
2. crear carpeta `tests/` con mínimo 6 pruebas,
3. incluir al menos 1 caso de error con `pytest.raises`,
4. crear `Dockerfile` que ejecute `pytest`,
5. demostrar ejecución exitosa en contenedor.

Criterio de aprobación sugerido:
- `pytest` pasa al 100%.
- pruebas cubren casos normales y de borde.
- contenedor ejecuta pruebas sin intervención manual.
