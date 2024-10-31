from PIL import Image, ImageDraw, ImageFont
import numpy as np

# Función para aplicar umbrales a cada banda de una imagen y devolver imágenes binarias
def aplicar_umbral_por_banda(imagen, umbrales):
    bandas = imagen.split()
    imagenes_binarias = []
    
    for i, banda in enumerate(bandas):
        banda_array = np.array(banda)
        binaria = np.where(banda_array >= umbrales[i], 255, 0).astype(np.uint8)
        imagen_binaria = Image.fromarray(binaria)
        imagenes_binarias.append(imagen_binaria)
    
    return imagenes_binarias

# Función para combinar la imagen original y las imágenes binarias en un solo archivo con etiquetas
def combinar_imagenes_con_etiquetas(imagen_original, imagenes_binarias, etiquetas):
    ancho, alto = imagen_original.size
    espacio_texto = 40  # Espacio adicional para etiquetas
    
    # Crear una nueva imagen con el cuádruple de ancho y espacio adicional para las etiquetas
    imagen_combinada = Image.new("RGB", (ancho * 4, alto + espacio_texto), "white")
    draw = ImageDraw.Draw(imagen_combinada)
    
    try:
        font = ImageFont.truetype("arial.ttf", 20)  # Tamaño ajustable
    except IOError:
        font = ImageFont.load_default()
    
    # Pegar la imagen original
    imagen_combinada.paste(imagen_original, (0, 0))
    
    # Agregar la etiqueta para la imagen original
    texto_original = etiquetas[0]
    text_bbox = draw.textbbox((0, 0), texto_original, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    x_text = (ancho - text_width) // 2
    y_text = alto + 5
    draw.text((x_text, y_text), texto_original, fill="black", font=font)
    
    # Pegar cada imagen binaria en la imagen combinada y agregar etiquetas
    for i, imagen_binaria in enumerate(imagenes_binarias):
        imagen_binaria_rgb = Image.merge("RGB", (imagen_binaria, imagen_binaria, imagen_binaria))
        imagen_combinada.paste(imagen_binaria_rgb, ((i + 1) * ancho, 0))
        
        texto = etiquetas[i + 1]
        text_bbox = draw.textbbox((0, 0), texto, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        x_text = (i + 1) * ancho + (ancho - text_width) // 2
        draw.text((x_text, y_text), texto, fill="black", font=font)
    
    return imagen_combinada

# Ejemplo de uso
if __name__ == "__main__":
    ruta_imagen = r"C:\Users\digni\OneDrive\Desktop\tp1\aves.jpg"
    
    # Cargar la imagen en modo RGB
    imagen = Image.open(ruta_imagen).convert("RGB")
    
    # Aplicar umbrales a cada banda
    umbrales = [100, 150, 200]
    imagenes_binarias = aplicar_umbral_por_banda(imagen, umbrales)
    
    # Etiquetas para cada banda
    etiquetas = ["Imagen Original", "Rojo (R)", "Verde (G)", "Azul (B)"]
    
    # Combinar la imagen original y las imágenes binarias con etiquetas
    imagen_combinada = combinar_imagenes_con_etiquetas(imagen, imagenes_binarias, etiquetas)
    
    # Guardar y mostrar la imagen combinada
    imagen_combinada.save("imagen_combinada_binaria_con_etiquetas.jpg")
    imagen_combinada.show()
