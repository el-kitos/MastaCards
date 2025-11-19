import pygame
import random
import sys
from Funciones_Poker import draw_button,draw_text,render_card,render_back_card,animate_card,create_deck,card_value,hand_value,draw_hand

# Inicialización

pygame.init()
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Blackjack")
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 28, bold=True)

# Colores
GREEN_TABLE = (39, 119, 20)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GOLD = (255, 215, 0)
RED = (200, 30, 30)
GRAY = (180, 180, 180)
BLUE = (30, 144, 255)
GREEN = (0, 200, 0)

# Sonidos
try:
    sound_card = pygame.mixer.Sound("sounds/card.wav")
    sound_win = pygame.mixer.Sound("sounds/win.wav")
    sound_lose = pygame.mixer.Sound("sounds/lose.wav")
    sound_draw = pygame.mixer.Sound("sounds/draw.wav")
except:
    sound_card = sound_win = sound_lose = sound_draw = None



# Cartas
suits = ['♠', '♥', '♦', '♣']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

card_images = {f"{rank}{suit}": render_card(f"{rank}{suit}",font) for suit in suits for rank in ranks}
card_back = render_back_card()

# Juego principal
def mainBlackjack():
    players = [
        {"name": "Jugador 1", "money": 1000, "bet": 100},
        {"name": "Jugador 2", "money": 1000, "bet": 100}
    ]
    stats = {"ganadas": 0, "perdidas": 0, "empatadas": 0}
    current_player = 0

    while any(player["money"] > 0 for player in players):
        player = players[current_player]
        if player["money"] <= 0:
            current_player = (current_player + 1) % 2
            continue

        # FASE DE APUESTA (se salta al inicio para iniciar animación directamente)
        
        ajustar_apuesta = True
        btns_y = 600
        spacing = 20
        btn_width = 150
        apuesta_mas_btn = pygame.Rect(50, btns_y, btn_width, 50)
        apuesta_menos_btn = pygame.Rect(50 + (btn_width + spacing), btns_y, btn_width, 50)
        confirmar_apuesta_btn = pygame.Rect(50 + 2*(btn_width + spacing), btns_y, btn_width, 50)
        salir_btn = pygame.Rect(50 + 3*(btn_width + spacing), btns_y, btn_width, 50)
        

        while ajustar_apuesta:
            screen.fill(GREEN_TABLE)
            draw_text(f"{player['name']} - Masta Coins: ${player['money']}", 20, 20, screen)
            draw_text(f"Inversion: ${player['bet']}", 20, 60, screen)

            draw_button(apuesta_mas_btn, "+50", font, screen, player["bet"] + 50 <= player["money"])
            draw_button(apuesta_menos_btn, "-50", font, screen, player["bet"] - 50 >= 50)
            draw_button(confirmar_apuesta_btn, "Confirmar", font, screen, True)
            draw_button(salir_btn, "Salir", font, screen, True)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if salir_btn.collidepoint(event.pos):
                        return
                    elif apuesta_mas_btn.collidepoint(event.pos) and player["bet"] + 50 <= player["money"]:
                        player["bet"] += 50
                    elif apuesta_menos_btn.collidepoint(event.pos) and player["bet"] - 50 >= 50:
                        player["bet"] -= 50
                    elif confirmar_apuesta_btn.collidepoint(event.pos):
                        ajustar_apuesta = False

            pygame.display.flip()
            clock.tick(30)

        # -----------------------------
        # REPARTO DE CARTAS INICIAL
        # -----------------------------
        deck = create_deck()
        player_hand, dealer_hand = [], []
        animaciones = []
        pending_dealer_resolution = False

        for _ in range(2):
            card = deck.pop()
            player_hand.append(card)
            if sound_card: sound_card.play()
            anim = animate_card(card_images[card], (WIDTH // 2, HEIGHT // 2), (100 + len(player_hand) * 70, 380), card_key=card, duration = 1000)
            animaciones.append(anim)

            card_d = deck.pop()
            dealer_hand.append(card_d)
            if sound_card: sound_card.play()
            anim_d = animate_card(card_images[card_d], (WIDTH // 2, HEIGHT // 2), (100 + len(dealer_hand) * 70, 100), card_key=card_d, duration = 1000)
            animaciones.append(anim_d)

        # -----------------------------
        # BUCLE DE JUEGO DEL JUGADOR
        # -----------------------------
        stand = False
        game_over = False
        result = ""
        ronda_terminada = False

        # Botones del juego
        pedir_btn = pygame.Rect(15, btns_y, 200, 50)
        plantarse_btn = pygame.Rect(50 + (btn_width + spacing), btns_y, 180, 50)
        doblar_btn = pygame.Rect(65 + 2*(btn_width + spacing), btns_y, btn_width, 50)
        split_btn = pygame.Rect(55 + 3*(btn_width + spacing), btns_y, btn_width, 50)
        otra_ronda_btn = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 30, 200, 50)
        siguienteMano_btn = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 30, 200, 50)  # Misma posición que otra_ronda_btn
        salir_btn = pygame.Rect(50 + 4*(btn_width + spacing), btns_y, btn_width, 50)


        # Agregar variables para control de split
        is_split = False
        split_hands = []
        current_split_hand = 0
        split_results = ["", ""]  # Guardar resultados de cada mano split

        while not ronda_terminada:
            screen.fill(GREEN_TABLE)
            pygame.draw.rect(screen, (20, 90, 20), (0, 550, WIDTH, 150))
            pygame.draw.rect(screen, BLACK, (0,0,WIDTH,550), width=10)

            draw_text(f"{player['name']} - Masta Coins: ${player['money']}", 20, 20, screen)
            draw_text(f"Inversion: ${player['bet']}", 20, 60, screen)

            # Dibujar cartas
            draw_hand(player_hand, 380, card_back, card_images, screen)
            if stand or game_over:
                draw_hand(dealer_hand, 100, card_back, card_images, screen)
            else:
                draw_hand(dealer_hand, 100, card_back, card_images, screen, hide_first=True)

            draw_text(f"{player['name']}: {hand_value(player_hand)}", 100, 340, screen)
            if stand or game_over:
                draw_text(f"Croupier: {hand_value(dealer_hand)}", 100, 200, screen)

            # Botones activos/inactivos (solo si no hay game over)
            if not game_over:
                draw_button(pedir_btn, "Pedir Carta", font, screen, True)
                draw_button(plantarse_btn, "Plantarse", font, screen, True)
                draw_button(doblar_btn, "Doblar", font, screen, len(player_hand) == 2 and player["money"] >= player["bet"])
                draw_button(split_btn, "Split", font, screen, len(player_hand) == 2 and player_hand[0][:-1] == player_hand[1][:-1] and player["money"] >= player["bet"])
            
            draw_button(salir_btn, "Salir", font, screen, True)

            # Mostrar indicador de mano actual si hay split
            if is_split:
                draw_text(f"Jugando Mano {current_split_hand + 1} de 2", WIDTH//2, 280, screen, WHITE, center=True)

            # Resultado y botón de otra ronda
            if game_over:
                color = GREEN if "Ganaste" in result else RED if "Pierdes" in result else BLUE
                pygame.draw.rect(screen, BLACK, (280, 260, 440, 120), border_radius=15)
                pygame.draw.rect(screen, WHITE, (280, 260, 440, 120), 4, border_radius=15)
                
                if is_split:
                    # Guardar el resultado de la mano actual
                    split_results[current_split_hand] = result
                    if current_split_hand == 0:
                        # Primera mano: mostrar resultado y botón de continuar
                        draw_text(f"Mano 1: {result}", WIDTH//2, 320, screen, color, center=True, big=True)
                        draw_button(siguienteMano_btn, "Siguiente Mano", font, screen, True)
                    else:
                        # Segunda mano: mostrar ambos resultados
                        draw_text(f"Mano 1: {split_results[0]}", WIDTH//2, 300, screen, color, center=True)
                        draw_text(f"Mano 2: {split_results[1]}", WIDTH//2, 340, screen, color, center=True)
                        draw_button(otra_ronda_btn, "Otra ronda", font, screen, True)
                else:
                    draw_text(result, WIDTH//2, 320, screen, color, center=True, big=True)
                    draw_button(otra_ronda_btn, "Otra ronda", font, screen, True)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if salir_btn.collidepoint(event.pos):
                        return
                    # Si hay game over, manejar los botones de siguiente mano y otra ronda
                    if game_over:
                        if is_split and current_split_hand == 0 and siguienteMano_btn.collidepoint(event.pos):
                            # Cambiar a la segunda mano
                            current_split_hand += 1
                            player_hand = split_hands[current_split_hand]
                            stand = False
                            game_over = False
                            result = ""
                            # Resetear la mano del crupier para la segunda mano
                            dealer_hand = dealer_hand[:2]  # Mantener solo las dos primeras cartas
                            pending_dealer_resolution = False
                            continue
                        elif otra_ronda_btn.collidepoint(event.pos):
                            ronda_terminada = True
                            continue
                        continue

                    # Pedir carta
                    if pedir_btn.collidepoint(event.pos):
                        card = deck.pop()
                        player_hand.append(card)
                        if sound_card: sound_card.play()
                        anim = animate_card(card_images[card], (WIDTH//2, HEIGHT//2), (100 + len(player_hand)*70, 380), card_key=card, duration = 1000)
                        animaciones.append(anim)
                        if hand_value(player_hand) > 21:
                            result = "¡Te pasaste! Pierdes."
                            player["money"] -= player["bet"]
                            stats["perdidas"] += 1
                            if sound_lose: sound_lose.play()
                            game_over = True
                    # Plantarse
                    elif plantarse_btn.collidepoint(event.pos):
                        stand = True
                        # Encolar cartas del crupier y sus animaciones; la evaluación se hará cuando terminen las animaciones
                        while hand_value(dealer_hand) < 17:
                            card = deck.pop()
                            dealer_hand.append(card)
                            if sound_card: sound_card.play()
                            anim = animate_card(card_images[card], (WIDTH//2, HEIGHT//2), (100 + len(dealer_hand)*70, 100), card_key=card, duration = 1000)
                            animaciones.append(anim)
                        pending_dealer_resolution = True
                    # Doblar
                    elif doblar_btn.collidepoint(event.pos):
                        # Doblar: duplicar la apuesta, pedir exactamente una carta y plantarse.
                        # No reiniciamos la mano; si se pasa, se aplica la pérdida.
                        if player["money"] >= player["bet"]:
                            # sacar una carta del mazo
                            card = deck.pop()
                            player_hand.append(card)
                            if sound_card: sound_card.play()
                            # duplicar la apuesta (no restamos ahora; se aplica al resolver)
                            player["bet"] *= 2
                            # encolar animación de la carta recibida
                            anim = animate_card(card_images[card], (WIDTH//2, HEIGHT//2), (100 + len(player_hand)*70, 380), card_key=card, duration = 1000)
                            animaciones.append(anim)
                            # el jugador se planta automáticamente tras doblar
                            stand = True
                            # si al doblar se pasa, terminar la ronda
                            if hand_value(player_hand) > 21:
                                result = "¡Te pasaste! Pierdes."
                                # al perder se resta la apuesta actual (ya duplicada)
                                player["money"] -= player["bet"]
                                stats["perdidas"] += 1
                                if sound_lose: sound_lose.play()
                                # Mostrar el resultado, pero no reiniciar la mano automáticamente;
                                # el jugador deberá pulsar 'Otra ronda' para avanzar.
                                game_over = True
                    # Split (solo efecto visual básico, puedes ampliar)
                    elif split_btn.collidepoint(event.pos):
                        if len(player_hand) == 2 and player_hand[0][:-1] == player_hand[1][:-1] and player["money"] >= player["bet"]:
                            is_split = True
                            # Crear las dos manos separadas
                            split_hands = [[player_hand[0]], [player_hand[1]]]
                            player_hand = split_hands[0]  # Comenzar con la primera mano
                            # Dar una carta nueva a cada mano
                            for hand in split_hands:
                                card = deck.pop()
                                hand.append(card)
                                if sound_card: sound_card.play()
                                anim = animate_card(card_images[card], (WIDTH//2, HEIGHT//2), (100 + len(hand)*70, 380), card_key=card, duration = 1000)
                                animaciones.append(anim)
                            
                            player["money"] -= player["bet"]  # Descontar la apuesta adicional
                            stand = False
                            game_over = False

            # Actualizar animaciones (no bloqueante) y dibujarlas
            for anim in animaciones[:]:
                finished = anim.update(screen)
                if finished:
                    animaciones.remove(anim)
            for anim in animaciones:
                screen.blit(anim.card_surf, (anim.x, anim.y))

            # Si las animaciones terminaron y estamos esperando resolver la mano del crupier
            if not animaciones and pending_dealer_resolution:
                # Evaluar ganador ahora que el crupier terminó
                p_val = hand_value(player_hand)
                d_val = hand_value(dealer_hand)
                if d_val > 21 or p_val > d_val:
                    result = "¡Ganaste!"
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
                    stats["empatadas"] += 1
                    if sound_draw: sound_draw.play()
                game_over = True
                pending_dealer_resolution = False
            # Finalmente, actualizar la pantalla después de dibujar animaciones
            pygame.display.flip()
            clock.tick(30)

        current_player = (current_player + 1) % 2

    print("Fin del juego.")


if __name__ == "__main__":
    mainBlackjack()
