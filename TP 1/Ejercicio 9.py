from PIL import Image, ImageOps, ImageDraw
import numpy as np

# Función para ecualizar el histograma de cada banda en una imagen en color
def ecualizar_imagen_color(imagen):
    bandas = imagen.split()
    bandas_ecualizadas = []
    
    for banda in bandas:
        banda_array = np.array(banda)
        histograma, _ = np.histogram(banda_array, bins=256, range=(0, 255))
        cdf = histograma.cumsum()
        cdf_normalizada = cdf * 255 / cdf[-1]
        
        banda_ecualizada = np.interp(banda_array.flatten(), range(256), cdf_normalizada)
        banda_ecualizada = banda_ecualizada.reshape(banda_array.shape).astype(np.uint8)
        
        bandas_ecualizadas.append(Image.fromarray(banda_ecualizada))
    
    return Image.merge("RGB", bandas_ecualizadas)

# Función para ecualizar el histograma de una imagen en escala de grises
def ecualizar_imagen_grises(imagen_gris):
    imagen_array = np.array(imagen_gris)
    histograma, _ = np.histogram(imagen_array, bins=256, range=(0, 255))
    cdf = histograma.cumsum()
    cdf_normalizada = cdf * 255 / cdf[-1]
    
    imagen_ecualizada = np.interp(imagen_array.flatten(), range(256), cdf_normalizada)
    imagen_ecualizada = imagen_ecualizada.reshape(imagen_array.shape).astype(np.uint8)
    
    return Image.fromarray(imagen_ecualizada)

# Función para combinar todas las imágenes en un solo archivo
def combinar_imagenes(imagen_color, imagen_color_ecualizada, imagen_grises, imagen_grises_ecualizada):
    ancho, alto = imagen_color.size
    espacio_texto = 30  # Espacio adicional para las etiquetas
    
    # Crear una nueva imagen con el doble de ancho y el doble de alto para las cuatro imágenes
    imagen_combinada = Image.new("RGB", (ancho * 2, alto * 2 + espacio_texto), "white")
    draw = ImageDraw.Draw(imagen_combinada)
    
    # Pegar cada imagen en la posición correspondiente
    imagen_combinada.paste(imagen_color, (0, 0))
    imagen_combinada.paste(imagen_color_ecualizada, (ancho, 0))
    imagen_combinada.paste(imagen_grises, (0, alto))
    imagen_combinada.paste(imagen_grises_ecualizada, (ancho, alto))
    
    # Agregar etiquetas
    etiquetas = ["Color Original", "Color Ecualizado", "Grises Original", "Grises Ecualizado"]
    posiciones = [(0, alto), (ancho, alto), (0, alto * 2), (ancho, alto * 2)]
    
    for i, (texto, (x, y)) in enumerate(zip(etiquetas, posiciones)):
        draw.text((x + (ancho - draw.textlength(texto)) // 2, y + espacio_texto), texto, fill="black")
    
    return imagen_combinada

# Ejemplo de uso
if __name__ == "__main__":
    ruta_imagen = r"C:\Users\digni\OneDrive\Desktop\tp1\aves.jpg"
    
    # Cargar la imagen en modo RGB y en escala de grises
    imagen_color = Image.open(ruta_imagen).convert("RGB")
    imagen_grises = Image.open(ruta_imagen).convert("L")
    
    # Ecualizar la imagen en color
    imagen_color_ecualizada = ecualizar_imagen_color(imagen_color)
    
    # Ecualizar la imagen en escala de grises
    imagen_grises_ecualizada = ecualizar_imagen_grises(imagen_grises)
    
    # Combinar todas las imágenes en un solo archivo
    imagen_combinada = combinar_imagenes(
        imagen_color, imagen_color_ecualizada, imagen_grises, imagen_grises_ecualizada
    )
    
    # Guardar y mostrar la imagen combinada
    imagen_combinada.save("imagen_combinada_ecualizada.jpg")
    imagen_combinada.show()
