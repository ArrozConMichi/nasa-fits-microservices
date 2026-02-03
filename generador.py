import numpy as np
from astropy.io import fits
import os

def crear_fits_sintetico(nombre_archivo="test.fits", size=512):
    print(f"Creando {nombre_archivo} ({size}x{size})...")
    
    # Generamos datos float32 para precisión
    data = np.zeros((size, size), dtype=np.float32)
    
    # Fondo con estructura de ruido un poco más compleja
    data += np.random.normal(loc=100, scale=10, size=(size, size))
    
    # Añadir galaxia central (espiral simulada simplificada)
    xx, yy = np.meshgrid(np.arange(size), np.arange(size))
    dist = np.sqrt((xx - size//2)**2 + (yy - size//2)**2)
    # Un brillo central que cae suavemente
    data += 3000 * np.exp(-(dist**2) / (2 * (size/4)**2))

    # Añadir 50 estrellas aleatorias
    for _ in range(50):
        x = np.random.randint(0, size)
        y = np.random.randint(0, size)
        brillo = np.random.randint(500, 2000)
        radio = np.random.uniform(2, 6)
        dist_local = np.sqrt((xx - x)**2 + (yy - y)**2)
        data += brillo * np.exp(-(dist_local**2) / (2 * radio**2))

    hdu = fits.PrimaryHDU(data)
    hdu.writeto(nombre_archivo, overwrite=True)
    print(f"Guardado: {nombre_archivo} ({os.path.getsize(nombre_archivo)/1024/1024:.2f} MB)")

# Generar archivos de prueba de distintos tamaños
if not os.path.exists('data'): os.makedirs('data')

crear_fits_sintetico("data/small.fits", size=512)      # ~1 MB
crear_fits_sintetico("data/medium.fits", size=1024)    # ~4 MB
crear_fits_sintetico("data/large.fits", size=2048)     # ~16 MB - Bueno para probar lag
crear_fits_sintetico("data/huge.fits", size=4096)      # ~64 MB - Stress test real