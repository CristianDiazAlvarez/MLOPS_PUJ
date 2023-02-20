# Data Validation


## Tensor Flow Data Validation

---

Instalation of TFX may be a complex process, that why docker it is usefull tool. Also each important framework generate an image to use their tools, this is the case of TFX. There are an example for use this container using a volume to keep data saved over the host machine. Also the container expose a jupyter lab instance ready to work.


---
```bash
    sudo docker run -it --name tfx --rm -p 8888:8888 -p 6006:6006 -v $PWD:/tfx/src --entrypoint /run_jupyter.sh  tensorflow/tfx:1.12.0
```

---

Understanding the docker command:

- **-it** allow an interactive mode
- **--name tfx** set a specific name to the container in this case 'tfx'
- **--rm** remove any continer if named as tfx
- **-p** publish or expose port host_port:container_port
- **-v** mount bind volume as file or folder. host_folder:docker_folder
- **--entrypoint** stablish command to run and set container life as this command 
- **tensorflow/tfx** define docker image as default search local then on dockerhub

---


TFDV notebook shows an example over diabetes data of how to use TFDV based on TF example.




---
## pycaret


Build own images are common practices, in this case, the **Dockerfile** file let us the posibility to create an image ready to use pycaret library exposed on a Jupyter Lab. Please Check requierements.txt and Dockerfile.

---
```bash
    docker build -t pycaret .
    docker run -it --name pycaret --rm -e TZ=America/Bogota -p 8888:8888 -v $PWD:/work pycaret:latest
```

---

Understanding the docker command:

- **-it** allow an interactive mode
- **--name pycaret** set a specific name to the container in this case 'pycaret'
- **-e TZ=America/Bogota** Set env variable in the container, this modify time zone
- **--rm** remove any continer if named as tfx
- **-p** publish or expose port host_port:container_port
- **-v** mount bind volume as file or folder. host_folder:docker_folder
- **pycaret:latest** define docker image created by previous docker comand

---

**pycaret** notebook shows an example over diabetes data of how to use **pycaret** based on Docs example.