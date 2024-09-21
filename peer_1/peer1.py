
import sys,os,json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'GRPC')))
import requests,json,grpc,FileSharing_pb2,FileSharing_pb2_grpc
class Peer1:
    username = ""
    peerConfig = json
    peersWithFile = []
    def __init__(self, api_url):
        with open('peer_1//config.json', 'r') as file:
            data = json.load(file)
        
        self.peerConfig = data
        self.api_url = api_url
        self.last_result = None
          # Variable para almacenar el último resultado
        print(self.api_url)


    def login(self, username, password):
        url = f"{self.api_url}/login"
        self.username = username
        if self.peerConfig['username'] == username:
            data = {"username": username, "password": password}
            response = requests.post(url, json=data, headers={'username': username})
            self.last_result = response.json()  # Guardar el resultado en una variable
            return self.last_result
#        if response.status_code == 200:
        else: 
            return 'Wrong user!'

        

    def logout(self):
        url = f"{self.api_url}/logout"
        data = {"username": self.username}
        response = requests.post(url, json=data, headers={'username': self.username})
        self.last_result = response.json()  # Guardar el resultado
        return self.last_result

    def search(self, file_name):
        self.peersWithFile = []
        url = f"{self.api_url}/search"
        params = {"file": file_name}
        response = requests.get(url, params=params, headers={'username': self.username})
        self.last_result = response.json()
        for peer in self.last_result['peers_with_file']:
            self.peersWithFile.append(peer['peer'])
        print(self.peersWithFile)  # Guardar el resultado
        return self.last_result  # Guardar el resultado
       
    
    def index(self):
        url = f"{self.api_url}/index"
        try:
            with open('peer_1//config.json', 'r') as file:
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
            'peer1': {
                'files': files,
                'ip': ip,
                'port': port,
                'folder': folder
            }
        }

        response = requests.post(url, json=peer_data, headers={'username': self.username})
        self.last_result = response.json()  # Guardar el resultado
        return self.last_result

    def download(self, peer_ip,peer_port, file_name):
        if file_name in self.peerConfig['files']:
            print(f"El archivo {file_name} ya se encuentra en el peer")
            return -1
        url=f"{self.api_url}/verifyLogin"
        response = requests.post(url,headers={'username':self.username})
        if response.status_code  != 200:
            return 'You must be logged in'
        # Crear un canal gRPC hacia el otro peer
        channel = grpc.insecure_channel(f'{peer_ip}:{peer_port}')
        stub = FileSharing_pb2_grpc.FileServiceStub(channel)

        # Crear una solicitud para descargar el archivo
        request = FileSharing_pb2.FileRequest(file_name=file_name)

        # Realizar la llamada al servidor gRPC del otro peer
        try:
            response = stub.DownloadFile(request)
            if response:
                with open('peer_1//config.json', 'w') as file:
                    self.peerConfig['files'].append(file_name)
                    json.dump(self.peerConfig, file, indent=4)
            print(f"Nombre del archivo recibido: {response.file_content}")
        except grpc.RpcError as e:
            print(f"Error al descargar el archivo: {e}")

def main_menu(peer):
    while True:
        print("\n--- Menú de Peer 1 ---")
        print("1. Login")
        print("2. Logout")
        print("3. Indexar Archivos")
        print("4. Buscar Archivos")
        print("5. Descargar Archivo")
        print("6. Ver último resultado")

        choice = input("Selecciona una opción: ")

        if choice == '1':
            username = input("Ingrese el nombre de usuario: ")
            password = input("Ingrese la contraseña: ")
            result = peer.login(username, password)
            print(f"Resultado del login: {result}")

        elif choice == '2':
            result = peer.logout()
            print(f"Resultado del logout: {result}")
            print("Saliendo del programa...")
            break

        elif choice == '3':
            result = peer.index()
            print(f"Resultado de la indexación: {result}")

        elif choice == '4':
            file_name = input("Ingrese el nombre del archivo a buscar: ")
            result = peer.search(file_name)


        elif choice == '5':
            file_name = input("Ingrese el nombre del archivo a descargar: ")
            peers = peer.search(file_name)
            if 'peers_with_file' in peers:
                peersD = peers['peers_with_file']
                peerToDownload = peersD[0]              
                peer_ip = peerToDownload['ip']
                peer_port = peerToDownload['port']
                response = peer.download(peer_ip,peer_port, file_name)
                if response == -1:
                    break
                print(f"archivo descargado desde {peerToDownload['peer']}")
            else:
                print("No se encontraron peers con el archivo.")

        elif choice == '6':
            if peer.last_result:
                print(f"Último resultado: {peer.last_result}")
            else:
                print("No se ha ejecutado ninguna operación aún.")

        else:
            print("Opción no válida. Por favor, intente de nuevo.")


if __name__ == '__main__':
    api_url = 'http://127.0.0.1:6970'
    peer = Peer1(api_url)
    main_menu(peer)
