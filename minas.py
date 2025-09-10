import pygame
import sys
import random
import os

pygame.init()

# --- CONFIGURACIÓN ---
ANCHO, ALTO = 600, 750
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego de Minas - Temuliano")

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
GRIS = (40, 40, 40)
VERDE = (0, 200, 100)
ROJO = (200, 50, 50)
CELESTE = (50, 200, 200)

# Grilla
FILAS, COLUMNAS = 5, 5
TAM_CASILLA = 100
OFFSET_Y = 180

# Fuente
fuente = pygame.font.SysFont("Arial", 28, bold=True)
fuente_peque = pygame.font.SysFont("Arial", 22)

# Multiplicadores
MULTIPLICADORES = {
    3: 1.054,
    5: 1.12,
    10: 1.23,
    15: 1.56,
    24: 23.0
}

IMG_DIR = "IMG"

def cargar_imagen(nombre, size=None, fallback_color=(100, 100, 100)):
    ruta = os.path.join(IMG_DIR, nombre)
    if os.path.exists(ruta):
        img = pygame.image.load(ruta).convert_alpha()
        if size:
            img = pygame.transform.smoothscale(img, size)
        return img
    surf = pygame.Surface(size if size else (50, 50))
    surf.fill(fallback_color)
    return surf

# --- CARGAR IMÁGENES ---
money_img = cargar_imagen("money.png", (TAM_CASILLA-20, TAM_CASILLA-20), (0, 200, 0))
bomb_img = cargar_imagen("bomb.png", (TAM_CASILLA-20, TAM_CASILLA-20), (200, 0, 0))
tile_img = cargar_imagen("tile.png", (TAM_CASILLA, TAM_CASILLA), (50, 50, 50))


class Juego:
    def __init__(self):
        self.reset()

    def reset(self):
        self.minas = 0
        self.matriz_minas = []
        self.revelado = [[False for _ in range(COLUMNAS)] for _ in range(FILAS)]
        self.jugando = False
        self.multiplicador = 1.0
        self.banca = 500
        self.apuesta = 0
        self.dinero_actual = 0
        self.input_apuesta = ""  # texto que escribe el jugador
        self.explosiones = []  # animaciones activas

    def elegir_minas(self, cantidad):
        self.minas = cantidad
        posiciones = random.sample(range(FILAS * COLUMNAS), cantidad)
        self.matriz_minas = [[False for _ in range(COLUMNAS)] for _ in range(FILAS)]
        for pos in posiciones:
            f, c = divmod(pos, COLUMNAS)
            self.matriz_minas[f][c] = True
        self.jugando = True
        self.multiplicador = 1.0
        self.revelado = [[False for _ in range(COLUMNAS)] for _ in range(FILAS)]
        self.dinero_actual = self.apuesta

    def click(self, x, y):
        if not self.jugando:
            return
        fila = (y - OFFSET_Y) // TAM_CASILLA
        col = x // TAM_CASILLA
        if 0 <= fila < FILAS and 0 <= col < COLUMNAS:
            if self.revelado[fila][col]:
                return
            self.revelado[fila][col] = True
            if self.matriz_minas[fila][col]:  # Mina
                self.dinero_actual = 0
                self.jugando = False
                # Añadir animación
                cx = col * TAM_CASILLA + TAM_CASILLA//2
                cy = fila * TAM_CASILLA + OFFSET_Y + TAM_CASILLA//2
                self.explosiones.append({"x": cx, "y": cy, "r": 10, "max_r": 80})
            else:  # Acierto
                self.multiplicador *= MULTIPLICADORES[self.minas]
                self.dinero_actual *= self.multiplicador

    def retirar(self):
        if self.jugando:
            self.banca += self.dinero_actual
            self.jugando = False
            self.dinero_actual = 0

    def apostar(self):
        if not self.jugando and self.input_apuesta.isdigit():
            cantidad = int(self.input_apuesta)
            if cantidad <= self.banca and cantidad > 0:
                self.apuesta = cantidad
                self.banca -= cantidad
            self.input_apuesta = ""  # limpiar input

    def dibujar(self, ventana):
        # Fondo degradado oscuro
        for i in range(ALTO):
            color = (i//10, i//15, i//12)
            pygame.draw.line(ventana, color, (0, i), (ANCHO, i))

        # Dinero
        texto = fuente.render(f"Banca: ${self.banca:.2f}", True, CELESTE)
        ventana.blit(texto, (20, 20))
        texto2 = fuente.render(f"Apuesta: ${self.apuesta}", True, VERDE)
        ventana.blit(texto2, (20, 60))
        texto3 = fuente.render(f"Ganancia: ${self.dinero_actual:.2f}", True, ROJO)
        ventana.blit(texto3, (20, 100))

        # Input apuesta
        if not self.jugando:
            rect = pygame.Rect(300, 20, 200, 40)
            pygame.draw.rect(ventana, (30, 30, 30), rect)
            pygame.draw.rect(ventana, BLANCO, rect, 2)
            txt = fuente.render(self.input_apuesta, True, BLANCO)
            ventana.blit(txt, (rect.x + 10, rect.y + 5))

            # Botón confirmar
            btn = pygame.Rect(300, 70, 120, 30)
            pygame.draw.rect(ventana, VERDE, btn)
            txt = fuente_peque.render("CONFIRMAR", True, NEGRO)
            ventana.blit(txt, (btn.x + 10, btn.y + 5))

        # Botones de minas
        if not self.jugando and self.apuesta > 0:
            opciones = [3, 5, 10, 15, 24]
            for i, val in enumerate(opciones):
                rect = pygame.Rect(20 + i * 110, 140, 100, 25)
                pygame.draw.rect(ventana, (60, 60, 60), rect)
                txt = fuente.render(str(val), True, BLANCO)
                ventana.blit(txt, (rect.x + 30, rect.y))

        # Botón retirar
        if self.jugando:
            rect = pygame.Rect(450, 120, 120, 30)
            pygame.draw.rect(ventana, VERDE, rect)
            txt = fuente.render("RETIRAR", True, NEGRO)
            ventana.blit(txt, (rect.x + 10, rect.y + 2))

        # Dibujar grilla
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for f in range(FILAS):
            for c in range(COLUMNAS):
                x = c * TAM_CASILLA
                y = f * TAM_CASILLA + OFFSET_Y
                rect = pygame.Rect(x, y, TAM_CASILLA, TAM_CASILLA)

                # hover efecto
                if rect.collidepoint(mouse_x, mouse_y):
                    ventana.blit(tile_img, rect.topleft)
                    s = pygame.Surface((TAM_CASILLA, TAM_CASILLA), pygame.SRCALPHA)
                    s.fill((255, 255, 255, 50))
                    ventana.blit(s, rect.topleft)
                else:
                    ventana.blit(tile_img, rect.topleft)

                if self.revelado[f][c]:
                    if self.matriz_minas[f][c]:
                        ventana.blit(bomb_img, (x+10, y+10))
                    else:
                        ventana.blit(money_img, (x+10, y+10))

        # Dibujar animaciones de explosión
        for exp in self.explosiones:
            pygame.draw.circle(ventana, ROJO, (exp["x"], exp["y"]), exp["r"])
            pygame.draw.circle(ventana, (255, 150, 0), (exp["x"], exp["y"]), exp["r"]//2)
            exp["r"] += 5
        self.explosiones = [e for e in self.explosiones if e["r"] < e["max_r"]]

        pygame.display.flip()


def main():
    juego = Juego()
    clock = pygame.time.Clock()

    while True:
        if juego.banca <= 0:
            pygame.quit()
            sys.exit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and not juego.jugando:
                if event.key == pygame.K_BACKSPACE:
                    juego.input_apuesta = juego.input_apuesta[:-1]
                elif event.unicode.isdigit():
                    juego.input_apuesta += event.unicode

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if not juego.jugando:
                    # Confirmar apuesta
                    if 300 <= x <= 420 and 70 <= y <= 100:
                        juego.apostar()
                    # Botones minas
                    if juego.apuesta > 0 and 140 <= y <= 165:
                        opciones = [3, 5, 10, 15, 24]
                        for i, val in enumerate(opciones):
                            if 20 + i * 110 <= x <= 120 + i * 110:
                                juego.elegir_minas(val)
                else:
                    # Retirar
                    if 450 <= x <= 570 and 120 <= y <= 150:
                        juego.retirar()
                    else:
                        juego.click(x, y)

        juego.dibujar(VENTANA)
        clock.tick(30)


if __name__ == "__main__":
    main()
