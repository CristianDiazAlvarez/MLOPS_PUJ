---
## pycaret


Build own images are common practices, in this case, the **Dockerfile** file let us the posibility to create an image ready to use pycaret library exposed on a Jupyter Lab. Please Check requierements.txt and Dockerfile.

---
```bash
    docker build -t pycaret .
    docker run -it --name pycaret --rm -e TZ=America/Bogota -p 8888:8888 -v $PWD:/work pycaret:latest
    docker rmi $(docker images --filter "dangling=true" -q --no-trunc)
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