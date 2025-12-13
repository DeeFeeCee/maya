"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   🚀 STARSHIP GENERATOR V2 - LAUNCHER                                        ║
║      Advanced Edition with More Detail!                                      ║
║                                                                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║   INSTRUCTIONS:                                                              ║
║   1. Open Maya                                                               ║
║   2. Open Script Editor: Windows > General Editors > Script Editor           ║
║   3. Click the "Python" tab (NOT MEL)                                        ║
║   4. Copy ALL code below the dashed line, paste, press Ctrl+Enter            ║
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
│ Create a detailed starship with advanced features.                          │
│                                                                             │
│ SIGNATURE:                                                                  │
│   create_starship(                                                          │
│       name="starship",          # str: Name for the ship                    │
│       ship_class="interceptor", # str: "interceptor", "heavy_fighter",      │
│                                 #      "racer"                              │
│       theme="federation",       # str: "federation", "empire",              │
│                                 #      "bounty_hunter", "alien",            │
│                                 #      "stealth", "racer"                   │
│       scale=1.0,                # float: Size multiplier                    │
│       add_animation=True,       # bool: Add engine and flight animations    │
│       animation_style="hover"   # str: "hover", "flyby", "banking"          │
│   ) -> str                      # Returns: Name of the ship group           │
│                                                                             │
│ EXAMPLES:                                                                   │
│   create_starship("red_five", "interceptor", "federation")                  │
│   create_starship("tie_fighter", "interceptor", "empire", scale=0.8)        │
│   create_starship("slave_one", "heavy_fighter", "bounty_hunter")            │
│   create_starship("speed_demon", "racer", "racer")                          │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ create_squadron(...)                                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│ Create a squadron of ships in formation.                                    │
│                                                                             │
│ SIGNATURE:                                                                  │
│   create_squadron(                                                          │
│       count=3,                  # int: Number of ships (1-12)               │
│       ship_class="interceptor", # str: Type of ships                        │
│       theme="federation",       # str: Color scheme                         │
│       formation="v"             # str: "v", "line", "diamond", "echelon"    │
│   ) -> str                      # Returns: Name of the squadron group       │
│                                                                             │
│ EXAMPLES:                                                                   │
│   create_squadron()                                                         │
│   create_squadron(5, "interceptor", "federation", "v")                      │
│   create_squadron(4, "heavy_fighter", "empire", "diamond")                  │
│   create_squadron(6, "racer", "racer", "echelon")                           │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ show_ui()                                                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│ Open the Starship Generator V2 UI window.                                   │
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

THEMES (6 available):
  • "federation"    - Light silver hull, blue accents, cyan glow
  • "empire"        - Dark gray hull, red accents, blue glow
  • "bounty_hunter" - Worn tan hull, gold accents, orange glow
  • "alien"         - Dark green hull, purple accents, green glow
  • "stealth"       - Near-black hull, minimal lighting
  • "racer"         - Bright orange hull, white stripes, cyan glow

SHIP CLASSES (3 implemented):
  • "interceptor"   - Fast, agile fighter with forward-swept wings
  • "heavy_fighter" - Balanced combat ship with thick armor
  • "racer"         - Ultra-fast ship built for speed

FORMATIONS (4 available):
  • "v"             - V-formation like flying geese (leader in front)
  • "line"          - Ships in a horizontal line
  • "diamond"       - Ships arranged in a circle/diamond
  • "echelon"       - Diagonal staircase formation

ANIMATION STYLES (3 available):
  • "hover"         - Gentle floating motion
  • "flyby"         - Flying past camera
  • "banking"       - Banking turn animation

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

# Import and run the starship generator
try:
    # Reload in case we made changes
    if 'starship_v2' in sys.modules:
        del sys.modules['starship_v2']
    
    import starship_v2
    from starship_v2 import create_starship, create_squadron, show_ui
    
    print("\n" + "═"*60)
    print("🚀 STARSHIP GENERATOR V2 LOADED!")
    print("═"*60)
    print()
    print("QUICK START:")
    print("  show_ui()                    # Open the UI")
    print("  create_starship()            # Create one ship")
    print("  create_squadron(5)           # Create a squadron")
    print()
    print("EXAMPLES:")
    print("  create_starship('red_five', 'interceptor', 'federation')")
    print("  create_starship('tie', 'interceptor', 'empire', scale=0.8)")
    print("  create_starship('hunter', 'heavy_fighter', 'bounty_hunter')")
    print("  create_starship('shadow', 'interceptor', 'stealth')")
    print("  create_starship('speed_demon', 'racer', 'racer')")
    print("  create_squadron(5, 'interceptor', 'federation', 'v')")
    print()
    print("THEMES: federation, empire, bounty_hunter, alien, stealth, racer")
    print("CLASSES: interceptor, heavy_fighter, racer")
    print("FORMATIONS: v, line, diamond, echelon")
    print("═"*60 + "\n")
    
    # Automatically open the UI for easy use
    show_ui()
    
except Exception as e:
    print(f"\n❌ Error loading starship_v2: {e}")
    print("\nMake sure the script is in:", scripts_path)
    import traceback
    traceback.print_exc()
