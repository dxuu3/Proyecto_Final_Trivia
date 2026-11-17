import json
import os
import tkinter as tk
from tkinter import messagebox
import winsound  

archivo_preguntas = "preguntas.json"
archivo_puntajes = "puntajes.json"

def cargar_preguntas():
    if not os.path.exists(archivo_preguntas):
        return []
    with open(archivo_preguntas, "r", encoding="utf-8") as f:
        return json.load(f)

def guardar_puntaje(nombre, puntaje):
    datos = {"jugador": nombre, "puntaje": puntaje}
    with open(archivo_puntajes, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4)

class AppTrivia:
    def __init__(self, root):
        self.root = root
        self.root.title("Proyecto Final - Trivia interactiva")
        self.root.geometry("500x400")

        self.preguntas = cargar_preguntas()
        self.indice_pregunta = 0
        self.puntaje = 0
        self.nombre_jugador = ""

        self.crear_pantalla_inicio()

    def limpiar_pantalla(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def crear_pantalla_inicio(self):
        self.limpiar_pantalla()

        lbl_titulo = tk.Label(self.root, text="Bienvenido a la Trivia", font=("Arial", 16, "bold"))
        lbl_titulo.pack(pady=25)

        lbl_nombre = tk.Label(self.root, text="Ingresa un nombre de usuario:", font=("Arial", 11))
        lbl_nombre.pack(pady=5)

        self.entry_nombre = tk.Entry(self.root, font=("Arial", 11), justify="center", width=25)
        self.entry_nombre.pack(pady=10)

        btn_empezar = tk.Button(self.root, text="Comenzar Juego", font=("Arial", 11), bg="#00DFFC", fg="white", width=20, command=self.validar_inicio)
        btn_empezar.pack(pady=20)

    def validar_inicio(self):
        nombre = self.entry_nombre.get().strip()
        if not nombre:
            messagebox.showerror("Error", "Por favor, ingresa un nombre de usuario.")
            return
        if not self.preguntas:
            messagebox.showerror("Error", "No hay preguntas disponibles. Por favor, agrega algunas al archivo 'preguntas.json'.")
            return

        self.nombre_jugador = nombre
        self.mostrar_pregunta()

    def mostrar_pregunta(self):
        self.limpiar_pantalla()

        if self.indice_pregunta < len(self.preguntas):
            p_actual = self.preguntas[self.indice_pregunta]

            lbl_progreso = tk.Label(self.root, text=f"Pregunta {self.indice_pregunta + 1} de {len(self.preguntas)}", font=("Arial", 9), fg="gray")
            lbl_progreso.pack(pady=5)

            lbl_pregunta = tk.Label(self.root, text=p_actual["pregunta"], font=("Arial", 11, "bold"), wraplength=450, justify="center")
            lbl_pregunta.pack(pady=15)

            for idx, opcion in enumerate(p_actual["opciones"]):
                btn = tk.Button(self.root, text=opcion, font=("Arial", 10), width=40,
                                command=lambda idx=idx: self.verificar_respuesta(idx))
                btn.pack(pady=6)
        else:
            self.finalizar_juego()

    def verificar_respuesta(self, indice_seleccionado):
        p_actual = self.preguntas[self.indice_pregunta]

        if indice_seleccionado == p_actual["respuesta"]:
            self.puntaje += 10
            winsound.Beep(880, 300)  # Sonido de respuesta correcta
            messagebox.showinfo("Correcto", "¡Respuesta correcta, has ganado 10 puntos!")
        else:
            winsound.Beep(300, 400)  # Sonido de respuesta incorrecta
            messagebox.showerror("Incorrecto", f"Respuesta incorrecta. La respuesta correcta era: {p_actual['opciones'][p_actual['respuesta']]}")

        self.indice_pregunta += 1
        self.mostrar_pregunta()

    def finalizar_juego(self):
        self.limpiar_pantalla()

        guardar_puntaje(self.nombre_jugador, self.puntaje)

        lbl_fin = tk.Label(self.root, text=f"Juego terminado, {self.nombre_jugador}!", font=("Arial", 14, "bold"))
        lbl_fin.pack(pady=20)

        lbl_puntaje = tk.Label(self.root, text=f"Tu puntaje final es: {self.puntaje}", font=("Arial", 12))
        lbl_puntaje.pack(pady=10)

        lbl_guardado = tk.Label(self.root, text="Tu puntaje ha sido guardado en 'puntajes.json'.", font=("Arial", 9), fg="green")
        lbl_guardado.pack(pady=5)

        btn_salir = tk.Button(self.root, text="Salir", font=("Arial", 11), bg="#FF5733", fg="white", width=15, command=self.root.quit)
        btn_salir.pack(pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = AppTrivia(root)
    root.mainloop()