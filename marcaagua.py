from tkinter import Tk, Button, Label, filedialog, Scale, messagebox, PhotoImage, Frame, StringVar
import os
from PIL import Image, ImageTk
from tkinter.ttk import Progressbar
import time

class AplicacionMarcaDeAgua:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Aplicación de Marca de Agua")
        self.ventana.geometry("1200x600")  # Establecer las dimensiones de la ventana

        # Cargar el logo y redimensionarlo
        self.logo = PhotoImage(file="./logo.png")
        self.logo_label = Label(ventana, image=self.logo)
        self.logo_label.image = self.logo  
        self.logo_label.grid(row=0, column=0, pady=5, padx=5, sticky="n")  

        # Variables para almacenar la ruta de la imagen de marca de agua y la carpeta de imágenes
        self.ruta_marca_de_agua = ''
        self.ruta_carpeta_imagenes = ''

        # Variables para controlar el margen y el tamaño de la marca de agua
        self.margen_superior = Scale(ventana, from_=0, to=100, orient='horizontal', label="Margen Superior", command=self.actualizar_previsualizacion)
        self.margen_izquierdo = Scale(ventana, from_=0, to=100, orient='horizontal', label="Margen Izquierdo", command=self.actualizar_previsualizacion)
        self.tamano_marca_de_agua = Scale(ventana, from_=0, to=400, orient='horizontal', label="Tamaño de la Marca de Agua", command=self.actualizar_previsualizacion)

        # Establecer el valor inicial del tamaño de la marca de agua
        self.tamano_marca_de_agua.set(100)

        # Variables StringVar para mostrar la ruta de la marca de agua y la carpeta de imágenes
        self.path_marca_de_agua = StringVar()
        self.path_carpeta_imagenes = StringVar()

        # Botones para seleccionar la imagen de marca de agua y la carpeta de imágenes
        self.boton_seleccionar_marca_de_agua = Button(ventana, text="Seleccionar Imagen de Marca de Agua", command=self.seleccionar_marca_de_agua)
        self.boton_seleccionar_marca_de_agua.grid(row=1, column=0, pady=5, padx=5, sticky="n")

        self.boton_seleccionar_carpeta_imagenes = Button(ventana, text="Seleccionar Carpeta de Imágenes", command=self.seleccionar_carpeta_imagenes, state='disabled')
        self.boton_seleccionar_carpeta_imagenes.grid(row=2, column=0, pady=5, padx=5, sticky="n")

        # Colocar sliders para el margen superior, izquierdo y tamaño de la marca de agua
        self.margen_superior.grid(row=5, column=0, pady=5, padx=5, sticky="n")
        self.margen_izquierdo.grid(row=6, column=0, pady=5, padx=5, sticky="n")
        self.tamano_marca_de_agua.grid(row=7, column=0, pady=5, padx=5, sticky="n")

        # Botón para aplicar la marca de agua a todas las imágenes en la carpeta
        Button(ventana, text="Aplicar Marca de Agua", command=self.aplicar_marca_de_agua).grid(row=8, column=0, pady=5, padx=5, sticky="n")

        # Barra de progreso
        self.barra_progreso = Progressbar(ventana, orient="horizontal", length=200, mode="determinate")
        self.barra_progreso.grid(row=9, column=0, pady=5, padx=5, sticky="n")

        # Crear un marco para la previsualización y el borde negro
        self.previsualizacion_frame = Frame(ventana, width=550, height=550, bd=2, relief="solid")
        self.previsualizacion_frame.grid(row=0, column=1, rowspan=10, pady=5, padx=5, sticky="nsew")
        self.previsualizacion_frame.grid_propagate(False)  # Evitar que el marco cambie de tamaño

        # Etiqueta para la imagen de previsualización
        self.previsualizacion = Label(self.previsualizacion_frame)
        self.previsualizacion.pack(fill="both", expand=True)


    def seleccionar_marca_de_agua(self):
        self.ruta_marca_de_agua = filedialog.askopenfilename(filetypes=[("Imagen", "*.jpg;*.jpeg;*.png")])
        if self.ruta_marca_de_agua:
            self.path_marca_de_agua.set(self.ruta_marca_de_agua)
            self.boton_seleccionar_marca_de_agua.config(text=self.ruta_marca_de_agua)
            self.boton_seleccionar_carpeta_imagenes.config(state='normal')

    def seleccionar_carpeta_imagenes(self):
        self.ruta_carpeta_imagenes = filedialog.askdirectory()
        if self.ruta_carpeta_imagenes:
            self.path_carpeta_imagenes.set(self.ruta_carpeta_imagenes)
            self.boton_seleccionar_carpeta_imagenes.config(text=self.ruta_carpeta_imagenes)
            self.mostrar_previsualizacion()

    def mostrar_previsualizacion(self):
        # Mostrar previsualización de la primera imagen en la carpeta seleccionada
        archivos_imagen = [archivo for archivo in os.listdir(self.ruta_carpeta_imagenes) if archivo.endswith(('.jpg', '.jpeg', '.png'))]
        if archivos_imagen:
            imagen = Image.open(os.path.join(self.ruta_carpeta_imagenes, archivos_imagen[0]))
            imagen_con_marca_de_agua = self.aplicar_marca_de_agua_a_imagen(imagen, margen_superior=self.margen_superior.get(), margen_izquierdo=self.margen_izquierdo.get())
            imagen_con_marca_de_agua.thumbnail((550, 550))  # Redimensionar la imagen a 550x550
            imagen_con_marca_de_agua = ImageTk.PhotoImage(imagen_con_marca_de_agua)
            self.previsualizacion.config(image=imagen_con_marca_de_agua)
            self.previsualizacion.image = imagen_con_marca_de_agua

    def aplicar_marca_de_agua_a_imagen(self, imagen, margen_superior, margen_izquierdo):
        # Obtener la marca de agua y ajustar su tamaño
        marca_de_agua = Image.open(self.ruta_marca_de_agua).convert('RGBA')
        tamano_marca_de_agua = self.tamano_marca_de_agua.get()
        marca_de_agua = marca_de_agua.resize((tamano_marca_de_agua, tamano_marca_de_agua))

        # Aplicar la marca de agua en la posición especificada
        imagen_con_marca_de_agua = imagen.copy()
        imagen_con_marca_de_agua.paste(marca_de_agua, (margen_izquierdo, margen_superior), marca_de_agua)

        return imagen_con_marca_de_agua

    def aplicar_marca_de_agua(self):
        if self.ruta_marca_de_agua and self.ruta_carpeta_imagenes:
            # Crear las carpetas "procesada", "jpg" y "webp" dentro de la carpeta de imágenes si no existen
            carpeta_procesada = os.path.join(self.ruta_carpeta_imagenes, "procesada")
            carpeta_jpg = os.path.join(carpeta_procesada, "jpg")
            carpeta_webp = os.path.join(carpeta_procesada, "webp")
            for carpeta in [carpeta_procesada, carpeta_jpg, carpeta_webp]:
                if not os.path.exists(carpeta):
                    os.makedirs(carpeta)

            archivos_imagen = [archivo for archivo in os.listdir(self.ruta_carpeta_imagenes) if archivo.endswith(('.jpg', '.jpeg', '.png'))]
            total_archivos = len(archivos_imagen)
            if total_archivos == 0:
                messagebox.showwarning("Advertencia", "No se encontraron archivos de imágenes en la carpeta seleccionada.")
                return

            # Configurar la barra de progreso
            self.barra_progreso["value"] = 0
            self.barra_progreso["maximum"] = total_archivos

            for i, archivo_imagen in enumerate(archivos_imagen):
                self.barra_progreso["value"] = i + 1
                self.ventana.update_idletasks()  # Actualizar la ventana para mostrar la barra de progreso

                if archivo_imagen.endswith(('.jpg', '.jpeg', '.png')):
                    imagen = Image.open(os.path.join(self.ruta_carpeta_imagenes, archivo_imagen))
                    imagen_con_marca_de_agua = self.aplicar_marca_de_agua_a_imagen(imagen, margen_superior=self.margen_superior.get(), margen_izquierdo=self.margen_izquierdo.get())

                    # Generar timestamp
                    timestamp = str(int(time.time()))

                    # Guardar imagen con marca de agua en formato webp o jpg con el nombre adecuado
                    nombre_imagen_salida = os.path.splitext(archivo_imagen)[0]
                    ruta_imagen_salida_jpg = os.path.join(carpeta_jpg, f"{nombre_imagen_salida}.jpg")
                    ruta_imagen_salida_webp = os.path.join(carpeta_webp, f"{nombre_imagen_salida}-{timestamp}.webp")

                    imagen_con_marca_de_agua.thumbnail((1200, 1200))  # Redimensionar la imagen a 1200x1200

                    # Guardar imagen en formato webp
                    imagen_con_marca_de_agua.save(ruta_imagen_salida_webp, "WEBP", quality=100)

                    # Guardar imagen en formato jpg
                    imagen_con_marca_de_agua.save(ruta_imagen_salida_jpg, "JPEG", quality=100)

            # Restablecer la barra de progreso después de completar el procesamiento
            self.barra_progreso["value"] = 0
            messagebox.showinfo("Proceso Completado", f"Se han procesado y guardado {total_archivos} imágenes en las carpetas 'jpg' y 'webp' dentro de la carpeta 'procesada'.")
            
            # Abrir el explorador en la carpeta procesada
            os.startfile(carpeta_procesada)

    def actualizar_previsualizacion(self, *args):
        if self.ruta_carpeta_imagenes:
            self.mostrar_previsualizacion()

if __name__ == "__main__":
    ventana_principal = Tk()
    aplicacion = AplicacionMarcaDeAgua(ventana_principal)
    ventana_principal.mainloop()