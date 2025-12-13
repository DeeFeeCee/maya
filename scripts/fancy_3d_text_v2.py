"""
Fancy 3D Text Generator for Maya - Using Type Tool (More Reliable)
===================================================================
This version uses Maya's Type node which is more reliable than textCurves.

Author: Douglas's Learning Project
Version: 2.0.0

Usage in Maya:
    from fancy_3d_text_v2 import hello_world, create_3d_text, show_ui
    hello_world()  # Quick demo
    show_ui()      # Full UI
"""

import maya.cmds as cmds
import maya.mel as mel
import random
import math

# ═══════════════════════════════════════════════════════════════════════════════
# COLOR PRESETS
# ═══════════════════════════════════════════════════════════════════════════════

COLOR_PRESETS = {
    "rainbow": [
        (1.0, 0.0, 0.0),    # Red
        (1.0, 0.5, 0.0),    # Orange
        (1.0, 1.0, 0.0),    # Yellow
        (0.0, 1.0, 0.0),    # Green
        (0.0, 0.5, 1.0),    # Cyan
        (0.0, 0.0, 1.0),    # Blue
        (0.5, 0.0, 1.0),    # Purple
        (1.0, 0.0, 0.5),    # Pink
    ],
    "fire": [
        (1.0, 0.0, 0.0),    # Red
        (1.0, 0.3, 0.0),    # Orange-red
        (1.0, 0.5, 0.0),    # Orange
        (1.0, 0.7, 0.0),    # Yellow-orange
        (1.0, 1.0, 0.0),    # Yellow
    ],
    "ocean": [
        (0.0, 0.2, 0.4),    # Deep blue
        (0.0, 0.4, 0.6),    # Ocean blue
        (0.0, 0.6, 0.8),    # Light blue
        (0.0, 0.8, 0.8),    # Cyan
        (0.5, 1.0, 1.0),    # Aqua
    ],
    "neon": [
        (1.0, 0.0, 0.5),    # Hot pink
        (0.0, 1.0, 1.0),    # Cyan
        (1.0, 1.0, 0.0),    # Yellow
        (0.0, 1.0, 0.0),    # Green
        (1.0, 0.0, 1.0),    # Magenta
    ],
    "gold": [
        (1.0, 0.84, 0.0),   # Gold
        (0.85, 0.65, 0.13), # Goldenrod
        (1.0, 0.75, 0.0),   # Orange gold
        (0.96, 0.87, 0.70), # Wheat
        (1.0, 0.94, 0.0),   # Bright gold
    ],
    "forest": [
        (0.13, 0.55, 0.13), # Forest green
        (0.0, 0.39, 0.0),   # Dark green
        (0.18, 0.55, 0.34), # Sea green
        (0.56, 0.74, 0.56), # Dark sea green
        (0.49, 0.99, 0.0),  # Lawn green
    ],
}


# ═══════════════════════════════════════════════════════════════════════════════
# CORE 3D TEXT FUNCTION - Using Type Tool
# ═══════════════════════════════════════════════════════════════════════════════

def create_3d_text(
    text="HELLO WORLD",
    color_preset="rainbow",
    extrude_depth=0.5,
    bevel_depth=0.05,
    add_glow=True,
    glow_intensity=0.3,
    add_animation=True,
    animation_type="wave",
    scale=1.0
):
    """
    Create fancy 3D text using Maya's Type tool (more reliable than textCurves).
    
    Args:
        text (str): The text to create (default: "HELLO WORLD")
        color_preset (str): Color scheme - "rainbow", "fire", "ocean", "neon", "gold", "forest"
        extrude_depth (float): How deep the 3D extrusion is (default: 0.5)
        bevel_depth (float): Bevel size for edges (default: 0.05)
        add_glow (bool): Add glowing effect (default: True)
        glow_intensity (float): How strong the glow is (default: 0.3)
        add_animation (bool): Animate the text (default: True)
        animation_type (str): "wave", "bounce", "spin", "pop" (default: "wave")
        scale (float): Overall scale multiplier (default: 1.0)
    
    Returns:
        tuple: (main_group, list_of_meshes)
    
    Example:
        >>> create_3d_text("MAYA", color_preset="fire", animation_type="bounce")
        >>> create_3d_text("PYTHON", color_preset="neon", add_animation=False)
    """
    
    print("\n" + "═" * 60)
    print(f"✨ Creating Fancy 3D Text: {text}")
    print("═" * 60)
    
    # Get colors
    colors = COLOR_PRESETS.get(color_preset, COLOR_PRESETS["rainbow"])
    
    # Store created objects
    all_meshes = []
    type_transform = None
    
    # METHOD 1: Use MEL to create Type with proper text
    print("  📝 Creating 3D Type text...")
    
    try:
        # First, create the type node using MEL (more reliable)
        mel.eval('CreatePolygonType')
        
        # Find the newly created type node
        type_nodes = cmds.ls(type="polyType")
        if type_nodes:
            type_node = type_nodes[-1]
            
            # IMPORTANT: Set the text FIRST before anything else
            cmds.setAttr(f"{type_node}.textInput", text, type="string")
            
            # Set extrusion
            cmds.setAttr(f"{type_node}.enableExtrusion", 1)
            cmds.setAttr(f"{type_node}.extrudeDepth", extrude_depth * scale)
            cmds.setAttr(f"{type_node}.extrudeDivisions", 1)
            
            # Force update
            cmds.refresh()
            
            # Find the transform connected to this type node
            # The type node is connected to a mesh shape
            connections = cmds.listConnections(type_node, type="mesh")
            if connections:
                for conn in connections:
                    parent = cmds.listRelatives(conn, parent=True)
                    if parent:
                        type_transform = parent[0]
                        all_meshes.append(type_transform)
                        break
            
            # If we couldn't find it via connections, search for recent transforms
            if not type_transform:
                all_transforms = cmds.ls(type="transform")
                for t in all_transforms:
                    if "type" in t.lower() or "Type" in t:
                        shapes = cmds.listRelatives(t, shapes=True, type="mesh")
                        if shapes:
                            type_transform = t
                            all_meshes.append(t)
                            break
            
            if type_transform:
                print(f"  ✓ Created 3D text: '{text}'")
            else:
                print("  ⚠️ Type created but couldn't find transform")
                
    except Exception as e:
        print(f"  ⚠️ Type tool failed: {e}")
    
    # METHOD 2: Fallback to primitive text (guaranteed to work)
    if not all_meshes:
        print("  📝 Using blocky text fallback...")
        all_meshes = create_primitive_text(text, scale)
        if all_meshes:
            print(f"  ✓ Created blocky text: '{text}'")
    
    if not all_meshes:
        print("  ❌ Could not create text!")
        return None, []
    
    # Create main group
    main_group = cmds.group(empty=True, name=f"fancy_text_{text.replace(' ', '_')}_grp")
    
    for mesh in all_meshes:
        try:
            cmds.parent(mesh, main_group)
        except Exception:
            pass
    
    # Apply materials
    print("  🎨 Applying materials...")
    for i, mesh in enumerate(all_meshes):
        color = colors[i % len(colors)]
        apply_fancy_material(mesh, color, add_glow, glow_intensity, f"text_mat_{i}")
    
    # Scale the result
    if scale != 1.0:
        cmds.scale(scale, scale, scale, main_group)
    
    # Add animation
    if add_animation and all_meshes:
        print(f"  🎬 Adding {animation_type} animation...")
        add_text_animation(all_meshes, animation_type)
    
    # Center the group
    cmds.xform(main_group, centerPivots=True)
    cmds.move(0, 0, 0, main_group, absolute=True)
    
    print("═" * 60)
    print(f"✅ 3D Text '{text}' Created Successfully!")
    print("═" * 60 + "\n")
    
    return main_group, all_meshes


def create_primitive_text(text, scale=1.0):
    """
    Create text using primitive shapes as a fallback.
    Simple but works when other methods fail.
    """
    meshes = []
    x_pos = 0
    
    # Simple letter definitions using cubes (blocky style)
    letter_patterns = {
        'A': [(0,0), (0,1), (0,2), (1,2), (2,2), (2,1), (2,0), (1,1)],
        'B': [(0,0), (0,1), (0,2), (1,2), (2,1.5), (1,1), (2,0.5), (1,0)],
        'C': [(0,0), (0,1), (0,2), (1,2), (2,2), (1,0), (2,0)],
        'D': [(0,0), (0,1), (0,2), (1,2), (2,1), (1,0)],
        'E': [(0,0), (0,1), (0,2), (1,2), (2,2), (1,1), (1,0), (2,0)],
        'F': [(0,0), (0,1), (0,2), (1,2), (2,2), (1,1)],
        'G': [(0,0), (0,1), (0,2), (1,2), (2,2), (2,0), (1,0), (2,1), (1.5,1)],
        'H': [(0,0), (0,1), (0,2), (1,1), (2,0), (2,1), (2,2)],
        'I': [(0,0), (1,0), (2,0), (1,1), (0,2), (1,2), (2,2)],
        'J': [(0,0), (1,0), (2,0), (2,1), (2,2), (1,2), (0,2)],
        'K': [(0,0), (0,1), (0,2), (1,1), (2,0), (2,2)],
        'L': [(0,0), (0,1), (0,2), (1,0), (2,0)],
        'M': [(0,0), (0,1), (0,2), (1,1.5), (2,2), (2,1), (2,0)],
        'N': [(0,0), (0,1), (0,2), (1,1.5), (2,2), (2,1), (2,0)],
        'O': [(0,0), (0,1), (0,2), (1,2), (2,2), (2,1), (2,0), (1,0)],
        'P': [(0,0), (0,1), (0,2), (1,2), (2,2), (2,1.5), (1,1)],
        'Q': [(0,0), (0,1), (0,2), (1,2), (2,2), (2,1), (2,0), (1,0), (1.5,-0.5)],
        'R': [(0,0), (0,1), (0,2), (1,2), (2,2), (2,1.5), (1,1), (2,0)],
        'S': [(0,0), (1,0), (2,0), (2,1), (1,1), (0,1), (0,2), (1,2), (2,2)],
        'T': [(0,2), (1,2), (2,2), (1,1), (1,0)],
        'U': [(0,2), (0,1), (0,0), (1,0), (2,0), (2,1), (2,2)],
        'V': [(0,2), (0,1), (1,0), (2,1), (2,2)],
        'W': [(0,2), (0,1), (0,0), (1,0.5), (2,0), (2,1), (2,2)],
        'X': [(0,0), (0,2), (1,1), (2,0), (2,2)],
        'Y': [(0,2), (1,1), (2,2), (1,0)],
        'Z': [(0,2), (1,2), (2,2), (2,1), (1,1), (0,1), (0,0), (1,0), (2,0)],
        ' ': [],  # Space
        '!': [(1,2), (1,1), (1,0)],
        '.': [(1,0)],
    }
    
    for char in text.upper():
        if char == ' ':
            x_pos += 2 * scale
            continue
        
        pattern = letter_patterns.get(char, letter_patterns.get('?', [(1,1)]))
        
        if pattern:
            letter_group = cmds.group(empty=True, name=f"letter_{char}_grp")
            
            for px, py in pattern:
                cube = cmds.polyCube(w=0.4*scale, h=0.4*scale, d=0.5*scale)[0]
                cmds.move((x_pos + px * 0.5) * scale, py * 0.5 * scale, 0, cube)
                cmds.parent(cube, letter_group)
            
            # Combine cubes into one mesh
            children = cmds.listRelatives(letter_group, children=True)
            if children and len(children) > 1:
                combined = cmds.polyUnite(children, ch=False, mergeUVSets=True)[0]
                cmds.parent(combined, letter_group)
                meshes.append(letter_group)
            elif children:
                meshes.append(letter_group)
        
        x_pos += 3 * scale
    
    return meshes


def apply_fancy_material(mesh, color, add_glow=True, glow_intensity=0.3, mat_name="fancy_mat"):
    """Apply a fancy material to a mesh."""
    try:
        # Create Blinn material
        material = cmds.shadingNode('blinn', asShader=True, name=mat_name)
        shading_group = cmds.sets(renderable=True, noSurfaceShader=True, 
                                   empty=True, name=f'{mat_name}_SG')
        cmds.connectAttr(f'{material}.outColor', f'{shading_group}.surfaceShader')
        
        # Set color
        cmds.setAttr(f'{material}.color', color[0], color[1], color[2], type='double3')
        
        # Shiny settings
        cmds.setAttr(f'{material}.specularColor', 1, 1, 1, type='double3')
        cmds.setAttr(f'{material}.specularRollOff', 0.7)
        cmds.setAttr(f'{material}.eccentricity', 0.2)
        cmds.setAttr(f'{material}.reflectivity', 0.3)
        
        # Glow
        if add_glow:
            cmds.setAttr(f'{material}.glowIntensity', glow_intensity)
            cmds.setAttr(f'{material}.incandescence', 
                        color[0] * 0.2, color[1] * 0.2, color[2] * 0.2, type='double3')
        
        # Apply to mesh
        cmds.sets(mesh, edit=True, forceElement=shading_group)
        
    except Exception as e:
        print(f"  ⚠️ Could not apply material: {e}")


def add_text_animation(meshes, animation_type="wave"):
    """Add animation to text meshes."""
    if not meshes:
        return
    
    cmds.playbackOptions(min=1, max=120, ast=1, aet=120)
    
    for i, mesh in enumerate(meshes):
        offset = i * 5
        
        if animation_type == "wave":
            cmds.setKeyframe(mesh, attribute='translateY', value=0, time=1 + offset)
            cmds.setKeyframe(mesh, attribute='translateY', value=0.5, time=15 + offset)
            cmds.setKeyframe(mesh, attribute='translateY', value=0, time=30 + offset)
            
        elif animation_type == "bounce":
            cmds.setKeyframe(mesh, attribute='translateY', value=0, time=1 + offset)
            cmds.setKeyframe(mesh, attribute='translateY', value=1.0, time=10 + offset)
            cmds.setKeyframe(mesh, attribute='translateY', value=0, time=20 + offset)
            cmds.setKeyframe(mesh, attribute='translateY', value=0.5, time=25 + offset)
            cmds.setKeyframe(mesh, attribute='translateY', value=0, time=30 + offset)
            
        elif animation_type == "spin":
            cmds.setKeyframe(mesh, attribute='rotateY', value=0, time=1)
            cmds.setKeyframe(mesh, attribute='rotateY', value=360, time=120)
            
        elif animation_type == "pop":
            cmds.setKeyframe(mesh, attribute='scaleX', value=0, time=1 + offset)
            cmds.setKeyframe(mesh, attribute='scaleY', value=0, time=1 + offset)
            cmds.setKeyframe(mesh, attribute='scaleZ', value=0, time=1 + offset)
            cmds.setKeyframe(mesh, attribute='scaleX', value=1.2, time=10 + offset)
            cmds.setKeyframe(mesh, attribute='scaleY', value=1.2, time=10 + offset)
            cmds.setKeyframe(mesh, attribute='scaleZ', value=1.2, time=10 + offset)
            cmds.setKeyframe(mesh, attribute='scaleX', value=1, time=15 + offset)
            cmds.setKeyframe(mesh, attribute='scaleY', value=1, time=15 + offset)
            cmds.setKeyframe(mesh, attribute='scaleZ', value=1, time=15 + offset)


# ═══════════════════════════════════════════════════════════════════════════════
# QUICK ACCESS FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def hello_world():
    """
    Quick demo - creates "HELLO WORLD" with rainbow colors and wave animation.
    Run this to test the script!
    """
    return create_3d_text(
        text="HELLO WORLD",
        color_preset="rainbow",
        animation_type="wave"
    )


def show_ui():
    """
    Show a simple UI for creating 3D text.
    """
    window_name = "fancy3DTextUI"
    
    if cmds.window(window_name, exists=True):
        cmds.deleteUI(window_name)
    
    window = cmds.window(window_name, title="Fancy 3D Text Generator v2", 
                         widthHeight=(350, 400), sizeable=True)
    
    cmds.columnLayout(adjustableColumn=True, rowSpacing=10, columnOffset=["both", 10])
    
    cmds.separator(height=10)
    cmds.text(label="✨ FANCY 3D TEXT GENERATOR ✨", font="boldLabelFont", height=30)
    cmds.text(label="Version 2.0 - Using Type Tool", font="smallPlainLabelFont")
    cmds.separator(height=10)
    
    # Text input
    cmds.text(label="Enter Text:", align="left")
    text_field = cmds.textField(text="HELLO WORLD", width=300)
    
    cmds.separator(height=10)
    
    # Color preset
    cmds.text(label="Color Preset:", align="left")
    color_menu = cmds.optionMenu(width=300)
    for preset in COLOR_PRESETS.keys():
        cmds.menuItem(label=preset.title())
    
    cmds.separator(height=5)
    
    # Animation
    cmds.text(label="Animation Type:", align="left")
    anim_menu = cmds.optionMenu(width=300)
    for anim in ["Wave", "Bounce", "Spin", "Pop", "None"]:
        cmds.menuItem(label=anim)
    
    cmds.separator(height=5)
    
    # Options
    cmds.text(label="Options:", align="left")
    extrude_slider = cmds.floatSliderGrp(label="Extrude:", field=True, 
                                          minValue=0.1, maxValue=2.0, value=0.5)
    scale_slider = cmds.floatSliderGrp(label="Scale:", field=True,
                                        minValue=0.5, maxValue=3.0, value=1.0)
    glow_check = cmds.checkBox(label="Add Glow Effect", value=True)
    
    cmds.separator(height=15)
    
    # Create button
    def on_create(*args):
        text = cmds.textField(text_field, query=True, text=True)
        color = cmds.optionMenu(color_menu, query=True, value=True).lower()
        anim = cmds.optionMenu(anim_menu, query=True, value=True).lower()
        if anim == "none":
            anim = None
        extrude = cmds.floatSliderGrp(extrude_slider, query=True, value=True)
        scl = cmds.floatSliderGrp(scale_slider, query=True, value=True)
        glow = cmds.checkBox(glow_check, query=True, value=True)
        
        create_3d_text(
            text=text,
            color_preset=color,
            extrude_depth=extrude,
            add_glow=glow,
            add_animation=anim is not None,
            animation_type=anim if anim else "wave",
            scale=scl
        )
    
    cmds.button(label="🚀 CREATE 3D TEXT", height=50, 
                backgroundColor=(0.2, 0.6, 0.2), command=on_create)
    
    cmds.separator(height=10)
    
    # Quick presets
    cmds.text(label="Quick Presets:", align="left")
    cmds.rowLayout(numberOfColumns=3, columnWidth3=(110, 110, 110))
    cmds.button(label="🔥 Fire", width=100,
                command=lambda x: create_3d_text("FIRE", color_preset="fire"))
    cmds.button(label="🌊 Ocean", width=100,
                command=lambda x: create_3d_text("OCEAN", color_preset="ocean"))
    cmds.button(label="✨ Neon", width=100,
                command=lambda x: create_3d_text("NEON", color_preset="neon"))
    cmds.setParent("..")
    
    cmds.showWindow(window)
    print("✅ UI loaded! Create some awesome 3D text!")


# ═══════════════════════════════════════════════════════════════════════════════
# SCRIPT ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("\n" + "═" * 60)
    print("🎨 FANCY 3D TEXT GENERATOR v2.0")
    print("═" * 60)
    print("\nQuick Start Commands:")
    print("  hello_world()     - Create demo text")
    print("  show_ui()         - Open the UI")
    print("  create_3d_text('YOUR TEXT', color_preset='fire')")
    print("═" * 60 + "\n")
