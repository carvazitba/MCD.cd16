from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

# Función para calcular y devolver el histograma de niveles de gris de cada banda
def calcular_histograma(imagen):
    # Separar las bandas (R, G, B)
    bandas = imagen.split()
    
    # Diccionario para almacenar el histograma de cada banda
    histogramas = {}
    colores = ['Red', 'Green', 'Blue']
    
    # Calcular el histograma para cada banda
    for i, banda in enumerate(bandas):
        histograma, _ = np.histogram(banda, bins=256, range=(0, 255))
        histogramas[colores[i]] = histograma
    
    return histogramas

# Función para mostrar el histograma de cada banda
def mostrar_histogramas(histogramas):
    colores = ['Red', 'Green', 'Blue']
    plt.figure(figsize=(12, 4))
    
    # Graficar el histograma de cada banda
    for i, color in enumerate(colores):
        plt.subplot(1, 3, i+1)
        plt.bar(range(256), histogramas[color], color=color.lower())
        plt.title(f"Histograma de la banda {color}")
        plt.xlabel("Intensidad")
        plt.ylabel("Frecuencia")
    
    plt.tight_layout()
    plt.show()

# Ejemplo de uso
if __name__ == "__main__":
    ruta_imagen = r"C:\Users\digni\OneDrive\Desktop\tp1\aves.jpg"
    
    # Cargar la imagen en modo RGB
    imagen = Image.open(ruta_imagen).convert("RGB")
    
    # Calcular el histograma de cada banda
    histogramas = calcular_histograma(imagen)
    
    # Mostrar los histogramas
    mostrar_histogramas(histogramas)
