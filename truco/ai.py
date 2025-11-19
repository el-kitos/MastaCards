
import random
from typing import List
try:
    from truco.cartas import Card, calculate_envido
except Exception:
    from cartas import Card, calculate_envido

def choose_card_ai(hand: List[Card], table_cards: List[Card], turn:int) -> Card:
    """
    Heurística simple:
    - Si tiene un 1 o 3 (alto) juega primero esas cartas cuando quiere ganar.
    - Si está perdiendo, puede jugar carta baja (aleatorio).
    - En esta versión, comport. básico
    """
    # intentar jugar la carta con mejor truco_value
    sorted_hand = sorted(hand, key=lambda c: c.truco_value())
    # 60% chance jugar mejor carta, 40% jugar aleatoria
    if random.random() < 0.6:
        return sorted_hand[0]
    return random.choice(hand)

def decide_accept_truco() -> bool:
    # IA acepta truco con 60% probabilidad
    return random.random() < 0.6

def decide_accept_envido(hand: List[Card]) -> bool:
    # calcula envido y acepta si tiene > 22 (heurística)
    score = calculate_envido(hand)
    return score >= 22
