import argparse
import tkinter as tk
from typing import Dict, List, Optional, Any
from CanvasManager import CanvasManager
from ToolManager import ToolManager
from UIManager import UIManager
from FileManager import FileManager
from EventHandler import EventHandler
from SettingsManager import SettingsManager
from TextManager import TextManager

class MainApplication:
    """
    MainApplication initializes and manages the main components of the Vector Graphics Editor.
    """
    def __init__(self, root: tk.Tk) -> None:
        """
         Initialize the main application with necessary managers and configurations.
         :param root: The root window for the application.
         """
        self.root: tk.Tk = root
        self.root.title("Vector Graphics Editor")
        self.root.resizable(False, False)
        self.canvas: tk.Canvas = tk.Canvas(root, width=900, height=400, bg="white")
        self.canvas.pack(expand=True, fill=tk.BOTH)
        self.text_input: Any = TextManager.text_input

        # Dictionary mapping line IDs to their segment data
        self.line_id_to_segments: Dict[int, List[int]] = {}

        # Dictionary to store text font data
        self.text_fonts: Dict[Any, Any] = {}

        # Currently selected line ID
        self.selected_line_id: Optional[int] = None

        # List of lines on the canvas
        self.lines: List[List[int]] = []


        # Setup the popup menu.
        self.popup: tk.Menu = tk.Menu(self.root, tearoff=0)

        # Set the default mode of the application to drawing.
        self.mode = "draw"

        # Initialize all managers involved in the application.
        self.text_manager = TextManager(self.canvas, self.line_id_to_segments)
        self.settings_manager = SettingsManager(self.canvas,self.selected_line_id, self.line_id_to_segments, self.text_manager.text_fonts)
        self.file_manager = FileManager(self.canvas, self.line_id_to_segments, self.lines,self.settings_manager)
        self.canvas_manager = CanvasManager(self.canvas,self.line_id_to_segments,self.settings_manager,self.lines)
        self.event_handler = EventHandler(self.canvas, self.mode, self.canvas_manager, self.text_manager.text_input, self.popup,self.settings_manager,self.file_manager)
        self.tool_manager = ToolManager(self.event_handler, self.canvas_manager, self.canvas)


        # Initialize the user interface and link the popup menu.
        self.ui_manager: UIManager = UIManager(root, self.canvas, self.tool_manager, self.canvas_manager, self.file_manager,
                                    self.settings_manager, self.event_handler)

        # Set the popup menu from UIManager to be used in the application
        self.event_handler.popup = self.ui_manager.popup


def main():
    parser = argparse.ArgumentParser(
        description="Vector Graphics Editor: A simple tool for creating and manipulating vector graphics.")
    args = parser.parse_args()  # This parses the command-line arguments

    root = tk.Tk()
    app = MainApplication(root)
    root.mainloop()

if __name__ == "__main__":
    main()
