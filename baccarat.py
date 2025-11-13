import pygame
import random
import sys
import time
from Funciones_Poker import draw_button,draw_text,render_card,render_back_card,animate_card,create_deck,draw_hand
from Menu import menu_principal
#Cartas
suits = ['♠', '♥', '♦', '♣']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

# Colores
GREEN_TABLE = (39, 119, 20)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GOLD = (255, 215, 0)
RED = (200, 30, 30)
GRAY = (180, 180, 180)
BLUE = (30, 144, 255)
GREEN = (0, 200, 0)

try:
    sound_card = pygame.mixer.Sound("sounds/card.wav")
    sound_win = pygame.mixer.Sound("sounds/win.wav")
    sound_lose = pygame.mixer.Sound("sounds/lose.wav")
    sound_draw = pygame.mixer.Sound("sounds/draw.wav")
except:
    sound_card = sound_win = sound_lose = sound_draw = None


pygame.init()
ANCHO, ALTO = 1152, 700
screen = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Baccarat")
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 28, bold=True)



# === Pantalla de carga estilo casino ===
loading_font = pygame.font.SysFont("arial", 40, bold=True)
#7 mensajes de carga
mensajes = ["Preparando la mesa", "Esperando a los crupiers", "Barajando cartas", "Posicionando mazo", "Limpiando la mesa","Preparando fichas","Por favor espere" ]
card_images = {}
# Preparar lista de todas las cartas
mazo = [f"{rank}{suit}" for suit in suits for rank in ranks]
# Variables de animación
i = 0
mensaje_index = 0
puntos_animados = 0
loading = True

while loading:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Fondo con degradado
    for y in range(ALTO):
        color = (
            int(30 + (y / ALTO) * 50),
            int(100 + (y / ALTO) * 60),
            int(30 + (y / ALTO) * 30)
        )
        pygame.draw.line(screen, color, (0, y), (ANCHO, y))

    pygame.draw.rect(screen, (255, 215, 0), (50, 50, ANCHO - 100, ALTO - 150), 6, border_radius=30)

    # Mensaje animado
    mensaje = mensajes[mensaje_index % len(mensajes)]
    puntos = "." * ((puntos_animados // 10) % 4)
    text = loading_font.render(mensaje + puntos, True, WHITE)
    screen.blit(text, (ANCHO // 2 - text.get_width() // 2, ALTO // 2 - text.get_height() // 2))

    # Barra de progreso
    progreso = i / len(mazo)
    pygame.draw.rect(screen, (60, 60, 60), (200, ALTO - 100, ANCHO - 400, 25), border_radius=10)
    pygame.draw.rect(screen, (255, 215, 0), (200, ALTO - 100, int((ANCHO - 400) * progreso), 25), border_radius=10)

    # Renderizar solo 1 carta por frame
    if i < len(mazo):
        card_images[mazo[i]] = render_card(mazo[i], font)
        i += 1
    else:
        loading = False  # carga completa

    # Actualizar animación puntos y mensaje
    puntos_animados += 1
    if puntos_animados % 20 == 0:
        mensaje_index += 1

    pygame.display.flip()
    clock.tick(60)


# Valores especiales de cartas
def card_valuesBaccarat():
    return {
        "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9,
        "10": 0, "J": 0, "Q": 0, "K": 0, "A": 1
    }
            
def hand_valueBaccarat(hand):
    values = card_valuesBaccarat()
    total = sum(values[card[:-1]] for card in hand)
    return total % 10

def mainBaccarat():
    players = [
        {"name": "Jugador 1", "money": 1000, "bet": 100},
        {"name": "Jugador 2", "money": 1000, "bet": 100}
    ]
    stats = {"ganadas": 0, "perdidas": 0, "empatadas": 0}
    current_player = 0
    animaciones = []
    
    while any(player["money"] > 0 for player in players):
        player = players[current_player]
        if player["money"] <= 0:
            current_player = (current_player + 1) % 2
            continue

        deck = create_deck()
        player_hand, dealer_hand = [], []
        
        card_images = {f"{rank}{suit}": render_card(f"{rank}{suit}",font) for suit in suits for rank in ranks}
        card_back = render_back_card()

        for _ in range(2):
            card = deck.pop()
            player_hand.append(card)
            card_d = deck.pop()
            dealer_hand.append(card_d)

        eleccion = ""
        game_over = False
        result = ""
        ronda_terminada = False

        rect_negro = pygame.Rect(0, 0, ANCHO, 550)

        jugador_btn = pygame.Rect(50, 600, 180, 50)
        banca_btn = pygame.Rect(250, 600, 180, 50)
        apuesta_mas_btn = pygame.Rect(470, 600, 100, 50)
        apuesta_menos_btn = pygame.Rect(580, 600, 100, 50)
        salir_btn = pygame.Rect(700, 600, 180, 50)
        otra_ronda_btn = pygame.Rect(400, 400, 200, 50)

        screen.fill(GREEN_TABLE)
        # Indicador para asegurarse de iniciar las animaciones de reparto solo una vez por ronda
        deal_started = False
        while not ronda_terminada:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if salir_btn.collidepoint(event.pos):
                        return

                    # Si hay animaciones en curso, bloquear entradas de apuesta/elección
                    if animaciones:
                        # mientras se animan permitir solo 'salir'; ignorar otros clics
                        continue

                    if not game_over:
                        # allow changing bet only before choosing
                        if eleccion == "":
                            if apuesta_mas_btn.collidepoint(event.pos) and player["bet"] + 50 <= player["money"]:
                                player["bet"] += 50
                            elif apuesta_menos_btn.collidepoint(event.pos) and player["bet"] - 50 >= 50:
                                player["bet"] -= 50
                        # choosing player or banca triggers the deal (only if not chosen yet)
                        if eleccion == "":
                            if jugador_btn.collidepoint(event.pos):
                                eleccion = "Jugador"
                            elif banca_btn.collidepoint(event.pos):
                                eleccion = "Banca"

                    if game_over and otra_ronda_btn.collidepoint(event.pos):
                        player_hand.clear()
                        dealer_hand.clear()
                        ronda_terminada = True

            # Iniciar el reparto inicial solo después de que el jugador haya elegido (eleccion != "")
            if not deal_started and eleccion != "":
                # animar las cartas más recientemente añadidas (segunda carta de cada mano)
                p_card = player_hand[-1]
                d_card = dealer_hand[-1]
                if sound_card: sound_card.play()
                animaciones.append(animate_card(card_images[p_card], (ANCHO // 2, ALTO // 2), (100 + (len(player_hand)-1) * 70, 380), card_key=p_card, duration = 1000))
                if sound_card: sound_card.play()
                animaciones.append(animate_card(card_images[d_card], (ANCHO // 2, ALTO // 2), (100 + (len(dealer_hand)-1) * 70, 100), card_key=d_card, duration = 1000))
                deal_started = True

            # Limpiar la pantalla y dibujar la mesa y la interfaz
            screen.fill(GREEN_TABLE)
            pygame.draw.rect(screen, (20, 90, 20), (0, 550, ANCHO, 150))
            pygame.draw.rect(screen, BLACK , rect_negro, width=10)
            draw_text(f"{player['name']} - Masta Coins: ${player['money']}", 20, 20, screen)
            draw_text(f"Inversion: ${player['bet']}", 20, 60, screen)

            # Mostrar las manos y valores solo después de que el jugador haya elegido
            if eleccion != "" or game_over:
                draw_text(f"{player['name']}: {hand_valueBaccarat(player_hand)}", 100, 340, screen)
                draw_text(f"Croupier: {hand_valueBaccarat(dealer_hand)}", 100, 200, screen)

                # dibujar las manos (ocultar cualquier carta que se esté animando
                # dibujando el dorso en esa posición)
                animated_keys = {anim.card_key for anim in animaciones if getattr(anim, 'card_key', None)}
                for i, card in enumerate(player_hand):
                    if card in animated_keys:
                        screen.blit(card_back, (100 + i * 70, 380))
                    else:
                        screen.blit(card_images[card], (100 + i * 70, 380))
                for i, card in enumerate(dealer_hand):
                    if card in animated_keys:
                        screen.blit(card_back, (100 + i * 70, 100))
                    else:
                        screen.blit(card_images[card], (100 + i * 70, 100))
            else:
                # Before choice, hide hands and values (only show labels)
                draw_text(f"{player['name']}", 100, 340, screen)

            # Actualizar animaciones (no bloqueante)
            for anim in animaciones[:]:
                finished = anim.update(screen)
                if finished:
                    animaciones.remove(anim)
            # dibujar fotogramas de animación por encima de las manos
            for anim in animaciones:
                # anim.card_surf is the image to draw; anim.x/anim.y are current coords
                screen.blit(anim.card_surf, (anim.x, anim.y))

            # Después de que las animaciones terminan, evaluar el resultado si el jugador ya eligió
            if not animaciones and not game_over and eleccion != "":
                p_val = hand_valueBaccarat(player_hand)
                d_val = hand_valueBaccarat(dealer_hand)
                if eleccion == "Jugador":
                    if p_val > d_val:
                        result = "Ganaste"
                        player["money"] += player["bet"]
                        stats["ganadas"] += 1
                        if sound_win: sound_win.play()
                    elif p_val < d_val:
                        result = "Pierdes."
                        player["money"] -= player["bet"]
                        stats["perdidas"] += 1
                        if sound_lose: sound_lose.play()
                    else:
                        result = "Empate."
                elif eleccion == "Banca":
                    if d_val > p_val:
                        result = "Ganaste"
                        player["money"] += player["bet"]
                        stats["ganadas"] += 1
                        if sound_win: sound_win.play()
                    elif d_val < p_val:
                        result = "Pierdes."
                        player["money"] -= player["bet"]
                        stats["perdidas"] += 1
                        if sound_lose: sound_lose.play()
                    else:
                        result = "Empate."
                else:
                    result = "Empate."
                game_over = True
                eleccion = ""

            # dibujar botones y posible ventana de resultado
            if game_over:
                color = GREEN if "Ganaste" in result else RED if "Pierdes" in result else BLUE
                pygame.draw.rect(screen, BLACK, (280, 260, 440, 120), border_radius=15)
                pygame.draw.rect(screen, WHITE, (280, 260, 440, 120), 4, border_radius=15)
                draw_text(result, ANCHO // 2, 320, screen, color, center=True, big=True)
                draw_button(otra_ronda_btn,"Otra ronda", font, screen )

            # Si hay animaciones activas, desactivar botones de apuesta/elección hasta que terminen
            interactive = not animaciones and not game_over
            draw_button(jugador_btn, "Jugador", font, screen, interactive)
            draw_button(banca_btn, "Banca", font, screen, interactive)
            draw_button(apuesta_mas_btn, "+50", font, screen, interactive and player["bet"] + 50 <= player["money"])
            draw_button(apuesta_menos_btn, "-50", font, screen, interactive and player["bet"] - 50 >= 50)
            draw_button(salir_btn, "Salir", font, screen, True,)

            pygame.display.flip()
            clock.tick(60)

        current_player = (current_player + 1) % 2 


    menu_principal()  
    print("Fin del juego.")

if __name__ == "__main__":
    mainBaccarat()
