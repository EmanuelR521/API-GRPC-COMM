sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'GRPC')))
import sys
import FileSharing_pb2, FileSharing_pb2_grpc
import grpc
from concurrent import futures
import time


class FileService(FileSharing_pb2_grpc.FileServiceServicer):
    def DownloadFile(self, request, context):
        # Simulación de la respuesta del nombre del archivo
        file_name = request.file_name
        # Retornar el nombre del archivo solicitado como cadena de texto
        return FileSharing_pb2.FileResponse(file_content=file_name)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    file_service = FileService()
    FileSharing_pb2_grpc.add_FileServiceServicer_to_server(file_service, server)
    server.add_insecure_port('[::]:50001')
    server.start()
    print("Servidor gRPC en ejecución en el puerto 50001.")
    try:
        while True:
            time.sleep(86400)  # Mantener el servidor en ejecución
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
