import requests
import json
import os
import grpc
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'GRPC')))

import FileSharing_pb2, FileSharing_pb2_grpc

class Peer4:
    def __init__(self, base_url):
        self.base_url = base_url
        self.last_result = None  # Variable para almacenar el último resultado
        print(self.base_url)

    def login(self, username, password):
        url = f"{self.base_url}/login"
        data = {"username": username, "password": password}
        response = requests.post(url, json=data)
        self.last_result = response.json()  # Guardar el resultado en una variable
        return self.last_result

    def logout(self):
        url = f"{self.base_url}/logout"
        data = {"username": "peer4"}
        response = requests.post(url, json=data)
        self.last_result = response.json()  # Guardar el resultado
        return self.last_result

    def search(self, file_name):
        url = f"{self.base_url}/search"
        params = {"file": file_name}
        response = requests.get(url, params=params)
        self.last_result = response.json()  # Guardar el resultado
        return self.last_result

    def index(self):
        url = f"{self.base_url}/index"
        try:
            path = os.path.abspath("peer_4//config.json")
            with open(path, 'r') as file:
                data = json.load(file)
                files = data.get('files', [])
                ip = data.get('ip', '')
                port = data.get('port', '')
                folder = data.get('folder', '')
                print(f"Archivos encontrados en config.json: {files}")
        except FileNotFoundError:
            print("El archivo config.json no se encuentra.")
            return None
        except json.JSONDecodeError:
            print("Error al decodificar el archivo config.json.")
            return None

        # Enviar los archivos junto con la IP, el puerto y la carpeta a la API
        peer_data = {
            'peer4': {
                'files': files,
                'ip': ip,
                'port': port,
                'folder': folder
            }
        }

        response = requests.post(url, json=peer_data)
        self.last_result = response.json()  # Guardar el resultado
        return self.last_result

    def download(self, peer_ip,peer_port, file_name):
        # Crear un canal gRPC hacia el otro peer
        channel = grpc.insecure_channel(f'{peer_ip}:{peer_port}')
        stub = FileSharing_pb2_grpc.FileServiceStub(channel)

        # Crear una solicitud para descargar el archivo
        request = FileSharing_pb2.FileRequest(file_name=file_name)

        # Realizar la llamada al servidor gRPC del otro peer
        try:
            response = stub.DownloadFile(request)
            print(f"Nombre del archivo recibido: {response.file_content}")
        except grpc.RpcError as e:
            print(f"Error al descargar el archivo: {e}")

def main_menu(peer):
    while True:
        print("\n--- Menú de Peer4 ---")
        print("1. Login")
        print("2. Logout")
        print("3. Indexar Archivos")
        print("4. Buscar Archivos")
        print("5. Descargar Archivo")
        print("6. Ver último resultado")
        print("7. Salir")

        choice = input("Selecciona una opción: ")

        if choice == '1':
            username = input("Ingrese el nombre de usuario: ")
            password = input("Ingrese la contraseña: ")
            result = peer.login(username, password)
            print(f"Resultado del login: {result}")

        elif choice == '2':
            result = peer.logout()
            print(f"Resultado del logout: {result}")

        elif choice == '3':
            result = peer.index()
            print(f"Resultado de la indexación: {result}")

        elif choice == '4':
            file_name = input("Ingrese el nombre del archivo a buscar: ")
            result = peer.search(file_name)
            print(f"Resultado de la búsqueda: {result}")

        elif choice == '5':
            file_name = input("Ingrese el nombre del archivo a descargar: ")
            peers = peer.search(file_name)
            if 'peers_with_file' in peers:
                for p in peers['peers_with_file']:
                    peer_ip = p[0]['ip']
                    peer.download(peer_ip, file_name)
            else:
                print("No se encontraron peers con el archivo.")

        elif choice == '6':
            if peer.last_result:
                print(f"Último resultado: {peer.last_result}")
            else:
                print("No se ha ejecutado ninguna operación aún.")

        elif choice == '7':
            print("Saliendo del programa...")
            break

        else:
            print("Opción no válida. Por favor, intente de nuevo.")

if __name__ == '__main__':
    base_url = 'http://127.0.0.1:6970'
    peer = Peer4(base_url)
    main_menu(peer)

