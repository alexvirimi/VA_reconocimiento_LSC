import cv2
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

class SignLanguageApp:
    def __init__(self, window):
        self.window = window
        self.window.title("Interprete de Lenguaje de Señas")
        self.window.geometry("640x480")
        self.cap = None  # Variable para la cámara, se inicializa cuando se empieza a interpretar

        self.frame = None  # Frame actual capturado de la cámara

        # Iniciar con la pantalla de bienvenida
        self.create_welcome_screen()

    def create_welcome_screen(self):
        """Crea la pantalla de bienvenida con un mensaje y botón para continuar."""
        self.clear_window()

        welcome_label = tk.Label(self.window, text="¡Bienvenido al intérprete de lenguaje de señas!", font=("Arial", 16))
        welcome_label.pack(pady=40)

        start_button = tk.Button(self.window, text="Continuar", command=self.create_main_menu, width=20, height=2)
        start_button.pack()

    def create_main_menu(self):
        """Crea el menú principal con opciones para empezar a interpretar o salir."""
        self.clear_window()

        menu_label = tk.Label(self.window, text="Menú principal", font=("Arial", 16))
        menu_label.pack(pady=20)

        start_interpret_button = tk.Button(self.window, text="Empezar a interpretar", command=self.create_interpret_options, width=25, height=2)
        start_interpret_button.pack(pady=10)

        quit_button = tk.Button(self.window, text="Salir", command=self.quit, width=25, height=2)
        quit_button.pack(pady=10)

    def create_interpret_options(self):
        """Pantalla para elegir el modo de interpretación: letra por letra o por palabras."""
        self.clear_window()

        option_label = tk.Label(self.window, text="¿Cómo quieres interpretar?", font=("Arial", 16))
        option_label.pack(pady=20)

        # Botón para interpretar letra por letra
        letter_button = tk.Button(self.window, text="por letras", command=lambda: self.start_interpretation("letra"), width=20, height=2)
        letter_button.pack(pady=10)

        # Botón para interpretar por palabras (aún no disponible)
        word_button = tk.Button(self.window, text="Por palabras", command=self.word_not_available, width=20, height=2)
        word_button.pack(pady=10)

        # Botón para volver al menú principal
        back_button = tk.Button(self.window, text="Volver", command=self.create_main_menu, width=20, height=2)
        back_button.pack(pady=20)

    def word_not_available(self):
        """Muestra un mensaje indicando que la opción por palabras no está disponible y regresa al menú de opciones."""
        messagebox.showinfo("Información", "No disponible de momento")
        self.create_interpret_options()

    def start_interpretation(self, mode):
        """
        Inicia la interpretación según el modo seleccionado.
        Muestra la cámara y un botón para salir.
        """
        self.clear_window()
        self.mode = mode

        info_label = tk.Label(self.window, text=f"Interpretando {mode}...\nPresiona 'Salir' para detener.", font=("Arial", 14))
        info_label.pack(pady=10)

        # Label donde se mostrará el video de la cámara
        self.video_label = tk.Label(self.window)
        self.video_label.pack()

        # Botón para detener la interpretación y volver al menú
        quit_button = tk.Button(self.window, text="Salir", command=self.stop_interpretation, width=20, height=2)
        quit_button.pack(pady=10)

        # Abrir la cámara
        self.cap = cv2.VideoCapture(0)
        self.update_video()

    def update_video(self):
        """
        Captura un frame de la cámara, lo procesa y lo muestra en la interfaz.
        Aquí es donde se debe integrar la lógica de reconocimiento de letras.
        """
        ret, frame = self.cap.read()
        if ret:
            self.frame = frame

            # Aquí va la lógica para interpretar por letras
            # 
            # 
            #    
            #      Mostrar resultado en la interfaz 

            # Convertir la imagen de BGR (OpenCV) a RGB (PIL/Tkinter)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame_rgb)
            imgtk = ImageTk.PhotoImage(image=img)

            # Actualizar el label con la imagen capturada
            self.video_label.imgtk = imgtk
            self.video_label.configure(image=imgtk)

        # Llamar a esta función nuevamente después de 10 ms para actualizar el video
        self.window.after(10, self.update_video)

    def stop_interpretation(self):
        """Detiene la cámara y regresa al menú principal."""
        if self.cap:
            self.cap.release()
            self.cap = None
        self.create_main_menu()

    def clear_window(self):
        """Elimina todos los widgets de la ventana para cambiar de pantalla."""
        for widget in self.window.winfo_children():
            widget.destroy()

    def quit(self):
        """Libera la cámara y cierra la aplicación."""
        if self.cap:
            self.cap.release()
        self.window.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = SignLanguageApp(root)
    root.mainloop()
