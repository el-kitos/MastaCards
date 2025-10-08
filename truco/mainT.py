"""
Archivo de entrada: inicializa Pygame, muestra el menu y ejecuta las pantallas.
"""
import pygame
from truco.menu import Menu
from truco.juego import Game
from truco.data_manager import load_history
import sys


SCREEN_W = 1000
SCREEN_H = 700

def mainTruco():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption("Truco Argentino")

    menu = Menu(screen)

    while True:
        choice = menu.run()
        if choice == "Salir" or choice == "salir":
            pygame.quit()
            sys.exit(0)
        elif choice == "Jugar partida":
            # Preguntar modo (vs IA por defecto)
            game = Game(screen, vs_ai=True, player_name="Jugador")
            res = game.play()
            if res == "salir":
                pygame.quit()
                sys.exit(0)
            # volver al menu
        elif choice == "Ver reglas":
            show_rules(screen)
        elif choice == "Historial / Puntajes":
            show_history(screen)

def show_rules(screen):
    font = pygame.font.SysFont("arial", 18)
    rules = [
        "Reglas (simplificadas):",
        "- Se reparten 3 cartas a cada jugador.",
        "- Se juegan hasta 3 manos por ronda; quien gana 2 manos gana la ronda.",
        "- Orden de cartas (mayor a menor simplificado): 1,3,2,12,11,10,7,6,5,4",
        "- Se puede cantar Truco (T) para subir puntos. El otro puede aceptar o rechazar.",
        "- Se puede cantar Envido (E) antes de jugar cartas para ganar puntos por combinacion de palo.",
        "- Historial y puntajes se guardan en data/history.json"
    ]
    showing = True
    while showing:
        screen.fill((50,50,100))
        y = 50
        for line in rules:
            txt = font.render(line, True, (255,255,255))
            screen.blit(txt, (40, y))
            y += 30
        txt2 = font.render("Presione ESC para volver", True, (255,255,200))
        screen.blit(txt2, (40, y+20))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                showing = False

def show_history(screen):
    font = pygame.font.SysFont("arial", 18)
    hist = load_history()
    showing = True
    scroll = 0
    while showing:
        screen.fill((30,30,30))
        y = 30
        title = pygame.font.SysFont("arial", 28, bold=True).render("Historial de partidas", True, (255,255,255))
        screen.blit(title, (40, 5))
        for i, h in enumerate(reversed(hist[-30:])):  # mostrar últimas 30
            txt = font.render(f"{i+1}. Ganador: {h.get('winner', h.get('hand_winner','-'))}  P:{h.get('player_score','-')} - CPU:{h.get('cpu_score','-')}", True, (200,200,200))
            screen.blit(txt, (40, y + i*24 - scroll))
        info = font.render("Arriba/Abajo: Scroll  ESC: volver", True, (255,255,255))
        screen.blit(info, (40, SCREEN_H-30))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    showing = False
                if event.key == pygame.K_UP:
                    scroll = max(0, scroll-24)
                if event.key == pygame.K_DOWN:
                    scroll += 24

if __name__ == "__main__":
    mainTruco()
