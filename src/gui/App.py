# GUI Utama

import customtkinter as ctk

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.geometry("400x300")
root.title("Test CustomTkinter")

label = ctk.CTkLabel(root, text="Hello, CustomTkinter!")
label.pack(pady=20)

button = ctk.CTkButton(root, text="Click Me", command=lambda: print("Clicked!"))
button.pack()

root.mainloop()