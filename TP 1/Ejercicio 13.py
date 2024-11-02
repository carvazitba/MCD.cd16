import cv2
import numpy as np
from PIL import Image

# Función para aplicar el filtro de la media
def filtro_media(imagen, tamaño):
    return cv2.blur(imagen, (tamaño, tamaño))

# Función para aplicar el filtro de la mediana
def filtro_mediana(imagen, tamaño):
    return cv2.medianBlur(imagen, tamaño)

# Función para aplicar el filtro de la mediana ponderada de 3x3
def filtro_mediana_ponderada(imagen):
    kernel = np.array([[1, 2, 1], [2, 4, 2], [1, 2, 1]], np.float32) / 16   #corregir kernel!!!!
    return cv2.filter2D(imagen, -1, kernel)

# Función para aplicar el filtro de Gauss con diferentes valores de sigma
def filtro_gaussiano(imagen, tamaño, sigma):
    return cv2.GaussianBlur(imagen, (tamaño, tamaño), sigma)

# Función para aplicar un filtro de realce de bordes
def filtro_realce_bordes(imagen):
    kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]], np.float32)
    return cv2.filter2D(imagen, -1, kernel)

# Función principal para aplicar todos los filtros y combinar las imágenes
def aplicar_filtros(imagen, tamaño, sigma):
    # Aplicar cada filtro
    imagen_media = filtro_media(imagen, tamaño)
    imagen_mediana = filtro_mediana(imagen, tamaño)
    imagen_mediana_ponderada = filtro_mediana_ponderada(imagen)
    imagen_gauss = filtro_gaussiano(imagen, tamaño, sigma)
    imagen_bordes = filtro_realce_bordes(imagen)
    
    # Combinar las imágenes en una sola fila
    imagen_combinada = np.hstack((
        imagen, 
        imagen_media, 
        imagen_mediana, 
        imagen_mediana_ponderada, 
        imagen_gauss, 
        imagen_bordes
    ))
    
    # Convertir la imagen combinada de BGR a RGB para mostrar con PIL
    return Image.fromarray(cv2.cvtColor(imagen_combinada, cv2.COLOR_BGR2RGB))

# Ejemplo de uso
if __name__ == "__main__":
    ruta_imagen = r"C:\Users\digni\OneDrive\Desktop\tp1\LC09_L2SP_226087_20241026_20241027_02_T1_thumb_large.jpeg"
    imagen = cv2.imread(ruta_imagen)
    
    # Parámetros para los filtros
    tamaño = 3  # Tamaño de la ventana (debe ser impar)
    sigma = 1.0  # Desviación estándar para el filtro gaussiano
    
    # Aplicar filtros y combinar las imágenes en una sola
    imagen_combinada = aplicar_filtros(imagen, tamaño, sigma)
    
    # Guardar y mostrar la imagen combinada
   # imagen_combinada.save("imagen_con_filtros_aplicados.jpg")
    imagen_combinada.show()
