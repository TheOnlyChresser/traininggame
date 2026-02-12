import threading
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

SUPPORTED_LAYER_TYPES = {"Linear", "Flatten", "Dropout"}
SUPPORTED_LOSSES = {"L1Loss", "MSELoss", "HuberLoss", "BCEWithLogitsLoss", "KLDivLoss"}


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
    filled_width = int(bar_width * max(0.0, min(1.0, value)))
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

    dropdown = UIDropdown(styles="flex flex-col w-300 top-12", children=[trigger, menu])
    return dropdown, label


def parse_scalar(value):
    value = value.strip()
    if not value:
        return value
    if value.lower() in ("true", "false"):
        return value.lower() == "true"
    try:
        if "." in value:
            return float(value)
        return int(value)
    except ValueError:
        return value


def parse_layer_params(layer_type, raw_text):
    params = {}
    raw_text = raw_text.strip()
    if raw_text:
        for pair in raw_text.split(","):
            piece = pair.strip()
            if not piece:
                continue
            if "=" not in piece:
                raise ValueError(f"Invalid parameter format: '{piece}'. Use key=value.")
            key, value = piece.split("=", 1)
            params[key.strip()] = parse_scalar(value.strip())

    if layer_type == "Linear":
        if "in" in params:
            params["in_features"] = params.pop("in")
        if "out" in params:
            params["out_features"] = params.pop("out")
    elif layer_type == "Flatten":
        if "start" in params:
            params["start_dim"] = params.pop("start")
        if "end" in params:
            params["end_dim"] = params.pop("end")
    elif layer_type == "Dropout":
        if "rate" in params:
            params["p"] = params.pop("rate")
    else:
        supported = ", ".join(sorted(SUPPORTED_LAYER_TYPES))
        raise ValueError(f"Unsupported layer type: {layer_type}. Supported: {supported}")

    return params


def parse_epochs(raw):
    raw = raw.strip()
    if not raw:
        return 3
    value = int(raw)
    if value <= 0:
        raise ValueError("Epochs must be greater than 0.")
    return value


def parse_learning_rate(raw):
    raw = raw.strip()
    if not raw:
        return 0.001
    value = float(raw)
    if value <= 0:
        raise ValueError("Learning rate must be greater than 0.")
    return value


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

training_lock = threading.Lock()
training_state = {
    "status": "idle",
    "progress": 0.0,
    "epoch": 0,
    "epochs_total": 0,
    "loss": None,
    "accuracy": None,
    "message": "",
    "error": "",
    "thread": None,
}


def build_menu():
    root = UIDiv(styles="flex flex-col justify-center top-180 items-center w-800 h-600 bg-neutral-50")
    root.children.extend(
        [
            UIDiv(
                styles="h-100 w-400 text-3xl font-arial top-0",
                children=[UIText("Velkommen til demoen", styles="text-center font-arial text-5xl")],
            ),
            game_button("Prov demo", lambda: switch_state(STATE_SETUP)),
            game_button("Afslut demo", lambda: exit()),
        ]
    )
    return root


def build_setup():
    root = UIDiv(styles="w-800 h-1200 bg-neutral-50 flex flex-col top-0")
    error_text = UIText("", styles="text-center font-arial text-base text-rose-500")

    layers_input = game_input("Antal lag (f.eks. 3)")
    epochs_input = game_input("Epoker (tom = 3)")
    lr_input = game_input("Laeringsrate (tom = 0.001)")

    loss_options = [name for name in TorcHdata["lossFunktioner"].keys() if name in SUPPORTED_LOSSES]
    act_options = list(TorcHdata["aktFunktioner"].keys())

    def set_loss(value):
        config["loss"] = value

    def set_activation(value):
        config["activation"] = value

    loss_dropdown, _ = make_dropdown(loss_options, "Vaelg lossfunktion", set_loss)
    act_dropdown, _ = make_dropdown(act_options, "Vaelg aktiveringsfunktion", set_activation)

    def go_next():
        try:
            layers_text = layers_input.text.strip()
            if not layers_text.isdigit() or int(layers_text) <= 0:
                raise ValueError("Antal lag skal vaere et heltal over 0.")
            if config["loss"] is None or config["activation"] is None:
                raise ValueError("Vaelg baade loss- og aktiveringsfunktion.")

            parse_epochs(epochs_input.text)
            parse_learning_rate(lr_input.text)
        except Exception as exc:
            error_text.text = str(exc)
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

    return root, [layers_input, epochs_input, lr_input]


def init_layers(count):
    global layer_configs, current_layer_index
    layer_configs = []
    for _ in range(count):
        layer_configs.append({"type": None, "params": ""})
    current_layer_index = 0


def build_layers():
    root = UIDiv(styles="w-800 h-1200 bg-neutral-50 flex flex-col top-0")
    title = UIText("", styles="text-center font-arial text-4xl")
    helper = UIText("Linear: in=784,out=128 | Flatten: start=1,end=-1 | Dropout: p=0.5", styles="text-center font-arial text-sm text-neutral-500")
    error_text = UIText("", styles="text-center font-arial text-base text-rose-500")

    layer_type_options = [name for name in TorcHdata["lagTyper"].keys() if name in SUPPORTED_LAYER_TYPES]

    def set_layer_type(value):
        layer_configs[current_layer_index]["type"] = value

    layer_dropdown, layer_label = make_dropdown(
        layer_type_options,
        "Vaelg lagtype",
        set_layer_type,
    )
    params_input = game_input("Parametre")

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
            helper,
            layer_dropdown,
            params_input,
            game_button("Tilbage", go_back),
            game_button("Naeste", go_next),
            error_text,
        ]
    )

    sync_layer_fields()
    return root, params_input, sync_layer_fields


def build_results():
    root = UIDiv(styles="flex flex-col justify-center top-120 items-center w-800 h-600 bg-neutral-50")
    headline = UIText("Traening starter...", styles="text-center font-arial text-4xl")
    status = UIText("", styles="text-center font-arial text-base text-neutral-600")
    metrics = UIText("", styles="text-center font-arial text-base text-neutral-700")
    error = UIText("", styles="text-center font-arial text-base text-rose-500")

    def back_to_layers():
        switch_state(STATE_LAYERS)

    def back_to_menu():
        switch_state(STATE_MENU)

    root.children.extend(
        [
            headline,
            status,
            metrics,
            error,
        ]
    )

    return root, headline, status, metrics, error


def change_layer(index):
    global current_layer_index
    current_layer_index = index
    layer_sync()


def _update_training(payload):
    with training_lock:
        phase = payload.get("phase")
        if phase == "training":
            training_state["status"] = "running"
            training_state["progress"] = float(payload.get("progress", 0.0))
            training_state["epoch"] = int(payload.get("epoch", 0))
            training_state["epochs_total"] = int(payload.get("epochs_total", 0))
            training_state["loss"] = payload.get("loss")
            training_state["message"] = f"Epoch {training_state['epoch']} / {training_state['epochs_total']}"
        elif phase == "done":
            training_state["status"] = "success"
            training_state["progress"] = 1.0
            training_state["loss"] = payload.get("loss")
            training_state["accuracy"] = payload.get("accuracy")
            training_state["message"] = "Traening faerdig."


def _start_training():
    try:
        from Include.ai import UserAI

        layers = []
        for layer in layer_configs:
            layer_type = layer["type"]
            if layer_type is None:
                raise ValueError("Alle lag skal have en lagtype.")
            layers.append({"type": layer_type, "params": parse_layer_params(layer_type, layer["params"])})

        epochs = parse_epochs(config["epochs"])
        learning_rate = parse_learning_rate(config["learning_rate"])

        ai_runner = UserAI(
            layers=layers,
            activation_name=str(config["activation"]),
            loss_name=str(config["loss"]),
            epochs=epochs,
            learning_rate=learning_rate,
        )

        with training_lock:
            training_state["status"] = "running"
            training_state["progress"] = 0.0
            training_state["epoch"] = 0
            training_state["epochs_total"] = epochs
            training_state["loss"] = None
            training_state["accuracy"] = None
            training_state["message"] = "Starter traening..."
            training_state["error"] = ""

        def worker():
            try:
                ai_runner.run_training(progress_callback=_update_training)
            except Exception as exc:
                with training_lock:
                    training_state["status"] = "error"
                    training_state["error"] = str(exc)
                    training_state["message"] = "Traening fejlede."

        train_thread = threading.Thread(target=worker, daemon=True)
        with training_lock:
            training_state["thread"] = train_thread
        train_thread.start()
    except ModuleNotFoundError as exc:
        missing = str(exc)
        if "torch" in missing:
            message = "PyTorch mangler. Installer 'torch' og 'torchvision' i dit aktive miljoe."
        else:
            message = missing
        with training_lock:
            training_state["status"] = "error"
            training_state["progress"] = 0.0
            training_state["error"] = message
            training_state["message"] = "Traening kan ikke starte."
    except Exception as exc:
        with training_lock:
            training_state["status"] = "error"
            training_state["progress"] = 0.0
            training_state["error"] = str(exc)
            training_state["message"] = "Konfigurationen er ugyldig."


def switch_state(next_state):
    global state
    UIDropdown.active_dropdown = None
    state = next_state
    if state == STATE_RESULTS:
        _start_training()


menu_root = build_menu()
setup_root, setup_inputs = build_setup()
layers_root, layers_params_input, layer_sync = build_layers()
results_root, results_headline, results_status, results_metrics, results_error = build_results()

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
        with training_lock:
            snapshot = dict(training_state)

        if snapshot["status"] == "running":
            results_headline.text = f"Traening... {int(snapshot['progress'] * 100)}%"
            results_status.text = snapshot["message"]
            if snapshot["loss"] is not None:
                results_metrics.text = f"Seneste loss: {snapshot['loss']:.6f}"
            else:
                results_metrics.text = ""
            results_error.text = ""
        elif snapshot["status"] == "success":
            results_headline.text = "Traening faerdig"
            results_status.text = snapshot["message"]
            loss = snapshot["loss"]
            accuracy = snapshot["accuracy"]
            results_metrics.text = f"Loss: {loss:.6f} | Accuracy: {accuracy:.2f}%"
            results_error.text = ""
        elif snapshot["status"] == "error":
            results_headline.text = "Traening fejlede"
            results_status.text = snapshot["message"]
            results_metrics.text = ""
            results_error.text = snapshot["error"]
        else:
            results_headline.text = "Klar"
            results_status.text = ""
            results_metrics.text = ""
            results_error.text = ""

        results_root.compute_box()
        results_root.update_hover(mouse_position)
        results_root.render(surface)
        progress_bar(surface, snapshot["progress"])

    pygame.display.update()


pygame.quit()
