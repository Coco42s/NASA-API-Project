import tkinter as tk
from tkextrafont import Font

window = tk.Tk()
font = Font(file="font/nasalization_rg.ttf", family="Nasalization Rg")
tk.Label(window, text="Hello", font=("Nasalization Rg",15)).pack()
window.mainloop()