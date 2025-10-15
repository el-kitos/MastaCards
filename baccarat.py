import pygame
import random
import sys
from blackjack import draw_button,draw_text,render_card,render_back_card,animate_card,create_deck,draw_hand
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
clock.tick(60)

card_images = {f"{rank}{suit}": render_card(f"{rank}{suit}") for suit in suits for rank in ranks}
card_back = render_back_card()

#Valores especiales de cartas
def card_valuesBaccarat():
    for rank in ranks:
        if rank in ["J", "Q", "K"]:
            value = 0
        elif rank == "A":
            value = 1
        else:
            value = int(rank)
            
def hand_valueBaccarat(hand):
    total = sum(card_valuesBaccarat()[card[:-1]] for card in hand)
    return total % 10

def mainNBaccarat():
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

    deck = create_deck()
    player_hand, dealer_hand = [], []

    for _ in range(2):
        card = deck.pop()
        player_hand.append(card)
        if sound_card: sound_card.play()
        animate_card(card_images[card], (ANCHO // 2, ALTO // 2), (100 + len(player_hand) * 70, 380))

        card_d = deck.pop()
        dealer_hand.append(card_d)
        if sound_card: sound_card.play()
        animate_card(card_images[card_d], (ANCHO // 2, ALTO // 2), (100 + len(dealer_hand) * 70, 100))

    stand = False
    game_over = False
    result = ""
    ronda_terminada = False

    rect_negro = pygame.Rect(0, 0, ANCHO, 550)
    #pygame.draw.rect(screen, BLACK , rect_negro, width=10) se dibuja bien tranquilay

    jugador_btn = pygame.Rect(50, 600, 180, 50)
    banca_btn = pygame.Rect(250, 600, 180, 50)
    apuesta_mas_btn = pygame.Rect(470, 600, 100, 50)
    apuesta_menos_btn = pygame.Rect(580, 600, 100, 50)
    salir_btn = pygame.Rect(700, 600, 180, 50)
    otra_ronda_btn = pygame.Rect(400, 400, 200, 50)

    while not ronda_terminada:
        screen.fill(GREEN_TABLE)
        pygame.draw.rect(screen, (20, 90, 20), (0, 550, ANCHO, 150))
        pygame.draw.rect(screen, BLACK , rect_negro, width=10)

        draw_text(f"{player['name']} - Dinero: ${player['money']}", 20, 20)
        draw_text(f"Apuesta: ${player['bet']}", 20, 60)

        draw_hand(player_hand, 380)
        draw_hand(dealer_hand, 100)

        draw_text(f"{player['name']}: {hand_valueBaccarat(player_hand)}", 100, 340)
        draw_text(f"Croupier: {hand_valueBaccarat(dealer_hand)}", 100, 200)

        if game_over:
                color = GREEN if "Ganaste" in result else RED if "Pierdes" in result else BLUE
                pygame.draw.rect(screen, BLACK, (280, 260, 440, 120), border_radius=15)
                pygame.draw.rect(screen, WHITE, (280, 260, 440, 120), 4, border_radius=15)
                draw_text(result, ANCHO // 2, 320, color, center=True, big=True)
                draw_button(otra_ronda_btn, "Otra ronda")

        draw_button(jugador_btn, "Jugador", not game_over)
        draw_button(banca_btn, "Banca", not game_over)
        draw_button(apuesta_mas_btn, "+50", not game_over and player["bet"] + 50 <= player["money"])
        draw_button(apuesta_menos_btn, "-50", not game_over and player["bet"] - 50 >= 50)
        draw_button(salir_btn, "Salir", True)

        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if salir_btn.collidepoint(event.pos):
                        pygame.quit(); sys.exit()

                    if not game_over:
                        if apuesta_mas_btn.collidepoint(event.pos) and player["bet"] + 50 <= player["money"]:
                            player["bet"] += 50
                        elif apuesta_menos_btn.collidepoint(event.pos) and player["bet"] - 50 >= 50:
                            player["bet"] -= 50