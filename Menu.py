import pygame
import sys
import os

pygame.init()

# --- CONFIGURACIÓN ---
# Obtener el directorio donde está este script
BASE_DIR = os.path.dirname(__file__)
# Armar la ruta completa hacia la carpeta IMG
IMG_DIR = os.path.join(BASE_DIR, "IMG")
# Ruta de la imagen de fondo
FONDO = os.path.join(IMG_DIR, "2f790fe1-b065-4dfc-939a-95b6c100a2cc.png")

# Colores
AMARILLO = (255, 255, 0)

# Ventana
screen = pygame.display.set_mode((1152, 768))
pygame.display.set_caption("Menu MA$TA")

# Opciones del menú (ya están pintadas en la imagen)
opciones = ["PLAY", "EXIT", "TUTORIAL"]
opcion_seleccionada = 0

# Coordenadas de las opciones en la imagen
posiciones = [
    (screen.get_width() // 2, 450),  # PLAY
    (screen.get_width() // 2, 550),  # EXIT
    (screen.get_width() // 2, 650)   # TUTORIAL
]

# Cargar fondo desde la carpeta IMG
fondo = pygame.image.load(FONDO).convert()

# Clock
clock = pygame.time.Clock()
running = True

while running:
    screen.blit(fondo, (0, 0))

    # Dibujar rectángulo de selección
    for i, pos in enumerate(posiciones):
        if i == opcion_seleccionada:
            x, y = pos
            rect = pygame.Rect(0, 0, 400, 60)
            rect.center = (x, y)
            pygame.draw.rect(screen, AMARILLO, rect, 3)

    pygame.display.flip()

    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                opcion_seleccionada = (opcion_seleccionada - 1) % len(opciones)
            elif event.key == pygame.K_DOWN:
                opcion_seleccionada = (opcion_seleccionada + 1) % len(opciones)
            elif event.key == pygame.K_RETURN:
                if opciones[opcion_seleccionada] == "EXIT":
                    running = False
                elif opciones[opcion_seleccionada] == "PLAY":
                    print("Iniciando el juego...")
                elif opciones[opcion_seleccionada] == "TUTORIAL":
                    print("Mostrando tutorial...")

    clock.tick(60)

pygame.quit()
sys.exit()
