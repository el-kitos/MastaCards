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
    pass



