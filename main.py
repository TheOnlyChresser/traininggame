import pygame
from ui import UIDiv, UIText, Screen, UIInput

screen = Screen(800, 600)
surface = screen.surface
pygame.display.set_caption("AI spil")
menu=True

def start_game():
    global menu
    menu=False

def input_function():
    return print("WOOOHOOOO!")

menu = UIDiv(styles="flex flex-col justify-center top-180 items-center w-800 h-600 bg-neutral-50")

game = UIDiv(styles="w-800 h-600 bg-neutral-50 flex flex-col top-100")

loss_function = ""

def game_input(placeholder, initial_text):
    return UIInput(
        placeholder=placeholder,
        initial=initial_text,
        on_input=input_function,
        styles="w-300 h-60 bg-neutral-100 rounded-sm top-12 items-center flex flex-col justify-center font-arial"
    )

def game_button(text, on_click):
    return UIDiv(
        styles="w-300 h-60 bg-sky-500 rounded-sm hover:bg-sky-400 top-12 items-center flex flex-col justify-center",
        on_click=on_click,
        children=[UIText(text, styles="text-neutral-50 text-xl font-arial text-center")]
    )

menu.children.extend([
    UIDiv(styles="h-100 w-400 text-3xl font-arial top-0", children=[UIText("Velkommen til demoen", styles="text-center font-arial text-5xl")]),
    game_button("Prøv demo", lambda: start_game()),
    game_button("Afslut demo", lambda: exit())
])

game.children.extend([game_input("Skriv dit navn her", loss_function), game_button("Start spillet", lambda: start_game())])

game.compute_box()
menu.compute_box()


running = True
while running:
    mouse_position = pygame.mouse.get_pos()
    surface.fill((250,250,250))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if menu:
            menu.handle_event(event)
    if menu:
        menu.update_hover(mouse_position)
        menu.render(surface)
    elif not menu:
        game.update_hover(mouse_position)
        game.render(surface)

    pygame.display.update()


pygame.quit()