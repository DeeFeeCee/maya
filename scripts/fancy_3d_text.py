"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║   ██╗  ██╗███████╗██╗     ██╗      ██████╗     ██╗    ██╗ ██████╗ ██████╗     ║
║   ██║  ██║██╔════╝██║     ██║     ██╔═══██╗    ██║    ██║██╔═══██╗██╔══██╗    ║
║   ███████║█████╗  ██║     ██║     ██║   ██║    ██║ █╗ ██║██║   ██║██████╔╝    ║
║   ██╔══██║██╔══╝  ██║     ██║     ██║   ██║    ██║███╗██║██║   ██║██╔══██╗    ║
║   ██║  ██║███████╗███████╗███████╗╚██████╔╝    ╚███╔███╔╝╚██████╔╝██║  ██║    ║
║   ╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝ ╚═════╝      ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝    ║
║                                                                               ║
║                    🌟 FANCY 3D TEXT GENERATOR FOR MAYA 🌟                      ║
║                                                                               ║
║   Author: Douglas's Maya Python Tools                                         ║
║   Version: 1.0.0                                                              ║
║   Description: Creates stunning 3D text with animations and effects           ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""

import maya.cmds as cmds
import maya.mel as mel
import random
import math

# ═══════════════════════════════════════════════════════════════════════════════
#                              🎨 COLOR PRESETS
# ═══════════════════════════════════════════════════════════════════════════════

COLOR_PRESETS = {
    "rainbow": [
        (1.0, 0.2, 0.2),    # Red
        (1.0, 0.5, 0.0),    # Orange
        (1.0, 1.0, 0.0),    # Yellow
        (0.0, 1.0, 0.3),    # Green
        (0.0, 0.8, 1.0),    # Cyan
        (0.3, 0.3, 1.0),    # Blue
        (0.8, 0.2, 1.0),    # Purple
    ],
    "fire": [
        (1.0, 0.9, 0.0),    # Bright Yellow
        (1.0, 0.6, 0.0),    # Orange
        (1.0, 0.2, 0.0),    # Red-Orange
        (0.8, 0.0, 0.0),    # Dark Red
    ],
    "ice": [
        (0.9, 1.0, 1.0),    # White
        (0.6, 0.9, 1.0),    # Light Blue
        (0.2, 0.6, 1.0),    # Blue
        (0.1, 0.3, 0.8),    # Deep Blue
    ],
    "neon": [
        (1.0, 0.0, 0.5),    # Hot Pink
        (0.0, 1.0, 1.0),    # Cyan
        (0.5, 0.0, 1.0),    # Purple
        (0.0, 1.0, 0.5),    # Green
    ],
    "gold": [
        (1.0, 0.95, 0.6),   # Light Gold
        (1.0, 0.84, 0.0),   # Gold
        (0.85, 0.65, 0.13), # Goldenrod
        (0.72, 0.53, 0.04), # Dark Gold
    ],
    "sunset": [
        (1.0, 0.4, 0.4),    # Coral
        (1.0, 0.6, 0.2),    # Orange
        (1.0, 0.8, 0.4),    # Peach
        (0.8, 0.4, 0.6),    # Mauve
        (0.5, 0.3, 0.7),    # Purple
    ],
}


# ═══════════════════════════════════════════════════════════════════════════════
#                           🔧 UTILITY FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def create_material(name, color, emission=0.0, metallic=0.0):
    """
    Create a shiny material with optional glow effect.
    
    Args:
        name (str): Material name
        color (tuple): RGB color values (0-1)
        emission (float): Glow intensity (0-1)
        metallic (float): Metallic look (0-1)
    
    Returns:
        str: Name of the created shader
    """
    # Create shader
    shader = cmds.shadingNode('aiStandardSurface', asShader=True, name=f"{name}_shader")
    shading_group = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=f"{name}_SG")
    cmds.connectAttr(f"{shader}.outColor", f"{shading_group}.surfaceShader", force=True)
    
    # Set base color
    cmds.setAttr(f"{shader}.baseColor", *color, type="double3")
    cmds.setAttr(f"{shader}.base", 1.0)
    
    # Add emission for glow
    if emission > 0:
        cmds.setAttr(f"{shader}.emission", emission)
        cmds.setAttr(f"{shader}.emissionColor", *color, type="double3")
    
    # Metallic properties
    cmds.setAttr(f"{shader}.metalness", metallic)
    cmds.setAttr(f"{shader}.specular", 0.8)
    cmds.setAttr(f"{shader}.specularRoughness", 0.2)
    
    return shader, shading_group


def create_blinn_material(name, color, glow=0.0):
    """
    Create a Blinn material (works without Arnold).
    
    Args:
        name (str): Material name
        color (tuple): RGB color values (0-1)
        glow (float): Incandescence intensity (0-1)
    
    Returns:
        str: Name of the created shader
    """
    shader = cmds.shadingNode('blinn', asShader=True, name=f"{name}_shader")
    shading_group = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=f"{name}_SG")
    cmds.connectAttr(f"{shader}.outColor", f"{shading_group}.surfaceShader", force=True)
    
    # Set color
    cmds.setAttr(f"{shader}.color", *color, type="double3")
    
    # Shiny properties
    cmds.setAttr(f"{shader}.eccentricity", 0.3)
    cmds.setAttr(f"{shader}.specularRollOff", 0.7)
    cmds.setAttr(f"{shader}.specularColor", 1, 1, 1, type="double3")
    cmds.setAttr(f"{shader}.reflectivity", 0.2)
    
    # Glow effect
    if glow > 0:
        cmds.setAttr(f"{shader}.incandescence", 
                     color[0] * glow, 
                     color[1] * glow, 
                     color[2] * glow, 
                     type="double3")
    
    return shader, shading_group


def assign_material(obj, shading_group):
    """Assign a material to an object."""
    cmds.sets(obj, edit=True, forceElement=shading_group)


# ═══════════════════════════════════════════════════════════════════════════════
#                          ✨ MAIN TEXT CREATION
# ═══════════════════════════════════════════════════════════════════════════════

# Maya font candidates - these need EXACT Maya font names with style suffixes
# Maya uses format: "FontFamily - Style Width" e.g. "Arial - Bold UltraCondensed"
MAYA_FONT_CANDIDATES = [
    # These are fallback patterns - we prefer using fontDialog results
    "Arial - UltraCondensed",
    "Arial - Bold UltraCondensed", 
    "Times New Roman - UltraCondensed",
    "Courier New - UltraCondensed",
    "Verdana - UltraCondensed",
    "Tahoma - UltraCondensed",
    "Georgia - UltraCondensed",
    "Impact - UltraCondensed",
]


def get_maya_fonts():
    """
    Get list of fonts available in Maya using MEL.
    This is the most reliable way to get available fonts.
    Returns the EXACT font names Maya expects.
    """
    try:
        # This MEL command returns all available fonts with exact names
        fonts = mel.eval('fontDialog -FontList')
        if fonts:
            return fonts
    except Exception:
        pass
    return []


def get_available_font(preferred_font=None):
    """
    Get a font that's available in Maya.
    Returns the preferred font if available, otherwise finds a working fallback.
    
    IMPORTANT: Maya requires exact font names from fontDialog -FontList
    Simple names like "Arial" don't work - need "Arial - UltraCondensed" etc.
    """
    # First, get Maya's ACTUAL font list - this is the key!
    maya_fonts = get_maya_fonts()
    
    # Try preferred font first (if it's an exact match)
    if preferred_font:
        if maya_fonts and preferred_font in maya_fonts:
            return preferred_font
        # Try finding a font that STARTS with the preferred name
        if maya_fonts:
            for font in maya_fonts:
                if font.lower().startswith(preferred_font.lower()):
                    print(f"  ✓ Found matching font: {font}")
                    return font
        print(f"  ⚠️ Font '{preferred_font}' not found, using first available...")
    
    # Use the first available font from Maya's list
    if maya_fonts and len(maya_fonts) > 0:
        # Try to find a simple/common font first
        preferred_starters = ["Arial", "Times", "Verdana", "Tahoma", "Courier"]
        for starter in preferred_starters:
            for font in maya_fonts:
                if font.startswith(starter):
                    print(f"  ✓ Using font: {font}")
                    return font
        
        # Just use the first one
        print(f"  ✓ Using font: {maya_fonts[0]}")
        return maya_fonts[0]
    
    # Fallback to our candidates (unlikely to work but try anyway)
    for font in MAYA_FONT_CANDIDATES:
        try:
            test = cmds.textCurves(font=font, text="A")
            if test:
                cmds.delete(test)
                print(f"  ✓ Using font: {font}")
                return font
        except Exception:
            continue
    
    # Absolute last resort
    print("  ⚠️ Could not detect fonts - Maya may have font issues")
    return "Arial - UltraCondensed"


def list_available_fonts():
    """
    Print all fonts available in Maya.
    Run this to see what fonts you can use!
    """
    print("\n" + "═" * 50)
    print("📋 AVAILABLE FONTS IN MAYA")
    print("═" * 50)
    
    # Get Maya's font list via MEL
    maya_fonts = get_maya_fonts()
    
    if maya_fonts:
        print(f"\nFound {len(maya_fonts)} fonts via Maya:\n")
        for font in maya_fonts[:20]:  # Show first 20
            print(f"  ✓ {font}")
        if len(maya_fonts) > 20:
            print(f"  ... and {len(maya_fonts) - 20} more")
        
        # Show some useful ones
        print("\n📌 Recommended fonts for 3D text:")
        preferred = ["Arial", "Times", "Impact", "Verdana"]
        for p in preferred:
            matches = [f for f in maya_fonts if f.startswith(p)]
            if matches:
                print(f"  ⭐ {matches[0]}")
    else:
        print("\n⚠️ Could not get font list from Maya")
        print("Try running: mel.eval('fontDialog -FontList')")
    
    print("═" * 50 + "\n")
    return maya_fonts if maya_fonts else []


def create_3d_text(
    text="HELLO WORLD",
    font=None,  # None = auto-detect best available font
    extrude_depth=0.5,
    bevel_width=0.1,
    bevel_depth=0.05,
    color_preset="rainbow",
    per_letter_colors=True,
    add_glow=True,
    glow_intensity=0.3,
    add_animation=True,
    animation_type="wave",
    letter_spacing=0.2,
    scale=1.0
):
    """
    ╔═══════════════════════════════════════════════════════════════════════════╗
    ║                    🌟 CREATE FANCY 3D TEXT IN MAYA 🌟                      ║
    ╠═══════════════════════════════════════════════════════════════════════════╣
    ║                                                                           ║
    ║  Creates stunning 3D extruded text with bevels, materials, and optional   ║
    ║  animations. Perfect for titles, logos, and motion graphics!              ║
    ║                                                                           ║
    ╚═══════════════════════════════════════════════════════════════════════════╝
    
    Args:
        text (str): The text to create (default: "HELLO WORLD")
        font (str): Font family name (default: None = auto-detect)
                    Run list_available_fonts() to see available fonts
        extrude_depth (float): How deep to extrude (default: 0.5)
        bevel_width (float): Width of bevel edges (default: 0.1)
        bevel_depth (float): Depth of bevels (default: 0.05)
        color_preset (str): Color scheme - "rainbow", "fire", "ice", "neon", "gold", "sunset"
        per_letter_colors (bool): Different color per letter (default: True)
        add_glow (bool): Add glowing effect (default: True)
        glow_intensity (float): How strong the glow is (default: 0.3)
        add_animation (bool): Animate the text (default: True)
        animation_type (str): "wave", "bounce", "spin", "pop" (default: "wave")
        letter_spacing (float): Space between letters (default: 0.2)
        scale (float): Overall scale multiplier (default: 1.0)
    
    Returns:
        tuple: (main_group, list_of_letter_meshes)
    
    Example:
        >>> create_3d_text("MAYA", color_preset="fire", animation_type="bounce")
        >>> create_3d_text("PYTHON", color_preset="neon", add_animation=False)
    """
    
    print("\n" + "═" * 60)
    print("✨ Creating Fancy 3D Text: " + text)
    print("═" * 60)
    
    # Find a working font - ALWAYS get a font, never None
    working_font = get_available_font(font)
    print(f"  🔤 Using font: {working_font}")
    
    # Get colors
    colors = COLOR_PRESETS.get(color_preset, COLOR_PRESETS["rainbow"])
    
    # Store created objects
    letter_meshes = []
    letter_groups = []
    current_x = 0
    
    # Create each letter
    for i, char in enumerate(text):
        if char == " ":
            current_x += 0.8 * scale  # Space width
            continue
        
        print(f"  📝 Creating letter: {char}")
        
        # Create text curves - ALWAYS specify font
        try:
            text_curves = cmds.textCurves(
                font=working_font,
                text=char,
                name=f"letter_{char}_{i}"
            )
        except Exception as e:
            print(f"  ⚠️ Could not create letter '{char}': {e}")
            continue
        
        # Get all curve shapes under the text group
        curve_transform = text_curves[0]
        all_curves = cmds.listRelatives(curve_transform, allDescendents=True, type="nurbsCurve")
        
        if not all_curves:
            cmds.delete(curve_transform)
            continue
        
        # Get curve transforms
        curve_transforms = list(set([cmds.listRelatives(c, parent=True)[0] for c in all_curves]))
        
        # Create planar surface and extrude each curve
        extruded_meshes = []
        
        for curve_t in curve_transforms:
            try:
                # Create planar trim surface
                planar = cmds.planarSrf(curve_t, ch=False, tolerance=0.01, degree=3)
                if planar:
                    # Convert NURBS to poly and extrude
                    poly_mesh = cmds.nurbsToPoly(planar[0], mnd=1, ch=False, f=2, pt=1, 
                                                  pc=200, chr=0.9, ft=0.01, mel=0.001,
                                                  d=0.1, ut=1, un=3, vt=1, vn=3)[0]
                    
                    # Extrude the polygon
                    cmds.polyExtrudeFacet(poly_mesh + ".f[*]", 
                                          kft=True, 
                                          ltz=extrude_depth * scale,
                                          divisions=1)
                    
                    # Add bevel
                    if bevel_width > 0:
                        edges = cmds.polyListComponentConversion(poly_mesh, toEdge=True)
                        cmds.polyBevel3(edges, 
                                       offsetAsFraction=False,
                                       offset=bevel_width * scale * 0.5,
                                       segments=2,
                                       depth=bevel_depth,
                                       chamfer=False)
                    
                    extruded_meshes.append(poly_mesh)
                    cmds.delete(planar)
                    
            except Exception as e:
                print(f"    ⚠️ Could not extrude curve: {e}")
                continue
        
        # Combine meshes for this letter
        if extruded_meshes:
            if len(extruded_meshes) > 1:
                letter_mesh = cmds.polyUnite(extruded_meshes, ch=False, name=f"letter_{char}_{i}_mesh")[0]
            else:
                letter_mesh = cmds.rename(extruded_meshes[0], f"letter_{char}_{i}_mesh")
            
            # Center pivot
            cmds.xform(letter_mesh, centerPivots=True)
            
            # Get bounding box for positioning
            bbox = cmds.exactWorldBoundingBox(letter_mesh)
            letter_width = bbox[3] - bbox[0]
            
            # Position letter
            cmds.move(current_x - bbox[0], 0, 0, letter_mesh, relative=True)
            current_x += letter_width + letter_spacing * scale
            
            # Create and assign material
            color_index = i % len(colors)
            color = colors[color_index] if per_letter_colors else colors[0]
            glow = glow_intensity if add_glow else 0
            
            try:
                shader, sg = create_material(f"letter_{char}_{i}_mat", color, emission=glow, metallic=0.3)
            except:
                # Fallback to Blinn if Arnold not available
                shader, sg = create_blinn_material(f"letter_{char}_{i}_mat", color, glow=glow)
            
            assign_material(letter_mesh, sg)
            
            # Create letter group for animation
            letter_grp = cmds.group(letter_mesh, name=f"letter_{char}_{i}_grp")
            cmds.xform(letter_grp, pivots=[cmds.xform(letter_mesh, q=True, ws=True, rp=True)[0],
                                            0, 0], ws=True)
            
            letter_meshes.append(letter_mesh)
            letter_groups.append(letter_grp)
        
        # Cleanup original curves
        if cmds.objExists(curve_transform):
            cmds.delete(curve_transform)
    
    # Create main group
    if letter_groups:
        main_group = cmds.group(letter_groups, name=f"text_{text.replace(' ', '_')}_grp")
        
        # Center the entire text
        bbox = cmds.exactWorldBoundingBox(main_group)
        center_x = (bbox[0] + bbox[3]) / 2
        cmds.move(-center_x, 0, 0, main_group, relative=True)
        
        # Scale
        cmds.scale(scale, scale, scale, main_group)
        
        # Freeze transforms
        cmds.makeIdentity(main_group, apply=True, t=True, r=True, s=True)
        
        # ═══════════════════════════════════════════════════════════════════
        #                         🎬 ANIMATION
        # ═══════════════════════════════════════════════════════════════════
        
        if add_animation and letter_groups:
            print(f"\n  🎬 Adding {animation_type} animation...")
            
            cmds.playbackOptions(minTime=1, maxTime=120, animationStartTime=1, animationEndTime=120)
            
            for i, grp in enumerate(letter_groups):
                offset = i * 5  # Stagger animation
                
                if animation_type == "wave":
                    # Wave animation - letters move up and down
                    for frame in range(1, 121, 10):
                        cmds.setKeyframe(grp, attribute='translateY', 
                                        value=math.sin((frame + offset) * 0.15) * 0.5 * scale,
                                        time=frame)
                    
                elif animation_type == "bounce":
                    # Bounce animation
                    cmds.setKeyframe(grp, attribute='translateY', value=0, time=1 + offset)
                    cmds.setKeyframe(grp, attribute='translateY', value=1.5 * scale, time=15 + offset)
                    cmds.setKeyframe(grp, attribute='translateY', value=0, time=30 + offset)
                    cmds.setKeyframe(grp, attribute='translateY', value=0.5 * scale, time=40 + offset)
                    cmds.setKeyframe(grp, attribute='translateY', value=0, time=50 + offset)
                    # Make it loop
                    cmds.setKeyframe(grp, attribute='translateY', value=0, time=70 + offset)
                    cmds.setKeyframe(grp, attribute='translateY', value=1.5 * scale, time=85 + offset)
                    cmds.setKeyframe(grp, attribute='translateY', value=0, time=100 + offset)
                    
                elif animation_type == "spin":
                    # Spin animation - each letter rotates
                    cmds.setKeyframe(grp, attribute='rotateY', value=0, time=1)
                    cmds.setKeyframe(grp, attribute='rotateY', value=360, time=60 + offset)
                    cmds.setKeyframe(grp, attribute='rotateY', value=720, time=120)
                    
                elif animation_type == "pop":
                    # Pop in animation
                    cmds.setKeyframe(grp, attribute='scaleX', value=0, time=1 + offset)
                    cmds.setKeyframe(grp, attribute='scaleY', value=0, time=1 + offset)
                    cmds.setKeyframe(grp, attribute='scaleZ', value=0, time=1 + offset)
                    
                    cmds.setKeyframe(grp, attribute='scaleX', value=1.3, time=10 + offset)
                    cmds.setKeyframe(grp, attribute='scaleY', value=1.3, time=10 + offset)
                    cmds.setKeyframe(grp, attribute='scaleZ', value=1.3, time=10 + offset)
                    
                    cmds.setKeyframe(grp, attribute='scaleX', value=1, time=20 + offset)
                    cmds.setKeyframe(grp, attribute='scaleY', value=1, time=20 + offset)
                    cmds.setKeyframe(grp, attribute='scaleZ', value=1, time=20 + offset)
            
            # Set keyframe tangents for smooth animation
            cmds.keyTangent(letter_groups, edit=True, inTangentType='spline', outTangentType='spline')
        
        print("\n" + "═" * 60)
        print("✅ SUCCESS! 3D Text created: " + text)
        print("═" * 60)
        print(f"  📦 Main Group: {main_group}")
        print(f"  🔤 Letters: {len(letter_meshes)}")
        print(f"  🎨 Color Preset: {color_preset}")
        if add_animation:
            print(f"  🎬 Animation: {animation_type}")
        print("═" * 60 + "\n")
        
        return main_group, letter_meshes
    
    return None, []


# ═══════════════════════════════════════════════════════════════════════════════
#                           🖥️ USER INTERFACE
# ═══════════════════════════════════════════════════════════════════════════════

def show_ui():
    """
    ╔═══════════════════════════════════════════════════════════════════════════╗
    ║                     🎮 FANCY 3D TEXT GENERATOR UI 🎮                       ║
    ╚═══════════════════════════════════════════════════════════════════════════╝
    
    Opens a user-friendly window to create 3D text with all options.
    """
    
    window_name = "fancy3DTextWindow"
    
    # Delete existing window
    if cmds.window(window_name, exists=True):
        cmds.deleteUI(window_name)
    
    # Create window
    window = cmds.window(
        window_name,
        title="✨ Fancy 3D Text Generator ✨",
        widthHeight=(400, 500),
        sizeable=True
    )
    
    # Main layout
    main_layout = cmds.columnLayout(adjustableColumn=True, rowSpacing=10, columnOffset=["both", 10])
    
    cmds.separator(height=10, style="none")
    
    # Header
    cmds.text(label="🌟 FANCY 3D TEXT GENERATOR 🌟", font="boldLabelFont", height=30)
    cmds.text(label="Create stunning 3D text with animations!", font="smallPlainLabelFont")
    
    cmds.separator(height=20, style="in")
    
    # ═══════════════════════════════════════════════════════════════════════
    #                           TEXT OPTIONS
    # ═══════════════════════════════════════════════════════════════════════
    
    cmds.frameLayout(label="📝 Text Options", collapsable=True, collapse=False)
    cmds.columnLayout(adjustableColumn=True, rowSpacing=5, columnOffset=["both", 5])
    
    text_field = cmds.textFieldGrp(label="Text:", text="HELLO WORLD", columnWidth=[(1, 80), (2, 280)])
    font_field = cmds.textFieldGrp(label="Font:", text="", placeholderText="(auto-detect)", 
                                   columnWidth=[(1, 80), (2, 280)],
                                   annotation="Leave empty for auto-detect, or run list_available_fonts()")
    
    cmds.setParent('..')
    cmds.setParent('..')
    
    # ═══════════════════════════════════════════════════════════════════════
    #                          GEOMETRY OPTIONS  
    # ═══════════════════════════════════════════════════════════════════════
    
    cmds.frameLayout(label="📐 Geometry", collapsable=True, collapse=False)
    cmds.columnLayout(adjustableColumn=True, rowSpacing=5, columnOffset=["both", 5])
    
    extrude_slider = cmds.floatSliderGrp(label="Extrude Depth:", field=True, 
                                          minValue=0.1, maxValue=2.0, value=0.5,
                                          columnWidth=[(1, 100), (2, 60), (3, 200)])
    bevel_slider = cmds.floatSliderGrp(label="Bevel Width:", field=True,
                                        minValue=0.0, maxValue=0.5, value=0.1,
                                        columnWidth=[(1, 100), (2, 60), (3, 200)])
    scale_slider = cmds.floatSliderGrp(label="Scale:", field=True,
                                        minValue=0.1, maxValue=5.0, value=1.0,
                                        columnWidth=[(1, 100), (2, 60), (3, 200)])
    spacing_slider = cmds.floatSliderGrp(label="Letter Spacing:", field=True,
                                          minValue=0.0, maxValue=1.0, value=0.2,
                                          columnWidth=[(1, 100), (2, 60), (3, 200)])
    
    cmds.setParent('..')
    cmds.setParent('..')
    
    # ═══════════════════════════════════════════════════════════════════════
    #                           COLOR OPTIONS
    # ═══════════════════════════════════════════════════════════════════════
    
    cmds.frameLayout(label="🎨 Colors", collapsable=True, collapse=False)
    cmds.columnLayout(adjustableColumn=True, rowSpacing=5, columnOffset=["both", 5])
    
    color_menu = cmds.optionMenuGrp(label="Color Preset:", columnWidth=[(1, 100)])
    cmds.menuItem(label="🌈 Rainbow")
    cmds.menuItem(label="🔥 Fire")
    cmds.menuItem(label="❄️ Ice")
    cmds.menuItem(label="💜 Neon")
    cmds.menuItem(label="✨ Gold")
    cmds.menuItem(label="🌅 Sunset")
    
    per_letter_check = cmds.checkBoxGrp(label="Per-Letter Colors:", value1=True, columnWidth=[(1, 100)])
    glow_check = cmds.checkBoxGrp(label="Add Glow:", value1=True, columnWidth=[(1, 100)])
    glow_slider = cmds.floatSliderGrp(label="Glow Intensity:", field=True,
                                       minValue=0.0, maxValue=1.0, value=0.3,
                                       columnWidth=[(1, 100), (2, 60), (3, 200)])
    
    cmds.setParent('..')
    cmds.setParent('..')
    
    # ═══════════════════════════════════════════════════════════════════════
    #                         ANIMATION OPTIONS
    # ═══════════════════════════════════════════════════════════════════════
    
    cmds.frameLayout(label="🎬 Animation", collapsable=True, collapse=False)
    cmds.columnLayout(adjustableColumn=True, rowSpacing=5, columnOffset=["both", 5])
    
    anim_check = cmds.checkBoxGrp(label="Add Animation:", value1=True, columnWidth=[(1, 100)])
    
    anim_menu = cmds.optionMenuGrp(label="Animation Type:", columnWidth=[(1, 100)])
    cmds.menuItem(label="🌊 Wave")
    cmds.menuItem(label="⬆️ Bounce")
    cmds.menuItem(label="🔄 Spin")
    cmds.menuItem(label="💥 Pop")
    
    cmds.setParent('..')
    cmds.setParent('..')
    
    cmds.separator(height=20, style="in")
    
    # ═══════════════════════════════════════════════════════════════════════
    #                           CREATE BUTTON
    # ═══════════════════════════════════════════════════════════════════════
    
    def on_create(*args):
        """Callback for create button."""
        # Get values
        text = cmds.textFieldGrp(text_field, query=True, text=True)
        font = cmds.textFieldGrp(font_field, query=True, text=True)
        # Use None for empty font to trigger auto-detect
        if not font or font.strip() == "":
            font = None
        extrude = cmds.floatSliderGrp(extrude_slider, query=True, value=True)
        bevel = cmds.floatSliderGrp(bevel_slider, query=True, value=True)
        scale = cmds.floatSliderGrp(scale_slider, query=True, value=True)
        spacing = cmds.floatSliderGrp(spacing_slider, query=True, value=True)
        
        # Color preset (remove emoji prefix)
        color_preset_raw = cmds.optionMenuGrp(color_menu, query=True, value=True)
        color_map = {
            "🌈 Rainbow": "rainbow", "🔥 Fire": "fire", "❄️ Ice": "ice",
            "💜 Neon": "neon", "✨ Gold": "gold", "🌅 Sunset": "sunset"
        }
        color_preset = color_map.get(color_preset_raw, "rainbow")
        
        per_letter = cmds.checkBoxGrp(per_letter_check, query=True, value1=True)
        add_glow = cmds.checkBoxGrp(glow_check, query=True, value1=True)
        glow_intensity = cmds.floatSliderGrp(glow_slider, query=True, value=True)
        add_anim = cmds.checkBoxGrp(anim_check, query=True, value1=True)
        
        # Animation type
        anim_raw = cmds.optionMenuGrp(anim_menu, query=True, value=True)
        anim_map = {
            "🌊 Wave": "wave", "⬆️ Bounce": "bounce", 
            "🔄 Spin": "spin", "💥 Pop": "pop"
        }
        anim_type = anim_map.get(anim_raw, "wave")
        
        # Create the text!
        create_3d_text(
            text=text,
            font=font,
            extrude_depth=extrude,
            bevel_width=bevel,
            bevel_depth=bevel * 0.5,
            color_preset=color_preset,
            per_letter_colors=per_letter,
            add_glow=add_glow,
            glow_intensity=glow_intensity,
            add_animation=add_anim,
            animation_type=anim_type,
            letter_spacing=spacing,
            scale=scale
        )
    
    cmds.button(
        label="✨ CREATE 3D TEXT ✨",
        height=50,
        backgroundColor=(0.2, 0.6, 0.4),
        command=on_create
    )
    
    cmds.separator(height=10, style="none")
    
    cmds.text(label="💡 Tip: Press Play to see animations!", font="smallPlainLabelFont")
    
    cmds.separator(height=10, style="none")
    
    # Show window
    cmds.showWindow(window)
    
    print("\n✨ Fancy 3D Text Generator UI opened! ✨\n")


# ═══════════════════════════════════════════════════════════════════════════════
#                              🚀 QUICK START
# ═══════════════════════════════════════════════════════════════════════════════

def hello_world():
    """
    Quick function to create a Hello World with default fancy settings.
    Just run: hello_world()
    """
    return create_3d_text(
        text="HELLO WORLD",
        color_preset="rainbow",
        animation_type="wave",
        add_glow=True,
        glow_intensity=0.3
    )


# ═══════════════════════════════════════════════════════════════════════════════
#                              📋 EXAMPLES
# ═══════════════════════════════════════════════════════════════════════════════

"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                              📋 USAGE EXAMPLES                                 ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║  # Open the UI:                                                               ║
║  show_ui()                                                                    ║
║                                                                               ║
║  # Quick Hello World:                                                         ║
║  hello_world()                                                                ║
║                                                                               ║
║  # Custom text with fire colors:                                              ║
║  create_3d_text("MAYA", color_preset="fire", animation_type="bounce")         ║
║                                                                               ║
║  # Neon style with spin animation:                                            ║
║  create_3d_text("PYTHON", color_preset="neon", animation_type="spin")         ║
║                                                                               ║
║  # Gold text, no animation:                                                   ║
║  create_3d_text("GOLD", color_preset="gold", add_animation=False)             ║
║                                                                               ║
║  # Large sunset text with pop animation:                                      ║
║  create_3d_text("BIG", color_preset="sunset", animation_type="pop", scale=3)  ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""

# ═══════════════════════════════════════════════════════════════════════════════
#                           🎉 AUTO-RUN UI ON LOAD
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    show_ui()
