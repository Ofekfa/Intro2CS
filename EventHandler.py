import tkinter as tk
from typing import Any, Callable, Optional


class EventHandler:
    """
    Handles events on the canvas based on the current mode, coordinating between different managers.
    """
    def __init__(self, canvas: tk.Canvas, mode: str, canvas_manager: Any, text_input: Callable, popup, settings_manager: Any, file_manager: Any) -> None:
        """
        Initializes the event handler with the necessary components and settings.

        :param canvas: The canvas where the events will be handled.
        :param mode: The initial mode the application is set to.
        :param canvas_manager: The manager that handles drawing and object manipulation on the canvas.
        :param text_input: The function to handle text input events.
        :param popup: The popup menu to be used for context actions.
        :param settings_manager: Manages application settings like tool configurations.
        :param file_manager: Manages file-related actions such as save, load, and export.
        """
        self.canvas: tk.Canvas = canvas
        self.mode: str = mode
        self.canvas_manager: Any = canvas_manager
        self.text_input: Callable = text_input
        self.popup: tk.Menu = popup
        self.update_mouse_events()
        self.settings_manager: Any = settings_manager
        self.file_manager: Any = file_manager
        self.selected_line_id: Optional[int] = None
        self.prev_x: Optional[int] = None
        self.prev_y: Optional[int] = None


    def update_mouse_events(self) -> None:
        """
        Updates the mouse event bindings based on the current mode.
        """
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")

        if self.mode == "draw":
            self.canvas.bind("<Button-1>", self.canvas_manager.on_mouse_down)
            self.canvas.bind("<B1-Motion>", self.canvas_manager.on_mouse_move)
            self.canvas.bind("<ButtonRelease-1>", self.canvas_manager.on_mouse_release)
        elif self.mode == "move":
            self.canvas.bind("<Button-1>", self.canvas_manager.on_mouse_down)
            self.canvas.bind("<B1-Motion>", self.canvas_manager.on_mouse_move)
            self.canvas.bind("<ButtonRelease-1>", self.canvas_manager.on_mouse_release)
        elif self.mode == "circle":
            self.canvas.bind("<Button-1>", self.canvas_manager.start_circle)
            self.canvas.bind("<B1-Motion>", self.canvas_manager.draw_circle)
            self.canvas.bind("<ButtonRelease-1>", self.canvas_manager.finish_circle)
        elif self.mode == "rectangle":
            self.canvas.bind("<Button-1>", self.canvas_manager.start_rectangle)
            self.canvas.bind("<B1-Motion>", self.canvas_manager.draw_rectangle)
            self.canvas.bind("<ButtonRelease-1>", self.canvas_manager.finish_rectangle)
        elif self.mode == "triangle":
            self.canvas.bind("<Button-1>", self.canvas_manager.start_triangle)
            self.canvas.bind("<B1-Motion>", self.canvas_manager.draw_triangle)
            self.canvas.bind("<ButtonRelease-1>", self.canvas_manager.finish_triangle)
        elif self.mode == "polygon":
            self.canvas.bind("<Button-1>", self.canvas_manager.add_polygon_point)
            self.canvas.bind("<Double-1>", self.canvas_manager.finish_polygon)
        elif self.mode == "Remove":
            self.canvas.bind("<Button-1>", self.canvas_manager.on_mouse_down)
        elif self.mode == "eraser":
            self.canvas.bind("<B1-Motion>", self.canvas_manager.eraser)
        elif self.mode == "text":
            self.canvas.bind("<Button-1>", self.text_input)
            print("Text input function is bound to canvas click.")
        elif self.mode == "copy":
            self.canvas.bind("<Button-1>", self.copy_selected_object)
        elif self.mode == "paste":
            self.canvas.bind("<Button-1>", self.paste_copied_object)
        # If no valid mode is set, ensure no events are bound
        else:
            self.canvas.unbind("<Button-1>")
            self.canvas.unbind("<B1-Motion>")
            self.canvas.unbind("<ButtonRelease-1>")

    def popup_menu(self, event: tk.Event) -> None:
        """
        Displays a popup menu at the cursor location if a line is selected.

        :param event: The mouse event that triggered the popup.
        """
        self.selected_line_id = self.canvas_manager.select_line(event.x, event.y)
        if self.selected_line_id:
            self.settings_manager.selected_line_id = self.selected_line_id
            self.canvas_manager.selected_line_id = self.selected_line_id
            self.popup.post(event.x_root, event.y_root)
        else:
            self.selected_line_id = None

    def set_start_position(self, event: tk.Event) -> None:
        """
        Sets the starting position for operations such as drawing and moving objects based on the mouse event.

        :param event: The mouse event containing the coordinates where the action begins.
        """
        self.prev_x = event.x
        self.prev_y = event.y

    def copy_selected_object(self, event: tk.Event) -> None:
        """
        Copies the selected object based on the cursor location during the event.

        :param event: The mouse event that triggered the copy action.
        """
        selected_item = self.canvas_manager.select_line(event.x, event.y)
        if not selected_item:
            closest_items = self.canvas.find_closest(event.x, event.y)
            if closest_items:
                selected_item = closest_items[0]
            else:
                return
        self.file_manager.copy_object(selected_item)

    def paste_copied_object(self, event: tk.Event) -> None:
        """
        Pastes the copied object to the location specified by the cursor during the event.

        :param event: The mouse event that triggered the paste action.
        """
        self.file_manager.paste_object(event.x, event.y)

    def rotate_object(self, event: tk.Event) -> None:
        """
        Rotates the object closest to the cursor based on the current mouse location.

        :param event: The mouse event that triggered the rotation.
        """
        self.canvas_manager.rotate_object(event)
