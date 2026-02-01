import tkinter as tk
import math
from typing import List, Dict, Optional, Any, Tuple


class CanvasManager:
    """
    Manages all canvas operations including drawing, moving, and deleting graphical objects.
    """
    def __init__(self, canvas: tk.Canvas, line_id_to_segments: Dict[int, List[int]], settings_manager: Any, lines: List[List[int]]) -> None:
        """
        Initializes the CanvasManager with necessary references.

        :param canvas: The canvas on which all drawings are made.
        :param line_id_to_segments: Dictionary mapping line IDs to their respective segments.
        :param settings_manager: Manages settings such as line width and color.
        :param lines: List of all line segments.
        """
        self.canvas: tk.Canvas = canvas
        self.start_x: Optional[int] = None
        self.start_y: Optional[int] = None
        self.current_circle: Optional[int] = None
        self.current_rectangle: Optional[int] = None
        self.current_triangle: Optional[int] = None
        self.polygon_points: List[Tuple[int, int]] = []
        self.current_line_segments: List[int] = []
        self.lines: List[List[int]] = lines
        self.line_id_to_segments: Dict[int, List[int]] = line_id_to_segments
        self.prev_x: Optional[int] = None
        self.prev_y: Optional[int] = None
        self.selected_line_id: Optional[int] = None
        self.eraser_size: int = 0
        self.moving_line_segments: List[int] = []
        self.mode: Optional[str] = None
        self.settings_manager: Any = settings_manager

    def set_event_handler(self, event_handler: Any) -> None:
        """
        Associates an event handler with the canvas manager.

        :param event_handler: The event handler to associate.
        """
        self.event_handler = event_handler

    def start_circle(self, event: tk.Event) -> None:
        """
        Begins the process of drawing a circle using the initial mouse event coordinates.

        :param event: The mouse event with the initial coordinates.
        """
        self.start_x = event.x
        self.start_y = event.y
        self.current_circle = None

    def draw_circle(self, event: tk.Event) -> None:
        """
        Continuously updates the circle's dimensions as the mouse moves.

        :param event: The mouse event with the current coordinates.
        """
        if self.current_circle:
            self.canvas.delete(self.current_circle)
        radius = ((event.x - self.start_x) ** 2 + (event.y - self.start_y) ** 2) ** 0.5
        self.current_circle = self.canvas.create_oval(
            self.start_x - radius, self.start_y - radius,
            self.start_x + radius, self.start_y + radius,
            outline="",fill="black", width=self.settings_manager.current_line_width
        )

    def finish_circle(self, event: tk.Event) -> None:
        """
        Finalizes the circle drawing, stores its reference, and resets the temporary circle storage.

        :param event: The mouse event when the drawing is completed.
        """
        if self.current_circle:
            self.canvas.delete(self.current_circle)
        radius = ((event.x - self.start_x) ** 2 + (event.y - self.start_y) ** 2) ** 0.5
        circle_id = self.canvas.create_oval(
            self.start_x - radius, self.start_y - radius,
            self.start_x + radius, self.start_y + radius,
            outline="",fill="black", width=self.settings_manager.current_line_width
        )
        self.line_id_to_segments[circle_id] = [circle_id]
        self.current_circle = None

    def start_rectangle(self, event: tk.Event) -> None:
        """
        Initiates the drawing of a rectangle based on the starting mouse event coordinates.

        :param event: The mouse event with the initial coordinates.
        """
        self.start_x = event.x
        self.start_y = event.y
        self.current_rectangle = None

    def draw_rectangle(self, event: tk.Event) -> None:
        """
        Dynamically updates the rectangle dimensions as the mouse is dragged.

        :param event: The mouse event with the current coordinates.
        """
        if self.current_rectangle:
            self.canvas.delete(self.current_rectangle)
        side_length = min(abs(event.x - self.start_x), abs(event.y - self.start_y))
        sign_x = 1 if event.x >= self.start_x else -1
        sign_y = 1 if event.y >= self.start_y else -1
        self.current_rectangle = self.canvas.create_rectangle(
            self.start_x, self.start_y,
            self.start_x + sign_x * side_length, self.start_y + sign_y * side_length,
            outline="", fill="black", width=self.settings_manager.current_line_width
        )

    def finish_rectangle(self, event: tk.Event) -> None:
        """
        Completes the rectangle drawing, saves its reference, and resets the temporary rectangle storage.

        :param event: The mouse event when the drawing is completed.
        """
        if self.current_rectangle:
            self.canvas.delete(self.current_rectangle)
        side_length = min(abs(event.x - self.start_x), abs(event.y - self.start_y))
        sign_x = 1 if event.x >= self.start_x else -1
        sign_y = 1 if event.y >= self.start_y else -1
        rectangle_id = self.canvas.create_rectangle(
            self.start_x, self.start_y,
            self.start_x + sign_x * side_length, self.start_y + sign_y * side_length,
            outline="", fill="black", width=self.settings_manager.current_line_width
        )
        self.line_id_to_segments[rectangle_id] = [rectangle_id]
        self.current_rectangle = None

    def start_triangle(self, event: tk.Event) -> None:
        """
        Initiates the drawing of a triangle with the first mouse click defining the apex.

        :param event: The mouse event with the initial coordinates.
        """
        self.start_x = event.x
        self.start_y = event.y
        self.current_triangle = None

    def draw_triangle(self, event: tk.Event) -> None:
        """
        Dynamically updates the triangle shape as the mouse moves.

        :param event: The mouse event with the current coordinates.
        """
        if self.current_triangle:
            self.canvas.delete(self.current_triangle)
        height = ((event.x - self.start_x) ** 2 + (event.y - self.start_y) ** 2) ** 0.5  # מרחק מהנקודה הראשונה
        apex_x = self.start_x
        apex_y = self.start_y - height
        left_base_x = self.start_x - height / 2
        left_base_y = self.start_y
        right_base_x = self.start_x + height / 2
        right_base_y = self.start_y
        self.current_triangle = self.canvas.create_polygon(
            [apex_x, apex_y, left_base_x, left_base_y, right_base_x, right_base_y],
            outline="", fill="black", width=self.settings_manager.current_line_width
        )

    def finish_triangle(self, event: tk.Event) -> None:
        """
        Finalizes the triangle drawing, saves its reference, and resets the temporary triangle storage.

        :param event: The mouse event when the drawing is completed.
        """
        if self.current_triangle:
            self.canvas.delete(self.current_triangle)
        height = ((event.x - self.start_x) ** 2 + (event.y - self.start_y) ** 2) ** 0.5
        apex_x = self.start_x
        apex_y = self.start_y - height
        left_base_x = self.start_x - height / 2
        left_base_y = self.start_y
        right_base_x = self.start_x + height / 2
        right_base_y = self.start_y
        triangle_id = self.canvas.create_polygon(
            [apex_x, apex_y, left_base_x, left_base_y, right_base_x, right_base_y],
            outline="", fill="black", width=self.settings_manager.current_line_width
        )
        self.line_id_to_segments[triangle_id] = [triangle_id]
        self.current_triangle = None

    def add_polygon_point(self, event: tk.Event) -> None:
        """
        Adds a point to the current polygon and draws a line segment to the previous point if applicable.

        :param event: The mouse event with the current coordinates.
        """
        self.polygon_points.append((event.x, event.y))
        if len(self.polygon_points) > 1:
            self.canvas.create_line(self.polygon_points[-2], self.polygon_points[-1], fill="",
                                    width=self.settings_manager.current_line_width)

    def finish_polygon(self, event: tk.Event) -> None:
        """
        Closes the polygon drawing, creates a filled shape, and clears the temporary drawing lines.

        :param event: The mouse event when the drawing is completed.
        """
        if len(self.polygon_points) > 2:
            polygon_id = self.canvas.create_polygon(self.polygon_points, outline="", fill="black",
                                                    width=self.settings_manager.current_line_width)
            self.line_id_to_segments[polygon_id] = [polygon_id]

        self.polygon_points = []
        self.delete_polygon_lines()  # Call the function to delete the drawing lines

    def delete_polygon_lines(self) -> None:
        """
        Deletes all temporary line segments used for drawing the polygon.
        """
        for segment in self.current_line_segments:
            self.canvas.delete(segment)
        self.current_line_segments.clear()  # Clear the list after deleting the segments

    def restart_canvas(self) -> None:
        """
        Clears all drawings from the canvas and resets all associated data structures.
        """
        self.canvas.delete("all")
        self.lines.clear()
        self.current_line_segments.clear()
        self.moving_line_segments.clear()
        self.line_id_to_segments.clear()

    def move_forward(self) -> None:
        """
        Raises the selected graphical object one layer up in the stack.
        """
        if self.selected_line_id and self.selected_line_id in self.line_id_to_segments:
            segments_to_raise = self.line_id_to_segments[self.selected_line_id]
            for segment in segments_to_raise:
                self.canvas.tag_raise(segment, None)

    def move_backward(self) -> None:
        """
        Lowers the selected graphical object one layer down in the stack.
        """
        if self.selected_line_id and self.selected_line_id in self.line_id_to_segments:
            segments_to_lower = self.line_id_to_segments[self.selected_line_id]
            for segment in segments_to_lower:
                self.canvas.tag_lower(segment, None)

    def eraser(self, event) -> None:
        """
        Erases graphical objects within a specified area around the cursor.

        :param event: The mouse event with the current coordinates.
        """
        x1, y1 = (event.x - self.eraser_size), (event.y - self.eraser_size)
        x2, y2 = (event.x + self.eraser_size), (event.y + self.eraser_size)
        items = self.canvas.find_overlapping(x1, y1, x2, y2)
        for item in items:
            if item in self.line_id_to_segments:
                self.remove_segment(item)

    def remove_segment(self, item) -> None:
        """
        Removes a specific graphical object and updates the associated data structures.

        :param item: The item ID of the segment to remove.
        """
        if item in self.line_id_to_segments:
            self.canvas.delete(item)
            segments = self.line_id_to_segments.pop(item, [])
            if segments:
                index = segments.index(item)
                before_segments = segments[:index]
                after_segments = segments[index + 1:]

                if before_segments:
                    self.lines.append(before_segments)
                    for seg in before_segments:
                        self.line_id_to_segments[seg] = before_segments

                if after_segments:
                    self.lines.append(after_segments)
                    for seg in after_segments:
                        self.line_id_to_segments[seg] = after_segments

    def draw(self, event: tk.Event) -> None:
        """
        Draws a line segment between the previous and current mouse positions.

        :param event: The mouse event with the current coordinates.
        """
        if self.prev_x is not None and self.prev_y is not None:
            line = self.canvas.create_line(self.prev_x, self.prev_y, event.x, event.y, fill="black", width=self.settings_manager.current_line_width)
            self.current_line_segments.append(line)
            self.prev_x = event.x
            self.prev_y = event.y

    def on_mouse_down(self, event: tk.Event) -> None:
        """
        Handles mouse down events, initiating drawing or moving operations.

        :param event: The mouse event with the starting coordinates.
        """
        self.prev_x = event.x
        self.prev_y = event.y
        selected_line = self.select_line(event.x, event.y)
        if selected_line:
            self.selected_line_id = selected_line  # Update the selected line ID
            if self.mode == "move":
                self.moving_line_segments = self.line_id_to_segments.get(selected_line, [])
            elif self.mode == "Remove":
                self.Remove_continuous_line(selected_line)
                self.moving_line_segments = []

    def on_mouse_move(self, event: tk.Event) -> None:
        """
        Handles mouse move events, updating positions or continuing to draw based on the mode.

        :param event: The mouse event with the current coordinates.
        """
        if self.prev_x is not None and self.prev_y is not None:
            dx = event.x - self.prev_x
            dy = event.y - self.prev_y
            if self.mode == "move" and self.moving_line_segments:
                for line_id in self.moving_line_segments:
                    self.canvas.move(line_id, dx, dy)
                self.prev_x = event.x
                self.prev_y = event.y
            elif self.mode == "draw":
                line = self.canvas.create_line(self.prev_x, self.prev_y, event.x, event.y, fill="black",
                                               width=self.settings_manager.current_line_width)
                self.current_line_segments.append(line)
                self.prev_x = event.x
                self.prev_y = event.y

    def on_mouse_release(self, event: tk.Event) -> None:
        """
        Handles mouse release events, finalizing drawing or moving operations.
        """
        if self.mode == "move":
            for line_id in self.moving_line_segments:
                final_coords = self.canvas.coords(line_id)
            self.moving_line_segments = []
        elif self.mode == "draw":
            self.lines.append(self.current_line_segments.copy())
            for segment in self.current_line_segments:
                self.line_id_to_segments[segment] = self.current_line_segments.copy()
            self.current_line_segments = []

    def select_line(self, x: int, y: int) -> Optional[int]:
        """
        Selects a line based on proximity to the given coordinates.

        :param x: The x-coordinate.
        :param y: The y-coordinate.
        :return: The ID of the selected line, or None if no line is found.
        """
        items = self.canvas.find_overlapping(x - 1, y - 1, x + 1, y + 1)
        for item in items:
            if item in self.line_id_to_segments:
                print(f"select_line: item={item} found and selected, segments={self.line_id_to_segments[item]}")
                return item
        print("select_line: No item found")
        return None

    def Remove_continuous_line(self, line_id: int) -> None:
        """
        Removes a continuous line from the canvas and updates data structures accordingly.

        :param line_id: The ID of the line to remove.
        """
        segments = self.line_id_to_segments.pop(line_id, None)
        if segments is not None:
            if segments in self.lines:
                self.lines.remove(segments)
            for segment in segments:
                self.canvas.delete(segment)

    def rotate_object(self, event: tk.Event) -> None:
        """
        Rotates an object around its center based on the provided event coordinates.

        :param event: The mouse event with the coordinates used for the center of rotation.
        """
        item = self.canvas.find_closest(event.x, event.y)[0]
        if item:
            angle = math.radians(90)
            item_type = self.canvas.type(item)

            if item_type == "line":
                all_segments = self.line_id_to_segments.get(item, [])
                for segment in all_segments:
                    coords = self.canvas.coords(segment)
                    if len(coords) % 4 == 0:
                        new_coords = []
                        for i in range(0, len(coords), 2):
                            x, y = coords[i], coords[i + 1]
                            new_x, new_y = self._rotate_point(x, y, event.x, event.y, angle)
                            new_coords.extend([new_x, new_y])
                        self.canvas.coords(segment, *new_coords)

            elif item_type in ["oval", "rectangle", "text"]:
                # Rotation is not defined for ovals, rectangles, or text.
                pass

            elif item_type == "polygon":
                coords = self.canvas.coords(item)
                centroid_x = sum(coords[::2]) / (len(coords) / 2)
                centroid_y = sum(coords[1::2]) / (len(coords) / 2)
                new_coords = []
                for i in range(0, len(coords), 2):
                    new_x, new_y = self._rotate_point(coords[i], coords[i + 1], centroid_x, centroid_y, angle)
                    new_coords.extend([new_x, new_y])
                self.canvas.coords(item, *new_coords)

    def _rotate_point(self, x: float, y: float, cx: float, cy: float, angle: float) -> Tuple[float, float]:
        """
        Calculates the new coordinates of a point after rotation around a given center.

        :param x: The original x-coordinate of the point.
        :param y: The original y-coordinate of the point.
        :param cx: The x-coordinate of the center of rotation.
        :param cy: The y-coordinate of the center of rotation.
        :param angle: The angle of rotation in radians.
        :return: The new x and y coordinates after rotation.
        """
        new_x = cx + math.cos(angle) * (x - cx) - math.sin(angle) * (y - cy)
        new_y = cy + math.sin(angle) * (x - cx) + math.cos(angle) * (y - cy)
        return new_x, new_y
