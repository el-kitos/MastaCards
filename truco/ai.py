import random
from typing import List
from truco.cartas import Card, calculate_envido

def choose_card_ai(hand: List[Card], table_cards: List[Card], turn: int) -> Card:
    """
    Heurística mejorada para elegir carta:
    - Evalúa qué cartas son fuertes (1, 3, 7 de espada/oro)
    - Juega estratégicamente según el turno
    """
    if not hand:
        return None
    
    # Ordenar por valor de truco (menor = mejor)
    sorted_hand = sorted(hand, key=lambda c: c.truco_value())
    
    # Primera jugada: jugar carta media-alta
    if turn == 1:
        # 70% jugar carta fuerte, 30% media
        if random.random() < 0.7 and len(sorted_hand) > 1:
            return sorted_hand[0]  # Mejor carta
        else:
            return sorted_hand[len(sorted_hand) // 2]  # Carta media
    
    # Segunda/tercera jugada: más estratégico
    if turn >= 2:
        # Si tiene carta muy fuerte (valor < 5), jugarla
        if sorted_hand[0].truco_value() < 5:
            return sorted_hand[0]
        # Sino jugar aleatoria o media
        if random.random() < 0.5:
            return sorted_hand[0]
        else:
            return random.choice(hand)
    
    # Por defecto: carta aleatoria
    return random.choice(hand)


def decide_accept_truco() -> bool:
    """
    IA decide si acepta Truco.
    Acepta con 60% probabilidad (puede mejorarse evaluando la mano)
    """
    return random.random() < 0.6


def decide_accept_envido(hand: List[Card]) -> bool:
    """
    IA decide si acepta Envido basándose en su puntaje.
    Acepta si tiene >= 22 puntos (envido razonable)
    """
    score = calculate_envido(hand)
    # Acepta si tiene buen envido, o a veces con envido medio (bluff)
    if score >= 25:
        return True
    elif score >= 20:
        return random.random() < 0.7
    else:
        return random.random() < 0.3


def decide_call_truco(hand: List[Card]) -> bool:
    """
    IA decide si canta Truco según la calidad de su mano.
    Canta si tiene cartas fuertes.
    """
    if not hand:
        return False
    
    # Evaluar la mano: contar cartas fuertes
    strong_cards = sum(1 for c in hand if c.truco_value() < 6)
    
    # Si tiene 2+ cartas fuertes, canta con probabilidad
    if strong_cards >= 2:
        return random.random() < 0.5
    elif strong_cards == 1:
        return random.random() < 0.25
    
    return False


def decide_call_envido(hand: List[Card]) -> bool:
    """
    IA decide si canta Envido según su puntaje.
    Canta si tiene buen envido (>= 24)
    """
    score = calculate_envido(hand)
    
    if score >= 28:
        return random.random() < 0.8
    elif score >= 24:
        return random.random() < 0.5
    elif score >= 20:
        return random.random() < 0.2
    
    return False