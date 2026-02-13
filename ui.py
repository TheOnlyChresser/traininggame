import pygame
from pygame.locals import GL_MULTISAMPLESAMPLES, GL_MULTISAMPLEBUFFERS

# Font cache to avoid recreating fonts every frame
_font_cache = {}

def get_cached_font(font_name, font_size):
    key = (font_name, font_size)
    if key not in _font_cache:
        _font_cache[key] = pygame.font.SysFont(font_name, font_size)
    return _font_cache[key]

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
    "xs": 12,
    "sm": 14,
    "base": 16,
    "lg": 18,
    "xl": 20,
    "2xl": 24,
    "3xl": 30,
    "4xl": 36,
    "5xl": 48
}

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2],16) for i in (0,2,4))

def parse_classes(class_string):
    styles = {
        "display": None,
        "position": None,
        "justify": None,
        "items": None,
        "width": None,
        "height": None,
        "top": None,
        "left": None,
        "background": None,
        "color": None,
        "font_size": None,
        "font_family": None,
        "radius": None,
    }
    hover_styles = {}

    radius_sizes = {
        "none":0,
        "sm":4,
        "md":8,
        "lg":12,
        "xl":16,
        "2xl":24,
        "3xl":32,
        "full":999
    }

    for cls in class_string.split():
        is_hover = cls.startswith("hover:")
        cls_name = cls[6:] if is_hover else cls
        target = hover_styles if is_hover else styles
        parts = cls_name.split("-")

        def set_style(key,value): target[key]=value

        if cls_name in ("flex","block"): set_style("display",cls_name)
        elif cls_name in ("relative","absolute","fixed"): set_style("position",cls_name)
        elif parts[0] in ("justify","items"): set_style(parts[0],parts[1])
        elif parts[0] in ("w", "h", "top", "left"):
            key_map = {"w": "width", "h": "height", "top": "top", "left": "left"}
            set_style(key_map[parts[0]], int(parts[1]) if parts[1].isdigit() else None)
        elif parts[0]=="bg" and parts[1] in colors and parts[2] in colors[parts[1]]:
            set_style("background",hex_to_rgb(colors[parts[1]][parts[2]]))
        elif parts[0]=="text":
            if parts[1] in colors and parts[2] in colors[parts[1]]:
                set_style("color",hex_to_rgb(colors[parts[1]][parts[2]]))
            elif parts[1] in sizes: set_style("font_size",sizes[parts[1]])
        elif parts[0]=="font": set_style("font_family",parts[1].capitalize())
        elif parts[0]=="rounded":
            if len(parts)==2 and parts[1] in radius_sizes: set_style("radius",radius_sizes[parts[1]])
            elif len(parts)==2 and parts[1].isdigit(): set_style("radius",int(parts[1]))
            elif len(parts)==1: set_style("radius",radius_sizes["md"])
    return styles, hover_styles

class UIBase:
    def __init__(self,styles="",parent=None):
        self.styles_str = styles
        self.parent = parent
        self.computed,self.hover_styles = parse_classes(styles)
        self.is_hovered = False
        self.children=[]
        self.box=None
        if parent: parent.children.append(self)

    def is_descendant_of(self, ancestor):
        node = self
        while node:
            if node is ancestor:
                return True
            node = node.parent
        return False

    def is_render_allowed(self):
        active = UIDropdown.active_dropdown if "UIDropdown" in globals() else None
        if not active:
            return True
        return self.is_descendant_of(active)

    def update_hover(self,mouse_pos):
        if not self.box: return
        x,y,w,h=self.box
        self.is_hovered=(x<=mouse_pos[0]<=x+w and y<=mouse_pos[1]<=y+h)
        if self.is_hovered: self.computed.update(self.hover_styles)
        else: self.computed=parse_classes(self.styles_str)[0]

    def get_style(self, key, default=None):
        value = self.computed.get(key)
        return default if value is None else value

    def shift(self, dx, dy):
        if self.box:
            x, y, w, h = self.box
            self.box = (x + dx, y + dy, w, h)
        for child in self.children:
            if hasattr(child, "shift"):
                child.shift(dx, dy)

    def shift_descendants(self, dx, dy):
        for child in self.children:
            if hasattr(child, "shift"):
                child.shift(dx, dy)

    def compute_box(self):
        parent_w = self.parent.box[2] if self.parent and self.parent.box else 800
        width = int(self.get_style("width") or (parent_w if self.get_style("display")=="block" else 100))
        height = int(self.get_style("height") or 50)
        x = int(self.get_style("left") or 0)
        y = int(self.get_style("top") or 0)
        self.box=(x,y,width,height)
        for child in self.children: child.compute_box()
        if self.get_style("height") is None and self.children:
            total_child_height=sum(int(child.box[3]) for child in self.children if child.box and child.box[3] is not None)
            self.box=(x,y,width,max(height,total_child_height))
        return self.box

class UIText(UIBase):
    def __init__(self, text, styles="", parent=None):
        super().__init__(styles, parent)
        self.text = text
        self.font_name = self.get_style("font_family", "Arial")

    def compute_box(self):
        font_size = self.get_style("font_size", 16)
        font = get_cached_font(self.font_name, font_size)
        text_width, text_height = font.size(self.text)
        width = self.get_style("width") or text_width
        height = self.get_style("height") or text_height
        x = int(self.get_style("left") or 0)
        y = int(self.get_style("top") or 0)
        self.box = (x, y, width, height)
        return self.box


    def render(self, surface):
        if not self.is_render_allowed():
            return
        font_size = self.get_style("font_size", 16)
        color = self.get_style("color") or (0, 0, 0)
        font = get_cached_font(self.font_name, font_size)
        text_surface = font.render(self.text, True, color)
        surface.blit(text_surface, (self.box[0], self.box[1]))




class UIDiv(UIBase):
    def __init__(self, styles="", parent=None, children=None, on_click=None):
        super().__init__(styles, parent)
        self.children = children or []
        for child in self.children:
            child.parent = self
        self.on_click = on_click
        self.radius = self.get_style("radius") or 0
        self.flex_direction = "row" 

        if "flex-col" in styles:
            self.flex_direction = "column"

    def compute_box(self):
        parent_w = self.parent.box[2] if self.parent and self.parent.box else 800

        width = int(self.get_style("width") or (parent_w if self.get_style("display")=="block" else 100))
        height = int(self.get_style("height") or 50)
        x = int(self.get_style("left") or 0)
        y = int(self.get_style("top") or 0)

        self.box = (x, y, width, height)

        child_specs = []
        for child in self.children:
            child.compute_box()
            old_x = child.box[0] if child.box else 0
            old_y = child.box[1] if child.box else 0
            cw = child.box[2] if child.box else 0
            ch = child.box[3] if child.box else 0
            child_specs.append((child, old_x, old_y, cw, ch))

        if child_specs:
            gap = 10
            justify = self.get_style("justify")
            items = self.get_style("items")

            if self.flex_direction == "row":
                total_main = sum(spec[3] for spec in child_specs) + gap * (len(child_specs) - 1)
                if justify == "center":
                    cursor_main = x + (width - total_main) // 2
                elif justify in ("end", "right"):
                    cursor_main = x + (width - total_main)
                else:
                    cursor_main = x

                for child, old_x, old_y, cw, ch in child_specs:
                    if items == "center":
                        cross = y + (height - ch) // 2
                    elif items in ("end", "bottom"):
                        cross = y + (height - ch)
                    else:
                        cross = y

                    new_x, new_y = cursor_main, cross
                    cursor_main += cw + gap

                    child.box = (new_x, new_y, cw, ch)
                    dx = new_x - old_x
                    dy = new_y - old_y
                    if (dx or dy) and hasattr(child, "shift_descendants"):
                        child.shift_descendants(dx, dy)
            else:
                total_main = sum(spec[4] for spec in child_specs) + gap * (len(child_specs) - 1)
                if justify == "center":
                    cursor_main = y + (height - total_main) // 2
                elif justify in ("end", "bottom"):
                    cursor_main = y + (height - total_main)
                else:
                    cursor_main = y

                for child, old_x, old_y, cw, ch in child_specs:
                    if items == "center":
                        cross = x + (width - cw) // 2
                    elif items in ("end", "right"):
                        cross = x + (width - cw)
                    else:
                        cross = x

                    new_x, new_y = cross, cursor_main
                    cursor_main += ch + gap

                    child.box = (new_x, new_y, cw, ch)
                    dx = new_x - old_x
                    dy = new_y - old_y
                    if (dx or dy) and hasattr(child, "shift_descendants"):
                        child.shift_descendants(dx, dy)

        if self.flex_direction == "row" and self.get_style("height") is None:
            self.box = (x, y, width, max(height, max((child.box[3] for child in self.children), default=height)))
        if self.flex_direction == "column" and self.get_style("width") is None:
            self.box = (x, y, max(width, max((child.box[2] for child in self.children), default=width)), height)

        return self.box

    def handle_event(self, event):
        # Open dropdowns get first priority and consume clicks outside/inside the menu.
        for child in reversed(self.children):
            if isinstance(child, UIDropdown) and child.is_open:
                if child.handle_event(event):
                    return True

        if self.on_click and event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            x, y, w, h = self.box
            if x <= mx <= x + w and y <= my <= y + h:
                self.on_click()
                return True

        for child in reversed(self.children):
            if hasattr(child, "handle_event") and child.handle_event(event):
                return True
        return False
    def update_hover(self, mouse_pos):
        if not self.box:
            return
        x, y, w, h = self.box
        self.is_hovered = (x <= mouse_pos[0] <= x + w and y <= mouse_pos[1] <= y + h)
        if self.is_hovered and self.hover_styles:
            self.computed.update(self.hover_styles)
        elif not self.is_hovered:
            self.computed = parse_classes(self.styles_str)[0]

        for child in self.children:
            if hasattr(child, "update_hover"):
                child.update_hover(mouse_pos)

    def render(self, surface):
        if not self.box:
            self.compute_box()

        if not self.is_render_allowed():
            for child in self.children:
                child.render(surface)
            return

        bg = self.get_style("background")
        if bg:
            pygame.draw.rect(surface, bg, self.box, border_radius=self.radius or 0)

        open_dropdowns = []
        for child in self.children:
            if isinstance(child, UIDropdown) and child.is_open:
                open_dropdowns.append(child)
                continue

            if isinstance(child, UIText):
                x = child.box[0] or 0
                y = child.box[1] or 0
                font_size = child.get_style("font_size", 16)
                color = child.get_style("color") or (0, 0, 0)
                font = get_cached_font(child.font_name, font_size)
                text_surface = font.render(child.text, True, color)
                tx = x + (child.box[2] - text_surface.get_width()) // 2
                ty = y + (child.box[3] - text_surface.get_height()) // 2
                surface.blit(text_surface, (tx, ty))
            else:
                child.render(surface)

        # Render open dropdowns last so the menu appears above sibling controls.
        for dropdown in open_dropdowns:
            dropdown.render(surface)



class UIInput(UIBase):
    def __init__(self, placeholder="", styles="", parent=None, on_change=None):
        super().__init__(styles, parent)
        self.placeholder = placeholder
        self.text = ""
        self.focused = False
        self.on_change = on_change
        self.cursor_visible = True
        self.cursor_timer = 0
        self.font_name = self.get_style("font_family", "Arial")
        self.radius = self.get_style("radius") or 0

    def compute_box(self):
        parent_w = self.parent.box[2] if self.parent and self.parent.box else 800
        width = int(self.get_style("width") or 200)
        height = int(self.get_style("height") or 40)
        x = int(self.get_style("left") or 0)
        y = int(self.get_style("top") or 0)
        self.box = (x, y, width, height)
        return self.box

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            x, y, w, h = self.box
            if x <= mx <= x + w and y <= my <= y + h:
                self.focused = True
                return True
            else:
                self.focused = False

        if self.focused and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN:
                self.focused = False
            elif event.key == pygame.K_ESCAPE:
                self.focused = False
            else:
                if event.unicode and event.unicode.isprintable():
                    self.text += event.unicode
            
            if self.on_change:
                self.on_change(self.text)
            return True
        return False

    def update(self, dt):
        self.cursor_timer += dt
        if self.cursor_timer >= 500:
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = 0

    def render(self, surface):
        if not self.box:
            self.compute_box()

        if not self.is_render_allowed():
            return

        x, y, w, h = self.box

        # Draw background
        bg = self.get_style("background") or (255, 255, 255)
        pygame.draw.rect(surface, bg, self.box, border_radius=self.radius)

        # Draw border (highlighted if focused)
        border_color = (0, 120, 215) if self.focused else (200, 200, 200)
        pygame.draw.rect(surface, border_color, self.box, width=2, border_radius=self.radius)

        # Draw text or placeholder
        font_size = self.get_style("font_size", 16)
        font = get_cached_font(self.font_name, font_size)
        
        padding = 10
        if self.text:
            color = self.get_style("color") or (0, 0, 0)
            text_surface = font.render(self.text, True, color)
        else:
            placeholder_color = (150, 150, 150)
            text_surface = font.render(self.placeholder, True, placeholder_color)

        # Center text vertically, align left with padding
        tx = x + padding
        ty = y + (h - text_surface.get_height()) // 2
        
        # Clip text to input bounds
        clip_rect = pygame.Rect(x + padding, y, w - padding * 2, h)
        surface.set_clip(clip_rect)
        surface.blit(text_surface, (tx, ty))
        surface.set_clip(None)

        # Draw cursor if focused
        if self.focused and self.cursor_visible:
            cursor_x = tx + font.size(self.text)[0]
            cursor_y1 = y + 8
            cursor_y2 = y + h - 8
            pygame.draw.line(surface, (0, 0, 0), (cursor_x, cursor_y1), (cursor_x, cursor_y2), 2)


class UIIconButton(UIDiv):
    def __init__(self, on_click=None, styles="", label="i"):
        base_styles = (
            "w-26 h-26 bg-sky-500 rounded-full hover:bg-sky-400 "
            "items-center flex flex-col justify-center font-arial"
        )
        merged_styles = f"{base_styles} {styles}".strip()
        super().__init__(
            styles=merged_styles,
            children=[UIText(label, styles="text-neutral-50 text-sm font-arial text-center")],
            on_click=on_click,
        )


class UIModal:
    def __init__(self):
        self.visible = False
        self.title = ""
        self.body = ""
        self.panel_rect = None
        self.close_rect = None

    def is_open(self):
        return self.visible

    def open(self, title, body):
        self.title = title or "Info"
        self.body = body or ""
        self.visible = True

    def close(self):
        self.visible = False

    def _wrap_text(self, text, font, max_width):
        lines = []
        for paragraph in text.split("\n"):
            words = paragraph.split()
            if not words:
                lines.append("")
                continue

            current = words[0]
            for word in words[1:]:
                trial = f"{current} {word}"
                if font.size(trial)[0] <= max_width:
                    current = trial
                else:
                    lines.append(current)
                    current = word
            lines.append(current)
        return lines

    def handle_event(self, event):
        if not self.visible:
            return False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.close()
            return True

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()

            if self.close_rect and self.close_rect.collidepoint(mx, my):
                self.close()
                return True

            if self.panel_rect and not self.panel_rect.collidepoint(mx, my):
                self.close()
                return True

            return True

        # Modal is open: consume remaining events to block underlying UI.
        return True

    def render(self, surface):
        if not self.visible:
            return

        surface_width, surface_height = surface.get_size()
        panel_width = min(620, surface_width - 80)
        panel_height = min(360, surface_height - 80)
        panel_x = (surface_width - panel_width) // 2
        panel_y = (surface_height - panel_height) // 2

        self.panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
        self.close_rect = pygame.Rect(panel_x + panel_width - 40, panel_y + 12, 28, 28)

        overlay = pygame.Surface((surface_width, surface_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 140))
        surface.blit(overlay, (0, 0))

        pygame.draw.rect(surface, (250, 250, 250), self.panel_rect, border_radius=12)
        pygame.draw.rect(surface, (200, 200, 200), self.panel_rect, width=2, border_radius=12)

        pygame.draw.rect(surface, (230, 230, 230), self.close_rect, border_radius=6)
        close_font = get_cached_font("Arial", 18)
        close_text = close_font.render("X", True, (60, 60, 60))
        close_x = self.close_rect.x + (self.close_rect.width - close_text.get_width()) // 2
        close_y = self.close_rect.y + (self.close_rect.height - close_text.get_height()) // 2
        surface.blit(close_text, (close_x, close_y))

        title_font = get_cached_font("Arial", 26)
        body_font = get_cached_font("Arial", 18)

        title_surface = title_font.render(self.title, True, (20, 20, 20))
        surface.blit(title_surface, (panel_x + 20, panel_y + 20))

        body_lines = self._wrap_text(self.body, body_font, panel_width - 40)
        cursor_y = panel_y + 70
        for line in body_lines:
            if cursor_y > panel_y + panel_height - 30:
                break
            line_surface = body_font.render(line, True, (50, 50, 50))
            surface.blit(line_surface, (panel_x + 20, cursor_y))
            cursor_y += 24

class UIDropdown(UIDiv):
    """Dropdown container. Children: UIDropdownTrigger, UIDropdownMenu"""
    active_dropdown = None
    def __init__(self, styles="", parent=None, children=None, on_click=None):
        super().__init__(styles, parent, children, on_click)
        self.is_open = False
        self.trigger = None
        self.menu = None
        # Find trigger and menu from children
        for child in self.children:
            if isinstance(child, UIDropdownTrigger):
                self.trigger = child
                child.dropdown = self
                child.parent = self
            elif isinstance(child, UIDropdownMenu):
                self.menu = child
                child.dropdown = self
                child.parent = self

    def _layout_children(self):
        if not self.box:
            return
        x, y, w, h = self.box
        if self.trigger:
            self.trigger.compute_box()
            tw = self.trigger.box[2] if self.trigger.box else w
            th = self.trigger.box[3] if self.trigger.box else 50
            self.trigger.box = (x, y, tw, th)
        if self.menu:
            self.menu.compute_box()
            mw = self.menu.box[2] if self.menu.box else w
            mh = self.menu.box[3] if self.menu.box else 50
            trigger_h = self.trigger.box[3] if self.trigger and self.trigger.box else 0
            self.menu.box = (x, y + trigger_h, mw, mh)

    def compute_box(self):
        parent_w = self.parent.box[2] if self.parent and self.parent.box else 800
        width = int(self.get_style("width") or (parent_w if self.get_style("display") == "block" else 100))
        height = int(self.get_style("height") or 50)
        x = int(self.get_style("left") or 0)
        y = int(self.get_style("top") or 0)
        self.box = (x, y, width, height)
        self._layout_children()
        if self.get_style("height") is None and self.trigger and self.trigger.box:
            self.box = (x, y, width, int(self.trigger.box[3]))
            self._layout_children()
        return self.box

    def toggle(self):
        self.is_open = not self.is_open
        if self.is_open:
            UIDropdown.active_dropdown = self
        elif UIDropdown.active_dropdown is self:
            UIDropdown.active_dropdown = None

    def close(self):
        self.is_open = False
        if UIDropdown.active_dropdown is self:
            UIDropdown.active_dropdown = None

    def handle_event(self, event):
        self._layout_children()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            # Check if clicked on trigger
            if self.trigger and self.trigger.box:
                tx, ty, tw, th = self.trigger.box
                if tx <= mx <= tx + tw and ty <= my <= ty + th:
                    self.toggle()
                    return True

            # While menu is open it owns the mouse event.
            if self.is_open:
                if self.menu and self.menu.box:
                    mx2, my2, mw, mh = self.menu.box
                    inside_menu = mx2 <= mx <= mx2 + mw and my2 <= my <= my2 + mh
                    if inside_menu:
                        for option in reversed(self.menu.children):
                            if hasattr(option, "handle_event") and option.handle_event(event):
                                return True
                        return True

                self.close()
                return True

        for child in self.children:
            if hasattr(child, "handle_event") and child.handle_event(event):
                return True
        return False

    def render(self, surface):
        if not self.box:
            self.compute_box()
        else:
            self._layout_children()
        if self.trigger and not self.is_open:
            self.trigger.render(surface)
        if self.is_open:
            # Render menu
            if self.menu:
                self.menu.render(surface)


class UIDropdownTrigger(UIDiv):
    """Dropdown trigger button. Parent: UIDropdown"""
    def __init__(self, styles="", parent=None, children=None, on_click=None):
        super().__init__(styles, parent, children, on_click)
        self.dropdown = None  # Set by parent UIDropdown

    def handle_event(self, event):
        # Trigger events are handled by parent UIDropdown
        for child in self.children:
            if hasattr(child, "handle_event") and child.handle_event(event):
                return True
        return False


class UIDropdownMenu(UIDiv):
    """Dropdown menu container. Parent: UIDropdown, Children: UIDropdownOption"""
    def __init__(self, styles="", parent=None, children=None, on_click=None):
        super().__init__(styles, parent, children, on_click)
        self.dropdown = None  # Set by parent UIDropdown
        self.options = []
        # Find options from children
        for child in self.children:
            if isinstance(child, UIDropdownOption):
                self.options.append(child)
                child.menu = self
                child.parent = self

    def compute_box(self):
        super().compute_box()
        # Position menu below trigger if dropdown exists
        if self.dropdown and self.dropdown.trigger and self.dropdown.trigger.box:
            tx, ty, tw, th = self.dropdown.trigger.box
            old_x, old_y, w, h = self.box
            new_x, new_y = tx, ty + th
            self.box = (new_x, new_y, w, h)
            dx = new_x - old_x
            dy = new_y - old_y
            if dx or dy:
                for child in self.children:
                    if hasattr(child, "shift"):
                        child.shift(dx, dy)
        return self.box


class UIDropdownOption(UIDiv):
    """Dropdown menu option. Parent: UIDropdownMenu"""
    def __init__(self, value="", styles="", parent=None, children=None, on_click=None, on_select=None):
        super().__init__(styles, parent, children, on_click)
        self.value = value
        self.menu = None  # Set by parent UIDropdownMenu
        self.on_select = on_select

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            if self.box:
                x, y, w, h = self.box
                if x <= mx <= x + w and y <= my <= y + h:
                    if self.on_select:
                        self.on_select(self.value)
                    if self.menu and self.menu.dropdown:
                        self.menu.dropdown.close()
                    if self.on_click:
                        self.on_click()
                    return True
        for child in self.children:
            if hasattr(child, "handle_event") and child.handle_event(event):
                return True
        return False

class Screen:
    def __init__(self,width,height):
        pygame.init()
        self.surface = pygame.display.set_mode((width, height))
        self.width,self.height=width,height

