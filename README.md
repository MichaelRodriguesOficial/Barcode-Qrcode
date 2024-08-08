# Barcode-Qrcode

Este é um aplicativo simples para capturar e decodificar códigos de barras e QR codes a partir da tela do seu computador.

## Requisitos

* Python 3.x
* Bibliotecas Python:
    * opencv-python (cv2)
    * pyautogui
    * pyzbar
    * pyperclip
    * tkinter
    * pillow

## Como usar

1. Certifique-se de ter instalado todos os requisitos listados acima.
2. Execute o script `frontend.py`.
3. Uma janela será aberta com os botões "Capturar", "Exportar", "Câmera" e "Sair".
4. Clique em "Capturar" para capturar a tela e decodificar os códigos presentes nela.
5. Clique em "Câmera" para capturar e decodificar códigos usando a câmera do seu dispositivo.
6. Os códigos decodificados serão exibidos na tabela, contendo a data/hora da captura, o código e o tipo (QR Code ou Código de Barras).
7. Para copiar um código, clique com o botão direito sobre ele na tabela.
8. Para exportar os códigos capturados, clique em "Exportar" e escolha o local e o nome do arquivo CSV.
9. Para sair do aplicativo, clique em "Sair" ou feche a janela.

## Funções principais

* **Capturar**: Tira uma captura de tela e decodifica os códigos presentes nela.
* **Câmera**: Abre a câmera do dispositivo para captura e decodificação de códigos.
* **Exportar**: Permite exportar os códigos capturados para um arquivo CSV.
* **Sair**: Fecha o aplicativo.

## Transformando o código em .exe com o PyInstaller

Instale o PyInstaller:

```bash
pip install pyinstaller
```
```bash
pyinstaller --noconfirm --onefile --windowed --icon "C:/caminho/do_seu/favicon.ico" --add-data "C:/caminho/do_seu/Python/Python311/Lib/site-packages/pyzbar/libiconv.dll;." --add-data "C:/caminho/do_seu/Python/Python311/Lib/site-packages/pyzbar/libzbar-64.dll;." "C:/caminho/do_seu/frontend.py"
```

## Observações

* Copie o favicon.ico para o mesmo local do executável.
* Os códigos decodificados são exibidos na tabela e também são automaticamente copiados para a área de transferência.
* A tabela permite ordenação por data/hora, código e tipo de código.
* Clicar om o botão direito no código na tabela o copiará para a área de transferência.


Este projeto foi desenvolvido usando Python e a biblioteca Tkinter para a interface gráfica. O reconhecimento e decodificação dos códigos são realizados usando OpenCV e Pyzbar.