import numpy as np
from PIL import Image

# Funciones para calcular los índices NDVI, NDWI y SVI
def calcular_ndvi(banda_nir, banda_roja):
    # NDVI = (NIR - Red) / (NIR + Red)
    banda_nir = banda_nir.astype(np.float32)
    banda_roja = banda_roja.astype(np.float32)
    ndvi = (banda_nir - banda_roja) / (banda_nir + banda_roja + 1e-5)  # Evitar división por cero
    return ndvi

def calcular_ndwi(banda_nir, banda_verde):
    # NDWI = (Green - NIR) / (Green + NIR)
    banda_nir = banda_nir.astype(np.float32)
    banda_verde = banda_verde.astype(np.float32)
    ndwi = (banda_verde - banda_nir) / (banda_verde + banda_nir + 1e-5)  # Evitar división por cero
    return ndwi

def calcular_svi(banda_nir, banda_roja):
    # SVI puede variar, pero se usa comúnmente NIR / Red
    svi = banda_nir / (banda_roja + 1e-5)  # Evitar división por cero
    return svi

# Función para normalizar el índice y convertirlo en una imagen visualizable
def normalizar_y_convertir_a_imagen(indice):
    # Normalizar los valores a un rango de 0 a 255 para visualización
    indice_normalizado = (indice - np.min(indice)) / (np.max(indice) - np.min(indice)) * 255
    return Image.fromarray(indice_normalizado.astype(np.uint8))

# Ejemplo de uso
if __name__ == "__main__":
    # Rutas a las bandas (supongamos que están separadas en archivos)
    ruta_banda_nir = r"C:\ruta\de\tu\banda_nir.tif"
    ruta_banda_roja = r"C:\ruta\de\tu\banda_roja.tif"
    ruta_banda_verde = r"C:\ruta\de\tu\banda_verde.tif"

    # Cargar las bandas como arreglos de NumPy
    banda_nir = np.array(Image.open(ruta_banda_nir))
    banda_roja = np.array(Image.open(ruta_banda_roja))
    banda_verde = np.array(Image.open(ruta_banda_verde))

    # Calcular los índices
    ndvi = calcular_ndvi(banda_nir, banda_roja)
    ndwi = calcular_ndwi(banda_nir, banda_verde)
    svi = calcular_svi(banda_nir, banda_roja)

    # Convertir los índices a imágenes para visualización
    imagen_ndvi = normalizar_y_convertir_a_imagen(ndvi)
    imagen_ndwi = normalizar_y_convertir_a_imagen(ndwi)
    imagen_svi = normalizar_y_convertir_a_imagen(svi)

    # Mostrar y guardar los índices como imágenes
    imagen_ndvi.show(title="NDVI")
    imagen_ndvi.save("ndvi.jpg")
    
    imagen_ndwi.show(title="NDWI")
    imagen_ndwi.save("ndwi.jpg")
    
    imagen_svi.show(title="SVI")
    imagen_svi.save("svi.jpg")
