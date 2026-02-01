from typing import Any


class ToolManager:
    """
    Manages tool interactions and modes within the application, coordinating with event and canvas managers.
    """
    def __init__(self, event_handler: Any, canvas_manager: Any, canvas) -> None:
        """
        Initialize the ToolManager with necessary handlers and canvas.

        :param event_handler: The handler responsible for managing events.
        :param canvas_manager: The manager responsible for direct canvas manipulations.
        :param canvas: The canvas object where drawing operations are performed.
        """
        self.event_handler: Any = event_handler
        self.canvas_manager: Any = canvas_manager
        self.canvas = canvas

    def set_mode(self, mode: str) -> None:
        """
        Sets the operational mode for tools and updates event handling accordingly.

        :param mode: A string representing the mode to be set (e.g., 'circle', 'rectangle', 'eraser').
        """
        self.event_handler.mode = mode
        self.canvas_manager.mode = mode
        self.event_handler.update_mouse_events()

    def enable_draw_circle(self) -> None:
        """
        Activates the mode for drawing circles.
        """
        self.set_mode("circle")

    def enable_draw_rectangle(self) -> None:
        """
        Activates the mode for drawing rectangles.
        """
        self.set_mode("rectangle")

    def enable_draw_triangle(self) -> None:
        """
        Activates the mode for drawing triangles.
        """
        self.set_mode("triangle")

    def enable_draw_polygon(self) -> None:
        """
        Activates the mode for drawing polygons and initializes the polygon point list.
        """
        self.canvas_manager.polygon_points = []
        self.set_mode("polygon")

    def enable_eraser(self, size: int) -> None:
        """
        Activates the eraser tool and sets its size.

        :param size: The size of the eraser tool.
        """
        self.canvas_manager.eraser_size = size
        self.set_mode("eraser")

    def enable_draw(self) -> None:
        """
        Sets the mode to free-form drawing.
        """
        self.set_mode("draw")

    def enable_Remove(self) -> None:
        """
        Sets the mode to remove graphical objects from the canvas.
        """
        self.set_mode("Remove")

    def enable_move(self) -> None:
        """
        Activates the move tool, allowing for the repositioning of graphical objects.
        """
        self.set_mode("move")

    def enable_text(self) -> None:
        """
        Activates the text tool, enabling text input on the canvas.
        """
        self.set_mode("text")
        self.event_handler.mode = "text"
        self.canvas.bind("<Button-1>", self.event_handler.text_input)

    def enable_copy(self) -> None:
        """
        Activates the copy tool to copy graphical objects.
        """
        self.set_mode("copy")

    def enable_paste(self) -> None:
        """
        Activates the paste tool to paste copied graphical objects.
        """
        self.set_mode("paste")

    def enable_rotate(self) -> None:
        """
        Activates the rotate tool and sets up event handling for object rotation.
        """
        self.set_mode("rotate")
        self.canvas.bind("<Button-1>", self.event_handler.rotate_object)
