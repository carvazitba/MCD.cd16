import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage import util

# Función para agregar ruido Gaussiano y ruido de sal y pimienta
def agregar_ruido(imagen, tipo_ruido):
    if tipo_ruido == 'gaussiano':
        return util.random_noise(imagen, mode='gaussian', mean=0, var=0.01)
    elif tipo_ruido == 'sal_pimienta':
        return util.random_noise(imagen, mode='s&p', amount=0.05)
    return imagen

# Implementación básica de SUSAN para detección de bordes y esquinas
def susan_detector(imagen, modo='bordes', radio=3, threshold=27):
    # Convertir la imagen a escala de grises
    imagen_gray = cv2.cvtColor(imagen, cv2.COLOR_RGB2GRAY)
    h, w = imagen_gray.shape
    salida = np.zeros((h, w), dtype=np.uint8)
    
    # Crear una ventana circular (máscara) para analizar el vecindario
    mascara = np.zeros((2*radio+1, 2*radio+1), dtype=np.uint8)
    cv2.circle(mascara, (radio, radio), radio, 1, -1)
    
    # Procesar cada píxel
    for i in range(radio, h - radio):
        for j in range(radio, w - radio):
            region = imagen_gray[i - radio:i + radio + 1, j - radio:j + radio + 1]
            region_mascara = region[mascara == 1]
            
            # Contar los píxeles similares al centro
            centro = imagen_gray[i, j]
            num_similares = np.sum(np.abs(region_mascara - centro) < threshold)
            
            # Detectar bordes o esquinas
            if modo == 'bordes':
                if num_similares < 0.5 * np.sum(mascara):  # Umbral para bordes
                    salida[i, j] = 255
            elif modo == 'esquinas':
                if num_similares < 0.75 * np.sum(mascara):  # Umbral para esquinas
                    salida[i, j] = 255
    
    return salida

# Función para mostrar los resultados
def mostrar_resultados(imagen_original, imagen_ruido_gaussiano, imagen_ruido_sal_pimienta, tipo_deteccion):
    plt.figure(figsize=(15, 10))
    
    # Original
    plt.subplot(2, 3, 1)
    plt.imshow(imagen_original, cmap='gray')
    plt.title("Original")
    plt.axis("off")

    # Aplicar SUSAN a la imagen original
    resultado_original = susan_detector(imagen_original, tipo_deteccion)
    plt.subplot(2, 3, 2)
    plt.imshow(resultado_original, cmap='gray')
    plt.title(f"{tipo_deteccion.capitalize()} (Original)")
    plt.axis("off")

    # Imagen con ruido Gaussiano
    plt.subplot(2, 3, 4)
    plt.imshow(imagen_ruido_gaussiano, cmap='gray')
    plt.title("Ruido Gaussiano")
    plt.axis("off")

    # Aplicar SUSAN a la imagen con ruido Gaussiano
    resultado_gaussiano = susan_detector(imagen_ruido_gaussiano, tipo_deteccion)
    plt.subplot(2, 3, 5)
    plt.imshow(resultado_gaussiano, cmap='gray')
    plt.title(f"{tipo_deteccion.capitalize()} (Ruido Gaussiano)")
    plt.axis("off")

    # Imagen con ruido de Sal y Pimienta
    plt.subplot(2, 3, 6)
    plt.imshow(imagen_ruido_sal_pimienta, cmap='gray')
    plt.title("Ruido Sal y Pimienta")
    plt.axis("off")

    # Aplicar SUSAN a la imagen con ruido de Sal y Pimienta
    resultado_sal_pimienta = susan_detector(imagen_ruido_sal_pimienta, tipo_deteccion)
    plt.subplot(2, 3, 3)
    plt.imshow(resultado_sal_pimienta, cmap='gray')
    plt.title(f"{tipo_deteccion.capitalize()} (Ruido Sal y Pimienta)")
    plt.axis("off")

    plt.tight_layout()
    plt.show()

# Ejemplo de uso
if __name__ == "__main__":
    # Cargar una imagen de prueba
    ruta_imagen = r"C:\Users\digni\OneDrive\Desktop\tp2\t72-1.jpg"  # Cambia esta ruta a tu imagen
    imagen = cv2.imread(ruta_imagen)
    
    # Crear versiones contaminadas de la imagen
    imagen_ruido_gaussiano = agregar_ruido(imagen, 'gaussiano')
    imagen_ruido_sal_pimienta = agregar_ruido(imagen, 'sal_pimienta')

    # Convertir a formato 8 bits (de 0 a 255) para visualización
    imagen_ruido_gaussiano = (imagen_ruido_gaussiano * 255).astype(np.uint8)
    imagen_ruido_sal_pimienta = (imagen_ruido_sal_pimienta * 255).astype(np.uint8)

    # Aplicar el detector SUSAN para detección de bordes
    mostrar_resultados(imagen, imagen_ruido_gaussiano, imagen_ruido_sal_pimienta, 'bordes')

    # Aplicar el detector SUSAN para detección de esquinas
    mostrar_resultados(imagen, imagen_ruido_gaussiano, imagen_ruido_sal_pimienta, 'esquinas')
