import pygame
import sys
import os

# ---------------- CONFIG ---------------- #
<<<<<<< Updated upstream
ANCHO, ALTO = 1152, 700
=======
ANCHO, ALTO = 1152, 768
>>>>>>> Stashed changes
FPS = 60
AMARILLO = (255, 255, 0)

pygame.init()
screen = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("MASTA - Menú")
clock = pygame.time.Clock()

<<<<<<< Updated upstream
# --- Posiciones del texto pintado en la imagen (NORMALIZADAS) --- 
POS_MENU_PRINCIPAL_NORM = [0.399, 0.526, 0.652]
OPCIONES_PRINCIPAL = ["PLAY", "EXIT", "TUTORIAL"]

# Tamaño de los rectángulos de resaltado y click (proporcional)
WBTN = int(ANCHO * 0.38)
HBTN = int(ALTO * 0.085)
=======
# Coordenadas de los textos que ya vienen pintados en la imagen
POS_MENU_PRINCIPAL = [
    (ANCHO // 2, 450),  # PLAY
    (ANCHO // 2, 550),  # EXIT
    (ANCHO // 2, 650)   # TUTORIAL
]
OPCIONES_PRINCIPAL = ["PLAY", "EXIT", "TUTORIAL"]

>>>>>>> Stashed changes

# ---------------- UTILIDADES ---------------- #
BASE_DIR = os.path.dirname(__file__)
IMG_DIR = os.path.join(BASE_DIR, "IMG")

def cargar_imagen(nombre, fallback_color=(10, 10, 10)):
<<<<<<< Updated upstream
=======
    """Carga una imagen de IMG/. Si no existe, devuelve un Surface color sólido."""
>>>>>>> Stashed changes
    ruta = os.path.join(IMG_DIR, nombre)
    if os.path.exists(ruta):
        img = pygame.image.load(ruta).convert()
        if img.get_size() != (ANCHO, ALTO):
            img = pygame.transform.smoothscale(img, (ANCHO, ALTO)).convert()
        return img
<<<<<<< Updated upstream
=======
    # Fallback: pantalla sólida si no está la imagen
>>>>>>> Stashed changes
    surf = pygame.Surface((ANCHO, ALTO))
    surf.fill(fallback_color)
    return surf

<<<<<<< Updated upstream
def get_btn_rect(center):
    rect = pygame.Rect(0, 0, WBTN, HBTN)
    rect.center = center
    return rect

def dibujar_resaltado(rect, grosor=3, color=AMARILLO):
=======
def dibujar_resaltado(pos, w=400, h=60, grosor=3, color=AMARILLO):
    rect = pygame.Rect(0, 0, w, h)
    rect.center = pos
>>>>>>> Stashed changes
    pygame.draw.rect(screen, color, rect, grosor)

def esperar_frame():
    pygame.display.flip()
    clock.tick(FPS)


# ---------------- ESCENAS ---------------- #
def menu_principal():
<<<<<<< Updated upstream
    fondo = cargar_imagen("mastafamilyfriendly.png")
    seleccion = 0
    cursor_hand = pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND)
    cursor_arrow = pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW)

    while True:
        centros = [(ANCHO // 2, int(ALTO * p)) for p in POS_MENU_PRINCIPAL_NORM]
        rects = [get_btn_rect(c) for c in centros]

        screen.blit(fondo, (0, 0))

        mouse_pos = pygame.mouse.get_pos()
        hovered = None
        for i, r in enumerate(rects):
            if r.collidepoint(mouse_pos):
                hovered = i
                break
        if hovered is not None:
            seleccion = hovered
            pygame.mouse.set_cursor(cursor_hand)
        else:
            pygame.mouse.set_cursor(cursor_arrow)

        dibujar_resaltado(rects[seleccion])
        esperar_frame()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

=======
    """
    Dibuja el menú principal usando la imagen con el texto ya pintado.
    Devuelve: 'play' | 'exit' | 'tutorial'
    """
    fondo = cargar_imagen("MENU MASTA.png")  # <- usa el nombre con espacio
    seleccion = 0

    while True:
        # Dibujo
        screen.blit(fondo, (0, 0))
        for i, pos in enumerate(POS_MENU_PRINCIPAL):
            if i == seleccion:
                dibujar_resaltado(pos)
        esperar_frame()

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
>>>>>>> Stashed changes
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP, pygame.K_w):
                    seleccion = (seleccion - 1) % len(OPCIONES_PRINCIPAL)
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    seleccion = (seleccion + 1) % len(OPCIONES_PRINCIPAL)
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    eleccion = OPCIONES_PRINCIPAL[seleccion]
<<<<<<< Updated upstream
                    if eleccion == "EXIT": return "exit"
                    if eleccion == "PLAY": return "play"  # siempre devuelve 'play'
                    if eleccion == "TUTORIAL": return "tutorial"

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if rects[seleccion].collidepoint(event.pos):
                    eleccion = OPCIONES_PRINCIPAL[seleccion]
                    if eleccion == "EXIT": return "exit"
                    if eleccion == "PLAY": return "play"  # siempre devuelve 'play'
                    if eleccion == "TUTORIAL": return "tutorial"
=======
                    if eleccion == "EXIT":
                        return "exit"
                    if eleccion == "PLAY":
                        return "play"
                    if eleccion == "TUTORIAL":
                        return "tutorial"
>>>>>>> Stashed changes


def menu_play():
    """
<<<<<<< Updated upstream
    Submenú simple para PLAY. Devuelve 'new_game' o 'back'.
    Sin mostrar el título 'PLAY MENU'.
    """
    opciones = ["NEW GAME", "BACK"]
    seleccion = 0
    fondo = cargar_imagen("mastafamilyfriendly.png")
    fuente = pygame.font.Font(None, 72)

    posiciones = [(ANCHO // 2, int(ALTO * 0.52)),
                  (ANCHO // 2, int(ALTO * 0.62))]

    cursor_hand = pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND)
    cursor_arrow = pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW)

    while True:
=======
    Submenú simple para PLAY. Devuelve 'start' o 'back'.
    (Podés cambiar opciones a lo que necesites.)
    """
    opciones = ["NEW GAME", "BACK"]
    seleccion = 0
    fondo = cargar_imagen("MENU MASTA.png")  # reutilizo el fondo; podés poner otro

    # Posiciones para este submenú
    posiciones = [(ANCHO // 2, 500), (ANCHO // 2, 600)]
    fuente = pygame.font.Font(None, 72)

    while True:
        # Fondo + leve oscurecido para contraste
>>>>>>> Stashed changes
        screen.blit(fondo, (0, 0))
        overlay = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 140))
        screen.blit(overlay, (0, 0))

<<<<<<< Updated upstream
        rects = []
        mouse_pos = pygame.mouse.get_pos()
        hovered = None

        for i, (txt, pos) in enumerate(zip(opciones, posiciones)):
            col = (255, 255, 255) if i != seleccion else AMARILLO
            rend = fuente.render(txt, True, col)
            r = rend.get_rect(center=pos)
            rects.append(r.inflate(30, 20))
            screen.blit(rend, r)
            if rects[i].collidepoint(mouse_pos):
                hovered = i

        if hovered is not None:
            seleccion = hovered
            pygame.mouse.set_cursor(cursor_hand)
        else:
            pygame.mouse.set_cursor(cursor_arrow)

        dibujar_resaltado(rects[seleccion])
        esperar_frame()

=======
        # Título
        titulo = fuente.render("PLAY MENU", True, (230, 230, 230))
        screen.blit(titulo, titulo.get_rect(center=(ANCHO//2, 380)))

        # Opciones
        for i, (txt, pos) in enumerate(zip(opciones, posiciones)):
            col = (255, 255, 255) if i != seleccion else AMARILLO
            rend = fuente.render(txt, True, col)
            screen.blit(rend, rend.get_rect(center=pos))
            if i == seleccion:
                dibujar_resaltado(pos, w=rend.get_width()+30, h=rend.get_height()+20)

        esperar_frame()

        # Eventos
>>>>>>> Stashed changes
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP, pygame.K_w):
                    seleccion = (seleccion - 1) % len(opciones)
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    seleccion = (seleccion + 1) % len(opciones)
<<<<<<< Updated upstream
                elif event.key == pygame.K_ESCAPE:
                    return "back"
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    return "new_game" if opciones[seleccion] == "NEW GAME" else "back"
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if rects[seleccion].collidepoint(event.pos):
                    return "new_game" if opciones[seleccion] == "NEW GAME" else "back"


def pantalla_tutorial():
=======
                elif event.key in (pygame.K_ESCAPE,):
                    return "back"
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    return "start" if opciones[seleccion] == "NEW GAME" else "back"


def pantalla_tutorial():
    """
    Muestra una imagen distinta para el tutorial.
    Poné tu archivo en IMG/TUTORIAL.png (cualquier tamaño, se escala).
    Volvés con ESC o ENTER.
    """
>>>>>>> Stashed changes
    fondo_tutorial = cargar_imagen("TUTORIAL.png", fallback_color=(20, 10, 30))
    fuente = pygame.font.Font(None, 48)

    while True:
        screen.blit(fondo_tutorial, (0, 0))
<<<<<<< Updated upstream
=======

        # Si no hay imagen, doy pistas (solo si usamos fallback oscuro)
>>>>>>> Stashed changes
        texto = "Press ESC to return"
        help_txt = fuente.render(texto, True, (230, 230, 230))
        screen.blit(help_txt, help_txt.get_rect(center=(ANCHO//2, ALTO-60)))

        esperar_frame()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_SPACE):
                    return
<<<<<<< Updated upstream
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                return
=======


def pantalla_mensaje(msg, segundos=1.2):
    """Pantalla breve para feedback (opcional)."""
    screen.fill((0, 0, 0))
    fuente = pygame.font.Font(None, 72)
    rend = fuente.render(msg, True, (230, 230, 230))
    screen.blit(rend, rend.get_rect(center=(ANCHO//2, ALTO//2)))
    esperar_frame()
    pygame.time.delay(int(segundos * 1000))
>>>>>>> Stashed changes


# ---------------- BUCLE PRINCIPAL ---------------- #
def main():
    while True:
<<<<<<< Updated upstream
=======
        # 1) Menú principal
>>>>>>> Stashed changes
        destino = menu_principal()
        if destino == "exit":
            pygame.quit(); sys.exit()
        elif destino == "play":
            elec = menu_play()
<<<<<<< Updated upstream
            if elec == "new_game":
                pantalla_tutorial()  # NEW GAME abre la pantalla del tutorial
        elif destino == "tutorial":
            pantalla_tutorial()


if __name__ == "__main__":
    main()

#flama tu menu broder atte 4to
=======
            if elec == "start":
                pantalla_mensaje("Starting game...")
                # acá podrías saltar al loop real del juego
        elif destino == "tutorial":
            pantalla_tutorial()

if __name__ == "__main__":
    main()
>>>>>>> Stashed changes
