import grpc
import sys
import os
from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response

# Asegurar que encuentra el proto (en producción esto se maneja montando volúmenes o instalando el paquete proto)
# Asumimos que en Docker el volumen se monta en /app/proto
sys.path.append('/app/proto') 
import fits_pb2
import fits_pb2_grpc

class FitsMetadataView(APIView):
    """
    API View que recibe una petición HTTP GET /api/metadata/<filename>
    y la traduce a una llamada gRPC al microservicio fits-metadata.
    """
    def get(self, request, filename):
        try:
            # Conectar al servicio de metadatos (nombre del servicio en docker-compose)
            with grpc.insecure_channel('fits-metadata:50051') as channel:
                stub = fits_pb2_grpc.MetadataServiceStub(channel)
                grpc_response = stub.GetFileMetadata(fits_pb2.MetadataRequest(filename=filename))
                
                if grpc_response.success:
                    # Formatear la respuesta para el Frontend
                    headers_data = [
                        {'key': h.key, 'value': h.value, 'comment': h.comment} 
                        for h in grpc_response.headers
                    ]
                    return Response({
                        'status': 'success',
                        'filename': filename,
                        'data': headers_data
                    })
                else:
                    return Response({
                        'status': 'error',
                        'message': grpc_response.message
                    }, status=404)

        except grpc.RpcError as e:
            return Response({
                'status': 'error', 
                'message': f'gRPC communication error: {e.code()}'
            }, status=503)
        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=500)
        
class FitsImageView(APIView):
    """
    Recibe un GET /api/image/<filename>
    Llama al procesador y devuelve los bytes de la imagen.
    """
    def get(self, request, filename):
        try:
            # Usamos el canal del nuevo servicio de imágenes
            with grpc.insecure_channel('fits-processor:50052') as channel:
                stub = fits_pb2_grpc.ImageServiceStub(channel)
                grpc_response = stub.GetImageData(fits_pb2.ImageRequest(filename=filename))
                
                if grpc_response.success:
                    # Devolvemos la imagen directamente al navegador
                    return HttpResponse(content=grpc_response.image_data, content_type='image/png')
                else:
                    return Response({'status': 'error', 'message': 'Could not process image'}, status=500)

        except grpc.RpcError as e:
            return Response({'status': 'error', 'message': f'gRPC error: {e.code()}'}, status=503)