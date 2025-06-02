# GUI Utama

import customtkinter as ctk

class App:
    def __init__(self):
        # Setup global appearance
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        # Create root window
        self.root = ctk.CTk()
        self.root.geometry("400x300")
        self.root.title("Test CustomTkinter")

        # Add components
        label = ctk.CTkLabel(self.root, text="Hello, CustomTkinter!")
        label.pack(pady=20)

        button = ctk.CTkButton(self.root, text="Click Me", command=lambda: print("Clicked!"))
        button.pack()

    def run(self):
        self.root.mainloop()
