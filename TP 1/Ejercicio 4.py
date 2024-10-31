import rasterio
import numpy as np

# Cargar la imagen satelital
def cargar_imagen(ruta_archivo):
    return rasterio.open(ruta_archivo)

# Analizar región y calcular estadísticas
def analizar_region(imagen, caja):
    # Extraer las coordenadas de la caja
    x1, y1, x2, y2 = caja
    
    # Leer las bandas en la región especificada
    bandas = []
    for i in range(1, imagen.count + 1):  # imagen.count da el número de bandas
        banda = imagen.read(i, window=rasterio.windows.Window(x1, y1, x2 - x1, y2 - y1))
        bandas.append(banda)

    # Calcular cantidad de píxeles en la región
    num_pixels = bandas[0].size

    # Calcular el promedio por cada banda en la región
    promedios = [np.mean(banda) for banda in bandas]

    # Imprimir resultados
    print(f"Cantidad de píxeles en la región: {num_pixels}")
    print(f"Cantidad de bandas: {len(bandas)}")
    for i, promedio in enumerate(promedios, start=1):
        print(f"Promedio de la banda {i}: {promedio}")

# Ejemplo de uso
if __name__ == "__main__":
    ruta_imagen = r"C:\Users\digni\OneDrive\Desktop\tp1\LC09_L2SP_226087_20241026_20241027_02_T1_thumb_large.jpeg"
    with cargar_imagen(ruta_imagen) as imagen:
        # Define la caja de la región a analizar (x1, y1, x2, y2) en coordenadas de píxel
        caja = (100, 100, 400, 400)
        analizar_region(imagen, caja)
