from PIL import Image
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.preprocessing import StandardScaler

# Función para extraer características de textura usando estadísticas básicas
def extraer_caracteristicas_basicas(region):
    mean = np.mean(region)
    std_dev = np.std(region)
    median = np.median(region)
    max_val = np.max(region)
    min_val = np.min(region)
    return [mean, std_dev, median, max_val, min_val]

# Función para cortar regiones y crear conjuntos de datos
def crear_conjunto_datos(imagen, etiquetas, tamaño_region=50):
    datos = []
    labels = []
    for etiqueta, coords in etiquetas.items():
        for (x, y) in coords:
            region = imagen[y:y+tamaño_region, x:x+tamaño_region]
            if region.shape[0] == tamaño_region and region.shape[1] == tamaño_region:
                caracteristicas = extraer_caracteristicas_basicas(region)
                datos.append(caracteristicas)
                labels.append(etiqueta)
    return np.array(datos), np.array(labels)

# Cargar y preprocesar la imagen usando PIL
ruta_imagen = r"C:\Users\digni\OneDrive\Desktop\tp1\LC09_L2SP_226087_20241026_20241027_02_T1_thumb_large.jpeg"  # Cambia esta ruta a la ubicación de tu imagen
try:
    imagen = Image.open(ruta_imagen).convert("L")  # Convertir a escala de grises
    imagen = np.array(imagen)
except FileNotFoundError:
    print("Error: No se pudo cargar la imagen. Verifica la ruta del archivo.")
    exit()

# Definir las coordenadas de las regiones de diferentes texturas para el entrenamiento y asignar etiquetas numéricas
etiquetas = {
    1: [(30, 30), (80, 80), (130, 130)],  # Coordenadas de las regiones para Clase 1
    2: [(180, 30), (230, 80), (280, 130)],  # Coordenadas de las regiones para Clase 2
    3: [(30, 180), (80, 230), (130, 280)]   # Coordenadas de las regiones para Clase 3
}

# Crear el conjunto de datos y etiquetas
datos, labels = crear_conjunto_datos(imagen, etiquetas)

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
print("Matriz de confusión:\n", confusion_matrix(y_test, y_pred))
print("Reporte de clasificación:\n", classification_report(y_test, y_pred, zero_division=0))

# Aplicar el modelo entrenado para clasificar la imagen completa
alto, ancho = imagen.shape
imagen_clasificada = np.zeros((alto, ancho), dtype=np.uint8)
tamaño_region = 50  # Tamaño de la ventana para clasificación

for y in range(0, alto, tamaño_region):
    for x in range(0, ancho, tamaño_region):
        region = imagen[y:y+tamaño_region, x:x+tamaño_region]
        if region.shape[0] == tamaño_region and region.shape[1] == tamaño_region:
            caracteristicas = extraer_caracteristicas_basicas(region)
            caracteristicas = scaler.transform([caracteristicas])
            prediccion = modelo_svm.predict(caracteristicas)
            imagen_clasificada[y:y+tamaño_region, x:x+tamaño_region] = int(prediccion[0] * 85)  # Escala para visualización

# Mostrar la imagen clasificada
imagen_clasificada = Image.fromarray(imagen_clasificada)
imagen_clasificada.show()
imagen_clasificada.save("imagen_clasificada_svm.jpg")
