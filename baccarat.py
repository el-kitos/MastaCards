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



pygame.init()
ANCHO, ALTO = 1152, 700
pantalla = pygame.display.set_mode((ANCHO, ALTO))
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
            


def mainNBaccarat():
    players = [
        {"name": "Jugador 1", "money": 1000, "bet": 100},
        {"name": "Jugador 2", "money": 1000, "bet": 100}
    ]
    stats = {"ganadas": 0, "perdidas": 0, "empatadas": 0}
    current_player = 0

    deck = create_deck()
    player_hand, dealer_hand = [], []

    


