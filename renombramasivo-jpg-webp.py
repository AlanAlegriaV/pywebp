import os
import datetime
from PIL import Image
from tqdm import tqdm

def resize_and_convert_image(image_path, timestamp):
    with Image.open(image_path) as img:
        img = img.convert("RGB")
        new_img = Image.new("RGB", img.size, (255, 255, 255))
        new_img.paste(img, (0, 0))
        new_img = new_img.resize((1200, 1200))
        file_name, _ = os.path.splitext(image_path)
        new_file_name = f"{file_name}-{timestamp}"
        output_path = f"{new_file_name}.webp"
        new_img.save(output_path, format="WEBP", quality=95, dpi=(72, 72))

def process_folder(folder_path, timestamp, pbar):
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isdir(item_path):
            process_folder(item_path, timestamp, pbar)
        elif item.lower().endswith(".jpg"):
            resize_and_convert_image(item_path, timestamp)
            pbar.update(1)

def main():
    root_folder = input("Introduce la ruta de la carpeta a procesar: ")
    if not os.path.isdir(root_folder):
        print(f"La ruta '{root_folder}' no es una carpeta válida.")
        return

    timestamp_seconds = datetime.datetime.now().timestamp()
    timestamp = int(timestamp_seconds)

    total_files = sum(len(files) for _, _, files in os.walk(root_folder) if files)
    with tqdm(total=total_files, desc="Procesando imágenes") as pbar:
        process_folder(root_folder, timestamp, pbar)
        pbar.close()
    print("Procesamiento completado.")

main()