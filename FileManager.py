from tkinter import filedialog
from PIL import Image, ImageGrab
import json
import tkinter.font as font
from typing import List, Dict, Optional, Any, Tuple, Callable


class FileManager:
    """
    Manages file operations such as save, load, export, copy, and paste for the graphical objects on the canvas.
    """

    def __init__(self, canvas, line_id_to_segments: Dict[int, List[int]], lines: List[List[int]], settings_manager: Any) -> None:
        """
        Initializes the FileManager with the canvas and associated data structures.

        :param canvas: The canvas object where the drawings are rendered.
        :param line_id_to_segments: A dictionary mapping line IDs to their respective segments.
        :param lines: A list of all lines drawn on the canvas.
        :param settings_manager: The manager for application settings.
        """
        self.canvas = canvas
        self.line_id_to_segments: Dict[int, List[int]] = line_id_to_segments
        self.lines: List[List[int]] = lines
        self.copied_object: Optional[Dict[str, Any]] = None
        self.settings_manager: Any = settings_manager



    def export_canvas(self) -> None:
        """
        Exports the current canvas view as an image file.
        """
        default_file_type = [('JPEG files', '*.jpeg'), ('PNG files', '*.png'), ('GIF files', '*.gif')]
        file_path: str = filedialog.asksaveasfilename(defaultextension='.jpeg', filetypes=default_file_type,
                                                 title="Save as...")

        if file_path:
            x: int = self.canvas.winfo_rootx()
            y: int = self.canvas.winfo_rooty()
            x1: int = x + self.canvas.winfo_width()
            y1: int = y + self.canvas.winfo_height()
            img = ImageGrab.grab().crop((x, y, x1, y1))
            img.save(file_path)

    def save_drawing(self) -> None:
        """
        Saves the current drawing to a JSON file, which includes all graphical objects.
        """
        file_path: str = filedialog.asksaveasfilename(defaultextension='.json', filetypes=[('JSON files', '*.json')],
                                                 title="Save drawing as...")
        if file_path:
            objects: List[Dict[str, Any]] = []
            for line_segments in self.lines:
                line_data = {'type': 'line', 'coords': [], 'width': self.canvas.itemcget(line_segments[0], 'width'),
                             'fill': self.canvas.itemcget(line_segments[0], 'fill')}
                for segment in line_segments:
                    line_data['coords'].extend(self.canvas.coords(segment))
                objects.append(line_data)
            for item in self.canvas.find_all():
                obj_type = self.canvas.type(item)
                if obj_type not in ['line']:
                    obj_data = {
                        'type': obj_type,
                        'coords': self.canvas.coords(item),
                        'width': self.canvas.itemcget(item, 'width'),
                        'fill': self.canvas.itemcget(item, 'fill')
                    }
                    if obj_type in ['oval', 'rectangle', 'polygon']:
                        obj_data['outline'] = self.canvas.itemcget(item, 'outline')
                    elif obj_type == 'text':
                        obj_data['text'] = self.canvas.itemcget(item, 'text')
                        font_info = self.canvas.itemcget(item, 'font')
                        if font_info:
                            font_obj = font.Font(font=font_info)
                            obj_data['font'] = {'family': font_obj.actual()['family'],
                                                'size': font_obj.actual()['size']}
                    objects.append(obj_data)
            with open(file_path, 'w') as f:
                json.dump(objects, f, indent=4)

    def load_drawing(self) -> None:
        """
        Loads a drawing from a JSON file and recreates the graphical objects on the canvas.
        """
        file_path: str = filedialog.askopenfilename(filetypes=[('JSON files', '*.json')], title="Load drawing")
        if file_path:
            with open(file_path, 'r') as f:
                objects: List[Dict[str, Any]] = json.load(f)
            self.canvas.delete("all")
            self.line_id_to_segments.clear()

            for obj in objects:
                coords = obj['coords']
                if obj['type'] == 'line':
                    line_id = self.canvas.create_line(coords, fill=obj['fill'], width=obj['width'])
                    self.line_id_to_segments[line_id] = [line_id]
                elif obj['type'] in ['oval', 'rectangle', 'polygon']:
                    create_func = getattr(self.canvas, f'create_{obj["type"]}')
                    shape_id = create_func(coords, outline=obj.get('outline', ''), fill=obj['fill'], width=obj['width'])
                    self.line_id_to_segments[shape_id] = [shape_id]
                elif obj['type'] == 'text':
                    font_properties = (obj['font']['family'], int(obj['font']['size']))
                    font_obj = font.Font(family=font_properties[0], size=font_properties[1])
                    text_id = self.canvas.create_text(coords, text=obj['text'], font=font_obj, fill=obj['fill'])
                    self.line_id_to_segments[text_id] = [text_id]
                    self.settings_manager.text_fonts[text_id] = (obj['font']['family'], int(obj['font']['size']), obj['fill'])

    def copy_object(self, object_id: int):
        """
        Copies the properties of the selected object for later pasting.

        :param object_id: The ID of the object to copy.
        """
        if object_id:
            obj_type: str = self.canvas.type(object_id)
            coords: List[float] = self.canvas.coords(object_id)
            properties: Dict[str, Any] = {
                'type': obj_type,
                'coords': coords,
                'width': self.canvas.itemcget(object_id, 'width'),
                'fill': self.canvas.itemcget(object_id, 'fill')
            }
            if obj_type in ['oval', 'rectangle', 'polygon']:
                properties['outline'] = self.canvas.itemcget(object_id, 'outline')
            elif obj_type == 'text':
                properties['text'] = self.canvas.itemcget(object_id, 'text')
                font_info = self.canvas.itemcget(object_id, 'font')
                if font_info:
                    font_obj = font.Font(font=font_info)
                    properties['font'] = {'family': font_obj.actual()['family'],
                                          'size': font_obj.actual()['size']}
            self.copied_object = properties
            if obj_type == 'line':
                all_related_segments = self.line_id_to_segments.get(object_id, [])
                coords = []
                for segment in all_related_segments:
                    coords.extend(self.canvas.coords(segment))
                properties['coords'] = coords


    def paste_object(self, x: int, y: int) -> None:
        """
        Pastes the copied object to a new location on the canvas.

        :param x: The x-coordinate of the new location.
        :param y: The y-coordinate of the new location.
        """
        if self.copied_object:
            obj_type: str = self.copied_object['type']
            create_func: Callable = getattr(self.canvas, f'create_{obj_type}')
            new_coords: List[float] = []

            if obj_type == 'text':
                font_properties: Tuple[str, int] = (self.copied_object['font']['family'], int(self.copied_object['font']['size']))
                font_obj = font.Font(family=font_properties[0], size=font_properties[1])
                item_id = self.canvas.create_text(x, y, text=self.copied_object['text'],
                                                  font=font_obj, fill=self.copied_object['fill'])
                self.line_id_to_segments[item_id] = [item_id]
                self.settings_manager.text_fonts[item_id] = (
                font_properties[0], font_properties[1], self.copied_object['fill'])

            elif obj_type in ['polygon', 'triangle']:
                original_coords: List[float] = self.copied_object['coords']
                coord_diff_x: float = x - original_coords[0]
                coord_diff_y: float = y - original_coords[1]
                new_coords = [coord + (coord_diff_x if i % 2 == 0 else coord_diff_y) for i, coord in
                              enumerate(original_coords)]
                item_id = create_func(new_coords, outline=self.copied_object.get('outline', ''),
                                      fill=self.copied_object['fill'], width=self.copied_object['width'])

            elif obj_type == 'line':
                original_coords: List[float] = self.copied_object['coords']
                dx: float = x - original_coords[0]
                dy: float = y - original_coords[1]
                for i in range(0, len(original_coords), 4):
                    new_coords.extend([original_coords[i] + dx, original_coords[i+1] + dy, original_coords[i+2] + dx, original_coords[i+3] + dy])
                item_id = create_func(new_coords, fill=self.copied_object['fill'], width=self.copied_object['width'])
                self.line_id_to_segments[item_id] = [item_id]
                self.lines.append([item_id])

            else:
                original_coords: List[float] = self.copied_object['coords']
                width: float = original_coords[2] - original_coords[0]
                height: float = original_coords[3] - original_coords[1]
                new_coords = [x - width / 2, y - height / 2, x + width / 2, y + height / 2]
                item_id = create_func(new_coords, outline=self.copied_object['outline'],
                                      fill=self.copied_object['fill'], width=self.copied_object['width'])
                self.line_id_to_segments[item_id] = [item_id]
