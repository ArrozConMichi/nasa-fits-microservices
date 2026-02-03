import numpy as np
import grpc
from concurrent import futures
import os
import fits_pb2
import fits_pb2_grpc
from astropy.io import fits
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io

DATA_DIR = "/app/data"

class ImageServicer(fits_pb2_grpc.ImageServiceServicer):
    def GetImageData(self, request, context):
        file_path = os.path.join(DATA_DIR, request.filename)
        
        if not os.path.exists(file_path):
            return fits_pb2.ImageResponse(success=False, format="", image_data=b"")

        try:
            with fits.open(file_path) as hdul:
                data = hdul[0].data
                
                # Si la data es None (archivo vacío de imagen), salimos
                if data is None:
                    return fits_pb2.ImageResponse(success=False, format="", image_data=b"")

                # Manejo de cubos de datos (3D)
                if len(data.shape) == 3: 
                    data = data[0]
                
                # --- MANEJO DE PIXELS DAÑADOS (NaN) ---
                # Esto evita que crashee si el FITS tiene "huecos" o píxeles muertos
                valid_data = data[np.isfinite(data)]
                
                if valid_data.size > 0:
                    p1, p99 = np.percentile(valid_data, (1, 99))
                else:
                    # Si todo son errores, usamos valores por defecto para evitar crash
                    p1, p99 = 0, 1
                
                # --- RENDERIZADO ---
                plt.figure(figsize=(10, 10))
                
                # Usamos 'inferno' como te gustó, y 'nan' se verá transparente/negro
                plt.imshow(data, cmap='inferno', origin='lower', vmin=p1, vmax=p99, interpolation='nearest')
                plt.axis('off')
                
                buf = io.BytesIO()
                plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
                buf.seek(0)
                img_bytes = buf.getvalue()
                plt.close()

                return fits_pb2.ImageResponse(success=True, format="png", image_data=img_bytes)
                
        except Exception as e:
            print(f"Error procesando {request.filename}: {e}")
            return fits_pb2.ImageResponse(success=False, format="", image_data=b"")
        file_path = os.path.join(DATA_DIR, request.filename)
        
        if not os.path.exists(file_path):
            return fits_pb2.ImageResponse(success=False, format="", image_data=b"")

        try:
            with fits.open(file_path) as hdul:
                data = hdul[0].data
                if len(data.shape) == 3: data = data[0]

                # --- MAGIA VISUAL: Percentile Stretching ---
                # En lugar de min/max, usamos el 1% y 99% para ignorar ruido extremo
                # Esto hace que el fondo sea negro y los detalles resalten
                p1, p99 = np.percentile(data, (1, 99))
                
                plt.figure(figsize=(10, 10))
                # vmin/vmax normalizados
                plt.imshow(data, cmap='inferno', origin='lower', vmin=p1, vmax=p99)
                plt.axis('off')
                
                buf = io.BytesIO()
                plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
                buf.seek(0)
                img_bytes = buf.getvalue()
                plt.close()

                return fits_pb2.ImageResponse(success=True, format="png", image_data=img_bytes)
                
        except Exception as e:
            print(f"Error: {e}")
            return fits_pb2.ImageResponse(success=False, format="", image_data=b"")
        file_path = os.path.join(DATA_DIR, request.filename)
        
        if not os.path.exists(file_path):
            return fits_pb2.ImageResponse(
                success=False,
                format="",
                image_data=b""
            )

        try:
            with fits.open(file_path) as hdul:
                # Intentamos obtener los datos de la primera extensión
                # Los FITS suelen tener la imagen en la extensión 1, a veces en la 0
                data = hdul[0].data
                
                # Si la imagen es 3D (un cubo de datos), tomamos la primera capa
                if len(data.shape) == 3:
                    data = data[0]

                # Normalizar y graficar con Matplotlib
                plt.figure(figsize=(8, 8))
                plt.imshow(data, cmap='gray', origin='lower', vmin=data.min(), vmax=data.max())
                plt.axis('off') # Sin ejes, solo la imagen

                # Guardar en memoria (BytesIO) en lugar de archivo
                buf = io.BytesIO()
                plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
                buf.seek(0)
                img_bytes = buf.getvalue()
                plt.close()

                return fits_pb2.ImageResponse(
                    success=True,
                    format="png",
                    image_data=img_bytes
               )
                
        except Exception as e:
            print(f"Error procesando imagen: {e}")
            return fits_pb2.ImageResponse(
                success=False,
                format="",
                image_data=b""
            )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    fits_pb2_grpc.add_ImageServiceServicer_to_server(ImageServicer(), server)
    server.add_insecure_port('[::]:50052')
    print("Microservicio de Imágenes iniciado en puerto 50052...")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()