#   API-GRPC-COMMS
Solución con API Rest y gRPC para una red P2P server-based

#   Sistema P2P para Compartición de Archivos
Este proyecto implementa un sistema distribuido peer-to-peer (P2P) para la compartición de archivos, utilizando Flask para la API REST y gRPC para la comunicación entre peers. El sistema permite que los peers se comuniquen y compartan archivos.

## Características
-   API REST para la gestión de archivos.
-   Comunicación gRPC entre peers.
-   Registro de peers y archivos en un servidor de Directorio y Localización.
-   Compatibilidad con múltiples peers, cada uno con su configuración independiente.

##  Arquitectura del Sistema
El sistema está diseñado bajo una arquitectura descentralizada, donde cada peer puede actuar como cliente y servidor simultáneamente. La interacción entre los peers ocurre a través de:

**API REST:** Se implementa para registrar archivos en el servidor de Directorio y Localización.

**gRPC:** se implementa para la transferencia de archivos entre peers.


## Requisitos
Antes de comenzar, asegúrate de tener lo siguiente instalado en su maquina:
-   Python 3.12
-   Flask
-   gRPC
-   requests
-   Protobuf

## Instalación y ejecución del proyecto
1.  Clonar repositorio:
```bash
   git clone https://github.com/EmanuelR521/API-GRPC-COMM.git
   ```
2. Instalar los requisitos.
3. Configura los archivos config.json para cada peer, donde debes especificar el nombre del usuario, la IP, el puerto, y los archivos disponibles.
4. Ejecuta la API central:
```bash
   python api.py
   ```
5. Ejecutar los peers (reemplace el # por el digito del peer que quiera ejecutar (1,2,3 ó 4)):
```bash
   python peer#.py
   ```

## Configuración del peer
Cada peer tiene su propio archivo de configuración config.json. A continuación se explica cada parámetro:
```bash
   config.json
{
    "username": "peer1",
    "status": "off",
    "files": [
        "file1.txt"
    ],
    "ip": "127.0.0.1",
    "port": "50001",
    "folder": "myFiles"
}
   ```

- **username:** Nombre único del peer.
- **status:** Estado del peer (puede ser on u off).
- **files:** Lista de archivos que el peer comparte.
- **ip:** Dirección IP en la que el peer escucha las solicitudes.
- **port:** Puerto donde el peer estará disponible para la comunicación.
- **folder:** Carpeta local donde se almacenan los archivos compartidos por el peer.

## Archivo.proto (FileSharing.proto)
El archivo .proto define el servicio de descarga de archivos entre los peers utilizando gRPC. El servicio expone un método DownloadFile que recibe una solicitud con el nombre del archivo y responde con el contenido del archivo.
proto

```bash
syntax = "proto3";

service FileService {
  rpc DownloadFile (FileRequest) returns (FileResponse);
}

message FileRequest {
  string file_name = 1;
}

message FileResponse {
  string file_content = 1;
}

   ```

##  Uso de gRPC
La implementación de gRPC permite que los peers soliciten archivos entre sí de manera eficiente. El archivo .proto especifica las reglas de esta comunicación.

##  Funciones del API
1. **POST /login**

    Permite que un peer inicie sesión en el sistema. El peer debe enviar su nombre de usuario y contraseña. Si el usuario ya está registrado, se le permitirá realizar otras operaciones.

    **Parámetros:** username, password

    **Respuesta:** Mensaje de éxito o error en la autenticación.

2. **POST /logout**

    Permite a un peer cerrar su sesión y eliminar su registro de la red.

    **Parámetros:** username.

    **Respuesta:** Mensaje confirmando el cierre de sesión.

3. **POST /index**

    Permite que un peer registre (indexe) sus archivos en la red, incluyendo la IP, el puerto y la carpeta donde se encuentran.

    **Parámetros:** JSON con información del peer (files, ip, port, folder).

    **Respuesta:** Mensaje de éxito si la operación es correcta.

4. **GET /search**

    Permite a un peer buscar un archivo en la red. El sistema devolverá una lista de peers que tienen el archivo disponible junto con su IP, puerto y carpeta.

    **Parámetros:** file (nombre del archivo a buscar).

    **Respuesta:** Lista de peers con el archivo o un mensaje de que no se encontró.

5. **POST /verifyLogin**

    Verifica si un peer está autenticado para poder realizar operaciones.

    **Respuesta:** Mensaje de confirmación de acceso.

##  Funciones de los Peers
1. **login**

    Permite a un peer iniciar sesión en la red, enviando su nombre de usuario y contraseña al API central. Si el login es exitoso, el peer puede realizar otras operaciones.

    **Parámetros:** username, password

    **Respuesta:** Mensaje de éxito o error.

2. **logout**

    Permite a un peer desconectarse de la red y eliminar su registro.

    **Parámetros:** Ninguno, pero utiliza el nombre de usuario guardado en la sesión actual.

    **Respuesta:** Confirmación de logout.

3. **search**

    Permite a un peer buscar un archivo en la red utilizando el API. Si el archivo es encontrado, muestra los peers que lo poseen.

    **Parámetros:** file_name (nombre del archivo a buscar).

    **Respuesta:** Lista de peers que poseen el archivo.

4. **index**

    Permite a un peer indexar sus archivos, es decir, informar al sistema central sobre qué archivos tiene disponibles, su IP, puerto, y la carpeta donde se encuentran.
S
    **Parámetros:** JSON con los archivos y la información de red del peer.

    **Respuesta:** Confirmación de indexación.

5. **download**

    Permite a un peer descargar un archivo desde otro peer utilizando gRPC. Se establece una conexión entre los peers y se recibe el archivo solicitado.

    **Parámetros:** peer_ip, peer_port, file_name (IP y puerto del peer con el archivo y el nombre del archivo).

    **Respuesta:** El archivo descargado o un mensaje de error si falla la descarga.

##  Ejecución
1.  Inicia la API central para que gestione el registro y la búsqueda de archivos.

2.  Cada peer se conectará a la API para autenticar, indexar sus archivos y buscar o descargar archivos de otros peers.

### Flujo de Operación:
Un peer se autentica mediante el API central.
Luego, puede indexar sus archivos en la red.
Si necesita un archivo que no posee, puede buscarlo entre los peers registrados.
Finalmente, puede descargar el archivo desde otro peer utilizando gRPC.