import os
from PIL import Image
from tqdm import tqdm

def convertir_jpg_a_png(ruta):
    # Contar la cantidad total de archivos jpg
    total_archivos_jpg = sum(1 for raiz, _, archivos in os.walk(ruta) for archivo in archivos if archivo.lower().endswith('.jpg'))

    with tqdm(total=total_archivos_jpg, desc="Conversión de imágenes") as pbar:
        # Iterar sobre los archivos y subdirectorios en la ruta proporcionada
        for raiz, directorios, archivos in os.walk(ruta):
            for archivo in archivos:
                if archivo.lower().endswith('.jpg'):
                    # Obtener la ruta completa del archivo JPG
                    ruta_jpg = os.path.join(raiz, archivo)
                    # Crear la ruta para el PNG (cambiando la extensión)
                    ruta_png = os.path.splitext(ruta_jpg)[0] + '.png'
                    try:
                        # Abrir el archivo JPG
                        imagen = Image.open(ruta_jpg)
                        # Guardar la imagen como PNG (con máxima calidad)
                        imagen.save(ruta_png, quality=95)
                        pbar.update(1)  # Incrementar la barra de progreso
                    except Exception as e:
                        print(f'Error al convertir {ruta_jpg}: {e}')

# Ruta a la carpeta principal
ruta_principal = input("Introduce la ruta de la carpeta: ")

# Llamar a la función con la ruta proporcionada
convertir_jpg_a_png(ruta_principal)