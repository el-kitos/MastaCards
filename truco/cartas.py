"""
Módulo cartas: define Card, Deck y lógica de comparación correcta para Truco.
Usa el diccionario cartas_truco con imágenes pre-cargadas.
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
    "1espada": {"valor_truco": 15, "valor_envido": 1, "img": None},
    "1basto": {"valor_truco": 14, "valor_envido": 1, "img": None},
    "7espada": {"valor_truco": 13, "valor_envido": 7, "img": None},
    "7oro": {"valor_truco": 12, "valor_envido": 7, "img": None},
    "3espada": {"valor_truco": 11, "valor_envido": 3, "img": None},
    "3basto": {"valor_truco": 11, "valor_envido": 3, "img": None},
    "3oro": {"valor_truco": 11, "valor_envido": 3, "img": None},
    "3copa": {"valor_truco": 11, "valor_envido": 3, "img": None},
    "2espada": {"valor_truco": 10, "valor_envido": 2, "img": None},
    "2basto": {"valor_truco": 10, "valor_envido": 2, "img": None},
    "2oro": {"valor_truco": 10, "valor_envido": 2, "img": None},
    "2copa": {"valor_truco": 10, "valor_envido": 2, "img": None},
    "1oro": {"valor_truco": 9, "valor_envido": 1, "img": None},
    "1copa": {"valor_truco": 9, "valor_envido": 1, "img": None},
    "12espada": {"valor_truco": 8, "valor_envido": 0, "img": None},
    "12basto": {"valor_truco": 8, "valor_envido": 0, "img": None},
    "12oro": {"valor_truco": 8, "valor_envido": 0, "img": None},
    "12copa": {"valor_truco": 8, "valor_envido": 0, "img": None},
    "11espada": {"valor_truco": 7, "valor_envido": 0, "img": None},
    "11basto": {"valor_truco": 7, "valor_envido": 0, "img": None},
    "11oro": {"valor_truco": 7, "valor_envido": 0, "img": None},
    "11copa": {"valor_truco": 7, "valor_envido": 0, "img": None},
    "10espada": {"valor_truco": 6, "valor_envido": 0, "img": None},
    "10basto": {"valor_truco": 6, "valor_envido": 0, "img": None},
    "10oro": {"valor_truco": 6, "valor_envido": 0, "img": None},
    "10copa": {"valor_truco": 6, "valor_envido": 0, "img": None},
    "7copa": {"valor_truco": 5, "valor_envido": 7, "img": None},
    "7basto": {"valor_truco": 4, "valor_envido": 7, "img": None},
    "6espada": {"valor_truco": 3, "valor_envido": 6, "img": None},
    "6basto": {"valor_truco": 3, "valor_envido": 6, "img": None},
    "6oro": {"valor_truco": 3, "valor_envido": 6, "img": None},
    "6copa": {"valor_truco": 3, "valor_envido": 6, "img": None},
    "5espada": {"valor_truco": 2, "valor_envido": 5, "img": None},
    "5basto": {"valor_truco": 2, "valor_envido": 5, "img": None},
    "5oro": {"valor_truco": 2, "valor_envido": 5, "img": None},
    "5copa": {"valor_truco": 2, "valor_envido": 5, "img": None},
    "4espada": {"valor_truco": 1, "valor_envido": 4, "img": None},
    "4basto": {"valor_truco": 1, "valor_envido": 4, "img": None},
    "4oro": {"valor_truco": 1, "valor_envido": 4, "img": None},
    "4copa": {"valor_truco": 1, "valor_envido": 4, "img": None}
}

SUITS = ("espada", "basto", "oro", "copa")
RANKS = (1, 2, 3, 4, 5, 6, 7, 10, 11, 12)

IMG_DIR = "IMG"

def cargar_imagenes_cartas():
    """Carga todas las imágenes de cartas al iniciar"""
    for key in cartas_truco.keys():
        nombre_archivo = f"{key[:-1]}_de_{key[-1] if len(key) <= 6 else key[-(len(key)-2):]}.png"
        # Parsear correctamente el nombre
        # Ejemplos: "1espada" -> "1_de_espada.png"
        #          "12basto" -> "12_de_basto.png"
        
        # Separar número y palo
        if key.startswith("12"):
            numero = "12"
            palo = key[2:]
        elif key.startswith("11"):
            numero = "11"
            palo = key[2:]
        elif key.startswith("10"):
            numero = "10"
            palo = key[2:]
        else:
            numero = key[0]
            palo = key[1:]
        
        nombre_archivo = f"{numero}_de_{palo}.png"
        ruta = os.path.join(IMG_DIR, nombre_archivo)
        
        if os.path.exists(ruta):
            try:
                cartas_truco[key]["img"] = pygame.image.load(ruta).convert_alpha()
            except pygame.error as e:
                print(f"Error cargando {nombre_archivo}: {e}")
                cartas_truco[key]["img"] = None
        else:
            print(f"No se encontró imagen: {nombre_archivo}")
            cartas_truco[key]["img"] = None




class Card:
    def __init__(self, rank: int, suit: str):
        self.rank = rank
        self.suit = suit
        self.key = f"{rank}{suit}"
    
    def truco_value(self) -> int:
        """
        Valor para comparar en Truco.
        MAYOR número = MEJOR carta (15 = 1 de espada, mejor carta)
        """
        return cartas_truco.get(self.key, {}).get("valor_truco", 0)
    
    def envido_value(self) -> int:
        """Valor para calcular envido"""
        return cartas_truco.get(self.key, {}).get("valor_envido", 0)
    
    def get_image(self):
        """Retorna la imagen de la carta"""
        return cartas_truco.get(self.key, {}).get("img", None)
    
    def id(self) -> str:
        """ID para buscar imagen fallback"""
        return f"{self.rank}_{self.suit}"
    
    def __repr__(self):
        return f"{self.rank} de {self.suit}"

class Deck:
    def __init__(self):
        self.cards: List[Card] = [Card(r, s) for s in SUITS for r in RANKS]
        self.shuffle()
    
    def shuffle(self):
        random.shuffle(self.cards)
    
    def deal(self, n: int) -> List[Card]:
        dealt = []
        for _ in range(n):
            if not self.cards:
                raise IndexError("No quedan cartas en el mazo")
            dealt.append(self.cards.pop())
        return dealt

def compare_cards(card_a: Card, card_b: Card) -> int:
    """
    Compara dos cartas según orden de Truco.
    Retorna:
        1 si card_a gana
       -1 si card_b gana
        0 si empatan
    
    MAYOR valor_truco = MEJOR carta
    """
    va = card_a.truco_value()
    vb = card_b.truco_value()
    
    if va > vb:
        return 1  # card_a es mejor
    elif va < vb:
        return -1  # card_b es mejor
    else:
        return 0  # Empate (mismo valor)

def calculate_envido(hand: List[Card]) -> int:
    """
    Cálculo de envido:
    - Si hay 2+ cartas del mismo palo: las dos mejores suman + 20
    - Si no: la carta con mayor envido_value
    """
    best = 0
    suits = {}
    
    for c in hand:
        suits.setdefault(c.suit, []).append(c)
    
    for suit_cards in suits.values():
        if len(suit_cards) >= 2:
            # Tomar las 2 mejores cartas de ese palo
            vals = sorted([c.envido_value() for c in suit_cards], reverse=True)
            en = vals[0] + vals[1] + 20
            best = max(best, en)
    
    if best == 0:
        # No hay pares de palo: tomar mayor envido_value
        best = max(c.envido_value() for c in hand)
    
    return best