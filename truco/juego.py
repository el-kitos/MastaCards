"""
Módulo principal del juego: lógica de turno, UI de juego, manejo de Truco y Envido (simplificados).
"""

import pygame
from cartas import Deck, compare_cards, calculate_envido, Card
from utils import load_card_image, draw_text_center
from data_manager import save_history
from ai import choose_card_ai, decide_accept_truco, decide_accept_envido
import time
import random

SCREEN_W = 1000
SCREEN_H = 700

class Game:
    def __init__(self, screen, vs_ai=True, player_name="Jugador"):
        self.screen = screen
        self.vs_ai = vs_ai
        self.player_name = player_name
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("arial", 20)
        self.large_font = pygame.font.SysFont("arial", 28, bold=True)
        self.reset_match()

    def reset_match(self):
        self.deck = Deck()
        self.player_hand = self.deck.deal(3)
        self.cpu_hand = self.deck.deal(3)
        self.player_score = 0
        self.cpu_score = 0
        self.round_wins = {self.player_name:0, "CPU":0}
        self.table_cards = []  # pares (player_card, cpu_card) por mano
        self.truco_value = 1  # puntos en juego para la mano (puede subir a 2 si se canta Truco y se acepta)
        self.history = []
        self.turn = "player" if random.random() < 0.5 else "cpu"
        self.game_over = False

    def play(self):
        """
        Bucle principal de la partida. Retorna al menú cuando se sale.
        """
        running = True
        while running:
            self.screen.fill((0,120,0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "salir"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return "menu"
            # UI: dibujar manos, puntajes y opciones
            self.draw_ui()
            if not self.game_over:
                # gestión del turno
                if self.turn == "player":
                    result = self.player_turn()
                    if result == "salir":
                        return "salir"
                    elif result == "menu":
                        return "menu"
                else:
                    self.cpu_turn()
            else:
                # mostrar ganador y guardar historial
                time.sleep(1)
                winner = self.player_name if self.player_score > self.cpu_score else "CPU"
                save_history({
                    "winner": winner,
                    "player_score": self.player_score,
                    "cpu_score": self.cpu_score,
                    "timestamp": time.time()
                })
                # reset sencillo para jugar otra
                self.reset_match()
            pygame.display.flip()
            self.clock.tick(30)
        return "menu"

    def player_turn(self):
        """
        Manejo simple del turno del jugador: click en carta para jugar.
        También permite cantar Truco o Envido (teclas T y E).
        """
        clicked_card = None
        waiting = True
        while waiting:
            self.screen.fill((0,120,0))
            self.draw_ui()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "salir"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_t:
                        # cantar truco
                        accepted = self.handle_truco_call(caller="player")
                        if not accepted:
                            # jugador canta truco y CPU rechaza -> jugador gana truco_value puntos
                            self.player_score += self.truco_value
                            self.game_over = self.check_game_over()
                            return
                        else:
                            # aumenta valor de la mano
                            self.truco_value = 2
                    if event.key == pygame.K_e:
                        # cantar envido antes de jugar la carta (si no se jugaron cartas)
                        accepted = self.handle_envido_call(caller="player")
                        if not accepted:
                            # rechazado -> otorgar 1 punto al que canta? aquí otorgamos 1 al que canta.
                            self.player_score += 1
                            self.game_over = self.check_game_over()
                            return
                    if event.key == pygame.K_ESCAPE:
                        return "menu"
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mx,my = pygame.mouse.get_pos()
                    # detectar click en cartas del jugador (dibujadas abajo)
                    rects = self.get_player_card_rects()
                    for idx, r in enumerate(rects):
                        if r.collidepoint((mx,my)):
                            clicked_card = self.player_hand.pop(idx)
                            waiting = False
                            break
            if self.vs_ai and not waiting and clicked_card:
                # jugar carta y luego CPU responde
                self.table_cards.append((clicked_card, None))
                # CPU selecciona carta
                cpu_choice = choose_card_ai(self.cpu_hand, [c for c,_ in self.table_cards], len(self.table_cards))
                self.cpu_hand.remove(cpu_choice)
                self.table_cards[-1] = (clicked_card, cpu_choice)
                self.resolve_trick()
                return
            elif not self.vs_ai and not waiting and clicked_card:
                # en versión local multijugador deberías gestionar turnos de otro jugador (no implementado)
                # para ahora asumimos vs CPU
                pass
            pygame.display.flip()
            self.clock.tick(30)
        return

    def cpu_turn(self):
        """
        Turno de la CPU: selecciona carta, espera interacción si el jugador debe responder.
        """
        # cpu juega carta
        cpu_card = choose_card_ai(self.cpu_hand, [c for c,_ in self.table_cards], len(self.table_cards))
        try:
            self.cpu_hand.remove(cpu_card)
        except ValueError:
            # defensiva
            cpu_card = self.cpu_hand.pop(0)
        # si es turno cpu y vs jugador, el jugador debe responder: esperar click
        self.table_cards.append((None, cpu_card))
        # ahora esperar a que jugador responda eligiendo carta
        waiting = True
        while waiting:
            self.screen.fill((0,120,0))
            self.draw_ui()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "salir"
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mx,my = pygame.mouse.get_pos()
                    rects = self.get_player_card_rects()
                    for idx, r in enumerate(rects):
                        if r.collidepoint((mx,my)):
                            player_card = self.player_hand.pop(idx)
                            self.table_cards[-1] = (player_card, cpu_card)
                            waiting = False
                            break
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return "menu"
            pygame.display.flip()
            self.clock.tick(30)
        self.resolve_trick()

    def resolve_trick(self):
        """
        Resuelve la mano actual comparando las dos cartas en mesa.
        Incrementa round_wins y asigna puntos si termina la mano de 3 jugadas.
        """
        last = self.table_cards[-1]
        player_card, cpu_card = last
        if player_card is None or cpu_card is None:
            return
        cmp = compare_cards(player_card, cpu_card)
        if cmp == 1:
            winner = self.player_name
        elif cmp == -1:
            winner = "CPU"
        else:
            winner = "empate"
        if winner != "empate":
            self.round_wins[winner] = self.round_wins.get(winner,0) + 1
        # verificar si alguien ganó dos rondas
        if self.round_wins[self.player_name] == 2 or self.round_wins["CPU"] == 2:
            if self.round_wins[self.player_name] > self.round_wins["CPU"]:
                self.player_score += self.truco_value
            else:
                self.cpu_score += self.truco_value
            # guardar en historial local de la mano
            save_history({
                "hand_winner": self.player_name if self.player_score>self.cpu_score else "CPU",
                "player_score": self.player_score,
                "cpu_score": self.cpu_score,
                "timestamp": time.time()
            })
            # verificar si fin de partida
            self.game_over = self.check_game_over()
            # reset para próxima mano si no terminó el partido
            if not self.game_over:
                # repartir de nuevo si quedan cartas, sino reconstruir mazo
                try:
                    self.player_hand = self.deck.deal(3)
                    self.cpu_hand = self.deck.deal(3)
                except Exception:
                    # reconstruir el mazo
                    self.deck = Deck()
                    self.player_hand = self.deck.deal(3)
                    self.cpu_hand = self.deck.deal(3)
                self.round_wins = {self.player_name:0, "CPU":0}
                self.table_cards = []
                self.truco_value = 1
                self.turn = "player" if random.random() < 0.5 else "cpu"

    def handle_truco_call(self, caller="player") -> bool:
        """
        Caller canta Truco. Retorna True si el otro acepta, False si rechaza.
        IA responde con decide_accept_truco.
        """
        if caller == "player":
            # preguntar al CPU
            if self.vs_ai:
                accept = decide_accept_truco()
                return accept
            else:
                # para multijugador local: aceptar con tecla A o rechazar R (no implementado UI)
                return True
        else:
            # CPU canta: el jugador recibe prompt sencillo
            # Mostramos un mensaje y espera Y/N
            return self.prompt_yes_no("CPU canta Truco. ¿Aceptas? (Y/N)")

    def handle_envido_call(self, caller="player") -> bool:
        """
        Caller canta Envido. Retorna True si el otro acepta, False si rechaza.
        Si aceptan se compara y se otorgan puntos.
        """
        if caller == "player":
            if self.vs_ai:
                accept = decide_accept_envido(self.cpu_hand)
                if not accept:
                    return False
                # si acepta, comparar envidos
                p_en = calculate_envido(self.player_hand)
                c_en = calculate_envido(self.cpu_hand)
                if p_en > c_en:
                    self.player_score += 2
                else:
                    self.cpu_score += 2
                self.game_over = self.check_game_over()
                return True
            else:
                return True
        else:
            # CPU canta envido: preguntar jugador
            if self.vs_ai:
                accept = self.prompt_yes_no("CPU canta Envido. ¿Aceptas? (Y/N)")
                if not accept:
                    # CPU gana 1 punto por abandono
                    self.cpu_score += 1
                    self.game_over = self.check_game_over()
                    return False
                # si acepta comparar
                p_en = calculate_envido(self.player_hand)
                c_en = calculate_envido(self.cpu_hand)
                if p_en > c_en:
                    self.player_score += 2
                else:
                    self.cpu_score += 2
                self.game_over = self.check_game_over()
                return True
            else:
                return True

    def prompt_yes_no(self, message:str) -> bool:
        """
        Muestra mensaje y espera respuesta Y/N del jugador. Retorna True si Y.
        (Bloqueante, sencillo)
        """
        asking = True
        while asking:
            self.screen.fill((0,120,0))
            draw_text_center(self.screen, message, SCREEN_W//2, SCREEN_H//2, self.large_font, (255,255,255))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:
                        return True
                    if event.key == pygame.K_n:
                        return False
            self.clock.tick(30)
        return False

    def check_game_over(self):
        """Condición ejemplo: llegar a 30 puntos (puedes ajustar)."""
        if self.player_score >= 30 or self.cpu_score >= 30:
            return True
        return False

    # ---------- UI helpers ----------
    def draw_ui(self):
        # Puntajes
        draw_text_center(self.screen, f"{self.player_name}: {self.player_score}", 150, 30, self.large_font, (255,255,255))
        draw_text_center(self.screen, f"CPU: {self.cpu_score}", SCREEN_W-150, 30, self.large_font, (255,255,255))
        # Dibujar cartas del jugador
        rects = self.get_player_card_rects()
        for idx, c in enumerate(self.player_hand):
            img = load_card_image(c, (90,130))
            self.screen.blit(img, rects[idx].topleft)
        # Dibujar cartas CPU (ocultas)
        cpu_rects = self.get_cpu_card_rects()
        for idx in range(len(self.cpu_hand)):
            # dibujar dorso simple
            r = cpu_rects[idx]
            pygame.draw.rect(self.screen, (200,200,200), r)
            pygame.draw.rect(self.screen, (0,0,0), r, 2)
        # Dibujar cartas en mesa
        y = SCREEN_H//2 - 80
        x = SCREEN_W//2 - 200
        for idx, pair in enumerate(self.table_cards):
            p_card, c_card = pair
            if p_card:
                img = load_card_image(p_card, (80,110))
                self.screen.blit(img, (x + idx*180, y + 120))
            if c_card:
                img = load_card_image(c_card, (80,110))
                self.screen.blit(img, (x + idx*180, y))
        # instrucciones
        instr = "Click en una carta para jugar. T=cantar Truco, E=cantar Envido, Esc=volver"
        draw_text_center(self.screen, instr, SCREEN_W//2, SCREEN_H-30, self.font, (255,255,255))

    def get_player_card_rects(self):
        rects = []
        base_x = SCREEN_W//2 - 200
        y = SCREEN_H - 160
        for i in range(3):
            rects.append(pygame.Rect(base_x + i*140, y, 90, 130))
        return rects

    def get_cpu_card_rects(self):
        rects = []
        base_x = SCREEN_W//2 - 200
        y = 40
        for i in range(3):
            rects.append(pygame.Rect(base_x + i*140, y, 90, 130))
        return rects

