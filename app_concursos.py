import tkinter as tk
from tkinter import messagebox
import json
from PIL import Image, ImageTk

# Carregar questões de um arquivo JSON externo
with open("questoes.json", "r", encoding="utf-8") as f:
    questoes = json.load(f)

indice = 0
img_tk = None
img_original = None  # guarda a imagem original

def mostrar_questao():
    global indice, img_original
    questao = questoes[indice]

    # Texto interpretativo
    texto_label.config(text=questao.get("texto", "") or "")

    # Pergunta
    pergunta_label.config(text=questao["pergunta"])

    # Imagem
    if questao.get("imagem"):
        try:
            img_original = Image.open(questao["imagem"])
            atualizar_imagem()  # ajusta ao tamanho atual da janela
        except Exception as e:
            print("Erro ao carregar imagem:", e)
            imagem_label.config(image="")
            imagem_label.image = None
            img_original = None
    else:
        imagem_label.config(image="")
        imagem_label.image = None
        img_original = None

     # Alternativas com identificador A, B, C, D
    letras = ["A", "B", "C", "D"]
    opcao_var.set(-1)  # limpa seleção
    for i, rb in enumerate(radios):
        if i < len(questao["alternativas"]):
            rb.config(text=f"{letras[i]}) {questao['alternativas'][i]}", value=i)
            rb.pack(fill="x", padx=20, pady=5)
        else:
            rb.pack_forget()   # esconde radios extras se houver menos alternativas

def atualizar_imagem(event=None):
    """Redimensiona a imagem conforme o tamanho da janela"""
    global img_tk, img_original
    if img_original:
        largura = max(root.winfo_width() - 50, 100)   # margem lateral, valor mínimo
        altura = max(root.winfo_height() // 3, 100)   # ocupa 1/3 da altura, valor mínimo
        img = img_original.copy()
        img = img.resize((largura, altura))
        img_tk = ImageTk.PhotoImage(img)
        imagem_label.config(image=img_tk)
        imagem_label.image = img_tk  # mantém referência

def responder():
    global indice
    escolha = opcao_var.get()
    correta = questoes[indice]["correta"]

    if escolha == correta:
        messagebox.showinfo("Resultado", "✅ Correto!\n" + questoes[indice]["explicacao"])
    else:
        messagebox.showerror("Resultado", "❌ Errado.\n" + questoes[indice]["explicacao"])

    indice = (indice + 1) % len(questoes)
    mostrar_questao()

# Interface
root = tk.Tk()
root.title("App de Questões de Concurso")

# Variável para RadioButtons (crie depois do root!)
opcao_var = tk.IntVar()

# Label para texto interpretativo
texto_label = tk.Label(root, text="", font=("Arial", 12), wraplength=500, justify="left")
texto_label.pack(pady=10)

# Label para pergunta
pergunta_label = tk.Label(root, text="", font=("Arial", 14, "bold"), wraplength=500)
pergunta_label.pack(pady=10)

# Label para imagem
imagem_label = tk.Label(root)
imagem_label.pack(pady=10, fill="both", expand=True)

# Criar RadioButtons para alternativas (até 4 por padrão)
radios = []
for i in range(4):
    rb = tk.Radiobutton(root, text="", variable=opcao_var, value=i,
                        wraplength=500, justify="left", anchor="w")
    rb.pack(fill="x", padx=20, pady=5)
    radios.append(rb)

# Botão para responder
btn_responder = tk.Button(root, text="Responder", command=responder)
btn_responder.pack(pady=10)

# Atualiza imagem sempre que a janela mudar de tamanho
root.bind("<Configure>", atualizar_imagem)

mostrar_questao()
root.mainloop()