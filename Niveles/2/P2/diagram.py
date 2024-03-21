from diagrams import Cluster, Diagram, Edge

# OnPrem components
from diagrams.onprem.compute import Server
from diagrams.onprem.network import Internet
from diagrams.onprem.container import Docker
from diagrams.onprem.client import Users
from diagrams.onprem.database import Mysql
from diagrams.onprem.workflow import Airflow
from diagrams.onprem.mlops import Mlflow
from diagrams.programming.framework import Fastapi

from diagrams.custom import Custom


graph_attr = {
    "layout":"dot",
    "compound":"true",
    "size":"10",
    "pad":"0"
    }



with Diagram(name="Project 2", direction='LR', show=False, graph_attr=graph_attr):

    with Cluster("MLOps VM", direction='LR'):

        with Cluster("docker-compose", direction='RL', graph_attr={"bgcolor":"#F3E2A9"}):
            
            with Cluster("minio", graph_attr={"bgcolor":"#D8D8D8"}):
                cc_minio = Custom("object store", "./images/MINIO_wordmark.png")
            with Cluster("inference", graph_attr={"bgcolor":"#D0E1E8"}):
                fastapi = Fastapi("AI model")
            with Cluster("mlflow", direction='TB', graph_attr={"bgcolor":"#F392A9"}):
                mlflow_model_registry = Mlflow("Model Registry")
                mlflow_tracking = Mlflow("Tracking")
            with Cluster("mysql", graph_attr={"bgcolor":"#FA8258"}):
                mysql = Mysql("ML_metadata")

            with Cluster("airflow", graph_attr={"bgcolor":"#AF8258"}):
                airflow = Airflow("Airflow system")

        

    with Cluster("Internet", direction="LR", graph_attr={"bgcolor":"#B6E0F8"}):
        with Cluster("10.43.101.149:80", graph_attr={"bgcolor":"#C6E1E8"}):
            i_fastapi = Fastapi("Data API")


    ## VM Connections
    
    cc_minio << Edge(color="blue", minlen="2", constraint="True", ltail="cluster_minio") >> mlflow_model_registry
    mlflow_model_registry << Edge(color="black", minlen="2", constraint="True", ltail="cluster_inference") >> fastapi
    mlflow_tracking << Edge(color="black", minlen="2", constraint="False", ltail="cluster_server", lhead="cluster_mlflow") >> mlflow_model_registry
    
    airflow << Edge(color="black", minlen="2", constraint="False", lhead="cluster_airflow") >> mlflow_model_registry
    airflow << Edge(color="black", minlen="2", constraint="False", ltail="cluster_airflow") >> mlflow_tracking

    mlflow_tracking << Edge(color="black", minlen="2", constraint="True", ltail="cluster_mysql") >> mysql
    


    ## Connections from VM to internet
    i_fastapi << Edge(color="black", minlen="2", ltail="cluster_10.43.101.149:80", lhead="cluster_airflow") >> airflow
    # i_mlflow << Edge(color="black", minlen="2", ltail="cluster_mlops-vm-ip:5000", lhead="cluster_server ") >> mlflow_model_registry
    # i_mlflow << Edge(color="black", minlen="2", constraint="False", ltail="cluster_mlops-vm-ip:5000", lhead="cluster_server") >> mlflow_tracking
    # i_jupyter << Edge(color="black", minlen="2", constraint="False", ltail="cluster_mlops-vm-ip:8888", lhead="cluster_from dockerfile") >> cc_jupyter

    ## Internet conections
    # i_cc_minio << Edge(color="black", minlen="2", constraint="False", ltail="cluster_mlops-vm-ip:9000", lhead="cluster_mlops-vm-ip:5000") >> i_mlflow
    # i_jupyter << Edge(color="black", minlen="2", constraint="False", ltail="cluster_mlops-vm-ip:8888", lhead="cluster_mlops-vm-ip:5000") >> i_mlflow
    

 