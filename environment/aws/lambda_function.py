import boto3
import json
import base64
import urllib.request
import urllib.error


# Configuración
DATABRICKS_HOST = "dbc-1207e041-2bad.cloud.databricks.com"
DATABRICKS_TOKEN = "[TOKEN]"
TARGET_PATH = "/Users/manuelalensanchez7@gmail.com/"  # Ruta destino en Workspace


s3 = boto3.client('s3')


def lambda_handler(event, context):
    # 1. Obtener bucket y nombre del archivo
    bucket = event['Records'][0]['s3']['bucket']['name']
    key    = event['Records'][0]['s3']['object']['key']
   
    local_file = f"/tmp/{key.split('/')[-1]}"
    s3.download_file(bucket, key, local_file)
   
    # 2. Leer contenido y codificar en base64
    with open(local_file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")
   
    # 3. Subir al Workspace de Databricks
    payload = {
        "path": f"{TARGET_PATH}{key}",
        "format": "AUTO",
        "language": "PYTHON",  # o "TEXT" si es .csv
        "overwrite": True,
        "content": encoded
    }


    req = urllib.request.Request(
        url=f"https://{DATABRICKS_HOST}/api/2.0/workspace/import",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {DATABRICKS_TOKEN}",
            "Content-Type": "application/json"
        },
        method="POST"
    )


    try:
        with urllib.request.urlopen(req) as res:
            print("✅ Archivo subido a Workspace")
    except urllib.error.HTTPError as e:
        print(f"❌ Error al subir archivo: {e.code} - {e.reason}")
        print(e.read().decode())
        raise


    # 4. Lanzar pipeline por nombre
    launch_pipeline("pl_starwars_2_dt")


    return {
        "status": "ok",
        "message": f"Archivo {key} subido y pipeline lanzada"
    }




def launch_pipeline(name):
    # Obtener pipeline ID por nombre
    req_list = urllib.request.Request(
        url=f"https://{DATABRICKS_HOST}/api/2.0/pipelines",
        headers={"Authorization": f"Bearer {DATABRICKS_TOKEN}"}
    )
    with urllib.request.urlopen(req_list) as res:
        pipelines = json.loads(res.read())
        pipeline_id = next(p["pipeline_id"] for p in pipelines["statuses"] if p["name"] == name)


    # Lanzar actualización
    req_run = urllib.request.Request(
        url=f"https://{DATABRICKS_HOST}/api/2.0/pipelines/{pipeline_id}/updates",
        data=json.dumps({"full_refresh": False}).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {DATABRICKS_TOKEN}",
            "Content-Type": "application/json"
        },
        method="POST"
    )


    with urllib.request.urlopen(req_run) as res:
        print("🚀 Pipeline lanzada correctamente")
