# Airflow en Kubernetes Local (Helm)

Este módulo entrega una base para que el curso pase de **Airflow con Docker Compose (Nivel 2)** a **Airflow en Kubernetes local (Nivel 3)** usando el Helm Chart oficial de Apache Airflow.

El enfoque es:
1. Despliegue paso a paso en clúster local.
2. Extensión del despliegue para incluir DAGs propios.

## 1. Objetivo de aprendizaje

Al finalizar esta guía, el estudiante podrá:
- Instalar Airflow en Kubernetes local con Helm.
- Validar estado de componentes (pods, release, servicio web).
- Empaquetar DAGs en una imagen custom.
- Actualizar el despliegue de Airflow para usar esa imagen.

## 2. Prerrequisitos

Tener instalados:
- `docker`
- `kubectl`
- `helm`

Validar herramientas:

```bash
docker --version
kubectl version --client
helm version
```

`kind` no es obligatorio. Solo se usa si el estudiante no tiene clúster local activo.

Si ya dispone de un clúster local (por ejemplo `microk8s`, `minikube`, `kubeadm` en VMs locales o Docker Desktop), no cree `kind`; solo asegure que `kubectl` apunte al contexto correcto:

```bash
kubectl config get-contexts
kubectl config use-context <su-contexto-local>
kubectl get nodes
```

### 2.0 ¿Cuándo usar kind?

Use `kind` solo si:
- no tiene clúster local instalado, o
- quiere un clúster temporal para laboratorio que pueda crear y borrar rápido.

Si ya tiene `microk8s` o Kubernetes local en Docker Desktop/kubeadm, continúe con ese clúster.

### 2.0.1 Instalación de kind (opcional)

macOS (Homebrew):

```bash
brew install kind
kind version
```

Linux:

```bash
curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.30.0/kind-linux-amd64
chmod +x ./kind
sudo mv ./kind /usr/local/bin/kind
kind version
```

Windows (Chocolatey):

```powershell
choco install kind
kind version
```

### 2.1 Instalación de Helm

Instale Helm según su sistema operativo:

macOS (Homebrew):

```bash
brew install helm
```

Ubuntu/Debian (script oficial):

```bash
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
```

Windows (Chocolatey):

```powershell
choco install kubernetes-helm
```

Windows (Scoop):

```powershell
scoop install helm
```

### 2.2 Validación de Helm con Kubernetes local

Verifique versión y conexión con el clúster actual:

```bash
helm version
kubectl config current-context
kubectl get nodes
```

Prueba rápida de Helm:

```bash
helm repo add apache-airflow https://airflow.apache.org
helm repo update
helm search repo apache-airflow/airflow
```

Si está en `microk8s`, asegure que `kubectl` apunte a ese clúster antes de usar Helm.
Si está en Docker Desktop, normalmente el contexto es `docker-desktop`.

## 3. Despliegue base (paso a paso)

### Paso 1: Definir clúster de trabajo

Si ya tiene clúster local, use ese contexto y continúe al Paso 2:

```bash
kubectl config current-context
kubectl get nodes
```

Si no tiene clúster local, cree uno con `kind`:

Se recomienda Kubernetes 1.30+:

```bash
kind create cluster --image kindest/node:v1.30.13
kubectl cluster-info --context kind-kind
kubectl get nodes
```

### Paso 2: Agregar repositorio de Airflow para Helm

```bash
helm repo add apache-airflow https://airflow.apache.org
helm repo update
```

### Paso 3: Definir namespace y release

```bash
export NAMESPACE=airflow-local
export RELEASE_NAME=airflow
kubectl create namespace $NAMESPACE
```

### Paso 4: Instalar Airflow (despliegue mínimo)

```bash
helm install $RELEASE_NAME apache-airflow/airflow \
  --namespace $NAMESPACE \
  -f Niveles/3/Airflow/values/values-local.yaml
```

Nota de compatibilidad:
- No mezcle chart reciente con imágenes antiguas de Airflow.
- Ejemplo de error típico por incompatibilidad: `invalid choice: 'api-server'`.
- Recomendación: en instalación base use la imagen por defecto del chart (sin fijar `images.airflow.tag`).

### Paso 5: Verificar despliegue

```bash
kubectl get pods -n $NAMESPACE
helm list -n $NAMESPACE
```

Espere a que los pods principales estén en `Running` o `Completed` (jobs de init).

### Paso 6: Exponer UI de Airflow localmente

```bash
kubectl port-forward svc/$RELEASE_NAME-api-server 8080:8080 -n $NAMESPACE
```

Abrir: `http://localhost:8080`

## 4. Opción útil para clase: activar DAGs de ejemplo

Para entornos de aprendizaje puede ser útil habilitar ejemplos:

```bash
helm upgrade --install $RELEASE_NAME apache-airflow/airflow \
  --namespace $NAMESPACE \
  --set-string "env[0].name=AIRFLOW__CORE__LOAD_EXAMPLES" \
  --set-string "env[0].value=True"
```

Para laboratorio evaluable, se sugiere dejarlo en `False` y usar DAGs propios.

## 5. Proyecto base para DAGs propios

En esta carpeta se incluye un punto de partida en:

- `proyecto_base/Dockerfile`
- `proyecto_base/requirements.txt`
- `proyecto_base/dags/hello_level3.py`

### Paso 1: Construir imagen custom

Desde `Niveles/3/Airflow/proyecto_base`:

```bash
cd Niveles/3/Airflow/proyecto_base
export AIRFLOW_BASE_TAG=3.1.8
docker build --pull \
  --build-arg AIRFLOW_BASE_TAG=$AIRFLOW_BASE_TAG \
  --tag airflow-local-dags:0.0.1 .
```

Recomendación importante:
- Mantenga `AIRFLOW_BASE_TAG` alineado con `APP VERSION` del chart instalado.
- Puede validarlo con: `helm status $RELEASE_NAME -n $NAMESPACE`.

### Paso 2: Cargar imagen en el clúster local

`kind`:

```bash
kind load docker-image airflow-local-dags:0.0.1
```

`minikube`:

```bash
minikube image load airflow-local-dags:0.0.1
```

`microk8s`:

```bash
docker save airflow-local-dags:0.0.1 | microk8s ctr -n k8s.io images import -
```

Docker Desktop Kubernetes:
- normalmente puede usar la imagen construida localmente sin paso adicional.
- si no la encuentra, use un registro local o cambie a estrategia con repo remoto.

### Paso 3: Actualizar Airflow para usar la imagen

```bash
helm upgrade --install $RELEASE_NAME apache-airflow/airflow \
  --namespace $NAMESPACE \
  --set images.airflow.repository=airflow-local-dags \
  --set images.airflow.tag=0.0.1 \
  -f ../values/values-local.yaml \
  --wait --timeout 20m
```

### Paso 4: Validar DAGs

- Ingrese a la UI de Airflow.
- Verifique que aparezca `hello_level3`.
- Ejecute el DAG manualmente y revise logs.

## 6. Estructura recomendada para que cada grupo trabaje

```text
Niveles/3/Airflow/proyecto_base/
  dags/
    dag_equipo_1.py
    dag_equipo_2.py
  requirements.txt
  Dockerfile
```

Flujo sugerido de trabajo:
1. Crear/editar DAGs en `dags/`.
2. Actualizar `requirements.txt` si se agregan librerías.
3. Reconstruir imagen con nueva versión (`0.0.2`, `0.0.3`, ...).
4. Cargar imagen según su clúster (`kind/minikube/microk8s`).
5. `helm upgrade ...` con el nuevo tag.

## 7. Archivo de valores base para local

Se incluye `values/values-local.yaml` con ajustes mínimos para laboratorio local:
- `executor: LocalExecutor`
- `LOAD_EXAMPLES=False`
- configuración simple para ejecutar en clúster local

Puede usarse desde la primera instalación:

```bash
helm upgrade --install $RELEASE_NAME apache-airflow/airflow \
  --namespace $NAMESPACE \
  -f values/values-local.yaml
```

## 8. Problemas frecuentes

1. `CrashLoopBackOff` en `airflow-api-server` con error `invalid choice: 'api-server'`
- Causa: incompatibilidad entre versión de chart y versión de imagen (por ejemplo, chart Airflow 3.x con imagen 2.x).
- Solución: reinstalar/actualizar usando imagen compatible con el chart o dejando la imagen por defecto del chart.

```bash
helm upgrade --install $RELEASE_NAME apache-airflow/airflow \
  --namespace $NAMESPACE \
  -f Niveles/3/Airflow/values/values-local.yaml \
  --wait --timeout 10m
```

2. `ImagePullBackOff` después del upgrade
- Causa probable: imagen no cargada en kind o tag incorrecto.
- Cargar imagen según su clúster (`kind/minikube/microk8s`) y repetir upgrade.
- En Docker Desktop, si persiste el error, usar un tag nuevo y validar que la imagen exista: `docker image ls | grep airflow-local-dags`.

3. No aparece el DAG nuevo
- Verificar que el archivo esté en `proyecto_base/dags/`.
- Reconstruir imagen y subir versión de tag.
- Confirmar en Helm qué imagen está activa:
  `kubectl get pod -n $NAMESPACE -o jsonpath='{..image}' | tr ' ' '\n'`

4. Servicio no abre en localhost
- Revisar si el `port-forward` sigue activo en la terminal.
- Validar nombre del servicio:
  `kubectl get svc -n $NAMESPACE`

## 9. Limpieza de laboratorio

```bash
helm uninstall $RELEASE_NAME -n $NAMESPACE
kubectl delete namespace $NAMESPACE
```

Si creó clúster con `kind`, elimínelo:

```bash
kind delete cluster
```
