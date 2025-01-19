import pyglet

class BlackjackWindow:
    """Class for rendering"""
    
    unicode_hex = 0x1f0a1 # Starting card. See https://en.wikipedia.org/wiki/Playing_cards_in_Unicode
    card_to_unicode = {}
    for suit in "SHDC":
        for value in "A23456789TJNQK": # N is for "Knight"??? Don't ask me why
            card_unicode = str(hex(unicode_hex))[2:]
            card_to_unicode[value + suit] = chr(int(card_unicode, 16))
            unicode_hex += 1
        unicode_hex += 2
    card_to_unicode["HIDDEN"] = chr(0x1f0a0)
    
    def __init__(self, X, Y):
        self.active = True
        self.width = X
        self.height = Y
        self.display_surface = pyglet.window.Window(width=X, height=Y+50)
        self.top = Y
        
        # make OpenGL context current
        self.display_surface.switch_to()
        self.reset()
        
    def text(self, text, x, y, font_size=20, color=(255, 255, 255)):
        """Draw text"""
        y = self.top - y
        label = pyglet.text.Label(text, font_size=font_size, 
                                  x=x, y=y, anchor_x='center', anchor_y='center',
                                  color=color)
        label.draw()
    
    def card(self, x, y, c):
        """Draw a card"""
        card = self.card_to_unicode[c]
        self.text(card, x, y, font_size=100)
        
    def reset(self):
        """New frame"""
        pyglet.clock.tick()
        self.display_surface.dispatch_events()
        from pyglet.gl import glClear
        glClear(pyglet.gl.GL_COLOR_BUFFER_BIT)

    def update(self):
        """Draw the current state on screen"""
        self.display_surface.flip()
        
if __name__ == '__main__':
    bjw = BlackjackWindow(400, 400)

    bjw.reset()
    bjw.card(100, 100, "HIDDEN")
    bjw.update()
    input()