


import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

def apply_gamma_correction(image_array, gamma, c=1):
    # Normalizar la imagen a [0, 1]
    normalized_image = image_array / 255.0
    # Aplicar la transformación gamma
    gamma_corrected_image = c * (normalized_image ** gamma)
    # Desnormalizar de vuelta a [0, 255]
    gamma_corrected_image = np.clip(gamma_corrected_image * 255, 0, 255).astype(np.uint8)
    return gamma_corrected_image

# Cargar la imagen en escala de grises
file_path = r"C:\Users\digni\OneDrive\Desktop\tp1\LC09_L2SP_226087_20241026_20241027_02_T1_thumb_large.jpeg"  # Cambia a tu imagen
image = Image.open(file_path).convert('L')  # Convertir a escala de grises
image_array = np.array(image)

# Variar los valores de gamma
gamma_values = [0.5, 0.8, 1.2, 1.5]
gamma_images = []

# Aplicar la corrección gamma para cada valor
for gamma in gamma_values:
    corrected_image = apply_gamma_correction(image_array, gamma)
    gamma_images.append(corrected_image)

# Mostrar las imágenes originales y corregidas
plt.figure(figsize=(12, 8))
plt.subplot(2, 3, 1)
plt.imshow(image_array, cmap='gray')
plt.title('Imagen Original')
plt.axis('off')

for i, gamma in enumerate(gamma_values):
    plt.subplot(2, 3, i + 2)
    plt.imshow(gamma_images[i], cmap='gray')
    plt.title(f'Gamma = {gamma}')
    plt.axis('off')

plt.tight_layout()
plt.show()


# Ejemplo de uso
# file_path = r"C:\Users\digni\OneDrive\Desktop\tp1\LC09_L2SP_226087_20241026_20241027_02_T1_thumb_large.jpeg"  # Ruta de la imagen satelital
