from functools import wraps
from flask import Flask, request, jsonify
import json 

api = Flask(__name__)

# Base de datos en memoria para almacenar peers y sus archivos
peers = []

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        username = request.headers.get('username')
        if username not in peers:
            return jsonify({'message': 'You must be logged in!'}), 401
        return f(*args, **kwargs)
    return decorated

@api.route('/verifyLogin', methods=['POST'])
@login_required
def verifyLogin():
    username = request.headers.get('username')
    if username in peers:
        response = jsonify({'message':'Access granted!'}),200
    else:
        response = jsonify({'message':'You must be logged in'}),401
    return response

# Endpoint para que un peer haga login
@api.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password= data.get('password')

    if username and password:
        if username in peers:
            response = jsonify({"message": f"User {username} already logged."}), 200
        else:    
            response = jsonify({"message": f"User {username} logged in."}), 200
            peers.append(username)
            print(peers)
    else:
        response = jsonify({"message": f"No ingresó alguno de los datos"}), 402
    return response

# Endpoint para que un peer haga logout
@api.route('/logout', methods=['POST'])
@login_required
def logout():
    data = request.get_json()
    username = data.get('username')

    if username:
        if username in peers:
            peers.pop(peers.index(username))
            print(peers)
            response = jsonify({"message": f"User {username} logged out."}), 200
        else:    
            response = jsonify({"message": f"User {username} in not logged in."}), 200
            print(peers)
    else:
        response = jsonify({"message": f"No ingresó alguno de los datos"}), 402
    return response

# Endpoint para que un peer indexe sus archivos
# AGREGAR CONTROL DE ERRORES EN CASO DE NO SUBIR UN JSON
@api.route('/index', methods=['POST'])
@login_required
def index_files():
    data = request.get_json()
    peer_name = list(data.keys())[0]
    peer_info = data[peer_name]

    # Verificar si se enviaron los campos necesarios
    if 'files' not in peer_info or 'ip' not in peer_info or 'port' not in peer_info or 'folder' not in peer_info:
        return jsonify({"status": "error", "message": "Faltan datos necesarios"}), 400

    try:
        # Leer el archivo filesDB.json
        with open('API//filesDB.json', 'r') as file:
            files_db = json.load(file)
    except FileNotFoundError:
        files_db = {}

    # Actualizar el contenido con los datos recibidos
    files_db[peer_name] = {
        "files": peer_info['files'],
        "ip": peer_info['ip'],
        "port": peer_info['port'],
        "folder": peer_info['folder']
    }

    # Guardar los cambios en filesDB.json
    with open('Api//filesDB.json', 'w') as file:
        json.dump(files_db, file, indent=4)

    return jsonify({"status": "success"}), 200


# Endpoint para que un peer busque un archivo
@api.route('/search', methods=['GET'])
@login_required
def search():
    file_name = request.args.get('file')
    
    if not file_name:
        return jsonify({"error": "El nombre del archivo es necesario."}), 400

    # Leer el archivo filesDB.json
    try:
        with open('API//filesDB.json', 'r') as file:
            files_db = json.load(file)
    
    except FileNotFoundError:
        return jsonify({"error": "El archivo filesDB.json no se encuentra."}), 404
    
    except json.JSONDecodeError:
        return jsonify({"error": "Error al decodificar el archivo filesDB.json."}), 400

    # Buscar el archivo en filesDB.json y obtener información adicional
    peers_with_file = []
    for peer, data in files_db.items():
        if file_name in data.get('files', []):
            # Incluir el IP, puerto y carpeta del peer en la respuesta
            peer_info = {
                "peer": peer,
                "ip": data.get('ip', 'No IP'),
                "port": data.get('port', 'No Port'),
                "folder": data.get('folder', 'No Folder')
            }
            peers_with_file.append(peer_info)

    # Si se encuentran peers con el archivo, devolver la información
    if peers_with_file:
        return jsonify({"peers_with_file": peers_with_file}), 200

    return jsonify({"message": "Archivo no encontrado en los peers."}), 404


if __name__ == '__main__':
    api.run(debug=True, host='0.0.0.0', port=6970)

