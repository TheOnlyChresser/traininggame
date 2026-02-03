import pygame
from ui import UIDiv, UIText, Screen, UIInput

def game_input(placeholder):
    return UIInput(
        placeholder=placeholder,
        styles="w-300 h-60 bg-neutral-100 rounded-sm items-center flex flex-col justify-center font-arial"
    )

def game_button(text, on_click):
    return UIDiv(
        styles="w-300 h-60 bg-sky-500 rounded-sm hover:bg-sky-400 top-12 items-center flex flex-col justify-center",
        on_click=on_click,
        children=[UIText(text, styles="text-neutral-50 text-xl font-arial text-center")]
    )

screen = Screen(800, 600)
surface = screen.surface
pygame.display.set_caption("AI spil")
menu=True
training=False

def start_game():
    global menu
    menu=False

def progress_bar(value):
    bar_width = 400
    bar_height = 30
    filled_width = int(bar_width * value)

    pygame.draw.rect(surface, (200, 200, 200), (200, 300, bar_width, bar_height))
    pygame.draw.rect(surface, (100, 200, 100), (200, 300, filled_width, bar_height))

def start_training(node_count, layer_count, learning_rate, epochs, loss_function):
    global training
    training = True
    print("Træning startet med følgende parametre:")
    print(f"Noder: {node_count}, Lag: {layer_count}, Læringsrate: {learning_rate}, Epoker: {epochs}, Tabelfunktion: {loss_function}")
    progress_bar(0.5)

menu = UIDiv(styles="flex flex-col justify-center top-180 items-center w-800 h-600 bg-neutral-50")

game = UIDiv(styles="w-800 h-1200 bg-neutral-50 flex flex-col top-0")

menu.children.extend([
    UIDiv(styles="h-100 w-400 text-3xl font-arial top-0", children=[UIText("Velkommen til demoen", styles="text-center font-arial text-5xl")]),
    game_button("Prøv demo", lambda: start_game()),
    game_button("Afslut demo", lambda: exit())
])

is_dropdown_open = False

def dropdown_trigger(options, placeholder="Vælg tabelfunktion"):
    global is_dropdown_open

    return UIDiv(
        styles="w-300 h-60 bg-neutral-100 rounded-sm top-12 items-center flex flex-col justify-center font-arial",
        on_click=lambda: setattr(globals(), 'is_dropdown_open', not is_dropdown_open),
        children=[UIText(placeholder, styles="text-neutral-700 text-center")],
    )

def dropdown_option(text, on_click):
    return UIDiv(
        styles="w-300 h-40 bg-neutral-200 rounded-sm hover:bg-neutral-300 top-0 items-center flex flex-col justify-center font-arial",
        on_click=on_click,
        children=[UIText(text, styles="text-neutral-700 text-center")]
    )

def dropdown_menu(options, placeholder="Vælg tabelfunktion"):
    global is_dropdown_open
    children = [dropdown_trigger(options, placeholder)]
    if is_dropdown_open:
        for option in options:
            children.append(dropdown_option(option, lambda: print(f"Valgt: {option}")))
    return UIDiv(
        styles="flex flex-col top-12",
        children=children
    )

node_input = game_input("Skriv antallat af noder her")
lag_input = game_input("Skriv antal af lag her")
learning_rate_input = game_input("Skriv læringsrate her")
epoker_input = game_input("Skriv antallat af epoker her")
drop = dropdown_menu([], placeholder="Vælg tabelfunktion")

game.children.extend(
    [
        UIText("Byg din egen AI", styles="text-center font-arial text-5xl"),
        node_input, 
        lag_input,
        learning_rate_input,
        epoker_input,
        game_button("Start spillet", lambda: start_training(
            node_input.text,
            lag_input.text,
            learning_rate_input.text,
            epoker_input.text,
            "some function"
        )),
        ]
        )

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
        else:
            if not training:
                game.handle_event(event)
    if menu:
        menu.update_hover(mouse_position)
        menu.render(surface)
    elif not menu:
        if not training:
            game.update_hover(mouse_position)
            game.render(surface)
        else:
            progress_bar(0.75)

    pygame.display.update()


pygame.quit()