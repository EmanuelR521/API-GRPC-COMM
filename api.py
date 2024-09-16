from flask import Flask, request, jsonify
import json 

api = Flask(__name__)

# Base de datos en memoria para almacenar peers y sus archivos
peers = []

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
            response = jsonify({"message": f"User {username} registrado con éxito."}), 200
            peers.append(username)
            print(peers)
    else:
        response = jsonify({"message": f"No ingresó alguno de los datos"}), 402
    return response

@api.route('/logout', methods=['POST'])
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
@api.route('/index', methods=['POST'])
def index_files():
    data = request.get_json()
    with open('filesDB.json', 'r') as file:
        files_db = json.load(file)

        # Actualizar el contenido con los datos recibidos
    files_db.update(data)

        # Guardar los cambios en filesDB.json
    with open('filesDB.json', 'w') as file:
        json.dump(files_db, file, indent=4)

        return jsonify({"status": "success"}), 200
    response = data
    return response


@api.route('/search', methods=['GET'])
def search():
    file_name = request.args.get('file')
    
    if not file_name:
        return jsonify({"error": "El nombre del archivo es necesario."}), 400

    # Leer el archivo filesDB.json
    try:
        with open('filesDB.json', 'r') as file:
            files_db = json.load(file)
    except FileNotFoundError:
        return jsonify({"error": "El archivo filesDB.json no se encuentra."}), 404
    except json.JSONDecodeError:
        return jsonify({"error": "Error al decodificar el archivo filesDB.json."}), 400

    # Buscar el archivo en filesDB.json
    peers_with_file = [peer for peer, data in files_db.items() if file_name in data.get('files', [])]
    if peers_with_file[0] == "peer1":
        with open('filesDB.json', 'r') as file:
            files_db = json.load(file)
            
    if peers_with_file:
        return jsonify({"peers_with_file": peers_with_file}), 200
    return jsonify({"message": "Archivo no encontrado en los peers."}), 404

if __name__ == '__main__':
    api.run(debug=True, host='0.0.0.0', port=6970)

