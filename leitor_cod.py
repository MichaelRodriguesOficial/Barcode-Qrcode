import cv2
import os
import pyautogui
from pyzbar.pyzbar import decode
import pyperclip
import tkinter as tk
from tkinter import ttk
from datetime import datetime
import csv
import tkinter.filedialog as fd

# Inicializa history_list fora da função main()
history_list = []

# Variáveis globais para rastrear o estado de classificação das colunas
sort_column = 0  # Definindo a primeira coluna como padrão para classificação
sort_order = True  # Classificação ascendente como padrão

# Variável global para a janela principal
root = None

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
    msg_root.overrideredirect(True)  # Remove bordas decorativas

    label_header = tk.Label(msg_root, text=code_type, font=("Helvetica", 12, "bold"))
    label_header.pack(pady=5)

    if message:  # Adiciona uma verificação para exibir a mensagem apenas se houver uma
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


def decode_and_print(image):
    decoded_objects = decode(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY))
    if decoded_objects:
        for obj in decoded_objects:
            barcode_data = obj.data.decode("utf-8")
            print("Tipo:", obj.type)
            print("Dados:", barcode_data)
            pyperclip.copy(barcode_data)
            if obj.type == 'QRCODE':
                message = "Código copiado, você já pode colar ele:\n\n{}".format(
                    barcode_data[:len(barcode_data) // 2] + "\n" + barcode_data[len(barcode_data) // 2:]
                )
            else:
                message = "Código copiado, você já pode colar ele:\n\n{}".format(
                    barcode_data
                )
            code_type = "QR Code" if obj.type == 'QRCODE' else "Cód de Barras"
            update_history(barcode_data, code_type)
            update_treeview()  # Chama update_treeview() antes de mostrar a mensagem
            show_message(message, code_type)
    else:  # Se não houver códigos detectados, exibe uma mensagem
        show_message(None, "Nenhum código detectado")

def update_history(data, code_type):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    history_list.append((timestamp, data, code_type))

def capture_screen(filename):
    screenshot = pyautogui.screenshot()
    screenshot.save(filename)

def capture_code():
    root_path = "./"
    image_filename = "screenshot.png"
    image_path = os.path.join(root_path, image_filename)
    capture_screen(image_path)
    image = cv2.imread(image_path)
    decode_and_print(image)

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
            writer.writerow(["Data/Hora", "Codigo", "Tipo"])  # Escreve cabeçalhos das colunas
            for item in history_list:
                writer.writerow(item)  # Escreve cada linha com os dados dos códigos capturados


# Tamanho mínimo da janela
MIN_WINDOW_WIDTH = 400
MIN_WINDOW_HEIGHT = 300

def main():
    # Define colors and fonts
    BACKGROUND_COLOR = "#f0f0f0"
    FONT_FAMILY = "Segoe UI"
    BUTTON_FONT = (FONT_FAMILY, 12, "bold")

    global root
    root = tk.Tk()
    root.title("CAV - Leitor de Código")  # Changed title to "Leitor de Código" (Code Reader)
    root.configure(bg=BACKGROUND_COLOR)

    # Remove o botão de maximizar
    #root.resizable(False, False)

    # Define o ícone
    root.iconbitmap("favicon.ico")

    # Define um estilo para o Treeview
    style = ttk.Style()
    style.theme_use("clam")  # Escolha um tema que suporte Treeview
    style.configure("Treeview", background="#fff")  # Define a cor de fundo do Treeview

    # Treeview Frame
    treeview_frame = tk.Frame(root, bg="#fff")  # Defina a cor de fundo do frame do Treeview aqui
    treeview_frame.pack(padx=10, pady=10, fill="both", expand=True)

    # Create the Treeview widget
    global treeview
    treeview = ttk.Treeview(treeview_frame, columns=("Data/Hora", "Código", "Tipo"), show="headings")
    treeview.pack(side="left", fill="both", expand=True)

    treeview.heading("Data/Hora", text="Data/Hora", command=lambda: sort_treeview(0))
    treeview.heading("Código", text="Código", command=lambda: sort_treeview(1))
    treeview.heading("Tipo", text="Tipo", command=lambda: sort_treeview(2))

    # Define column widths
    treeview.column("Data/Hora", width=70)
    treeview.column("Código", width=200)
    treeview.column("Tipo", width=50)

    # Scrollbar
    scrollbar = tk.Scrollbar(treeview_frame, orient="vertical", command=treeview.yview)
    scrollbar.pack(side="right", fill="y")
    treeview.config(yscrollcommand=scrollbar.set)

    treeview.bind("<Double-1>", copy_code)

    # Mensagem em negrito acima dos botões
    message_label = tk.Label(root, text="Para copiar um código, basta clicar duas vezes em cima dele", font=BUTTON_FONT)
    message_label.pack(pady=5)

    # Botões em um frame separado
    button_frame = tk.Frame(root, bg=BACKGROUND_COLOR)
    button_frame.pack(fill="x", padx=10, pady=10)

    # Capture button
    capture_button = tk.Button(
        button_frame,
        text="Capturar",
        command=capture_code,
        font=BUTTON_FONT,
        width=15,
        bg="#4CAF50",  # Green button
        fg="#fff",  # White text
    )
    capture_button.pack(side="left")

    # Exit button
    exit_button = tk.Button(
        button_frame,
        text="Sair",
        command=exit_application,
        font=BUTTON_FONT,
        width=15,
        bg="#f44336",  # Red button
        fg="#fff",  # White text
    )
    exit_button.pack(side="right")

    # Export button - centralizado
    export_button = tk.Button(
        button_frame,
        text="Exportar Códigos",
        command=export_codes,
        font=BUTTON_FONT,
        width=15,
        bg="#007bff",  # Blue button
        fg="#fff",  # White text
    )
    export_button.pack(side="left", expand=True)

    adjust_window_size(root, MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT)

    root.mainloop()

# Function for centering and adjusting the window size based on screen resolution and DPI
def adjust_window_size(root, min_width, min_height):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Calcula o tamanho ideal da janela baseado na resolução da tela, com um mínimo garantido
    width = max(min_width, int(screen_width * 0.5))
    height = max(min_height, int(screen_height * 0.5))

    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    root.geometry(f"{width}x{height}+{x}+{y}")

if __name__ == "__main__":
    main()
