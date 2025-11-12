"""
Módulo principal del juego: lógica de turno, UI de juego, manejo de Truco y Envido.
SISTEMA CORRECTO:
- Mano normal = 1 punto
- Truco aceptado = 2 puntos
- Se gana una MANO con 2 JUGADAS ganadas (best of 3)
"""

import pygame
from truco.cartas import Deck, compare_cards, calculate_envido, Card, cargar_imagenes_cartas
from truco.utils import load_card_image, draw_text_center
from truco.data_manager import save_history
from truco.ai import choose_card_ai, decide_accept_truco, decide_accept_envido, decide_call_truco, decide_call_envido
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
        
        # Fuentes con tamaños claros
        self.font_huge = pygame.font.SysFont("arial", 42, bold=True)
        self.font_large = pygame.font.SysFont("arial", 32, bold=True)
        self.font_medium = pygame.font.SysFont("arial", 24)
        self.font_small = pygame.font.SysFont("arial", 18)
        
        # Cargar imágenes de cartas
        cargar_imagenes_cartas()
        
        # Puntaje total del partido
        self.player_score = 0
        self.cpu_score = 0
        self.game_over = False
        self.winner_message = ""
        
        # Iniciar primera mano
        self.reset_hand()

    def reset_hand(self):
        """Resetea una MANO (conjunto de hasta 3 JUGADAS)"""
        self.deck = Deck()
        self.player_hand = self.deck.deal(3)
        self.cpu_hand = self.deck.deal(3)
        
        # Victorias de JUGADAS en esta MANO
        self.jugadas_ganadas = {self.player_name: 0, "CPU": 0}
        self.table_cards = []  # Lista de tuplas (player_card, cpu_card) por jugada
        
        # SISTEMA DE PUNTOS CORRECTO
        self.hand_value = 1  # Valor BASE de la mano SIN truco
        self.truco_cantado = False
        self.truco_aceptado = False
        
        # Envido
        self.envido_cantado = False
        self.envido_resuelto = False
        self.primera_carta_jugada = False
        
        # Mensajes
        self.mensaje = ""
        self.mensaje_timer = 0
        
        # Turno inicial (aleatorio o del ganador anterior)
        self.turn = "player" if random.random() < 0.5 else "cpu"
        self.mano_terminada = False

    def mostrar_mensaje(self, texto, duracion=2.0):
        """Muestra un mensaje temporal"""
        self.mensaje = texto
        self.mensaje_timer = duracion

    def actualizar_mensajes(self, dt):
        """Actualiza el timer de mensajes"""
        if self.mensaje_timer > 0:
            self.mensaje_timer -= dt
            if self.mensaje_timer <= 0:
                self.mensaje = ""

    def play(self):
        """Bucle principal de la partida"""
        running = True
        while running:
            dt = self.clock.tick(30) / 1000.0
            
            self.screen.fill((0, 100, 0))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "salir"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return "menu"
            
            self.actualizar_mensajes(dt)
            self.draw_ui()
            
            if self.game_over:
                self.draw_game_over()
                pygame.display.flip()
                
                waiting = True
                while waiting:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            return "salir"
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                                self.player_score = 0
                                self.cpu_score = 0
                                self.game_over = False
                                self.reset_hand()
                                waiting = False
                            elif event.key == pygame.K_ESCAPE:
                                return "menu"
                    self.clock.tick(30)
            
            elif self.mano_terminada:
                time.sleep(1.5)
                self.reset_hand()
            
            else:
                if self.turn == "player":
                    result = self.player_turn()
                    if result == "salir":
                        return "salir"
                    elif result == "menu":
                        return "menu"
                else:
                    self.cpu_turn()
            
            pygame.display.flip()
        
        return "menu"

    def player_turn(self):
        """Turno del jugador"""
        # CPU puede cantar antes
        if not self.primera_carta_jugada and not self.envido_cantado and self.vs_ai:
            if decide_call_envido(self.cpu_hand):
                self.mostrar_mensaje("¡CPU CANTA ENVIDO!", 2.5)
                self.draw_ui()
                pygame.display.flip()
                time.sleep(1.5)
                
                accepted = self.prompt_yes_no("CPU canta ENVIDO\n¿Aceptas?")
                if not accepted:
                    self.cpu_score += 1
                    self.mostrar_mensaje(f"Envido rechazado - CPU gana 1 punto", 2.5)
                    self.mano_terminada = True
                    self.check_game_over()
                    return
                else:
                    self.manejar_comparacion_envido()
                    return
        
        if not self.truco_cantado and self.vs_ai:
            if decide_call_truco(self.cpu_hand):
                self.mostrar_mensaje("¡CPU CANTA TRUCO!", 2.5)
                self.draw_ui()
                pygame.display.flip()
                time.sleep(1.5)
                
                accepted = self.prompt_yes_no("CPU canta TRUCO\n¿Aceptas?")
                if not accepted:
                    # Rechazado: CPU gana el valor actual (1 punto)
                    self.cpu_score += self.hand_value
                    self.mostrar_mensaje(f"Truco rechazado - CPU gana {self.hand_value} punto", 2.5)
                    self.mano_terminada = True
                    self.check_game_over()
                    return
                else:
                    # Aceptado: ahora vale 2 puntos
                    self.truco_cantado = True
                    self.truco_aceptado = True
                    self.hand_value = 2
                    self.mostrar_mensaje("Truco aceptado - La mano vale 2 puntos", 2.5)
        
        # Turno del jugador para elegir carta
        clicked_card = None
        waiting = True
        
        while waiting:
            dt = self.clock.tick(30) / 1000.0
            self.actualizar_mensajes(dt)
            self.screen.fill((0, 100, 0))
            self.draw_ui()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "salir"
                
                if event.type == pygame.KEYDOWN:
                    # Cantar TRUCO
                    if event.key == pygame.K_t:
                        if not self.truco_cantado:
                            accepted = self.manejar_canto_truco(caller="player")
                            if not accepted:
                                self.player_score += self.hand_value
                                self.mostrar_mensaje(f"Truco rechazado - Ganas {self.hand_value} punto", 2.5)
                                self.mano_terminada = True
                                self.check_game_over()
                                return
                            else:
                                self.truco_cantado = True
                                self.truco_aceptado = True
                                self.hand_value = 2
                                self.mostrar_mensaje("Truco aceptado - La mano vale 2 puntos", 2.5)
                        else:
                            self.mostrar_mensaje("Ya se cantó Truco", 1.5)
                    
                    # Cantar ENVIDO
                    if event.key == pygame.K_e:
                        if not self.primera_carta_jugada and not self.envido_cantado:
                            accepted = self.manejar_canto_envido(caller="player")
                            if not accepted:
                                self.player_score += 1
                                self.mostrar_mensaje("Envido rechazado - Ganas 1 punto", 2.5)
                                self.mano_terminada = True
                                self.check_game_over()
                                return
                            else:
                                self.manejar_comparacion_envido()
                        else:
                            if self.primera_carta_jugada:
                                self.mostrar_mensaje("¡Solo se puede cantar Envido ANTES de jugar!", 2.0)
                            else:
                                self.mostrar_mensaje("Ya se cantó Envido", 1.5)
                    
                    if event.key == pygame.K_ESCAPE:
                        return "menu"
                
                # Click en carta
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mx, my = pygame.mouse.get_pos()
                    rects = self.get_player_card_rects()
                    for idx, r in enumerate(rects):
                        if idx < len(self.player_hand) and r.collidepoint((mx, my)):
                            clicked_card = self.player_hand.pop(idx)
                            waiting = False
                            break
            
            pygame.display.flip()
        
        if clicked_card:
            self.primera_carta_jugada = True
            self.table_cards.append((clicked_card, None))
            
            # CPU responde
            if self.vs_ai and self.cpu_hand:
                time.sleep(0.5)
                cpu_choice = choose_card_ai(self.cpu_hand, [c for c, _ in self.table_cards], len(self.table_cards))
                self.cpu_hand.remove(cpu_choice)
                self.table_cards[-1] = (clicked_card, cpu_choice)
                
                self.resolver_jugada()

    def cpu_turn(self):
        """Turno de la CPU"""
        # CPU puede cantar antes
        if not self.primera_carta_jugada and not self.envido_cantado and self.vs_ai:
            if decide_call_envido(self.cpu_hand):
                self.mostrar_mensaje("¡CPU CANTA ENVIDO!", 2.5)
                self.draw_ui()
                pygame.display.flip()
                time.sleep(1.5)
                
                accepted = self.prompt_yes_no("CPU canta ENVIDO\n¿Aceptas?")
                if not accepted:
                    self.cpu_score += 1
                    self.mostrar_mensaje(f"Envido rechazado - CPU gana 1 punto", 2.5)
                    self.mano_terminada = True
                    self.check_game_over()
                    return
                else:
                    self.manejar_comparacion_envido()
                    return
        
        if not self.truco_cantado and self.vs_ai:
            if decide_call_truco(self.cpu_hand):
                self.mostrar_mensaje("¡CPU CANTA TRUCO!", 2.5)
                self.draw_ui()
                pygame.display.flip()
                time.sleep(1.5)
                
                accepted = self.prompt_yes_no("CPU canta TRUCO\n¿Aceptas?")
                if not accepted:
                    self.cpu_score += self.hand_value
                    self.mostrar_mensaje(f"Truco rechazado - CPU gana {self.hand_value} punto", 2.5)
                    self.mano_terminada = True
                    self.check_game_over()
                    return
                else:
                    self.truco_cantado = True
                    self.truco_aceptado = True
                    self.hand_value = 2
                    self.mostrar_mensaje("Truco aceptado - La mano vale 2 puntos", 2.5)
        
        # CPU juega carta
        if not self.cpu_hand:
            return
        
        time.sleep(0.8)
        cpu_card = choose_card_ai(self.cpu_hand, [c for c, _ in self.table_cards], len(self.table_cards))
        self.cpu_hand.remove(cpu_card)
        self.primera_carta_jugada = True
        
        self.table_cards.append((None, cpu_card))
        
        # Jugador responde
        waiting = True
        while waiting:
            dt = self.clock.tick(30) / 1000.0
            self.actualizar_mensajes(dt)
            self.screen.fill((0, 100, 0))
            self.draw_ui()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mx, my = pygame.mouse.get_pos()
                    rects = self.get_player_card_rects()
                    for idx, r in enumerate(rects):
                        if idx < len(self.player_hand) and r.collidepoint((mx, my)):
                            player_card = self.player_hand.pop(idx)
                            self.table_cards[-1] = (player_card, cpu_card)
                            waiting = False
                            break
                
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return
            
            pygame.display.flip()
        
        self.resolver_jugada()

    def resolver_jugada(self):
        """Resuelve UNA JUGADA de la mano"""
        if not self.table_cards:
            return
        
        last = self.table_cards[-1]
        player_card, cpu_card = last
        
        if player_card is None or cpu_card is None:
            return
        
        cmp = compare_cards(player_card, cpu_card)
        
        if cmp == 1:
            winner = self.player_name
            self.mostrar_mensaje(f"¡Ganaste esta jugada!", 1.8)
        elif cmp == -1:
            winner = "CPU"
            self.mostrar_mensaje(f"CPU gana esta jugada", 1.8)
        else:
            winner = "empate"
            self.mostrar_mensaje(f"¡Parda! (empate)", 1.8)
        
        if winner != "empate":
            self.jugadas_ganadas[winner] += 1
        
        time.sleep(1.0)
        
        # Verificar si alguien ganó la MANO (2 jugadas ganadas)
        if self.jugadas_ganadas[self.player_name] == 2:
            self.terminar_mano(self.player_name)
        elif self.jugadas_ganadas["CPU"] == 2:
            self.terminar_mano("CPU")
        elif len(self.table_cards) == 3:
            # Se jugaron las 3 cartas
            if self.jugadas_ganadas[self.player_name] > self.jugadas_ganadas["CPU"]:
                self.terminar_mano(self.player_name)
            elif self.jugadas_ganadas["CPU"] > self.jugadas_ganadas[self.player_name]:
                self.terminar_mano("CPU")
            else:
                # Empate total (parda-parda-parda o 1-1)
                self.terminar_mano(self.player_name)

    def terminar_mano(self, winner):
        """Termina la MANO y otorga puntos"""
        if winner == self.player_name:
            self.player_score += self.hand_value
            self.mostrar_mensaje(f"¡GANASTE LA MANO! +{self.hand_value} punto(s)", 3.0)
        else:
            self.cpu_score += self.hand_value
            self.mostrar_mensaje(f"CPU GANA LA MANO +{self.hand_value} punto(s)", 3.0)
        
        save_history({
            "hand_winner": winner,
            "player_score": self.player_score,
            "cpu_score": self.cpu_score,
            "timestamp": time.time()
        })
        
        self.mano_terminada = True
        self.check_game_over()

    def manejar_canto_truco(self, caller="player") -> bool:
        """Maneja el canto de Truco"""
        if caller == "player":
            if self.vs_ai:
                return decide_accept_truco()
        return True

    def manejar_canto_envido(self, caller="player") -> bool:
        """Maneja el canto de Envido"""
        if caller == "player":
            if self.vs_ai:
                self.envido_cantado = True
                return decide_accept_envido(self.cpu_hand)
        return True

    def manejar_comparacion_envido(self):
        """Compara los envidos y otorga 2 puntos al ganador"""
        p_en = calculate_envido(self.player_hand)
        c_en = calculate_envido(self.cpu_hand)
        
        self.mostrar_mensaje(f"Tu envido: {p_en} | CPU: {c_en}", 3.5)
        self.draw_ui()
        pygame.display.flip()
        time.sleep(3.0)
        
        if p_en > c_en:
            self.player_score += 2
            self.mostrar_mensaje(f"¡GANASTE EL ENVIDO! +2 puntos", 2.5)
        elif c_en > p_en:
            self.cpu_score += 2
            self.mostrar_mensaje(f"CPU GANA EL ENVIDO +2 puntos", 2.5)
        else:
            # Empate - gana el mano (asumimos jugador)
            self.player_score += 2
            self.mostrar_mensaje(f"Empate en Envido - ¡Ganaste! +2 puntos", 2.5)
        
        self.envido_resuelto = True
        self.check_game_over()

    def prompt_yes_no(self, mensaje: str) -> bool:
        """Muestra diálogo Y/N"""
        asking = True
        while asking:
            self.screen.fill((0, 100, 0))
            
            # Fondo oscuro
            overlay = pygame.Surface((SCREEN_W, SCREEN_H))
            overlay.set_alpha(200)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))
            
            # Cuadro de diálogo
            dialog_rect = pygame.Rect(SCREEN_W//2 - 250, SCREEN_H//2 - 100, 500, 200)
            pygame.draw.rect(self.screen, (50, 50, 50), dialog_rect)
            pygame.draw.rect(self.screen, (255, 255, 0), dialog_rect, 4)
            
            # Texto
            lines = mensaje.split('\n')
            y_offset = SCREEN_H//2 - 60
            for line in lines:
                draw_text_center(self.screen, line, SCREEN_W//2, y_offset, self.font_large, (255, 255, 255))
                y_offset += 40
            
            draw_text_center(self.screen, "Y = SÍ  |  N = NO", SCREEN_W//2, SCREEN_H//2 + 50, self.font_medium, (255, 255, 0))
            
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
        """Verifica si el juego terminó (30 puntos)"""
        if self.player_score >= 30:
            self.game_over = True
            self.winner_message = f"¡{self.player_name} GANÓ EL PARTIDO!"
            save_history({
                "winner": self.player_name,
                "player_score": self.player_score,
                "cpu_score": self.cpu_score,
                "timestamp": time.time()
            })
        elif self.cpu_score >= 30:
            self.game_over = True
            self.winner_message = "CPU GANÓ EL PARTIDO"
            save_history({
                "winner": "CPU",
                "player_score": self.player_score,
                "cpu_score": self.cpu_score,
                "timestamp": time.time()
            })

    def draw_game_over(self):
        """Pantalla de fin de juego"""
        overlay = pygame.Surface((SCREEN_W, SCREEN_H))
        overlay.set_alpha(220)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        draw_text_center(self.screen, self.winner_message, SCREEN_W//2, SCREEN_H//2 - 80, 
                        self.font_huge, (255, 255, 0))
        draw_text_center(self.screen, f"Puntaje Final: {self.player_score} - {self.cpu_score}", 
                        SCREEN_W//2, SCREEN_H//2, self.font_large, (255, 255, 255))
        draw_text_center(self.screen, "ENTER = Jugar de nuevo  |  ESC = Menú", 
                        SCREEN_W//2, SCREEN_H//2 + 80, self.font_medium, (200, 200, 200))

    def draw_ui(self):
        """Dibuja la interfaz - POSICIONAMIENTO CLARO"""
        # ========== PUNTAJES TOTALES (arriba) ==========
        draw_text_center(self.screen, f"{self.player_name}", 120, 25, self.font_medium, (255, 255, 255))
        draw_text_center(self.screen, f"{self.player_score} puntos", 120, 55, self.font_huge, (255, 255, 100))
        
        draw_text_center(self.screen, f"CPU", SCREEN_W - 120, 25, self.font_medium, (255, 255, 255))
        draw_text_center(self.screen, f"{self.cpu_score} puntos", SCREEN_W - 120, 55, self.font_huge, (255, 100, 100))
        
        # ========== ESTADO DE LA MANO (centro arriba) ==========
        valor_texto = f"MANO: {self.hand_value} PUNTO{'S' if self.hand_value > 1 else ''}"
        if self.truco_cantado:
            valor_texto += " [TRUCO]"
        draw_text_center(self.screen, valor_texto, SCREEN_W//2, 35, self.font_large, (255, 255, 0))
        
        # ========== JUGADAS GANADAS ==========
        jugadas_texto = f"Jugadas ganadas: {self.jugadas_ganadas[self.player_name]} - {self.jugadas_ganadas['CPU']}"
        draw_text_center(self.screen, jugadas_texto, SCREEN_W//2, 75, self.font_medium, (200, 200, 200))
        
        # ========== MENSAJE TEMPORAL ==========
        if self.mensaje:
            # Fondo para el mensaje
            msg_rect = pygame.Rect(SCREEN_W//2 - 300, 110, 600, 50)
            pygame.draw.rect(self.screen, (0, 0, 0), msg_rect)
            pygame.draw.rect(self.screen, (255, 255, 0), msg_rect, 3)
            draw_text_center(self.screen, self.mensaje, SCREEN_W//2, 135, self.font_large, (255, 255, 0))
        
        # ========== CARTAS DEL JUGADOR (abajo) ==========
        rects = self.get_player_card_rects()
        for idx, c in enumerate(self.player_hand):
            if idx < len(rects):
                img = load_card_image(c, (100, 145))
                self.screen.blit(img, rects[idx].topleft)
                # Borde para resaltar
                pygame.draw.rect(self.screen, (255, 255, 255), rects[idx], 2)
        
        # ========== CARTAS CPU (arriba - dorso) ==========
        cpu_rects = self.get_cpu_card_rects()
        for idx in range(len(self.cpu_hand)):
            if idx < len(cpu_rects):
                r = cpu_rects[idx]
                pygame.draw.rect(self.screen, (150, 0, 0), r)
                pygame.draw.rect(self.screen, (200, 200, 200), r, 3)
                # Texto "CPU"
                draw_text_center(self.screen, "CPU", r.centerx, r.centery, self.font_medium, (255, 255, 255))
        
        # ========== CARTAS EN MESA (centro) ==========
        y_cpu = 220
        y_player = 380
        x_start = SCREEN_W//2 - 180
        
        for idx, pair in enumerate(self.table_cards):
            p_card, c_card = pair
            x_pos = x_start + idx * 120
            
            if c_card:
                img = load_card_image(c_card, (90, 130))
                self.screen.blit(img, (x_pos, y_cpu))
            
            if p_card:
                img = load_card_image(p_card, (90, 130))
                self.screen.blit(img, (x_pos, y_player))
        
        # ========== INSTRUCCIONES (abajo) ==========
        instr = "CLICK: Jugar carta  |  T: Cantar Truco  |  E: Cantar Envido  |  ESC: Menú"
        draw_text_center(self.screen, instr, SCREEN_W//2, SCREEN_H - 25, self.font_small, (255, 255, 255))

    def get_player_card_rects(self):
        """Rectángulos de cartas del jugador"""
        rects = []
        base_x = SCREEN_W//2 - 180
        y = SCREEN_H - 170
        for i in range(3):
            rects.append(pygame.Rect(base_x + i * 120, y, 100, 145))
        return rects

    def get_cpu_card_rects(self):
        """Rectángulos de cartas CPU"""
        rects = []
        base_x = SCREEN_W//2 - 180
        y = 180
        for i in range(3):
            rects.append(pygame.Rect(base_x + i * 120, y, 100, 145))
        return rects