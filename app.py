from flask import Flask, request, jsonify, render_template
from google.cloud import storage
import os
from time import sleep
import json
from google.oauth2 import service_account

app = Flask(__name__)

# Cargar las credenciales desde la variable de entorno
credentials_json = os.getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON")
if not credentials_json:
     raise Exception("Las credenciales no están configuradas en las variables de entorno")

credentials_dict = json.loads(credentials_json)
credentials = service_account.Credentials.from_service_account_info(credentials_dict)

# Usar el cliente de Google Cloud
from google.cloud import storage
storage_client = storage.Client(credentials=credentials)

# # Credenciales de Google Cloud, deben estar en la raíz del proyecto (SOLAMENTE LOCAL) - Comentar para Deployment
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "service-account-key.json"

BUCKET_NAME = "pruebas_ale"
# En caso de algún cambio: Reemplazar con el nombre del bucket de GCS  

# Carga la interfaz web
@app.route('/')
def index():
    return render_template('index.html')

# Backend para subir archivos a GCS
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No se encontró el archivo", 400

    file = request.files['file']
    if file.filename == '':
        return "El nombre del archivo está vacío", 400

    # Conecta con Google Cloud Storage
    storage_client = storage.Client()
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(file.filename)

    # Subir el archivo al bucket
    
    # Barra de progreso
    with blob.open("wb") as f:
        chunk_size = 1024 * 1024  # 1 MB por chunk
        file_stream = file.stream

        while chunk := file_stream.read(chunk_size):
            f.write(chunk)
            
    # Confirmación de subida
    return f"Archivo '{file.filename}' subido exitosamente", 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
