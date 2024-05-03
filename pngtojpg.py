import os
from tkinter import filedialog, Tk
from PIL import Image

def convertir_png_a_jpg_con_resolucion(png_path, jpg_path):
    imagen_png = Image.open(png_path)
    resolucion = imagen_png.info.get("dpi", (72, 72))
    imagen_png.save(jpg_path, dpi=resolucion)

def seleccionar_carpeta():
    # Abrir el diálogo para seleccionar la carpeta
    carpeta = filedialog.askdirectory()
    if carpeta:
        # Iterar sobre los directorios y archivos dentro de la carpeta y sus subcarpetas
        for root_dir, _, files in os.walk(carpeta):
            for filename in files:
                if filename.endswith(".png"):
                    png_path = os.path.join(root_dir, filename)
                    jpg_path = os.path.join(root_dir, filename[:-4] + ".jpg")
                    convertir_png_a_jpg_con_resolucion(png_path, jpg_path)
        print("¡Proceso completado!")

# Configurar la ventana principal de tkinter
root = Tk()
root.withdraw()  # Ocultar la ventana principal

# Llamar a la función para seleccionar la carpeta
seleccionar_carpeta()