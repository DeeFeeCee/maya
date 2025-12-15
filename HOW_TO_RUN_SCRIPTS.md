# 🚀 How to Run Scripts in Maya

This guide explains how to load and execute the Python scripts from this repository in Autodesk Maya.

---

## 📋 Prerequisites

- **Autodesk Maya 2022+** (Python 3 support)
- Scripts from this repository downloaded to your computer

---

## 🎯 Method 1: Use Launcher Scripts (Recommended)

The easiest way! Use the pre-made launcher scripts in the `launchers/` folder.

### Steps:

1. **Open a launcher file** in VS Code or any text editor (e.g., `launchers/RUN_STARSHIP_V1.py`)
2. **Copy everything below the dashed line** (`# ----------- COPY EVERYTHING BELOW THIS LINE -----------`)
3. **In Maya**, open the **Script Editor**:
   - Menu: `Windows → General Editors → Script Editor`
   - Or press the `{;}` button in the bottom-right corner
4. **Click the Python tab** at the bottom of the Script Editor
5. **Paste** (`Ctrl+V`) the code
6. **Run** by pressing `Ctrl+Enter` or clicking the ▶️ Play button

### Available Launchers:

| Launcher | Description |
|----------|-------------|
| `RUN_STARSHIP_V1.py` | Starship Generator V1 - Classic edition |
| `RUN_STARSHIP_V2.py` | Starship Generator V2 - Advanced with squadrons |
| `RUN_STARWARS_FLEET.py` | ⭐ Star Wars Fleet Generator - X-Wings, TIEs & more! |
| `RUN_MINECRAFT.py` | 🟫 Minecraft Characters - Steve, Creeper & more! |
| `RUN_3D_TEXT.py` | 3D Text Generator V2 - Type tool version |
| `RUN_3D_TEXT_V1.py` | 3D Text Generator V1 - textCurves version |
| `RUN_FONT_DIAGNOSTIC.py` | Font troubleshooting utility |
| `RUN_IN_MAYA.py` | Quick launcher for Starship V1 |

Each launcher includes full function signatures, usage examples, and options reference!

---

## 🎯 Method 2: Execute File Directly

Run a launcher or script file without copying its contents.

### In the Script Editor (Python tab):

```python
# Run a launcher (recommended)
exec(open(r"C:\Development\maya\launchers\RUN_STARSHIP_V1.py").read())

# Or run a script directly
exec(open(r"C:\Development\maya\scripts\starship.py").read())
```

### Then call functions:

```python
# Starship Generator
show_ui()
create_starship("my_ship", "fighter", "rebel")
create_fleet(5, "v")

# 3D Text Generator
hello_world()
create_3d_text("MAYA ROCKS", color_preset="fire")
```

---

## 🎯 Method 3: Add to Maya's Script Path (Recommended for Regular Use)

This method lets you import scripts like regular Python modules.

### Step 1: Create/Edit userSetup.py

Create a file called `userSetup.py` in your Maya scripts folder:

| OS | Location |
|----|----------|
| **Windows** | `C:\Users\<username>\Documents\maya\<version>\scripts\userSetup.py` |
| **macOS** | `~/Library/Preferences/Autodesk/maya/<version>/scripts/userSetup.py` |
| **Linux** | `~/maya/<version>/scripts/userSetup.py` |

### Step 2: Add This Code to userSetup.py

```python
import sys
import maya.utils

# Add your scripts folder to Maya's Python path
SCRIPT_PATHS = [
    r"C:\Development\maya\scripts",  # Change this to your path!
]

for path in SCRIPT_PATHS:
    if path not in sys.path:
        sys.path.insert(0, path)

def startup_message():
    print("✨ Custom scripts loaded from: C:\\Development\\maya\\scripts")

maya.utils.executeDeferred(startup_message)
```

### Step 3: Restart Maya

After restarting, you can import scripts directly:

```python
# Starship Generator V1
import starship
starship.show_ui()
starship.create_starship("x_wing", "fighter", "rebel")
starship.create_fleet(5, "v")

# Starship Generator V2
import starship_v2
starship_v2.show_ui()
starship_v2.create_starship("red_five", "interceptor", "federation")
starship_v2.create_squadron(5, "interceptor", "federation", "v")

# 3D Text Generator
import fancy_3d_text_v2
fancy_3d_text_v2.show_ui()
fancy_3d_text_v2.create_3d_text("AWESOME", color_preset="neon")
```

---

## 🎯 Method 4: Create a Shelf Button

Add a button to Maya's shelf for one-click access.

### How to Create a Shelf Button

1. **Open the Script Editor** and enter your script or import code
2. **Select the code** you want to save
3. **Middle-mouse drag** the selected code to a shelf tab
4. A new button appears! Click it anytime to run the script

### Example Shelf Button Code

```python
# Starship Generator
import starship
starship.show_ui()

# Or 3D Text
import fancy_3d_text_v2
fancy_3d_text_v2.show_ui()
```

### Customize the Button

- **Right-click** the shelf button → `Edit`
- Change the **icon** and **tooltip**
- Add a **label** for easy identification

---

## 📂 Quick Reference - All Scripts

### 🛸 Starship Generator V1 (`scripts/starship.py`)

```python
exec(open(r"C:\Development\maya\launchers\RUN_STARSHIP_V1.py").read())
```

| Function | Description |
|----------|-------------|
| `create_starship(name, ship_type, color_scheme, scale, add_animation)` | Create a starship |
| `create_fleet(count, formation)` | Create multiple ships in formation |
| `show_ui()` | Open the UI window |

**Color Schemes:** `classic`, `rebel`, `imperial`, `pirate`, `alien`
**Ship Types:** `fighter`, `scout`, `bomber`, `cruiser`
**Formations:** `line`, `v`, `diamond`, `random`

### 🚀 Starship Generator V2 (`scripts/starship_v2.py`)

```python
exec(open(r"C:\Development\maya\launchers\RUN_STARSHIP_V2.py").read())
```

| Function | Description |
|----------|-------------|
| `create_starship(name, ship_class, theme, scale, add_animation, animation_style)` | Create detailed ship |
| `create_squadron(count, ship_class, theme, formation)` | Create a squadron |
| `show_ui()` | Open the advanced UI |

**Themes:** `federation`, `empire`, `bounty_hunter`, `alien`, `stealth`, `racer`
**Ship Classes:** `interceptor`, `heavy_fighter`, `racer`
**Formations:** `v`, `line`, `diamond`, `echelon`
**Animation Styles:** `hover`, `flyby`, `banking`

### ⭐ Star Wars Fleet Generator (`scripts/starwars_fleet.py`)

```python
exec(open(r"C:\Development\maya\launchers\RUN_STARWARS_FLEET.py").read())
```

| Function | Description |
|----------|-------------|
| `create_ship(ship_type, name, scale, position)` | Create iconic ships |
| `create_fleet(faction, count, formation)` | Create faction fleets |
| `show_ui()` | Open the Star Wars UI |

**Ship Types:** `xwing`, `tie`, `ywing`, `awing`, `falcon`, `shuttle`, `interceptor`, `slave1`
**Factions:** `rebel`, `imperial`, `mixed`, `bounty_hunter`
**Formations:** `attack` (V), `patrol` (line), `escort` (diamond)

### 🟫 Minecraft Characters (`scripts/minecraft_characters.py`)

```python
exec(open(r"C:\Development\maya\launchers\RUN_MINECRAFT.py").read())
```

| Function | Description |
|----------|-------------|
| `create_character(char_type, name, scale, pose, held_item, armor)` | Create any character |
| `create_village(character_count, radius)` | Create village scene |
| `create_mob_horde(mob_type, count, formation)` | Create hostile mob group |
| `show_ui()` | Open the character generator UI |

**Characters:** `steve`, `alex`, `zombie`, `skeleton`, `creeper`, `enderman`, `villager`, `pigman`, `witch`, `iron_golem`
**Poses:** `standing`, `walking`, `wave`, `zombie`
**Items:** `sword`, `pickaxe`, `bow`
**Armor:** `leather`, `chainmail`, `iron`, `gold`, `diamond`, `netherite`

### ✨ 3D Text Generator (`scripts/fancy_3d_text_v2.py`)

```python
exec(open(r"C:\Development\maya\launchers\RUN_3D_TEXT.py").read())
```

| Function | Description |
|----------|-------------|
| `create_3d_text(text, color_preset, ...)` | Create 3D text |
| `hello_world()` | Quick demo with rainbow text |
| `show_ui()` | Open the UI window |

**Color Presets:** `rainbow`, `fire`, `ocean`, `neon`, `gold`, `forest`
**Animation Types:** `wave`, `bounce`, `spin`, `pop`

### 🔍 Font Diagnostic (`scripts/font_diagnostic.py`)

```python
exec(open(r"C:\Development\maya\launchers\RUN_FONT_DIAGNOSTIC.py").read())
```

Run this first if you have font issues with 3D text!

---

## 🐛 Troubleshooting

### Script Not Found

```python
# Make sure the path exists and is correct
import os
print(os.path.exists(r"C:\Development\maya\scripts\starship.py"))
print(os.path.exists(r"C:\Development\maya\launchers\RUN_STARSHIP_V1.py"))
```

### Module Import Error

```python
# Check if path is in sys.path
import sys
print(sys.path)

# Add it manually if needed
sys.path.insert(0, r"C:\Development\maya\scripts")
```

### Font Not Found (3D Text)

Run the font diagnostic first:
```python
exec(open(r"C:\Development\maya\launchers\RUN_FONT_DIAGNOSTIC.py").read())
```

Or use `fancy_3d_text_v2.py` which uses Maya's Type tool and has fewer font issues.

### Animation Not Playing

1. Make sure you're not on frame 1
2. Press **Play** in the timeline (or press `Alt+V`)
3. Set playback range: `1-120` frames

### Arnold Materials Not Working

If you don't have Arnold, the scripts automatically use Lambert/Blinn materials instead.

---

## 📚 More Resources

- [Maya Python Documentation](https://help.autodesk.com/view/MAYAUL/2024/ENU/?guid=Maya_SDK_Maya_Python_API_html)
- [Domain Knowledge Guide](domain-knowledge/DK-MAYA-PYTHON-SCRIPTING-v1.0.0.md)
- [README.md](README.md) - Full project documentation

---

**Happy Scripting! 🎉**
