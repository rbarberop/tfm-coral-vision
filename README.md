# Vision artificial aplicada al estudio de arrecifes de coral

## Roberto Barbero - TFM 

Este repositorio contiene los programas auxiliares utilizados
durante el desarrollo del TFM.

El usuario debe tener conocimiento previo del uso de Google Cloud, 
especialmente para autenticación y uso de APIs

`cloudvision_clasificador.py` 
    
    utiliza Cloud Vision API para realizar una primera clasificación de las imágenes contenidas en un bucket GCS

`automl_generacsv.py` 
    
    genera un CSV para ser utilizado como entrada para AutoML, en base a las imágenes clasificadas por el script anterior

