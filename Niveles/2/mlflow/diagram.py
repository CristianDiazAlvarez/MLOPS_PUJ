from diagrams import Cluster, Diagram, Edge
from diagrams.onprem.compute import Server
from diagrams.onprem.network import Internet
from diagrams.custom import Custom

from diagrams.onprem.database import Mysql
from diagrams.onprem.mlops import Mlflow

graph_attr = {
    "layout":"dot",
    "compound":"true",
    "size":"10",
    "pad":"0"
    }



with Diagram(name="MLflow Class explanation", show=False, direction="TB", graph_attr=graph_attr):

    with Cluster("MLOps VM",direction="TB"):

        with Cluster("docker-compose", graph_attr={"bgcolor":"#D8D8D8"}):
            cc_minio = Custom("object store", "./images/MINIO_wordmark.png")

        with Cluster("systemd_service", direction='LR', graph_attr={"bgcolor":"#F3E2A9"}):
            with Cluster("server", graph_attr={"bgcolor":"#F3E2A9"}):
                mlflow_tracking = Mlflow("Tracking")
            with Cluster("server ", graph_attr={"bgcolor":"#F3E2A9"}):
                mlflow_model_registry = Mlflow("Model Registry")
            
            

            with Cluster("File", graph_attr={"bgcolor":"#FA8258"}):
                cc_sqlite = Custom("ML_metadata", "./images/SQLite.png")

        

        with Cluster("from dockerfile", graph_attr={"bgcolor":"#81F7BE"}):
            cc_jupyter = Custom("Notebooks", "./images/jupyter.png")

    with Cluster("Internet", direction="LR", graph_attr={"bgcolor":"#E6E0F8"}):
        with Cluster("mlops-vm-ip:5000", graph_attr={"bgcolor":"#E6E1E8"}):
            i_mlflow = Internet("MLflow")
        #with Cluster(":5000", graph_attr={"bgcolor":"#E6E1E8"}):
            #i_mysql = Internet("Mysql")
        with Cluster("mlops-vm-ip:9000", graph_attr={"bgcolor":"#E6E1E8"}):
            i_cc_minio = Internet("minio")
        with Cluster("mlops-vm-ip:8888", graph_attr={"bgcolor":"#E6E1E8"}):
            i_jupyter = Internet("JupyterLab")


    ## VM Connections
    mlflow_tracking << Edge(color="black", minlen="2", constraint="False", ltail="cluster_server", lhead="cluster_server ") >> mlflow_model_registry
    mlflow_tracking << Edge(color="black", minlen="2", constraint="False") >> cc_sqlite


    ## Connections from VM to internet
    i_cc_minio << Edge(color="black", minlen="2", ltail="cluster_mlops-vm-ip:9000", lhead="cluster_docker-compose") >> cc_minio
    i_mlflow << Edge(color="black", minlen="2", ltail="cluster_mlops-vm-ip:5000", lhead="cluster_server ") >> mlflow_model_registry
    i_mlflow << Edge(color="black", minlen="2", constraint="False", ltail="cluster_mlops-vm-ip:5000", lhead="cluster_server") >> mlflow_tracking
    i_jupyter << Edge(color="black", minlen="2", constraint="False", ltail="cluster_mlops-vm-ip:8888", lhead="cluster_from dockerfile") >> cc_jupyter

    ## Internet conections
    i_cc_minio << Edge(color="black", minlen="2", constraint="False", ltail="cluster_mlops-vm-ip:9000", lhead="cluster_mlops-vm-ip:5000") >> i_mlflow
    i_jupyter << Edge(color="black", minlen="2", constraint="False", ltail="cluster_mlops-vm-ip:8888", lhead="cluster_mlops-vm-ip:5000") >> i_mlflow
    

    