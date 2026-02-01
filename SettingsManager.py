import tkinter as tk
from tkinter import font
from typing import Dict, List, Optional, Tuple


class SettingsManager:
    """
    Manages settings for graphical objects on the canvas, including line width, line color, and text fonts.
    """
    def __init__(self, canvas: tk.Canvas, selected_line_id: Optional[int], line_id_to_segments: Dict[int, List[int]], text_fonts: Dict[int, Tuple[str, int, str]]):
        """
        Initializes the settings manager with references to canvas components and configurations.

        :param canvas: The canvas object where the drawings are rendered.
        :param selected_line_id: The ID of the currently selected graphical object.
        :param line_id_to_segments: A dictionary mapping line IDs to their respective segments.
        :param text_fonts: A dictionary storing font settings for text objects.
        """
        self.canvas: tk.Canvas = canvas
        self.selected_line_id: Optional[int] = selected_line_id
        self.line_id_to_segments: Dict[int, List[int]] = line_id_to_segments
        self.text_fonts: Dict[int, Tuple[str, int, str]] = text_fonts
        self.current_line_width: int = 1

    def change_line_width(self, value: int) -> None:
        """
        Changes the line width for the currently selected object.

        :param value: The new line width to be set.
        """
        self.current_line_width: int = int(value)

    def set_line_width(self, width: int) -> None:
        """
        Sets the line width or text font size based on the type of the selected object.

        :param width: The width or font size to set for the selected object.
        """
        if self.selected_line_id:
            item_type: str = self.canvas.type(self.selected_line_id)
            if item_type == "line":
                for segment in self.line_id_to_segments[self.selected_line_id]:
                    self.canvas.itemconfig(segment, width=width)
            elif item_type == "text":
                if self.selected_line_id in self.text_fonts:
                    font_name, original_size, original_color = self.text_fonts[self.selected_line_id]
                    new_size = width
                    new_font = font.Font(family=font_name, size=new_size*8)
                    self.canvas.itemconfig(self.selected_line_id, font=new_font)
                    self.text_fonts[self.selected_line_id] = (font_name, new_size, original_color)

    def set_line_color_black(self) -> None:
        """
        Sets the line color to black for the selected object.
        """
        if self.selected_line_id:
            for segment in self.line_id_to_segments[self.selected_line_id]:
                self.canvas.itemconfig(segment, fill='black')

    def set_line_color_green(self) -> None:
        """
        Sets the line color to green for the selected object.
        """
        if self.selected_line_id:
            for segment in self.line_id_to_segments[self.selected_line_id]:
                self.canvas.itemconfig(segment, fill='green')

    def set_line_color_red(self) -> None:
        """
        Sets the line color to red for the selected object.
        """
        if self.selected_line_id:
            for segment in self.line_id_to_segments[self.selected_line_id]:
                self.canvas.itemconfig(segment, fill='red')

    def set_line_color_blue(self) -> None:
        """
        Sets the line color to blue for the selected object.
        """
        if self.selected_line_id:
            for segment in self.line_id_to_segments[self.selected_line_id]:
                self.canvas.itemconfig(segment, fill='blue')

    def set_line_color_yellow(self) -> None:
        """
        Sets the line color to yellow for the selected object.
        """
        if self.selected_line_id:
            for segment in self.line_id_to_segments[self.selected_line_id]:
                self.canvas.itemconfig(segment, fill='yellow')