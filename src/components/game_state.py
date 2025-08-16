import tkinter as tk

#Interface onde vai rodar as coisas
root = tk.Tk()
root.title("Star Strike")
root.geometry("720x480")  # Define o tamanho da janela
root.configure(bg="white")

# Criando um Canvas grande o suficiente
canvas = tk.Canvas(root, width=720, height=480, bg="black")
canvas.place(x=0, y=0, width=720, height=480)

nave_img = tk.PhotoImage(file="src/assets/nave.png")
alien_img = tk.PhotoImage(file="src/assets/alien.png")
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
# game_state.py
nave_alien_ativa = False  # Por padrão não cria naves
projeteis_alien_ativos = False
projeteis_ativos = False
botao_disparos = False

