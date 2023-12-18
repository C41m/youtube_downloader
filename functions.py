from tkinter import filedialog
import tkinter as tk

def select_folder():
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    folder_path = filedialog.askdirectory()
    root.destroy()
    return folder_path