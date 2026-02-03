import grpc
from concurrent import futures
import os
import fits_pb2
import fits_pb2_grpc
from astropy.io import fits

# Ruta donde montaremos los datos en Docker
DATA_DIR = "/app/data"

class MetadataServicer(fits_pb2_grpc.MetadataServiceServicer):
    def GetFileMetadata(self, request, context):
        file_path = os.path.join(DATA_DIR, request.filename)
        
        if not os.path.exists(file_path):
            return fits_pb2.MetadataResponse(
                success=False, 
                message=f"File {request.filename} not found."
            )

        try:
            # Abrir el FITS con Astropy
            with fits.open(file_path) as hdul:
                headers_list = []
                # Leemos los metadatos del Header Primario (HDU 0)
                # En el futuro podríamos iterar sobre hdul para ver todas las extensiones
                primary_header = hdul[0].header
                
                for key, value in primary_header.items():
                    # Filtramos comentarios internos de FITS si es necesario
                    if key and not key.startswith('HISTORY') and not key.startswith('COMMENT'):
                        headers_list.append(
                            fits_pb2.HeaderEntry(
                                key=str(key),
                                value=str(value),
                                comment=primary_header.comments[key] if key in primary_header.comments else ""
                            )
                        )

            return fits_pb2.MetadataResponse(
                success=True,
                message="Metadata retrieved successfully",
                headers=headers_list
            )
            
        except Exception as e:
            return fits_pb2.MetadataResponse(
                success=False,
                message=str(e)
            )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    fits_pb2_grpc.add_MetadataServiceServicer_to_server(MetadataServicer(), server)
    server.add_insecure_port('[::]:50051')
    print("Microservicio de Metadatos iniciado en puerto 50051...")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    # Nota: Asegúrate de generar fits_pb2.py antes de correr esto
    # comando: python -m grpc_tools.protoc -I../proto --python_out=. --grpc_python_out=. ../proto/fits.proto
    serve()
