# Kubernetes

[Kubernetes the hard way](https://github.com/kelseyhightower/kubernetes-the-hard-way).

Kubernetes, también conocido como K8s, es un sistema de código abierto para automatizar la implementación, el escalado y la gestión de aplicaciones en contenedores.

Agrupa los contenedores que componen una aplicación en unidades lógicas para facilitar la gestión y el descubrimiento. Kubernetes se basa en 15 años de experiencia en la ejecución de cargas de trabajo de producción en Google, combinado con las mejores ideas y prácticas de la comunidad.

En este nivel se instalará Kubernetes sobre las máquinas virtuales de la universidad (**Rocky Linux**) usando **Rancher**.

---

## ¿Qué es Rancher?

[Rancher](https://www.rancher.com/) es una plataforma de código abierto (de SUSE) para **crear, administrar y operar clústeres de Kubernetes** desde una sola interfaz web. Con Rancher se puede:

- Crear clústeres nuevos (usando sus distribuciones **RKE2** o **K3s**) sobre máquinas propias, en la nube o en VMs.
- Importar clústeres existentes (EKS, AKS, GKE, microk8s, etc.).
- Administrar workloads, servicios, namespaces, usuarios y permisos de forma gráfica.
- Abrir una terminal `kubectl` desde el navegador y descargar el `kubeconfig` de cada clúster.

### Un clúster de Kubernetes dentro de un contenedor

La forma más sencilla de instalar Rancher es como **un solo contenedor Docker**. Lo interesante es que, para funcionar, Rancher necesita a su vez un Kubernetes donde guardar su estado. Por eso, al iniciar el contenedor `rancher/rancher`, este levanta internamente un clúster **K3s** (un Kubernetes liviano) de un solo nodo. En la interfaz este clúster aparece con el nombre **`local`**.

```text
┌──────────────────────────── VM Rocky Linux ────────────────────────────┐
│  Docker                                                                │
│  ┌───────────────── contenedor rancher/rancher (--privileged) ──────┐  │
│  │  K3s (clúster "local")                                           │  │
│  │   ├── API server, scheduler, controller manager, etcd/kine       │  │
│  │   ├── containerd ──► pods de Rancher (cattle, fleet, webhook…)   │  │
│  │   └── containerd ──► pods que despleguemos nosotros              │  │
│  └──────────────────────────────────────────────────────────────────┘  │
│        ▲ puertos 80 / 443 (UI web y API de Rancher)                    │
└────────────────────────────────────────────────────────────────────────┘
```

Es decir, **los contenedores (pods) de Kubernetes corren dentro de otro contenedor**. Por eso el contenedor se ejecuta con `--privileged`: K3s necesita acceso al kernel del host (módulos de `iptables`, cgroups, redes) para crear la red de los pods y ejecutar sus propios contenedores.

Puntos importantes:

- El clúster `local` es ideal para **aprender y hacer pruebas**, pero **no es una instalación de producción** (un solo nodo, todo dentro de un contenedor).
- Para un clúster real, Rancher se usa como "panel de control" y se crean **clústeres downstream** (RKE2/K3s) en otras VMs, que se registran ante Rancher. Esto se explica en la sección [Agregar múltiples nodos](#agregar-múltiples-nodos-al-clúster).

---

## Instalación de Rancher en Rocky Linux

Guía de referencia: [Working with Rancher and Kubernetes - Rocky Linux Documentation](https://docs.rockylinux.org/10/guides/containers/rancher_and_kubernetes/)

Prerrequisito: tener **Docker** instalado en la VM. Para validarlo:

```bash
    docker --version
    sudo systemctl status docker
```

### 1. Cargar los módulos del kernel

K3s (dentro del contenedor) necesita algunos módulos de `iptables` del kernel del host. Se configuran para que carguen automáticamente al iniciar:

```bash
    sudo vim /etc/modules-load.d/rancher.conf
```

Presionar la tecla `i` para escribir y pegar:

```text
ip_tables
ip_conntrack
iptable_filter
ipt_state
```

Guardar y salir con `Esc` y luego `:wq`.

Luego reiniciar la VM para que se carguen los módulos:

```bash
    sudo reboot
```

Esto va a cerrar la sesión de terminal. Esperar unos segundos y volver a iniciar la conexión SSH.

Validar que los módulos estén cargados:

```bash
    lsmod | grep -E "ip_tables|iptable_filter|conntrack"
```

### 2. Descargar y ejecutar Rancher

```bash
    docker pull rancher/rancher:latest

    docker run -d --name=rancher --privileged --restart=unless-stopped -p 80:80 -p 443:443 rancher/rancher:latest
```

- `--privileged`: necesario para que K3s pueda ejecutarse dentro del contenedor.
- `--restart=unless-stopped`: el contenedor se reinicia solo si la VM o Docker se reinician.
- `-p 80:80 -p 443:443`: expone la interfaz web y la API de Rancher.

### 3. Abrir el firewall

```bash
    sudo systemctl enable --now firewalld
    sudo firewall-cmd --permanent --zone=public --add-service=https
    sudo firewall-cmd --zone=public --add-service=https
```

### 4. Obtener la contraseña inicial (Bootstrap Password)

Rancher tarda un par de minutos en iniciar. Luego se obtiene la contraseña inicial con:

```bash
    docker logs rancher  2>&1 | grep "Bootstrap Password:"
```

Abrir en el navegador `https://<IP_DE_LA_VM>`. El certificado es autofirmado, así que el navegador mostrará una advertencia; se debe aceptar para continuar. Ingresar la contraseña inicial, definir una nueva contraseña para el usuario `admin` y confirmar la **Server URL** (la IP o nombre de la VM, que es la dirección que usarán los otros nodos para comunicarse con Rancher).

### Comandos útiles de Docker

Validar el estado de Docker:

```bash
    sudo systemctl status docker
```

Reiniciar Docker:

```bash
    sudo systemctl restart docker
```

Ver los logs de Rancher en tiempo real (aquí se puede ver cómo se crea el clúster K3s interno):

```bash
    docker logs -f $(docker ps -q --filter ancestor=rancher/rancher)
```

---

## Probar el clúster

### Desde la interfaz web

1. En el menú principal ir a **Cluster Management**; debe aparecer el clúster `local` en estado **Active**.
2. Entrar al clúster `local` y revisar **Nodes**, **Workloads** y **Namespaces**.
3. En la parte superior derecha está el botón **Kubectl Shell** (icono `>_`), que abre una terminal con `kubectl` ya configurado:

```bash
    kubectl get nodes
    kubectl get pods --all-namespaces
```

### Desde la terminal de la VM, dentro del contenedor

El contenedor de Rancher trae `kubectl`, así que se puede consultar el clúster interno directamente:

```bash
    docker exec -it rancher kubectl get nodes
    docker exec -it rancher kubectl get pods --all-namespaces
```

Se observará un único nodo (el propio contenedor) y los pods del sistema de Rancher (`cattle-system`, `cattle-fleet-system`, `kube-system`, etc.).

### Desde la terminal de la VM con kubectl (recomendado)

Instalar `kubectl` en la VM:

```bash
    curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
    sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
    kubectl version --client
```

En la interfaz de Rancher, entrar al clúster y usar el botón **Download KubeConfig** (o **Copy KubeConfig to Clipboard**). Guardar el contenido en `~/.kube/config`:

```bash
    mkdir -p ~/.kube
    vim ~/.kube/config   # pegar el contenido del kubeconfig
    chmod 600 ~/.kube/config
```

Probar:

```bash
    kubectl get nodes
    kubectl get all --all-namespaces
```

### Prueba rápida: desplegar una aplicación

```bash
    kubectl create deployment hola --image=nginx
    kubectl get pods -w          # esperar a que el pod quede en Running (Ctrl+C para salir)
    kubectl expose deployment hola --port=80
    kubectl port-forward --address 0.0.0.0 service/hola 8081:80
```

En otra terminal (o desde el navegador, si el puerto está abierto en el firewall) consultar `http://<IP_DE_LA_VM>:8081`. Debe responder la página de bienvenida de nginx. El despliegue también se puede ver en Rancher, en **Workloads > Deployments**.

Limpiar:

```bash
    kubectl delete service hola
    kubectl delete deployment hola
```

---

## Pasar de docker compose a kubernetes

Ahora se usa [kompose](https://kompose.io/) para convertir un `docker-compose.yml` a los manifiestos de Kubernetes y desplegarlos en el clúster de Rancher.

Descargar, dar permisos y mover kompose:

```bash
    curl -L https://github.com/kubernetes/kompose/releases/download/v1.34.0/kompose-linux-amd64 -o kompose
    chmod +x kompose
    sudo mv ./kompose /usr/local/bin/kompose
    kompose version
```

### Este ejemplo esta pensado a partir de un proceso de inferencia simple

Se usa el [docker-compose.yml](docker-compose.yml) de esta carpeta (servicios `adminer`, `train` e `inference`).

Convertir docker compose a archivos de configuración yaml:

```bash
    kompose convert
    # Usando una carpeta en especifico, especificando como tratar los volumenes
    kompose convert -f docker-compose.yml -o komposefiles/ --volumes hostPath
```

Nota: Si desea agregar balanceador de carga para poder exponer servicios, agregue lo siguiente en cada servicio.

```yaml
    labels:
      kompose.service.type: LoadBalancer
```

En una instalación sin balanceador de carga externo (como las VMs de la universidad) se puede usar `NodePort` en lugar de `LoadBalancer`, lo que expone el servicio en un puerto entre 30000 y 32767 de cada nodo.

```bash
INFO Network netinference is detected at Source, shall be converted to equivalent NetworkPolicy at Destination 
INFO Network taller1-net-db is detected at Source, shall be converted to equivalent NetworkPolicy at Destination 
INFO Kubernetes file "komposefiles/adminer-service.yaml" created 
INFO Kubernetes file "komposefiles/inference-service.yaml" created 
INFO Kubernetes file "komposefiles/train-service.yaml" created 
INFO Kubernetes file "komposefiles/adminer-deployment.yaml" created 
INFO Kubernetes file "komposefiles/inference-deployment.yaml" created 
INFO Kubernetes file "komposefiles/netinference-networkpolicy.yaml" created 
INFO Kubernetes file "komposefiles/train-deployment.yaml" created 
INFO Kubernetes file "komposefiles/taller1-net-db-networkpolicy.yaml" created 
```

Se deben aplicar estas configuraciones agregando cada uno de los archivos de configuración creados, separados por coma:

```bash
    kubectl apply -f adminer-service.yaml,adminer-deployment.yaml,inference-service.yaml,inference-deployment.yaml,train-service.yaml,train-deployment.yaml
    # Usando una carpeta en especifico
    kubectl apply -f komposefiles/
```

```bash
deployment.apps/adminer created
service/adminer created
deployment.apps/inference created
service/inference created
networkpolicy.networking.k8s.io/netinference created
networkpolicy.networking.k8s.io/taller1-net-db created
deployment.apps/train created
service/train created
```

Si no se instaló `kubectl` en la VM, hay dos alternativas:

- Copiar los archivos al contenedor de Rancher y aplicarlos desde ahí:

    ```bash
        docker cp komposefiles rancher:/tmp/komposefiles
        docker exec -it rancher kubectl apply -f /tmp/komposefiles/
    ```

- En la interfaz de Rancher, usar el botón **Import YAML** (icono de flecha hacia arriba, parte superior derecha) y pegar el contenido de los archivos.

Validar el estado de todo:

```bash
    kubectl get all --all-namespaces
```

Para ver especificamente los servicios:

```bash
    kubectl get service
```

Los mismos recursos se pueden revisar en Rancher en **Workloads** y en **Service Discovery > Services**, incluyendo logs y una terminal dentro de cada pod.

Para exponer de manera temporal un servicio en especifico:

```bash
    kubectl port-forward --address 0.0.0.0 service/adminer 8080:8080
```

Si se desea borrar todos los componentes de un namespace especifico (default):

```bash
    kubectl delete --all daemonsets,replicasets,services,deployments,pods,rc,ingress,networkpolicies --namespace=default
```

Mas informacion sobre [kompose](https://kubernetes.io/docs/tasks/configure-pod-container/translate-compose-kubernetes/)

---

## Agregar múltiples nodos al clúster

El clúster `local` (K3s dentro del contenedor) **no admite agregar nodos**: es de uso interno de Rancher. Para tener un clúster de varios nodos se crea un **clúster Custom (RKE2 o K3s)** desde Rancher, usando otras VMs como nodos. Rancher genera un comando de registro que se ejecuta en cada VM; este instala un agente que descarga e instala Kubernetes y une la VM al clúster.

Referencias:

- [Rocky Linux - Rancher and Kubernetes (sección de clúster on-premise)](https://docs.rockylinux.org/10/guides/containers/rancher_and_kubernetes/)
- [Rancher - Launching Kubernetes on Existing Custom Nodes](https://ranchermanager.docs.rancher.com/reference-guides/cluster-configuration/rancher-server-configuration/use-existing-nodes)
- [Rancher - Node Requirements / Port Requirements](https://ranchermanager.docs.rancher.com/getting-started/installation-and-upgrade/installation-requirements/port-requirements)

### Arquitectura sugerida

```text
            ┌──────────────────────┐
            │  VM 1: Rancher       │   (contenedor rancher/rancher, solo administración)
            │  https://<IP_VM1>    │
            └──────────┬───────────┘
                       │ registro de nodos (443)
     ┌─────────────────┼─────────────────┐
     ▼                 ▼                 ▼
┌──────────┐     ┌──────────┐     ┌──────────┐
│  VM 2    │     │  VM 3    │     │  VM 4    │
│ etcd     │     │ worker   │     │ worker   │
│ control  │     │          │     │          │
│ worker   │     │          │     │          │
└──────────┘     └──────────┘     └──────────┘
      clúster "mlops" (RKE2)
```

Roles de un nodo:

| Rol | Función |
| --- | --- |
| **etcd** | Base de datos clave-valor donde se guarda todo el estado del clúster. |
| **Control Plane** | API server, scheduler y controller manager: toman las decisiones del clúster. |
| **Worker** | Ejecuta los pods de las aplicaciones. |

Consideraciones:

- **No registrar como nodo la misma VM donde corre el contenedor de Rancher**: entran en conflicto los puertos 80/443 y los componentes de Kubernetes.
- El clúster necesita al menos un nodo con cada rol. Un nodo puede tener los tres roles.
- Los nodos con rol etcd/control plane deben ser un número **impar** (1, 3, 5) para mantener el quórum.
- En los nodos **no es necesario instalar Docker**: RKE2 y K3s traen su propio `containerd`.
- Cada VM debe tener un **hostname único** y poder conectarse a la VM de Rancher por el puerto 443.

### 1. Preparar cada VM que será nodo

Asignar un hostname único (por ejemplo `nodo1`, `nodo2`, ...):

```bash
    sudo hostnamectl set-hostname nodo1
```

Kubernetes administra sus propias reglas de red, por lo que la guía de Rocky Linux recomienda desactivar `firewalld` en los nodos y usar `nftables`:

```bash
    sudo systemctl stop firewalld
    sudo systemctl disable firewalld
    sudo systemctl start nftables
    sudo systemctl enable nftables
```

Si se prefiere mantener `firewalld` activo, se deben abrir los puertos que usa RKE2 entre los nodos:

```bash
    sudo firewall-cmd --permanent --add-port=9345/tcp         # registro de nodos RKE2
    sudo firewall-cmd --permanent --add-port=6443/tcp         # API de Kubernetes
    sudo firewall-cmd --permanent --add-port=10250/tcp        # kubelet
    sudo firewall-cmd --permanent --add-port=2379-2381/tcp    # etcd
    sudo firewall-cmd --permanent --add-port=8472/udp         # red de pods (Canal/VXLAN)
    sudo firewall-cmd --permanent --add-port=9099/tcp         # health check de Canal
    sudo firewall-cmd --permanent --add-port=30000-32767/tcp  # servicios NodePort
    sudo firewall-cmd --permanent --add-service=http --add-service=https  # ingress
    sudo firewall-cmd --reload
```

### 2. Crear el clúster en Rancher

1. En Rancher ir a **Cluster Management > Clusters > Create**.
2. En la sección *Use existing nodes and create a cluster using RKE2/K3s* seleccionar **Custom**.
3. Asignar un nombre (por ejemplo `mlops`), dejar la versión de Kubernetes por defecto (RKE2) y dar clic en **Create**.
4. Rancher abre la pestaña **Registration**.

### 3. Registrar los nodos

1. En **Registration**, seleccionar los roles del nodo que se va a agregar (para el primero: **etcd**, **Control Plane** y **Worker**).
2. Como Rancher usa un certificado autofirmado, marcar la casilla **Insecure: Select this to skip TLS verification** (agrega `--insecure` al `curl`).
3. Copiar el comando generado. Tiene una forma similar a:

    ```bash
        curl --insecure -fL https://<IP_VM1>/system-agent-install.sh | sudo sh -s - \
          --server https://<IP_VM1> --label 'cattle.io/os=linux' \
          --token <TOKEN> --ca-checksum <CHECKSUM> \
          --etcd --controlplane --worker
    ```

4. Ejecutar el comando por SSH en la VM que será nodo.
5. Repetir en las demás VMs, cambiando los roles antes de copiar el comando (por ejemplo, solo **Worker** para los nodos de trabajo).

El clúster pasa por los estados **Updating** → **Active**. El primer nodo puede tardar varios minutos, mientras descarga e instala RKE2.

Para ver el progreso en un nodo:

```bash
    sudo journalctl -u rancher-system-agent -f
    # cuando ya se instaló RKE2
    sudo journalctl -u rke2-server -f    # nodos etcd / control plane
    sudo journalctl -u rke2-agent -f     # nodos solo worker
```

### 4. Validar el clúster multinodo

En Rancher, entrar al clúster `mlops` > **Nodes**: deben aparecer todos los nodos en estado **Active** con sus roles.

Descargar el kubeconfig de **este** clúster (**Download KubeConfig**) y usarlo con `kubectl`:

```bash
    kubectl --kubeconfig ~/.kube/mlops.yaml get nodes -o wide
```

```bash
NAME    STATUS   ROLES                       AGE   VERSION
nodo1   Ready    control-plane,etcd,master   15m   v1.xx.x+rke2r1
nodo2   Ready    worker                      8m    v1.xx.x+rke2r1
nodo3   Ready    worker                      6m    v1.xx.x+rke2r1
```

También es posible usar `kubectl` directamente en un nodo de control plane:

```bash
    sudo /var/lib/rancher/rke2/bin/kubectl --kubeconfig /etc/rancher/rke2/rke2.yaml get nodes
```

Para comprobar que los pods se reparten entre nodos, desplegar los archivos de kompose en este clúster y escalar un deployment:

```bash
    kubectl --kubeconfig ~/.kube/mlops.yaml apply -f komposefiles/
    kubectl --kubeconfig ~/.kube/mlops.yaml scale deployment inference --replicas=4
    kubectl --kubeconfig ~/.kube/mlops.yaml get pods -o wide   # columna NODE
```

### Quitar o reutilizar un nodo

Eliminar el nodo desde Rancher (**Nodes > ⋮ > Delete**) y luego limpiar la VM antes de registrarla de nuevo:

```bash
    sudo /usr/local/bin/rancher-system-agent-uninstall.sh
    sudo /usr/local/bin/rke2-uninstall.sh
```

---

## Otras alternativas de instalación

Estas opciones sirven para pruebas locales en un solo nodo.

### Minikube

Es una distribución de Kubernetes orientada a nuevos usuarios y trabajo de desarrollo. Sin embargo, no está diseñado para implementaciones de producción, ya que solo puede ejecutar un clúster de un solo nodo en su máquina. [Instrucciones de instalación](https://minikube.sigs.k8s.io/docs/start/).

```bash
    curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
    sudo install minikube-linux-amd64 /usr/local/bin/minikube
    minikube start -p puj
    minikube kubectl -p puj -- get all
```

### microk8s

[Instrucciones de instalación](https://microk8s.io/#install-microk8s).

```bash
    sudo snap install microk8s --classic
    microk8s status --wait-ready
    microk8s kubectl get all --all-namespaces
    microk8s dashboard-proxy
```

Con estas alternativas, los comandos `kubectl` de esta guía se reemplazan por `minikube kubectl -p puj --` o `microk8s kubectl`.
