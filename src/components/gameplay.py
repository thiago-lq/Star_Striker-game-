import random as rd
from src.components import game_state as state
#limites de tempo
tempo_naves = 1500
tempo_disparos = 2000

# Criar naves aliens
def criar_nave_alien():
    if not state.nave_alien_ativa:
        return
    coordenada_nave_y = rd.randint(50, 300)
    nave = state.canvas.create_image(500, coordenada_nave_y, image=state.alien_img)
    state.naves_alien.append(nave)
    # Passa a nave recém-criada para disparar projéteis
    disparar_projeteis_alien(nave)
    # Continua criando naves a cada 1,5 segundos
    state.root.after(tempo, criar_nave_alien)
    tempo -= 10

# Disparar projéteis das naves aliens
def disparar_projeteis_alien(nave):
    coordenada_dProjeteis_x, coordenada_dProjeteis_y = state.canvas.coords(nave)
    projetil = state.canvas.create_oval(
        coordenada_dProjeteis_x - 3, coordenada_dProjeteis_y - 5,
        coordenada_dProjeteis_x + 3, coordenada_dProjeteis_y + 5,
        fill="red"
    )
    state.projeteis_alien.append(projetil)
    # Dispara projéteis a cada 2 segundos
    state.root.after(2000, lambda: disparar_projeteis_alien(nave))
