"""
Módulo cartas: define Card, Deck y lógica de comparación simplificada para Truco.
Usa listas, tuplas y diccionarios.
"""

import random
from typing import List, Tuple, Dict

SUITS = ("espadas", "bastos", "oros", "copas")
RANKS = (1,2,3,4,5,6,7,10,11,12)  # Baraja española de 40 cartas

# Orden de Truco simplificado: 1 (alto),3,2,12,11,10,7,6,5,4
TRUCO_RANK_ORDER = {1:0, 3:1, 2:2, 12:3, 11:4, 10:5, 7:6, 6:7, 5:8, 4:9}

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
