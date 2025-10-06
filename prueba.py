import tkinter as tk
from PIL import Image, ImageTk
import serial
import threading

class Parqueo:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Parqueo")
        self.max_carros = 14
        self.espacios = []
        self.contador = 0

        # Configuración del contador visual
        self.label_contador = tk.Label(self.root, text=f"Carros en el parqueo: {self.contador}", font=("Arial", 16))
        self.label_contador.pack(pady=10)
        
        self.label_parqueo_lleno = tk.Label(self.root, text="", font=("Arial", 16), fg="red")
        self.label_parqueo_lleno.pack(pady=5)

        # Crear un frame para los espacios de estacionamiento
        self.frame_espacios = tk.Frame(self.root)
        self.frame_espacios.pack(pady=20)

        # Crear un frame para las imágenes de los carros
        self.frame_carros = tk.Frame(self.root)
        self.frame_carros.pack(pady=20)

        # Cargar la imagen del carro
        self.carro_img = Image.open("carro1.png")
        self.carro_img = self.carro_img.resize((100, 100), Image.Resampling.LANCZOS)
        self.carro_photo = ImageTk.PhotoImage(self.carro_img)

        # Crear los espacios de estacionamiento (7 arriba y 7 abajo)
        for i in range(7):
            # Fila superior
            label = tk.Label(self.frame_espacios, text="", borderwidth=2, relief="solid",width=13, height=6)
            label.grid(row=0, column=i, padx=10, pady=5)
            self.espacios.append(label)

        for i in range(7):
            # Fila inferior
            label = tk.Label(self.frame_espacios, text="", borderwidth=2, relief="solid",width=13, height=6)
            label.grid(row=1, column=i, padx=10, pady=5)
            self.espacios.append(label)

        # Mostrar imagen de carro en cada espacio del frame de carros
        self.carro_labels = []
        for i in range(14):
            carro_label = tk.Label(self.frame_carros, image=self.carro_photo)
            carro_label.grid(row=i // 7, column=i % 7, padx=10, pady=5)
            self.carro_labels.append(carro_label)
        
        # Configuración del puerto serial
        self.ard = serial.Serial("COM2", 9600)
        
        # Crear y comenzar un hilo para leer datos de la serial
        self.serial_thread = threading.Thread(target=self.read_serial)
        self.serial_thread.daemon = True
        self.serial_thread.start()

    def read_serial(self):
        x=0
        while True:
            if self.ard.in_waiting > 0:
                datos = self.ard.readline().decode('utf-8').strip()
                #self.root.after(0, self.update_serial_label, datos)
                try:
                    numero = int(datos)
                    #self.root.after(0, self.update_serial_label, f"Datos de Serial (numérico): {numero}")
                    if numero > x:
                        d=numero-x
                        for i in range(d):
                            for carro in self.carro_labels:
                                if carro.cget("image")==str(self.carro_photo):
                                    carro.config(image="")
                                    break
                            for espacio in self.espacios:
                                if espacio.cget("image") == "":
                                    espacio.config(image=self.carro_photo,width=100, height=100)
                                    break
                            self.contador += 1
                            self.actualizar_contador()            
                            #print("numero es mayor")
                    elif numero < x :
                        e=x-numero
                        for i in range(e):
                            for espacio in self.espacios:
                                if espacio.cget("image") == str(self.carro_photo):
                                    espacio.config(image="",width=13, height=6)
                                    break
                            for carro in self.carro_labels:
                                if carro.cget("image")=="":
                                    carro.config(image=self.carro_photo)
                                    break
                            self.contador -=1   
                            self.actualizar_contador() 
                            #print("numero menor")
                    x=numero
                except ValueError:
                    self.root.after(0, self.update_serial_label, f"Datos de Serial (no numérico): {datos}")

    def actualizar_contador(self):
        self.label_contador.config(text=f"Carros en el parqueo: {self.contador}")
        if self.contador == self.max_carros:
            self.label_parqueo_lleno.config(text="Parqueo lleno")
        else:
            self.label_parqueo_lleno.config(text="")

    def agregar_carros(self):
        # Implementa la lógica de agregar carros si es necesario
        pass

# Crear la ventana principal
root = tk.Tk()
app = Parqueo(root)
root.mainloop()