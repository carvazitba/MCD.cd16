import cv2
import matplotlib.pyplot as plt

def apply_filters(image_path):
    # Cargar la imagen en color
    img = cv2.imread(image_path)
    if img is None:
        print(f"Error: No se pudo cargar la imagen en {image_path}. Verifica la ruta.")
        return
    
    # Aplicar filtro bilateral con diferentes parámetros
    bilateral1 = cv2.bilateralFilter(img, d=9, sigmaColor=75, sigmaSpace=75)
    bilateral2 = cv2.bilateralFilter(img, d=15, sigmaColor=150, sigmaSpace=150)
    bilateral3 = cv2.bilateralFilter(img, d=25, sigmaColor=250, sigmaSpace=250)
    
    # Aplicar filtro Gaussiano para comparar
    gaussian = cv2.GaussianBlur(img, (15, 15), sigmaX=0, sigmaY=0)

    # Mostrar los resultados para comparación en una disposición de 3x2
    plt.figure(figsize=(15, 15))  # Ajuste del tamaño de la figura para una visualización más grande
    plt.subplot(3, 2, 1)
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.title("Original")
    plt.axis("off")

    plt.subplot(3, 2, 2)
    plt.imshow(cv2.cvtColor(bilateral1, cv2.COLOR_BGR2RGB))
    plt.title("Bilateral d=9, sc=75, ss=75")
    plt.axis("off")
    
    plt.subplot(3, 2, 3)
    plt.imshow(cv2.cvtColor(bilateral2, cv2.COLOR_BGR2RGB))
    plt.title("Bilateral d=15, sc=150, ss=150")
    plt.axis("off")

    plt.subplot(3, 2, 4)
    plt.imshow(cv2.cvtColor(bilateral3, cv2.COLOR_BGR2RGB))
    plt.title("Bilateral d=25, sc=250, ss=250")
    plt.axis("off")

    plt.subplot(3, 2, 5)
    plt.imshow(cv2.cvtColor(gaussian, cv2.COLOR_BGR2RGB))
    plt.title("GaussianBlur k=15")
    plt.axis("off")
    
    plt.show()

# Ejemplo de uso
# Cambia la ruta de la imagen según la ubicación de tu archivo.
image_path = r'C:\Users\digni\OneDrive\Desktop\tp2\t80-1.jpg'  # Asegúrate de que esta ruta sea correcta
apply_filters(image_path)
