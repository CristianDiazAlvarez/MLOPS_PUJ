# Data Validation

Instalation of TFX may be a complex process, that why docker it is usefull tool. Also each important framework generate an image to use their tools, this is the case of TFX. There are an example for use this container using a volume to keep data saved over the host machine. Also the container expose a jupyter lab instance ready to work.


---

`sudo docker run -it --name tfx --rm -p 8888:8888 -p 6006:6006 -v $PWD:/tfx/src --entrypoint /run_jupyter.sh  tensorflow/tfx`

---

Understand the command:

- -it allow an interactive mode
- --name tfx set a specific name to the container in this case 'tfx'
- --rm remove any continer if named as tfx
- -p