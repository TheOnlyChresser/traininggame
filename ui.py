all_styles = {}

class UIBase:
    def __init__(self, box, styles, parent, inherit):
        self.box = box
        self.styles = styles
        self.parent = parent
        self.inherit = inherit
    def add_child(self):
        pass
    def get_computed_styles(self):
        pass

class UIText(UIBase):
    def __init__(self, box, styles, parent, inherit, text, font):
        super().__init__(box, styles, parent, inherit)
        self.text = text
        self.font = font

    def render(self):
        pass

class UIDiv(UIBase):
    def __init__(self, box, styles, parent, inherit, children):
        super().__init__(box, styles, parent, inherit)
        self.children = children

    def render(self):
        pass