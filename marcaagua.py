# Importar las bibliotecas necesarias
from tkinter import Tk, Button, Label, filedialog, Scale, messagebox, PhotoImage, Frame, StringVar
import os
from PIL import Image, ImageTk
from tkinter.ttk import Progressbar
import time

# Definir la clase de la aplicación
class AplicacionMarcaDeAgua:
    # Método constructor para inicializar la aplicación
    def __init__(self, ventana):
        # Asignar la ventana principal a la variable de instancia
        self.ventana = ventana
        # Establecer el título y las dimensiones de la ventana
        self.ventana.title("Aplicación de Marca de Agua")
        self.ventana.geometry("1200x600")  

        # Cargar el logo y mostrarlo en la ventana
        self.logo = PhotoImage(file="./logo.png")
        self.logo_label = Label(ventana, image=self.logo)
        self.logo_label.image = self.logo  
        self.logo_label.grid(row=0, column=0, pady=5, padx=5, sticky="n")  

        # Variables para almacenar las rutas de las imágenes
        self.ruta_marca_de_agua = ''
        self.ruta_carpeta_imagenes = ''

        # Variables para controlar el margen y el tamaño de la marca de agua
        self.margen_superior = Scale(ventana, from_=0, to=100, orient='horizontal', label="Margen Superior", command=self.actualizar_previsualizacion)
        self.margen_izquierdo = Scale(ventana, from_=0, to=100, orient='horizontal', label="Margen Izquierdo", command=self.actualizar_previsualizacion)
        self.tamano_marca_de_agua = Scale(ventana, from_=0, to=400, orient='horizontal', label="Tamaño de la Marca de Agua", command=self.actualizar_previsualizacion)
        self.tamano_marca_de_agua.set(100)  # Establecer el tamaño inicial de la marca de agua

        # Variables StringVar para mostrar las rutas de las imágenes
        self.path_marca_de_agua = StringVar()
        self.path_carpeta_imagenes = StringVar()

        # Botones para seleccionar las imágenes
        self.boton_seleccionar_marca_de_agua = Button(ventana, text="Seleccionar Imagen de Marca de Agua", command=self.seleccionar_marca_de_agua)
        self.boton_seleccionar_marca_de_agua.grid(row=1, column=0, pady=5, padx=5, sticky="n")
        self.boton_seleccionar_carpeta_imagenes = Button(ventana, text="Seleccionar Carpeta de Imágenes", command=self.seleccionar_carpeta_imagenes, state='disabled')
        self.boton_seleccionar_carpeta_imagenes.grid(row=2, column=0, pady=5, padx=5, sticky="n")

        # Colocar sliders para el margen y el tamaño de la marca de agua
        self.margen_superior.grid(row=5, column=0, pady=5, padx=5, sticky="n")
        self.margen_izquierdo.grid(row=6, column=0, pady=5, padx=5, sticky="n")
        self.tamano_marca_de_agua.grid(row=7, column=0, pady=5, padx=5, sticky="n")

        # Botón para aplicar la marca de agua a las imágenes
        Button(ventana, text="Aplicar Marca de Agua", command=self.aplicar_marca_de_agua).grid(row=8, column=0, pady=5, padx=5, sticky="n")

        # Barra de progreso
        self.barra_progreso = Progressbar(ventana, orient="horizontal", length=200, mode="determinate")
        self.barra_progreso.grid(row=9, column=0, pady=5, padx=5, sticky="n")

        # Crear un marco para la previsualización de la imagen
        self.previsualizacion_frame = Frame(ventana, width=550, height=550, bd=2, relief="solid")
        self.previsualizacion_frame.grid(row=0, column=1, rowspan=10, pady=5, padx=5, sticky="nsew")
        self.previsualizacion_frame.grid_propagate(False)  # Evitar que el marco cambie de tamaño

        # Etiqueta para la imagen de previsualización
        self.previsualizacion = Label(self.previsualizacion_frame)
        self.previsualizacion.pack(fill="both", expand=True)

    # Método para seleccionar la imagen de marca de agua
    def seleccionar_marca_de_agua(self):
        # Solicitar al usuario que seleccione una imagen y almacenar la ruta seleccionada
        self.ruta_marca_de_agua = filedialog.askopenfilename(filetypes=[("Imagen", "*.jpg;*.jpeg;*.png")])
        # Verificar si se ha seleccionado una imagen
        if self.ruta_marca_de_agua:
            # Establecer la ruta seleccionada como valor de la variable path_marca_de_agua
            self.path_marca_de_agua.set(self.ruta_marca_de_agua)
            # Configurar el texto del botón de selección de imagen de marca de agua con la ruta seleccionada
            self.boton_seleccionar_marca_de_agua.config(text=self.ruta_marca_de_agua)
            # Habilitar el botón para seleccionar la carpeta de imágenes
            self.boton_seleccionar_carpeta_imagenes.config(state='normal')

    # Método para seleccionar la carpeta de imágenes
    def seleccionar_carpeta_imagenes(self):
        # Solicitar al usuario que seleccione una carpeta y almacenar la ruta seleccionada
        self.ruta_carpeta_imagenes = filedialog.askdirectory()
        # Verificar si se ha seleccionado una carpeta
        if self.ruta_carpeta_imagenes:
            # Establecer la ruta seleccionada como valor de la variable path_carpeta_imagenes
            self.path_carpeta_imagenes.set(self.ruta_carpeta_imagenes)
            # Configurar el texto del botón de selección de carpeta de imágenes con la ruta seleccionada
            self.boton_seleccionar_carpeta_imagenes.config(text=self.ruta_carpeta_imagenes)
            # Mostrar la previsualización de la primera imagen en la carpeta seleccionada
            self.mostrar_previsualizacion()

    # Método para mostrar la previsualización de la primera imagen en la carpeta seleccionada
    def mostrar_previsualizacion(self):
        # Obtener la lista de archivos de imagen en la carpeta seleccionada
        archivos_imagen = [archivo for archivo in os.listdir(self.ruta_carpeta_imagenes) if archivo.endswith(('.jpg', '.jpeg', '.png'))]
        # Verificar si hay archivos de imagen en la carpeta
        if archivos_imagen:
            # Abrir la primera imagen en la lista
            imagen = Image.open(os.path.join(self.ruta_carpeta_imagenes, archivos_imagen[0]))
            # Aplicar la marca de agua a la imagen y redimensionarla
            imagen_con_marca_de_agua = self.aplicar_marca_de_agua_a_imagen(imagen, margen_superior=self.margen_superior.get(), margen_izquierdo=self.margen_izquierdo.get())
            imagen_con_marca_de_agua.thumbnail((550, 550))  # Redimensionar la imagen a 550x550
            # Convertir la imagen para mostrarla en el widget Label
            imagen_con_marca_de_agua = ImageTk.PhotoImage(imagen_con_marca_de_agua)
            # Configurar la imagen en el widget Label de previsualización
            self.previsualizacion.config(image=imagen_con_marca_de_agua)
            self.previsualizacion.image = imagen_con_marca_de_agua

    # Método para aplicar la marca de agua a una imagen
    def aplicar_marca_de_agua_a_imagen(self, imagen, margen_superior, margen_izquierdo):
        # Cargar la imagen de marca de agua y convertirla al formato RGBA
        marca_de_agua = Image.open(self.ruta_marca_de_agua).convert('RGBA')
        # Obtener el tamaño de la marca de agua
        tamano_marca_de_agua = self.tamano_marca_de_agua.get()
        # Redimensionar la marca de agua al tamaño especificado
        marca_de_agua = marca_de_agua.resize((tamano_marca_de_agua, tamano_marca_de_agua))
        # Copiar la imagen original
        imagen_con_marca_de_agua = imagen.copy()
        # Aplicar la marca de agua a la imagen original
        imagen_con_marca_de_agua.paste(marca_de_agua, (margen_izquierdo, margen_superior), marca_de_agua)
        # Devolver la imagen con la marca de agua aplicada
        return imagen_con_marca_de_agua

    # Método para aplicar la marca de agua a todas las imágenes en la carpeta
    def aplicar_marca_de_agua(self):
        # Verificar si se han seleccionado tanto la imagen de marca de agua como la carpeta de imágenes
        if self.ruta_marca_de_agua and self.ruta_carpeta_imagenes:
            # Crear las carpetas "procesada", "jpg" y "webp" si no existen
            carpeta_procesada = os.path.join(self.ruta_carpeta_imagenes, "procesada")
            carpeta_jpg = os.path.join(carpeta_procesada, "jpg")
            carpeta_webp = os.path.join(carpeta_procesada, "webp")
            for carpeta in [carpeta_procesada, carpeta_jpg, carpeta_webp]:
                if not os.path.exists(carpeta):
                    os.makedirs(carpeta)

            # Obtener la lista de archivos de imagen en la carpeta seleccionada
            archivos_imagen = [archivo for archivo in os.listdir(self.ruta_carpeta_imagenes) if archivo.endswith(('.jpg', '.jpeg', '.png'))]
            total_archivos = len(archivos_imagen)
            # Verificar si hay archivos de imagen en la carpeta
            if total_archivos == 0:
                # Mostrar un mensaje de advertencia si no se encuentran archivos de imagen
                messagebox.showwarning("Advertencia", "No se encontraron archivos de imágenes en la carpeta seleccionada.")
                return

            # Configurar la barra de progreso
            self.barra_progreso["value"] = 0
            self.barra_progreso["maximum"] = total_archivos

            # Iterar sobre cada archivo de imagen en la carpeta
            for i, archivo_imagen in enumerate(archivos_imagen):
                # Actualizar el valor de la barra de progreso
                self.barra_progreso["value"] = i + 1
                self.ventana.update_idletasks()

                # Verificar si el archivo es una imagen
                if archivo_imagen.endswith(('.jpg', '.jpeg', '.png')):
                    # Abrir la imagen
                    imagen = Image.open(os.path.join(self.ruta_carpeta_imagenes, archivo_imagen))
                    # Aplicar la marca de agua a la imagen
                    imagen_con_marca_de_agua = self.aplicar_marca_de_agua_a_imagen(imagen, margen_superior=self.margen_superior.get(), margen_izquierdo=self.margen_izquierdo.get())
                    # Generar un timestamp para el nombre de archivo único
                    timestamp = str(int(time.time()))

                    # Definir las rutas de salida para la imagen en formato webp y jpg
                    nombre_imagen_salida = os.path.splitext(archivo_imagen)[0]
                    ruta_imagen_salida_jpg = os.path.join(carpeta_jpg, f"{nombre_imagen_salida}.jpg")
                    ruta_imagen_salida_webp = os.path.join(carpeta_webp, f"{nombre_imagen_salida}-{timestamp}.webp")

                    # Redimensionar la imagen con marca de agua para evitar problemas de tamaño
                    imagen_con_marca_de_agua.thumbnail((1200, 1200))

                    # Guardar la imagen con marca de agua en formato webp
                    imagen_con_marca_de_agua.save(ruta_imagen_salida_webp, "WEBP", quality=100)

                    # Guardar la imagen con marca de agua en formato jpg sin timestamp
                    imagen_con_marca_de_agua.save(ruta_imagen_salida_jpg, "JPEG", quality=100)

            # Restablecer la barra de progreso después de completar el procesamiento
            self.barra_progreso["value"] = 0
            # Mostrar un mensaje de información sobre la finalización del proceso
            messagebox.showinfo("Proceso Completado", f"Se han procesado y guardado {total_archivos} imágenes en las carpetas 'jpg' y 'webp' dentro de la carpeta 'procesada'.")
            # Abrir la carpeta procesada después de completar el procesamiento
            os.startfile(carpeta_procesada)

    # Método para actualizar la previsualización
    def actualizar_previsualizacion(self, *args):
        # Verificar si se ha seleccionado una carpeta de imágenes
        if self.ruta_carpeta_imagenes:
            # Mostrar la previsualización de la primera imagen en la carpeta
            self.mostrar_previsualizacion()

# Inicializar la aplicación
if __name__ == "__main__":
    ventana_principal = Tk()
    aplicacion = AplicacionMarcaDeAgua(ventana_principal)
    ventana_principal.mainloop()