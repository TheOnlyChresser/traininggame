import pygame

colors = {
    "red": {
        "50": "#fef2f2",
        "100": "#ffe2e2",
        "200": "#ffc9c9",
        "300": "#ffa2a2",
        "400": "#ff6467",
        "500": "#fb2c36",
        "600": "#e7000b",
        "700": "",
        "800": "",
        "900": "",
        "950": "",
    },
    "orange": {
        "50": "",
        "100": "",
        "200": "",
        "300": "",
        "400": "",
        "500": "",
        "600": "",
        "700": "",
        "800": "",
        "900": "",
        "950": "",
    },
    "amber": {
        "50": "",
        "100": "",
        "200": "",
        "300": "",
        "400": "",
        "500": "",
        "600": "",
        "700": "",
        "800": "",
        "900": "",
        "950": "",
    },
    "yellow": {
        "50": "",
        "100": "",
        "200": "",
        "300": "",
        "400": "",
        "500": "",
        "600": "",
        "700": "",
        "800": "",
        "900": "",
        "950": "",
    },
    "lime": {
        "50": "",
        "100": "",
        "200": "",
        "300": "",
        "400": "",
        "500": "",
        "600": "",
        "700": "",
        "800": "",
        "900": "",
        "950": "",
    },
    "green": {
        "50": "#f0fdf4",
        "100": "#dcfce7",
        "200": "#b9f8cf",
        "300": "#7bf1a8",
        "400": "#05df72",
        "500": "#00c951",
        "600": "#00a63e",
        "700": "",
        "800": "",
        "900": "",
        "950": "",
    },
    "emerald": {
        "50": "#ecfdf5",
        "100": "#d0fae5",
        "200": "#a4f4cf",
        "300": "#5ee9b5",
        "400": "#00d492",
        "500": "#00bc7d",
        "600": "#009966",
        "700": "",
        "800": "",
        "900": "",
        "950": "",
    },
    "teal": {
        "50": "",
        "100": "",
        "200": "",
        "300": "",
        "400": "",
        "500": "",
        "600": "",
        "700": "",
        "800": "",
        "900": "",
        "950": "",
    },
    "cyan": {
        "50": "",
        "100": "",
        "200": "",
        "300": "",
        "400": "",
        "500": "",
        "600": "",
        "700": "",
        "800": "",
        "900": "",
        "950": "",
    },
    "sky": {
        "50": "#f0f9ff",
        "100": "#dff2fe",
        "200": "#b8e6fe",
        "300": "#74d4ff",
        "400": "#00bcff",
        "500": "#00a6f4",
        "600": "#0084d1",
        "700": "",
        "800": "",
        "900": "",
        "950": "",
    },
    "blue": {
        "50": "",
        "100": "",
        "200": "",
        "300": "",
        "400": "",
        "500": "",
        "600": "",
        "700": "",
        "800": "",
        "900": "",
        "950": "",
    },
    "indigo": {
        "50": "",
        "100": "",
        "200": "",
        "300": "",
        "400": "",
        "500": "",
        "600": "",
        "700": "",
        "800": "",
        "900": "",
        "950": "",
    },
    "violet": {
        "50": "",
        "100": "",
        "200": "",
        "300": "",
        "400": "",
        "500": "",
        "600": "",
        "700": "",
        "800": "",
        "900": "",
        "950": "",
    },
    "purple": {
        "50": "",
        "100": "",
        "200": "",
        "300": "",
        "400": "",
        "500": "",
        "600": "",
        "700": "",
        "800": "",
        "900": "",
        "950": "",
    },
    "fuchsia": {
        "50": "",
        "100": "",
        "200": "",
        "300": "",
        "400": "",
        "500": "",
        "600": "",
        "700": "",
        "800": "",
        "900": "",
        "950": "",
    },
    "pink": {
        "50": "",
        "100": "",
        "200": "",
        "300": "",
        "400": "",
        "500": "",
        "600": "",
        "700": "",
        "800": "",
        "900": "",
        "950": "",
    },
    "rose": {
        "50": "#fff1f2",
        "100": "#ffe4e6",
        "200": "#ffccd3",
        "300": "#ffa1ad",
        "400": "#ff637e",
        "500": "#ff2056",
        "600": "#ec003f",
        "700": "",
        "800": "",
        "900": "",
        "950": "",
    },
    "slate": {
        "50": "",
        "100": "",
        "200": "",
        "300": "",
        "400": "",
        "500": "",
        "600": "",
        "700": "",
        "800": "",
        "900": "",
        "950": "",
    },
    "gray": {
        "50": "",
        "100": "",
        "200": "",
        "300": "",
        "400": "",
        "500": "",
        "600": "",
        "700": "",
        "800": "",
        "900": "",
        "950": "",
    },
    "zinc": {
        "50": "",
        "100": "",
        "200": "",
        "300": "",
        "400": "",
        "500": "",
        "600": "",
        "700": "",
        "800": "",
        "900": "",
        "950": "",
    },
    "neutral": {
        "50": "#fafafa",
        "100": "#f5f5f5",
        "200": "#e5e5e5",
        "300": "#d4d4d4",
        "400": "#a1a1a1",
        "500": "#737373",
        "600": "#525252",
        "700": "#404040",
        "800": "#262626",
        "900": "#171717",
        "950": "#0a0a0a",
    },
    "stone": {
        "50": "",
        "100": "",
        "200": "",
        "300": "",
        "400": "",
        "500": "",
        "600": "",
        "700": "",
        "800": "",
        "900": "",
        "950": "",
    }
}
sizes = {
    "xs": "12",
    "sm": "14",
    "md": "16",
    "lg": "18",
    "xl": "20",
    "2xl": "24",
    "3xl": "30",
    "4xl": "36",
    "5xl": "48",
    "6xl": "60",
}

weights = {
    "thin": "100",
    "extralight": "200",
    "light": "300",
    "normal": "400",
    "medium": "500",
    "semibold": "600",
    "bold": "700",
    "extrabold": "800",
    "black": "900",
}
#chatgpt kode
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def parse_classes(class_string):
    styles = {
        "display": "flex",
        "position": "relative",
        "justify": "start",
        "items": "start",
        "width": None,
        "height": None,
        "top": None,
        "left": None,
        "right": None,
        "bottom": None,
        "background": None,
        "color": None,
        "font_size": None,
        "font_family": None,
    }
    hover_styles = {}

    for parsed_class in class_string.split():
        is_hover = parsed_class.startswith("hover:")
        class_to_parse = parsed_class[6:] if is_hover else parsed_class
        parts = class_to_parse.split("-")

        def set_style(dict, key, value):
            dict[key] = value

        target = hover_styles if is_hover else styles

        if class_to_parse == "flex":
            set_style(target, "display", "flex")
        elif class_to_parse == "block":
            set_style(target, "display", "block")
        elif class_to_parse == "fixed":
            set_style(target, "position", "fixed")

        elif parts[0] == "justify":
            set_style(target, "justify", parts[1])
        elif parts[0] == "items":
            set_style(target, "items", parts[1])

        elif parts[0] == "w":
            set_style(target, "width", int(parts[1]))
        elif parts[0] == "h":
            set_style(target, "height", int(parts[1]))

        elif parts[0] in ("top", "left", "right", "bottom"):
            set_style(target, parts[0], int(parts[1]))

        elif parts[0] == "bg":
            if parts[1] in colors and parts[2] in colors[parts[1]] and colors[parts[1]][parts[2]]:
                set_style(target, "background", hex_to_rgb(colors[parts[1]][parts[2]]))

        elif parts[0] == "text":
            if parts[1] in colors and parts[2] in colors[parts[1]] and colors[parts[1]][parts[2]]:
                set_style(target, "color", hex_to_rgb(colors[parts[1]][parts[2]]))
            elif parts[1] in sizes:
                set_style(target, "font_size", int(sizes[parts[1]]))
        elif parts[0] == "font":
            set_style(target, "font_family", parts[1].capitalize())

    return styles, hover_styles

class Screen:
    def __init__(self, width, height, surface):
        self.width = width
        self.height = height
        self.surface = surface
        pygame.init()
        self.surface = pygame.display.set_mode((self.width, self.height))

class UIBase:
    def __init__(self, box, styles, parent, inherit):
        self.box = box
        self.styles = styles
        self.parent = parent
        self.inherit = inherit
        self.computed, self.hover_styles = parse_classes(styles)
        self.is_hovered = False
        self.children = []
        if parent and hasattr(parent, "children"):
            parent.children.append(self)

    def update_hover(self, mouse_position):
        x, y, w, h = self.box
        self.is_hovered = (x <= mouse_position[0] <= x + w and y <= mouse_position[1] <= y + h)
        if self.is_hovered and self.hover_styles:
            self.computed.update(self.hover_styles)
        elif not self.is_hovered:
            self.computed = parse_classes(self.styles)[0]

    def add_child(self, child):
        self.children.append(child)

    def get_computed_style(self, key, default=None):
        return self.computed.get(key, default)



class UIText(UIBase):
    def __init__(self, box, styles, parent, inherit, text, font=None):
        super().__init__(box, styles, parent, inherit)
        self.text = text
        self.font = font or self.get_computed_style("font_family", "Arial")

    def handle_hover(self, mouse_position):
        self.update_hover(mouse_position)

    def render(self):
        font_size = self.get_computed_style("font_size", 16)
        color = self.get_computed_style("color", (255, 255, 255))
        # fikser fejl hvis ikke rgb
        if not (isinstance(color, tuple) and len(color) == 3 and all(isinstance(c, int) and 0 <= c <= 255 for c in color)):
            color = (255, 255, 255)
        font = pygame.font.SysFont(self.font, font_size)
        return font.render(self.text, True, color)

class UIDiv(UIBase):
    def __init__(self, styles, parent, inherit, children):
        super().__init__(styles, parent, inherit)
        self.children = children

    def render(self, screen):
        box_w = self.get_computed_styles("size", "w")
        box_h = self.get_computed_styles("size", "h")
        box_bg = self.get_computed_styles("bg", "color")
        return pygame.draw.rect(screen.surface, (box_w, box_h))