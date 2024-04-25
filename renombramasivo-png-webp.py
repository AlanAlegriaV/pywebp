import os
import datetime
from PIL import Image
from tkinter import Tk, Button, Label, filedialog
from tkinter import PhotoImage  # Necesario para cargar imágenes
from tqdm import tqdm
import shutil

def resize_and_convert_image(image_path, timestamp, output_folder):
    with Image.open(image_path) as img:
        img = img.convert("RGB")
        new_img = Image.new("RGB", img.size, (255, 255, 255))
        new_img.paste(img, (0, 0))
        new_img = new_img.resize((1200, 1200))
        file_name, _ = os.path.splitext(os.path.basename(image_path))
        new_file_name = f"{file_name}-{timestamp}.webp"
        output_path = os.path.join(output_folder, new_file_name)
        new_img.save(output_path, format="WEBP", quality=100, dpi=(72, 72))

def count_files_and_folders(folder_path):
    total_png_files = 0
    total_folders = 0

    for root, dirs, files in os.walk(folder_path):
        total_folders += len(dirs)  # Count folders
        for file in files:
            if file.lower().endswith('.png'):
                total_png_files += 1

    return total_png_files, total_folders

def process_folder(folder_path, output_folder, timestamp, pbar):
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isdir(item_path):
            # No procesar la carpeta "Procesado" para evitar bucles infinitos
            if item == "Procesado":
                continue
            # Crear la misma estructura de carpetas en la carpeta Procesado
            new_output_folder = os.path.join(output_folder, item)
            os.makedirs(new_output_folder, exist_ok=True)
            process_folder(item_path, new_output_folder, timestamp, pbar)
        elif item.lower().endswith(".png"):
            resize_and_convert_image(item_path, timestamp, output_folder)
            pbar.update(1)

def start_processing():
    root_folder = folder_path_label.cget("text")
    if not os.path.isdir(root_folder):
        print(f"La ruta '{root_folder}' no es una carpeta válida.")
        return

    num_png_files, num_folders = count_files_and_folders(root_folder)
    png_count_label.config(text=f"Archivos PNG: {num_png_files}")
    folders_count_label.config(text=f"Carpetas: {num_folders}")

    timestamp_seconds = datetime.datetime.now().timestamp()
    timestamp = int(timestamp_seconds)

    output_folder = os.path.join(root_folder, "Procesado")
    os.makedirs(output_folder, exist_ok=True)

    total_files = num_png_files
    with tqdm(total=total_files, desc="Procesando imágenes") as pbar:
        process_folder(root_folder, output_folder, timestamp, pbar)
        pbar.close()
    print("Procesamiento completado.")

def browse_folder():
    folder_selected = filedialog.askdirectory()
    folder_path_label.config(text=folder_selected)
    num_png_files, num_folders = count_files_and_folders(folder_selected)
    png_count_label.config(text=f"Archivos PNG: {num_png_files}")
    folders_count_label.config(text=f"Carpetas: {num_folders}")

# GUI setup
root = Tk()
root.title("Procesador de Imágenes")
root.geometry("640x400")

# Cargar la imagen que deseas mostrar
img = PhotoImage(file="./logo.png")  # Cambia "ruta_de_la_imagen.png" por la ruta de tu imagen
image_label = Label(root, image=img)
image_label.image = img  # Mantiene una referencia para evitar que la imagen sea eliminada por el recolector de basura
image_label.pack(pady=5, padx=5, side="top", anchor="n")  # Alinear arriba (norte)

folder_path_label = Label(root, text="Selecciona una carpeta")
folder_path_label.pack(pady=10)

browse_button = Button(root, text="Seleccionar Carpeta", command=browse_folder)
browse_button.pack(pady=5)

png_count_label = Label(root, text="Archivos PNG: 0")
png_count_label.pack(pady=5)

folders_count_label = Label(root, text="Carpetas: 0")
folders_count_label.pack(pady=5)

start_button = Button(root, text="Iniciar Proceso", command=start_processing, bg="lightblue")
start_button.pack(pady=5)

root.mainloop()