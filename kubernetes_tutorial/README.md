# Kubernetes


[Kubernetes the hard way](https://github.com/kelseyhightower/kubernetes-the-hard-way).

Kubernetes, también conocido como K8s, es un sistema de código abierto para automatizar la implementación, el escalado y la gestión de aplicaciones en contenedores.


Agrupa los contenedores que componen una aplicación en unidades lógicas para facilitar la gestión y el descubrimiento. Kubernetes se basa en 15 años de experiencia en la ejecución de cargas de trabajo de producción en Google, combinado con las mejores ideas y prácticas de la comunidad.

---
## Instalación

### Minikube:
Es una distribución de Kubernetes orientada a nuevos usuarios y trabajo de desarrollo. Sin embargo, no está diseñado para implementaciones de producción, ya que solo puede ejecutar un clúster de un solo nodo en su máquina. [Instrucciones de instalación](https://minikube.sigs.k8s.io/docs/start/).


```bash
    curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
    sudo install minikube-linux-amd64 /usr/local/bin/minikube
```

Inicia el Cluster

    minikube start -p puj

Interactuar con su clúster
Si ya tiene instalado kubectl, ahora puede usarlo para acceder a su nuevo y brillante clúster:

    kubectl get po -A


### micrk8s:


[Instrucciones de instalación](https://microk8s.io/#install-microk8s).

Instalar Mocrok8s on Linux

    sudo snap install microk8s --classic

Validar el estado, revisar cuando kubernetes inicie y este listo

    microk8s status --wait-ready

Empezar a usar kubernetes

    microk8s kubectl get all --all-namespaces


Acceder al dashboard de Kubernetes
    
    microk8s dashboard-proxy


## Pasar de docker compose a kubernetes


Descargar, dar permisos y mover kompose


    curl -L https://github.com/kubernetes/kompose/releases/download/v1.26.0/kompose-linux-amd64 -o kompose
    chmod +x kompose
    sudo mv ./kompose /usr/local/bin/kompose
##### Este ejemplo esta pensado a partir de la informacion del taller 1
---


Mover taller1 a carpeta, para no modificar la entrega inicial.

    cp -a /source/. /dest/

Convertir docker compose a archivos de configuración yaml

    kompose convert
    # Usando una carpeta en especifico, especificando como tratar los volumenes
    kompose convert -f docker-compose.yml -o komposefiles/ --volumes hostPath


Nota: Si desea agregar balanceador de carga para poder exponer servicios, agregue lo siguiente en cada servicio.


    labels:
      kompose.service.type: LoadBalancer


```bash
INFO Network netinference is detected at Source, shall be converted to equivalent NetworkPolicy at Destination 
INFO Network netinference is detected at Source, shall be converted to equivalent NetworkPolicy at Destination 
INFO Network taller1-net-db is detected at Source, shall be converted to equivalent NetworkPolicy at Destination 
INFO Kubernetes file "inference-tcp-service.yaml" created 
INFO Kubernetes file "train-tcp-service.yaml" created 
INFO Kubernetes file "inference-deployment.yaml" created 
INFO Kubernetes file "netinference-networkpolicy.yaml" created 
INFO Kubernetes file "train-deployment.yaml" created 
INFO Kubernetes file "taller1-net-db-networkpolicy.yaml" created 
```

se debe aplicar estas configuraciones  agregando cada uno de los archivos de configuración creados, separados por coma

    microk8s kubectl apply -f inference-tcp-service.yaml,train-tcp-service.yaml,inference-deployment.yaml,netinference-networkpolicy.yaml,train-deployment.yaml,taller1-net-db-networkpolicy.yaml
    # Usando una carpeta en especifico
    microk8s kubectl apply -f komposefiles/



```bash
service/inference created
service/train created
deployment.apps/inference created
networkpolicy.networking.k8s.io/netinference configured
deployment.apps/train created
networkpolicy.networking.k8s.io/taller1-net-db created
```
Validar el estado de todo:

    microk8s kubectl get all --all-namespaces

Para ver especificamente los servicios:

    microk8s kubectl get service

Para exponer de manera temporal un servicio en especifico:


    microk8s kubectl port-forward --address 0.0.0.0 service/adminer 8080:8080


Si se desea borrar todos los componentes de un namespace especifico (default):


    microk8s kubectl delete --all daemonsets,replicasets,services,deployments,pods,rc,ingress --namespace=default


Mas informacion sobre kompose
https://kubernetes.io/docs/tasks/configure-pod-container/translate-compose-kubernetes/