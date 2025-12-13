"""
Font Diagnostic Script for Maya
==============================
Run this first to find available fonts on your system!

Usage in Maya:
    1. Open Script Editor (Windows > General Editors > Script Editor)
    2. Copy and paste this entire script into the Python tab
    3. Press Ctrl+Enter to run
"""

import maya.cmds as cmds
import maya.mel as mel

def diagnose_fonts():
    """
    Diagnose font availability in Maya.
    Run this to see what fonts work on your system!
    """
    print("\n" + "═" * 60)
    print("🔍 MAYA FONT DIAGNOSTIC")
    print("═" * 60)
    
    # Method 1: Try MEL fontDialog
    print("\n📋 Method 1: MEL fontDialog -FontList")
    print("-" * 40)
    try:
        fonts = mel.eval('fontDialog -FontList')
        if fonts:
            print(f"✓ Found {len(fonts)} fonts!")
            print("First 10 fonts:")
            for f in fonts[:10]:
                print(f"    • {f}")
            working_font = fonts[0]
            print(f"\n✓ Recommended font: '{working_font}'")
        else:
            print("✗ fontDialog returned empty list")
            working_font = None
    except Exception as e:
        print(f"✗ fontDialog failed: {e}")
        working_font = None
    
    # Method 2: Try common font names
    print("\n📋 Method 2: Testing common fonts")
    print("-" * 40)
    
    test_fonts = [
        # Windows fonts
        "Arial",
        "Times New Roman",
        "Courier New",
        "Verdana",
        "Tahoma",
        "Georgia",
        "Trebuchet MS",
        "Impact",
        "Comic Sans MS",
        # Maya/Adobe fonts
        "Bitstream Vera Sans",
        "Courier",
        "Helvetica",
        # Generic
        "fixed",
        "system",
    ]
    
    working_fonts = []
    
    for font in test_fonts:
        try:
            # Try to create text with this font
            result = cmds.textCurves(font=font, text="A")
            if result:
                cmds.delete(result)
                print(f"    ✓ '{font}' - WORKS!")
                working_fonts.append(font)
            else:
                print(f"    ✗ '{font}' - No result")
        except Exception as e:
            print(f"    ✗ '{font}' - {str(e)[:30]}")
    
    # Summary
    print("\n" + "═" * 60)
    print("📊 SUMMARY")
    print("═" * 60)
    
    if working_fonts:
        print(f"\n✓ {len(working_fonts)} working fonts found!")
        print("\nUse any of these in fancy_3d_text.py:")
        for f in working_fonts:
            print(f'    create_3d_text("HELLO", font="{f}")')
        
        # Suggest the best one
        best = working_fonts[0]
        print(f"\n⭐ BEST CHOICE: '{best}'")
        print(f"\nCopy this to use:")
        print(f'    from fancy_3d_text import create_3d_text')
        print(f'    create_3d_text("HELLO WORLD", font="{best}")')
    else:
        print("\n⚠️ No standard fonts worked!")
        print("\nTrying alternative approach...")
        
        # Try without font parameter at all
        try:
            result = cmds.textCurves(text="A")
            if result:
                cmds.delete(result)
                print("✓ Default font (no parameter) works!")
                print("\nUse this:")
                print('    create_3d_text("HELLO WORLD")  # Uses Maya default')
        except Exception as e:
            print(f"✗ Even default failed: {e}")
            print("\nMaya may need font configuration. Check:")
            print("  - Windows Fonts folder has fonts installed")
            print("  - Maya preferences aren't corrupted")
    
    print("\n" + "═" * 60)
    print("🏁 Diagnostic Complete!")
    print("═" * 60 + "\n")
    
    return working_fonts


# Run the diagnostic
if __name__ == "__main__":
    diagnose_fonts()
else:
    # Also run when imported
    diagnose_fonts()
