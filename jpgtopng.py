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
        # Iterar sobre los directorios y archivos dentro de la carpeta y sus subcarpetas
        for root_dir, _, files in os.walk(carpeta):
            for filename in files:
                if filename.endswith(".jpg") or filename.endswith(".jpeg"):
                    jpg_path = os.path.join(root_dir, filename)
                    png_path = os.path.join(root_dir, filename[:-4] + ".png")
                    convertir_jpg_a_png_con_resolucion(jpg_path, png_path)
        print("¡Proceso completado!")

# Configurar la ventana principal de tkinter
root = Tk()
root.withdraw()  # Ocultar la ventana principal

# Llamar a la función para seleccionar la carpeta
seleccionar_carpeta()