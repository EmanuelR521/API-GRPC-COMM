# Librerias a importar
import argparse
import requests
import json
import os

# Variable global
username = 'peer3'

class Peer3:
    def __init__(self, base_url):
        self.base_url = base_url
        print(self.base_url)

    def login(self, username, password):
        url = f"{self.base_url}/login"
        data = {"username": username, "password": password}
        response = requests.post(url, json=data) # Falta modificar el status del peer en el arc config.json
        return response.json()

    def logout(self):
        url = f"{self.base_url}/logout"
        data = {"username":"peer3"}
        response = requests.post(url,json=data)
        return response.json()

    def search(self, file_name):
        url = f"{self.base_url}/search"
        params = {"file": file_name}  # Usar 'file' como clave en los parámetros
        response = requests.get(url, params=params)
        return response.json()
    
    def index(self):
        url = f"{self.base_url}/index"
        try:
            
            path = os.path.abspath("peer_3//config.json")
            with open(path, 'r') as file:
                data = json.load(file)
                # Extraer la lista de archivos del campo 'files'
                files = data.get('files', [])
                print(files)
        
        except FileNotFoundError:
            print("El archivo config.json no se encuentra.")
            return None
        
        except json.JSONDecodeError:
            print("Error al decodificar el archivo config.json.")
            return None
        
        #files = arc.get('files',[])
        # Enviar los archivos a la API
        response = requests.post(url, json={'peer3': {'files':files}})
        return response.json()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Command line client for peer3 API operations')
    parser.add_argument('operation', help='Operation to perform', choices=['login', 'logout', 'search', 'index'])
    parser.add_argument('--username', help='Username for login')
    parser.add_argument('--password', help='Password for login')
    parser.add_argument('--file_name', help='Search file')
    parser.add_argument('--base_url', default='http://127.0.0.1:6970', help='Base URL of the API')

    args = parser.parse_args()

    peer = Peer3(args.base_url)
    print(peer.base_url)
    
    if args.operation == 'login':
        if not all([args.username, args.password]):
            print("Username and password are required for login")
        else:
            print(peer.login(args.username, args.password))
            
    elif args.operation == 'logout':
        print(peer.logout())
        
    elif args.operation == 'search':
        if not args.file_name:
            print("File name is required for search")
        else:
            print(peer.search(args.file_name))
            
    elif args.operation == 'index':
        print(peer.index())    