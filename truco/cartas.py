"""
Módulo cartas: define Card, Deck y lógica de comparación simplificada para Truco.
Usa listas, tuplas y diccionarios.
"""
import random
from typing import List, Tuple, Dict
import os
import pygame

# Ruta segura para IMG (usa la carpeta del módulo y, si no existe, busca en la carpeta padre)
BASE_DIR = os.path.dirname(__file__)
IMG_DIR = os.path.join(BASE_DIR, "IMG")
if not os.path.isdir(IMG_DIR):
    IMG_DIR = os.path.join(os.path.dirname(BASE_DIR), "IMG")
IMG_DIR = os.path.abspath(IMG_DIR)

cartas_truco = {

    "1espada": {"valor_truco": 15, "valor_envido": 1, "img": pygame.image.load(os.path.join("IMG", "1_de_espada.png"))},
    "1basto": {"valor_truco": 14, "valor_envido": 1, "img": pygame.image.load(os.path.join("IMG", "1_de_basto.png"))},
    "7espada": {"valor_truco": 13, "valor_envido": 7, "img": pygame.image.load(os.path.join("IMG", "7_de_espada.png"))},
    "7oro": {"valor_truco": 12, "valor_envido": 7, "img": pygame.image.load(os.path.join("IMG", "7_de_oro.png"))},
    "3espada": {"valor_truco": 11, "valor_envido": 3, "img": pygame.image.load(os.path.join("IMG", "3_de_espada.png"))},
    "3basto": {"valor_truco": 11, "valor_envido": 3, "img": pygame.image.load(os.path.join("IMG", "3_de_basto.png"))},
    "3oro": {"valor_truco": 11, "valor_envido": 3, "img": pygame.image.load(os.path.join("IMG", "3_de_oro.png"))},
    "3copa": {"valor_truco": 11, "valor_envido": 3, "img": pygame.image.load(os.path.join("IMG", "3_de_copa.png"))},
    "2espada": {"valor_truco": 10, "valor_envido": 2, "img": pygame.image.load(os.path.join("IMG", "2_de_espada.png"))},
    "2basto": {"valor_truco": 10, "valor_envido": 2, "img": pygame.image.load(os.path.join("IMG", "2_de_basto.png"))},
    "2oro": {"valor_truco": 10, "valor_envido": 2, "img": pygame.image.load(os.path.join("IMG", "2_de_oro.png"))},
    "2copa": {"valor_truco": 10, "valor_envido": 2, "img": pygame.image.load(os.path.join("IMG", "2_de_copa.png"))},
    "1oro": {"valor_truco": 9, "valor_envido": 1, "img": pygame.image.load(os.path.join("IMG", "1_de_oro.png"))},
    "1copa": {"valor_truco": 9, "valor_envido": 1, "img": pygame.image.load(os.path.join("IMG", "1_de_copa.png"))},
    "12espada": {"valor_truco": 8, "valor_envido": 0, "img": pygame.image.load(os.path.join("IMG", "12_de_espada.png"))},
    "12basto": {"valor_truco": 8, "valor_envido": 0, "img": pygame.image.load(os.path.join("IMG", "12_de_basto.png"))},
    "12oro": {"valor_truco": 8, "valor_envido": 0, "img": pygame.image.load(os.path.join("IMG", "12_de_oro.png"))},
    "12copa": {"valor_truco": 8, "valor_envido": 0, "img": pygame.image.load(os.path.join("IMG", "12_de_copa.png"))},
    "11espada": {"valor_truco": 7, "valor_envido": 0, "img": pygame.image.load(os.path.join("IMG", "11_de_espada.png"))},
    "11basto": {"valor_truco": 7, "valor_envido": 0, "img": pygame.image.load(os.path.join("IMG", "11_de_basto.png"))},
    "11oro": {"valor_truco": 7, "valor_envido": 0, "img": pygame.image.load(os.path.join("IMG", "11_de_oro.png"))},
    "11copa": {"valor_truco": 7, "valor_envido": 0, "img": pygame.image.load(os.path.join("IMG", "11_de_copa.png"))},
    "10espada": {"valor_truco": 6, "valor_envido": 0, "img": pygame.image.load(os.path.join("IMG", "10_de_espada.png"))},
    "10basto": {"valor_truco": 6, "valor_envido": 0, "img": pygame.image.load(os.path.join("IMG", "10_de_basto.png"))},
    "10oro": {"valor_truco": 6, "valor_envido": 0, "img": pygame.image.load(os.path.join("IMG", "10_de_oro.png"))},
    "10copa": {"valor_truco": 6, "valor_envido": 0, "img": pygame.image.load(os.path.join("IMG", "10_de_copa.png"))},
    "7copa": {"valor_truco": 5, "valor_envido": 7, "img": pygame.image.load(os.path.join("IMG", "7_de_copa.png"))},
    "7basto": {"valor_truco": 4, "valor_envido": 7, "img": pygame.image.load(os.path.join("IMG", "7_de_basto.png"))},
    "6espada": {"valor_truco": 3, "valor_envido": 6, "img": pygame.image.load(os.path.join("IMG", "6_de_espada.png"))},
    "6basto": {"valor_truco": 3, "valor_envido": 6, "img": pygame.image.load(os.path.join("IMG", "6_de_basto.png"))},
    "6oro": {"valor_truco": 3, "valor_envido": 6, "img": pygame.image.load(os.path.join("IMG", "6_de_oro.png"))},
    "6copa": {"valor_truco": 3, "valor_envido": 6, "img": pygame.image.load(os.path.join("IMG", "6_de_copa.png"))},
    "5espada": {"valor_truco": 2, "valor_envido": 5, "img": pygame.image.load(os.path.join("IMG", "5_de_espada.png"))},
    "5basto": {"valor_truco": 2, "valor_envido": 5, "img": pygame.image.load(os.path.join("IMG", "5_de_basto.png"))},
    "5oro": {"valor_truco": 2, "valor_envido": 5, "img": pygame.image.load(os.path.join("IMG", "5_de_oro.png"))},
    "5copa": {"valor_truco": 2, "valor_envido": 5, "img": pygame.image.load(os.path.join("IMG", "5_de_copa.png"))},
    "4espada": {"valor_truco": 1, "valor_envido": 4, "img": pygame.image.load(os.path.join("IMG", "4_de_espada.png"))},
    "4basto": {"valor_truco": 1, "valor_envido": 4, "img": pygame.image.load(os.path.join("IMG", "4_de_basto.png"))},
    "4oro": {"valor_truco": 1, "valor_envido": 4, "img": pygame.image.load(os.path.join("IMG", "4_de_oro.png"))},
    "4copa": {"valor_truco": 1, "valor_envido": 4, "img": pygame.image.load(os.path.join("IMG", "4_de_copa.png"))}
}

SUITS = ("espada", "basto", "oro", "copa")
RANKS = (1,2,3,4,5,6,7,10,11,12)  # Baraja española de 40 cartas

# Orden de Truco simplificado: 1 (alto),3,2,12,11,10,7,6,5,4
TRUCO_RANK_ORDER = {1:0, 3:1, 2:2, 12:3, 11:4, 10:5, 7:6, 6:7, 5:8, 4:9}

def cargar_imagen(nombre, size=(20,20), fallback_color=(100, 100, 100)):
    ruta = os.path.join(IMG_DIR, nombre)
    if os.path.exists(ruta):
        try:
            img = pygame.image.load(ruta).convert_alpha()
            if size:
                img = pygame.transform.smoothscale(img, size)
            return img
        except pygame.error:
            pass
    size_safe = size if size else (50, 50)
    surf = pygame.Surface(size_safe, pygame.SRCALPHA)
    surf.fill(fallback_color)
    return surf



class Card:
    def __init__(self, rank:int, suit:str):
        self.rank = rank
        self.suit = suit  # string de SUITS

    def truco_value(self) -> int:
        """Valor para comparar en Truco (menor es mejor en este mapping)."""
        return TRUCO_RANK_ORDER.get(self.rank, 99)

    def envido_value(self) -> int:
        """Valor usado para calcular 'envido' (10-12 -> 0)."""
        if self.rank in (10,11,12):
            return 0
        return self.rank

    def id(self) -> str:
        return f"{self.rank}_{self.suit}"

    def __repr__(self):
        return f"{self.rank} de {self.suit}"

class Deck:
    def __init__(self):
        self.cards: List[Card] = [Card(r, s) for s in SUITS for r in RANKS]
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self, n:int) -> List[Card]:
        dealt = []
        for _ in range(n):
            if not self.cards:
                raise IndexError("No quedan cartas en el mazo")
            dealt.append(self.cards.pop())
        return dealt

def compare_cards(card_a: Card, card_b: Card) -> int:
    """
    Compara dos cartas según orden de Truco:
    devuelve 1 si card_a gana, -1 si card_b gana, 0 empate (rara vez).
    """
    va = card_a.truco_value()
    vb = card_b.truco_value()
    if va < vb:
        return 1
    if va > vb:
        return -1
    # En empate de valor, desempata por el rank numérico mayor
    if card_a.rank > card_b.rank:
        return 1
    if card_a.rank < card_b.rank:
        return -1
    return 0

def calculate_envido(hand: List[Card]) -> int:
    """
    Cálculo simplificado de envido:
    - Si hay al menos dos cartas del mismo palo: suman sus envido_values + 20.
    - Si no hay cartas del mismo palo: el mayor envido_value.
    """
    best = 0
    suits = {}
    for c in hand:
        suits.setdefault(c.suit, []).append(c)
    for suit_cards in suits.values():
        if len(suit_cards) >= 2:
            # considerar mejor combinación de 2 cartas
            vals = sorted([c.envido_value() for c in suit_cards], reverse=True)
            en = vals[0] + vals[1] + 20
            best = max(best, en)
    if best == 0:
        # no hay pares de palo: tomar mayor envido_value
        best = max(c.envido_value() for c in hand)
    return best
