import tkinter as tk  # Importar la biblioteca tkinter para crear la interfaz gráfica
from tkinter import filedialog  # Importar filedialog de tkinter para manejar diálogos de archivo
import pandas as pd  # Importar la biblioteca pandas para trabajar con datos de Excel
import os  # Importar la biblioteca os para operaciones de sistema

# Función para seleccionar una carpeta
def select_folder():
    folder_path = filedialog.askdirectory()  # Mostrar un diálogo para seleccionar una carpeta
    folder_entry.delete(0, tk.END)  # Limpiar el widget de entrada de la carpeta
    folder_entry.insert(0, folder_path)  # Insertar la ruta de la carpeta seleccionada en el widget de entrada

# Función para seleccionar un archivo Excel
def select_excel_file():
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])  # Mostrar un diálogo para seleccionar un archivo Excel
    file_entry.delete(0, tk.END)  # Limpiar el widget de entrada del archivo Excel
    file_entry.insert(0, file_path)  # Insertar la ruta del archivo Excel seleccionado en el widget de entrada

# Función para iniciar el proceso de creación de carpetas
def start_process():
    folder_path = folder_entry.get()  # Obtener la ruta de la carpeta seleccionada desde el widget de entrada
    file_path = file_entry.get()  # Obtener la ruta del archivo Excel seleccionado desde el widget de entrada

    if folder_path and file_path:  # Verificar si se han seleccionado una carpeta y un archivo Excel
        df = pd.read_excel(file_path)  # Leer el archivo Excel y cargar los datos en un DataFrame de pandas

        for index, row in df.iterrows():  # Iterar sobre cada fila del DataFrame
            folder_name = str(row.iloc[0])  # Obtener el nombre de la carpeta de la primera columna de la fila actual
            folder_path = folder_entry.get()  # Obtener la ruta de la carpeta seleccionada desde el widget de entrada
            folder_path = os.path.join(folder_path, folder_name)  # Crear la ruta completa de la nueva carpeta
            os.makedirs(folder_path, exist_ok=True)  # Crear la carpeta (si no existe) en la ruta especificada

        status_label.config(text="Proceso completado: se han creado las carpetas.")  # Actualizar el mensaje de estado
    else:
        status_label.config(text="Por favor, selecciona una carpeta y un archivo Excel.")  # Indicar al usuario que seleccione una carpeta y un archivo Excel

# Crear la ventana principal
root = tk.Tk()  # Crear una instancia de la clase Tk de tkinter
root.title("Programa de Creación de Carpetas")  # Establecer el título de la ventana

# Agregar el logo
logo_image = tk.PhotoImage(file="logo.png")  # Cargar la imagen desde el archivo "logo.png"
logo_label = tk.Label(root, image=logo_image)  # Crear un widget de etiqueta para mostrar la imagen
logo_label.grid(row=0, column=0, columnspan=3, padx=10, pady=5)  # Colocar el widget de etiqueta en la ventana

# Crear los widgets de la interfaz gráfica
folder_label = tk.Label(root, text="Selecciona una carpeta:")  # Crear una etiqueta para indicar la selección de la carpeta
folder_label.grid(row=1, column=0, padx=10, pady=5)  # Colocar la etiqueta en la ventana

folder_entry = tk.Entry(root, width=50)  # Crear un widget de entrada para mostrar la ruta de la carpeta seleccionada
folder_entry.grid(row=1, column=1, padx=10, pady=5)  # Colocar el widget de entrada en la ventana

folder_button = tk.Button(root, text="Seleccionar Carpeta", command=select_folder)  # Crear un botón para seleccionar una carpeta
folder_button.grid(row=1, column=2, padx=10, pady=5)  # Colocar el botón en la ventana

file_label = tk.Label(root, text="Selecciona un archivo Excel:")  # Crear una etiqueta para indicar la selección del archivo Excel
file_label.grid(row=2, column=0, padx=10, pady=5)  # Colocar la etiqueta en la ventana

file_entry = tk.Entry(root, width=50)  # Crear un widget de entrada para mostrar la ruta del archivo Excel seleccionado
file_entry.grid(row=2, column=1, padx=10, pady=5)  # Colocar el widget de entrada en la ventana

file_button = tk.Button(root, text="Seleccionar Archivo", command=select_excel_file)  # Crear un botón para seleccionar un archivo Excel
file_button.grid(row=2, column=2, padx=10, pady=5)  # Colocar el botón en la ventana

start_button = tk.Button(root, text="Iniciar Proceso", command=start_process)  # Crear un botón para iniciar el proceso de creación de carpetas
start_button.grid(row=3, column=1, padx=10, pady=5)  # Colocar el botón en la ventana

status_label = tk.Label(root, text="")  # Crear una etiqueta para mostrar el estado del proceso
status_label.grid(row=4, column=0, columnspan=3, padx=10, pady=5)  # Colocar la etiqueta en la ventana

# Ejecutar la aplicación
root.mainloop()  # Iniciar el bucle principal de la aplicación