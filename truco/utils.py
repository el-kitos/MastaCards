"""
Funciones utilitarias: carga de imágenes de cartas con fallback
"""

import pygame
from typing import Tuple
try:
    from truco.cartas import Card
except Exception:
    from cartas import Card
import os

# Ruta base y assets: intenta en la carpeta del módulo y, si no existe, en la carpeta padre
BASE_DIR = os.path.dirname(__file__)
ASSETS_DIR = os.path.join(BASE_DIR, "..", "assets")
if not os.path.isdir(ASSETS_DIR):
    # fallback: buscar en la carpeta padre (por si el módulo está en un submódulo)
    ASSETS_DIR = os.path.join(os.path.dirname(BASE_DIR), "assets")
ASSETS_DIR = os.path.abspath(ASSETS_DIR)

CARDS_DIR = os.path.join(ASSETS_DIR, "cards")

def load_card_image(card: Card, size: Tuple[int, int]) -> pygame.Surface:
    """
    Carga la imagen de una carta desde IMG/<numero>_de_<palo>.png
    Si no existe, crea un fallback dibujado
    """
    # Obtener imagen del diccionario si existe
    img = card.get_image()
    
    if img is not None:
        # Redimensionar
        return pygame.transform.smoothscale(img, size)
    
    # Fallback: intentar cargar desde archivo
    filename = f"{card.rank}_de_{card.suit}.png"
    path = os.path.join(IMG_DIR, filename)
    
    if os.path.exists(path):
        try:
            img = pygame.image.load(path).convert_alpha()
            return pygame.transform.smoothscale(img, size)
        except Exception as e:
            print(f"Error cargando {filename}: {e}")
    
    # Fallback final: dibujar carta
    return crear_carta_fallback(card, size)


def crear_carta_fallback(card: Card, size: Tuple[int, int]) -> pygame.Surface:
    """
    Crea una representación visual de la carta cuando no hay imagen
    """
    surface = pygame.Surface(size)
    surface.fill((255, 255, 255))
    
    # Borde
    pygame.draw.rect(surface, (0, 0, 0), surface.get_rect(), 3)
    
    # Color según palo
    colores = {
        "espada": (0, 0, 0),
        "basto": (0, 0, 0),
        "oro": (220, 180, 0),
        "copa": (200, 0, 0)
    }
    color = colores.get(card.suit, (0, 0, 0))
    
    # Textos
    font_big = pygame.font.SysFont("arial", size[1] // 3, bold=True)
    font_small = pygame.font.SysFont("arial", size[1] // 6, bold=True)
    
    # Número
    numero_text = font_big.render(str(card.rank), True, color)
    numero_rect = numero_text.get_rect(center=(size[0] // 2, size[1] // 3))
    surface.blit(numero_text, numero_rect)
    
    # Palo (abreviado)
    palo_abrev = {
        "espada": "ESP",
        "basto": "BAS",
        "oro": "ORO",
        "copa": "COP"
    }
    palo_text = font_small.render(palo_abrev.get(card.suit, ""), True, color)
    palo_rect = palo_text.get_rect(center=(size[0] // 2, size[1] * 2 // 3))
    surface.blit(palo_text, palo_rect)
    
    # Valor de truco pequeño (para debug)
    valor_font = pygame.font.SysFont("arial", 12)
    valor_text = valor_font.render(f"[{card.truco_value()}]", True, (100, 100, 100))
    surface.blit(valor_text, (5, size[1] - 15))
    
    return surface


def draw_text_center(screen, text, x, y, font, color=(0, 0, 0)):
    """Dibuja texto centrado en una posición"""
    txt = font.render(text, True, color)
    rect = txt.get_rect(center=(x, y))
    screen.blit(txt, rect)