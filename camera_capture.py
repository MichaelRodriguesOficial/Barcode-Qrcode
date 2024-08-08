import cv2
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import messagebox
from pyzbar.pyzbar import decode
import pyperclip
import threading
import screen_capture  # Certifique-se de que este módulo esteja corretamente importado
import os

def open_camera(root, update_history, update_treeview, show_message):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        messagebox.showerror("Erro", "Não foi possível abrir a câmera")
        return

    last_code_data = None  # Variável para armazenar o último código lido

    def restart_camera():
        nonlocal cap
        if cap is not None:
            cap.release()
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            messagebox.showerror("Erro", "Não foi possível reiniciar a câmera")
            return
        show_frame()  # Reinicia a captura de frames

    def process_decoded_objects(decoded_objects):
        nonlocal last_code_data
        for obj in decoded_objects:
            barcode_data = obj.data.decode("utf-8")
            if barcode_data == last_code_data:
                continue  # Se o código for igual ao último lido, ignora
            last_code_data = barcode_data  # Atualiza o último código lido
            code_type = "QR Code" if obj.type == 'QRCODE' else "Cód de Barras"
            
            # Copia o código para o clipboard
            pyperclip.copy(barcode_data)
            
            message = "Código copiado, você já pode colar ele:\n\n{}".format(
                barcode_data[:len(barcode_data) // 2] + "\n" + barcode_data[len(barcode_data) // 2:]
            )
            update_history(barcode_data, code_type)
            update_treeview()  # Atualiza a árvore ou histórico
            show_message(message, code_type)

    def show_frame():
        nonlocal cap
        ret, frame = cap.read()
        if not ret:
            messagebox.showerror("Erro", "Falha ao capturar frame")
            return

        # Decodifica QR Codes e códigos de barras
        decoded_objects = decode(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))
        if decoded_objects:
            # Processa os códigos em um thread separado
            threading.Thread(target=process_decoded_objects, args=(decoded_objects,)).start()

            # Desenha retângulos ao redor dos códigos detectados e exibe o texto
            for obj in decoded_objects:
                (x, y, w, h) = obj.rect
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 2)
                barcode_data = obj.data.decode("utf-8")
                code_type = "QR Code" if obj.type == 'QRCODE' else "Cód de Barras"
                cv2.putText(frame, code_type, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

        # Converte o frame para RGB e para ImageTk
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)

        # Atualiza o label da câmera com o novo frame
        camera_label.imgtk = imgtk
        camera_label.configure(image=imgtk)

        # Continua a captura de frames independentemente da detecção
        camera_label.after(10, show_frame)

    def close_camera():
        nonlocal cap
        if cap is not None:
            cap.release()
        camera_window.destroy()

    camera_window = tk.Toplevel(root)
    camera_window.title("CAV - Captura")
    
    # Define o ícone da janela
    #favicon_filename = "favicon.ico"
    #root_path = os.path.dirname(__file__)
    #camera_window.iconbitmap(os.path.join(root_path, favicon_filename))
    # Define o ícone
    camera_window.iconbitmap("favicon.ico")

    # Desabilita o botão de maximizar
    camera_window.resizable(False, False)
    
    # Fecha a câmera ao clicar no botão de fechar (x)
    camera_window.protocol("WM_DELETE_WINDOW", close_camera)
    
    camera_label = tk.Label(camera_window)
    camera_label.pack()

    show_frame()  # Inicia o loop de captura de frames

    camera_window.mainloop()
