"""
IA muy básica para jugar contra la PC.
Toma decisiones con heurística simple basada en fuerza de la mano.
"""

import random
from typing import List
from cartas import Card, calculate_envido

def choose_card_ai(hand: List[Card], table_cards: List[Card], turn:int) -> Card:
    """
    Heurística simple:
    - Intenta jugar la carta con mejor truco_value (menor truco_value es mejor).
    - 60% chance jugar mejor carta, 40% jugar aleatoria para variar.
    """
    if not hand:
        raise ValueError("Mano vacía en choose_card_ai")
    sorted_hand = sorted(hand, key=lambda c: c.truco_value())
    # 60% chance jugar mejor carta, 40% jugar aleatoria
    if random.random() < 0.6:
        return sorted_hand[0]
    return random.choice(hand)

def decide_accept_truco(opponent_hand: List[Card]=None) -> bool:
    """
    Decide si aceptar Truco.
    Si se le pasa la mano del oponente (o propia), usa heurística:
    - Si la mano tiene al menos una carta con truco_value <= 1 (1 o 3), acepta.
    - Si no, acepta con probabilidad 0.45 (más conservadora).
    """
    if not opponent_hand:
        # si no se conoce la mano, comportamiento por defecto
        return random.random() < 0.6
    # fuerza: buscar la mejor carta (menor truco_value)
    best_val = min(c.truco_value() for c in opponent_hand)
    if best_val <= 1:
        return True
    # si no tiene cartas muy buenas, aceptar con menor probabilidad
    return random.random() < 0.45

def decide_accept_envido(hand: List[Card]) -> bool:
    # calcula envido y acepta si tiene > 22 (heurística)
    score = calculate_envido(hand)
    return score >= 22
