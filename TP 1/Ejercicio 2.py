# 2. Implementar un programa que realice las siguientes operaciones con im´agenes en diferentes formatos (raw, pgm, ppm, jpg) y una imagen satelital ´optica:

# Cargamos la libreria PIL (Python Imaging Library) la cual nos permite trabajar con imagenes

from PIL import Image

# Ahora se definen las funciones a utilizar.

# a) Cargar una imagen de un archivo y desplegarla.
def cargar_imagen(ruta_archivo):
    imagen = Image.open(ruta_archivo)
    imagen.show()  # Despliega la imagen
    return imagen

# b) Guardar una imagen a un archivo.
def guardar_imagen(imagen, ruta_guardado):
    imagen.save(ruta_guardado)
    print(f"Imagen guardada en {ruta_guardado}")

# c) Obtener el valor de un píxel en una imagen.
def valor_pixel(imagen, x, y):
    pixel = imagen.getpixel((x, y))
    print(f"Valor del píxel en ({x}, {y}): {pixel}")
    return pixel

# d) Copiar una parte de la imagen en otra imagen nueva.
def copiar_region(imagen, caja):
    region = imagen.crop(caja)  # Define la región de la imagen (x1, y1, x2, y2)
    return region

# e) Guardar la imagen cortada con otro nombre.
def guardar_region(region, ruta_guardado):
    region.save(ruta_guardado)
    print(f"Imagen cortada guardada en {ruta_guardado}")

# Resolucion del item 2
if __name__ == "__main__":
    ruta_imagen = r"C:\Users\digni\OneDrive\Desktop\tp1\LC09_L2SP_226087_20241026_20241027_02_T1_thumb_large.jpeg"
    imagen = cargar_imagen(ruta_imagen)
    
    # Guardar la imagen en un nuevo archivo
    guardar_imagen(imagen, "nueva_imagen.jpg")
    
    # Obtener el valor de un píxel específico
    valor_pixel(imagen, 50, 50)  # Cambia (50, 50) por las coordenadas deseadas
    
    # Copiar una región de la imagen (definir la caja como (x1, y1, x2, y2))
    region = copiar_region(imagen, (100, 100, 400, 400))
    region.show()  # Despliega la región copiada
    
    # Guardar la región copiada con un nuevo nombre
    guardar_region(region, "region_copiada.jpg")
