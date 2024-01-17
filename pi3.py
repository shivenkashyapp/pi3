"""
A tiny wrapper for i3bar using python, that uses JSON output.
"""

import time
import json

def h(d):
    _ = hex(d).split("x")[-1]
    if len(_) == 1: return "0" + _
    return _

def Hex(r, g, b) -> str:
    """Parse RGB colors into HTML-like hex color strings."""
    return f"#{h(r)}{h(g)}{h(b)}" 

class Block:
    def __init__(
            self, 

            name: str,                      # name and instance are ignored by i3bar, 
            instance: str,                  # but are used to identify a block in scripts.

            full_text: str,
            short_text: str,                # text when 
            
            color: str = "#ffffff",         # foreground color
            background: str = "#000000",    # override background color

            border: str = "#000000",        # border color
            border_top: int = 1,
            border_left: int = 1,
            border_right: int = 1,
            border_bottom: int = 1,

            min_width: int = 40,            # pixels
            align: str = "left",            # center, right, left (default)
            
            separator: bool = 1,            # draw a separator after the block?
            separator_block_width: int = 3, # set this to an odd value, since the separator is drawn in the middle.

            markup: str = "pango"           # pango, none. (pango works only with a pango font)
            ) -> None:

        self.name = name
        self.instance = instance
        self.full_text = full_text
        self.short_text = short_text
        self.color = color
        self.background = self.bg = background

        self.border = border
        self.border_top, self.border_left, self.border_right, self.border_bottom = border_top, border_left, border_right, border_bottom
        
        self.min_width = min_width
        self.align = align
        self.separator = separator
        self.sep_width = separator_block_width
        self.markup = markup

        
    def json(self):
        return vars(self)

class Bar:
    """A utility class to allow users to construct blocks of data output to the statusline."""
    def __init__(self, version: int, stop_signal: int = 10, cont_signal: int = 12, click_events: bool = True) -> None:
        self.version = version
        self.stop_signal = stop_signal
        self.cont_signal = cont_signal
        self.click_events = click_events

        self.blocks: list = []
        self.jsons: list = []
        
        """
        self.header = json.dumps({
                'version':      self.version,
                'stop_signal':  self.stop_signal,
                'cont_signal':  self.cont_signal,
                'click_events': self.click_events
            }
        )
        """
        self.header = '{ "version" : 1 }'

    def add(self, block: Block) -> None:
        self.blocks.append(copy(block))

    def run(self, repeat: int | float = 1) -> None:
        """Pipe JSON for the Blocks onto stdout."""
        print(self.header)
        print("[\n[],\n")

        l = len(self.blocks)

        while 1:
            ch = ","; print("[\n")

            for c in range(l):
                if c == l-1: ch = ""
                print(json.dumps(self.blocks[c].json(), indent=4) + ch)
            print("],")

            time.sleep(repeat)
