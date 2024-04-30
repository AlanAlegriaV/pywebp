import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image

def contar_archivos_png(carpeta):
    count = 0
    for root, dirs, files in os.walk(carpeta):
        for file in files:
            if file.endswith('.png'):
                count += 1
    return count

def convertir_png_a_jpg_con_resolucion(png_path, jpg_path):
    imagen_png = Image.open(png_path)
    resolucion = imagen_png.info.get("dpi", (72, 72))
    imagen_png.save(jpg_path, "JPEG", dpi=resolucion)

def seleccionar_carpeta():
    carpeta = filedialog.askdirectory()
    if carpeta:
        label_carpeta.config(text="Carpeta seleccionada: " + carpeta)
        lista_archivos.delete(0, tk.END)
        for root, dirs, files in os.walk(carpeta):
            for file in files:
                if file.endswith('.png'):
                    lista_archivos.insert(tk.END, os.path.join(root, file))

def convertir_png_a_jpg():
    carpeta = label_carpeta.cget("text").split(": ")[1]
    carpeta_procesada = os.path.join(carpeta, "procesado")
    os.makedirs(carpeta_procesada, exist_ok=True)
    for root, dirs, files in os.walk(carpeta):
        carpeta_rel = os.path.relpath(root, carpeta)
        carpeta_procesada_rel = os.path.join(carpeta_procesada, carpeta_rel)
        os.makedirs(carpeta_procesada_rel, exist_ok=True)
        for file in files:
            if file.endswith('.png'):
                png_path = os.path.join(root, file)
                jpg_path = os.path.join(carpeta_procesada_rel, file[:-4] + ".jpg")
                convertir_png_a_jpg_con_resolucion(png_path, jpg_path)
    print("¡Proceso completado!")

# Configurar la ventana principal de tkinter
root = tk.Tk()
root.title("Convertidor PNG a JPG")

# Crear la etiqueta para mostrar la carpeta seleccionada
label_carpeta = tk.Label(root, text="Carpeta seleccionada: ")
label_carpeta.pack()

# Crear la lista para mostrar los archivos PNG
lista_archivos = tk.Listbox(root, width=50, height=15)
lista_archivos.pack()

# Crear el botón para seleccionar la carpeta
boton_seleccionar_carpeta = tk.Button(root, text="Seleccionar carpeta", command=seleccionar_carpeta)
boton_seleccionar_carpeta.pack()

# Crear el botón para convertir los archivos PNG a JPG
boton_convertir = tk.Button(root, text="Convertir PNG a JPG", command=convertir_png_a_jpg)
boton_convertir.pack()

root.mainloop()