# Vector Graphics Editor (Tkinter)

A lightweight **vector graphics editor** built with **Python + Tkinter**, designed for creating and manipulating simple vector shapes on a canvas. The project focuses on a clean, modular architecture (manager-based design) and event-driven UI interactions.

## Features

- **Freehand drawing** with adjustable line width.
- Draw **circle, rectangle, triangle, and polygon** shapes.
- Add **text** with configurable **font family, size, and color**.
- **Move** objects by dragging.
- **Rotate** (90°) supported for lines and polygons.
- **Copy / paste** objects to a new location.
- **Erase** with small/large eraser, or **remove** an entire continuous line.
- **Layer ordering**: bring forward / move backward.
- **Save / load** drawings as **JSON**.
- **Export** the canvas as an image (**PNG / JPEG / GIF**).

## Project Structure

- `main.py` – application entry-point, creates the Tk root and wires all managers together.
- `UIManager.py` – builds the GUI: tool panels, buttons, sliders, and the right-click context menu.
- `ToolManager.py` – switches tool “modes” (draw/move/shape/text/erase/copy/paste/rotate) and updates bindings.
- `EventHandler.py` – centralizes mouse-event bindings based on the current mode.
- `CanvasManager.py` – core drawing + editing logic on the Tk canvas (create shapes, move, erase, rotate, layering).
- `TextManager.py` – text dialog + placement and tracking per-text font settings.
- `SettingsManager.py` – line width + color settings (and text size changes via context menu).
- `FileManager.py` – persistence & export: save/load to JSON, export to image, copy/paste implementation.

## Tech Stack

- **Python**
- **Tkinter** (GUI)
- **Pillow (PIL)** for image export (`ImageGrab`)
- Type hints throughout the codebase (`typing`)

## Getting Started

### 1) Create & activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
# .venv\Scripts\activate  # Windows
```

### 2) Install dependencies

```bash
pip install -r requirements.txt
```

### 3) Run the application

```bash
python main.py
```

## How to Use

### Drawing & editing
- Use the buttons on the left panel to switch modes (Draw, Move, Shapes, Text, Copy/Paste, Rotate, etc.).
- **Line Width**: adjust via the slider.
- **Right-click** an object to open a context menu:
  - quick sizes
  - colors
  - bring forward / move backward

### Polygon tool
- Click multiple points to define a polygon.
- Double-click to finish and close the polygon.

### Save / Load
- **Save** writes the canvas objects into a JSON file (coordinates + styling).
- **Load** rebuilds objects from the saved JSON.

### Export
- **Export** captures the canvas area and saves it as an image (PNG/JPEG/GIF).

## Programming Skills Demonstrated 

- **Object-Oriented Design & separation of concerns**: distinct manager classes for UI, tools, events, canvas logic, settings, text, and file I/O.
- **Event-driven programming**: dynamic binding/unbinding of mouse handlers based on the active tool mode.
- **State management**: internal tracking of selected items, grouped line segments, and per-object metadata.
- **Data modeling & serialization**: custom JSON format to persist and restore drawings.
- **GUI engineering**: multi-panel Tk layout, context menus, sliders, and dialogs.
- **Practical graphics operations**: geometric calculations, hit-testing, layering, and canvas coordinate manipulation.
- **Type annotations**: consistent use of `typing` for maintainability and clarity.

---

**Author:** Ofek Farkash
