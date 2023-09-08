# Clasificacion de imagenes utilizando Google Cloud Vision API
# 
# Roberto Barbero - TFM
#
# Parametros: bucket_origen bucket_destino
#
# bucket_origen - nombre del bucket donde se encuentran las imagenes a clasificar
# bucket_destino - nombre del bucket donde se copiaran las imagenes clasificadas
# (las imagenes se copiaran en los directorios /person /net o /negative del bucket_destino)
#
# Para el correcto funcionamiento, el usuario debe estar autenticado con Google Cloud
# y las APIs de Storage y Cloud Vision activas

import sys
from google.cloud import storage
from google.cloud import vision

def clasifica_imagenes(bucket_origen, bucket_destino):

    # Etiquetas indicativas de cada clase
    labels_persona = ["Person", "Underwater diving", "Scuba diving" , "Divemaster", "Diving equipment", "Diving regulator", "Diving mask"]
    labels_red = ["Fishing net", "Net", "Boat", "Fishing boat", "Diver boat", "Anchor", "Pattern"]

    # Inicializacion de elementos Google Cloud
    storage_client = storage.Client()
    vision_client = vision.ImageAnnotatorClient()

    source_bucket = storage_client.get_bucket(bucket_origen)
    destination_bucket = storage_client.get_bucket(bucket_destino)

    # Array con todas las imagenes a clasificar
    blobs = storage_client.list_blobs(bucket_origen)

    for blob in blobs:
        # Por cada imagen, se hace llamada a Cloud Vision API y se capturan las etiquetas
        if (blob.name.endswith(".jpg") or blob.name.endswith(".JPG") or blob.name.endswith(".jpeg") or blob.name.endswith(".JPEG")):
            image = vision.Image()
            image.source.image_uri = "gs://" + bucket_origen + "/" + blob.name
            print(image.source.image_uri)
            response = vision_client.label_detection(image = image)
            labels = response.label_annotations

            etiquetada = False

            # Por cada etiqueta, se comprueba si existe en las etiquetas de cada clase, y se copia la imagen al destino correspondiente
            for label in labels:
                if label.description in labels_persona:
                    print ("Persona detectada")
                    etiquetada = True
                    source_bucket.copy_blob(blob, destination_bucket, "person/"+ blob.name)
                    break
                elif label.description in labels_red:
                    print ("Red detectada")
                    etiquetada = True
                    source_bucket.copy_blob(blob, destination_bucket, "net/"+ blob.name)
                    break

            if not etiquetada:
                print ("Persona o Red no detectadas")
                source_bucket.copy_blob(blob, destination_bucket, "negative/"+ blob.name)


if __name__ == "__main__":
    clasifica_imagenes(bucket_origen=sys.argv[1], bucket_destino=sys.argv[2])