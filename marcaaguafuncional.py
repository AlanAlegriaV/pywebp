import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image
from tkinter import ttk

# Variables globales para almacenar las rutas de la imagen de marca de agua y la carpeta de imágenes
marca_de_agua_path = ""
carpeta_imagenes = ""

def superponer_marca_de_agua(imagen_principal_path, output_path, margen_superior=10, margen_izquierdo=10):
    global marca_de_agua_path
    
    # Abrir la imagen principal (JPEG)
    imagen_principal = Image.open(imagen_principal_path).convert("RGB")

    # Abrir la marca de agua (PNG)
    marca_de_agua = Image.open(marca_de_agua_path).convert("RGBA")

    # Obtener las dimensiones de la imagen principal
    ancho_principal, alto_principal = imagen_principal.size

    # Calcular la posición donde se pegará la marca de agua
    posicion = (margen_izquierdo, margen_superior)

    # Superponer la marca de agua
    imagen_principal.paste(marca_de_agua, posicion, marca_de_agua)

    # Guardar la imagen resultante en la carpeta "procesado"
    output_folder = os.path.join(os.path.dirname(output_path), "procesado")
    os.makedirs(output_folder, exist_ok=True)  # Verificar si la carpeta ya existe antes de crearla
    output_file = os.path.join(output_folder, os.path.basename(output_path))
    imagen_principal.save(output_file, "JPEG")

def seleccionar_imagen_marca_de_agua():
    global marca_de_agua_path
    
    # Abrir el diálogo para seleccionar la imagen de marca de agua
    marca_de_agua_path = filedialog.askopenfilename(title="Selecciona la imagen de marca de agua",
                                                    filetypes=[("Imágenes", "*.png;*.jpg;*.jpeg")])

def seleccionar_carpeta_imagenes():
    global carpeta_imagenes
    
    # Abrir el diálogo para seleccionar la carpeta que contiene las imágenes JPEG
    carpeta_imagenes = filedialog.askdirectory(title="Selecciona la carpeta con las imágenes JPEG")

def iniciar_proceso():
    global marca_de_agua_path, carpeta_imagenes
    
    if marca_de_agua_path and carpeta_imagenes:
        # Contar la cantidad de imágenes en la carpeta
        num_imagenes = len([filename for filename in os.listdir(carpeta_imagenes) if filename.endswith(".jpg") or filename.endswith(".jpeg")])

        # Barra de progreso
        progress_bar["maximum"] = num_imagenes

        # Crear la carpeta "procesado" si no existe
        output_folder = os.path.join(carpeta_imagenes, "procesado")
        os.makedirs(output_folder, exist_ok=True)

        # Iterar sobre las imágenes en la carpeta y superponer la marca de agua
        for i, filename in enumerate(os.listdir(carpeta_imagenes)):
            if filename.endswith(".jpg") or filename.endswith(".jpeg"):
                imagen_principal_path = os.path.join(carpeta_imagenes, filename)
                output_path = os.path.join(output_folder, filename)
                superponer_marca_de_agua(imagen_principal_path, output_path, margen_superior=10, margen_izquierdo=10)
                # Actualizar la barra de progreso
                progress_bar["value"] = i + 1
                root.update()

        # Mostrar mensaje de proceso completado
        tk.messagebox.showinfo("Proceso completado", "¡Proceso completado!")
    else:
        # Mostrar un mensaje si falta seleccionar la imagen de marca de agua o la carpeta de imágenes
        tk.messagebox.showwarning("Advertencia", "Por favor, selecciona la imagen de marca de agua y la carpeta de imágenes.")

# Crear la ventana principal
root = tk.Tk()
root.title("Aplicación para superponer marca de agua")

# Botón para seleccionar la imagen de marca de agua
btn_seleccionar_marca_de_agua = tk.Button(root, text="Seleccionar imagen de marca de agua", command=seleccionar_imagen_marca_de_agua)
btn_seleccionar_marca_de_agua.pack(pady=10)

# Botón para seleccionar la carpeta de imágenes
btn_seleccionar_carpeta_imagenes = tk.Button(root, text="Seleccionar carpeta de imágenes", command=seleccionar_carpeta_imagenes)
btn_seleccionar_carpeta_imagenes.pack(pady=10)

# Botón para iniciar el proceso
btn_iniciar_proceso = tk.Button(root, text="Iniciar proceso", command=iniciar_proceso)
btn_iniciar_proceso.pack(pady=10)

# Barra de progreso
progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
progress_bar.pack(pady=10)

# Ejecutar la ventana principal
root.mainloop()