import tkinter as tk
import tkinter.font as font
from typing import Callable, Any


class UIManager:
    """
    Manages the user interface components such as buttons and menus for the application.
    """
    def __init__(self, root: tk.Tk, canvas: tk.Canvas, tool_manager: Any, canvas_manager: Any, file_manager: Any, settings_manager: Any, event_handler: Any):
        """
        Initializes the user interface manager with all necessary components and configurations.

        :param root: The root window of the application.
        :param canvas: The canvas on which graphical operations are performed.
        :param tool_manager: Manages the tools used for drawing and editing on the canvas.
        :param canvas_manager: Manages direct interactions with the canvas.
        :param file_manager: Manages file operations such as save and load.
        :param settings_manager: Manages settings such as line width and color.
        :param event_handler: Manages events triggered by user interactions.
        """
        self.root: tk.Tk = root
        self.canvas: tk.Canvas = canvas
        self.tool_manager: Any = tool_manager
        self.canvas_manager: Any = canvas_manager
        self.file_manager: Any = file_manager
        self.settings_manager: Any = settings_manager
        self.event_handler: Any = event_handler

        self.root.configure(bg='#333')
        style_font: font.Font = font.Font(family="Helvetica", size=9, weight="bold")
        button_width: int = 20
        self.setup_buttons(style_font, button_width)
        self.setup_popup_menu()

    def setup_buttons(self, style_font: font.Font, button_width: int) -> None:
        """
        Sets up the buttons and their respective frames for different categories of tools.
        """
        line_frame = tk.Frame(self.root, bg='#444')
        line_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        erase_frame = tk.Frame(self.root, bg='#444')
        erase_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        shape_frame = tk.Frame(self.root, bg='#444')
        shape_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        edit_frame = tk.Frame(self.root, bg='#444')
        edit_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        file_frame = tk.Frame(self.root, bg='#444')
        file_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        # Line tools
        self.create_button(line_frame, "Draw", self.tool_manager.enable_draw, style_font, button_width)
        self.line_width_scroll = tk.Scale(line_frame, from_=1, to=10, orient=tk.HORIZONTAL, label="Line Width",
                                           command=self.settings_manager.change_line_width, font=style_font, bg='#666',
                                           fg='white')
        self.line_width_scroll.pack(fill=tk.X, padx=5, pady=5)

        # Erase tools
        self.create_button(erase_frame, "Remove", self.tool_manager.enable_Remove, style_font,
                           button_width)  # Check enable_Remove spelling or function existence
        self.create_button(erase_frame, "Small Eraser", lambda: self.tool_manager.enable_eraser(2), style_font,
                           button_width)
        self.create_button(erase_frame, "Large Eraser", lambda: self.tool_manager.enable_eraser(15), style_font,
                           button_width)
        self.create_button(erase_frame, "Restart", self.canvas_manager.restart_canvas, style_font, button_width)

        # Shape tools
        self.create_button(shape_frame, "Draw Circle", self.tool_manager.enable_draw_circle, style_font, button_width)
        self.create_button(shape_frame, "Draw Rectangle", self.tool_manager.enable_draw_rectangle, style_font,
                           button_width)
        self.create_button(shape_frame, "Draw Triangle", self.tool_manager.enable_draw_triangle, style_font,
                           button_width)
        self.create_button(shape_frame, "Draw Polygon", self.tool_manager.enable_draw_polygon, style_font, button_width)
        self.create_button(shape_frame, "Text", self.tool_manager.enable_text, style_font, button_width)

        # Editing tools
        self.create_button(edit_frame, "Move", self.tool_manager.enable_move, style_font, button_width)
        self.create_button(edit_frame, "Rotate", self.tool_manager.enable_rotate, style_font, button_width)
        self.create_button(edit_frame, "Copy", self.tool_manager.enable_copy, style_font, button_width)
        self.create_button(edit_frame, "Paste", self.tool_manager.enable_paste, style_font, button_width)

        # File management tools
        self.create_button(file_frame, "Save", self.file_manager.save_drawing, style_font, button_width)
        self.create_button(file_frame, "Load", self.file_manager.load_drawing, style_font, button_width)
        self.create_button(file_frame, "Export", self.file_manager.export_canvas, style_font,button_width)

        # Bind events
        self.canvas.bind("<Button-1>", self.canvas_manager.on_mouse_move)
        self.canvas.bind("<B1-Motion>", self.canvas_manager.on_mouse_move)
        self.canvas.bind("<ButtonRelease-1>", self.canvas_manager.on_mouse_release)
        self.canvas.bind("<Button-3>", self.event_handler.popup_menu)

    def create_button(self, frame: tk.Frame, text: str, command: Callable, font: font.Font, width: int):
        """
        Creates a button and adds it to the specified frame.

        :param frame: The frame in which the button will be placed.
        :param text: The text to display on the button.
        :param command: The function to execute when the button is clicked.
        :param font: The font used for the button text.
        :param width: The width of the button.
        :return: The created button object.
        """
        button = tk.Button(frame, text=text, command=command, font=font, bg='#555', fg='white', relief=tk.FLAT,
                            width=width)
        button.pack(pady=5, padx=5, fill=tk.X)
        return button

    def setup_popup_menu(self) -> None:
        """
        Sets up the popup menu for additional options and commands.
        """
        self.popup = tk.Menu(self.root, tearoff=0, bg='#444', fg='white')
        self.popup.add_command(label="First Size", command=lambda: self.settings_manager.set_line_width(4))
        self.popup.add_command(label="Second Size", command=lambda: self.settings_manager.set_line_width(7))
        self.popup.add_command(label="Third Size", command=lambda: self.settings_manager.set_line_width(10))
        self.popup.add_separator()
        self.popup.add_command(label="Black", command=lambda: self.settings_manager.set_line_color_black())
        self.popup.add_command(label="Green", command=lambda: self.settings_manager.set_line_color_green())
        self.popup.add_command(label="Red", command=lambda: self.settings_manager.set_line_color_red())
        self.popup.add_command(label="Blue", command=lambda: self.settings_manager.set_line_color_blue())
        self.popup.add_command(label="Yellow", command=lambda: self.settings_manager.set_line_color_yellow())
        self.popup.add_separator()
        self.popup.add_command(label="Bring Forward", command=self.canvas_manager.move_forward)
        self.popup.add_command(label="Move Backward", command=self.canvas_manager.move_backward)

