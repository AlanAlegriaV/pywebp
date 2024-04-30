import os
import tkinter as tk
from tkinter import filedialog, messagebox

def contar_archivos_ocultos(carpeta):
    cantidad_archivos_underscore = 0
    cantidad_archivos_ds_store = 0
    for ruta, directorios, archivos in os.walk(carpeta):
        for archivo in archivos:
            if archivo.startswith("._"):
                cantidad_archivos_underscore += 1
            elif archivo == ".DS_Store":
                cantidad_archivos_ds_store += 1
    return cantidad_archivos_underscore, cantidad_archivos_ds_store

def eliminar_archivos_ocultos(carpeta):
    archivos_eliminados = 0
    for ruta, directorios, archivos in os.walk(carpeta):
        for archivo in archivos:
            if archivo.startswith("._") or archivo == ".DS_Store":
                ruta_completa = os.path.join(ruta, archivo)
                os.remove(ruta_completa)
                archivos_eliminados += 1
    return archivos_eliminados

def seleccionar_carpeta():
    carpeta = filedialog.askdirectory()
    if carpeta:
        cantidad_archivos_underscore, cantidad_archivos_ds_store = contar_archivos_ocultos(carpeta)
        etiqueta_ruta.config(text=f"Ruta de la carpeta seleccionada: {carpeta}")
        etiqueta_cantidad_underscore.config(text=f"Cantidad de archivos ocultos '._' encontrados: {cantidad_archivos_underscore}")
        etiqueta_cantidad_ds_store.config(text=f"Cantidad de archivos ocultos '.DS_Store' encontrados: {cantidad_archivos_ds_store}")
        boton_eliminar.config(state=tk.NORMAL, command=lambda: eliminar_archivos(carpeta))

def eliminar_archivos(carpeta):
    archivos_eliminados = eliminar_archivos_ocultos(carpeta)
    messagebox.showinfo("Proceso Completado", f"Se han eliminado {archivos_eliminados} archivos ocultos en la carpeta y subcarpetas.")
    etiqueta_cantidad_underscore.config(text=f"Cantidad de archivos '._' encontrados: 0")
    etiqueta_cantidad_ds_store.config(text=f"Cantidad de archivos '.DS_Store' encontrados: 0")

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Eliminador de archivos ocultos MAC")

# Cargar el logo
try:
    imagen_logo = tk.PhotoImage(file="logo.png")
    etiqueta_logo = tk.Label(ventana, image=imagen_logo)
    etiqueta_logo.pack(pady=10)
except Exception as e:
    print("No se pudo cargar el logo:", e)

# Etiqueta para mostrar la ruta de la carpeta seleccionada
etiqueta_ruta = tk.Label(ventana, text="")
etiqueta_ruta.pack(pady=5)

# Etiqueta para mostrar la cantidad de archivos ._ encontrados
etiqueta_cantidad_underscore = tk.Label(ventana, text="")
etiqueta_cantidad_underscore.pack(pady=5)

# Etiqueta para mostrar la cantidad de archivos .DS_Store encontrados
etiqueta_cantidad_ds_store = tk.Label(ventana, text="")
etiqueta_cantidad_ds_store.pack(pady=5)

# Botón para seleccionar la carpeta
boton_seleccionar = tk.Button(ventana, text="Seleccionar Carpeta", command=seleccionar_carpeta)
boton_seleccionar.pack(pady=10)

# Botón para eliminar los archivos
boton_eliminar = tk.Button(ventana, text="Eliminar archivos ocultos Mac ._", state=tk.DISABLED)
boton_eliminar.pack(pady=10)

# Ejecutar el bucle de eventos
ventana.mainloop()