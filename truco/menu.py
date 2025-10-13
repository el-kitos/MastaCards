"""
Pantalla de menú principal con opciones:
- Jugar partida
- Ver reglas
- Historial / puntajes
- Salir
"""

import pygame
from typing import Tuple

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("arial", 36, bold=True)
        self.options = ["Jugar partida", "Ver reglas", "Historial / Puntajes", "Salir"]
        self.selected = 0

    def run(self) -> str:
        clock = pygame.time.Clock()
        running = True
        while running:
            self.screen.fill((30,120,30))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "salir"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.selected = (self.selected - 1) % len(self.options)
                    elif event.key == pygame.K_DOWN:
                        self.selected = (self.selected + 1) % len(self.options)
                    elif event.key == pygame.K_RETURN:
                        return self.options[self.selected]
                    elif event.key == pygame.K_ESCAPE:
                        return "salir"
            # dibujar título y opciones
            title_font = pygame.font.SysFont("arial", 48, bold=True)
            title = title_font.render("Truco Argentino", True, (255,255,255))
            self.screen.blit(title, (50, 40))
            y = 160
            for i, opt in enumerate(self.options):
                color = (255,255,0) if i == self.selected else (255,255,255)
                txt = self.font.render(opt, True, color)
                self.screen.blit(txt, (100, y))
                y += 60
            pygame.display.flip()
            clock.tick(30)
        return "salir"
