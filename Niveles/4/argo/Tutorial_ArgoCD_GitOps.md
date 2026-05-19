# Tutorial: Argo CD + GitOps en Kubernetes Local

Este tutorial es un punto de partida para desplegar una API simple en Kubernetes local usando Argo CD bajo principio GitOps.

## 1. Objetivo

Al finalizar, el estudiante podrá:

1. Instalar Argo CD en clúster local,
2. enlazar un repositorio Git,
3. definir manifiestos Kubernetes como fuente de verdad,
4. crear una `Application` y sincronizar despliegue,
5. validar cómo un commit en Git se refleja en el clúster.

## 2. Prerrequisitos

- `kubectl`
- clúster local (`Docker Desktop`, `microk8s`, `minikube` o `kind`)
- acceso a repositorio GitHub del curso o fork

Validación:

```bash
kubectl config current-context
kubectl get nodes
```

## 3. Estructura base incluida

```text
Niveles/4/argo/gitops-api-base/
  manifests/api/
    namespace.yaml
    deployment.yaml
    service.yaml
  argocd/
    application-local-api.yaml
```

## 4. Instalar Argo CD en local

### Paso 1: crear namespace de Argo CD

```bash
kubectl create namespace argocd
```

### Paso 2: instalar Argo CD

```bash
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

### Paso 3: validar pods

```bash
kubectl get pods -n argocd
```

Espere hasta que los pods estén en `Running`.

## 5. Acceso a la UI de Argo CD

### Paso 1: port-forward

```bash
kubectl port-forward svc/argocd-server -n argocd 8081:443
```

Abrir: `https://localhost:8081`

### Paso 2: obtener clave inicial admin

```bash
kubectl -n argocd get secret argocd-initial-admin-secret \
  -o jsonpath="{.data.password}" | base64 --decode && echo
```

Usuario: `admin`

## 6. Enlazar repositorio Git

En Argo CD UI:
1. `Settings` -> `Repositories` -> `Connect Repo`.
2. Agregar URL del repositorio (HTTPS).
3. Si el repo es privado, registrar usuario/token.

Alternativa por CLI (si instala `argocd` CLI):

```bash
argocd login localhost:8081 --username admin --password <PASSWORD> --insecure
argocd repo add https://github.com/<ORG_O_USUARIO>/<REPO>.git
```

## 7. Definir manifiestos a desplegar

El despliegue base usa estos manifiestos:
- `namespace.yaml`: namespace `mlops-api`
- `deployment.yaml`: pod de API simple (`hashicorp/http-echo`)
- `service.yaml`: servicio interno `ClusterIP`

Ruta declarada en GitOps:

`Niveles/4/argo/gitops-api-base/manifests/api`

## 8. Crear Application de Argo CD

Edite `application-local-api.yaml` y reemplace:
- `repoURL`
- `targetRevision` (por ejemplo `main`)

Archivo:

`Niveles/4/argo/gitops-api-base/argocd/application-local-api.yaml`

Aplicar:

```bash
kubectl apply -f Niveles/4/argo/gitops-api-base/argocd/application-local-api.yaml
```

Verificar:

```bash
kubectl get applications -n argocd
kubectl get all -n mlops-api
```

## 9. Validar funcionamiento de la API

```bash
kubectl port-forward svc/simple-api -n mlops-api 8082:80
curl http://localhost:8082
```

Respuesta esperada:

`hola desde argo cd`

## 10. Flujo GitOps básico

1. Cambie un manifiesto en Git, por ejemplo `deployment.yaml`:
- modificar texto del contenedor (`-text=...`), o
- cambiar `replicas`.

2. Haga `commit` y `push` a la rama configurada.

3. Argo CD detecta drift y sincroniza automáticamente (`selfHeal` + `automated`).

4. Verifique cambios en clúster:

```bash
kubectl get deploy -n mlops-api
kubectl describe deploy simple-api -n mlops-api
```

## 11. Actividad propuesta

1. Reemplazar imagen demo por una API propia en Python (FastAPI o Flask).
2. Agregar manifiestos de `ConfigMap` y variables de entorno.
3. Definir estrategia de despliegue con al menos 2 réplicas.
4. Validar despliegue GitOps con 2 cambios consecutivos vía commit.
5. Documentar evidencia (capturas de Argo CD + salida de `kubectl`).

## 12. Limpieza

```bash
kubectl delete application simple-api-gitops -n argocd
kubectl delete namespace mlops-api
kubectl delete namespace argocd
```
