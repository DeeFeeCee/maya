"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   ✨ 3D TEXT GENERATOR V2 - LAUNCHER                                         ║
║      Using Maya's Type Tool (More Reliable)                                  ║
║                                                                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║   INSTRUCTIONS:                                                              ║
║   1. Open Maya                                                               ║
║   2. Open Script Editor: Windows > General Editors > Script Editor           ║
║   3. Click the "Python" tab (NOT MEL)                                        ║
║   4. Copy ALL code below the dashed line, paste, press Ctrl+Enter            ║
║                                                                              ║
║   Created for Douglas to learn Maya Python scripting! ✨                     ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

═══════════════════════════════════════════════════════════════════════════════
                           AVAILABLE FUNCTIONS
═══════════════════════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────────────────────┐
│ create_3d_text(...)                                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│ Create fancy 3D text using Maya's Type tool.                                │
│                                                                             │
│ SIGNATURE:                                                                  │
│   create_3d_text(                                                           │
│       text="HELLO WORLD",       # str: The text to create                   │
│       color_preset="rainbow",   # str: "rainbow", "fire", "ocean",          │
│                                 #      "neon", "gold", "forest"             │
│       extrude_depth=0.5,        # float: How deep the 3D extrusion is       │
│       bevel_depth=0.05,         # float: Bevel size for edges               │
│       add_glow=True,            # bool: Add glowing effect                  │
│       glow_intensity=0.3,       # float: How strong the glow is (0-1)       │
│       add_animation=True,       # bool: Animate the text                    │
│       animation_type="wave",    # str: "wave", "bounce", "spin", "pop"      │
│       scale=1.0                 # float: Overall scale multiplier           │
│   ) -> str                      # Returns: Name of the text group           │
│                                                                             │
│ EXAMPLES:                                                                   │
│   create_3d_text("HELLO WORLD")                                             │
│   create_3d_text("MAYA", color_preset="fire", animation_type="bounce")      │
│   create_3d_text("PYTHON", color_preset="neon", add_animation=False)        │
│   create_3d_text("GOLD", color_preset="gold", extrude_depth=1.0)            │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ hello_world()                                                               │
├─────────────────────────────────────────────────────────────────────────────┤
│ Quick demo - creates "HELLO WORLD" with rainbow colors and wave animation.  │
│                                                                             │
│ SIGNATURE:                                                                  │
│   hello_world() -> str          # Returns: Name of the text group           │
│                                                                             │
│ EXAMPLE:                                                                    │
│   hello_world()                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ show_ui()                                                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│ Open the 3D Text Generator UI window.                                       │
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

COLOR PRESETS (6 available):
  • "rainbow"  - Red, orange, yellow, green, cyan, blue, purple, pink
  • "fire"     - Red to yellow gradient (hot flames)
  • "ocean"    - Deep blue to aqua (underwater)
  • "neon"     - Hot pink, cyan, yellow, green, magenta (80s arcade)
  • "gold"     - Gold, goldenrod, wheat (precious metal)
  • "forest"   - Forest green, sea green, lawn green (nature)

ANIMATION TYPES (4 available):
  • "wave"     - Letters move up and down in a wave pattern
  • "bounce"   - Letters bounce up and down
  • "spin"     - Letters rotate
  • "pop"      - Letters pop in with scale animation

NOTE: This script uses Maya's Type tool. Font may display as "3D Type"
      in the Maya interface, but the text you enter will work correctly.

═══════════════════════════════════════════════════════════════════════════════
"""

# ----------- COPY EVERYTHING BELOW THIS LINE -----------

import sys
import importlib

# Add the scripts folder to Maya's path
# IMPORTANT: Update this path if your folder is different!
scripts_path = r"c:/Development/maya/scripts"

if scripts_path not in sys.path:
    sys.path.insert(0, scripts_path)
    print(f"✓ Added to path: {scripts_path}")

print("\n" + "═" * 60)
print("✨ Loading 3D Text Generator v2...")
print("═" * 60)

try:
    # Import (and reload to get latest changes)
    import fancy_3d_text_v2
    importlib.reload(fancy_3d_text_v2)
    from fancy_3d_text_v2 import create_3d_text, hello_world, show_ui
    
    print()
    print("QUICK START:")
    print("  show_ui()                    # Open the UI")
    print("  hello_world()                # Quick rainbow demo")
    print("  create_3d_text('YOUR TEXT')  # Custom text")
    print()
    print("EXAMPLES:")
    print("  create_3d_text('MAYA', color_preset='fire')")
    print("  create_3d_text('PYTHON', color_preset='neon')")
    print("  create_3d_text('WOW', animation_type='bounce')")
    print()
    print("PRESETS: rainbow, fire, ocean, neon, gold, forest")
    print("ANIMATIONS: wave, bounce, spin, pop")
    print("═" * 60 + "\n")
    
    # Open the UI automatically
    show_ui()

except Exception as e:
    print(f"\n❌ Error loading fancy_3d_text_v2: {e}")
    print("\nMake sure the script is in:", scripts_path)
    import traceback
    traceback.print_exc()
