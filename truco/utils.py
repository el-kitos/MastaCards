"""
Funciones utilitarias: dibujo de cartas fallback, textos, manejo básico de eventos.
"""

import pygame
from typing import Tuple
from truco.cartas import Card
import os

# Ruta base y assets: intenta en la carpeta del módulo y, si no existe, en la carpeta padre
BASE_DIR = os.path.dirname(__file__)
ASSETS_DIR = os.path.join(BASE_DIR, "..", "assets")
if not os.path.isdir(ASSETS_DIR):
    # fallback: buscar en la carpeta padre (por si el módulo está en un submódulo)
    ASSETS_DIR = os.path.join(os.path.dirname(BASE_DIR), "assets")
ASSETS_DIR = os.path.abspath(ASSETS_DIR)

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
