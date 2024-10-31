from PIL import Image

# Cargar imagen
def cargar_imagen(ruta_archivo):
    return Image.open(ruta_archivo)

# Marcar región y obtener estadísticas
def analizar_region(imagen, caja):
    # Recortar la región definida por la caja (x1, y1, x2, y2)
    region = imagen.crop(caja)
    
    # Contar los píxeles en la región
    num_pixels = region.size[0] * region.size[1]

    # Calcular el promedio de niveles de gris o color
    if imagen.mode == "RGB":
        # Si es una imagen en color, calcular promedio de cada canal (R, G, B)
        r_total, g_total, b_total = 0, 0, 0
        for pixel in region.getdata():
            r_total += pixel[0]
            g_total += pixel[1]
            b_total += pixel[2]
        avg_r = r_total / num_pixels
        avg_g = g_total / num_pixels
        avg_b = b_total / num_pixels
        print(f"Promedio de color en la región - R: {avg_r}, G: {avg_g}, B: {avg_b}")
    else:
        # Si es una imagen en escala de grises
        total_gray = sum(region.getdata())
        avg_gray = total_gray / num_pixels
        print(f"Promedio de nivel de gris en la región: {avg_gray}")
    
    print(f"Cantidad de píxeles en la región: {num_pixels}")
    return region

# Ejemplo de uso
if __name__ == "__main__":
    ruta_imagen = r"C:\Users\digni\OneDrive\Desktop\tp1\LC09_L2SP_226087_20241026_20241027_02_T1_thumb_large.jpeg"
    imagen = cargar_imagen(ruta_imagen)
    
    # Define la caja de la región a analizar (x1, y1, x2, y2)
    caja = (100, 100, 400, 400)
    region = analizar_region(imagen, caja)
    
    # Mostrar la región seleccionada
    region.show()
