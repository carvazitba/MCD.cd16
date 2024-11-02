import cv2
import numpy as np
import matplotlib.pyplot as plt

def sift_feature_matching(img1_path, img2_path):
    # Intentar cargar la primera imagen
    print(f"Intentando cargar la imagen 1 desde: {img1_path}")
    img1 = cv2.imread(img1_path, cv2.IMREAD_GRAYSCALE)
    if img1 is None:
        print(f"Error: No se pudo cargar la imagen en {img1_path}. Verifica la ruta.")
        return

    # Intentar cargar la segunda imagen
    print(f"Intentando cargar la imagen 2 desde: {img2_path}")
    img2 = cv2.imread(img2_path, cv2.IMREAD_GRAYSCALE)
    if img2 is None:
        print(f"Error: No se pudo cargar la imagen en {img2_path}. Verifica la ruta.")
        return
    
    # Inicializar el detector SIFT
    sift = cv2.SIFT_create()
    
    # Detectar y computar puntos clave y descriptores con SIFT en ambas imágenes
    kp1, des1 = sift.detectAndCompute(img1, None)
    kp2, des2 = sift.detectAndCompute(img2, None)
    
    # Imprimir la cantidad de puntos clave detectados en cada imagen
    print(f"Puntos clave en la imagen 1: {len(kp1)}")
    print(f"Puntos clave en la imagen 2: {len(kp2)}")
    
    # Usar el matcher de FLANN para encontrar coincidencias entre los descriptores
    index_params = dict(algorithm=1, trees=5)  # Parámetros de FLANN
    search_params = dict(checks=50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des1, des2, k=2)
    
    # Aplicar la prueba de razón de Lowe para filtrar coincidencias
    good_matches = []
    for m, n in matches:
        if m.distance < 0.7 * n.distance:
            good_matches.append(m)
    
    # Imprimir el número de coincidencias válidas
    print(f"Coincidencias válidas: {len(good_matches)}")
    
       
    # Dibujar las coincidencias encontradas entre las dos imágenes con líneas más gruesas
    img_matches = cv2.drawMatches(
        img1, kp1, img2, kp2, good_matches, None, 
        flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS,
        matchColor=(0, 255, 0),  # Color de las líneas de coincidencia
        singlePointColor=(255, 0, 0),  # Color de los puntos clave
        matchesThickness=3  # Grosor de las líneas de coincidencia
    )
    
    # Mostrar el resultado
    plt.figure(figsize=(15, 10))
    plt.imshow(img_matches)
    plt.title(f"Coincidencias encontradas: {len(good_matches)}")
    plt.show()
    
    # Retornar el número de coincidencias
    return len(good_matches)

# Ejemplo de uso
# Cambia las rutas de las imágenes según la ubicación de tus archivos.
img1_path = r'C:\Users\digni\OneDrive\Desktop\tp2\t80-1.jpg'  # Asegúrate de que esta ruta sea correcta
img2_path = r'C:\Users\digni\OneDrive\Desktop\tp2\t72-sinfondo.png'  # Asegúrate de que esta ruta sea correcta
num_matches = sift_feature_matching(img1_path, img2_path)
print(f"Coincidencias encontradas: {num_matches}")
