import cv2
import numpy as np
import matplotlib.pyplot as plt

def anisotropic_diffusion(img, niter=10, kappa=50, gamma=0.1):
    """
    Aplica el filtro de difusión anisotrópica a una imagen en escala de grises.
    img: imagen en escala de grises.
    niter: número de iteraciones.
    kappa: parámetro que controla el suavizado en los bordes.
    gamma: tasa de difusión.
    """
    img = img.astype('float32')
    for i in range(niter):
        # Calcular gradientes en las cuatro direcciones
        deltaN = np.roll(img, -1, axis=0) - img
        deltaS = np.roll(img, 1, axis=0) - img
        deltaE = np.roll(img, -1, axis=1) - img
        deltaW = np.roll(img, 1, axis=1) - img
        
        # Función de conductancia (Perona-Malik)
        cN = np.exp(-(deltaN/kappa)**2)
        cS = np.exp(-(deltaS/kappa)**2)
        cE = np.exp(-(deltaE/kappa)**2)
        cW = np.exp(-(deltaW/kappa)**2)
        
        # Actualización de la imagen
        img += gamma * (cN * deltaN + cS * deltaS + cE * deltaE + cW * deltaW)
    
    return img

def apply_filters(image_path):
    # Cargar la imagen en escala de grises
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print(f"Error: No se pudo cargar la imagen en {image_path}. Verifica la ruta.")
        return
    
    # Aplicar filtro de difusión anisotrópica
    anisotropic_result = anisotropic_diffusion(img, niter=10, kappa=50, gamma=0.1)
    
    # Aplicar filtro Gaussiano para comparar
    gaussian_result = cv2.GaussianBlur(img, (15, 15), sigmaX=0, sigmaY=0)

    # Mostrar los resultados para comparación en una disposición de 3x1
    plt.figure(figsize=(10, 18))  # Tamaño de la figura para visualización más grande
    plt.subplot(3, 1, 1)
    plt.imshow(img, cmap='gray')
    plt.title("Original")
    plt.axis("off")

    plt.subplot(3, 1, 2)
    plt.imshow(anisotropic_result, cmap='gray')
    plt.title("Difusión Anisotrópica")
    plt.axis("off")
    
    plt.subplot(3, 1, 3)
    plt.imshow(gaussian_result, cmap='gray')
    plt.title("Filtro Gaussiano")
    plt.axis("off")
    
    plt.show()

# Ejemplo de uso
# Cambia la ruta de la imagen según la ubicación de tu archivo.
image_path = r'C:\Users\digni\OneDrive\Desktop\tp2\t80-1.jpg'  # Asegúrate de que esta ruta sea correcta
apply_filters(image_path)
