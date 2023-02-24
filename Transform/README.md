```bash
    docker build -t tfx_custom .
    docker rmi $(docker images --filter "dangling=true" -q --no-trunc)
    sudo docker run -it --name tfx_custom -e TZ=America/Bogota --rm -p 8888:8888  -v $PWD:/work tfx_custom
```