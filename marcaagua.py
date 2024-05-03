from tkinter import Tk, Button, Label, filedialog, Scale, messagebox, PhotoImage
import os
from PIL import Image, ImageTk
from tkinter.ttk import Progressbar

class AplicacionMarcaDeAgua:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Aplicación de Marca de Agua")
        self.ventana.geometry("950x950")  # Establecer las dimensiones de la ventana

        # Cargar el logo y redimensionarlo
        self.logo = PhotoImage(file="./logo.png")
        self.logo_label = Label(ventana, image=self.logo)
        self.logo_label.image = self.logo  # Mantener una referencia para evitar que la imagen sea eliminada por el recolector de basura
        self.logo_label.pack(pady=5, padx=5, side="top", anchor="n")  # Alinear la etiqueta en la parte superior

        # Variables para almacenar la ruta de la imagen de marca de agua y la carpeta de imágenes
        self.ruta_marca_de_agua = ''
        self.ruta_carpeta_imagenes = ''

        # Variables para controlar el margen y el tamaño de la marca de agua
        self.margen_superior = Scale(ventana, from_=0, to=100, orient='horizontal', label="Margen Superior")
        self.margen_izquierdo = Scale(ventana, from_=0, to=100, orient='horizontal', label="Margen Izquierdo")
        self.tamano_marca_de_agua = Scale(ventana, from_=0, to=400, orient='horizontal', label="Tamaño de la Marca de Agua")

        # Establecer el valor inicial del tamaño de la marca de agua
        self.tamano_marca_de_agua.set(100)

        # Botones para seleccionar la imagen de marca de agua y la carpeta de imágenes
        Button(ventana, text="Seleccionar Imagen de Marca de Agua", command=self.seleccionar_marca_de_agua).pack(pady=5, padx=5, side="top", anchor="n")
        Button(ventana, text="Seleccionar Carpeta de Imágenes", command=self.seleccionar_carpeta_imagenes).pack(pady=5, padx=5, side="top", anchor="n")

        # Colocar sliders para el margen superior, izquierdo y tamaño de la marca de agua
        self.margen_superior.pack(pady=5, padx=5, side="top", anchor="n")
        self.margen_izquierdo.pack(pady=5, padx=5, side="top", anchor="n")
        self.tamano_marca_de_agua.pack(pady=5, padx=5, side="top", anchor="n")

        # Botón para generar una nueva miniatura con los parámetros ingresados
        Button(ventana, text="Actualizar Miniatura", command=self.actualizar_miniatura).pack(pady=5, padx=5, side="top", anchor="n")

        # Etiqueta para mostrar una previsualización de la primera imagen en la carpeta de imágenes
        self.previsualizacion = Label(ventana, bd=2, relief="solid")  # Añadir borde negro
        self.previsualizacion.pack(pady=5, padx=5, side="top", anchor="n")
        
        # Botón para aplicar la marca de agua a todas las imágenes en la carpeta
        Button(ventana, text="Aplicar Marca de Agua", command=self.aplicar_marca_de_agua).pack(pady=5, padx=5, side="top", anchor="n")

        # Barra de progreso
        self.barra_progreso = Progressbar(ventana, orient="horizontal", length=200, mode="determinate")
        self.barra_progreso.pack(pady=5, padx=5, side="top", anchor="n")

    def seleccionar_marca_de_agua(self):
        self.ruta_marca_de_agua = filedialog.askopenfilename(filetypes=[("Imagen", "*.jpg;*.jpeg;*.png")])

    def seleccionar_carpeta_imagenes(self):
        self.ruta_carpeta_imagenes = filedialog.askdirectory()
        # Mostrar previsualización de la primera imagen en la carpeta seleccionada
        if self.ruta_carpeta_imagenes:
            archivos_imagen = [archivo for archivo in os.listdir(self.ruta_carpeta_imagenes) if archivo.endswith(('.jpg', '.jpeg', '.png'))]
            if archivos_imagen:
                imagen = Image.open(os.path.join(self.ruta_carpeta_imagenes, archivos_imagen[0]))
                imagen_con_marca_de_agua = self.aplicar_marca_de_agua_a_imagen(imagen, margen_superior=10, margen_izquierdo=10)
                imagen_con_marca_de_agua.thumbnail((350, 350))  # Tamaño de miniatura 350x350
                imagen_con_marca_de_agua = ImageTk.PhotoImage(imagen_con_marca_de_agua)
                self.previsualizacion.config(image=imagen_con_marca_de_agua)
                self.previsualizacion.image = imagen_con_marca_de_agua
                # Ajustar el tamaño de la etiqueta a la miniatura
                self.previsualizacion.config(width=imagen_con_marca_de_agua.width(), height=imagen_con_marca_de_agua.height())

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
            # Crear la carpeta "procesada" dentro de la carpeta de imágenes si no existe
            carpeta_procesada = os.path.join(self.ruta_carpeta_imagenes, "procesada")
            if not os.path.exists(carpeta_procesada):
                os.makedirs(carpeta_procesada)

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
                    imagen_con_marca_de_agua.save(os.path.join(carpeta_procesada, archivo_imagen), quality=100)

            # Restablecer la barra de progreso después de completar el procesamiento
            self.barra_progreso["value"] = 0
            messagebox.showinfo("Proceso Completado", f"Se han procesado y guardado {total_archivos} imágenes en la carpeta 'procesada'.")

    def actualizar_miniatura(self):
        if self.ruta_carpeta_imagenes:
            archivos_imagen = [archivo for archivo in os.listdir(self.ruta_carpeta_imagenes) if archivo.endswith(('.jpg', '.jpeg', '.png'))]
            if archivos_imagen:
                imagen = Image.open(os.path.join(self.ruta_carpeta_imagenes, archivos_imagen[0]))
                imagen_con_marca_de_agua = self.aplicar_marca_de_agua_a_imagen(imagen, margen_superior=self.margen_superior.get(), margen_izquierdo=self.margen_izquierdo.get())
                imagen_con_marca_de_agua.thumbnail((350, 350))  # Tamaño de miniatura 350x350
                imagen_con_marca_de_agua = ImageTk.PhotoImage(imagen_con_marca_de_agua)
                self.previsualizacion.config(image=imagen_con_marca_de_agua)
                self.previsualizacion.image = imagen_con_marca_de_agua
                # Ajustar el tamaño de la etiqueta a la miniatura
                self.previsualizacion.config(width=imagen_con_marca_de_agua.width(), height=imagen_con_marca_de_agua.height())

if __name__ == "__main__":
    ventana_principal = Tk()
    aplicacion = AplicacionMarcaDeAgua(ventana_principal)
    ventana_principal.mainloop()