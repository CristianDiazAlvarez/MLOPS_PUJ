# GitHub Actions para CI/CD básico

Este módulo conecta pruebas unitarias con automatización de integración y despliegue de imagen.

Objetivo:
- ejecutar pruebas automáticamente cuando hay cambios en una carpeta específica,
- publicar imagen en Docker Hub solo cuando los tests pasen y el cambio esté en `main`.

## Carpeta objetivo para el ejemplo

Usaremos como objetivo:

`Niveles/3/CICD/unit_testing/demo_app/**`

## Flujo esperado

1. En `push` o `pull_request` con cambios en la carpeta objetivo:
- se ejecuta job de pruebas unitarias (`pytest`).

2. Solo en `push` a `main`, y solo si las pruebas pasaron:
- se construye imagen,
- se publica en Docker Hub.

## Secrets requeridos en GitHub

En `Settings > Secrets and variables > Actions`, crear:
- `DOCKERHUB_USERNAME`
- `DOCKERHUB_TOKEN`

## Archivo workflow plantilla

Se incluye en:

`Niveles/3/CICD/github_actions/templates/ci-cd-unit-tests-dockerhub.yml`

Para activarlo, cópielo a:

`.github/workflows/ci-cd-unit-tests-dockerhub.yml`

## Actividad propuesta

1. Crear un módulo Python propio con pruebas unitarias.
2. Ajustar en el workflow el path monitoreado (`paths`).
3. Cambiar `IMAGE_NAME` por su usuario/repositorio Docker Hub.
4. Crear un Pull Request y validar que ejecuta pruebas.
5. Hacer merge a `main` y validar que publique imagen.

Evidencias sugeridas:
- captura de ejecución exitosa del job de tests,
- captura del job de publish en `main`,
- enlace a la imagen en Docker Hub.
