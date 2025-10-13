"""
Funciones utilitarias: dibujo de cartas fallback, textos, manejo básico de eventos.
"""

import pygame
from typing import Tuple
from cartas import Card
import os

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "..", "assets")
CARDS_DIR = os.path.join(ASSETS_DIR, "cards")

def load_card_image(card: Card, size: Tuple[int,int]) -> pygame.Surface:
    """
    Intenta cargar la imagen en assets/cards/<id>.png, si no existe genera un surface dibujado.
    id ejemplo: 1_espadas.png
    """
    filename = f"{card.id()}.png"
    path = os.path.join(CARDS_DIR, filename)
    if os.path.exists(path):
        try:
            img = pygame.image.load(path).convert_alpha()
            return pygame.transform.smoothscale(img, size)
        except Exception:
            pass
    # fallback: dibujar rectángulo con texto
    surface = pygame.Surface(size)
    surface.fill((255,255,255))
    pygame.draw.rect(surface, (0,0,0), surface.get_rect(), 2)
    font = pygame.font.SysFont("arial", 20, bold=True)
    lines = [str(card.rank), card.suit[:3]]
    y = 10
    for line in lines:
        text = font.render(line, True, (0,0,0))
        surface.blit(text, (10, y))
        y += 22
    return surface

def draw_text_center(screen, text, x, y, font, color=(0,0,0)):
    txt = font.render(text, True, color)
    rect = txt.get_rect(center=(x,y))
    screen.blit(txt, rect)
