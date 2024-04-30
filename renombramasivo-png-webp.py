import os  # Importar el módulo os para interactuar con el sistema operativo
import datetime  # Importar el módulo datetime para trabajar con fechas y horas
from PIL import Image  # Importar la clase Image de PIL para manipular imágenes
from tkinter import Tk, Button, Label, filedialog  # Importar clases de Tkinter para la interfaz gráfica
from tkinter import PhotoImage  # Importar PhotoImage para cargar imágenes en Tkinter
from tqdm import tqdm  # Importar la clase tqdm para mostrar barras de progreso
import shutil  # Importar shutil para operaciones de archivo de alto nivel

# Función para redimensionar y convertir una imagen a WebP
def resize_and_convert_image(image_path, timestamp, output_folder):
    with Image.open(image_path) as img:  # Abrir la imagen
        img = img.convert("RGB")  # Convertir a RGB
        new_img = Image.new("RGB", img.size, (255, 255, 255))  # Crear una nueva imagen RGB blanca
        new_img.paste(img, (0, 0))  # Pegar la imagen original en la nueva imagen
        new_img = new_img.resize((1200, 1200))  # Redimensionar la imagen a 1200x1200 píxeles
        file_name, _ = os.path.splitext(os.path.basename(image_path))  # Obtener el nombre del archivo sin extensión
        new_file_name = f"{file_name}-{timestamp}.webp"  # Construir el nuevo nombre de archivo con la marca de tiempo
        output_path = os.path.join(output_folder, new_file_name)  # Construir la ruta de salida
        new_img.save(output_path, format="WEBP", quality=100, dpi=(72, 72))  # Guardar la imagen en formato WebP

# Función para contar archivos y carpetas en una ruta dada
def count_files_and_folders(folder_path):
    total_png_files = 0  # Contador de archivos PNG
    total_folders = 0  # Contador de carpetas

    # Recorrer la estructura de carpetas y archivos
    for root, dirs, files in os.walk(folder_path):
        total_folders += len(dirs)  # Contar carpetas
        for file in files:
            if file.lower().endswith('.png'):  # Verificar si el archivo es PNG
                total_png_files += 1  # Incrementar el contador de archivos PNG

    return total_png_files, total_folders  # Devolver el total de archivos PNG y carpetas

# Función para procesar una carpeta y sus subcarpetas
def process_folder(folder_path, output_folder, timestamp, pbar):
    for item in os.listdir(folder_path):  # Iterar sobre los elementos de la carpeta
        item_path = os.path.join(folder_path, item)  # Obtener la ruta completa del elemento
        if os.path.isdir(item_path):  # Verificar si es una carpeta
            if item == "Procesado":  # Evitar bucles infinitos procesando la carpeta "Procesado"
                continue
            new_output_folder = os.path.join(output_folder, item)  # Construir la ruta de la nueva carpeta de salida
            os.makedirs(new_output_folder, exist_ok=True)  # Crear la carpeta de salida
            process_folder(item_path, new_output_folder, timestamp, pbar)  # Llamar recursivamente a la función para procesar la subcarpeta
        elif item.lower().endswith(".png"):  # Verificar si es un archivo PNG
            resize_and_convert_image(item_path, timestamp, output_folder)  # Redimensionar y convertir la imagen a WebP
            pbar.update(1)  # Actualizar la barra de progreso

# Función para iniciar el procesamiento de la carpeta seleccionada
def start_processing():
    root_folder = folder_path_label.cget("text")  # Obtener la ruta de la carpeta seleccionada
    if not os.path.isdir(root_folder):  # Verificar si la ruta es una carpeta válida
        print(f"La ruta '{root_folder}' no es una carpeta válida.")  # Imprimir un mensaje de error
        return

    num_png_files, num_folders = count_files_and_folders(root_folder)  # Contar archivos PNG y carpetas en la carpeta seleccionada
    png_count_label.config(text=f"Archivos PNG: {num_png_files}")  # Actualizar la etiqueta con la cantidad de archivos PNG
    folders_count_label.config(text=f"Carpetas: {num_folders}")  # Actualizar la etiqueta con la cantidad de carpetas

    timestamp_seconds = datetime.datetime.now().timestamp()  # Obtener la marca de tiempo actual en segundos
    timestamp = int(timestamp_seconds)  # Convertir la marca de tiempo a un entero

    output_folder = os.path.join(root_folder, "Procesado")  # Carpeta de salida para las imágenes procesadas
    os.makedirs(output_folder, exist_ok=True)  # Crear la carpeta de salida si no existe

    total_files = num_png_files  # Total de archivos a procesar
    with tqdm(total=total_files, desc="Procesando imágenes") as pbar:  # Inicializar la barra de progreso
        process_folder(root_folder, output_folder, timestamp, pbar)  # Procesar la carpeta y subcarpetas
        pbar.close()  # Cerrar la barra de progreso
    print("Procesamiento completado.")  # Imprimir un mensaje de éxito

# Función para seleccionar una carpeta
def browse_folder():
    folder_selected = filedialog.askdirectory()  # Mostrar un cuadro de diálogo para seleccionar una carpeta
    folder_path_label.config(text=folder_selected)  # Actualizar la etiqueta con la ruta de la carpeta seleccionada
    num_png_files, num_folders = count_files_and_folders(folder_selected)  # Contar archivos PNG y carpetas en la carpeta seleccionada
    png_count_label.config(text=f"Archivos PNG: {num_png_files}")  # Actualizar la etiqueta con la cantidad de archivos PNG
    folders_count_label.config(text=f"Carpetas: {num_folders}")  # Actualizar la etiqueta con la cantidad de carpetas

# Configuración de la interfaz gráfica
root = Tk()  # Crear una instancia de la clase Tk para la ventana principal
root.title("Procesador de Imágenes")  # Establecer el título de la ventana
root.geometry("640x400")  # Establecer las dimensiones de la ventana

img = PhotoImage(file="./logo.png")  # Cargar la imagen del logo
image_label = Label(root, image=img)  # Crear una etiqueta para mostrar la imagen del logo
image_label.image = img  # Mantener una referencia a la imagen para evitar que sea eliminada por el recolector de basura
image_label.pack(pady=5, padx=5, side="top", anchor="n")  # Alinear la etiqueta en la parte superior

folder_path_label = Label(root, text="Selecciona una carpeta")  # Crear una etiqueta para mostrar la ruta de la carpeta seleccionada
folder_path_label.pack(pady=10)  # Añadir la etiqueta al contenedor principal con un espacio de 10 píxeles arriba y abajo

browse_button = Button(root, text="Seleccionar Carpeta", command=browse_folder)  # Crear un botón para seleccionar una carpeta
browse_button.pack(pady=5)  # Añadir el botón al contenedor principal con un espacio de 5 píxeles arriba y abajo

png_count_label = Label(root, text="Archivos PNG: 0")  # Crear una etiqueta para mostrar la cantidad de archivos PNG
png_count_label.pack(pady=5)  # Añadir la etiqueta al contenedor principal con un espacio de 5 píxeles arriba y abajo

folders_count_label = Label(root, text="Carpetas: 0")  # Crear una etiqueta para mostrar la cantidad de carpetas
folders_count_label.pack(pady=5)  # Añadir la etiqueta al contenedor principal con un espacio de 5 píxeles arriba y abajo

start_button = Button(root, text="Iniciar Proceso", command=start_processing, bg="lightblue")  # Crear un botón para iniciar el proceso de procesamiento de imágenes
start_button.pack(pady=5)  # Añadir el botón al contenedor principal con un espacio de 5 píxeles arriba y abajo

root.mainloop()  # Iniciar el bucle principal de la interfaz gráfica