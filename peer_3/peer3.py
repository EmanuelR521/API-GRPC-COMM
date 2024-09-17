import requests
import json
import os

class Peer3:
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
        data = {"username": "peer3"}
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
            path = os.path.abspath("peer_3//config.json")
            with open(path, 'r') as file:
                data = json.load(file)
                files = data.get('files', [])
                print(f"Archivos encontrados en config.json: {files}")
        except FileNotFoundError:
            print("El archivo config.json no se encuentra.")
            return None
        except json.JSONDecodeError:
            print("Error al decodificar el archivo config.json.")
            return None

        response = requests.post(url, json={'peer3': {'files': files}})
        self.last_result = response.json()  # Guardar el resultado
        return self.last_result


def main_menu(peer):
    while True:
        print("\n--- Menú de Peer3 ---")
        print("1. Login")
        print("2. Logout")
        print("3. Indexar Archivos")
        print("4. Buscar Archivos")
        print("5. Ver último resultado")
        print("6. Salir")

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
            if peer.last_result:
                print(f"Último resultado: {peer.last_result}")
            else:
                print("No se ha ejecutado ninguna operación aún.")

        elif choice == '6':
            print("Saliendo del programa...")
            break

        else:
            print("Opción no válida. Por favor, intente de nuevo.")


if __name__ == '__main__':
    base_url = 'http://127.0.0.1:6970'
    peer = Peer3(base_url)
    main_menu(peer)
