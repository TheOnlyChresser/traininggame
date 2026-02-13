import queue
import threading

import pygame

from Include.ai import UserAI, parse_param_string
from data.ai_terms import (
    NO_ACTIVATION,
    SAFE_LAYER_TYPES,
    get_info_text,
    get_layer_info_key,
    get_layer_param_placeholder,
)
from data.torchDATA import TorcHdata
from ui import (
    UIDiv,
    UIDropdown,
    UIDropdownMenu,
    UIDropdownOption,
    UIDropdownTrigger,
    UIIconButton,
    UIInput,
    UIModal,
    Screen,
    UIText,
)


# Fælles input-stil til opsætnings- og lagformularer.
def game_input(placeholder):
    return UIInput(
        placeholder=placeholder,
        styles="w-320 h-56 bg-neutral-100 rounded-sm items-center flex flex-col justify-center font-arial",
    )


# Primær handlingsknap brugt på tværs af tilstande.
def game_button(text, on_click):
    return UIDiv(
        styles="w-320 h-56 bg-sky-500 rounded-sm hover:bg-sky-400 items-center flex flex-col justify-center",
        on_click=on_click,
        children=[UIText(text, styles="text-neutral-50 text-xl font-arial text-center")],
    )


# Sekundær knapstil til skift og lettere handlinger.
def game_secondary_button(text_widget, on_click):
    return UIDiv(
        styles="w-320 h-46 bg-neutral-200 rounded-sm hover:bg-neutral-300 items-center flex flex-col justify-center",
        on_click=on_click,
        children=[text_widget],
    )


# Tegner træningsfremdrift på resultatskærmen.
def progress_bar(surface, value):
    clamped = max(0.0, min(1.0, value))
    bar_width = 420
    bar_height = 30
    bar_x = 190
    bar_y = 390
    filled_width = int(bar_width * clamped)

    pygame.draw.rect(surface, (220, 220, 220), (bar_x, bar_y, bar_width, bar_height), border_radius=6)
    pygame.draw.rect(surface, (70, 170, 90), (bar_x, bar_y, filled_width, bar_height), border_radius=6)


# Enkel rullemenufabrik som holder label-tekst synkron med valg.
def make_dropdown(options, placeholder, on_select):
    label = UIText(placeholder, styles="text-neutral-700 text-center")
    trigger = UIDropdownTrigger(
        styles="w-320 h-56 bg-neutral-100 rounded-sm items-center flex flex-col justify-center font-arial",
        children=[label],
    )

    option_items = []
    for option in options:
        option_items.append(
            UIDropdownOption(
                value=option,
                styles="w-320 h-40 bg-neutral-200 rounded-sm hover:bg-neutral-300 items-center flex flex-col justify-center font-arial",
                children=[UIText(option, styles="text-neutral-700 text-center")],
                on_select=lambda value, cb=on_select, lbl=label: (cb(value), setattr(lbl, "text", value)),
            )
        )

    menu_height = max(50, 10 + (len(options) * 50))
    menu = UIDropdownMenu(styles=f"flex flex-col w-320 h-{menu_height}", children=option_items)

    dropdown = UIDropdown(styles="flex flex-col", children=[trigger, menu])
    return dropdown, label


# Hjælperække til label + info-knap-par.
def make_info_row(label_text, info_key_or_getter):
    def show_info():
        key = info_key_or_getter() if callable(info_key_or_getter) else info_key_or_getter
        open_info(key)

    return UIDiv(
        styles="w-320 h-34 flex justify-center items-center",
        children=[
            UIText(label_text, styles="w-250 h-28 text-neutral-700 text-base font-arial text-center"),
            UIIconButton(on_click=show_info),
        ],
    )


# Ensartet talformatering til metrik-tekst.
def format_number(value, digits=4):
    if value is None:
        return "-"
    return f"{value:.{digits}f}"


screen = Screen(800, 760)
surface = screen.surface
pygame.display.set_caption("AI spil")

STATE_MENU = "menu"
STATE_SETUP = "setup"
STATE_LAYERS = "layers"
STATE_RESULTS = "results"
state = STATE_MENU

# Global konfiguration delt mellem opsætning, lagredigering og træningsstart.
config = {
    "layers_count": 0,
    "epochs": 3,
    "learning_rate": 0.001,
    "loss": "CrossEntropyLoss",
    "advanced_mode": False,
}

layer_configs = []
current_layer_index = 0

info_modal = UIModal()

menu_root = None
setup_root = None
setup_inputs = []
setup_error_text = None
layers_root = None
layers_params_input = None
layer_sync = lambda: None
results_root = None
results_widgets = {}

# Tråd + kø-opsætning til ikke-blokerende træning i pygame-løkken.
training_queue = queue.Queue()
training_thread = None
training_cancel_event = None
training_progress = 0.0
training_result = None


# Åbner infomodal for en given ordliste-nøgle.
def open_info(info_key):
    title, body = get_info_text(info_key)
    info_modal.open(title, body)


# Vælger bedste ordliste-nøgle for det lag, der redigeres nu.
def current_layer_info_key():
    if not layer_configs:
        return "lagtype"
    layer_type = layer_configs[current_layer_index].get("type")
    return get_layer_info_key(layer_type)


# Sammensætning af hovedmenuen.
def build_menu():
    root = UIDiv(styles="flex flex-col justify-center top-160 items-center w-800 h-600 bg-neutral-50")
    root.children.extend(
        [
            UIDiv(
                styles="h-90 w-500 text-3xl font-arial",
                children=[UIText("Velkommen til AI-demo", styles="text-center font-arial text-5xl")],
            ),
            game_button("Byg din egen AI", lambda: switch_state(STATE_SETUP)),
            game_button("Afslut demo", lambda: pygame.event.post(pygame.event.Event(pygame.QUIT))),
        ]
    )
    return root


# Opsætningsskærm: globale træningsindstillinger og sikker/avanceret tilstand.
def build_setup():
    root = UIDiv(styles="w-800 h-1200 bg-neutral-50 flex flex-col items-center top-10")
    error_text = UIText("", styles="text-center font-arial text-base text-rose-500")

    layers_input = game_input("Antal lag (f.eks. 3)")
    epochs_input = game_input("Epoker (tom = 3)")
    lr_input = game_input("Laeringsrate (tom = 0.001)")

    # Forudfyld felter med tidligere valg, så brugeren kan justere uden at starte forfra.
    if config["layers_count"] > 0:
        layers_input.text = str(config["layers_count"])
    if config["epochs"] > 0:
        epochs_input.text = str(config["epochs"])
    if config["learning_rate"] > 0:
        lr_input.text = str(config["learning_rate"])

    loss_options = list(TorcHdata["lossFunktioner"].keys())

    def set_loss(value):
        config["loss"] = value

    loss_dropdown, loss_label = make_dropdown(loss_options, "Vaelg lossfunktion", set_loss)
    if config["loss"] in loss_options:
        loss_label.text = config["loss"]

    advanced_text = UIText(
        "Avanceret tilstand: Til" if config["advanced_mode"] else "Avanceret tilstand: Fra",
        styles="text-neutral-700 text-base font-arial text-center",
    )

    def toggle_advanced():
        config["advanced_mode"] = not config["advanced_mode"]
        advanced_text.text = "Avanceret tilstand: Til" if config["advanced_mode"] else "Avanceret tilstand: Fra"

    def go_next():
        # Tidlig validering så efterfølgende lag/træning altid har gyldig tilstand.
        layers_text = layers_input.text.strip()
        epochs_text = epochs_input.text.strip()
        lr_text = lr_input.text.strip()

        try:
            layers_count = int(layers_text)
            if layers_count <= 0:
                raise ValueError
        except ValueError:
            error_text.text = "Antal lag skal vaere et heltal over 0."
            return

        try:
            epochs = int(epochs_text)
            if epochs <= 0:
                raise ValueError
        except ValueError:
            error_text.text = "Epoker skal vaere et heltal over 0."
            return

        try:
            learning_rate = float(lr_text)
            if learning_rate <= 0:
                raise ValueError
        except ValueError:
            error_text.text = "Laeringsrate skal vaere et tal over 0."
            return

        if config.get("loss") is None:
            error_text.text = "Vaelg en lossfunktion."
            return

        config["layers_count"] = layers_count
        config["epochs"] = epochs
        config["learning_rate"] = learning_rate

        init_layers(layers_count)
        rebuild_layers()
        switch_state(STATE_LAYERS)

    root.children.extend(
        [
            UIText("Byg din egen AI", styles="text-center font-arial text-5xl"),
            make_info_row("Antal lag", "antal_lag"),
            layers_input,
            make_info_row("Epoker", "epoker"),
            epochs_input,
            make_info_row("Laeringsrate", "laeringsrate"),
            lr_input,
            make_info_row("Lossfunktion", "lossfunktion"),
            loss_dropdown,
            make_info_row("Avanceret tilstand", "avanceret_tilstand"),
            game_secondary_button(advanced_text, toggle_advanced),
            game_button("Naeste", go_next),
            error_text,
        ]
    )

    return root, [layers_input, epochs_input, lr_input], error_text


# Initialiserer kladdetilstand pr. lag før lagredigering åbnes.
def init_layers(count):
    global layer_configs, current_layer_index
    layer_configs = []
    for _ in range(count):
        layer_configs.append({"type": None, "params": "", "activation": NO_ACTIVATION})
    current_layer_index = 0


# Lagredigeringsskærm for type/parametre/aktivering pr. trin.
def build_layers():
    root = UIDiv(styles="w-800 h-1400 bg-neutral-50 flex flex-col items-center top-10")
    title = UIText("", styles="w-330 h-34 text-neutral-800 text-xl font-arial text-center")
    error_text = UIText("", styles="text-center font-arial text-base text-rose-500")
    hint_text = UIText("", styles="w-700 h-48 text-center font-arial text-sm text-neutral-500")

    # Avanceret tilstand viser hele lagerkataloget; ellers kun sikre startlag.
    if config.get("advanced_mode"):
        layer_type_options = list(TorcHdata["lagTyper"].keys())
    else:
        layer_type_options = [name for name in SAFE_LAYER_TYPES if name in TorcHdata["lagTyper"]]

    def set_layer_type(value):
        layer_configs[current_layer_index]["type"] = value
        placeholder = get_layer_param_placeholder(value)
        params_input.placeholder = placeholder
        hint_text.text = f"Hint: {placeholder}" if placeholder else "Hint: Ingen ekstra parametre noedvendige."

    layer_dropdown, layer_label = make_dropdown(layer_type_options, "Vaelg lagtype", set_layer_type)

    activation_options = [NO_ACTIVATION] + list(TorcHdata["aktFunktioner"].keys())

    def set_activation(value):
        layer_configs[current_layer_index]["activation"] = value

    activation_dropdown, activation_label = make_dropdown(
        activation_options,
        "Vaelg aktivering (valgfri)",
        set_activation,
    )

    params_input = game_input("key=value")

    def sync_layer_fields():
        # Holder synlige felter synkroniseret med det aktive lagindeks.
        if not layer_configs:
            title.text = "Lag"
            layer_label.text = "Vaelg lagtype"
            activation_label.text = "Vaelg aktivering (valgfri)"
            params_input.text = ""
            params_input.placeholder = "key=value"
            hint_text.text = ""
            error_text.text = ""
            return

        current = layer_configs[current_layer_index]
        title.text = f"Lag {current_layer_index + 1} af {len(layer_configs)}"

        selected_type = current.get("type")
        selected_activation = current.get("activation") or NO_ACTIVATION
        layer_label.text = selected_type or "Vaelg lagtype"
        activation_label.text = selected_activation
        params_input.text = current.get("params", "")

        placeholder = get_layer_param_placeholder(selected_type)
        params_input.placeholder = placeholder
        hint_text.text = f"Hint: {placeholder}" if placeholder else "Hint: Ingen ekstra parametre noedvendige."
        error_text.text = ""

    def save_current_layer():
        # Gem fritekst-parametre før enhver navigation.
        layer_configs[current_layer_index]["params"] = params_input.text.strip()

    def go_back():
        save_current_layer()
        if current_layer_index == 0:
            switch_state(STATE_SETUP)
            return
        change_layer(current_layer_index - 1)

    def go_next():
        save_current_layer()

        current = layer_configs[current_layer_index]
        if current.get("type") is None:
            error_text.text = "Vaelg en lagtype for dette lag."
            return

        try:
            parse_param_string(current.get("params", ""))
        except ValueError as error:
            error_text.text = str(error)
            return

        if current_layer_index + 1 >= len(layer_configs):
            switch_state(STATE_RESULTS)
            start_training()
            return

        change_layer(current_layer_index + 1)

    root.children.extend(
        [
            UIText("Lag-konfiguration", styles="text-center font-arial text-4xl"),
            UIDiv(
                styles="w-420 h-36 flex justify-center items-center",
                children=[title, UIIconButton(on_click=lambda: open_info(current_layer_info_key()))],
            ),
            make_info_row("Lagtype", "lagtype"),
            layer_dropdown,
            make_info_row("Parametre", "parametre"),
            params_input,
            hint_text,
            make_info_row("Per-lag aktivering", "per_lag_aktivering"),
            activation_dropdown,
            game_button("Tilbage", go_back),
            game_button("Naeste", go_next),
            error_text,
        ]
    )

    sync_layer_fields()
    return root, params_input, layer_label, activation_label, sync_layer_fields


# Resultatskærm: løbende fremdrift + endelige metrikker og resumé.
def build_results():
    root = UIDiv(styles="flex flex-col justify-center top-70 items-center w-800 h-780 bg-neutral-50")

    headline = UIText("Traening starter...", styles="text-center font-arial text-4xl")
    phase_text = UIText("", styles="text-center font-arial text-base text-neutral-600")

    loss_value = UIText("Loss: -", styles="w-300 h-30 text-neutral-700 text-base font-arial")
    accuracy_value = UIText("Accuracy: -", styles="w-300 h-30 text-neutral-700 text-base font-arial")
    summary_title = UIText("Modeloversigt", styles="text-center font-arial text-lg text-neutral-700")

    summary_lines = [
        UIText("", styles="w-720 h-24 text-neutral-600 text-sm font-arial") for _ in range(6)
    ]

    def back_to_layers():
        cancel_training_if_running()
        switch_state(STATE_LAYERS)

    def back_to_menu():
        cancel_training_if_running()
        switch_state(STATE_MENU)

    root.children.extend(
        [
            headline,
            phase_text,
            UIDiv(
                styles="w-360 h-34 flex justify-center items-center",
                children=[loss_value, UIIconButton(on_click=lambda: open_info("resultat_loss"))],
            ),
            UIDiv(
                styles="w-360 h-34 flex justify-center items-center",
                children=[accuracy_value, UIIconButton(on_click=lambda: open_info("resultat_accuracy"))],
            ),
            summary_title,
            *summary_lines,
            game_button("Tilbage til lag", back_to_layers),
            game_button("Tilbage til menu", back_to_menu),
        ]
    )

    widgets = {
        "headline": headline,
        "phase": phase_text,
        "loss": loss_value,
        "accuracy": accuracy_value,
        "summary_lines": summary_lines,
    }
    return root, widgets


def change_layer(index):
    global current_layer_index
    current_layer_index = index
    layer_sync()


# Genopbygningsfunktioner bruges ved tilstandsskift, så felter afspejler aktuel konfiguration.
def rebuild_setup():
    global setup_root, setup_inputs, setup_error_text
    setup_root, setup_inputs, setup_error_text = build_setup()


def rebuild_layers():
    global layers_root, layers_params_input, layer_sync
    layers_root, layers_params_input, _, _, layer_sync = build_layers()


def rebuild_results():
    global results_root, results_widgets
    results_root, results_widgets = build_results()


# Tøm ventende fremdrifts-/resultathændelser ved start af nyt run.
def clear_training_queue():
    while True:
        try:
            training_queue.get_nowait()
        except queue.Empty:
            break


# Viser modelresumé i et fast antal tekstlinjer.
def apply_summary_lines(summary_text):
    lines = [line for line in summary_text.split("\n") if line.strip()]
    line_widgets = results_widgets.get("summary_lines", [])

    for index, widget in enumerate(line_widgets):
        widget.text = lines[index] if index < len(lines) else ""


# Starter træningsarbejder og nulstiller resultatfelter til indlæsningsstatus.
def start_training():
    global training_thread, training_cancel_event, training_progress, training_result

    cancel_training_if_running()
    clear_training_queue()

    training_progress = 0.0
    training_result = None

    results_widgets["headline"].text = "Traening starter..."
    results_widgets["phase"].text = "Forbereder model..."
    results_widgets["loss"].text = "Loss: -"
    results_widgets["accuracy"].text = "Accuracy: -"
    apply_summary_lines("")

    training_cancel_event = threading.Event()

    # Kopiér lagkonfigurationen, så redigering i grænsefladen ikke ændrer aktiv træning.
    train_config = {
        "epochs": config["epochs"],
        "learning_rate": config["learning_rate"],
        "loss": config["loss"],
        "layers": [dict(layer) for layer in layer_configs],
    }

    def progress_callback(payload):
        training_queue.put({"type": "progress", "payload": payload})

    def worker():
        # Kør træning i baggrunden og aflever resultatet tilbage til hovedløkken via køen.
        ai_runner = UserAI()
        result = ai_runner.train(
            train_config,
            progress_callback=progress_callback,
            cancel_event=training_cancel_event,
        )
        training_queue.put({"type": "result", "payload": result})

    training_thread = threading.Thread(target=worker, daemon=True)
    training_thread.start()


# Kooperativ annullering for kørende trænings-tråde.
def cancel_training_if_running():
    global training_thread, training_cancel_event

    if training_thread and training_thread.is_alive():
        if training_cancel_event is not None:
            training_cancel_event.set()
        training_thread.join(timeout=1.5)

    training_thread = None
    training_cancel_event = None


# Henter fremdrifts-/resultatbeskeder fra køen og opdaterer visningstekster.
def poll_training_updates():
    global training_progress, training_result, training_thread, training_cancel_event

    while True:
        try:
            message = training_queue.get_nowait()
        except queue.Empty:
            break

        payload = message.get("payload", {})

        # To beskedtyper: løbende fremdrift og endeligt resultat.
        if message.get("type") == "progress":
            training_progress = payload.get("progress", training_progress)
            epoch = payload.get("epoch", 0)
            epochs = payload.get("epochs", 0)
            batch = payload.get("batch", 0)
            batches = payload.get("batches", 0)
            loss_value = payload.get("loss")

            results_widgets["headline"].text = f"Traening... {int(training_progress * 100)}%"
            results_widgets["phase"].text = f"Epoke {epoch}/{epochs}, batch {batch}/{batches}"
            results_widgets["loss"].text = f"Loss: {format_number(loss_value)}"

        if message.get("type") == "result":
            training_result = payload
            status = payload.get("status")

            if status == "completed":
                training_progress = 1.0
                results_widgets["headline"].text = "Traening faerdig"
                results_widgets["phase"].text = "Model og evaluering gennemfoert."
                results_widgets["loss"].text = f"Loss: {format_number(payload.get('final_loss'))}"
                results_widgets["accuracy"].text = f"Accuracy: {format_number(payload.get('accuracy'), 2)}%"
                apply_summary_lines(payload.get("model_summary", ""))

            elif status == "cancelled":
                results_widgets["headline"].text = "Traening stoppet"
                results_widgets["phase"].text = "Traeningen blev afbrudt af brugeren."
                results_widgets["loss"].text = f"Loss: {format_number(payload.get('final_loss'))}"
                results_widgets["accuracy"].text = "Accuracy: -"
                apply_summary_lines(payload.get("model_summary", ""))

            else:
                results_widgets["headline"].text = "Traening fejlede"
                results_widgets["phase"].text = payload.get("error") or "Ukendt fejl under traening."
                results_widgets["loss"].text = "Loss: -"
                results_widgets["accuracy"].text = "Accuracy: -"
                apply_summary_lines("")

            training_thread = None
            training_cancel_event = None


# Centraliseret tilstandsovergang med oprydnings-/genopbygningsregler.
def switch_state(next_state):
    global state

    if state == STATE_RESULTS and next_state != STATE_RESULTS:
        cancel_training_if_running()

    state = next_state

    if state == STATE_SETUP:
        rebuild_setup()
    elif state == STATE_LAYERS:
        rebuild_layers()
    elif state == STATE_RESULTS:
        rebuild_results()


# Returnerer rodtræet for grænsefladen i nuværende tilstand.
def active_root():
    if state == STATE_MENU:
        return menu_root
    if state == STATE_SETUP:
        return setup_root
    if state == STATE_LAYERS:
        return layers_root
    return results_root


menu_root = build_menu()
rebuild_setup()
rebuild_layers()
rebuild_results()

clock = pygame.time.Clock()
running = True

while running:
    dt = clock.tick(60)
    mouse_position = pygame.mouse.get_pos()
    surface.fill((250, 250, 250))

    poll_training_updates()

    root = active_root()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            cancel_training_if_running()
            running = False
            break

        if info_modal.is_open() and info_modal.handle_event(event):
            # Modalen ejer input, mens den er synlig.
            continue

        if root:
            root.handle_event(event)

    if not running:
        continue

    if state == STATE_SETUP:
        for input_box in setup_inputs:
            input_box.update(dt)

    if state == STATE_LAYERS and layers_params_input is not None:
        layers_params_input.update(dt)

    if root:
        root.compute_box()
        if not info_modal.is_open():
            root.update_hover(mouse_position)
        root.render(surface)

    if state == STATE_RESULTS:
        progress_bar(surface, training_progress)

    if info_modal.is_open():
        info_modal.render(surface)

    pygame.display.update()

pygame.quit()




