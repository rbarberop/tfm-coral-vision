# Generacion de CSV para Google Cloud AutoML
# 
# Roberto Barbero - TFM
#
# Parametros: bucket_origen 
#
# bucket_origen - nombre del bucket donde se encuentran las imagenes 
#
# Para el correcto funcionamiento, el usuario debe estar autenticado con Google Cloud
# y las APIs de Storage activa

import sys
from google.cloud import storage

def genera_csv(bucket_origen):

    # Inicializacion de elementos Google Cloud
    storage_client = storage.Client()

    # Inicializacion de fichero local
    f = open("./automl.csv", "w")

    source_bucket = storage_client.get_bucket(bucket_origen)
    blob_csv = source_bucket.blob("automl.csv")

    # Array con todas las imagenes a clasificar
    blobs = storage_client.list_blobs(bucket_origen)

    for blob in blobs:
        # Por cada imagen, se genera una linea en el CSV
        if (blob.name.endswith(".jpg") or blob.name.endswith(".JPG") or blob.name.endswith(".jpeg") or blob.name.endswith(".JPEG")):

            print(blob.name)
            categoria = blob.name.split("/")[0]

            f.write(",gs://" + bucket_origen + "/" + blob.name + "," + categoria.upper() + "\n")

    # Copiamos el CSV generado al bucket en Google Cloud
    blob_csv.upload_from_filename("./automl.csv")

            
if __name__ == "__main__":
    genera_csv(bucket_origen=sys.argv[1])