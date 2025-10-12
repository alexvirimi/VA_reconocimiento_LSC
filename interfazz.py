import cv2
import tkinter as tk
from tkinter import messagebox, scrolledtext
from PIL import Image, ImageTk

# Clase principal de la aplicación
class SignLanguageApp:
    def __init__(self, window):
        # Configuración inicial de la ventana principal
        self.window = window
        self.window.title("Intérprete de Lenguaje de Señas")
        self.window.geometry("900x600")      # Tamaño de la ventana
        self.window.configure(bg="#f2f4f7")  # Color de fondo

        # Variables para la cámara y el modo de interpretación
        self.cap = None
        self.frame = None
        self.mode = None

        # Pantalla inicial de bienvenida
        self.create_welcome_screen()

    # -----------------------------------------------------------
    # Función auxiliar: limpia todos los widgets de la ventana
    # -----------------------------------------------------------
    def clear_window(self):
        for widget in self.window.winfo_children():
            widget.destroy()

    # -----------------------------------------------------------
    # Pantalla 1: Bienvenida
    # -----------------------------------------------------------
    def create_welcome_screen(self):
        self.clear_window()

        # Contenedor principal de esta pantalla
        frame = tk.Frame(self.window, bg="#f2f4f7")
        frame.pack(expand=True)

        # Texto principal
        tk.Label(frame, text="¡Bienvenido al intérprete de lenguaje de señas!",
                 font=("Segoe UI", 18, "bold"), bg="#f2f4f7", fg="#2b3a55").pack(pady=40)

        # Botón para pasar al menú principal
        tk.Button(frame, text="Continuar", command=self.create_main_menu,
                  width=20, height=2, bg="#4a90e2", fg="white",
                  font=("Segoe UI", 12, "bold"), relief="flat").pack(pady=10)

    # -----------------------------------------------------------
    # Pantalla 2: Menú principal
    # -----------------------------------------------------------
    def create_main_menu(self):
        self.clear_window()

        frame = tk.Frame(self.window, bg="#f2f4f7")
        frame.pack(expand=True)

        # Título del menú
        tk.Label(frame, text="Menú principal", font=("Segoe UI", 18, "bold"),
                 bg="#f2f4f7", fg="#2b3a55").pack(pady=20)

        # Botón para ir al modo de interpretación
        tk.Button(frame, text="Empezar a interpretar", command=self.create_interpret_options,
                  width=25, height=2, bg="#4a90e2", fg="white",
                  font=("Segoe UI", 12, "bold"), relief="flat").pack(pady=10)

        # Botón para salir del programa
        tk.Button(frame, text="Salir", command=self.quit,
                  width=25, height=2, bg="#d9534f", fg="white",
                  font=("Segoe UI", 12, "bold"), relief="flat").pack(pady=10)

    # -----------------------------------------------------------
    # Pantalla 3: Opciones de interpretación
    # -----------------------------------------------------------
    def create_interpret_options(self):
        self.clear_window()

        frame = tk.Frame(self.window, bg="#f2f4f7")
        frame.pack(expand=True)

        # Título
        tk.Label(frame, text="¿Cómo quieres interpretar?", font=("Segoe UI", 18, "bold"),
                 bg="#f2f4f7", fg="#2b3a55").pack(pady=20)

        # Botón: interpretar por letras
        tk.Button(frame, text="Por letras", command=lambda: self.start_interpretation("letra"),
                  width=20, height=2, bg="#4a90e2", fg="white",
                  font=("Segoe UI", 12, "bold"), relief="flat").pack(pady=10)

        # Botón: interpretar por palabras (aún no implementado)
        tk.Button(frame, text="Por palabras", command=self.word_not_available,
                  width=20, height=2, bg="#999999", fg="white",
                  font=("Segoe UI", 12, "bold"), relief="flat").pack(pady=10)

        # Botón para volver al menú principal
        tk.Button(frame, text="Volver", command=self.create_main_menu,
                  width=20, height=2, bg="#d9534f", fg="white",
                  font=("Segoe UI", 12, "bold"), relief="flat").pack(pady=20)

    # -----------------------------------------------------------
    # Muestra mensaje de opción no disponible
    # -----------------------------------------------------------
    def word_not_available(self):
        messagebox.showinfo("Información", "No disponible de momento")

    # -----------------------------------------------------------
    # Pantalla 4: Modo de interpretación (cámara + texto)
    # -----------------------------------------------------------
    def start_interpretation(self, mode):
        self.clear_window()
        self.mode = mode

        # Etiqueta superior
        top_label = tk.Label(self.window, text=f"Interpretando por {mode}s...",
                             font=("Segoe UI", 16, "bold"), bg="#f2f4f7", fg="#2b3a55")
        top_label.pack(pady=10)

        # Contenedor principal (dividido en cámara y texto)
        container = tk.Frame(self.window, bg="#f2f4f7")
        container.pack(expand=True, fill="both", padx=20, pady=10)

        # ---------- Sección izquierda: cámara ----------
        left_frame = tk.Frame(container, bg="#dce3ed", width=500, height=400)
        left_frame.pack(side="left", padx=10, pady=10)
        left_frame.pack_propagate(False)  # Fijar tamaño

        # Etiqueta donde se mostrará el video
        self.video_label = tk.Label(left_frame, bg="#dce3ed")
        self.video_label.pack(expand=True)

        # ---------- Sección derecha: texto traducido ----------
        right_frame = tk.Frame(container, bg="#ffffff", width=300, height=400, relief="groove", bd=2)
        right_frame.pack(side="right", padx=10, pady=10)
        right_frame.pack_propagate(False)

        # Título del área de texto
        tk.Label(right_frame, text="Texto interpretado:", font=("Segoe UI", 12, "bold"), bg="#ffffff").pack(pady=5)

        # Cuadro de texto con scroll
        self.output_text = scrolledtext.ScrolledText(right_frame, wrap=tk.WORD, font=("Segoe UI", 11),
                                                     height=20, width=30)
        self.output_text.pack(padx=10, pady=10, fill="both", expand=True)
        self.output_text.insert(tk.END, "Aquí aparecerá el texto traducido...\n")

        # Botón para detener la interpretación
        quit_button = tk.Button(self.window, text="Detener y volver al menú",
                                command=self.stop_interpretation,
                                bg="#d9534f", fg="white", font=("Segoe UI", 12, "bold"),
                                relief="flat", width=25, height=2)
        quit_button.pack(pady=10)

        # Inicializar la cámara
        self.cap = cv2.VideoCapture(0)
        self.update_video()

    # -----------------------------------------------------------
    # Actualiza la imagen de la cámara en la interfaz
    # -----------------------------------------------------------
    def update_video(self):
        if self.cap:
            ret, frame = self.cap.read()
            if ret:
                # Convertir de BGR (OpenCV) a RGB (para Tkinter)
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame_rgb)
                imgtk = ImageTk.PhotoImage(image=img)

                # Mostrar imagen en el label
                self.video_label.imgtk = imgtk
                self.video_label.configure(image=imgtk)

                #  Aquí se debe agregar la lógica del modelo de interpretación
                

            # Volver a ejecutar esta función cada 10 ms (bucle de video)
            self.window.after(10, self.update_video)

    # -----------------------------------------------------------
    # Detiene la cámara y regresa al menú principal
    # -----------------------------------------------------------
    def stop_interpretation(self):
        if self.cap:
            self.cap.release()
            self.cap = None
        self.create_main_menu()

    # -----------------------------------------------------------
    # Cierra completamente la aplicación
    # -----------------------------------------------------------
    def quit(self):
        if self.cap:
            self.cap.release()
        self.window.destroy()


# -----------------------------------------------------------
# Ejecución principal del programa
# -----------------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = SignLanguageApp(root)
    root.mainloop()

