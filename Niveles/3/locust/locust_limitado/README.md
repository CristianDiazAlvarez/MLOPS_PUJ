# Locust con recursos limitados

Este escenario une la prueba de carga de Locust con los límites de CPU y memoria
explicados en [`../../Recursos`](../../Recursos/). Los límites se aplican a cada
réplica de la API; Locust y Nginx quedan sin límite intencionalmente para reducir
la posibilidad de que el generador o el balanceador sean el cuello de botella.

## ¿Qué son un proxy y Nginx?

Un **proxy** es un intermediario. En lugar de que Locust conozca la dirección de
cada réplica, envía todas las peticiones a una sola dirección. El proxy recibe
esas peticiones y las reenvía a la API. En este caso se denomina **proxy
inverso** porque está delante de los servidores y representa a todo el servicio
frente al cliente.

**Nginx** (se pronuncia *engine-x*) es un servidor web de código abierto que,
entre otras funciones, puede actuar como proxy inverso y balanceador de carga.
Un **balanceador de carga** reparte las peticiones entre varias réplicas para que
no todas lleguen al mismo contenedor.

El recorrido de una petición en este ejemplo es:

```text
Locust  ->  Nginx:8000  ->  API réplica 1
                         ->  API réplica 2
                         ->  API réplica 3
```

Nginx ofrece una dirección estable aunque cambie la cantidad de réplicas. Desde
otro contenedor del mismo Compose esa dirección es `http://proxy:8000`; desde la
máquina local es `http://localhost:8000`; y desde otro equipo es
`http://IP_DE_LA_VM:8000`. Esto es necesario porque varias réplicas no pueden
publicar al mismo tiempo el mismo puerto del host. Nginx las descubre mediante
el DNS interno de Docker y distribuye las peticiones entre ellas.

En [`nginx.conf`](./nginx.conf):

- `resolver 127.0.0.11` usa el DNS interno de Docker.
- `upstream api_backend` define el grupo de contenedores que atenderá la carga.
- `listen 8000` indica el puerto en el que Nginx recibe las peticiones.
- `proxy_pass http://api_backend` reenvía cada petición a una réplica del grupo.

El servicio `api` no tiene `container_name`: un nombre fijo impediría crear tres
contenedores con `--scale api=3`.

## Requisitos

- Docker Engine o Docker Desktop con Docker Compose v2.
- Recursos suficientes asignados a Docker Desktop. Por ejemplo, no se pueden
  probar tres réplicas de 1 CPU si la máquina virtual de Docker dispone de una
  sola CPU.
- Puertos 8000 y 8089 disponibles, o las variables `API_PORT` y `LOCUST_PORT`
  configuradas con otros valores.

## Prueba desde la interfaz web

Desde esta carpeta, inicie una réplica limitada a 1 CPU y 1 GB:

```bash
API_CPUS=1.0 API_MEMORY=1g docker compose --profile load up --build
```

Abra `http://localhost:8089`. El host ya está configurado como
`http://proxy:8000`: dentro de la red de Docker, `proxy` es el nombre del
contenedor Nginx. Aumente gradualmente los usuarios y observe los recursos en
otra terminal:

```bash
docker stats
```

Detenga el escenario antes de cambiar límites o cantidad de réplicas:

```bash
docker compose --profile load down
```

## Prueba headless reproducible

Primero inicie únicamente la API y el balanceador. Este ejemplo crea una réplica
limitada a 1 CPU y 1 GB:

```bash
API_CPUS=1.0 API_MEMORY=1g docker compose up --build -d --scale api=1 api proxy
```

Este comando significa:

- `API_CPUS=1.0 API_MEMORY=1g`: define los límites de cada réplica.
- `docker compose up`: crea e inicia los servicios.
- `--build`: reconstruye la imagen si el código cambió.
- `-d`: deja los contenedores ejecutándose en segundo plano.
- `--scale api=1`: solicita una réplica de `api`; use `api=3` para crear tres.
- `api proxy`: inicia únicamente la API y Nginx, no Locust.

Construya la imagen de Locust la primera vez:

```bash
docker compose build locust
```

Luego ejecute una prueba de dos minutos. `docker compose run` crea un contenedor
temporal del servicio `locust`, ejecuta la prueba y lo elimina al terminar. Esto
permite usar Locust sin instalar Python ni paquetes directamente en la máquina.
El Compose ya configura internamente `locust -f locustfile.py`; por eso el
comando siguiente solo agrega las opciones de la prueba:

```bash
docker compose run --rm --no-deps locust \
  --headless \
  --host http://proxy:8000 \
  --users 500 \
  --spawn-rate 50 \
  --run-time 2m \
  --csv /resultados/cpu1_ram1g_rep1_u500 \
  --only-summary
```

Cada parte tiene una función:

- `run`: ejecuta una tarea puntual en un contenedor nuevo, en lugar de dejar el
  servicio funcionando permanentemente.
- `--rm`: elimina ese contenedor temporal al terminar; no elimina los CSV.
- `--no-deps`: no intenta iniciar las dependencias de Locust. Es especialmente
  importante cuando la API está en otra VM.
- `locust`: es el servicio de Compose que se usará como generador de carga.
- `--headless`: ejecuta Locust sin interfaz web.
- `--host`: indica dónde está el sistema que recibirá la carga.
- `--users 500`: mantiene hasta 500 usuarios virtuales concurrentes.
- `--spawn-rate 50`: crea 50 usuarios virtuales por segundo hasta llegar a 500.
- `--run-time 2m`: detiene la prueba después de dos minutos.
- `--csv`: guarda las estadísticas en la carpeta `resultados`.
- `--only-summary`: muestra solamente el resumen final.

Un usuario virtual no equivale a una petición por segundo. Cada usuario ejecuta
la tarea y respeta el `wait_time` definido en `locustfile.py` antes de repetirla.

Locust genera archivos CSV dentro de `resultados/`. Si hay fallos, el comando
termina con un código distinto de cero. Eso es esperado durante la búsqueda del
límite: los CSV siguen siendo útiles para el análisis. Para el siguiente nivel,
cambie `--users` y conserve la duración, la tasa de aparición y el
`locustfile.py` para que las comparaciones sean válidas.

## Ejecución desde otra máquina

En el taller evaluado, la API, Nginx y sus demás dependencias se ejecutan en una
VM; Locust se ejecuta en una segunda VM o en la máquina personal. Reemplace
`IP_DE_LA_VM` por la dirección alcanzable de la VM que aloja Nginx:

```bash
docker compose run --rm --no-deps locust \
  --headless \
  --host http://IP_DE_LA_VM:8000 \
  --users 500 \
  --spawn-rate 50 \
  --run-time 2m \
  --csv /resultados/cpu1_ram1g_rep1_u500 \
  --only-summary
```

El puerto 8000 de la VM debe aceptar conexiones desde la máquina generadora. Si
la VM está en la nube, limite la regla de red o firewall a la IP de esa máquina;
no exponga el puerto a todo Internet. Compruebe primero la conectividad abriendo
`http://IP_DE_LA_VM:8000/docs` desde la máquina que ejecutará Locust.

Al terminar, ejecute lo siguiente en la VM que aloja la API y Nginx:

```bash
docker compose down
```

> `API_CPUS` y `API_MEMORY` se aplican **a cada réplica**. Tres réplicas con 1 CPU
> y 1 GB pueden consumir hasta 3 CPU y 3 GB en total, además de los recursos de
> Nginx y de los otros servicios. La VM debe tener capacidad suficiente para que
> Docker pueda aplicar esta comparación.

## Actividad en clase: efecto de CPU, memoria y réplicas

En grupos, ejecute los casos de la siguiente matriz con el ejemplo incluido en
esta carpeta. Cada grupo debe modificar una sola variable a la vez, observar
`docker stats` y registrar RPS, fallos y p95. Después compare los resultados con
el resto de la clase. Esta actividad sirve para comprender los límites; no
reemplaza el taller con las máquinas separadas.

| Caso | CPU por réplica | RAM por réplica | Réplicas | CPU total máxima | RAM total máxima |
|---|---:|---:|---:|---:|---:|
| CPU baja | 0.5 | 1 GB | 1 | 0.5 | 1 GB |
| Base | 1.0 | 1 GB | 1 | 1.0 | 1 GB |
| Más CPU | 2.0 | 1 GB | 1 | 2.0 | 1 GB |
| RAM baja | 1.0 | 128 MB | 1 | 1.0 | 128 MB |
| Más RAM | 1.0 | 2 GB | 1 | 1.0 | 2 GB |
| Escala horizontal | 1.0 | 1 GB | 3 | 3.0 | 3 GB |
| Réplicas, CPU fija total | 0.33 | 1 GB | 3 | 0.99 | 3 GB |

128 MB puede no bastar para una API o un modelo real. Si el contenedor termina
por falta de memoria, registre el caso como OOM en vez de interpretar la ausencia
de respuestas como rendimiento bajo. Confírmelo con:

```bash
docker compose ps -a
docker inspect "$(docker compose ps -q api | head -n 1)" \
  --format '{{.State.OOMKilled}}'
```

## Registro de resultados

Una configuración soporta un nivel solamente si cumple el criterio definido
durante toda la ventana estable. Una propuesta para este taller es menos de 1 %
de fallos y p95 menor a 500 ms durante dos minutos.

| CPU/réplica | RAM/réplica | Réplicas | Usuarios | RPS | Peticiones | Fallos % | p95 | CPU observada | RAM observada | Cumple |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|:---:|
| | | | | | | | | | | |

La capacidad máxima sostenible es el último nivel que cumple el criterio, no el
mayor número que Locust permite escribir. Reporte tanto usuarios concurrentes
como RPS, porque no son medidas equivalentes.
