"""
Starship Generator for Maya
===========================
Creates a cool 3D starship using only primitives - no fonts needed!

Author: Douglas's Learning Project
Version: 1.0.0

Usage in Maya:
    from starship import create_starship, create_fleet, show_ui
    create_starship()      # Create one starship
    create_fleet(5)        # Create a fleet of 5
    show_ui()              # Open the UI
"""

import maya.cmds as cmds
import random

# ═══════════════════════════════════════════════════════════════════════════════
# COLOR PRESETS FOR STARSHIPS
# ═══════════════════════════════════════════════════════════════════════════════

SHIP_COLORS = {
    "classic": {
        "hull": (0.7, 0.7, 0.75),      # Silver-gray
        "accent": (0.2, 0.4, 0.8),      # Blue
        "engine": (0.0, 0.8, 1.0),      # Cyan glow
        "cockpit": (0.2, 0.3, 0.4),     # Dark glass
    },
    "rebel": {
        "hull": (0.9, 0.9, 0.85),       # Off-white
        "accent": (1.0, 0.4, 0.0),      # Orange
        "engine": (1.0, 0.3, 0.1),      # Orange-red glow
        "cockpit": (0.1, 0.1, 0.15),    # Dark
    },
    "imperial": {
        "hull": (0.3, 0.3, 0.35),       # Dark gray
        "accent": (0.1, 0.1, 0.1),      # Black
        "engine": (0.0, 0.5, 1.0),      # Blue glow
        "cockpit": (0.05, 0.05, 0.1),   # Very dark
    },
    "pirate": {
        "hull": (0.4, 0.2, 0.1),        # Rusty brown
        "accent": (0.8, 0.0, 0.0),      # Red
        "engine": (1.0, 0.5, 0.0),      # Fire orange
        "cockpit": (0.2, 0.1, 0.05),    # Dark brown
    },
    "alien": {
        "hull": (0.2, 0.5, 0.3),        # Green
        "accent": (0.6, 0.0, 0.8),      # Purple
        "engine": (0.0, 1.0, 0.5),      # Green glow
        "cockpit": (0.1, 0.2, 0.15),    # Dark green
    },
}


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN STARSHIP CREATION FUNCTION
# ═══════════════════════════════════════════════════════════════════════════════

def create_starship(
    name="starship",
    ship_type="fighter",
    color_scheme="classic",
    scale=1.0,
    add_animation=True
):
    """
    Create a 3D starship using Maya primitives.
    
    Args:
        name (str): Name for the starship group
        ship_type (str): "fighter", "cruiser", "bomber", or "scout"
        color_scheme (str): "classic", "rebel", "imperial", "pirate", "alien"
        scale (float): Size multiplier
        add_animation (bool): Add engine glow animation
    
    Returns:
        str: Name of the created starship group
    
    Example:
        >>> create_starship("my_ship", ship_type="fighter", color_scheme="rebel")
    """
    
    print("\n" + "═" * 50)
    print(f"🚀 Creating Starship: {name}")
    print(f"   Type: {ship_type} | Colors: {color_scheme}")
    print("═" * 50)
    
    colors = SHIP_COLORS.get(color_scheme, SHIP_COLORS["classic"])
    
    # Create main group
    ship_group = cmds.group(empty=True, name=f"{name}_grp")
    
    # Build based on ship type
    if ship_type == "fighter":
        build_fighter(ship_group, colors, scale)
    elif ship_type == "cruiser":
        build_cruiser(ship_group, colors, scale)
    elif ship_type == "bomber":
        build_bomber(ship_group, colors, scale)
    elif ship_type == "scout":
        build_scout(ship_group, colors, scale)
    else:
        build_fighter(ship_group, colors, scale)  # Default
    
    # Add animation
    if add_animation:
        add_engine_animation(ship_group, colors["engine"])
    
    # Center pivot
    cmds.xform(ship_group, centerPivots=True)
    
    print("═" * 50)
    print(f"✅ Starship '{name}' created successfully!")
    print("═" * 50 + "\n")
    
    return ship_group


# ═══════════════════════════════════════════════════════════════════════════════
# SHIP TYPE BUILDERS
# ═══════════════════════════════════════════════════════════════════════════════

def build_fighter(group, colors, scale):
    """Build a sleek fighter ship."""
    s = scale
    
    # Main fuselage (elongated cone/cylinder)
    fuselage = cmds.polyCylinder(r=0.3*s, h=3*s, sx=8, sy=1, sz=1, ax=[0,0,1])[0]
    cmds.move(0, 0, 0, fuselage)
    apply_material(fuselage, colors["hull"], "hull_mat")
    
    # Nose cone
    nose = cmds.polyCone(r=0.3*s, h=1*s, sx=8, sy=1, sz=0, ax=[0,0,1])[0]
    cmds.move(0, 0, 2*s, nose)
    apply_material(nose, colors["hull"], "nose_mat")
    
    # Cockpit (glass dome)
    cockpit = cmds.polySphere(r=0.25*s, sx=8, sy=8)[0]
    cmds.scale(1, 0.6, 1.2, cockpit)
    cmds.move(0, 0.2*s, 0.5*s, cockpit)
    apply_material(cockpit, colors["cockpit"], "cockpit_mat", transparency=0.3)
    
    # Wings (left and right)
    wing_l = cmds.polyCube(w=2*s, h=0.05*s, d=1*s)[0]
    cmds.move(-1*s, 0, -0.3*s, wing_l)
    cmds.rotate(0, 0, -10, wing_l)
    apply_material(wing_l, colors["accent"], "wing_l_mat")
    
    wing_r = cmds.polyCube(w=2*s, h=0.05*s, d=1*s)[0]
    cmds.move(1*s, 0, -0.3*s, wing_r)
    cmds.rotate(0, 0, 10, wing_r)
    apply_material(wing_r, colors["accent"], "wing_r_mat")
    
    # Engine pods
    engine_l = cmds.polyCylinder(r=0.15*s, h=0.8*s, ax=[0,0,1])[0]
    cmds.move(-0.5*s, -0.1*s, -1.3*s, engine_l)
    apply_material(engine_l, colors["hull"], "engine_l_mat")
    
    engine_r = cmds.polyCylinder(r=0.15*s, h=0.8*s, ax=[0,0,1])[0]
    cmds.move(0.5*s, -0.1*s, -1.3*s, engine_r)
    apply_material(engine_r, colors["hull"], "engine_r_mat")
    
    # Engine glow (spheres at back)
    glow_l = cmds.polySphere(r=0.12*s, sx=8, sy=8)[0]
    cmds.move(-0.5*s, -0.1*s, -1.7*s, glow_l)
    apply_material(glow_l, colors["engine"], "glow_l_mat", glow=True)
    
    glow_r = cmds.polySphere(r=0.12*s, sx=8, sy=8)[0]
    cmds.move(0.5*s, -0.1*s, -1.7*s, glow_r)
    apply_material(glow_r, colors["engine"], "glow_r_mat", glow=True)
    
    # Weapons (small cylinders on wings)
    weapon_l = cmds.polyCylinder(r=0.03*s, h=0.6*s, ax=[0,0,1])[0]
    cmds.move(-1.5*s, 0, 0.2*s, weapon_l)
    apply_material(weapon_l, colors["accent"], "weapon_l_mat")
    
    weapon_r = cmds.polyCylinder(r=0.03*s, h=0.6*s, ax=[0,0,1])[0]
    cmds.move(1.5*s, 0, 0.2*s, weapon_r)
    apply_material(weapon_r, colors["accent"], "weapon_r_mat")
    
    # Parent all to group
    for obj in [fuselage, nose, cockpit, wing_l, wing_r, engine_l, engine_r, 
                glow_l, glow_r, weapon_l, weapon_r]:
        cmds.parent(obj, group)
    
    print("  ✓ Fighter built with wings, engines, and weapons")


def build_cruiser(group, colors, scale):
    """Build a large cruiser ship."""
    s = scale
    
    # Main hull (long box)
    hull = cmds.polyCube(w=1*s, h=0.5*s, d=5*s)[0]
    cmds.move(0, 0, 0, hull)
    apply_material(hull, colors["hull"], "hull_mat")
    
    # Bridge (command tower)
    bridge = cmds.polyCube(w=0.4*s, h=0.4*s, d=0.6*s)[0]
    cmds.move(0, 0.45*s, 1*s, bridge)
    apply_material(bridge, colors["accent"], "bridge_mat")
    
    # Bridge windows
    windows = cmds.polyCube(w=0.35*s, h=0.15*s, d=0.1*s)[0]
    cmds.move(0, 0.5*s, 1.35*s, windows)
    apply_material(windows, colors["cockpit"], "windows_mat", transparency=0.3)
    
    # Engine block
    engine_block = cmds.polyCube(w=0.8*s, h=0.4*s, d=0.6*s)[0]
    cmds.move(0, 0, -2.5*s, engine_block)
    apply_material(engine_block, colors["hull"], "engine_block_mat")
    
    # Multiple engines
    engines = []
    for i in range(3):
        x_pos = (i - 1) * 0.25 * s
        eng = cmds.polyCylinder(r=0.1*s, h=0.3*s, ax=[0,0,1])[0]
        cmds.move(x_pos, 0, -2.9*s, eng)
        apply_material(eng, colors["engine"], f"eng_{i}_mat", glow=True)
        engines.append(eng)
    
    # Side hangars
    hangar_l = cmds.polyCube(w=0.3*s, h=0.3*s, d=1.5*s)[0]
    cmds.move(-0.65*s, -0.1*s, 0.5*s, hangar_l)
    apply_material(hangar_l, colors["accent"], "hangar_l_mat")
    
    hangar_r = cmds.polyCube(w=0.3*s, h=0.3*s, d=1.5*s)[0]
    cmds.move(0.65*s, -0.1*s, 0.5*s, hangar_r)
    apply_material(hangar_r, colors["accent"], "hangar_r_mat")
    
    # Antenna
    antenna = cmds.polyCylinder(r=0.02*s, h=0.5*s, ax=[0,1,0])[0]
    cmds.move(0, 0.9*s, 1*s, antenna)
    apply_material(antenna, colors["hull"], "antenna_mat")
    
    # Parent all
    all_parts = [hull, bridge, windows, engine_block, hangar_l, hangar_r, antenna] + engines
    for obj in all_parts:
        cmds.parent(obj, group)
    
    print("  ✓ Cruiser built with bridge, hangars, and engines")


def build_bomber(group, colors, scale):
    """Build a heavy bomber ship."""
    s = scale
    
    # Wide main body
    body = cmds.polyCube(w=2*s, h=0.6*s, d=2.5*s)[0]
    apply_material(body, colors["hull"], "body_mat")
    
    # Bomb bay (underneath)
    bay = cmds.polyCube(w=1*s, h=0.3*s, d=1.5*s)[0]
    cmds.move(0, -0.45*s, 0, bay)
    apply_material(bay, colors["accent"], "bay_mat")
    
    # Cockpit bubble
    cockpit = cmds.polySphere(r=0.35*s)[0]
    cmds.scale(1, 0.5, 1, cockpit)
    cmds.move(0, 0.3*s, 0.8*s, cockpit)
    apply_material(cockpit, colors["cockpit"], "cockpit_mat", transparency=0.3)
    
    # Twin tail fins
    fin_l = cmds.polyCube(w=0.05*s, h=0.6*s, d=0.5*s)[0]
    cmds.move(-0.8*s, 0.3*s, -1.2*s, fin_l)
    apply_material(fin_l, colors["accent"], "fin_l_mat")
    
    fin_r = cmds.polyCube(w=0.05*s, h=0.6*s, d=0.5*s)[0]
    cmds.move(0.8*s, 0.3*s, -1.2*s, fin_r)
    apply_material(fin_r, colors["accent"], "fin_r_mat")
    
    # Four engines
    engine_positions = [(-0.7, -0.2, -1.3), (0.7, -0.2, -1.3), 
                        (-0.7, 0.2, -1.3), (0.7, 0.2, -1.3)]
    engines = []
    for i, (x, y, z) in enumerate(engine_positions):
        eng = cmds.polyCylinder(r=0.15*s, h=0.5*s, ax=[0,0,1])[0]
        cmds.move(x*s, y*s, z*s, eng)
        apply_material(eng, colors["engine"], f"eng_{i}_mat", glow=True)
        engines.append(eng)
    
    # Turret on top
    turret_base = cmds.polyCylinder(r=0.2*s, h=0.15*s, ax=[0,1,0])[0]
    cmds.move(0, 0.35*s, -0.3*s, turret_base)
    apply_material(turret_base, colors["hull"], "turret_base_mat")
    
    turret_gun = cmds.polyCylinder(r=0.05*s, h=0.4*s, ax=[0,0,1])[0]
    cmds.move(0, 0.4*s, -0.1*s, turret_gun)
    apply_material(turret_gun, colors["accent"], "turret_gun_mat")
    
    # Parent all
    all_parts = [body, bay, cockpit, fin_l, fin_r, turret_base, turret_gun] + engines
    for obj in all_parts:
        cmds.parent(obj, group)
    
    print("  ✓ Bomber built with bomb bay, turret, and quad engines")


def build_scout(group, colors, scale):
    """Build a small fast scout ship."""
    s = scale
    
    # Sleek body (sphere stretched)
    body = cmds.polySphere(r=0.4*s, sx=12, sy=12)[0]
    cmds.scale(0.8, 0.5, 1.5, body)
    apply_material(body, colors["hull"], "body_mat")
    
    # Large cockpit (most of front)
    cockpit = cmds.polySphere(r=0.35*s, sx=8, sy=8)[0]
    cmds.scale(0.7, 0.4, 0.8, cockpit)
    cmds.move(0, 0.1*s, 0.35*s, cockpit)
    apply_material(cockpit, colors["cockpit"], "cockpit_mat", transparency=0.4)
    
    # Swept wings
    wing_l = cmds.polyPrism(l=0.8*s, w=0.6*s, ns=3, sh=1)[0]
    cmds.rotate(90, 0, -30, wing_l)
    cmds.scale(1.5, 0.1, 1, wing_l)
    cmds.move(-0.6*s, 0, -0.1*s, wing_l)
    apply_material(wing_l, colors["accent"], "wing_l_mat")
    
    wing_r = cmds.polyPrism(l=0.8*s, w=0.6*s, ns=3, sh=1)[0]
    cmds.rotate(90, 0, 30, wing_r)
    cmds.scale(1.5, 0.1, 1, wing_r)
    cmds.move(0.6*s, 0, -0.1*s, wing_r)
    apply_material(wing_r, colors["accent"], "wing_r_mat")
    
    # Single large engine
    engine = cmds.polyCone(r=0.25*s, h=0.4*s, ax=[0,0,1])[0]
    cmds.rotate(180, 0, 0, engine)
    cmds.move(0, 0, -0.8*s, engine)
    apply_material(engine, colors["hull"], "engine_mat")
    
    # Engine glow
    glow = cmds.polySphere(r=0.2*s, sx=8, sy=8)[0]
    cmds.move(0, 0, -0.95*s, glow)
    apply_material(glow, colors["engine"], "glow_mat", glow=True)
    
    # Sensor dish on nose
    sensor = cmds.polyCylinder(r=0.1*s, h=0.02*s, ax=[0,0,1])[0]
    cmds.move(0, 0, 0.65*s, sensor)
    apply_material(sensor, colors["accent"], "sensor_mat")
    
    # Parent all
    for obj in [body, cockpit, wing_l, wing_r, engine, glow, sensor]:
        cmds.parent(obj, group)
    
    print("  ✓ Scout built with large cockpit and single engine")


# ═══════════════════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def apply_material(obj, color, name, transparency=0.0, glow=False):
    """Apply a material to an object."""
    # Create material
    mat = cmds.shadingNode('blinn', asShader=True, name=name)
    sg = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=f'{name}_SG')
    cmds.connectAttr(f'{mat}.outColor', f'{sg}.surfaceShader')
    
    # Set color
    cmds.setAttr(f'{mat}.color', color[0], color[1], color[2], type='double3')
    
    # Shiny metal look
    cmds.setAttr(f'{mat}.specularColor', 0.8, 0.8, 0.8, type='double3')
    cmds.setAttr(f'{mat}.specularRollOff', 0.6)
    cmds.setAttr(f'{mat}.reflectivity', 0.2)
    
    # Transparency
    if transparency > 0:
        cmds.setAttr(f'{mat}.transparency', transparency, transparency, transparency, type='double3')
    
    # Glow effect
    if glow:
        cmds.setAttr(f'{mat}.incandescence', color[0]*0.8, color[1]*0.8, color[2]*0.8, type='double3')
        cmds.setAttr(f'{mat}.glowIntensity', 0.5)
    
    # Apply
    cmds.sets(obj, edit=True, forceElement=sg)


def add_engine_animation(group, engine_color):
    """Add pulsing animation to engine glows."""
    # Find glow objects
    children = cmds.listRelatives(group, allDescendents=True, type='transform') or []
    
    cmds.playbackOptions(min=1, max=60, ast=1, aet=60)
    
    for child in children:
        if 'glow' in child.lower():
            # Pulsing scale animation
            cmds.setKeyframe(child, attribute='scaleX', value=1.0, time=1)
            cmds.setKeyframe(child, attribute='scaleY', value=1.0, time=1)
            cmds.setKeyframe(child, attribute='scaleZ', value=1.0, time=1)
            
            cmds.setKeyframe(child, attribute='scaleX', value=1.2, time=15)
            cmds.setKeyframe(child, attribute='scaleY', value=1.2, time=15)
            cmds.setKeyframe(child, attribute='scaleZ', value=1.1, time=15)
            
            cmds.setKeyframe(child, attribute='scaleX', value=1.0, time=30)
            cmds.setKeyframe(child, attribute='scaleY', value=1.0, time=30)
            cmds.setKeyframe(child, attribute='scaleZ', value=1.0, time=30)
            
            cmds.setKeyframe(child, attribute='scaleX', value=1.15, time=45)
            cmds.setKeyframe(child, attribute='scaleY', value=1.15, time=45)
            cmds.setKeyframe(child, attribute='scaleZ', value=1.05, time=45)
            
            cmds.setKeyframe(child, attribute='scaleX', value=1.0, time=60)
            cmds.setKeyframe(child, attribute='scaleY', value=1.0, time=60)
            cmds.setKeyframe(child, attribute='scaleZ', value=1.0, time=60)


def create_fleet(count=3, formation="line"):
    """
    Create multiple starships in formation.
    
    Args:
        count (int): Number of ships
        formation (str): "line", "v", "diamond", or "random"
    """
    print(f"\n🚀 Creating fleet of {count} ships in {formation} formation...")
    
    ships = []
    ship_types = ["fighter", "fighter", "scout", "bomber", "cruiser"]
    color_schemes = list(SHIP_COLORS.keys())
    
    for i in range(count):
        ship_type = ship_types[i % len(ship_types)]
        color = color_schemes[i % len(color_schemes)]
        
        ship = create_starship(
            name=f"ship_{i+1}",
            ship_type=ship_type,
            color_scheme=color,
            scale=0.8 if ship_type != "cruiser" else 1.2,
            add_animation=True
        )
        
        # Position based on formation
        if formation == "line":
            cmds.move(i * 4, 0, 0, ship)
        elif formation == "v":
            x = (i - count//2) * 3
            z = -abs(i - count//2) * 2
            cmds.move(x, 0, z, ship)
        elif formation == "diamond":
            angle = (i / count) * 360
            import math
            x = math.cos(math.radians(angle)) * 5
            z = math.sin(math.radians(angle)) * 5
            cmds.move(x, 0, z, ship)
            cmds.rotate(0, -angle + 90, 0, ship)
        else:  # random
            x = random.uniform(-10, 10)
            y = random.uniform(-2, 2)
            z = random.uniform(-10, 10)
            cmds.move(x, y, z, ship)
            cmds.rotate(0, random.uniform(0, 360), 0, ship)
        
        ships.append(ship)
    
    # Group the fleet
    fleet_grp = cmds.group(ships, name="fleet_grp")
    print(f"\n✅ Fleet created with {count} ships!")
    
    return fleet_grp


# ═══════════════════════════════════════════════════════════════════════════════
# UI
# ═══════════════════════════════════════════════════════════════════════════════

def show_ui():
    """Show the starship generator UI."""
    window_name = "starshipUI"
    
    if cmds.window(window_name, exists=True):
        cmds.deleteUI(window_name)
    
    window = cmds.window(window_name, title="🚀 Starship Generator", 
                         widthHeight=(320, 380), sizeable=True)
    
    cmds.columnLayout(adjustableColumn=True, rowSpacing=8, columnOffset=["both", 10])
    
    cmds.separator(height=10)
    cmds.text(label="🚀 STARSHIP GENERATOR 🚀", font="boldLabelFont", height=25)
    cmds.text(label="Create cool spaceships with no fonts needed!", font="smallPlainLabelFont")
    cmds.separator(height=10)
    
    # Ship name
    cmds.text(label="Ship Name:", align="left")
    name_field = cmds.textField(text="my_starship")
    
    # Ship type
    cmds.text(label="Ship Type:", align="left")
    type_menu = cmds.optionMenu()
    cmds.menuItem(label="Fighter - Fast & agile")
    cmds.menuItem(label="Scout - Small & quick")
    cmds.menuItem(label="Bomber - Heavy firepower")
    cmds.menuItem(label="Cruiser - Large command ship")
    
    # Color scheme
    cmds.text(label="Color Scheme:", align="left")
    color_menu = cmds.optionMenu()
    cmds.menuItem(label="Classic - Silver & Blue")
    cmds.menuItem(label="Rebel - White & Orange")
    cmds.menuItem(label="Imperial - Dark Gray")
    cmds.menuItem(label="Pirate - Rusty Red")
    cmds.menuItem(label="Alien - Green & Purple")
    
    # Scale
    scale_slider = cmds.floatSliderGrp(label="Scale:", field=True,
                                        minValue=0.5, maxValue=3.0, value=1.0)
    
    # Animation checkbox
    anim_check = cmds.checkBox(label="Add Engine Glow Animation", value=True)
    
    cmds.separator(height=10)
    
    # Create button
    def on_create(*args):
        name = cmds.textField(name_field, q=True, text=True)
        ship_type = cmds.optionMenu(type_menu, q=True, value=True).split(" -")[0].lower()
        color = cmds.optionMenu(color_menu, q=True, value=True).split(" -")[0].lower()
        scale = cmds.floatSliderGrp(scale_slider, q=True, value=True)
        anim = cmds.checkBox(anim_check, q=True, value=True)
        
        create_starship(name, ship_type, color, scale, anim)
    
    cmds.button(label="🚀 CREATE STARSHIP", height=40, 
                backgroundColor=(0.2, 0.5, 0.7), command=on_create)
    
    cmds.separator(height=10)
    
    # Fleet section
    cmds.text(label="Fleet Generator:", align="left", font="boldLabelFont")
    
    cmds.rowLayout(numberOfColumns=2, columnWidth2=(150, 150))
    fleet_count = cmds.intField(value=3, minValue=1, maxValue=20, width=50)
    fleet_formation = cmds.optionMenu(width=100)
    cmds.menuItem(label="Line")
    cmds.menuItem(label="V")
    cmds.menuItem(label="Diamond")
    cmds.menuItem(label="Random")
    cmds.setParent("..")
    
    def on_fleet(*args):
        count = cmds.intField(fleet_count, q=True, value=True)
        formation = cmds.optionMenu(fleet_formation, q=True, value=True).lower()
        create_fleet(count, formation)
    
    cmds.button(label="⚔️ CREATE FLEET", height=35,
                backgroundColor=(0.6, 0.3, 0.3), command=on_fleet)
    
    cmds.separator(height=10)
    
    # Quick buttons
    cmds.text(label="Quick Create:", align="left")
    cmds.rowLayout(numberOfColumns=4, columnWidth4=(70, 70, 70, 70))
    cmds.button(label="Fighter", w=65, command=lambda x: create_starship("fighter", "fighter"))
    cmds.button(label="Scout", w=65, command=lambda x: create_starship("scout", "scout"))
    cmds.button(label="Bomber", w=65, command=lambda x: create_starship("bomber", "bomber"))
    cmds.button(label="Cruiser", w=65, command=lambda x: create_starship("cruiser", "cruiser"))
    cmds.setParent("..")
    
    cmds.showWindow(window)
    print("✅ Starship Generator UI loaded!")


# ═══════════════════════════════════════════════════════════════════════════════
# ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("\n" + "═" * 50)
    print("🚀 STARSHIP GENERATOR")
    print("═" * 50)
    print("\nQuick Commands:")
    print("  create_starship()           - Create a fighter")
    print("  create_starship('name', 'cruiser', 'imperial')")
    print("  create_fleet(5, 'v')        - Create 5 ships in V formation")
    print("  show_ui()                   - Open the UI")
    print("═" * 50 + "\n")
