import pygame
from ui import UIDiv, UIText, Screen, colors

screen = Screen(800, 600)
surface = screen.surface
pygame.display.set_caption("AI spil")

menu = UIDiv(styles="flex flex-col justify-center top-180 items-center w-800 h-600 bg-neutral-50")

def game_button(text, on_click):
    return UIDiv(
        styles="w-300 h-60 bg-sky-500 rounded-md hover:bg-sky-400 top-12 items-center flex flex-col justify-center",
        on_click=on_click,
        children=[UIText(text, styles="text-neutral-50 text-xl font-arial text-center")]
    )

menu.children.extend([
    UIDiv(styles="h-100 w-400 text-3xl font-arial top-0", children=[UIText("Velkommen til demoen", styles="text-center font-arial text-5xl")]),
    game_button("Prøv demo", lambda: print("test")),
    game_button("Afslut demo", lambda: exit())
])

menu.compute_box()


running = True
while running:
    mouse_position = pygame.mouse.get_pos()
    surface.fill((250,250,250))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        menu.handle_event(event)
    
    menu.update_hover(mouse_position)
    menu.render(surface)

    pygame.display.update()


pygame.quit()