import cv2
import pyautogui
from pyzbar.pyzbar import decode
import pyperclip  # Importar pyperclip para copiar para o clipboard

def capture_screen(filename):
    screenshot = pyautogui.screenshot()
    screenshot.save(filename)

def load_image(image_path):
    return cv2.imread(image_path)

def decode_and_print(image, update_history, update_treeview, show_message):
    decoded_objects = decode(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY))
    
    if decoded_objects:
        for obj in decoded_objects:
            barcode_data = obj.data.decode("utf-8")
            code_type = "QR Code" if obj.type == 'QRCODE' else "Cód de Barras"
            print("Tipo:", code_type)
            print("Dados:", barcode_data)
            pyperclip.copy(barcode_data)  # Copia o código para o clipboard
            
            message = "Código copiado, você já pode colar ele:\n\n{}".format(
                barcode_data[:len(barcode_data) // 2] + "\n" + barcode_data[len(barcode_data) // 2:]
            )
            
            update_history(barcode_data, code_type)
            update_treeview()  # Chama update_treeview antes de mostrar a mensagem
            show_message(message, code_type)
    else:
        show_message("Nenhum código encontrado.", "Resultado")
