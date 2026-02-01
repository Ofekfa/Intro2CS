import tkinter as tki
from tkinter import font, Toplevel, Entry, Scale, Button, OptionMenu, StringVar
from typing import Dict, List, Tuple, Optional


class TextManager:
    """
    Manages text input and formatting options on the canvas.
    """
    def __init__(self, root: tki.Canvas, line_id_to_segments: Dict[int, List[int]]) -> None:
        """
        Initializes the TextManager with the main application window and line segments dictionary.

        :param root: The main application window.
        :param line_id_to_segments: Dictionary to keep track of line segments associated with text.
        """
        self.text_window: Optional[Toplevel] = None
        self.text_entry: Optional[Entry] = None
        self.font_var: Optional[StringVar] = None
        self.font_menu: Optional[OptionMenu] = None
        self.font_size: Optional[Scale] = None
        self.color_var: Optional[StringVar] = None
        self.color_menu: Optional[OptionMenu] = None
        self.original_font: Optional[Tuple[str, int, str]] = None
        self.canvas: tki.Canvas = root
        self.line_id_to_segments: Dict[int, List[int]] = line_id_to_segments
        self.text_fonts: Dict[int, Tuple[str, int, str]] = {}
        self.mode: str = "text"

    def text_input(self, event: tki.Event) -> None:
        """
        Opens a dialog for text input and formatting when in text mode.

        :param event: The event triggering the text input dialog.
        """
        if self.mode == "text":
            self.text_window = tki.Toplevel(self.canvas)
            self.text_window.title("Enter Text")
            self.text_entry = tki.Entry(self.text_window, width=20)
            self.text_entry.pack(pady=10)

            # Font selection
            self.font_families = font.families()
            self.font_var = tki.StringVar(self.text_window)
            self.font_var.set("Arial")  # default font
            self.font_menu = tki.OptionMenu(self.text_window, self.font_var, *self.font_families)
            self.font_menu.pack()

            # Font size selection
            self.font_size = tki.Scale(self.text_window, from_=8, to=72, orient=tki.HORIZONTAL, label="Font Size")
            self.font_size.set(16)
            self.font_size.pack()

            # Color selection
            self.colors = ['Black', 'Red', 'Green', 'Blue', 'Yellow', 'Orange', 'Purple', 'Brown']
            self.color_var = tki.StringVar(self.text_window)
            self.color_var.set('Black')
            self.color_menu = tki.OptionMenu(self.text_window, self.color_var, *self.colors)
            self.color_menu.pack()

            # Buttons for accept or cancel
            tki.Button(self.text_window, text="OK", command=lambda: self.place_text(event.x, event.y)).pack(side=tki.LEFT)
            tki.Button(self.text_window, text="Cancel", command=self.text_window.destroy).pack(side=tki.RIGHT)

    def place_text(self, x: int, y: int) -> None:
        """
        Places the entered text onto the canvas at the specified coordinates.

        :param x: X-coordinate on the canvas.
        :param y: Y-coordinate on the canvas.
        """
        user_text = self.text_entry.get()
        selected_font = self.font_var.get()
        selected_size = int(self.font_size.get())
        selected_color = self.color_var.get()
        self.original_font = (selected_font, selected_size, selected_color)
        text_font = font.Font(family=selected_font, size=selected_size)
        text_id = self.canvas.create_text(x, y, text=user_text, font=text_font, fill=selected_color)
        self.line_id_to_segments[text_id] = [text_id]
        self.text_window.destroy()
        self.text_fonts[text_id] = (selected_font, selected_size, selected_color)



