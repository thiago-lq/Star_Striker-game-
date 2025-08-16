import tkinter as tk
import os
import sys

def resource_path(relative_path):
    """Retorna o caminho absoluto do arquivo, compatível com PyInstaller."""
    try:
        # Se estiver rodando como executável
        base_path = sys._MEIPASS
    except Exception:
        # Se estiver rodando como script normal
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

#Interface onde vai rodar as coisas
root = tk.Tk()
root.title("Star Strike")
root.geometry("720x480")  # Define o tamanho da janela
root.configure(bg="white")
root.resizable(False, False)  # Impede o redimensionamento da janela
root.iconphoto(False, tk.PhotoImage(file=resource_path("src/assets/icone.png")))

# Criando um Canvas grande o suficiente para o jogo
canvas = tk.Canvas(root, width=720, height=480, bg="black")
canvas.place(x=0, y=0, width=720, height=480)

# Criando game states variables para usar no jogo
nave_img = tk.PhotoImage(file=resource_path("src/assets/nave.png"))
alien_img = tk.PhotoImage(file=resource_path("src/assets/alien.png"))
projeteis_alien = []
naves_alien = []
projeteis = []
estrelas = []
meteoros = []
vidas = 3
pontuacao = 0
nave = None
tempo_naves = 1500
tempo_disparos = 2000
nave_alien_ativa = False
projeteis_alien_ativos = False
projeteis_ativos = False    
botao_disparos = False