import random as rd
from src.components import game_state as state

def resetar_movimento_projeteis():
    state.projeteis = []

# Criar estrelas
for _ in range(200):
    x = rd.randint(0, 500)
    y = rd.randint(0, 400)
    estrela = state.canvas.create_oval(x, y, x + 2, y + 2, fill="white")
    state.estrelas.append(estrela)

# Criar meteoros
for _ in range(50):
    x = rd.randint(0, 500)
    y = rd.randint(0, 300)
    meteoro = state.canvas.create_line(x, y, x + 10, y + 5, fill="white")
    state.meteoros.append(meteoro)

# Animação do fundo
def animar_fundo():
    for i, estrela in enumerate(state.estrelas):
        state.canvas.move(estrela, -2, 0)
        coords = state.canvas.coords(estrela)
        if coords[2] < 0:
            x_new = 500 + rd.randint(0, 50)
            y_new = rd.randint(0, 400)
            state.canvas.coords(estrela, x_new, y_new, x_new + 2, y_new + 2)

    for i, meteoro in enumerate(state.meteoros):
        state.canvas.move(meteoro, -4, 0)
        if state.canvas.coords(meteoro)[0] < 0:
            x_new = 500 + rd.randint(0, 100)
            y_new = rd.randint(0, 300)
            state.canvas.coords(meteoro, x_new, y_new, x_new + 10, y_new + 5)

    state.root.after(50, animar_fundo)

# Movimento da nave
def mover_nave(event):
    if state.nave:
        state.canvas.coords(state.nave, event.x, event.y)

# Disparo da nave
def disparar_projeteis():
    if not state.nave:
        return
    x, y = state.canvas.coords(state.nave)

    proj_cima = state.canvas.create_oval(x - 3, y - 15, x + 3, y - 5, fill="yellow")
    proj_baixo = state.canvas.create_oval(x - 3, y + 5, x + 3, y + 15, fill="yellow")
    state.projeteis.extend([proj_cima, proj_baixo])

# Movimentar projéteis da nave
def mover_projeteis(ganhar_pontos_func):
    for proj in state.projeteis[:]:
        state.canvas.move(proj, 10, 0)
        x1, y1, x2, y2 = state.canvas.coords(proj)

        # Colisão com naves alien
        for nave in state.naves_alien[:]:
            nx, ny = state.canvas.coords(nave)
            if abs((x1 + x2) / 2 - nx) < 20 and abs((y1 + y2) / 2 - ny) < 20:
                state.canvas.delete(nave)
                state.canvas.delete(proj)
                state.naves_alien.remove(nave)
                state.projeteis.remove(proj)
                ganhar_pontos_func(100)
                break

        if x1 > 500:
            state.canvas.delete(proj)
            if proj in state.projeteis:
                state.projeteis.remove(proj)

    state.root.after(50, lambda: mover_projeteis(ganhar_pontos_func))

# Movimentar naves alienígenas
def mover_naves_alien():
    if not state.nave_alien_ativa:  # Para o loop se flag for False
        return

    for nave in state.naves_alien[:]:
        state.canvas.move(nave, -2, 0)
        if state.canvas.coords(nave)[0] < 0:
            state.canvas.delete(nave)
            state.naves_alien.remove(nave)

    state.root.after(50, mover_naves_alien)

# Movimentar projéteis alienígenas
def mover_projeteis_alien(atualizar_coracoes_func, fim_do_jogo_func):
    if not state.projeteis_alien_ativos:  # Para o loop se flag for False
        return

    for proj in state.projeteis_alien[:]:
        state.canvas.move(proj, -10, 0)
        x1, y1, x2, y2 = state.canvas.coords(proj)

        if state.nave:
            nx, ny = state.canvas.coords(state.nave)
            if abs((x1 + x2)/2 - nx) < 20 and abs((y1 + y2)/2 - ny) < 20:
                state.canvas.delete(proj)
                if proj in state.projeteis_alien:
                    state.projeteis_alien.remove(proj)
                state.vidas -= 1
                atualizar_coracoes_func()
                if state.vidas == 0:
                    fim_do_jogo_func()
                continue

        if x2 < 0:
            state.canvas.delete(proj)
            if proj in state.projeteis_alien:
                state.projeteis_alien.remove(proj)

    state.root.after(30, lambda: mover_projeteis_alien(atualizar_coracoes_func, fim_do_jogo_func))