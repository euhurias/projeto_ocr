import cv2
import easyocr
from tkinter import Tk, filedialog, Button, Label, Canvas, messagebox
from PIL import Image, ImageTk
import os

# Função para redimensionar imagens para exibição
def redimensionar_imagem(imagem, largura=300, altura=200):
    return cv2.resize(imagem, (largura, altura))

# Variáveis globais
imagem_path = None
texto_extraido = None

# Função para exibir a prévia de uma imagem no canvas
def exibir_previa(imagem_path):
    img = cv2.imread(imagem_path)
    img_resized = redimensionar_imagem(img)
    img_resized = cv2.cvtColor(img_resized, cv2.COLOR_BGR2RGB)  # Converter para formato RGB para exibição
    imagem_pil = Image.fromarray(img_resized)
    imagem_tk = ImageTk.PhotoImage(imagem_pil)
    canvas.create_image(0, 0, image=imagem_tk, anchor="nw")
    canvas.image = imagem_tk

# Função para realizar o OCR
def processar_imagem():
    global imagem_path, texto_extraido

    # Selecionar a imagem
    imagem_path = filedialog.askopenfilename(
        title="Selecione a Imagem",
        filetypes=[
            ("Todos os Arquivos de Imagem", "*.jpg *.jpeg *.png *.bmp *.tiff *.gif"), 
            ("JPEG", "*.jpg *.jpeg"),
            ("PNG", "*.png"),
            ("BMP", "*.bmp"),
            ("TIFF", "*.tiff"),
            ("GIF", "*.gif"),
        ],
    )
    if not imagem_path:
        return

    exibir_previa(imagem_path)  # Mostrar a imagem no canvas

    # Ler e pré-processar a imagem
    img = cv2.imread(imagem_path)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_bin = cv2.adaptiveThreshold(img_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                    cv2.THRESH_BINARY, 11, 2)

    # Realizar OCR
    reader = easyocr.Reader(['en'])
    resultado = reader.readtext(img_bin, detail=0)
    print(f"Resultado OCR: {resultado}")

    # Filtrar números detectados
    texto_extraido = " ".join(resultado).strip()
    if not texto_extraido:
        texto_extraido = "Texto não reconhecido"

    # Exibir o texto abaixo da imagem
    label_resultado.config(text=f"Texto Extraído: {texto_extraido}")

# Função para salvar a imagem
def salvar_imagem():
    global imagem_path, texto_extraido

    if not imagem_path or not texto_extraido:
        messagebox.showwarning("Aviso", "Nenhuma imagem processada ou texto extraído!")
        return

    # Selecionar a pasta de destino
    pasta_destino = filedialog.askdirectory(title="Selecione a Pasta de Destino")
    if not pasta_destino:
        return

    # Gerar novo nome de arquivo
    nome_arquivo, ext = os.path.splitext(os.path.basename(imagem_path))
    novo_nome = f"{texto_extraido.replace(' ', '_')}{ext}"
    caminho_novo = os.path.join(pasta_destino, novo_nome)

    # Salvar a imagem na pasta
    img = cv2.imread(imagem_path)
    cv2.imwrite(caminho_novo, img)

    # Feedback ao usuário
    messagebox.showinfo("Sucesso", f"Imagem salva como: {novo_nome}")

# Configuração inicial da interface
root = Tk()
root.title("Renomeador de Imagens com OCR")

# Tamanho e estilo da interface
root.geometry("500x600")
root.resizable(False, False)

# Título
label_titulo = Label(root, text="Renomeador de Imagens com OCR", font=("Arial", 16, "bold"))
label_titulo.pack(pady=10)

# Canvas para exibir a imagem
canvas = Canvas(root, width=300, height=200, bg="gray")
canvas.pack(pady=10)

# Botão para selecionar e processar a imagem
botao_processar_imagem = Button(root, text="Selecionar e Processar Imagem", font=("Arial", 12), command=processar_imagem)
botao_processar_imagem.pack(pady=10)

# Label para exibir o texto extraído
label_resultado = Label(root, text="", font=("Arial", 12), wraplength=400, justify="center")
label_resultado.pack(pady=10)

# Botão para salvar a imagem manualmente
botao_salvar_imagem = Button(root, text="Salvar Imagem", font=("Arial", 12), command=salvar_imagem)
botao_salvar_imagem.pack(pady=10)

# Rodar a interface
root.mainloop()
