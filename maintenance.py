# bibliotecas a serem utilizadas
import tkinter as tk
from tkinter import ttk
from tkinter.font import Font
from tkinter import messagebox
import subprocess
from os import system
import psutil

version = '1.0'

# Função para encontrar as unidades locais
def obter_unidades():
    unidades = psutil.disk_partitions()
    diretorios = []

    for unidade in unidades:
        # Objeto das unidades
        diretorios.append(unidade)

    return diretorios

nome_unidade = ''

# Função para obter apenas o nome das unidades
def obter_nome_unidades():
    unidades = obter_unidades()
    nome_unidades = []

    for unidade in unidades:
        nome_unidades.append(unidade.device)

    # retorna o objeto
    return nome_unidades

# Função para obter o armazenamento das unidades
def verificar_armazenamento(unidade_var, label_info):
    # Ira receber o nome da unidade
    try:
        unidade = unidade_var.get()

        disco = psutil.disk_usage(unidade)
        espaco_total = disco.total/1073741824
        espaco_usado = disco.used/1073741824
        espaco_livre = disco.free/1073741824

        info = f"Armazenamento da Unidade {unidade}\n\nEspaço Total: {espaco_total:.2f} GB\nEspaço Usado: {espaco_usado:.2f} GB\nEspaço Livre: {espaco_livre:.2f} GB"
        atualizar_label(label_info, info)

    except FileNotFoundError:
        messagebox.showerror('Unidade não selecionada','Você não selecionou nenhuma unidade!')

# Função que ira criar uma caixa de seleção referente as unidades instaladas
# Instaladas no computador do usuário
def caixa_selecoes_unidades():
    frame_caixa_selecao = ttk.Frame(janela)
    frame_caixa_selecao.pack()
    combo_var = tk.StringVar()

    unidades = obter_nome_unidades()
    
    unidades_ordenadas = sorted(unidades)
    tamanho_caixa_selecao = 20
    combo = ttk.Combobox(frame_caixa_selecao, textvariable=combo_var, state="readonly", values=unidades_ordenadas, width=tamanho_caixa_selecao)
    combo.pack(pady=5)
    
    return combo_var

def atualizar_label(label, info):
    label.config(text=info)

# Criando Janela
janela = tk.Tk()
janela.title(f'Maintence {version}')

# Definindo altura x largura
largura = 250
altura = 300

# Centralizando a janela em referencia a tela do computador do usuario
# Obtém as dimensões da tela
largura_tela = janela.winfo_screenwidth()
altura_tela = janela.winfo_screenheight()

# Calcula as coordenadas x e y para centralizar a janela
x = (largura_tela - largura) // 2
y = (altura_tela - altura) // 2

# Define a geometria da janela para centralizá-la
janela.geometry(f"{largura}x{altura}+{x}+{y-150}")

# Impedir o usuário de redimensionar a janela
janela.resizable(width=False, height=False)

# Label para escolher a unidade
principal = tk.Label(janela, text='Escolha uma unidade').pack(pady=10)
unidade_var = caixa_selecoes_unidades()

# label para o titulo referente das informações
titulo_label_info = tk.Label(janela, text='')

# Label para exibir informações
info_label = tk.Label(janela, text='')
info_label.pack(pady=10)

# Botão para verificar o armazenamento da unidade selecionada

botao_armazenamento = tk.Button(janela, text='Armazenamento', command=lambda: verificar_armazenamento(unidade_var, info_label))
botao_armazenamento.pack(pady=10)



janela.mainloop()
