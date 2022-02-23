# 2048

Tribute to the original game https://2048game.com

Project is created by Oleksii Hurov in Dec 2021
for educational purpose as well as part of portfolio.


## Technologies and programming methods learned during development

### Methods:
- Correct separating project's codebase into distinct modules.
- Parsing various format config-files (json, ini) and images (png).
- Distinct engine logic, which could be used separately.
- Division of project's modules to levels of abstraction:
    - (I) Data level abstraction - Data structures, types and interfaces;
    - (II) Input level abstraction - Predefined parameters and constants;
    - (III) Logic level abstraction - Logic, primary purpose and calculations;
    - (IV) Output level abstraction - Presentation, graphics & UI;
    - (V) Control level abstraction - Main program. Entry point.

### Technologies:
- Using scientific computing package "Numpy" for internal data storing.
- Applying external graphics module "Pygame" as an engine for output.
- Applying external graphics module "Pygame-gui" as an engine for UI.
- Dealing with events stack from keyboard and mouse as a source input.

### Coding:
- Widely using of docstrings and comments for better readability of code.
- Using type hinting generics for better readability of code.
- Composing Python classes as dataclasses, enums, type definitions, etc.
- No hard-coding. All the constants defined in separate configs.
- Mnemonic variables and functions names.
- Complete PEP 8 style compatibility.
- Main program entry point is not flooded with unnecessary code.


## Dependency on external modules and versions

* Python 3.9.5+
* numpy 1.21.4 (https://numpy.org)
* pygame 2.1.0 (https://www.pygame.org)
* pygame-gui 0.5.7 (https://pygame-gui.readthedocs.io)


## How to Use the Program

1. Open the project in any convenient Python IDE.
2. Install the following packages using pip: "numpy", "pygame" and "pygame-gui"
3. To adjust configuration for the game - edit parameters in the config.py
4. Run the project's main.py


## How to Play

Use your arrow keys to move the tiles.
When two tiles with the same number touch, they merge into one!


## Controls to Play
 
- Arrow keys (up, down, left, right) move the tiles to the corresponding border.
- Backspace key undo the last move.
- Esc key closes the program.


## Several screenshots from the project

![screenshot1.png](/screenshots/screenshot1.png)

![screenshot2.png](/screenshots/screenshot2.png)

![screenshot2_alternative.png](/screenshots/screenshot2_alternative.png)

![screenshot3.png](/screenshots/screenshot3.png)

![screenshot4.png](/screenshots/screenshot4.png)
