import os
from PIL import Image

def resize_and_convert_image(image_path, timestamp):
    # Abrir la imagen
    with Image.open(image_path) as img:
        # Convertir la imagen a RGB para evitar problemas de transparencia
        img = img.convert("RGB")
        # Crear una nueva imagen con fondo blanco
        new_img = Image.new("RGB", img.size, (255, 255, 255))
        # Pegar la imagen original en la nueva imagen
        new_img.paste(img, (0, 0))
        # Redimensionar la imagen a 1200x1200
        new_img = new_img.resize((1200, 1200))
        # Obtener la ruta y el nombre del archivo sin la extensión
        file_name, _ = os.path.splitext(image_path)
        # Crear el nuevo nombre del archivo con el timestamp
        new_file_name = f"{file_name}-{timestamp}"
        # Guardar la imagen redimensionada en formato WebP
        output_path = f"{new_file_name}.webp"
        new_img.save(output_path, format="WEBP", quality=95, dpi=(72, 72))

def process_folder(folder_path, timestamp, input_format):
    # Recorrer cada archivo y subcarpeta en la carpeta actual
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        # Si es una carpeta, procesarla recursivamente
        if os.path.isdir(item_path):
            process_folder(item_path, timestamp, input_format)
        # Si es un archivo con la extensión deseada, redimensionarlo y convertirlo
        elif item.lower().endswith(f".{input_format.lower()}"):
            resize_and_convert_image(item_path, timestamp)

def main():
    # Solicitar al usuario que ingrese la ruta de la carpeta
    root_folder = input("Ingrese la ruta de la carpeta: ")
    # Verificar que la ruta sea una carpeta válida
    if not os.path.isdir(root_folder):
        print(f"La ruta '{root_folder}' no es una carpeta válida.")
        return

    # Solicitar al usuario que ingrese la opción para el formato de imagen de entrada
    option = input("¿La imagen de entrada es PNG (Opción 1) o JPG (Opción 2)? Ingrese '1' o '2': ")
    if option == "1":
        input_format = "PNG"
    elif option == "2":
        input_format = "JPG"
    else:
        print("Opción no válida.")
        return

    # Solicitar al usuario que ingrese un timestamp
    timestamp = input("Ingrese un timestamp: ")

    # Procesar la carpeta raíz y sus subcarpetas
    process_folder(root_folder, timestamp, input_format)
    print("Procesamiento completado.")

# Llamar directamente a la función principal
main()
