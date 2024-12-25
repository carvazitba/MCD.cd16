import cv2
from PIL import Image, ImageOps, ImageDraw, ImageFont
import numpy as np
import matplotlib.pyplot as plt

# Función para aplicar el detector de bordes de Canny
def aplicar_canny(imagen, threshold1, threshold2):
    # Convertir la imagen a escala de grises
    imagen_gray = cv2.cvtColor(np.array(imagen), cv2.COLOR_RGB2GRAY)
    # Aplicar el detector de bordes de Canny
    bordes = cv2.Canny(imagen_gray, threshold1, threshold2)
    return Image.fromarray(bordes)

# Función para mostrar los resultados de Canny con diferentes parámetros en una sola imagen
def mostrar_resultados_canny(imagen_original, resultados_canny, parametros):
    ancho, alto = imagen_original.size
    filas = 1 + len(resultados_canny)  # Imagen original + resultados
    espacio_texto = 30  # Espacio para etiquetas

    # Crear una nueva imagen para acomodar todos los resultados
    imagen_combinada = Image.new("L", (ancho, alto * filas + espacio_texto * len(resultados_canny)), "white")
    draw = ImageDraw.Draw(imagen_combinada)
    font = ImageFont.load_default()

    # Pegar la imagen original
    imagen_combinada.paste(imagen_original.convert("L"), (0, 0))
    draw.text((10, alto - 20), "Imagen Original", fill="black", font=font)
    
    # Pegar cada resultado de Canny y agregar etiquetas con los parámetros usados
    for i, (imagen_canny, (t1, t2)) in enumerate(zip(resultados_canny, parametros)):
        y_offset = alto * (i + 1) + espacio_texto * i
        imagen_combinada.paste(imagen_canny, (0, y_offset))
        
        # Etiqueta para los parámetros de Canny
        etiqueta = f"Canny (t1={t1}, t2={t2})"
        draw.text((10, y_offset + alto - 20), etiqueta, fill="black", font=font)

    return imagen_combinada

# Ejemplo de uso
if __name__ == "__main__":
    ruta_imagen = r"c:\Users\digni\OneDrive\Desktop\tp2\radiografia2.jpg"
    
    # Cargar la imagen en modo RGB
    imagen = Image.open(ruta_imagen).convert("RGB")
    
    # Parámetros de Canny para probar
    parametros_canny = [
        (135, 140),
        (100, 200),
        (50, 150),
    ]
    
    # Aplicar el detector de Canny con diferentes parámetros
    resultados_canny = [aplicar_canny(imagen, t1, t2) for t1, t2 in parametros_canny]
    
    # Crear una imagen combinada con todos los resultados
    imagen_combinada = mostrar_resultados_canny(imagen, resultados_canny, parametros_canny)
    
    # Guardar y mostrar la imagen combinada
    imagen_combinada.save("imagen_canny_resultados.jpg")
    imagen_combinada.show("imagen_canny_resultados.jpg")
