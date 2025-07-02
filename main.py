#bibliotecas necessárias
import tkinter as tk
from tkinter import ttk
import random as rd

#listas necessárias
projeteis = []
naves_alien = []
projeteis_alien = []
estrelas = []
nave = None
# Funções para os botões aparecem e desaparecerem
def iniciar_jogo():
    label_opcao.place_forget()
    label_nome.place_forget()
    botao_entrar.place_forget()
    botao_sair.place_forget()
    label_placar.place(x = 10, y = (y1 + y2 - label_placar.winfo_reqheight()) / 2)
    coração_placar.place(x=375, y=(y1 + y2 - coração_placar.winfo_reqheight()) / 2)
    
    global nave
    nave = canvas.create_image(250, 200, image=nave_img)
    canvas.bind("<Motion>", mover_nave)
    canvas.bind("<Button-1>", disparar_projeteis)  # Dispara projéteis quando a tecla espaço é pressionada
    mover_projeteis()
    root.config(cursor="none")
    criar_nave_alien()
    mover_naves_alien()
    mover_projeteis_alien()
    root.bind("<Escape>", lambda event: fim_do_jogo_esc())

#Sair do jogo
def sair():
    root.quit()

#Animação do fundo do jogo
def animar_fundo():
    global estrelas, meteoros
    for i in range(len(estrelas)):
        canvas.move(estrelas[i], -2, 0)
        x1, y1, x2, y2 = canvas.coords(estrelas[i])
        if x2 < 0:
            x_new = 500 + rd.randint(0, 50) 
            y_new = rd.randint(0, 400)
            canvas.coords(estrelas[i], x_new , y_new, x_new + 2, y_new + 2)
    for i in range(len(meteoros)):
        canvas.move(meteoros[i], -4, 0)
        if (canvas.coords(meteoros[i])[0] < 0):
            x_novo = 500 + rd.randint(0, 100)
            y_novo = rd.randint(0, 300)
            canvas.coords(meteoros[i], x_novo, y_novo, x_novo + 10, y_novo + 5)
    root.after(50, animar_fundo)

#função para perder os corações
vidas = 3
def atualizar_coracoes():
    coracoes = "❤️" * vidas
    coração_placar.config(text=coracoes.strip())

#sistema de ganhar pontos
pontuacao = 0
def atualizar_pontuacao():
    label_placar.config(text=f"Pontuação: {pontuacao}")

#função para ganhar os pontos
def ganhar_pontos(valor):
    global pontuacao
    pontuacao += valor
    atualizar_pontuacao()

#movimento da nave
def mover_nave(event):
    canvas.coords(nave, event.x, event.y)

#projeteis que irão sair da nave
def disparar_projeteis(event):
    x, y = canvas.coords(nave)
    
    # Posição do disparo superior
    proj_cima = canvas.create_oval(x - 3, y - 15, x + 3, y - 5, fill="yellow")
    
    # Posição do disparo inferior
    proj_baixo = canvas.create_oval(x - 3, y + 5, x + 3, y + 15, fill="yellow")
    
    projeteis.extend([proj_cima, proj_baixo])

# Função para mover os projéteis
def mover_projeteis():
    for proj in projeteis[:]:
        canvas.move(proj, 10, 0)
        x1, y1, x2, y2 = canvas.coords(proj)

        # Verifica colisão com naves alienígenas
        for nave in naves_alien[:]:
            x_n, y_n = canvas.coords(nave)
            if abs((x1 + x2) / 2 - x_n) < 20 and abs((y1 + y2) / 2 - y_n) < 20:
                canvas.delete(nave)
                canvas.delete(proj)
                naves_alien.remove(nave)
                projeteis.remove(proj)
                ganhar_pontos(100)
                break  # Evita erro se proj for removido

        # Remove se sair da tela
        if x1 > 500:
            canvas.delete(proj)
            if proj in projeteis:
                projeteis.remove(proj)

    root.after(50, mover_projeteis)


#Criar naves aliens
def criar_nave_alien():
    y = rd.randint(50, 300)
    nave = canvas.create_image(500, y, image=alien_img)  # Simples, você pode trocar por imagem
    naves_alien.append(nave)
    disparar_projeteis_alien(nave)
    root.after(1500, criar_nave_alien)  # Cria uma nave nova a cada 5 segundos


#Mover naves aliens
def mover_naves_alien():
    for nave in naves_alien[:]:
        canvas.move(nave, -2, 0)
        x, y = canvas.coords(nave)
        if x < 0:
            canvas.delete(nave)
            naves_alien.remove(nave)
    root.after(50, mover_naves_alien)

#Disparar naves aliens
def disparar_projeteis_alien(nave):
    for nave in naves_alien:
        x, y = canvas.coords(nave)
        proj = canvas.create_oval(x - 3, y - 5, x + 3, y + 5, fill="red")
        projeteis_alien.append(proj)
    root.after(2000, disparar_projeteis_alien)  # 2000ms = 2 segundos

#mover projeteis das naves aliens
def mover_projeteis_alien():
    global vidas
    for proj in projeteis_alien[:]:
        canvas.move(proj, -10, 0)
        x1, y1, x2, y2 = canvas.coords(proj)

        # Verifica colisão com a nave do jogador
        if nave:
            x_n, y_n = canvas.coords(nave)
            if abs((x1 + x2) / 2 - x_n) < 20 and abs((y1 + y2) / 2 - y_n) < 20:
                canvas.delete(proj)
                projeteis_alien.remove(proj)
                vidas -= 1
                atualizar_coracoes()
                if vidas == 0:
                    fim_do_jogo()
                continue

        # Remove se sair da tela
        if x2 < 0:
            canvas.delete(proj)
            if proj in projeteis_alien:
                projeteis_alien.remove(proj)

    root.after(30, mover_projeteis_alien)

#função de reniciar o jogo
def reiniciar_jogo():
    global vidas, pontuacao, nave

    # Resetar variáveis
    vidas = 3
    pontuacao = 0
    atualizar_coracoes()
    atualizar_pontuacao()

    # Apagar elementos antigos
    for item in naves_alien + projeteis + projeteis_alien:
        canvas.delete(item)
    naves_alien.clear()
    projeteis.clear()
    projeteis_alien.clear()

    if nave:
        canvas.delete(nave)

    # Esconder Game Over e botão
    label_game_over.destroy()
    botao_reiniciar.place_forget()
    # Recriar nave e reativar eventos
    nave = canvas.create_image(250, 200, image=nave_img)
    canvas.bind("<Motion>", mover_nave)
    canvas.bind("<Button-1>", disparar_projeteis)

    # Recomeçar animações
    criar_nave_alien()
    mover_naves_alien()
    mover_projeteis()
    mover_projeteis_alien()

#fim de jogo
def fim_do_jogo():
    canvas.unbind("<Motion>")
    canvas.unbind("<Button-1>")
    root.config(cursor="")
    global label_game_over
    label_game_over = tk.Label(root, text="GAME OVER", font=("Orbitron", 24, "bold"), fg="red", bg="black")
    label_game_over.place(x=135, y=120)
    botao_reiniciar.place(x=215, y=220)

def fim_do_jogo_esc():
    global nave

    # Pausar o jogo
    canvas.unbind("<Motion>")
    canvas.unbind("<Button-1>")
    root.config(cursor="")

    # Remove a nave se existir
    if nave:
        canvas.delete(nave)

    # Apaga inimigos e projéteis
    for item in naves_alien + projeteis + projeteis_alien:
        canvas.delete(item)
        naves_alien.clear()
        projeteis.clear()
        projeteis_alien.clear()

    # Exibe "PAUSADO" ou "REINICIAR"
    global label_game_over
    label_game_over = tk.Label(root, text="JOGO PAUSADO", font=("Orbitron", 24, "bold"), fg="yellow", bg="black")
    label_game_over.place(x=100, y=120)
    botao_reiniciar.place(x=215, y=220)


#Interface onde vai rodar as coisas
root = tk.Tk()
root.title("Star Strike")
root.geometry("500x400")  # Define o tamanho da janela
root.configure(bg="white")

# Criando um Canvas grande o suficiente
canvas = tk.Canvas(root, width=500, height=400, bg="black")
canvas.place(x=0, y=0, width=500, height=400)

#----------------------------------------------------------------------------------------------------------------#
for _ in range(200):
    x = rd.randint(0, 500)
    y = rd.randint(0, 400)
    estrela = canvas.create_oval(x, y, x + 2, y + 2, fill = "white")
    estrelas.append(estrela)

meteoros = []
for _ in range(50):
    x = rd.randint(0, 500)
    y = rd.randint(0, 300)
    meteoro = canvas.create_line(x, y, x + 10, y + 5, fill = "white")
    meteoros.append(meteoro)

# Criando o retângulo na parte inferior
retangulo_placar = canvas.create_rectangle(0, 350, 500, 400, fill= "gray")  # Mudei a altura do retângulo

#Região do placar
global placar
x1, y1, x2, y2 = canvas.coords(retangulo_placar)

#Pontuação dinâmica do placar
label_placar = tk.Label(root, text = f"Pontuação: {pontuacao}", font = ("Orbitron", 8, "bold"), bg = "gray", fg = "white")

#criando os corações com label
coração_placar = tk.Label(root, text="❤️ ❤️ ❤️", font=("Arial", 12), bg="gray", fg="red")

# Criando o label e centralizando
label_nome = tk.Label(root, text="Star Striker", font = ("Orbitron", 32), bg = "black", fg = "white")
label_nome.place(x = (500 - label_nome.winfo_reqwidth()) / 2, y = 20)
label_opcao = tk.Label(root, text="Menu", font=("Orbitron", 11, "bold"), fg = "white", bg="black")
label_opcao.place(x=(500 - label_opcao.winfo_reqwidth()) / 2, y=250)

# Criando o botão "Entrar" e centralizando
botao_entrar = tk.Button(root, text="Entrar no jogo", command=iniciar_jogo, font=("Orbitron", 8, "bold"), fg="white", bg="black")
botao_entrar.place(x=(500 - botao_entrar.winfo_reqwidth()) / 2, y=280)

# Criando o botão "Sair" e centralizando
botao_sair = tk.Button(root, text="Sair do jogo", command=sair, font=("Orbitron", 8, "bold"), fg="white", bg="black")
botao_sair.place(x=(500 - botao_sair.winfo_reqwidth()) / 2, y=310)

#botão de reniciar o jogo
botao_reiniciar = tk.Button(root, text="Reiniciar", font=("Orbitron", 10, "bold"), fg="white", bg="black", command=lambda: reiniciar_jogo())
botao_reiniciar.place_forget()

#Nave e aliens que vai ter animação
nave_img = tk.PhotoImage(file="C:/Users/Thiago/Documents/programas/vs_code/Jogo.py/assets/nave.png")
alien_img = tk.PhotoImage(file="C:/Users/Thiago/Documents/programas/vs_code/Jogo.py/assets/alien.png")

animar_fundo()
label_placar.place_forget()
root.mainloop()
