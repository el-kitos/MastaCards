import pygame
import sys
import random
import os
import time

pygame.init()

# --- CONFIGURACIÓN ---
ANCHO, ALTO = 600, 700
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego de Minas - Temuliano")

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
GRIS = (40, 40, 40)
VERDE = (0, 200, 100)
ROJO = (200, 50, 50)
CELESTE = (50, 200, 200)
ACENTO = (140, 70, 200)
AZUL = (50, 150, 255)

# Grilla
FILAS, COLUMNAS = 5, 5
TAM_CASILLA = 80
GAP = 8
OFFSET_Y = 150

# Fuente
fuente = pygame.font.SysFont("Arial", 28, bold=True)
fuente_peque = pygame.font.SysFont("Arial", 20)

# Multiplicadores por cantidad de minas
MULTIPLICADORES = {
    3: 1.054,
    5: 1.12,
    10: 1.23,
    15: 1.56,
    24: 23.0
}

# Carpeta de imágenes
IMG_DIR = "IMG"

# Botones
APUESTAS = [10, 20, 50, 100, 500]
MINAS_OPCIONES = [3, 5, 10, 15, 24]

# --- Funciones auxiliares ---
def cargar_imagen(nombre, size=None, fallback_color=(100, 100, 100)):
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

money_img = cargar_imagen("money.png", (TAM_CASILLA-20, TAM_CASILLA-20), (0, 200, 0))
bomb_img = cargar_imagen("bomb.png", (TAM_CASILLA-20, TAM_CASILLA-20), (200, 0, 0))
tile_img = cargar_imagen("tile.png", (TAM_CASILLA, TAM_CASILLA), (30, 30, 30))


class Juego:
    def __init__(self):
        self.reset()

    def reset(self):
        self.minas = 0
        self.matriz_minas = [[False]*COLUMNAS for _ in range(FILAS)]
        self.revelado = [[False]*COLUMNAS for _ in range(FILAS)]
        self.jugando = False
        self.multiplicador = 1.0
        self.banca = 500
        self.apuesta = 0
        self.dinero_actual = 0
        self.explosiones = []
        self.msg = ""
        self.msg_timer = 0
        self.seleccion_minas = True
        self.perdiendo = False
        self.perdida_timer = 0

    # --- Funciones del juego ---
    def elegir_minas(self, cantidad):
        self.minas = cantidad
        self.seleccion_minas = False

    def iniciar_ronda(self):
        posiciones = random.sample(range(FILAS * COLUMNAS), self.minas)
        self.matriz_minas = [[False for _ in range(COLUMNAS)] for _ in range(FILAS)]
        for pos in posiciones:
            f, c = divmod(pos, COLUMNAS)
            self.matriz_minas[f][c] = True
        self.jugando = True
        self.multiplicador = 1.0
        self.revelado = [[False for _ in range(COLUMNAS)] for _ in range(FILAS)]
        self.dinero_actual = float(self.apuesta)

    def click_casilla(self, x, y):
        if not self.jugando or self.perdiendo:
            return
        fila = (y - OFFSET_Y) // (TAM_CASILLA + GAP)
        col = x // (TAM_CASILLA + GAP)
        if 0 <= fila < FILAS and 0 <= col < COLUMNAS:
            if self.revelado[fila][col]:
                return
            self.revelado[fila][col] = True
            if self.matriz_minas[fila][col]:
                self.dinero_actual = 0
                cx = col * (TAM_CASILLA + GAP) + TAM_CASILLA//2
                cy = fila * (TAM_CASILLA + GAP) + OFFSET_Y + TAM_CASILLA//2
                self.explosiones.append({"x": cx, "y": cy, "r": 8, "max_r": 90, "alpha": 220})
                self.revelar_todas_minas()
                self.jugando = False
                self.perdiendo = True
                self.perdida_timer = 90  # ~3 segundos a 30 FPS
            else:
                self.multiplicador *= MULTIPLICADORES.get(self.minas, 1.05)
                self.dinero_actual *= self.multiplicador

    def revelar_todas_minas(self):
        for f in range(FILAS):
            for c in range(COLUMNAS):
                if self.matriz_minas[f][c]:
                    self.revelado[f][c] = True

    def retirar(self):
        if self.jugando:
            self.banca += int(self.dinero_actual)
            self.jugando = False
            self.dinero_actual = 0
            self.apuesta = 0
            self.seleccion_minas = True

    def agregar_apuesta(self, monto):
        if self.jugando or self.seleccion_minas or self.perdiendo:
            return
        if self.apuesta + monto > self.banca:
            self.msg = "No tenés suficiente saldo"
            self.msg_timer = 60
            return
        self.apuesta += monto
        self.msg = f"Apuesta: ${self.apuesta}"
        self.msg_timer = 60

    # --- Función para actualizar estado de pérdida ---
    def actualizar_perdida(self):
        if self.perdiendo:
            self.perdida_timer -= 1
            if self.perdida_timer <= 0:
                self.apuesta = 0
                self.perdiendo = False
                self.seleccion_minas = True

    # --- Función para dibujar todo ---
    def dibujar(self, ventana):
        ventana.fill((10, 10, 10))

        # Textos
        ventana.blit(fuente.render(f"Banca: ${self.banca}", True, CELESTE), (20, 18))
        ventana.blit(fuente.render(f"Apuesta: ${self.apuesta}", True, VERDE), (20, 58))
        ventana.blit(fuente.render(f"Ganancia: ${int(self.dinero_actual)}", True, ACENTO), (20, 98))

        boton_rects = []

        # Botones de selección de minas
        if self.seleccion_minas:
            for i, val in enumerate(MINAS_OPCIONES):
                rect = pygame.Rect(20 + i*110, 140, 100, 40)
                pygame.draw.rect(ventana, AZUL, rect, border_radius=6)
                pygame.draw.rect(ventana, BLANCO, rect, 2, border_radius=6)
                ventana.blit(fuente_peque.render(str(val), True, BLANCO), (rect.x + 36, rect.y + 8))
                boton_rects.append(('minas', rect, val))
        else:
            # Botones de apuesta
            if not self.jugando and not self.perdiendo:
                for i, monto in enumerate(APUESTAS):
                    rect = pygame.Rect(20 + i*110, 140, 100, 40)
                    color = VERDE if self.apuesta + monto <= self.banca else GRIS
                    pygame.draw.rect(ventana, color, rect, border_radius=6)
                    pygame.draw.rect(ventana, BLANCO, rect, 2, border_radius=6)
                    ventana.blit(fuente_peque.render(f"${monto}", True, BLANCO), (rect.x + 25, rect.y + 8))
                    boton_rects.append(('apuesta', rect, monto))

            # Grilla
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for f in range(FILAS):
                for c in range(COLUMNAS):
                    x = c * (TAM_CASILLA + GAP)
                    y = f * (TAM_CASILLA + GAP) + OFFSET_Y
                    rect = pygame.Rect(x, y, TAM_CASILLA, TAM_CASILLA)
                    ventana.blit(tile_img, rect.topleft)
                    if rect.collidepoint(mouse_x, mouse_y) and not self.revelado[f][c] and self.jugando:
                        s = pygame.Surface((TAM_CASILLA, TAM_CASILLA), pygame.SRCALPHA)
                        s.fill((255, 255, 255, 30))
                        ventana.blit(s, rect.topleft)
                    if self.revelado[f][c]:
                        if self.matriz_minas[f][c]:
                            ventana.blit(bomb_img, (x + 10, y + 10))
                        else:
                            ventana.blit(money_img, (x + 10, y + 10))

        # Botón retirar
        retirar_rect = pygame.Rect(480, 20, 100, 40)
        if self.jugando:
            pygame.draw.rect(ventana, (25,25,25), retirar_rect, border_radius=6)
            pygame.draw.rect(ventana, VERDE, retirar_rect, 2, border_radius=6)
            ventana.blit(fuente_peque.render("RETIRAR", True, BLANCO), (retirar_rect.x + 10, retirar_rect.y + 8))

        # Explosiones
        expl_to_keep = []
        for exp in self.explosiones:
            max_r = exp["max_r"]
            surf = pygame.Surface((max_r*2,max_r*2), pygame.SRCALPHA)
            a = max(0, exp["alpha"])
            if exp["r"] < max_r:
                pygame.draw.circle(surf, (255,80,0,int(a)), (max_r,max_r), int(exp["r"]))
                pygame.draw.circle(surf, (255,170,0,int(max(0,a-80))), (max_r,max_r), int(max(0,exp["r"]//2)))
                ventana.blit(surf, (exp["x"] - max_r, exp["y"] - max_r))
                exp["r"] += 6
                exp["alpha"] -= 12
                expl_to_keep.append(exp)
        self.explosiones = expl_to_keep

        # Mensaje temporal
        if self.msg_timer > 0 and self.msg:
            ventana.blit(fuente_peque.render(self.msg, True, (255,220,120)), (20, 240))
            self.msg_timer -= 1

        pygame.display.flip()
        return boton_rects, retirar_rect


def main():
    juego = Juego()
    clock = pygame.time.Clock()

    while True:
        if juego.banca <= 0:
            pygame.quit()
            sys.exit()

        boton_rects, retirar_rect = juego.dibujar(VENTANA)
        juego.actualizar_perdida()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                for tipo, rect, val in boton_rects:
                    if rect.collidepoint(x, y):
                        if tipo == 'minas':
                            juego.elegir_minas(val)
                        elif tipo == 'apuesta':
                            juego.agregar_apuesta(val)

                # Iniciar ronda si ya hay apuesta y minas
                if not juego.seleccion_minas and not juego.jugando and juego.apuesta > 0:
                    juego.iniciar_ronda()

                if retirar_rect and retirar_rect.collidepoint(x, y):
                    juego.retirar()
                else:
                    juego.click_casilla(x, y)

        clock.tick(30)


if __name__ == "__main__":
    main()
