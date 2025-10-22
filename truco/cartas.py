"""
Módulo cartas: define Card, Deck y lógica de comparación simplificada para Truco.
Usa listas, tuplas y diccionarios.
"""
import random
from typing import List, Tuple, Dict
import os
import pygame

import pygame, os

cartas_truco = {
    "1_espada": {"valor_truco": 15, "valor_envido": 1, "img": pygame.image.load(os.path.join("IMG", "1_de_espada.png"))},
    "1_basto": {"valor_truco": 14, "valor_envido": 1, "img": pygame.image.load(os.path.join("IMG", "1_de_basto.png"))},
    "7_espada": {"valor_truco": 13, "valor_envido": 7, "img": pygame.image.load(os.path.join("IMG", "7_de_espada.png"))},
    "7_oro": {"valor_truco": 12, "valor_envido": 7, "img": pygame.image.load(os.path.join("IMG", "7_de_oro.png"))},
    
    "3_espada": {"valor_truco": 11, "valor_envido": 3, "img": pygame.image.load(os.path.join("IMG", "3_de_espada.png"))},
    "3_basto": {"valor_truco": 11, "valor_envido": 3, "img": pygame.image.load(os.path.join("IMG", "3_de_basto.png"))},
    "3_oro": {"valor_truco": 11, "valor_envido": 3, "img": pygame.image.load(os.path.join("IMG", "3_de_oro.png"))},
    "3_copa": {"valor_truco": 11, "valor_envido": 3, "img": pygame.image.load(os.path.join("IMG", "3_de_copa.png"))},

    "2_espada": {"valor_truco": 10, "valor_envido": 2, "img": pygame.image.load(os.path.join("IMG", "2_de_espada.png"))},
    "2_basto": {"valor_truco": 10, "valor_envido": 2, "img": pygame.image.load(os.path.join("IMG", "2_de_basto.png"))},
    "2_oro": {"valor_truco": 10, "valor_envido": 2, "img": pygame.image.load(os.path.join("IMG", "2_de_oro.png"))},
    "2_copa": {"valor_truco": 10, "valor_envido": 2, "img": pygame.image.load(os.path.join("IMG", "2_de_copa.png"))},

    "1_oro": {"valor_truco": 9, "valor_envido": 1, "img": pygame.image.load(os.path.join("IMG", "1_de_oro.png"))},
    "1_copa": {"valor_truco": 9, "valor_envido": 1, "img": pygame.image.load(os.path.join("IMG", "1_de_copa.png"))},

    "12_espada": {"valor_truco": 8, "valor_envido": 0, "img": pygame.image.load(os.path.join("IMG", "12_de_espada.png"))},
    "12_basto": {"valor_truco": 8, "valor_envido": 0, "img": pygame.image.load(os.path.join("IMG", "12_de_basto.png"))},
    "12_oro": {"valor_truco": 8, "valor_envido": 0, "img": pygame.image.load(os.path.join("IMG", "12_de_oro.png"))},
    "12_copa": {"valor_truco": 8, "valor_envido": 0, "img": pygame.image.load(os.path.join("IMG", "12_de_copa.png"))},

    "11_espada": {"valor_truco": 7, "valor_envido": 0, "img": pygame.image.load(os.path.join("IMG", "11_de_espada.png"))},
    "11_basto": {"valor_truco": 7, "valor_envido": 0, "img": pygame.image.load(os.path.join("IMG", "11_de_basto.png"))},
    "11_oro": {"valor_truco": 7, "valor_envido": 0, "img": pygame.image.load(os.path.join("IMG", "11_de_oro.png"))},
    "11_copa": {"valor_truco": 7, "valor_envido": 0, "img": pygame.image.load(os.path.join("IMG", "11_de_copa.png"))},

    "10_espada": {"valor_truco": 6, "valor_envido": 0, "img": pygame.image.load(os.path.join("IMG", "10_de_espada.png"))},
    "10_basto": {"valor_truco": 6, "valor_envido": 0, "img": pygame.image.load(os.path.join("IMG", "10_de_basto.png"))},
    "10_oro": {"valor_truco": 6, "valor_envido": 0, "img": pygame.image.load(os.path.join("IMG", "10_de_oro.png"))},
    "10_copa": {"valor_truco": 6, "valor_envido": 0, "img": pygame.image.load(os.path.join("IMG", "10_de_copa.png"))},

    "7_copa": {"valor_truco": 5, "valor_envido": 7, "img": pygame.image.load(os.path.join("IMG", "7_de_copa.png"))},
    "7_basto": {"valor_truco": 4, "valor_envido": 7, "img": pygame.image.load(os.path.join("IMG", "7_de_basto.png"))},

    "6_espada": {"valor_truco": 3, "valor_envido": 6, "img": pygame.image.load(os.path.join("IMG", "6_de_espada.png"))},
    "6_basto": {"valor_truco": 3, "valor_envido": 6, "img": pygame.image.load(os.path.join("IMG", "6_de_basto.png"))},
    "6_oro": {"valor_truco": 3, "valor_envido": 6, "img": pygame.image.load(os.path.join("IMG", "6_de_oro.png"))},
    "6_copa": {"valor_truco": 3, "valor_envido": 6, "img": pygame.image.load(os.path.join("IMG", "6_de_copa.png"))},

    "5_espada": {"valor_truco": 2, "valor_envido": 5, "img": pygame.image.load(os.path.join("IMG", "5_de_espada.png"))},
    "5_basto": {"valor_truco": 2, "valor_envido": 5, "img": pygame.image.load(os.path.join("IMG", "5_de_basto.png"))},
    "5_oro": {"valor_truco": 2, "valor_envido": 5, "img": pygame.image.load(os.path.join("IMG", "5_de_oro.png"))},
    "5_copa": {"valor_truco": 2, "valor_envido": 5, "img": pygame.image.load(os.path.join("IMG", "5_de_copa.png"))},

    "4_espada": {"valor_truco": 1, "valor_envido": 4, "img": pygame.image.load(os.path.join("IMG", "4_de_espada.png"))},
    "4_basto": {"valor_truco": 1, "valor_envido": 4, "img": pygame.image.load(os.path.join("IMG", "4_de_basto.png"))},
    "4_oro": {"valor_truco": 1, "valor_envido": 4, "img": pygame.image.load(os.path.join("IMG", "4_de_oro.png"))},
    "4_copa": {"valor_truco": 1, "valor_envido": 4, "img": pygame.image.load(os.path.join("IMG", "4_de_copa.png"))}
}


SUITS = ("espada", "basto", "oro", "copa")
RANKS = (1,2,3,4,5,6,7,10,11,12)  # Baraja española de 40 cartas



IMG_DIR = "IMG"

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
    def __init__(self, num, palo, img, truco, envido):
        self.num = num 
        self.palo = palo
        self.img = img
        self.valor_truco = truco
        self.valor_envido = envido

    def id(self) -> str:
        return f"{self.rank}{self.suit}"

    def __repr__(self):
        return f"{self.rank} de {self.suit}"
    
    def get_valor_truco(self):
        return self.valor_truco

class Deck:
    def __init__(self):
        self.cards = []
        for carta in cartas_truco:
            num, palo = carta.split("_")
            nueva_carta = Card(num, palo, cartas_truco[carta]["img"],cartas_truco[carta]["valor_truco"],cartas_truco[carta]["valor_envido"] )
            self.cards.append(nueva_carta)
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self, n) :
        dealt = []
        for _ in range(n):
            if not self.cards:
                raise IndexError("No quedan cartas en el mazo")
            dealt.append(self.cards.pop())
        return dealt

def compare_cards(card_a, card_b) :

    va = card_a.get_valor_truco()
    vb = card_b.get_valor_truco()
    if va < vb:
        return 1
    if va > vb:
        return -1
    
    return 0

def calculate_envido(hand):
    # Agrupamos las cartas por palo
    palos = {}
    for carta in hand:
        if carta.palo not in palos:
            palos[carta.palo] = []
        palos[carta.palo].append(carta.valor_envido)

    max_envido = 0  # acá guardamos el valor máximo encontrado

    for valores in palos.values():
        if len(valores) >= 2:
            # Si hay 2 o más del mismo palo → sumamos las 2 más altas + 20
            valores.sort(reverse=True)
            envido = valores[0] + valores[1] + 20
        else:
            # Si solo hay una carta de ese palo → solo su valor
            envido = valores[0]

        if envido > max_envido:
            max_envido = envido

    return max_envido

        
        
