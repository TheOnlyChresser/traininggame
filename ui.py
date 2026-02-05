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
        elif parts[0] in ("w","h","top","left"):
            set_style("width" if parts[0]=="w" else parts[0], int(parts[1]) if parts[1].isdigit() else None)
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

    def update_hover(self,mouse_pos):
        if not self.box: return
        x,y,w,h=self.box
        self.is_hovered=(x<=mouse_pos[0]<=x+w and y<=mouse_pos[1]<=y+h)
        if self.is_hovered: self.computed.update(self.hover_styles)
        else: self.computed=parse_classes(self.styles_str)[0]

    def get_style(self, key, default=None):
        value = self.computed.get(key)
        return default if value is None else value

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
        font_size = self.get_style("font_size", 16)
        color = self.get_style("color") or (0, 0, 0)
        font = get_cached_font(self.font_name, font_size)
        text_surface = font.render(self.text, True, color)
        surface.blit(text_surface, (self.box[0], self.box[1]))




class UIDiv(UIBase):
    def __init__(self, styles="", parent=None, children=None, on_click=None):
        super().__init__(styles, parent)
        self.children = children or []
        self.on_click = on_click
        self.radius = self.get_style("radius") or 0
        self.flex_direction = "row" 

        if "flex-col" in styles:
            self.flex_direction = "column"

    def compute_box(self):
        parent_w = self.parent.box[2] if self.parent and self.parent.box else 800
        parent_h = self.parent.box[3] if self.parent and self.parent.box else 600

        width = int(self.get_style("width") or (parent_w if self.get_style("display")=="block" else 100))
        height = int(self.get_style("height") or 50)
        x = int(self.get_style("left") or 0)
        y = int(self.get_style("top") or 0)

        self.box = (x, y, width, height)

        offset_x = 0
        offset_y = 0
        for child in self.children:
            child.compute_box()
            cw = child.box[2] if child.box else 0
            ch = child.box[3] if child.box else 0

            if self.flex_direction == "row":
                child.box = (x + offset_x, y + (height - ch)//2, cw, ch)
                offset_x += cw + 10
            else:
                child.box = (x + (width - cw)//2, y + offset_y, cw, ch)
                offset_y += ch + 10

        if self.flex_direction == "row" and self.get_style("height") is None:
            self.box = (x, y, width, max(height, max((child.box[3] for child in self.children), default=height)))
        if self.flex_direction == "column" and self.get_style("width") is None:
            self.box = (x, y, max(width, max((child.box[2] for child in self.children), default=width)), height)

        return self.box

    def handle_event(self, event):
        if self.on_click and event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            x, y, w, h = self.box
            if x <= mx <= x + w and y <= my <= y + h:
                self.on_click()
        for child in self.children:
            if hasattr(child, "handle_event"):
                child.handle_event(event)
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

        bg = self.get_style("background")
        if bg:
            pygame.draw.rect(surface, bg, self.box, border_radius=self.radius or 0)

        for child in self.children:
            if isinstance(child, UIText):
                x = self.box[0] + (child.box[0] or 0)
                y = self.box[1] + (child.box[1] or 0)
                font_size = child.get_style("font_size", 16)
                color = child.get_style("color") or (0, 0, 0)
                font = get_cached_font(child.font_name, font_size)
                text_surface = font.render(child.text, True, color)
                tx = x + (child.box[2] - text_surface.get_width()) // 2
                ty = y + (child.box[3] - text_surface.get_height()) // 2
                surface.blit(text_surface, (tx, ty))
            else:
                child.render(surface)



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

    def update(self, dt):
        self.cursor_timer += dt
        if self.cursor_timer >= 500:
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = 0

    def render(self, surface):
        if not self.box:
            self.compute_box()

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

class UIDropdown(UIDiv):
    """Dropdown container. Children: UIDropdownTrigger, UIDropdownMenu"""
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
            elif isinstance(child, UIDropdownMenu):
                self.menu = child
                child.dropdown = self

    def toggle(self):
        self.is_open = not self.is_open

    def close(self):
        self.is_open = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            # Check if clicked on trigger
            if self.trigger and self.trigger.box:
                tx, ty, tw, th = self.trigger.box
                if tx <= mx <= tx + tw and ty <= my <= ty + th:
                    self.toggle()
                    return
            # Check if clicked outside dropdown when open
            if self.is_open:
                if self.menu and self.menu.box:
                    mx2, my2, mw, mh = self.menu.box
                    if not (mx2 <= mx <= mx2 + mw and my2 <= my <= my2 + mh):
                        self.close()
        # Pass events to children
        for child in self.children:
            if hasattr(child, "handle_event"):
                child.handle_event(event)

    def render(self, surface):
        if not self.box:
            self.compute_box()
        # Render trigger
        if self.trigger:
            self.trigger.render(surface)
        # Render white overlay and menu when open
        if self.is_open:
            # Draw white overlay over entire screen
            overlay = pygame.Surface(surface.get_size())
            overlay.fill((255, 255, 255))
            surface.blit(overlay, (0, 0))
            # Re-render trigger on top of overlay
            if self.trigger:
                self.trigger.render(surface)
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
            if hasattr(child, "handle_event"):
                child.handle_event(event)


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

    def compute_box(self):
        super().compute_box()
        # Position menu below trigger if dropdown exists
        if self.dropdown and self.dropdown.trigger and self.dropdown.trigger.box:
            tx, ty, tw, th = self.dropdown.trigger.box
            x, y, w, h = self.box
            self.box = (tx, ty + th, w, h)
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
        for child in self.children:
            if hasattr(child, "handle_event"):
                child.handle_event(event)

class Screen:
    def __init__(self,width,height):
        pygame.init()
        self.surface = pygame.display.set_mode((width, height))
        self.width,self.height=width,height

