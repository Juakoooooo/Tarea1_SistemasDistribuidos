<h1 align="left"> Configuración Tarea 1 Sistemas Distribuidos </h1>

Para comenzar a ejecutar el proyecto, es necesario utilizar **Python**, y **Docker** junto con el plugin **Docker Compose**, para su instalación es posible hacerlo desde la documentación oficial de [Docker](https://docs.docker.com/desktop/install/linux/ubuntu/).

> [!NOTE]
> Si ya estaba instalado **Docker** previamente, se puede omitir el paso anterior.

Luego de instalar **Docker** y se debe importar el dataset que contiene los dominios con los que se trabajará. El link proviene desde Kaggle, pulse [aquí](https://www.kaggle.com/datasets/domainsindex/secondlevel-domains-listzone-file) para redirigirse al sitio web y descargar el dataset llamado ``"3rd_lev_domains.csv"``. 

> [!IMPORTANT]
> Para que los códigos operen de manera correcta, el nombre del archivo del dataset es modificado a  ``"dataset.csv"`` y se debe posicionar en la carpeta ``traffic-generator`` dentro de la carpeta raíz.

Ya con el dataset ubicado en su carpeta correspondiente, en el script que se encuentra en la carpeta raíz llamado ``"init-redis.sh"``, se le deben dar los permisos adecuados de ejecución para que las configuraciones dentro del script se apliquen de forma exitosa, esto se realiza con el siguiente comando:

```
sudo chmod +x init-redis.sh
```

A continuación de dar los permisos de ejecución al script, en la carpeta ``"grpc-server"`` se necesita generar los archivos ``"dns_resolver_pb2.py"`` y ``"dns_resolver_pb2_grpc.py"`` en base al archivo ``"dns_resolver.proto"`` ya que el servidor gRPC y la API los utilizan, estos códigos se generan con los siguientes comandos:

```
pip install grpcio grpcio-tools
python -m grpc_tools.protoc -I=. --python_out=. --grpc_python_out=. dns_resolver.proto
```

> [!IMPORTANT]
> Los códigos generados con el comando anterior, se deben copiar y pegar dentro de la carpeta ``"api"`` para obtener un funcionamiento correcto ya que la API también utiliza estos códigos.

Con estas configuraciones ya aplicadas, es posible levantar los contenedores mediante un **Compose**, para levantar y construir los contenedores del archivo ``"docker-compose.yml"`` se ejecuta el siguiente comando:

```
sudo docker-compose up --build
```

> [!TIP]
> Si no se desea ver en tiempo real el detalle de los contenedores, se le puede agregar el flag ``-d``

Para detener la ejecución de los contenedores, se ejecuta el siguiente comando:

```
sudo docker-compose stop
```

Para volver a comenzar con la ejecución manteniendo la permanencia de los datos, se ejecuta el siguiente comando:

```
sudo docker-compose start
```

Si se quiere detener la ejecución y eliminar los contenedores sin mantener la permanencia en los datos, se ejecuta el siguiente comando:

```
sudo docker-compose down --volumes
```

> [!WARNING]
> Si quedan contenedores que se consideren huérfanos (indicado por la misma terminal), agregar el flag ``--remove-orphans``, de lo contrario, se podrían generar errores en la construcción de los contenedores.
