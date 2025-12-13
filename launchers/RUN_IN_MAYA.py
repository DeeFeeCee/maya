"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   🚀 MAYA QUICK START - STARSHIP GENERATOR V1 LAUNCHER                       ║
║      Just Run This File in Maya!                                             ║
║                                                                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║   INSTRUCTIONS:                                                              ║
║   1. Open Maya                                                               ║
║   2. Open Script Editor: Windows > General Editors > Script Editor           ║
║   3. Click the "Python" tab (NOT MEL)                                        ║
║   4. Drag this file into the Script Editor, or paste code below              ║
║   5. Press Ctrl+Enter or click "Execute All"                                 ║
║                                                                              ║
║   The Starship Generator UI will open automatically!                         ║
║                                                                              ║
║   Created for Douglas to learn Maya Python scripting! 🚀                     ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

═══════════════════════════════════════════════════════════════════════════════
                           AVAILABLE FUNCTIONS
═══════════════════════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────────────────────┐
│ create_starship(...)                                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│ Create a 3D starship using Maya primitives.                                 │
│                                                                             │
│ SIGNATURE:                                                                  │
│   create_starship(                                                          │
│       name="starship",        # str: Name for the starship group            │
│       ship_type="fighter",    # str: "fighter", "cruiser", "bomber", "scout"│
│       color_scheme="classic", # str: "classic", "rebel", "imperial",        │
│                               #      "pirate", "alien"                      │
│       scale=1.0,              # float: Size multiplier                      │
│       add_animation=True      # bool: Add engine glow animation             │
│   ) -> str                    # Returns: Name of the created starship group │
│                                                                             │
│ EXAMPLES:                                                                   │
│   create_starship()                                                         │
│   create_starship("my_ship", ship_type="fighter", color_scheme="rebel")     │
│   create_starship("empire_ship", "cruiser", "imperial", scale=1.5)          │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ create_fleet(...)                                                           │
├─────────────────────────────────────────────────────────────────────────────┤
│ Create multiple starships in formation.                                     │
│                                                                             │
│ SIGNATURE:                                                                  │
│   create_fleet(                                                             │
│       count=3,                # int: Number of ships                        │
│       formation="line"        # str: "line", "v", "diamond", "random"       │
│   ) -> str                    # Returns: Name of the fleet group            │
│                                                                             │
│ EXAMPLES:                                                                   │
│   create_fleet()                                                            │
│   create_fleet(5, "v")                                                      │
│   create_fleet(8, "diamond")                                                │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ show_ui()                                                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│ Open the Starship Generator UI window.                                      │
│                                                                             │
│ SIGNATURE:                                                                  │
│   show_ui() -> None                                                         │
│                                                                             │
│ EXAMPLE:                                                                    │
│   show_ui()                                                                 │
└─────────────────────────────────────────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════════════════════
                              OPTIONS REFERENCE
═══════════════════════════════════════════════════════════════════════════════

COLOR SCHEMES (5 available):
  • "classic"   - Silver-gray hull with blue accents and cyan engine glow
  • "rebel"     - Off-white hull with orange accents
  • "imperial"  - Dark gray hull with black accents and blue glow
  • "pirate"    - Rusty brown hull with red accents
  • "alien"     - Green hull with purple accents

SHIP TYPES (4 available):
  • "fighter"   - Standard combat fighter
  • "cruiser"   - Large capital ship
  • "bomber"    - Heavy ship for big payloads
  • "scout"     - Small, fast reconnaissance ship

FORMATIONS (4 available):
  • "line"      - Ships in a horizontal line
  • "v"         - V-formation like flying geese
  • "diamond"   - Ships arranged in a circle/diamond
  • "random"    - Random positions and rotations

═══════════════════════════════════════════════════════════════════════════════
"""

# ----------- COPY EVERYTHING BELOW THIS LINE -----------

import sys

# Add the scripts folder to Maya's path
# IMPORTANT: Update this path if your folder is different!
scripts_path = r"c:/Development/maya/scripts"

if scripts_path not in sys.path:
    sys.path.insert(0, scripts_path)
    print(f"✓ Added to path: {scripts_path}")

print("\n" + "═" * 60)
print("🚀 Loading Starship Generator V1...")
print("═" * 60)

try:
    # Import and run the starship generator
    from starship import create_starship, create_fleet, show_ui
    
    print()
    print("QUICK START:")
    print("  show_ui()                    # Open the UI")
    print("  create_starship()            # Create one ship")
    print("  create_fleet(5, 'v')         # Create a fleet")
    print()
    print("EXAMPLES:")
    print("  create_starship('x_wing', 'fighter', 'rebel')")
    print("  create_starship('tie', 'fighter', 'imperial', scale=0.8)")
    print("  create_fleet(8, 'diamond')")
    print()
    print("COLOR SCHEMES: classic, rebel, imperial, pirate, alien")
    print("SHIP TYPES: fighter, cruiser, bomber, scout")
    print("FORMATIONS: line, v, diamond, random")
    print("═" * 60 + "\n")
    
    # Open the UI automatically
    show_ui()

except Exception as e:
    print(f"\n❌ Error loading starship: {e}")
    print("\nMake sure the script is in:", scripts_path)
    import traceback
    traceback.print_exc()
