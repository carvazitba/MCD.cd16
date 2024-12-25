import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage import util

# Función para agregar ruido a una imagen
def agregar_ruido(imagen, tipo_ruido):
    if tipo_ruido == 'gaussiano':
        return util.random_noise(imagen, mode='gaussian', mean=0, var=0.01)
    elif tipo_ruido == 'sal_pimienta':
        return util.random_noise(imagen, mode='s&p', amount=0.05)
    return imagen

# Función para aplicar K-medias a una imagen
def aplicar_kmedias(imagen, k):
    # Convertir la imagen a un arreglo de píxeles en 2D (cada fila es un píxel y cada columna un canal de color)
    datos = imagen.reshape((-1, 3))
    datos = np.float32(datos)  # Convertir a flotante para k-means
    
    # Criterios de parada para k-means (máximo 10 iteraciones o precisión de 1.0)
    criterios = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    
    # Aplicar K-medias
    _, etiquetas, centros = cv2.kmeans(datos, k, None, criterios, 10, cv2.KMEANS_RANDOM_CENTERS)
    
    # Convertir los centros de nuevo a enteros
    centros = np.uint8(centros)
    
    # Asignar el color del centroide a cada píxel
    imagen_segmentada = centros[etiquetas.flatten()]
    imagen_segmentada = imagen_segmentada.reshape(imagen.shape)
    
    return imagen_segmentada

# Función para mostrar los resultados
def mostrar_resultados(imagen_original, imagen_ruido_gaussiano, imagen_ruido_sal_pimienta, k):
    plt.figure(figsize=(15, 10))
    
    # Original
    plt.subplot(2, 3, 1)
    plt.imshow(imagen_original)
    plt.title("Original")
    plt.axis("off")

    # Aplicar K-medias a la imagen original
    resultado_original = aplicar_kmedias(imagen_original, k)
    plt.subplot(2, 3, 2)
    plt.imshow(resultado_original)
    plt.title(f"K-medias (Original, k={k})")
    plt.axis("off")

    # Imagen con ruido Gaussiano
    plt.subplot(2, 3, 4)
    plt.imshow(imagen_ruido_gaussiano)
    plt.title("Ruido Gaussiano")
    plt.axis("off")

    # Aplicar K-medias a la imagen con ruido Gaussiano
    resultado_gaussiano = aplicar_kmedias((imagen_ruido_gaussiano * 255).astype(np.uint8), k)
    plt.subplot(2, 3, 5)
    plt.imshow(resultado_gaussiano)
    plt.title(f"K-medias (Ruido Gaussiano, k={k})")
    plt.axis("off")

    # Imagen con ruido de Sal y Pimienta
    plt.subplot(2, 3, 6)
    plt.imshow(imagen_ruido_sal_pimienta)
    plt.title("Ruido Sal y Pimienta")
    plt.axis("off")

    # Aplicar K-medias a la imagen con ruido de Sal y Pimienta
    resultado_sal_pimienta = aplicar_kmedias((imagen_ruido_sal_pimienta * 255).astype(np.uint8), k)
    plt.subplot(2, 3, 3)
    plt.imshow(resultado_sal_pimienta)
    plt.title(f"K-medias (Ruido Sal y Pimienta, k={k})")
    plt.axis("off")

    plt.tight_layout()
    plt.show()

# Ejemplo de uso
if __name__ == "__main__":
    # Cargar una imagen de prueba
    ruta_imagen = r"C:\Users\digni\OneDrive\Desktop\tp2\t72-1.jpg"  # Cambia esta ruta a tu imagen
    imagen = cv2.imread(ruta_imagen)
    imagen_rgb = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)  # Convertir de BGR a RGB para mostrar correctamente
    
    # Crear versiones contaminadas de la imagen
    imagen_ruido_gaussiano = agregar_ruido(imagen_rgb, 'gaussiano')
    imagen_ruido_sal_pimienta = agregar_ruido(imagen_rgb, 'sal_pimienta')

    # Aplicar K-medias a la imagen original y las versiones contaminadas
    k = 3  # Número de clusters
    mostrar_resultados(imagen_rgb, imagen_ruido_gaussiano, imagen_ruido_sal_pimienta, k)
