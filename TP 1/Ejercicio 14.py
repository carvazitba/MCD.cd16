import cv2
import numpy as np
from PIL import Image

# Función para aplicar el operador de Prewitt
def detector_bordes_prewitt(imagen):
    # Convertir a escala de grises si la imagen es RGB
    imagen_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    
    # Definir los kernels de Prewitt para los gradientes X e Y
    kernel_prewitt_x = np.array([[1, 0, -1], [1, 0, -1], [1, 0, -1]], dtype=np.float32)
    kernel_prewitt_y = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]], dtype=np.float32)
    
    # Aplicar los filtros
    gradiente_x = cv2.filter2D(imagen_gris, -1, kernel_prewitt_x)
    gradiente_y = cv2.filter2D(imagen_gris, -1, kernel_prewitt_y)
    
    # Calcular la magnitud del gradiente
    magnitud_prewitt = cv2.magnitude(gradiente_x.astype(np.float32), gradiente_y.astype(np.float32))
    magnitud_prewitt = np.clip(magnitud_prewitt, 0, 255).astype(np.uint8)
    
    return magnitud_prewitt

# Función para aplicar el operador de Sobel
def detector_bordes_sobel(imagen):
    # Convertir a escala de grises si la imagen es RGB
    imagen_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    
    # Aplicar el filtro de Sobel para los gradientes X e Y
    gradiente_x = cv2.Sobel(imagen_gris, cv2.CV_64F, 1, 0, ksize=3)
    gradiente_y = cv2.Sobel(imagen_gris, cv2.CV_64F, 0, 1, ksize=3)
    
    # Calcular la magnitud del gradiente
    magnitud_sobel = cv2.magnitude(gradiente_x, gradiente_y)
    magnitud_sobel = np.clip(magnitud_sobel, 0, 255).astype(np.uint8)
    
    return magnitud_sobel

# Función para combinar las imágenes de los bordes detectados en un solo archivo
def combinar_imagenes_bordes(imagen_original, imagen_prewitt, imagen_sobel):
    # Convertir imágenes a RGB para su visualización conjunta
    imagen_original_rgb = cv2.cvtColor(imagen_original, cv2.COLOR_BGR2RGB)
    imagen_prewitt_rgb = cv2.cvtColor(imagen_prewitt, cv2.COLOR_GRAY2RGB)
    imagen_sobel_rgb = cv2.cvtColor(imagen_sobel, cv2.COLOR_GRAY2RGB)
    
    # Combinar las imágenes horizontalmente
    imagen_combinada = np.hstack((imagen_original_rgb, imagen_prewitt_rgb, imagen_sobel_rgb))
    
    return Image.fromarray(imagen_combinada)

# Ejemplo de uso
if __name__ == "__main__":
    ruta_imagen = r"C:\Users\digni\OneDrive\Desktop\tp1\LC09_L2SP_226087_20241026_20241027_02_T1_thumb_large.jpeg"
    imagen = cv2.imread(ruta_imagen)
    
    # Aplicar el detector de bordes con Prewitt y Sobel
    imagen_bordes_prewitt = detector_bordes_prewitt(imagen)
    imagen_bordes_sobel = detector_bordes_sobel(imagen)
    
    # Combinar las imágenes en una sola
    imagen_combinada = combinar_imagenes_bordes(imagen, imagen_bordes_prewitt, imagen_bordes_sobel)
    
    # Guardar y mostrar la imagen combinada
   #imagen_combinada.save("imagen_bordes_combinada.jpg")
    imagen_combinada.show()
