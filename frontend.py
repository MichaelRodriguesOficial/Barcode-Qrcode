import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import pyperclip
import csv
from datetime import datetime
from tkinter import filedialog as fd
import camera_capture
import screen_capture
import os

# Variáveis globais
history_list = []
sort_column = 0
sort_order = True
root = None
treeview = None

def adjust_window_size(root, width, height):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_coordinate = (screen_width - width) // 2
    y_coordinate = (screen_height - height) // 2
    root.geometry("{}x{}+{}+{}".format(width, height, x_coordinate, y_coordinate))

def show_message(message, code_type):
    msg_root = tk.Tk()
    msg_root.attributes("-topmost", True)
    msg_root.title("CAV - {}".format(code_type))
    msg_root.overrideredirect(True)

    label_header = tk.Label(msg_root, text=code_type, font=("Helvetica", 12, "bold"))
    label_header.pack(pady=5)

    if message:
        label_message = tk.Label(msg_root, text=message, font=("Helvetica", 12), wraplength=300)
        label_message.pack(pady=5)
    else:
        label_message = tk.Label(msg_root, text="", font=("Helvetica", 12))
        label_message.pack(pady=5)

    msg_root.update_idletasks()
    width = max(label_header.winfo_reqwidth(), label_message.winfo_reqwidth()) + 20
    height = label_header.winfo_reqheight() + label_message.winfo_reqheight() + 20

    adjust_window_size(msg_root, width, height)

    msg_root.after(3000, msg_root.destroy)
    msg_root.mainloop()

def update_history(data, code_type):
    timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    history_list.append((timestamp, data, code_type))

def update_treeview():
    treeview.delete(*treeview.get_children())
    sorted_history = sorted(history_list, key=lambda x: x[sort_column], reverse=sort_order)
    for item in sorted_history:
        timestamp, code, code_type = item
        treeview.insert("", "end", values=(timestamp, code, code_type), tags="centered")
    treeview.tag_configure("centered", anchor="center")

def copy_code(event):
    item = treeview.selection()[0]
    code = treeview.item(item, "values")[1]
    pyperclip.copy(code)

def exit_application():
    global root
    root.destroy()

def sort_treeview(column):
    global sort_column, sort_order
    if sort_column == column:
        sort_order = not sort_order
    else:
        sort_column = column
        sort_order = True
    update_treeview()

def export_codes():
    filename = fd.asksaveasfilename(defaultextension=".csv", filetypes=[("Arquivo CSV", "*.csv")])
    if filename:
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Data/Hora", "Codigo", "Tipo"])
            for item in history_list:
                writer.writerow(item)

def capture_code():
    image_path = "screenshot.png"
    screen_capture.capture_screen(image_path)
    image = screen_capture.load_image(image_path)
    screen_capture.decode_and_print(image, update_history, update_treeview, show_message)

def capture_from_camera():
    camera_capture.open_camera(root, update_history, update_treeview, show_message)

def main():
    global root, treeview
    root = tk.Tk()
    root.title("CAV - Leitor de Código")
    root.configure(bg="#f0f0f0")

    # Define o ícone
    #favicon_filename = "favicon.ico"
    #root_path = os.path.dirname(__file__)
    #root.iconbitmap(os.path.join(root_path, favicon_filename))
    # Define o ícone
    root.iconbitmap("favicon.ico")

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview", background="#fff")

    treeview_frame = tk.Frame(root, bg="#fff")
    treeview_frame.pack(padx=10, pady=10, fill="both", expand=True)

    treeview = ttk.Treeview(treeview_frame, columns=("Data/Hora", "Código", "Tipo"), show="headings")
    treeview.pack(side="left", fill="both", expand=True)

    treeview.heading("Data/Hora", text="Data/Hora", command=lambda: sort_treeview(0))
    treeview.heading("Código", text="Código", command=lambda: sort_treeview(1))
    treeview.heading("Tipo", text="Tipo", command=lambda: sort_treeview(2))

    # Definindo a largura das colunas
    treeview.column("Data/Hora", width=30)
    treeview.column("Código", width=400)  # Maior largura para a coluna "Código"
    treeview.column("Tipo", width=30)

    scrollbar = tk.Scrollbar(treeview_frame, orient="vertical", command=treeview.yview)
    scrollbar.pack(side="right", fill="y")
    treeview.configure(yscrollcommand=scrollbar.set)

    button_frame = tk.Frame(root, bg="#f0f0f0")
    button_frame.pack(padx=10, pady=10, fill="x")

    tk.Button(button_frame, text="Capturar", command=capture_code, font=("Segoe UI", 12, "bold"), width=15, bg="#4caf50", fg="#fff").pack(side="left", padx=5)
    tk.Button(button_frame, text="Exportar", command=export_codes, font=("Segoe UI", 12, "bold"), width=15, bg="#2196f3", fg="#fff").pack(side="left", padx=5)
    tk.Button(button_frame, text="Câmera", command=capture_from_camera, font=("Segoe UI", 12, "bold"), width=15, bg="#ff9800", fg="#fff").pack(side="left", padx=5)
    tk.Button(button_frame, text="Sair", command=exit_application, font=("Segoe UI", 12, "bold"), width=15, bg="#f44336", fg="#fff").pack(side="left", padx=5)

    root.bind("<Button-3>", copy_code)
    root.protocol("WM_DELETE_WINDOW", exit_application)
    root.mainloop()

if __name__ == "__main__":
    main()
