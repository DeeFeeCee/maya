"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   🔍 FONT DIAGNOSTIC - LAUNCHER                                              ║
║      Run This First to Find Available Fonts!                                 ║
║                                                                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║   INSTRUCTIONS:                                                              ║
║   1. Open Maya                                                               ║
║   2. Open Script Editor: Windows > General Editors > Script Editor           ║
║   3. Click the "Python" tab (NOT MEL)                                        ║
║   4. Copy ALL code below the dashed line, paste, press Ctrl+Enter            ║
║                                                                              ║
║   This will scan your system for available fonts and tell you which          ║
║   ones work with Maya's text creation commands.                              ║
║                                                                              ║
║   Created for Douglas to learn Maya Python scripting! 🔍                     ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

═══════════════════════════════════════════════════════════════════════════════
                           AVAILABLE FUNCTIONS
═══════════════════════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────────────────────┐
│ diagnose_fonts()                                                            │
├─────────────────────────────────────────────────────────────────────────────┤
│ Diagnose font availability in Maya.                                         │
│ Run this to see what fonts work on your system!                             │
│                                                                             │
│ SIGNATURE:                                                                  │
│   diagnose_fonts() -> list[str]   # Returns: List of working font names     │
│                                                                             │
│ WHAT IT DOES:                                                               │
│   1. Uses MEL fontDialog to list all available fonts                        │
│   2. Tests common font names (Arial, Times New Roman, Courier, etc.)        │
│   3. Reports which fonts work with Maya's textCurves command                │
│   4. Recommends the best font to use                                        │
│                                                                             │
│ EXAMPLE:                                                                    │
│   diagnose_fonts()                                                          │
│                                                                             │
│ TESTED FONTS:                                                               │
│   • Windows: Arial, Times New Roman, Courier New, Verdana, Tahoma,          │
│              Georgia, Trebuchet MS, Impact, Comic Sans MS                   │
│   • Maya/Adobe: Bitstream Vera Sans, Courier, Helvetica                     │
│   • Generic: fixed, system                                                  │
└─────────────────────────────────────────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════════════════════
                              TROUBLESHOOTING
═══════════════════════════════════════════════════════════════════════════════

If no fonts work:
  1. Check that Windows Fonts folder has fonts installed
  2. Try restarting Maya
  3. Check Maya preferences aren't corrupted
  4. Use the 3D Text Generator V2 (fancy_3d_text_v2.py) which uses Maya's
     Type tool and works without font issues

NOTE: The starship generators don't use fonts at all - they work 100%
      with Maya primitives. If you're having font issues, try the starships!

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
print("🔍 Loading Font Diagnostic Tool...")
print("═" * 60)

try:
    # Import and run the diagnostic
    from font_diagnostic import diagnose_fonts
    
    print("\nRunning font diagnostic...")
    print("This may take a moment...\n")
    
    # Run the diagnostic automatically
    working_fonts = diagnose_fonts()
    
    if working_fonts:
        print("\n✅ Diagnostic complete!")
        print(f"   Found {len(working_fonts)} working fonts.")
    else:
        print("\n⚠️ No standard fonts found.")
        print("   Try using fancy_3d_text_v2.py which doesn't need fonts.")
        print("   Or use the starship generators - they work 100%!")

except Exception as e:
    print(f"\n❌ Error loading font_diagnostic: {e}")
    print("\nMake sure the script is in:", scripts_path)
    import traceback
    traceback.print_exc()
