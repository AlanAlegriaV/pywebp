import os
from tkinter import filedialog, Tk
from PIL import Image

def convertir_jpg_a_png_con_resolucion(jpg_path, png_path):
    imagen_jpg = Image.open(jpg_path)
    resolucion = imagen_jpg.info.get("dpi", (72, 72))
    imagen_jpg.save(png_path, dpi=resolucion)

def seleccionar_carpeta():
    # Abrir el diálogo para seleccionar la carpeta
    carpeta = filedialog.askdirectory()
    if carpeta:
        # Iterar sobre los archivos en la carpeta
        for filename in os.listdir(carpeta):
            if filename.endswith(".jpg") or filename.endswith(".jpeg"):
                jpg_path = os.path.join(carpeta, filename)
                png_path = os.path.join(carpeta, filename[:-4] + ".png")
                convertir_jpg_a_png_con_resolucion(jpg_path, png_path)
        print("¡Proceso completado!")

# Configurar la ventana principal de tkinter
root = Tk()
root.withdraw()  # Ocultar la ventana principal

# Llamar a la función para seleccionar la carpeta
seleccionar_carpeta()