from src.components import game_state as state
from src.components import animacao, gameplay

# Funções de pontuação e vidas
def atualizar_coracoes():
    coracoes = "❤️" * state.vidas
    coração_placar.config(text=coracoes.strip())

def atualizar_pontuacao():
    label_placar.config(text=f"Pontuação: {state.pontuacao}")

def ganhar_pontos(valor):
    state.pontuacao += valor
    atualizar_pontuacao()

# Fim do jogo
def fim_do_jogo():
    state.canvas.unbind("<Motion>")
    state.canvas.unbind("<ButtonPress-1>", "ButtonRelease-1")
    state.root.config(cursor="")
    if state.nave:
        state.canvas.delete(state.nave)
    for item in state.naves_alien + state.projeteis + state.projeteis_alien:
        state.canvas.delete(item)
    state.naves_alien.clear()
    state.projeteis.clear()
    state.projeteis_alien.clear()
    state.nave_alien_ativa = False
    state.projeteis_alien_ativos = False
    state.tempo_disparos = 2000
    state.tempo_naves = 1500
    global label_game_over
    label_game_over = state.tk.Label(state.root, text="GAME OVER", font=("Orbitron", 24, "bold"), fg="red", bg="black")
    label_game_over.place(x=135, y=120)
    botao_reiniciar.place(x=215, y=220)

def fim_do_jogo_esc():
    state.canvas.unbind("<Motion>")
    state.canvas.unbind("<Button-1>")
    state.root.config(cursor="")
    state.nave_alien_ativa = False
    state.projeteis_alien_ativos = False
    global label_game_over
    label_game_over = state.tk.Label(state.root, text="JOGO PAUSADO", font=("Orbitron", 24, "bold"), fg="yellow", bg="black")
    label_game_over.place(x=100, y=120)
    botao_reiniciar.place(x=215, y=220)
    botao_resumir.place(x=210, y=180)

# Iniciar jogo
def iniciar_jogo():
    label_opcao.place_forget()
    label_nome.place_forget()
    botao_entrar.place_forget()
    botao_sair.place_forget()
    label_placar.place(x=10, y=(y1 + y2 - label_placar.winfo_reqheight()) / 2)
    coração_placar.place(x=375, y=(y1 + y2 - coração_placar.winfo_reqheight()) / 2)
    state.nave_alien_ativa = True
    state.projeteis_alien_ativos = True

    state.nave = state.canvas.create_image(250, 200, image=state.nave_img)
    state.canvas.bind("<Motion>", animacao.mover_nave)
    state.canvas.bind("<ButtonPress-1>", gameplay.iniciar_disparos)
    state.canvas.bind("<ButtonRelease-1>", gameplay.parar_disparos)
    # Passa callbacks
    animacao.mover_projeteis(ganhar_pontos)
    animacao.mover_projeteis_alien(atualizar_coracoes, fim_do_jogo)
    animacao.mover_naves_alien()
    gameplay.criar_nave_alien()

    state.root.config(cursor="none")
    state.root.bind("<Escape>", lambda event: fim_do_jogo_esc())

# Reiniciar jogo
def reiniciar_jogo():
    state.vidas = 3
    state.pontuacao = 0
    atualizar_coracoes()
    atualizar_pontuacao()

    if state.nave:
        state.canvas.delete(state.nave)
    for item in state.naves_alien + state.projeteis + state.projeteis_alien:
        state.canvas.delete(item)
    state.naves_alien.clear()
    state.projeteis.clear()
    state.projeteis_alien.clear()

    if 'label_game_over' in globals():
        label_game_over.destroy()
    botao_reiniciar.place_forget()
    botao_resumir.place_forget()
    
    state.nave_alien_ativa = True
    state.projeteis_alien_ativos = True
    state.tempo_naves = 1500
    state.tempo_disparos = 2000
    state.nave = state.canvas.create_image(250, 200, image=state.nave_img)
    state.canvas.bind("<Motion>", animacao.mover_nave)
    state.canvas.bind("<ButtonPress-1>", gameplay.iniciar_disparos)
    state.canvas.bind("<ButtonRelease-1>", gameplay.parar_disparos)

    animacao.mover_projeteis(ganhar_pontos)
    animacao.mover_projeteis_alien(atualizar_coracoes, fim_do_jogo)
    animacao.mover_naves_alien()
    gameplay.criar_nave_alien()

def resumir_jogo():
    if 'label_game_over' in globals():
        label_game_over.destroy()
    botao_reiniciar.place_forget()
    botao_resumir.place_forget()
    state.nave_alien_ativa = True
    state.projeteis_alien_ativos = True
    state.canvas.bind("<Motion>", animacao.mover_nave)
    state.canvas.bind("<ButtonPress-1>", gameplay.iniciar_disparos)
    state.canvas.bind("<ButtonRelease-1>", gameplay.parar_disparos)

    animacao.mover_projeteis(ganhar_pontos)
    animacao.mover_projeteis_alien(atualizar_coracoes, fim_do_jogo)
    animacao.mover_naves_alien()
    gameplay.criar_nave_alien()
    

# ------------------------------------------------------------------------------------------------------
# Configuração da interface
retangulo_placar = state.canvas.create_rectangle(0, 350, 500, 400, fill="gray")
x1, y1, x2, y2 = state.canvas.coords(retangulo_placar)

label_placar = state.tk.Label(state.root, text=f"Pontuação: {state.pontuacao}", font=("Orbitron", 8, "bold"), bg="gray", fg="white")
coração_placar = state.tk.Label(state.root, text="❤️ ❤️ ❤️", font=("Arial", 12), bg="gray", fg="red")

label_nome = state.tk.Label(state.root, text="Star Striker", font=("Orbitron", 32), bg="black", fg="white")
label_nome.place(x=(500 - label_nome.winfo_reqwidth()) / 2, y=20)
label_opcao = state.tk.Label(state.root, text="Menu", font=("Orbitron", 11, "bold"), fg="white", bg="black")
label_opcao.place(x=(500 - label_opcao.winfo_reqwidth()) / 2, y=250)

botao_entrar = state.tk.Button(state.root, text="Entrar no jogo", command=iniciar_jogo, font=("Orbitron", 8, "bold"), fg="white", bg="black")
botao_entrar.place(x=(500 - botao_entrar.winfo_reqwidth()) / 2, y=280)

botao_sair = state.tk.Button(state.root, text="Sair do jogo", command=lambda: state.root.quit(), font=("Orbitron", 8, "bold"), fg="white", bg="black")
botao_sair.place(x=(500 - botao_sair.winfo_reqwidth()) / 2, y=310)

botao_reiniciar = state.tk.Button(state.root, text="Reiniciar", font=("Orbitron", 10, "bold"), fg="white", bg="black", command=reiniciar_jogo)
botao_reiniciar.place_forget()

botao_resumir = state.tk.Button(state.root, text="Continuar", font=("Orbitron", 10, "bold"), fg="white", bg="black", command = resumir_jogo)
botao_resumir.place_forget()

# Iniciar animação do fundo
animacao.animar_fundo()
label_placar.place_forget()

state.root.mainloop()
