from PIL import Image, ImageOps, ImageDraw, ImageFont
import numpy as np

# Función para ecualizar el histograma de cada banda en una imagen en color
def ecualizar_imagen_color(imagen):
    bandas = imagen.split()
    bandas_ecualizadas = []
    
    for banda in bandas:
        banda_array = np.array(banda)
        histograma, _ = np.histogram(banda_array, bins=256, range=(0, 255))
        cdf = histograma.cumsum()  # Función de distribución acumulada (CDF)
        cdf_normalizada = cdf * 255 / cdf[-1]  # Normalizar la CDF
        banda_ecualizada = np.interp(banda_array.flatten(), range(256), cdf_normalizada)
        banda_ecualizada = banda_ecualizada.reshape(banda_array.shape).astype(np.uint8)
        bandas_ecualizadas.append(Image.fromarray(banda_ecualizada))
    
    return Image.merge("RGB", bandas_ecualizadas)

# Función para ecualizar el histograma de una imagen en escala de grises
def ecualizar_imagen_grises(imagen_gris):
    imagen_array = np.array(imagen_gris)
    histograma, _ = np.histogram(imagen_array, bins=256, range=(0, 255))
    cdf = histograma.cumsum()  # CDF
    cdf_normalizada = cdf * 255 / cdf[-1]  # Normalizar la CDF
    imagen_ecualizada = np.interp(imagen_array.flatten(), range(256), cdf_normalizada)
    imagen_ecualizada = imagen_ecualizada.reshape(imagen_array.shape).astype(np.uint8)
    
    return Image.fromarray(imagen_ecualizada)

# Función para combinar todas las imágenes en un solo archivo
def combinar_imagenes_en_un_archivo(imagen_color, imagen_color_ecualizada_primera, imagen_color_ecualizada_segunda,
                                    imagen_grises, imagen_grises_ecualizada_primera, imagen_grises_ecualizada_segunda):
    ancho, alto = imagen_color.size
    espacio_texto = 30  # Espacio para etiquetas

    # Crear una nueva imagen con el doble de alto y ancho para acomodar las seis imágenes
    imagen_combinada = Image.new("RGB", (ancho * 3, alto * 2 + espacio_texto), "white")
    draw = ImageDraw.Draw(imagen_combinada)
    font = ImageFont.load_default()

    # Pegar las imágenes en la combinación final
    imagen_combinada.paste(imagen_color, (0, 0))
    imagen_combinada.paste(imagen_color_ecualizada_primera, (ancho, 0))
    imagen_combinada.paste(imagen_color_ecualizada_segunda, (ancho * 2, 0))
    imagen_combinada.paste(imagen_grises, (0, alto))
    imagen_combinada.paste(imagen_grises_ecualizada_primera, (ancho, alto))
    imagen_combinada.paste(imagen_grises_ecualizada_segunda, (ancho * 2, alto))

    # Etiquetas
    etiquetas = ["Color Original", "Color Ecualización 1", "Color Ecualización 2",
                 "Grises Original", "Grises Ecualización 1", "Grises Ecualización 2"]
    posiciones = [(0, alto), (ancho, alto), (ancho * 2, alto),
                  (0, alto * 2), (ancho, alto * 2), (ancho * 2, alto * 2)]

    for (texto, (x, y)) in zip(etiquetas, posiciones):
        text_bbox = draw.textbbox((0, 0), texto, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        draw.text((x + (ancho - text_width) // 2, y + espacio_texto), texto, fill="black", font=font)

    return imagen_combinada

# Ejemplo de uso
if __name__ == "__main__":
    ruta_imagen = r"C:\Users\digni\OneDrive\Desktop\tp1\aves.jpg"
    
    # Cargar la imagen en modo RGB y en escala de grises
    imagen_color = Image.open(ruta_imagen).convert("RGB")
    imagen_grises = Image.open(ruta_imagen).convert("L")
    
    # Aplicar la ecualización una vez en color y en grises
    imagen_color_ecualizada_primera = ecualizar_imagen_color(imagen_color)
    imagen_grises_ecualizada_primera = ecualizar_imagen_grises(imagen_grises)
    
    # Aplicar la ecualización por segunda vez
    imagen_color_ecualizada_segunda = ecualizar_imagen_color(imagen_color_ecualizada_primera)
    imagen_grises_ecualizada_segunda = ecualizar_imagen_grises(imagen_grises_ecualizada_primera)
    
    # Combinar todas las imágenes en un solo archivo
    imagen_combinada = combinar_imagenes_en_un_archivo(
        imagen_color, imagen_color_ecualizada_primera, imagen_color_ecualizada_segunda,
        imagen_grises, imagen_grises_ecualizada_primera, imagen_grises_ecualizada_segunda
    )
    
    # Guardar y mostrar la imagen combinada
    imagen_combinada.save("imagen_combinada_ecualizacion_doble.jpg")
    imagen_combinada.show()
