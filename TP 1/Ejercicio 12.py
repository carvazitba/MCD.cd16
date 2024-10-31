from PIL import Image
import numpy as np

# Función para agregar ruido impulsivo (sal y pimienta)
def agregar_ruido_sal_pimienta(imagen, densidad):
    # Convertir la imagen a un arreglo NumPy
    imagen_array = np.array(imagen)
    
    # Crear una máscara aleatoria para aplicar el ruido
    mascara = np.random.rand(*imagen_array.shape[:2])
    
    # Aplicar "sal" (píxeles blancos)
    imagen_array[mascara < (densidad / 2)] = 255  # Sal
    
    # Aplicar "pimienta" (píxeles negros)
    imagen_array[(mascara >= (densidad / 2)) & (mascara < densidad)] = 0  # Pimienta
    
    # Convertir el arreglo de vuelta a una imagen
    return Image.fromarray(imagen_array)

# Función para combinar la imagen original y la imagen con ruido en un solo archivo
def combinar_imagenes(imagen_original, imagen_ruido):
    ancho, alto = imagen_original.size
    
    # Crear una nueva imagen con el doble de ancho para colocar ambas imágenes lado a lado
    imagen_combinada = Image.new("RGB", (ancho * 2, alto))
    
    # Pegar ambas imágenes en la imagen combinada
    imagen_combinada.paste(imagen_original, (0, 0))
    imagen_combinada.paste(imagen_ruido, (ancho, 0))
    
    return imagen_combinada

# Ejemplo de uso
if __name__ == "__main__":
    ruta_imagen = r"C:\Users\digni\OneDrive\Desktop\tp1\aves.jpg"
    imagen = Image.open(ruta_imagen).convert("RGB")
    
    # Parámetros de ruido
    densidad = 0.1  # Densidad de ruido entre 0 y 1 (por ejemplo, 0.1 para 10% de píxeles afectados)
    
    # Generar imagen con ruido de sal y pimienta
    imagen_ruido_sal_pimienta = agregar_ruido_sal_pimienta(imagen, densidad)
    
    # Combinar la imagen original y la imagen con ruido
    imagen_combinada = combinar_imagenes(imagen, imagen_ruido_sal_pimienta)
    
    # Mostrar y guardar la imagen combinada
    imagen_combinada.show()
    imagen_combinada.save("imagen_original_y_con_ruido_sal_pimienta.jpg")
