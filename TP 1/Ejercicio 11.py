from PIL import Image, ImageDraw, ImageFont
import numpy as np

# Función para agregar ruido gaussiano aditivo
def agregar_ruido_gaussiano(imagen, porcentaje, media=0, sigma=25):
    imagen_array = np.array(imagen, dtype=np.float32)
    ruido_gaussiano = np.random.normal(media, sigma, imagen_array.shape)
    mascara = np.random.rand(*imagen_array.shape[:2]) < (porcentaje / 100)
    mascara = np.repeat(mascara[:, :, np.newaxis], 3, axis=2)
    imagen_ruido = np.where(mascara, imagen_array + ruido_gaussiano, imagen_array)
    imagen_ruido = np.clip(imagen_ruido, 0, 255).astype(np.uint8)
    return Image.fromarray(imagen_ruido)

# Función para agregar ruido exponencial multiplicativo
def agregar_ruido_exponencial(imagen, porcentaje, escala=0.5):
    imagen_array = np.array(imagen, dtype=np.float32)
    ruido_exponencial = np.random.exponential(escala, imagen_array.shape)
    mascara = np.random.rand(*imagen_array.shape[:2]) < (porcentaje / 100)
    mascara = np.repeat(mascara[:, :, np.newaxis], 3, axis=2)
    imagen_ruido = np.where(mascara, imagen_array * ruido_exponencial, imagen_array)
    imagen_ruido = np.clip(imagen_ruido, 0, 255).astype(np.uint8)
    return Image.fromarray(imagen_ruido)

# Función para combinar las imágenes en un solo archivo
def combinar_imagenes(imagen_original, imagen_ruido_gaussiano, imagen_ruido_exponencial):
    ancho, alto = imagen_original.size
    imagen_combinada = Image.new("RGB", (ancho * 3, alto + 30), "white")
    draw = ImageDraw.Draw(imagen_combinada)
    font = ImageFont.load_default()

    imagen_combinada.paste(imagen_original, (0, 0))
    imagen_combinada.paste(imagen_ruido_gaussiano, (ancho, 0))
    imagen_combinada.paste(imagen_ruido_exponencial, (ancho * 2, 0))

    etiquetas = ["Original", "Ruido Gaussiano", "Ruido Exponencial"]
    posiciones = [(0, alto), (ancho, alto), (ancho * 2, alto)]

    for texto, (x, y) in zip(etiquetas, posiciones):
        text_width, _ = draw.textbbox((0, 0), texto, font=font)[2:]
        draw.text((x + (ancho - text_width) // 2, y + 5), texto, fill="black", font=font)

    return imagen_combinada

# Ejemplo de uso
if __name__ == "__main__":
    ruta_imagen = r"C:\Users\digni\OneDrive\Desktop\tp1\aves.jpg"
    imagen = Image.open(ruta_imagen).convert("RGB")
    
    # Parámetros de ruido
    porcentaje = 30  # Porcentaje de píxeles a contaminar
    
    # Generar las imágenes con ruido
    imagen_ruido_gaussiano = agregar_ruido_gaussiano(imagen, porcentaje, media=0, sigma=25)
    imagen_ruido_exponencial = agregar_ruido_exponencial(imagen, porcentaje, escala=0.5)
    
    # Combinar todas las imágenes en un solo archivo
    imagen_combinada = combinar_imagenes(imagen, imagen_ruido_gaussiano, imagen_ruido_exponencial)
    
    # Guardar y mostrar la imagen combinada
    imagen_combinada.save("imagen_con_ruido_combinada.jpg")
    imagen_combinada.show()
