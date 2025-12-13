"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   ✨ 3D TEXT GENERATOR V1 - LAUNCHER                                         ║
║      Using textCurves (requires working fonts)                               ║
║                                                                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║   INSTRUCTIONS:                                                              ║
║   1. Open Maya                                                               ║
║   2. Open Script Editor: Windows > General Editors > Script Editor           ║
║   3. Click the "Python" tab (NOT MEL)                                        ║
║   4. Copy ALL code below the dashed line, paste, press Ctrl+Enter            ║
║                                                                              ║
║   ⚠️ NOTE: This version uses textCurves which may have font issues.          ║
║   If you get font errors, use RUN_3D_TEXT.py (V2) instead!                   ║
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
│ Create fancy 3D text using Maya's textCurves command.                       │
│                                                                             │
│ SIGNATURE:                                                                  │
│   create_3d_text(                                                           │
│       text="HELLO WORLD",       # str: The text to create                   │
│       font=None,                # str: Font name (None = auto-detect)       │
│       extrude_depth=0.5,        # float: How deep to extrude                │
│       bevel_width=0.1,          # float: Width of bevel edges               │
│       bevel_depth=0.05,         # float: Depth of bevels                    │
│       color_preset="rainbow",   # str: "rainbow", "fire", "ice",            │
│                                 #      "neon", "gold", "sunset"             │
│       per_letter_colors=True,   # bool: Different color per letter          │
│       add_glow=True,            # bool: Add glowing effect                  │
│       glow_intensity=0.3,       # float: How strong the glow is (0-1)       │
│       add_animation=True,       # bool: Animate the text                    │
│       animation_type="wave",    # str: "wave", "bounce", "spin", "pop"      │
│       letter_spacing=0.2,       # float: Space between letters              │
│       scale=1.0                 # float: Overall scale multiplier           │
│   ) -> tuple                    # Returns: (main_group, list_of_meshes)     │
│                                                                             │
│ EXAMPLES:                                                                   │
│   create_3d_text("MAYA", color_preset="fire", animation_type="bounce")      │
│   create_3d_text("PYTHON", color_preset="neon", add_animation=False)        │
│   create_3d_text("HELLO", font="Arial")                                     │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ hello_world()                                                               │
├─────────────────────────────────────────────────────────────────────────────┤
│ Quick demo - creates "HELLO WORLD" with rainbow colors and wave animation.  │
│                                                                             │
│ SIGNATURE:                                                                  │
│   hello_world() -> tuple        # Returns: (main_group, list_of_meshes)     │
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
  • "rainbow"  - Red, orange, yellow, green, cyan, blue, purple
  • "fire"     - Yellow, orange, red-orange, dark red
  • "ice"      - White, light blue, blue, deep blue
  • "neon"     - Hot pink, cyan, purple, green (80s arcade)
  • "gold"     - Light gold, gold, goldenrod, dark gold
  • "sunset"   - Coral, orange, peach, mauve, purple

ANIMATION TYPES (4 available):
  • "wave"     - Letters move up and down in a wave pattern
  • "bounce"   - Letters bounce up and down
  • "spin"     - Letters rotate
  • "pop"      - Letters pop in with scale animation

⚠️ TROUBLESHOOTING FONTS:
  If you get font errors, run RUN_FONT_DIAGNOSTIC.py first to find
  which fonts work on your system. Or use RUN_3D_TEXT.py (V2) instead!

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
print("✨ Loading 3D Text Generator V1...")
print("═" * 60)

try:
    # Import (and reload to get latest changes)
    import fancy_3d_text
    importlib.reload(fancy_3d_text)
    from fancy_3d_text import create_3d_text, hello_world, show_ui
    
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
    print("PRESETS: rainbow, fire, ice, neon, gold, sunset")
    print("ANIMATIONS: wave, bounce, spin, pop")
    print()
    print("⚠️ If you get font errors, use RUN_3D_TEXT.py (V2) instead!")
    print("═" * 60 + "\n")
    
    # Open the UI automatically
    show_ui()

except Exception as e:
    print(f"\n❌ Error loading fancy_3d_text: {e}")
    print("\n⚠️ This is likely a font issue.")
    print("   Try using RUN_3D_TEXT.py (V2) instead!")
    print("   Or run RUN_FONT_DIAGNOSTIC.py to find working fonts.")
    print("\nMake sure the script is in:", scripts_path)
    import traceback
    traceback.print_exc()
