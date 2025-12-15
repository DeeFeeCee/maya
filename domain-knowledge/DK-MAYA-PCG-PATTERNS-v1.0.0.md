---
title: "Maya Procedural Content Generation Patterns"
version: "1.0.0"
domain: "Maya Python PCG"
created: "2024-12-14"
description: "Patterns and techniques for procedural 3D content generation in Maya using Python"
---

# Maya Procedural Content Generation Patterns

## Overview

This domain knowledge captures patterns learned from building procedural generators for Maya, including starships, Star Wars fleets, and Minecraft characters.

## Core Architecture Pattern

### Generator Structure
```
Generator Module
├── Configuration Dictionaries (themes, types, colors)
├── Material Creation Functions
├── Part Builder Functions (primitives → components)
├── Assembly Functions (components → complete objects)
├── Group Creation Functions (objects → scenes)
└── UI Function (show_ui)
```

### Configuration-Driven Design
```python
THEMES = {
    "theme_name": {
        "name": "Display Name",
        "description": "User-facing description",
        "colors": {
            "primary": (r, g, b),
            "accent": (r, g, b),
            "glow": (r, g, b),
        },
        "special": "optional_modifier"
    }
}
```

**Benefits:**
- Easy to add new themes without code changes
- Self-documenting configuration
- UI can iterate over dict keys

## Material Pattern

### Standard Material Creation
```python
def create_material(name, color, emission=0.0):
    """Create Lambert material with optional glow."""
    shader = cmds.shadingNode('lambert', asShader=True, name=f"{name}_mat")
    sg = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=f"{name}_SG")
    cmds.connectAttr(f"{shader}.outColor", f"{sg}.surfaceShader", force=True)
    cmds.setAttr(f"{shader}.color", *color, type="double3")

    if emission > 0:
        cmds.setAttr(f"{shader}.incandescence",
                     color[0] * emission,
                     color[1] * emission,
                     color[2] * emission,
                     type="double3")
    return sg

def apply_material(obj, shading_group):
    """Apply material to object."""
    cmds.sets(obj, edit=True, forceElement=shading_group)
```

**Key Insight:** Create materials once, apply many times. Use naming convention `{name}_{part}_mat`.

## Primitive Composition Patterns

### Scale-Relative Sizing
```python
def build_component(name, scale=1.0):
    # All dimensions relative to scale parameter
    part = cmds.polyCube(w=0.5*scale, h=1.0*scale, d=0.3*scale)
    cmds.move(0, 0.5*scale, 0, part)  # Positions also scaled
```

### Symmetric Parts with Loops
```python
for side in [-1, 1]:
    wing = cmds.polyCube(w=2*scale, h=0.1*scale, d=0.5*scale)
    cmds.move(side * 1.5 * scale, 0, 0, wing)  # Mirror position
```

### Part Collection Pattern
```python
def build_ship(name, config, scale):
    parts = []

    # Create materials once
    hull_mat = create_material(f"{name}_hull", config["colors"]["primary"])

    # Build parts, append to list
    fuselage = cmds.polyCylinder(...)[0]
    apply_material(fuselage, hull_mat)
    parts.append(fuselage)

    # ... more parts ...

    return parts  # Return for grouping
```

## Formation Algorithms

### V-Formation
```python
for i in range(count):
    row = i // 2
    side = 1 if i % 2 == 0 else -1
    if i == 0:
        x, y, z = 0, 0, 0  # Leader at front
    else:
        x = -row * spacing
        z = side * row * spread
```

### Circle/Diamond Formation
```python
for i in range(count):
    if i == 0:
        x, z = 0, 0  # Center
    else:
        angle = ((i - 1) / (count - 1)) * 360
        x = radius * math.cos(math.radians(angle))
        z = radius * math.sin(math.radians(angle))
```

### Line Formation
```python
for i in range(count):
    x = i * spacing
    y, z = 0, 0
```

## UI Patterns

### Standard Window Structure
```python
def show_ui():
    window_name = "uniqueWindowName"

    if cmds.window(window_name, exists=True):
        cmds.deleteUI(window_name)

    window = cmds.window(window_name, title="Title", widthHeight=(400, 500))

    cmds.columnLayout(adjustableColumn=True, rowSpacing=10)

    # Sections with frameLayout
    cmds.frameLayout(label="Section", collapsable=True)
    cmds.columnLayout(adjustableColumn=True)
    # ... controls ...
    cmds.setParent("..")
    cmds.setParent("..")

    cmds.showWindow(window)
```

### Option Menu → Value Mapping
```python
# Create menu
menu = cmds.optionMenu()
cmds.menuItem(label="Display Name 1")
cmds.menuItem(label="Display Name 2")

# In callback, map display to value
def callback(*args):
    display = cmds.optionMenu(menu, q=True, value=True)
    value_map = {"Display Name 1": "value1", "Display Name 2": "value2"}
    actual_value = value_map[display]
```

## Launcher Script Pattern

### Structure
```python
"""
╔══════════════════════════════════════════════════════════════╗
║   TOOL NAME                                                  ║
╚══════════════════════════════════════════════════════════════╝

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 FUNCTION SIGNATURES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

function_name(param1, param2=default, ...)
    param1 : type - Description
    param2 : type - Description (default: value)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📝 USAGE EXAMPLES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Example code here...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⬇️ COPY CODE BELOW TO MAYA SCRIPT EDITOR ⬇️
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import sys
scripts_path = r"path/to/scripts"
if scripts_path not in sys.path:
    sys.path.insert(0, scripts_path)

import module_name
import importlib
importlib.reload(module_name)

from module_name import function1, function2, show_ui

# Quick start options (commented)
show_ui()
```

## Synapses

### High-Strength Connections
- [alex-game-designer.instructions.md] (Critical, Implements, Bidirectional) - "PCG expertise application"
- [bootstrap-learning.instructions.md] (High, Demonstrates, Forward) - "Teaching-focused code patterns"

### Medium-Strength Connections
- [DK-VISUAL-ARCHITECTURE-DESIGN-v0.9.9.md] (Medium, Applies, Forward) - "Visual hierarchy in 3D"
- [DK-DOCUMENTATION-EXCELLENCE-v1.1.0.md] (Medium, Demonstrates, Forward) - "Launcher documentation patterns"

### Contextual Activation
- Maya scripting tasks → Activate this knowledge
- Procedural generation requests → Apply composition patterns
- Teaching/tutorial creation → Use launcher documentation style

---

## Application Guidelines

1. **Start with configuration** - Define themes/types before code
2. **Build bottom-up** - Primitives → Parts → Assemblies → Scenes
3. **Scale everything** - Use relative dimensions for flexibility
4. **Collect parts in lists** - Easy grouping and cleanup
5. **Document in launchers** - Users need signatures and examples
6. **Provide UI** - Visual exploration accelerates learning
