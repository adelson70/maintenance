# bibliotecas a serem utilizadas
import tkinter as tk
from tkinter import ttk
from tkinter.font import Font
from tkinter import messagebox
import subprocess
from os import system
import sys
import psutil
import threading
from time import sleep
import ctypes
import pyautogui

version = '1.1'

# Função que ira verificar se o programa possui privilegios de administrador
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# Se não possuir ira pedir reiniciar o programa e ira pedir as credenciais
if is_admin() != True:
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    sys.exit()


# Função para ajustar a janela principal conforme o conteudo que estiver nela
def ajustar_janela_ao_conteudo(root):
    root.update_idletasks()  # Atualiza a geometria da janela
    largura = root.winfo_reqwidth()  # Largura requisitada pelo conteúdo
    altura = root.winfo_reqheight()  # Altura requisitada pelo conteúdo

    # Obtém as dimensões da tela
    largura_tela = root.winfo_screenwidth()
    altura_tela = root.winfo_screenheight()

    # Calcula a posição para centralizar a janela
    x_pos = (largura_tela - largura) // 2
    y_pos = (altura_tela - altura) // 2

    # Define a geometria da janela
    root.geometry(f"{largura+100}x{altura}+{x_pos}+{y_pos-130}")

# Função de espera
def esperar(tempo=3):
    sleep(tempo)

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

# Função executada em uma thread
# Para que a janela principal do tkinter ainda fique responsiva!
def trhead_geral(funcao):
    threading.Thread(target=funcao).start()

# Função para obter o armazenamento das unidades
def verificar_armazenamento(unidade_var, label_info):
    global titulo_label_info
    # Ira receber o nome da unidade
    try:
        unidade = unidade_var.get()

        # print(unidade)
        # print(type(unidade))

        disco = psutil.disk_usage(unidade)
        espaco_total = disco.total/1073741824
        espaco_usado = disco.used/1073741824
        espaco_livre = disco.free/1073741824

        info = f"Espaço Total: {espaco_total:.2f} GB\nEspaço Usado: {espaco_usado:.2f} GB\nEspaço Livre: {espaco_livre:.2f} GB"
        
        atualizar_label(titulo_label_info,f'Armazenamento da Unidade {unidade}\n')
        atualizar_label(label_info, info)
        #ajustar_janela_ao_conteudo(janela)

    except FileNotFoundError:
        messagebox.showerror('Unidade não selecionada','Você não selecionou nenhuma unidade!')

# Função que ira chamar o ultilitario do windows para fazer a verificação de disco
def verificar_disco(unidade, label_info):
    unidade = unidade.get()[:2]

    try:
        # Apenas para tratamento de erro
        disco = psutil.disk_usage(unidade)
        
        atualizar_label(label_info, f'Verificando Unidade {unidade}')

        comando_chkdsk = f'chkdsk {unidade} /f /r'

        # Execute o comando usando subprocess.run()
        subprocess.run(comando_chkdsk, shell=True, check=True)

        pyautogui.write('Y')
        pyautogui.press('enter')
        

    except FileNotFoundError:
        messagebox.showerror('Unidade não selecionada','Você não selecionou nenhuma unidade!')


# Função que ira chamar o serviço do windows de limpeza de disco
def limpeza_disco(unidade,label):
    global titulo_label_info
    atualizar_label(titulo_label_info,'Status')
    
    unidade = unidade.get()

    try:
        # apenas para tratamento de erro
        disco = psutil.disk_usage(unidade)

        atualizar_label(label,f'Limpando Unidade {unidade}')

        # Executa o serviço do windows de limpeza de disco
        subprocess.run(['cleanmgr.exe', '/d', unidade, '/sagerun:1'])

        # atualiza a label
        label_info = label
        info = f'Limpeza da Unidade {unidade} foi concluída!'
        atualizar_label(label_info,info)
        esperar(5)
        atualizar_label(label_info,'')
        
    except FileNotFoundError:
        messagebox.showerror('Unidade não selecionada','Você não selecionou nenhuma unidade!')


# Função para acessar o serviço de gerenciamento de disco
def gerenciamento_disco():
    global info_label
    global titulo_label_info
    atualizar_label(titulo_label_info,'Status')
   # ajustar_janela_ao_conteudo(janela)

    # Atualiza Label
    atualizar_label(info_label,'Gerenciamento de Disco Aberto')

    # Executa o gerenciador de disco
    subprocess.run(['mmc.exe', 'diskmgmt.msc'], check=True, shell=True)

    atualizar_label(info_label,'')
    

# Função que ira criar uma caixa de seleção referente as unidades instaladas
# Instaladas no computador do usuário
def caixa_selecoes_unidades():
    frame_caixa_selecao = ttk.Frame(janela)
    frame_caixa_selecao.pack()
    combo_var = tk.StringVar()

    unidades = obter_nome_unidades()
    
    unidades_ordenadas = sorted(unidades)
    tamanho_caixa_selecao = 5
    combo = ttk.Combobox(frame_caixa_selecao, textvariable=combo_var, state="readonly", values=unidades_ordenadas, width=tamanho_caixa_selecao)
    combo.pack(pady=5)

    return combo_var


def atualizar_label(label, info):
    label.config(text=info)
    ajustar_janela_ao_conteudo(janela)
    janela.update

# Criando Janela
janela = tk.Tk()
janela.title(f'Maintence {version}')

# Fontes personalizadas
fonte_titulo = Font(family="Segoe UI", size=11, weight="normal")
fonte_info = Font(family="Segoe UI", size=9, weight="normal")
fonte_botao = Font(family="Segoe UI", size=10, weight="normal")


# Impedir o usuário de redimensionar a janela
janela.resizable(width=False, height=False)

# Label para escolher a unidade
principal = tk.Label(janela, text='Escolha uma unidade', font=fonte_titulo).pack(pady=10)
unidade_var = caixa_selecoes_unidades()

# label principal das infos que surgirão
# label para o titulo referente das informações
titulo_label_info = tk.Label(janela, text='Status', font=fonte_titulo)
titulo_label_info.pack()
# Label para exibir informações
info_label = tk.Label(janela, text='', font=fonte_info)
info_label.pack()

# Botão para verificar o armazenamento da unidade selecionada
botao_armazenamento = tk.Button(janela, text='Armazenamento', font=fonte_botao, command=lambda: trhead_geral(verificar_armazenamento(unidade_var, info_label)))
botao_armazenamento.pack(pady=10)

# Botão para acessar o gerenciador de disco - diskmgmt.msc
botao_gerenciador = tk.Button(janela, text='Gerenciador',font=fonte_botao, command=lambda: trhead_geral(gerenciamento_disco))
botao_gerenciador.pack(pady=10)

# Botão para fazer uma limpeza de disco - cleanmgr.exe
botao_limpeza_disco = tk.Button(janela, text='Limpeza de Disco',font=fonte_botao, command=lambda: trhead_geral(limpeza_disco(unidade_var, info_label)))
botao_limpeza_disco.pack(pady=10)

# Botão para fazer a verificação de disco
botao_verificacao_disco = tk.Button(janela, text='Verificar Disco', font=fonte_botao, command=lambda: trhead_geral(verificar_disco(unidade_var, info_label)))
botao_verificacao_disco.pack(pady=10)

ajustar_janela_ao_conteudo(janela)
janela.mainloop()
