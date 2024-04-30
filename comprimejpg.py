import os  # Importamos el módulo 'os' para interactuar con el sistema operativo
from tkinter import Tk, Button, Label, filedialog  # Importamos clases necesarias de tkinter para la interfaz gráfica
from PIL import Image, ImageTk  # Importamos clases necesarias de PIL para trabajar con imágenes
from tqdm import tqdm  # Importamos la clase tqdm para mostrar barras de progreso

# Variable global para almacenar la ruta de la carpeta seleccionada
folder_path = ""

# Función para comprimir una imagen dada una ruta de entrada y salida, y un tamaño objetivo en KB
def compress_image(input_path, output_path, target_size_kb):
    # Obtenemos el tamaño del archivo de entrada en bytes
    file_size = os.path.getsize(input_path)
    # Si el tamaño del archivo de entrada es mayor que el tamaño objetivo en KB
    if file_size / 1024 > target_size_kb:
        # Abrimos la imagen
        img = Image.open(input_path)
        # Comenzamos con la máxima calidad
        quality = 100
        # Iteramos para comprimir la imagen hasta alcanzar el tamaño objetivo
        while True:
            # Guardamos la imagen con la calidad actual
            img.save(output_path, optimize=True, quality=quality)
            # Obtenemos el tamaño del archivo de salida
            file_size = os.path.getsize(output_path)
            # Si el tamaño del archivo de salida es menor que el tamaño objetivo en KB o la calidad es 1 o menor, salimos del bucle
            if file_size / 1024 < target_size_kb or quality <= 1:
                break
            # Disminuimos la calidad para reducir el tamaño del archivo
            quality -= 1
    else:
        # Si el tamaño del archivo de entrada es menor que el tamaño objetivo en KB, simplemente copiamos el archivo
        with open(input_path, 'rb') as f_input:
            with open(output_path, 'wb') as f_output:
                f_output.write(f_input.read())

# Función para comprimir todas las imágenes en una carpeta dada una ruta y un tamaño objetivo en KB
def compress_images_in_folder(folder_path, target_size_kb):
    # Obtenemos todas las rutas de los archivos JPG en la carpeta y subcarpetas
    jpg_files = [os.path.join(root, file) for root, _, files in os.walk(folder_path) for file in files if file.lower().endswith('.jpg')]
    # Creamos una barra de progreso con la cantidad total de imágenes a comprimir
    progress_bar = tqdm(total=len(jpg_files), desc="Compressing images")
    # Iteramos sobre cada archivo JPG
    for file in jpg_files:
        # Generamos la ruta de salida para la imagen comprimida
        output_path = os.path.join(os.path.dirname(file), "compressed_" + os.path.basename(file))
        # Comprimimos la imagen
        compress_image(file, output_path, target_size_kb)
        # Actualizamos la barra de progreso
        progress_bar.update(1)
    # Cerramos la barra de progreso
    progress_bar.close()

# Función para seleccionar una carpeta y mostrar la cantidad de archivos JPG encontrados
def select_folder():
    global folder_path  # Accedemos a la variable global 'folder_path'
    # Abrimos un cuadro de diálogo para seleccionar una carpeta y almacenamos la ruta seleccionada
    folder_path = filedialog.askdirectory(title="Select Folder")
    # Si se seleccionó una carpeta
    if folder_path:
        # Contamos la cantidad de archivos JPG en la carpeta seleccionada
        jpg_count = count_jpg_files(folder_path)
        # Actualizamos la etiqueta con la información de la carpeta seleccionada y la cantidad de archivos JPG encontrados
        label.config(text=f"Carpeta seleccionada: {folder_path}\nArchivos JPG encontrados: {jpg_count}")

# Función para contar la cantidad de archivos JPG en una carpeta dada una ruta
def count_jpg_files(folder_path):
    jpg_count = 0
    # Recorremos la carpeta y subcarpetas para contar los archivos JPG
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith('.jpg'):
                jpg_count += 1
    return jpg_count

# Función para comprimir la carpeta seleccionada cuando se presiona el botón "Iniciar Proceso"
def compress_selected_folder():
    global folder_path  # Accedemos a la variable global 'folder_path'
    # Si se ha seleccionado una carpeta
    if folder_path:
        # Comprimimos las imágenes en la carpeta seleccionada con un tamaño objetivo de 200 KB
        compress_images_in_folder(folder_path, 200)
        # Actualizamos la etiqueta para indicar que el proceso de compresión ha finalizado
        label.config(text="Proceso de compresión completado")
    else:
        # Si no se ha seleccionado una carpeta, actualizamos la etiqueta para solicitar que se seleccione una carpeta primero
        label.config(text="Por favor, selecciona una carpeta primero")

# Crear la interfaz gráfica
root = Tk()  # Creamos una instancia de la clase Tk para la ventana principal
root.title("Image Compressor")  # Establecemos el título de la ventana
root.geometry("640x400")  # Establecemos las dimensiones de la ventana

# Agregar el logo si existe
logo_path = "logo.png"
if os.path.exists(logo_path):
    logo = Image.open(logo_path)  # Abrimos el archivo de imagen del logo
    logo_tk = ImageTk.PhotoImage(logo)  # Creamos un objeto ImageTk a partir de la imagen del logo
    logo_label = Label(root, image=logo_tk)  # Creamos una etiqueta para mostrar el logo
    logo_label.pack(pady=10)  # Añadimos la etiqueta al contenedor principal con un espacio de 10 píxeles arriba y abajo

# Creamos una etiqueta para mostrar información sobre la selección de la carpeta y la cantidad de archivos JPG
label = Label(root, text="Selecciona la carpeta con las imágenes JPG:")
label.pack(pady=10)  # Añadimos la etiqueta al contenedor principal con un espacio de 10 píxeles arriba y abajo

# Creamos un botón para seleccionar la carpeta
select_button = Button(root, text="Seleccionar Carpeta", command=select_folder)  # Creamos un botón con el texto "Seleccionar Carpeta" que al ser presionado ejecuta la función select_folder()
select_button.pack(pady=5)  # Añadimos el botón al contenedor principal con un espacio de 5 píxeles arriba y abajo

# Creamos un botón para iniciar el proceso de compresión
compress_button = Button(root, text="Iniciar Proceso", command=compress_selected_folder)  # Creamos un botón con el texto "Iniciar Proceso" que al ser presionado ejecuta la función compress_selected_folder()
compress_button.pack(pady=5)  # Añadimos el botón al contenedor principal con un espacio de 5 píxeles arriba y abajo

root.mainloop()  # Iniciamos el bucle principal de la interfaz gráfica para mostrar la ventana y esperar interacciones del usuario
