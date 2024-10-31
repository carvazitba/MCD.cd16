from PIL import Image
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.preprocessing import StandardScaler

# Función para calcular el índice NDVI a partir de las bandas NIR y Roja
def calcular_ndvi(banda_nir, banda_roja):
    banda_nir = banda_nir.astype(np.float32)
    banda_roja = banda_roja.astype(np.float32)
    ndvi = (banda_nir - banda_roja) / (banda_nir + banda_roja + 1e-5)  # Evitar división por cero
    return ndvi

# Función para extraer características básicas de NDVI (solo el valor medio de cada región)
def extraer_caracteristicas_ndvi(region):
    mean_ndvi = np.mean(region)
    return [mean_ndvi]

# Cargar las bandas NIR y Roja para calcular el NDVI
# Asegúrate de que las rutas sean correctas y los archivos existan en esas ubicaciones
ruta_banda_nir = r"C:\Users\digni\OneDrive\Desktop\tp1\banda_nir.tif"
ruta_banda_roja = r"C:\Users\digni\OneDrive\Desktop\tp1\banda_roja.tif"

try:
    # Cargar imágenes en escala de grises (L) y convertirlas en matrices NumPy
    banda_nir = np.array(Image.open(ruta_banda_nir).convert("L"))
    banda_roja = np.array(Image.open(ruta_banda_roja).convert("L"))
    ndvi = calcular_ndvi(banda_nir, banda_roja)
except FileNotFoundError:
    print("Error: No se pudieron cargar las bandas NIR y Roja. Verifica las rutas de los archivos.")
    exit()
except Exception as e:
    print(f"Ocurrió un error al cargar las bandas: {e}")
    exit()

# Definir las coordenadas de las regiones de diferentes texturas para el entrenamiento y asignar etiquetas numéricas
etiquetas = {
    1: [(30, 30), (80, 80), (130, 130)],  # Coordenadas de las regiones para Clase 1
    2: [(180, 30), (230, 80), (280, 130)],  # Coordenadas de las regiones para Clase 2
    3: [(30, 180), (80, 230), (130, 280)]   # Coordenadas de las regiones para Clase 3
}

# Función para cortar regiones y crear conjuntos de datos para NDVI
def crear_conjunto_datos_ndvi(ndvi, etiquetas, tamaño_region=50):
    datos = []
    labels = []
    for etiqueta, coords in etiquetas.items():
        for (x, y) in coords:
            region = ndvi[y:y+tamaño_region, x:x+tamaño_region]
            if region.shape[0] == tamaño_region and region.shape[1] == tamaño_region:
                caracteristicas = extraer_caracteristicas_ndvi(region)
                datos.append(caracteristicas)
                labels.append(etiqueta)
    return np.array(datos), np.array(labels)

# Crear el conjunto de datos y etiquetas usando la imagen NDVI
datos, labels = crear_conjunto_datos_ndvi(ndvi, etiquetas)

# Dividir el conjunto de datos en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(datos, labels, test_size=0.3, random_state=42, stratify=labels)

# Escalado de las características
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Entrenar el modelo SVM con kernel RBF
modelo_svm = SVC(kernel='rbf', C=1.0)
modelo_svm.fit(X_train, y_train)

# Evaluar el modelo
y_pred = modelo_svm.predict(X_test)
print("Matriz de confusión (NDVI):\n", confusion_matrix(y_test, y_pred))
print("Reporte de clasificación (NDVI):\n", classification_report(y_test, y_pred, zero_division=0))

# Aplicar el modelo entrenado para clasificar la imagen completa de NDVI
alto, ancho = ndvi.shape
imagen_clasificada_ndvi = np.zeros((alto, ancho), dtype=np.uint8)
tamaño_region = 50  # Tamaño de la ventana para clasificación

for y in range(0, alto, tamaño_region):
    for x in range(0, ancho, tamaño_region):
        region = ndvi[y:y+tamaño_region, x:x+tamaño_region]
        if region.shape[0] == tamaño_region and region.shape[1] == tamaño_region:
            caracteristicas = extraer_caracteristicas_ndvi(region)
            caracteristicas = scaler.transform([caracteristicas])
            prediccion = modelo_svm.predict(caracteristicas)
            imagen_clasificada_ndvi[y:y+tamaño_region, x:x+tamaño_region] = int(prediccion[0] * 85)  # Escala para visualización

# Mostrar la imagen clasificada de NDVI
imagen_clasificada_ndvi = Image.fromarray(imagen_clasificada_ndvi)
imagen_clasificada_ndvi.show()
imagen_clasificada_ndvi.save("imagen_clasificada_ndvi_svm.jpg")
