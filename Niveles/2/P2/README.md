## Herramienta proyecto 2

Esta carpeta contiene lo necesario para entregar a los estudiantes del curso los datos para desarrollar el proyecto 2

La información se entrega mediante una API, la cual requiere el numero del grupo, para poder entregar la infromación.

## Funcionamiento de la API

Los datos serán obtenidos a través de una API externa expuesta en la maquina virtual asignada al profesor alojada en la dirección IP http://10.43.101.149:80. Esta API proporcionará un conjunto de datos aleatorios que cambiarán cada 5 minutos. Los estudiantes deberán implementar un mecanismo para recolectar estos datos usando Airflow y utilizarlos para entrenar un modelo de IA en el entorno de MLflow.

El conjunto de datos fue divido en 10 partes (batch), por lo tanto para obtener cada una de esas 10 partes se debe hacer una petición, a la cual solo se solicitará el numero del grupo asignado en la petición. Esta petición retornará una porción aleatoria de los datos del batch actual. A partir de ese momento y durante los 5 minutos siguientes a la petición, se entregará información una porción aleatoria de el batch de información actual, después de esos 5 minutos se cambiaré el batch y se repetirá la condición de los 5 minutos nuevamente. Tenga en cuenta que para lograr

Si desea reiniciar la recolección de información la API tiene un metodo para reiniciar el batch actual.

Recuerde que aunque puede usar este código para hacer pruebas, la entrega debe hacerse usando la API desplegada por el profesor.

### Aclaración

La API tiene un tiempo de respuesta suficiente para no causar inconvenientes, sin embargo si está usando la API desde la documentación autogenerada (`/docs`) el timepo de renderizado de los datos en la interfaz grafica puede bloquear el navegador temporalmente, si desea revisar los datos desde ahí puede hacerlo, solo debe esperar y permitir al navegador esperar la respuesta, una vez cargue funcionará con normalidad.