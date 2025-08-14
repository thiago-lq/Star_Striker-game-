import random as rd
from src.components import game_state as state
from src.components import animacao
#limites de tempo
tempo_naves_minimo = 500
tempo_disparos_minimo = 1000

botao_pressionado = state.botao_disparos

def iniciar_disparos(event=None):
    global botao_pressionado
    botao_pressionado = True
    disparo_continuo()

def parar_disparos(event=None):
    global botao_pressionado
    botao_pressionado = False
    
def disparo_continuo():
    if botao_pressionado:
        animacao.disparar_projeteis()
        state.root.after(300, disparo_continuo)

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
    state.root.after(state.tempo_naves, criar_nave_alien)
    if state.tempo_naves > tempo_naves_minimo:
        state.tempo_naves = state.tempo_naves - 25

# Disparar projéteis das naves aliens
def disparar_projeteis_alien(nave):
    coords = state.canvas.coords(nave)
    if not coords:  # Se lista estiver vazia, significa que a nave não existe mais
        return
    
    coordenada_dProjeteis_x, coordenada_dProjeteis_y = state.canvas.coords(nave)
    projetil = state.canvas.create_oval(
        coordenada_dProjeteis_x - 3, coordenada_dProjeteis_y - 5,
        coordenada_dProjeteis_x + 3, coordenada_dProjeteis_y + 5,
        fill="red"
    )
    state.projeteis_alien.append(projetil)
    # Dispara projéteis a cada 2 segundos
    state.root.after(state.tempo_disparos, lambda: disparar_projeteis_alien(nave))
    if state.tempo_disparos > tempo_disparos_minimo:
        state.tempo_disparos = state.tempo_disparos - 25
