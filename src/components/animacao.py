import random as rd
from src.components import game_state as state

def resetar_movimento_projeteis():
    state.projeteis = []

# Criar estrelas
for _ in range(200):
    x = rd.randint(0, 720)
    y = rd.randint(0, 400)
    estrela = state.canvas.create_oval(x, y, x + 2, y + 2, fill="white")
    state.estrelas.append(estrela)

# Criar meteoros
for _ in range(50):
    x = rd.randint(0, 720)
    y = rd.randint(0, 400)
    meteoro = state.canvas.create_line(x, y, x + 10, y + 5, fill="white")
    state.meteoros.append(meteoro)

def animar_fundo():
    for i, estrela in enumerate(state.estrelas):
        state.canvas.move(estrela, -2, 0)
        coords = state.canvas.coords(estrela)
        if coords[2] < 0:
            x_new = 720 + rd.randint(0, 50)
            y_new = rd.randint(0, 400)
            state.canvas.coords(estrela, x_new, y_new, x_new + 2, y_new + 2)

    for i, meteoro in enumerate(state.meteoros):
        state.canvas.move(meteoro, -4, 0)
        if state.canvas.coords(meteoro)[0] < 0:
            x_new = 720 + rd.randint(0, 100)
            y_new = rd.randint(0, 400)
            state.canvas.coords(meteoro, x_new, y_new, x_new + 10, y_new + 5)

    state.root.after(50, animar_fundo)


def mover_nave(event):
    if state.nave:
        y_limitado = max(0, min(event.y, 400)) # Limita y entre 0 e 420
        state.canvas.coords(state.nave, event.x, y_limitado)



def disparar_projeteis():
    if not state.nave: # Verifica se existe uma nave
        return
    x, y = state.canvas.coords(state.nave)

    proj_cima = state.canvas.create_oval(x - 5, y - 17, x + 5, y - 7, fill="blue")
    proj_baixo = state.canvas.create_oval(x - 5, y + 7, x + 5, y + 17, fill="blue")
    state.projeteis.extend([proj_cima, proj_baixo])


def mover_projeteis(ganhar_pontos_func):
    if not state.projeteis_ativos: # Verifica se projeteis estão ativos
        return
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
                state.canvas.create_image(nx, ny, image=state.explosao_img, tag="explosao")
                state.projeteis.remove(proj)
                ganhar_pontos_func(100)
                state.canvas.after(300, lambda t="explosao": state.canvas.delete(t))
                break
        # Verifica se projéteis saíram da tela
        if x1 > 720:
            state.canvas.delete(proj)
            if proj in state.projeteis:
                state.projeteis.remove(proj)

    state.root.after(25, lambda: mover_projeteis(ganhar_pontos_func))


def mover_naves_alien():
    if not state.nave_alien_ativa: # Verifica se naves alien estão ativas
        return
    
    for nave in state.naves_alien[:]:
        state.canvas.move(nave, -2, 0)
        if state.canvas.coords(nave)[0] < 0:
            state.canvas.delete(nave)
            state.naves_alien.remove(nave)

    state.root.after(50, mover_naves_alien)

def mover_projeteis_alien(atualizar_coracoes_func, fim_do_jogo_func):
    if not state.projeteis_alien_ativos: # Verifica se projeteis alien estão ativos
        return

    for proj in state.projeteis_alien[:]:
        state.canvas.move(proj, -10, 0)
        x1, y1, x2, y2 = state.canvas.coords(proj)

        # Verifica se projéteis alien atingiram a nave do jogador
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

        if x2 < 0: # Verifica se projéteis dos aliens saíram da tela
            state.canvas.delete(proj)
            if proj in state.projeteis_alien:
                state.projeteis_alien.remove(proj)

    state.root.after(30, lambda: mover_projeteis_alien(atualizar_coracoes_func, fim_do_jogo_func))