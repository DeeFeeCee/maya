"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   ⭐ STAR WARS FLEET LAUNCHER ⭐                                              ║
║   Create iconic sci-fi starship fleets in Maya!                              ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 FUNCTION SIGNATURES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

create_ship(ship_type, name=None, scale=1.0, position=(0,0,0))
    ship_type : str    - Type of ship (see SHIP TYPES below)
    name      : str    - Custom name (auto-generated if None)
    scale     : float  - Size multiplier (default: 1.0)
    position  : tuple  - (x, y, z) world position

create_fleet(faction, count=5, formation="attack")
    faction   : str    - "rebel", "imperial", "mixed", "bounty_hunter"
    count     : int    - Number of ships in fleet (2-12 recommended)
    formation : str    - "attack" (V), "patrol" (line), "escort" (diamond)

show_ui()
    Opens the Star Wars Fleet Generator UI window

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚀 SHIP TYPES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

REBEL ALLIANCE:
  "xwing"       - X-Wing Fighter (S-foils in attack position)
  "ywing"       - Y-Wing Bomber (exposed engine machinery)
  "awing"       - A-Wing Interceptor (small, fast, red)
  "falcon"      - Light Freighter (YT-1300 style with mandibles)

GALACTIC EMPIRE:
  "tie"         - TIE Fighter (hexagonal solar panel wings)
  "interceptor" - TIE Interceptor (angled dagger wings, 4 cannons)
  "shuttle"     - Imperial Shuttle (Lambda-class, folding wings)

BOUNTY HUNTERS:
  "slave1"      - Firespray Gunship (vertical flight, unique shape)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎮 FORMATIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"attack"  - V-formation (lead ship at front, wings spread back)
"patrol"  - Horizontal line (ships side by side)
"escort"  - Diamond pattern (one center, others surrounding)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📝 USAGE EXAMPLES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Create individual ships:
create_ship("xwing")                              # Basic X-Wing
create_ship("tie", scale=1.5)                     # Larger TIE Fighter
create_ship("falcon", name="my_falcon")           # Named freighter
create_ship("shuttle", position=(10, 0, 0))       # Positioned shuttle

# Create fleets:
create_fleet("rebel")                             # 5 rebel ships, V-formation
create_fleet("imperial", count=8)                 # 8 imperial ships
create_fleet("rebel", count=6, formation="escort") # 6 ships in diamond
create_fleet("bounty_hunter", count=3)            # 3 bounty hunter ships

# Epic battle scene:
create_fleet("rebel", count=6, formation="attack")
create_fleet("imperial", count=8, formation="patrol")

# Open the UI:
show_ui()

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⬇️ COPY CODE BELOW TO MAYA SCRIPT EDITOR ⬇️
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import sys
import os

# Add scripts folder to path
scripts_path = r"c:\Development\maya\scripts"
if scripts_path not in sys.path:
    sys.path.insert(0, scripts_path)

# Import and reload for development
import starwars_fleet
import importlib
importlib.reload(starwars_fleet)

# Import functions for easy access
from starwars_fleet import create_ship, create_fleet, show_ui

# ═══════════════════════════════════════════════════════════════════════════════
# 🚀 QUICK START - Uncomment what you want!
# ═══════════════════════════════════════════════════════════════════════════════

# --- OPTION 1: Open the UI ---
show_ui()

# --- OPTION 2: Create a Rebel fleet (V-formation) ---
# create_fleet("rebel", count=5, formation="attack")

# --- OPTION 3: Create an Imperial fleet ---
# create_fleet("imperial", count=6, formation="patrol")

# --- OPTION 4: Epic battle scene! ---
# create_fleet("rebel", count=5, formation="attack")
# create_fleet("imperial", count=7, formation="escort")

# --- OPTION 5: Create individual ships ---
# create_ship("xwing")
# create_ship("tie", position=(10, 0, 0))
# create_ship("falcon", position=(0, 0, 10), scale=1.2)
# create_ship("slave1", position=(-10, 0, 0))

# --- OPTION 6: One of each ship type! ---
# ships = ["xwing", "tie", "ywing", "awing", "falcon", "shuttle", "interceptor", "slave1"]
# for i, ship_type in enumerate(ships):
#     create_ship(ship_type, position=(i * 8, 0, 0))
