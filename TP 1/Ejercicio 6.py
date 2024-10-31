from PIL import Image
import numpy as np

# Función para obtener el negativo de una imagen RGB
def obtener_negativo(imagen):
    # Convertir la imagen a un arreglo de NumPy para manipulación
    imagen_array = np.array(imagen)
    
    # Calcular el negativo de cada banda (R, G, B)
    negativo_array = 255 - imagen_array
    
    # Convertir el arreglo negativo de vuelta a una imagen
    return Image.fromarray(negativo_array)

# Crear una imagen combinada (original y negativa)
def crear_imagen_combinada(imagen_original, imagen_negativa):
    # Obtener dimensiones de la imagen original
    ancho, alto = imagen_original.size
    
    # Crear una nueva imagen con el doble de ancho para colocar ambas imágenes lado a lado
    imagen_combinada = Image.new("RGB", (ancho * 2, alto))
    
    # Pegar ambas imágenes en la imagen combinada
    imagen_combinada.paste(imagen_original, (0, 0))
    imagen_combinada.paste(imagen_negativa, (ancho, 0))
    
    return imagen_combinada

# Ejemplo de uso
if __name__ == "__main__":
    ruta_imagen = r"C:\Users\digni\OneDrive\Desktop\tp1\aves.jpg"
    
    # Cargar la imagen en modo RGB
    imagen = Image.open(ruta_imagen).convert("RGB")
    
    # Obtener el negativo de la imagen
    imagen_negativa = obtener_negativo(imagen)
    
    # Crear una imagen combinada
    imagen_combinada = crear_imagen_combinada(imagen, imagen_negativa)
    
    # Guardar y mostrar la imagen combinada
    imagen_combinada.save("imagen_original_y_negativa.jpg")
    imagen_combinada.show()
