################################################################################
# Copyright (C) 2020 Abstract Horizon
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License v2.0
# which accompanies this distribution, and is available at
# https://www.apache.org/licenses/LICENSE-2.0
#
#  Contributors:
#    Daniel Sendula - initial API and implementation
#
#################################################################################


from pyros_support_ui.components import *


class BackgroundChangeDecoration(Component):
    def __init__(self, colour):
        super(BackgroundChangeDecoration, self).__init__(None)  # Call super constructor to store rectable
        self.colour = colour

    def draw(self, surface):
        pygame.draw.rect(surface, self.colour, self.rect)


class MenuButtonBackgroundDecoration(Component):
    def __init__(self, colour):
        super(MenuButtonBackgroundDecoration, self).__init__(None)  # Call super constructor to store rectangle
        self.colour = colour

    def draw(self, surface):
        pygame.draw.rect(surface, self.colour, self.rect)


class ButtonRectangleDecoration(Component):
    def __init__(self, colour, background_colour):
        super(ButtonRectangleDecoration, self).__init__(None)  # Call super constructor to store rectangle
        self.colour = colour
        self.background_colour = background_colour
        self.strip_width = 5
        self.strip_margin = 3
        self.cut_width = 6
        self.cut_margin = 3
        self.cut_size = 15

    def draw(self, surface):
        if self.background_colour is not None:
            pygame.draw.rect(surface, self.background_colour, self.rect)

        x1 = self.rect.x
        x2 = self.rect.right - 1
        y1 = self.rect.y
        y2 = self.rect.bottom - 1
        try:
            pygame.draw.rect(surface, self.colour, pygame.Rect(x1, y1, self.strip_width, self.rect.height))
        except Exception:
            print(self.colour)
        pygame.draw.line(surface, self.colour, (x1 + self.strip_width + self.strip_margin, y1), (x2 - self.cut_size, y1))
        pygame.draw.line(surface, self.colour, (x2 - self.cut_size, y1), (x2, y1 + self.cut_size))
        pygame.draw.line(surface, self.colour, (x2, y1 + self.cut_size), (x2, y2))
        pygame.draw.line(surface, self.colour, (x2, y2), (x1 + self.strip_margin, y2))
        pygame.draw.line(surface, self.colour, (x1 + self.strip_width + self.strip_margin, y2), (x1 + self.strip_width + self.strip_margin, y1))

        pygame.draw.polygon(surface, self.colour, [
            (x2 - self.cut_size + self.cut_margin, y1),
            (x2 - self.cut_size + self.cut_margin + self.cut_width, y1),
            (x2, y1 + self.cut_size - self.cut_margin - self.cut_width),
            (x2, y1 + self.cut_size - self.cut_margin)
        ])


class BorderDecoration(Component):
    def __init__(self, rect, colour):
        super(BorderDecoration, self).__init__(rect)  # Call super constructor to store rectangle
        self.colour = colour
        self.top_left_cut = 8
        self.bottom_right_cut = 5

    def draw(self, surface):
        x1 = self.rect.x
        x2 = self.rect.right - 1
        y1 = self.rect.y
        y2 = self.rect.bottom - 1

        pygame.draw.polygon(surface, self.colour, [
            (x1 + self.top_left_cut, y1),
            (x2, y1),
            (x2, y2 - self.bottom_right_cut),
            (x2 - self.bottom_right_cut, y2),
            (x1, y2),
            (x1, y1 + self.top_left_cut)
        ], 1)


class BoxBlueSFThemeFactory(BaseUIFactory):
    def __init__(self, ui_adapter,
                 font=None,
                 small_font=None,
                 colour=pygame.color.THECOLORS['cornflowerblue'],
                 disabled_colour=pygame.color.THECOLORS['gray'],
                 background_colour=(0, 0, 0, 255),
                 mouse_over_colour=pygame.color.THECOLORS['yellow'],
                 mouse_over_background_colour=pygame.color.THECOLORS['gray32']):
        super(BoxBlueSFThemeFactory, self).__init__(ui_adapter,
                                                    font=font,
                                                    small_font=small_font,
                                                    colour=colour,
                                                    disabled_colour=disabled_colour,
                                                    background_colour=background_colour,
                                                    mouse_over_colour=mouse_over_colour)
        self.mouse_over_background_colour = mouse_over_background_colour

    def setMouseOverColour(self, mouse_over_colour):
        self.mouse_over_colour = mouse_over_colour

    def setBackgroundColour(self, background_colour):
        self.background_colour = background_colour

    def label(self, rect, text, font=None, colour=None, h_alignment=ALIGNMENT.LEFT, v_alignment=ALIGNMENT.TOP, hint=UiHint.NORMAL):
        return Label(rect, text, font=font if font is not None else self.font, colour=colour, h_alignment=h_alignment, v_alignment=v_alignment)

    def _disabled_label(self, rect, text, font=None, h_alignment=ALIGNMENT.LEFT, v_alignment=ALIGNMENT.TOP, hint=UiHint.NORMAL):
        return Label(rect, text, font=font if font is not None else self.font, colour=self.disabled_colour, h_alignment=h_alignment, v_alignment=v_alignment)

    def image(self, rect, image, h_alignment=ALIGNMENT.LEFT, v_alignment=ALIGNMENT.TOP, hint=UiHint.NORMAL):
        return Image(rect, image, h_alignment=h_alignment, v_alignment=v_alignment)

    def button(self, rect, on_click=None, on_hover=None,
               label=None, disabled_label=None, hint=UiHint.NORMAL):
        colour = self.colour
        background_colour = self.background_colour
        mouse_over_colour = self.mouse_over_colour
        mouse_over_background_colour = self.mouse_over_background_colour
        if hint == UiHint.WARNING:
            colour = pygame.color.THECOLORS['orange']
            background_colour = self.background_colour
            mouse_over_colour = pygame.color.THECOLORS['orange']
            mouse_over_background_colour = pygame.color.THECOLORS['darkorange4']
        elif hint == UiHint.ERROR:
            colour = pygame.color.THECOLORS['red']
            background_colour = self.background_colour
            mouse_over_colour = pygame.color.THECOLORS['red']
            mouse_over_background_colour = pygame.color.THECOLORS['darkred']
        if hint == UiHint.NO_DECORATION:
            return Button(rect, on_click, on_hover, label, disabled_label=disabled_label,
                          mouse_over_decoration=BackgroundChangeDecoration(mouse_over_background_colour))
        else:
            return Button(rect, on_click, on_hover, label, disabled_label=disabled_label,
                          background_decoration=ButtonRectangleDecoration(colour, background_colour),
                          mouse_over_decoration=ButtonRectangleDecoration(mouse_over_colour, mouse_over_background_colour))

    def panel(self, rect, background_colour=None, layout: Optional[BaseLayout] = None, hint=UiHint.NORMAL):
        if background_colour is None:
            if hint == UiHint.WARNING:
                background_colour = pygame.color.THECOLORS['orange']
            elif hint == UiHint.ERROR:
                background_colour = pygame.color.THECOLORS['red']
        return Panel(rect, background_colour, decoration=BorderDecoration(rect, self.colour), layout=layout)

    def menu(self, rect, background_colour=None, hint=UiHint.NORMAL):
        if background_colour is None:
            if hint == UiHint.WARNING:
                background_colour = pygame.color.THECOLORS['orange']
            elif hint == UiHint.ERROR:
                background_colour = pygame.color.THECOLORS['red']
        return Menu(rect, self, background_colour, decoration=BorderDecoration(rect, self.colour))

    def _menu_item_text_button(self, rect, label, callback):
        return self._menu_item_button(rect, self.label(None, label, h_alignment=ALIGNMENT.CENTER, v_alignment=ALIGNMENT.MIDDLE), callback)

    def _menu_item_button(self, rect, label, callback):
        return Button(rect, callback, label=label, mouse_over_decoration=MenuButtonBackgroundDecoration(self.mouse_over_background_colour))

    def border(self, rect, colour=pygame.color.THECOLORS['white']):
        return BorderDecoration(rect, colour)
