import tkinter as tk
from tkinter import filedialog, messagebox

import numpy as np

from PIL import Image, ImageTk
import matplotlib.pyplot as plt

def escala_grises(imagen):
    """
    Convierte una imagen RGB a escala de grises.

    La imagen llega como array:
        alto x ancho x 3

    El promedio de los tres canales genera un único valor
    de intensidad.

    Después repetimos ese canal 3 veces para conservar
    el formato RGB.
    """

    gris = imagen.mean(axis=2)

    resultado = np.stack(
        [gris, gris, gris],
        axis=2
    )

    return resultado


def solo_canal(imagen, canal):
    """
    Conserva solamente un canal RGB.

    canal:
        0 -> R
        1 -> G
        2 -> B
    """

    resultado = np.zeros_like(imagen)

    resultado[:, :, canal] = imagen[:, :, canal]

    return resultado


# ============================================================
# CLASE PRINCIPAL
# ============================================================

class AppPDI:

    def __init__(self, ventana):

        self.ventana = ventana

        self.ventana.title(
            "TP0 - Grupo 07 - PDI con Tkinter"
        )

        self.ventana.geometry(
            "1200x650"
        )

        # ----------------------------------------------------
        # Variables donde guardaremos las imágenes.
        #
        # Los valores estarán normalizados entre 0 y 1.
        # ----------------------------------------------------

        self.imagen_original = None

        self.imagen_actual = None

        # Construimos la interfaz.
        self.crear_interfaz()


    # ========================================================
    # INTERFAZ
    # ========================================================

    def crear_interfaz(self):

        # ----------------------------------------------------
        # Barra superior
        # ----------------------------------------------------

        barra = tk.Frame(self.ventana)
        barra.pack(
            side="top",
            fill="x",
            padx=10,
            pady=10
        )

        boton_abrir = tk.Button(
            barra,
            text="Abrir imagen",
            command=self.abrir_imagen
        )
        boton_abrir.pack(
            side="left",
            padx=5
        )

        boton_restaurar = tk.Button(
            barra,
            text="Restaurar",
            command=self.restaurar
        )
        boton_restaurar.pack(
            side="left",
            padx=5
        )

        

        # ----------------------------------------------------
        # Panel central
        # ----------------------------------------------------

        panel = tk.Frame(self.ventana)
        panel.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )


        
        # ----------------------------------------------------
        # Zona donde aparecen las imágenes (Original y Procesada)
        # ----------------------------------------------------
        
        frame_imagenes = tk.Frame(panel)
        frame_imagenes.pack(
            side="left",
            fill="both",
            expand=True
        )

        # Etiqueta para la imagen original
        self.label_original = tk.Label(
            frame_imagenes,
            text="Imagen Original",
            bg="#cccccc"
        )
        self.label_original.pack(
            side="left",
            fill="both",
            expand=True,
            padx=5
        )

        # Etiqueta para la imagen procesada
        self.label_procesada = tk.Label(
            frame_imagenes,
            text="Imagen Procesada",
            bg="#dddddd"
        )
        self.label_procesada.pack(
            side="left",
            fill="both",
            expand=True,
            padx=5
        )
                
        # ----------------------------------------------------
        # Panel de controles
        # ----------------------------------------------------

        controles = tk.Frame(panel)
        controles.pack(
            side="right",
            fill="y",
            padx=10
        )


        titulo = tk.Label(
            controles,
            text="Operaciones PDI",
            font=("Arial", 14, "bold")
        )
        titulo.pack(pady=10)


        # ----------------------------------------------------
        # OptionMenu
        # ----------------------------------------------------

        self.operacion = tk.StringVar()

        self.operacion.set(
            "Original"
        )

        opciones = [
            "Original",
            "Escala de grises",
            "Solo canal R",
            "Solo canal G",
            "Solo canal B"
        ]

        menu = tk.OptionMenu(
            controles,
            self.operacion,
            *opciones
        )

        menu.pack(
            fill="x",
            pady=5
        )



        # ----------------------------------------------------
        # Botón aplicar
        # ----------------------------------------------------

        boton_aplicar = tk.Button(
            controles,
            text="Aplicar operación",
            command=self.aplicar_operacion
        )

        boton_aplicar.pack(
            fill="x",
            pady=10
        )

        # ----------------------------------------------------
        # Botón para Histograma
        # ----------------------------------------------------
                
        boton_histograma = tk.Button(
            controles,
            text="Ver Histograma",
            command=self.mostrar_histograma
        )
        
        boton_histograma.pack(
             fill="x",
            pady=10
        )

        # ----------------------------------------------------
        # Botón para Guardar Resultado
        # ----------------------------------------------------
        
        boton_guardar = tk.Button(
            controles,
            text="Guardar resultado",
            command=self.guardar_resultado
        )

        boton_guardar.pack(
            fill="x",
            pady=10
        )        

        # ----------------------------------------------------
        # Botón para usar el resultado como nueva entrada
        # ----------------------------------------------------
        
        boton_como_entrada = tk.Button(
            controles,
            text="Usar resultado como entrada",
            command=self.usar_resultado_como_entrada, 
        )

        boton_como_entrada.pack(
            fill="x",
            pady=10
        )

        # ----------------------------------------------------
        # Estado
        # ----------------------------------------------------

        self.estado = tk.Label(
            self.ventana,
            text="Listo.",
            anchor="w"
        )

        self.estado.pack(
            side="bottom",
            fill="x",
            padx=10,
            pady=10
        )


    # ========================================================
    # ABRIR IMAGEN
    # ========================================================

    def abrir_imagen(self):

        ruta = filedialog.askopenfilename(
            title="Seleccionar imagen",
            filetypes=[
                ("Imágenes", "*.jpg *.jpeg *.png *.bmp *.tif *.tiff")
            ]
        )

        if not ruta:
            return

        # Pillow abre la imagen.
        imagen_pil = Image.open(
            ruta
        ).convert("RGB")

        # Convertimos Pillow -> NumPy.
        #
        # /255.0 normaliza:
        #
        # 0   -> 0.0
        # 255 -> 1.0
        #
        self.imagen_original = (
            np.array(imagen_pil) / 255.0
        )

        # La imagen actual comienza siendo igual
        # a la original.
        self.imagen_actual = (
            self.imagen_original.copy()
        )

        #self.mostrar_imagen(
        #    self.imagen_actual
        #)
        # Reemplaza el self.mostrar_imagen(...) existente por:
        self.mostrar_imagen(self.imagen_original, self.label_original)
        self.mostrar_imagen(self.imagen_actual, self.label_procesada)

        self.estado.config(
            text="Imagen cargada correctamente."
        )


    # ========================================================
    # APLICAR OPERACIÓN
    # ========================================================

    def aplicar_operacion(self):

        # Verificamos que exista una imagen.
        if self.imagen_original is None:

            messagebox.showwarning(
                "Atención",
                "Primero abrí una imagen."
            )

            return


        # Obtenemos la opción seleccionada.
        operacion = self.operacion.get()

        imagen = self.imagen_original


        # ----------------------------------------------------
        # Acá empieza la conexión entre Tkinter y PDI.
        # ----------------------------------------------------

        if operacion == "Original":

            resultado = imagen.copy()


        elif operacion == "Escala de grises":

            resultado = escala_grises(
                imagen
            )


        elif operacion == "Solo canal R":

            resultado = solo_canal(
                imagen,
                0
            )


        elif operacion == "Solo canal G":

            resultado = solo_canal(
                imagen,
                1
            )


        elif operacion == "Solo canal B":

            resultado = solo_canal(
                imagen,
                2
            )


        # Guardamos el resultado.
        self.imagen_actual = resultado


        # Mostramos el resultado.
        self.mostrar_imagen(
            self.imagen_actual,
            self.label_procesada
        )


        self.estado.config(
            text=f"Operación aplicada: {operacion}"
        )


    # ========================================================
    # MOSTRAR IMAGEN
    # ========================================================

    def mostrar_imagen(self, array_imagen, label_destino):

        # Convertimos 0-1 nuevamente a 0-255.
        imagen_uint8 = (
            np.clip(
                array_imagen,
                0,
                1
            ) * 255
        ).astype(np.uint8)


        # NumPy -> Pillow
        imagen_pil = Image.fromarray(
            imagen_uint8
        )


        # Reducimos el tamaño para mostrarla.
        imagen_pil.thumbnail(
            (600, 600)
        )


        # Pillow -> Tkinter
        foto = ImageTk.PhotoImage(
            imagen_pil
        )


        # Guardamos la referencia.
        label_destino.foto = foto


        # Mostramos la imagen.
        label_destino.config(
            image=foto,
            text=""
        )


    # ========================================================
    # RESTAURAR
    # ========================================================

    def restaurar(self):

        if self.imagen_original is None:
            return

        self.imagen_actual = (
            self.imagen_original.copy()
        )

        self.mostrar_imagen(
            self.imagen_actual,
            self.label_procesada
        )

        self.estado.config(
            text="Imagen original restaurada."
        )

    # ========================================================
    # MOSTRAR HISTOGRAMA
    # ========================================================

    def mostrar_histograma(self):

        if self.imagen_actual is None:
            messagebox.showwarning(
                "Atención",
                "Primero abrí una imagen."
            )
            return

        datos = (self.imagen_actual * 255).astype(np.uint8).flatten()
        plt.hist(datos, bins=32, color="gray")
        plt.title("Histograma de intensidades")
        plt.xlabel("Valor de intensidad (0-255)")
        plt.ylabel("Frecuencia")
        plt.show()

    # ========================================================
    # GUARDAR RESULTADO
    # ========================================================

    def guardar_resultado(self):

        if self.imagen_actual is None:
            messagebox.showwarning(
                "Atención",
                "No hay ninguna imagen procesada para guardar."
            )
            return

        # Abrimos el cuadro de diálogo para elegir la ruta y el nombre del archivo
        ruta_guardado = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[
                ("Archivos PNG", "*.png"),
                ("Archivos JPG", "*.jpg"),
                ("Todos los archivos", "*.*")
            ],
            title="Guardar imagen procesada"
        )

        # Si el usuario cancela la ventana, la ruta estará vacía
        if not ruta_guardado:
            return

        try:
            # 1. Convertimos el array normalizado (0-1) de vuelta a 0-255 con uint8
            imagen_uint8 = (
                np.clip(
                    self.imagen_actual,
                    0,
                    1
                ) * 255
            ).astype(np.uint8)

            # 2. Pasamos de NumPy a Pillow
            imagen_pil = Image.fromarray(imagen_uint8)

            # 3. Guardamos la imagen en la ruta elegida
            imagen_pil.save(ruta_guardado)

            # Actualizamos la barra de estado
            self.estado.config(
                text=f"Imagen guardada con éxito en: {ruta_guardado}"
            )

        except Exception as e:
            messagebox.showerror(
                "Error",
                f"No se pudo guardar la imagen.\nDetalle: {e}"
            )

    # ========================================================
    # USAR RESULTADO COMO ENTRADA
    # ========================================================

    def usar_resultado_como_entrada(self):
        """
        Toma la imagen procesada actual (la de la derecha) 
        y la establece como la nueva imagen original de entrada (la de la izquierda).
        """
        if self.imagen_actual is None:
            messagebox.showwarning(
                "Atención",
                "No hay ninguna imagen procesada para usar como entrada."
            )
            return

        # La imagen actual pasa a ser la nueva base/original
        self.imagen_original = self.imagen_actual.copy()

        # Actualizamos el panel izquierdo para que muestre esta nueva entrada
        self.mostrar_imagen(self.imagen_original, self.label_original)

        self.estado.config(
            text="El resultado actual ahora es la nueva imagen de entrada."
        )


# ============================================================
# PUNTO DE ENTRADA
# ============================================================

if __name__ == "__main__":

    ventana = tk.Tk()

    app = AppPDI(
        ventana
    )

    ventana.mainloop()
