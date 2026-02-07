import pygame
from ui import (
    UIDiv,
    UIText,
    Screen,
    UIInput,
    UIDropdown,
    UIDropdownTrigger,
    UIDropdownMenu,
    UIDropdownOption,
)
from data.torchDATA import TorcHdata


def game_input(placeholder):
    return UIInput(
        placeholder=placeholder,
        styles="w-300 h-60 bg-neutral-100 rounded-sm items-center flex flex-col justify-center font-arial",
    )


def game_button(text, on_click):
    return UIDiv(
        styles="w-300 h-60 bg-sky-500 rounded-sm hover:bg-sky-400 top-12 items-center flex flex-col justify-center",
        on_click=on_click,
        children=[UIText(text, styles="text-neutral-50 text-xl font-arial text-center")],
    )


def progress_bar(surface, value):
    bar_width = 400
    bar_height = 30
    filled_width = int(bar_width * value)

    pygame.draw.rect(surface, (200, 200, 200), (200, 300, bar_width, bar_height))
    pygame.draw.rect(surface, (100, 200, 100), (200, 300, filled_width, bar_height))


def make_dropdown(options, placeholder, on_select):
    label = UIText(placeholder, styles="text-neutral-700 text-center")
    trigger = UIDropdownTrigger(
        styles="w-300 h-60 bg-neutral-100 rounded-sm top-12 items-center flex flex-col justify-center font-arial",
        children=[label],
    )

    option_items = []
    for option in options:
        option_items.append(
            UIDropdownOption(
                value=option,
                styles="w-300 h-40 bg-neutral-200 rounded-sm hover:bg-neutral-300 top-0 items-center flex flex-col justify-center font-arial",
                children=[UIText(option, styles="text-neutral-700 text-center")],
                on_select=lambda value, cb=on_select, lbl=label: (cb(value), setattr(lbl, "text", value)),
            )
        )

    menu_height = max(50, 10 + (len(options) * 50))
    menu = UIDropdownMenu(
        styles=f"flex flex-col w-300 h-{menu_height} top-0",
        children=option_items,
    )

    dropdown = UIDropdown(styles="flex flex-col top-12", children=[trigger, menu])
    return dropdown, label


screen = Screen(800, 600)
surface = screen.surface
pygame.display.set_caption("AI spil")

STATE_MENU = "menu"
STATE_SETUP = "setup"
STATE_LAYERS = "layers"
STATE_RESULTS = "results"
state = STATE_MENU

config = {
    "layers_count": 0,
    "epochs": "",
    "learning_rate": "",
    "loss": None,
    "activation": None,
}

layer_configs = []
current_layer_index = 0
result_start_ms = 0


def build_menu():
    root = UIDiv(styles="flex flex-col justify-center top-180 items-center w-800 h-600 bg-neutral-50")
    root.children.extend(
        [
            UIDiv(
                styles="h-100 w-400 text-3xl font-arial top-0",
                children=[UIText("Velkommen til demoen", styles="text-center font-arial text-5xl")],
            ),
            game_button("Prøv demo", lambda: switch_state(STATE_SETUP)),
            game_button("Afslut demo", lambda: exit()),
        ]
    )
    return root


def build_setup():
    root = UIDiv(styles="w-800 h-1200 bg-neutral-50 flex flex-col top-0")
    error_text = UIText("", styles="text-center font-arial text-base text-rose-500")

    layers_input = game_input("Antal lag (f.eks. 3)")
    epochs_input = game_input("Epoker (f.eks. 3)")
    lr_input = game_input("Laeringsrate (f.eks. 0.001)")

    loss_options = list(TorcHdata["lossFunktioner"].keys())
    act_options = list(TorcHdata["aktFunktioner"].keys())

    def set_loss(value):
        config["loss"] = value

    def set_activation(value):
        config["activation"] = value

    loss_dropdown, loss_label = make_dropdown(loss_options, "Vaelg lossfunktion", set_loss)
    act_dropdown, act_label = make_dropdown(act_options, "Vaelg aktiveringsfunktion", set_activation)

    def go_next():
        layers_text = layers_input.text.strip()
        if not layers_text.isdigit() or int(layers_text) <= 0:
            error_text.text = "Antal lag skal vaere et heltal over 0."
            return
        if config["loss"] is None or config["activation"] is None:
            error_text.text = "Vaelg baade loss- og aktiveringsfunktion."
            return

        config["layers_count"] = int(layers_text)
        config["epochs"] = epochs_input.text.strip()
        config["learning_rate"] = lr_input.text.strip()

        init_layers(config["layers_count"])
        layer_sync()
        switch_state(STATE_LAYERS)

    root.children.extend(
        [
            UIText("Byg din egen AI", styles="text-center font-arial text-5xl"),
            layers_input,
            epochs_input,
            lr_input,
            loss_dropdown,
            act_dropdown,
            game_button("Naeste", go_next),
            error_text,
        ]
    )

    return root, [layers_input, epochs_input, lr_input], loss_label, act_label, error_text


def init_layers(count):
    global layer_configs, current_layer_index
    layer_configs = []
    for _ in range(count):
        layer_configs.append({"type": None, "params": ""})
    current_layer_index = 0


def build_layers():
    root = UIDiv(styles="w-800 h-1200 bg-neutral-50 flex flex-col top-0")
    title = UIText("", styles="text-center font-arial text-4xl")
    error_text = UIText("", styles="text-center font-arial text-base text-rose-500")

    layer_type_options = list(TorcHdata["lagTyper"].keys())

    def set_layer_type(value):
        layer_configs[current_layer_index]["type"] = value

    layer_dropdown, layer_label = make_dropdown(
        layer_type_options,
        "Vaelg lagtype",
        set_layer_type,
    )
    params_input = game_input("Parametre (f.eks. in=784,out=128)")

    def sync_layer_fields():
        if not layer_configs:
            title.text = "Lag"
            params_input.text = ""
            layer_label.text = "Vaelg lagtype"
            error_text.text = ""
            return
        title.text = f"Lag {current_layer_index + 1} af {len(layer_configs)}"
        current = layer_configs[current_layer_index]
        params_input.text = current["params"]
        layer_label.text = current["type"] or "Vaelg lagtype"
        error_text.text = ""

    def go_back():
        layer_configs[current_layer_index]["params"] = params_input.text.strip()
        if current_layer_index == 0:
            switch_state(STATE_SETUP)
            return
        change_layer(current_layer_index - 1)

    def go_next():
        layer_configs[current_layer_index]["params"] = params_input.text.strip()
        if layer_configs[current_layer_index]["type"] is None:
            error_text.text = "Vaelg en lagtype for dette lag."
            return
        if current_layer_index + 1 >= len(layer_configs):
            switch_state(STATE_RESULTS)
            return
        change_layer(current_layer_index + 1)

    root.children.extend(
        [
            title,
            layer_dropdown,
            params_input,
            game_button("Tilbage", go_back),
            game_button("Naeste", go_next),
            error_text,
        ]
    )

    sync_layer_fields()
    return root, params_input, layer_label, sync_layer_fields


def build_results():
    root = UIDiv(styles="flex flex-col justify-center top-120 items-center w-800 h-600 bg-neutral-50")
    headline = UIText("Traning korer...", styles="text-center font-arial text-4xl")
    hint = UIText("Mock resultat baseret pa setup", styles="text-center font-arial text-base text-neutral-500")

    def back_to_layers():
        switch_state(STATE_LAYERS)

    def back_to_menu():
        switch_state(STATE_MENU)

    root.children.extend(
        [
            headline,
            hint,
            game_button("Tilbage til lag", back_to_layers),
            game_button("Tilbage til menu", back_to_menu),
        ]
    )

    return root, headline


def change_layer(index):
    global current_layer_index
    current_layer_index = index
    layer_sync()


def switch_state(next_state):
    global state, result_start_ms
    state = next_state
    if state == STATE_RESULTS:
        result_start_ms = pygame.time.get_ticks()


menu_root = build_menu()
setup_root, setup_inputs, _, _, _ = build_setup()
layers_root, layers_params_input, _, layer_sync = build_layers()
results_root, results_headline = build_results()

clock = pygame.time.Clock()
running = True
while running:
    dt = clock.tick(60)
    mouse_position = pygame.mouse.get_pos()
    surface.fill((250, 250, 250))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if state == STATE_MENU:
            menu_root.handle_event(event)
        elif state == STATE_SETUP:
            setup_root.handle_event(event)
        elif state == STATE_LAYERS:
            layers_root.handle_event(event)
        elif state == STATE_RESULTS:
            results_root.handle_event(event)

    if state == STATE_SETUP:
        for input_box in setup_inputs:
            input_box.update(dt)
    if state == STATE_LAYERS:
        layers_params_input.update(dt)

    if state == STATE_MENU:
        menu_root.compute_box()
        menu_root.update_hover(mouse_position)
        menu_root.render(surface)
    elif state == STATE_SETUP:
        setup_root.compute_box()
        setup_root.update_hover(mouse_position)
        setup_root.render(surface)
    elif state == STATE_LAYERS:
        layers_root.compute_box()
        layers_root.update_hover(mouse_position)
        layers_root.render(surface)
    elif state == STATE_RESULTS:
        results_root.compute_box()
        results_root.update_hover(mouse_position)
        results_root.render(surface)

        elapsed = max(0, pygame.time.get_ticks() - result_start_ms)
        progress = min(1.0, elapsed / 5000.0)
        progress_bar(surface, progress)
        results_headline.text = f"Traning... {int(progress * 100)}%"

    pygame.display.update()


pygame.quit()