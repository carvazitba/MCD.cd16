from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

# Función de corrección gamma
def aplicar_gamma(imagen, gamma):
    # Convertir la imagen en escala de grises a un arreglo de NumPy
    imagen_array = np.array(imagen, dtype=np.float32) / 255.0  # Normalizar a [0,1]
    
    # Aplicar la transformación de potencia
    imagen_corrigida = np.power(imagen_array, gamma)
    
    # Convertir de nuevo a un rango de píxeles de 0-255
    imagen_corrigida = (imagen_corrigida * 255).astype(np.uint8)
    
    # Convertir el arreglo modificado de nuevo a una imagen
    return Image.fromarray(imagen_corrigida)

# Mostrar resultados con diferentes valores de gamma
def mostrar_resultados(imagen, gammas):
    plt.figure(figsize=(12, 4))
    for i, gamma in enumerate(gammas, start=1):
        imagen_corrigida = aplicar_gamma(imagen, gamma)
        plt.subplot(1, len(gammas), i)
        plt.imshow(imagen_corrigida, cmap="gray")
        plt.title(f"Gamma = {gamma}")
        plt.axis("off")
    plt.show()

# Ejemplo de uso
if __name__ == "__main__":
    ruta_imagen = r"C:\Users\digni\OneDrive\Desktop\tp1\LC09_L2SP_226087_20241026_20241027_02_T1_thumb_large.jpeg"
    
    # Cargar la imagen y convertirla a escala de grises
    imagen = Image.open(ruta_imagen).convert("L")
    
    # Valores de gamma para probar
    gammas = [0.5, 0.8, 1.2, 1.5]
    
    # Mostrar los resultados de la corrección gamma
    mostrar_resultados(imagen, gammas)
