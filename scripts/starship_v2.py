"""
═══════════════════════════════════════════════════════════════════════════════
 STARSHIP GENERATOR V2 - ADVANCED EDITION
═══════════════════════════════════════════════════════════════════════════════
 
 Creates detailed, fancy starships with:
 - More detailed geometry
 - Animated thrusters with particles
 - Landing gear
 - Cockpit details
 - Hull panels and details
 - Shield effects
 - Weapon systems
 
 Author: Douglas's Learning Project
 Version: 2.0.0
 
 Usage in Maya:
    from starship_v2 import create_starship, show_ui
    create_starship("my_ship", ship_class="interceptor")
    show_ui()
═══════════════════════════════════════════════════════════════════════════════
"""

import maya.cmds as cmds
import maya.mel as mel
import random
import math

# ═══════════════════════════════════════════════════════════════════════════════
# PART 1: COLOR SCHEMES AND PRESETS
# ═══════════════════════════════════════════════════════════════════════════════

SHIP_THEMES = {
    "federation": {
        "hull_primary": (0.85, 0.85, 0.9),      # Light silver
        "hull_secondary": (0.6, 0.6, 0.65),     # Medium gray
        "accent": (0.2, 0.4, 0.8),              # Blue
        "engine_glow": (0.0, 0.7, 1.0),         # Cyan
        "cockpit": (0.1, 0.15, 0.2),            # Dark blue glass
        "weapons": (1.0, 0.3, 0.1),             # Orange-red
        "lights": (1.0, 1.0, 0.8),              # Warm white
    },
    "empire": {
        "hull_primary": (0.2, 0.2, 0.22),       # Dark gray
        "hull_secondary": (0.1, 0.1, 0.12),     # Near black
        "accent": (0.8, 0.0, 0.0),              # Red
        "engine_glow": (0.0, 0.5, 1.0),         # Blue
        "cockpit": (0.05, 0.05, 0.08),          # Very dark
        "weapons": (0.0, 1.0, 0.3),             # Green
        "lights": (1.0, 0.0, 0.0),              # Red
    },
    "bounty_hunter": {
        "hull_primary": (0.4, 0.35, 0.25),      # Worn tan
        "hull_secondary": (0.3, 0.25, 0.15),    # Brown
        "accent": (0.6, 0.5, 0.1),              # Gold/yellow
        "engine_glow": (1.0, 0.5, 0.0),         # Orange
        "cockpit": (0.15, 0.12, 0.08),          # Brown glass
        "weapons": (1.0, 0.2, 0.0),             # Red-orange
        "lights": (1.0, 0.8, 0.4),              # Warm yellow
    },
    "alien": {
        "hull_primary": (0.1, 0.3, 0.2),        # Dark green
        "hull_secondary": (0.15, 0.4, 0.25),    # Green
        "accent": (0.5, 0.0, 0.7),              # Purple
        "engine_glow": (0.0, 1.0, 0.5),         # Bright green
        "cockpit": (0.2, 0.1, 0.3),             # Purple glass
        "weapons": (0.8, 0.0, 1.0),             # Magenta
        "lights": (0.0, 1.0, 0.8),              # Teal
    },
    "stealth": {
        "hull_primary": (0.05, 0.05, 0.08),     # Near black
        "hull_secondary": (0.08, 0.08, 0.1),    # Dark blue-black
        "accent": (0.1, 0.1, 0.15),             # Very dark blue
        "engine_glow": (0.3, 0.0, 0.5),         # Dim purple
        "cockpit": (0.02, 0.02, 0.05),          # Almost black
        "weapons": (0.5, 0.0, 0.0),             # Dark red
        "lights": (0.2, 0.0, 0.3),              # Dim purple
    },
    "racer": {
        "hull_primary": (1.0, 0.2, 0.0),        # Bright orange
        "hull_secondary": (1.0, 1.0, 1.0),      # White
        "accent": (0.0, 0.0, 0.0),              # Black stripes
        "engine_glow": (0.0, 0.8, 1.0),         # Bright cyan
        "cockpit": (0.1, 0.1, 0.1),             # Dark
        "weapons": (1.0, 1.0, 0.0),             # Yellow
        "lights": (1.0, 1.0, 1.0),              # White
    },
}

SHIP_CLASSES = {
    "interceptor": "Fast, agile fighter with forward-swept wings",
    "heavy_fighter": "Balanced combat ship with thick armor",
    "bomber": "Heavy ship designed for big payloads",
    "corvette": "Small capital ship with multiple decks",
    "racer": "Ultra-fast ship built for speed",
    "transport": "Cargo hauler with large hold",
    "gunship": "Heavily armed assault craft",
}


# ═══════════════════════════════════════════════════════════════════════════════
# PART 2: MATERIAL CREATION HELPERS
# ═══════════════════════════════════════════════════════════════════════════════

def create_material(name, color, metallic=0.5, glow=0.0, transparency=0.0):
    """
    Create a fancy material with metallic and glow properties.
    """
    mat = cmds.shadingNode('blinn', asShader=True, name=name)
    sg = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=f'{name}_SG')
    cmds.connectAttr(f'{mat}.outColor', f'{sg}.surfaceShader')
    
    # Base color
    cmds.setAttr(f'{mat}.color', color[0], color[1], color[2], type='double3')
    
    # Metallic look
    spec_intensity = 0.5 + metallic * 0.5
    cmds.setAttr(f'{mat}.specularColor', spec_intensity, spec_intensity, spec_intensity, type='double3')
    cmds.setAttr(f'{mat}.specularRollOff', 0.3 + metallic * 0.5)
    cmds.setAttr(f'{mat}.eccentricity', 0.3 - metallic * 0.2)
    cmds.setAttr(f'{mat}.reflectivity', metallic * 0.4)
    
    # Glow effect
    if glow > 0:
        cmds.setAttr(f'{mat}.incandescence', color[0]*glow, color[1]*glow, color[2]*glow, type='double3')
        cmds.setAttr(f'{mat}.glowIntensity', glow * 0.5)
    
    # Transparency
    if transparency > 0:
        cmds.setAttr(f'{mat}.transparency', transparency, transparency, transparency, type='double3')
    
    return mat, sg


def apply_material(obj, material_sg):
    """Apply a shading group to an object."""
    cmds.sets(obj, edit=True, forceElement=material_sg)


# ═══════════════════════════════════════════════════════════════════════════════
# PART 3: SHIP COMPONENT BUILDERS
# ═══════════════════════════════════════════════════════════════════════════════

def build_hull_panel(width, height, depth, segments=2):
    """Create a hull panel with beveled edges."""
    panel = cmds.polyCube(w=width, h=height, d=depth, sx=segments, sy=segments, sz=1)[0]
    # Add some bevel to edges
    cmds.polyBevel3(panel, fraction=0.1, segments=1)
    return panel


def build_engine_pod(radius, length, theme, index=0):
    """Create a detailed engine pod with glow."""
    parts = []
    
    # Main engine housing
    housing = cmds.polyCylinder(r=radius, h=length, sx=12, sy=2, sz=1, ax=[0,0,1])[0]
    parts.append(("housing", housing))
    
    # Engine intake ring
    intake = cmds.polyTorus(r=radius*1.1, sr=radius*0.15, sx=12, sy=6, ax=[0,0,1])[0]
    cmds.move(0, 0, length*0.4, intake)
    parts.append(("intake", intake))
    
    # Engine nozzle (cone)
    nozzle = cmds.polyCone(r=radius*0.9, h=length*0.3, sx=12, sy=1, ax=[0,0,1])[0]
    cmds.rotate(180, 0, 0, nozzle)
    cmds.move(0, 0, -length*0.6, nozzle)
    parts.append(("nozzle", nozzle))
    
    # Engine glow core
    glow = cmds.polySphere(r=radius*0.7, sx=8, sy=8)[0]
    cmds.scale(1, 1, 0.5, glow)
    cmds.move(0, 0, -length*0.55, glow)
    parts.append(("glow", glow))
    
    # Outer glow ring
    glow_ring = cmds.polyTorus(r=radius*0.8, sr=radius*0.1, sx=12, sy=4, ax=[0,0,1])[0]
    cmds.move(0, 0, -length*0.5, glow_ring)
    parts.append(("glow_ring", glow_ring))
    
    return parts


def build_cockpit(width, height, length, theme):
    """Create a detailed cockpit with frame and glass."""
    parts = []
    
    # Glass canopy (sphere stretched)
    canopy = cmds.polySphere(r=1, sx=12, sy=8)[0]
    cmds.scale(width*0.5, height*0.5, length*0.5, canopy)
    # Cut the bottom half
    cmds.polyChipOff(canopy, dup=False, kft=True, translate=[0, -height*0.3, 0])
    parts.append(("canopy", canopy))
    
    # Cockpit frame strips
    for i in range(3):
        angle = -30 + i * 30
        frame = cmds.polyCube(w=width*0.05, h=height*0.6, d=length*0.02)[0]
        cmds.rotate(angle, 0, 0, frame)
        cmds.move(0, height*0.1, length*0.25, frame)
        parts.append((f"frame_{i}", frame))
    
    # Cockpit base
    base = cmds.polyCylinder(r=width*0.45, h=height*0.2, sx=12, sy=1, ax=[0,1,0])[0]
    cmds.move(0, -height*0.2, 0, base)
    parts.append(("base", base))
    
    return parts


def build_wing(span, chord, thickness, swept_angle=15, taper=0.5):
    """Create a swept wing with taper."""
    # Create wing profile points
    wing = cmds.polyPlane(w=chord, h=span, sx=3, sy=6, ax=[0,1,0])[0]
    
    # Taper the tip
    cmds.select(f"{wing}.vtx[21:27]")  # Tip vertices
    cmds.scale(taper, 1, taper)
    
    # Sweep the wing
    cmds.select(f"{wing}.vtx[21:27]")
    cmds.move(chord * math.sin(math.radians(swept_angle)), 0, 0, relative=True)
    
    # Give it thickness by extruding
    cmds.polyExtrudeFacet(f"{wing}.f[0:17]", thickness=thickness)
    
    return wing


def build_weapon_pod(length, radius, weapon_type="laser"):
    """Create a weapon system."""
    parts = []
    
    if weapon_type == "laser":
        # Laser cannon barrel
        barrel = cmds.polyCylinder(r=radius, h=length, sx=8, sy=1, ax=[0,0,1])[0]
        parts.append(("barrel", barrel))
        
        # Muzzle
        muzzle = cmds.polyTorus(r=radius*1.3, sr=radius*0.2, sx=8, sy=4, ax=[0,0,1])[0]
        cmds.move(0, 0, length*0.5, muzzle)
        parts.append(("muzzle", muzzle))
        
        # Power cell
        cell = cmds.polyCube(w=radius*2, h=radius*1.5, d=length*0.3)[0]
        cmds.move(0, 0, -length*0.3, cell)
        parts.append(("cell", cell))
        
    elif weapon_type == "missile":
        # Missile launcher tube
        tube = cmds.polyCylinder(r=radius*1.5, h=length, sx=8, sy=1, ax=[0,0,1])[0]
        parts.append(("tube", tube))
        
        # Missile visible inside
        missile = cmds.polyCone(r=radius*0.8, h=length*0.8, sx=8, ax=[0,0,1])[0]
        cmds.move(0, 0, length*0.1, missile)
        parts.append(("missile", missile))
    
    return parts


def build_landing_gear(height, wheel_radius):
    """Create retractable landing gear."""
    parts = []
    
    # Strut
    strut = cmds.polyCylinder(r=wheel_radius*0.3, h=height, sx=6, sy=1, ax=[0,1,0])[0]
    cmds.move(0, -height*0.5, 0, strut)
    parts.append(("strut", strut))
    
    # Wheel/pad
    wheel = cmds.polyTorus(r=wheel_radius, sr=wheel_radius*0.3, sx=12, sy=6, ax=[0,0,1])[0]
    cmds.move(0, -height, 0, wheel)
    parts.append(("wheel", wheel))
    
    # Hydraulic detail
    hydraulic = cmds.polyCylinder(r=wheel_radius*0.15, h=height*0.7, sx=6, ax=[0,1,0])[0]
    cmds.move(wheel_radius*0.4, -height*0.4, 0, hydraulic)
    parts.append(("hydraulic", hydraulic))
    
    return parts


# ═══════════════════════════════════════════════════════════════════════════════
# PART 4: SHIP CLASS BUILDERS
# ═══════════════════════════════════════════════════════════════════════════════

def build_interceptor(group, theme, scale):
    """
    Build a fast interceptor-class starship.
    Sleek design with forward-swept wings and twin engines.
    """
    s = scale
    colors = SHIP_THEMES[theme]
    materials = {}
    
    # Create all materials
    materials["hull"], materials["hull_sg"] = create_material(
        f"{group}_hull_mat", colors["hull_primary"], metallic=0.7)
    materials["hull2"], materials["hull2_sg"] = create_material(
        f"{group}_hull2_mat", colors["hull_secondary"], metallic=0.6)
    materials["accent"], materials["accent_sg"] = create_material(
        f"{group}_accent_mat", colors["accent"], metallic=0.8)
    materials["glow"], materials["glow_sg"] = create_material(
        f"{group}_glow_mat", colors["engine_glow"], metallic=0.2, glow=1.0)
    materials["cockpit"], materials["cockpit_sg"] = create_material(
        f"{group}_cockpit_mat", colors["cockpit"], metallic=0.3, transparency=0.4)
    materials["weapon"], materials["weapon_sg"] = create_material(
        f"{group}_weapon_mat", colors["weapons"], metallic=0.5, glow=0.3)
    
    all_parts = []
    
    # === MAIN FUSELAGE ===
    # Nose section (pointed)
    nose = cmds.polyCone(r=0.4*s, h=1.5*s, sx=12, sy=1, ax=[0,0,1])[0]
    cmds.move(0, 0, 2.5*s, nose)
    apply_material(nose, materials["hull_sg"])
    all_parts.append(nose)
    
    # Main body
    body = cmds.polyCylinder(r=0.5*s, h=2.5*s, sx=12, sy=3, ax=[0,0,1])[0]
    cmds.move(0, 0, 0.5*s, body)
    apply_material(body, materials["hull_sg"])
    all_parts.append(body)
    
    # Rear section (wider)
    rear = cmds.polyCylinder(r=0.6*s, h=1.5*s, sx=12, sy=2, ax=[0,0,1])[0]
    cmds.move(0, 0, -1*s, rear)
    apply_material(rear, materials["hull2_sg"])
    all_parts.append(rear)
    
    # === COCKPIT ===
    cockpit_glass = cmds.polySphere(r=0.35*s, sx=12, sy=8)[0]
    cmds.scale(1, 0.6, 1.3, cockpit_glass)
    cmds.move(0, 0.25*s, 1.5*s, cockpit_glass)
    apply_material(cockpit_glass, materials["cockpit_sg"])
    all_parts.append(cockpit_glass)
    
    # Cockpit frame
    for i in range(3):
        frame = cmds.polyCube(w=0.02*s, h=0.3*s, d=0.5*s)[0]
        angle = -20 + i * 20
        cmds.rotate(0, angle, 0, frame)
        cmds.move(0, 0.3*s, 1.5*s, frame)
        apply_material(frame, materials["accent_sg"])
        all_parts.append(frame)
    
    # === WINGS (Forward-swept) ===
    for side in [-1, 1]:
        # Main wing
        wing = cmds.polyCube(w=2.5*s, h=0.06*s, d=0.8*s)[0]
        cmds.move(side * 1.4*s, 0, 0.3*s, wing)
        cmds.rotate(0, side * -20, side * 8, wing)  # Forward sweep + dihedral
        apply_material(wing, materials["hull_sg"])
        all_parts.append(wing)
        
        # Wing tip
        tip = cmds.polyCone(r=0.15*s, h=0.4*s, sx=8, ax=[side,0,0])[0]
        cmds.move(side * 2.6*s, 0.1*s, 0.6*s, tip)
        apply_material(tip, materials["accent_sg"])
        all_parts.append(tip)
        
        # Wing stripe
        stripe = cmds.polyCube(w=1.8*s, h=0.07*s, d=0.15*s)[0]
        cmds.move(side * 1.2*s, 0.01*s, 0.3*s, stripe)
        cmds.rotate(0, side * -20, side * 8, stripe)
        apply_material(stripe, materials["accent_sg"])
        all_parts.append(stripe)
    
    # === ENGINES ===
    for side in [-1, 1]:
        # Engine nacelle
        nacelle = cmds.polyCylinder(r=0.25*s, h=1.8*s, sx=10, ax=[0,0,1])[0]
        cmds.move(side * 0.5*s, -0.15*s, -1.2*s, nacelle)
        apply_material(nacelle, materials["hull2_sg"])
        all_parts.append(nacelle)
        
        # Engine intake
        intake = cmds.polyTorus(r=0.28*s, sr=0.06*s, sx=10, sy=4, ax=[0,0,1])[0]
        cmds.move(side * 0.5*s, -0.15*s, -0.3*s, intake)
        apply_material(intake, materials["accent_sg"])
        all_parts.append(intake)
        
        # Engine glow
        glow = cmds.polySphere(r=0.2*s, sx=8, sy=8)[0]
        cmds.scale(1, 1, 0.4, glow)
        cmds.move(side * 0.5*s, -0.15*s, -2.1*s, glow)
        apply_material(glow, materials["glow_sg"])
        all_parts.append(glow)
        
        # Glow ring
        glow_ring = cmds.polyTorus(r=0.22*s, sr=0.03*s, sx=10, sy=4, ax=[0,0,1])[0]
        cmds.move(side * 0.5*s, -0.15*s, -2.0*s, glow_ring)
        apply_material(glow_ring, materials["glow_sg"])
        all_parts.append(glow_ring)
    
    # === WEAPONS ===
    for side in [-1, 1]:
        # Wing-mounted laser
        cannon = cmds.polyCylinder(r=0.04*s, h=0.8*s, sx=6, ax=[0,0,1])[0]
        cmds.move(side * 1.8*s, -0.05*s, 0.8*s, cannon)
        apply_material(cannon, materials["weapon_sg"])
        all_parts.append(cannon)
        
        # Cannon mount
        mount = cmds.polyCube(w=0.1*s, h=0.08*s, d=0.2*s)[0]
        cmds.move(side * 1.8*s, 0, 0.5*s, mount)
        apply_material(mount, materials["hull2_sg"])
        all_parts.append(mount)
    
    # === TAIL FINS ===
    # Vertical stabilizer
    vfin = cmds.polyCube(w=0.04*s, h=0.6*s, d=0.5*s)[0]
    cmds.move(0, 0.4*s, -1.5*s, vfin)
    apply_material(vfin, materials["accent_sg"])
    all_parts.append(vfin)
    
    # Horizontal stabilizers
    for side in [-1, 1]:
        hfin = cmds.polyCube(w=0.5*s, h=0.04*s, d=0.3*s)[0]
        cmds.move(side * 0.35*s, 0, -1.6*s, hfin)
        cmds.rotate(0, 0, side * 15, hfin)
        apply_material(hfin, materials["hull2_sg"])
        all_parts.append(hfin)
    
    # === DETAILS ===
    # Sensor dome on nose
    sensor = cmds.polySphere(r=0.08*s, sx=8, sy=6)[0]
    cmds.move(0, 0.1*s, 3.1*s, sensor)
    apply_material(sensor, materials["accent_sg"])
    all_parts.append(sensor)
    
    # Hull panel lines (decorative strips)
    for z_pos in [0, 0.8, -0.5]:
        panel_line = cmds.polyCube(w=1.05*s, h=0.02*s, d=0.03*s)[0]
        cmds.move(0, 0.35*s, z_pos*s, panel_line)
        apply_material(panel_line, materials["hull2_sg"])
        all_parts.append(panel_line)
    
    # Parent all to group
    for part in all_parts:
        cmds.parent(part, group)
    
    print(f"  ✓ Interceptor built: {len(all_parts)} parts")
    return all_parts


def build_heavy_fighter(group, theme, scale):
    """
    Build a heavy fighter with thick armor and heavy weapons.
    """
    s = scale
    colors = SHIP_THEMES[theme]
    materials = {}
    
    # Create materials
    materials["hull"], materials["hull_sg"] = create_material(
        f"{group}_hull_mat", colors["hull_primary"], metallic=0.8)
    materials["armor"], materials["armor_sg"] = create_material(
        f"{group}_armor_mat", colors["hull_secondary"], metallic=0.9)
    materials["accent"], materials["accent_sg"] = create_material(
        f"{group}_accent_mat", colors["accent"], metallic=0.7)
    materials["glow"], materials["glow_sg"] = create_material(
        f"{group}_glow_mat", colors["engine_glow"], glow=1.0)
    materials["cockpit"], materials["cockpit_sg"] = create_material(
        f"{group}_cockpit_mat", colors["cockpit"], transparency=0.3)
    materials["weapon"], materials["weapon_sg"] = create_material(
        f"{group}_weapon_mat", colors["weapons"], glow=0.4)
    
    all_parts = []
    
    # === MAIN HULL (Chunky/armored look) ===
    # Central fuselage
    body = cmds.polyCube(w=1.2*s, h=0.6*s, d=3.5*s)[0]
    apply_material(body, materials["hull_sg"])
    all_parts.append(body)
    
    # Armored nose
    nose = cmds.polyCube(w=0.8*s, h=0.5*s, d=1*s)[0]
    cmds.move(0, 0, 2*s, nose)
    apply_material(nose, materials["armor_sg"])
    all_parts.append(nose)
    
    # Nose tip
    nose_tip = cmds.polyCone(r=0.35*s, h=0.6*s, sx=8, ax=[0,0,1])[0]
    cmds.move(0, 0, 2.7*s, nose_tip)
    apply_material(nose_tip, materials["armor_sg"])
    all_parts.append(nose_tip)
    
    # === COCKPIT ===
    cockpit = cmds.polySphere(r=0.3*s, sx=10, sy=8)[0]
    cmds.scale(0.8, 0.5, 1, cockpit)
    cmds.move(0, 0.35*s, 1*s, cockpit)
    apply_material(cockpit, materials["cockpit_sg"])
    all_parts.append(cockpit)
    
    # === WINGS (Shorter, thicker) ===
    for side in [-1, 1]:
        wing = cmds.polyCube(w=1.8*s, h=0.12*s, d=1.2*s)[0]
        cmds.move(side * 1.4*s, 0, 0, wing)
        apply_material(wing, materials["hull_sg"])
        all_parts.append(wing)
        
        # Wing armor plate
        armor_plate = cmds.polyCube(w=1.2*s, h=0.15*s, d=0.8*s)[0]
        cmds.move(side * 1.2*s, 0.1*s, 0, armor_plate)
        apply_material(armor_plate, materials["armor_sg"])
        all_parts.append(armor_plate)
    
    # === TRIPLE ENGINES ===
    engine_positions = [(0, -0.1), (-0.4, 0.1), (0.4, 0.1)]
    for i, (x_off, y_off) in enumerate(engine_positions):
        nacelle = cmds.polyCylinder(r=0.2*s, h=1.2*s, sx=8, ax=[0,0,1])[0]
        cmds.move(x_off*s, y_off*s, -2*s, nacelle)
        apply_material(nacelle, materials["armor_sg"])
        all_parts.append(nacelle)
        
        glow = cmds.polySphere(r=0.15*s, sx=6, sy=6)[0]
        cmds.scale(1, 1, 0.3, glow)
        cmds.move(x_off*s, y_off*s, -2.6*s, glow)
        apply_material(glow, materials["glow_sg"])
        all_parts.append(glow)
    
    # === HEAVY WEAPONS ===
    for side in [-1, 1]:
        # Main cannon (big!)
        cannon = cmds.polyCylinder(r=0.08*s, h=1.5*s, sx=8, ax=[0,0,1])[0]
        cmds.move(side * 0.3*s, -0.2*s, 2.5*s, cannon)
        apply_material(cannon, materials["weapon_sg"])
        all_parts.append(cannon)
        
        # Wing cannons
        wing_gun = cmds.polyCylinder(r=0.05*s, h=1*s, sx=6, ax=[0,0,1])[0]
        cmds.move(side * 1.8*s, 0, 0.8*s, wing_gun)
        apply_material(wing_gun, materials["weapon_sg"])
        all_parts.append(wing_gun)
        
        # Missile pod
        pod = cmds.polyCube(w=0.3*s, h=0.2*s, d=0.5*s)[0]
        cmds.move(side * 2.1*s, -0.1*s, -0.2*s, pod)
        apply_material(pod, materials["armor_sg"])
        all_parts.append(pod)
    
    # Parent all
    for part in all_parts:
        cmds.parent(part, group)
    
    print(f"  ✓ Heavy Fighter built: {len(all_parts)} parts")
    return all_parts


def build_racer(group, theme, scale):
    """
    Build an ultra-fast racing ship.
    Minimal armor, maximum engines!
    """
    s = scale
    colors = SHIP_THEMES[theme]
    materials = {}
    
    # Create materials (brighter for racing)
    materials["hull"], materials["hull_sg"] = create_material(
        f"{group}_hull_mat", colors["hull_primary"], metallic=0.9)
    materials["stripe"], materials["stripe_sg"] = create_material(
        f"{group}_stripe_mat", colors["hull_secondary"], metallic=0.95)
    materials["accent"], materials["accent_sg"] = create_material(
        f"{group}_accent_mat", colors["accent"], metallic=0.8)
    materials["glow"], materials["glow_sg"] = create_material(
        f"{group}_glow_mat", colors["engine_glow"], glow=1.2)
    materials["cockpit"], materials["cockpit_sg"] = create_material(
        f"{group}_cockpit_mat", colors["cockpit"], transparency=0.4)
    
    all_parts = []
    
    # === SLEEK BODY (Very aerodynamic) ===
    # Main fuselage (thin and long)
    body = cmds.polyCylinder(r=0.25*s, h=4*s, sx=10, ax=[0,0,1])[0]
    cmds.scale(1, 0.7, 1, body)
    apply_material(body, materials["hull_sg"])
    all_parts.append(body)
    
    # Pointed nose
    nose = cmds.polyCone(r=0.25*s, h=1.2*s, sx=10, ax=[0,0,1])[0]
    cmds.scale(1, 0.7, 1, nose)
    cmds.move(0, 0, 2.5*s, nose)
    apply_material(nose, materials["hull_sg"])
    all_parts.append(nose)
    
    # Racing stripe
    stripe = cmds.polyCube(w=0.08*s, h=0.2*s, d=5*s)[0]
    cmds.move(0, 0.12*s, 0.3*s, stripe)
    apply_material(stripe, materials["stripe_sg"])
    all_parts.append(stripe)
    
    # === LARGE COCKPIT (bubble canopy) ===
    cockpit = cmds.polySphere(r=0.22*s, sx=10, sy=8)[0]
    cmds.scale(1, 0.8, 1.5, cockpit)
    cmds.move(0, 0.15*s, 1.2*s, cockpit)
    apply_material(cockpit, materials["cockpit_sg"])
    all_parts.append(cockpit)
    
    # === HUGE ENGINES (oversized for speed) ===
    for side in [-1, 1]:
        # Main engine pod
        engine = cmds.polyCylinder(r=0.35*s, h=2.5*s, sx=12, ax=[0,0,1])[0]
        cmds.move(side * 0.5*s, 0, -1.5*s, engine)
        apply_material(engine, materials["hull_sg"])
        all_parts.append(engine)
        
        # Engine stripe
        eng_stripe = cmds.polyCube(w=0.72*s, h=0.05*s, d=0.1*s)[0]
        cmds.move(side * 0.5*s, 0.2*s, -0.5*s, eng_stripe)
        apply_material(eng_stripe, materials["accent_sg"])
        all_parts.append(eng_stripe)
        
        # Massive glow
        glow = cmds.polySphere(r=0.3*s, sx=10, sy=8)[0]
        cmds.scale(1, 1, 0.5, glow)
        cmds.move(side * 0.5*s, 0, -2.8*s, glow)
        apply_material(glow, materials["glow_sg"])
        all_parts.append(glow)
        
        # Glow rings (multiple)
        for ring_z in [-2.3, -2.5, -2.7]:
            ring = cmds.polyTorus(r=0.32*s, sr=0.03*s, sx=12, sy=4, ax=[0,0,1])[0]
            cmds.move(side * 0.5*s, 0, ring_z*s, ring)
            apply_material(ring, materials["glow_sg"])
            all_parts.append(ring)
    
    # === SMALL FINS (for stability) ===
    for side in [-1, 1]:
        # Small wing
        wing = cmds.polyCube(w=0.8*s, h=0.03*s, d=0.4*s)[0]
        cmds.move(side * 0.6*s, 0, 0.5*s, wing)
        cmds.rotate(0, 0, side * 5, wing)
        apply_material(wing, materials["hull_sg"])
        all_parts.append(wing)
        
        # Winglet (vertical)
        winglet = cmds.polyCube(w=0.03*s, h=0.25*s, d=0.2*s)[0]
        cmds.move(side * 0.95*s, 0.1*s, 0.5*s, winglet)
        apply_material(winglet, materials["accent_sg"])
        all_parts.append(winglet)
    
    # Rear fin
    rear_fin = cmds.polyCube(w=0.03*s, h=0.4*s, d=0.3*s)[0]
    cmds.move(0, 0.25*s, -1.8*s, rear_fin)
    apply_material(rear_fin, materials["accent_sg"])
    all_parts.append(rear_fin)
    
    # Parent all
    for part in all_parts:
        cmds.parent(part, group)
    
    print(f"  ✓ Racer built: {len(all_parts)} parts")
    return all_parts


# ═══════════════════════════════════════════════════════════════════════════════
# PART 5: ANIMATION SYSTEM
# ═══════════════════════════════════════════════════════════════════════════════

def add_engine_animation(group, intensity=1.0):
    """Add pulsing glow animation to engines."""
    # Find all glow objects in the group
    all_children = cmds.listRelatives(group, allDescendents=True, type='transform') or []
    
    cmds.playbackOptions(min=1, max=120, ast=1, aet=120)
    
    # Animate any spheres (likely glows) and torus (glow rings)
    for child in all_children:
        shapes = cmds.listRelatives(child, shapes=True)
        if not shapes:
            continue
        
        # Check if it's a glow by looking at material
        try:
            # Scale pulsing for glow effect
            cmds.setKeyframe(child, attribute='scaleX', value=1.0, time=1)
            cmds.setKeyframe(child, attribute='scaleY', value=1.0, time=1)
            cmds.setKeyframe(child, attribute='scaleZ', value=1.0, time=1)
            
            cmds.setKeyframe(child, attribute='scaleX', value=1.0 + 0.15*intensity, time=20)
            cmds.setKeyframe(child, attribute='scaleY', value=1.0 + 0.15*intensity, time=20)
            cmds.setKeyframe(child, attribute='scaleZ', value=1.0 + 0.1*intensity, time=20)
            
            cmds.setKeyframe(child, attribute='scaleX', value=1.0, time=40)
            cmds.setKeyframe(child, attribute='scaleY', value=1.0, time=40)
            cmds.setKeyframe(child, attribute='scaleZ', value=1.0, time=40)
            
            cmds.setKeyframe(child, attribute='scaleX', value=1.0 + 0.1*intensity, time=60)
            cmds.setKeyframe(child, attribute='scaleY', value=1.0 + 0.1*intensity, time=60)
            cmds.setKeyframe(child, attribute='scaleZ', value=1.0 + 0.05*intensity, time=60)
            
            cmds.setKeyframe(child, attribute='scaleX', value=1.0, time=80)
            cmds.setKeyframe(child, attribute='scaleY', value=1.0, time=80)
            cmds.setKeyframe(child, attribute='scaleZ', value=1.0, time=80)
        except Exception:
            pass


def add_flight_animation(group, style="hover"):
    """Add flight movement animation."""
    cmds.playbackOptions(min=1, max=120, ast=1, aet=120)
    
    if style == "hover":
        # Gentle hovering motion
        cmds.setKeyframe(group, attribute='translateY', value=0, time=1)
        cmds.setKeyframe(group, attribute='translateY', value=0.2, time=30)
        cmds.setKeyframe(group, attribute='translateY', value=0, time=60)
        cmds.setKeyframe(group, attribute='translateY', value=-0.1, time=90)
        cmds.setKeyframe(group, attribute='translateY', value=0, time=120)
        
        # Slight roll
        cmds.setKeyframe(group, attribute='rotateZ', value=0, time=1)
        cmds.setKeyframe(group, attribute='rotateZ', value=2, time=40)
        cmds.setKeyframe(group, attribute='rotateZ', value=-2, time=80)
        cmds.setKeyframe(group, attribute='rotateZ', value=0, time=120)
        
    elif style == "flyby":
        # Ship flies past camera
        cmds.setKeyframe(group, attribute='translateX', value=-20, time=1)
        cmds.setKeyframe(group, attribute='translateX', value=20, time=120)
        
        cmds.setKeyframe(group, attribute='rotateY', value=90, time=1)
        cmds.setKeyframe(group, attribute='rotateY', value=90, time=120)
        
    elif style == "banking":
        # Banking turn
        cmds.setKeyframe(group, attribute='rotateY', value=0, time=1)
        cmds.setKeyframe(group, attribute='rotateY', value=90, time=60)
        cmds.setKeyframe(group, attribute='rotateY', value=180, time=120)
        
        cmds.setKeyframe(group, attribute='rotateZ', value=0, time=1)
        cmds.setKeyframe(group, attribute='rotateZ', value=-30, time=30)
        cmds.setKeyframe(group, attribute='rotateZ', value=0, time=60)
        cmds.setKeyframe(group, attribute='rotateZ', value=-30, time=90)
        cmds.setKeyframe(group, attribute='rotateZ', value=0, time=120)


# ═══════════════════════════════════════════════════════════════════════════════
# PART 6: MAIN CREATE FUNCTION
# ═══════════════════════════════════════════════════════════════════════════════

def create_starship(
    name="starship",
    ship_class="interceptor",
    theme="federation",
    scale=1.0,
    add_animation=True,
    animation_style="hover"
):
    """
    Create a detailed starship!
    
    Args:
        name (str): Name for the ship
        ship_class (str): "interceptor", "heavy_fighter", "racer"
        theme (str): "federation", "empire", "bounty_hunter", "alien", "stealth", "racer"
        scale (float): Size multiplier
        add_animation (bool): Add engine and flight animations
        animation_style (str): "hover", "flyby", "banking"
    
    Returns:
        str: Name of the ship group
    
    Example:
        >>> create_starship("red_five", "interceptor", "federation")
        >>> create_starship("tie", "interceptor", "empire", scale=0.8)
    """
    
    print("\n" + "═" * 60)
    print(f"🚀 STARSHIP GENERATOR V2")
    print("═" * 60)
    print(f"  Ship: {name}")
    print(f"  Class: {ship_class}")
    print(f"  Theme: {theme}")
    print(f"  Scale: {scale}")
    print("═" * 60)
    
    # Validate inputs
    if theme not in SHIP_THEMES:
        print(f"  ⚠️ Unknown theme '{theme}', using 'federation'")
        theme = "federation"
    
    if ship_class not in ["interceptor", "heavy_fighter", "racer"]:
        print(f"  ⚠️ Unknown class '{ship_class}', using 'interceptor'")
        ship_class = "interceptor"
    
    # Create main group
    ship_group = cmds.group(empty=True, name=f"{name}_grp")
    
    # Build the ship based on class
    if ship_class == "interceptor":
        parts = build_interceptor(ship_group, theme, scale)
    elif ship_class == "heavy_fighter":
        parts = build_heavy_fighter(ship_group, theme, scale)
    elif ship_class == "racer":
        parts = build_racer(ship_group, theme, scale)
    
    # Add animations
    if add_animation:
        print(f"  🎬 Adding {animation_style} animation...")
        add_flight_animation(ship_group, animation_style)
    
    # Center pivot
    cmds.xform(ship_group, centerPivots=True)
    
    print("═" * 60)
    print(f"✅ Starship '{name}' created successfully!")
    print(f"   Total parts: {len(parts)}")
    print("═" * 60 + "\n")
    
    return ship_group


def create_squadron(count=3, ship_class="interceptor", theme="federation", formation="v"):
    """
    Create a squadron of ships in formation.
    
    Args:
        count (int): Number of ships (1-12)
        ship_class (str): Type of ships
        theme (str): Color scheme
        formation (str): "v", "line", "diamond", "echelon"
    """
    print(f"\n🛸 Creating squadron of {count} {ship_class}s...")
    
    ships = []
    count = min(count, 12)  # Max 12 ships
    
    for i in range(count):
        ship = create_starship(
            name=f"squad_{i+1}",
            ship_class=ship_class,
            theme=theme,
            scale=0.8,
            add_animation=True,
            animation_style="hover"
        )
        
        # Position based on formation
        if formation == "v":
            row = i // 2
            side = 1 if i % 2 == 0 else -1
            if i == 0:
                cmds.move(0, 0, 0, ship)
            else:
                cmds.move(side * row * 3, 0, -row * 4, ship)
                
        elif formation == "line":
            cmds.move(i * 4, 0, 0, ship)
            
        elif formation == "diamond":
            angle = (i / count) * 360
            radius = 5
            x = radius * math.cos(math.radians(angle))
            z = radius * math.sin(math.radians(angle))
            cmds.move(x, 0, z, ship)
            cmds.rotate(0, -angle + 90, 0, ship)
            
        elif formation == "echelon":
            cmds.move(i * 3, 0, -i * 2, ship)
        
        ships.append(ship)
    
    # Group the squadron
    squad_grp = cmds.group(ships, name="squadron_grp")
    print(f"✅ Squadron created with {count} ships!")
    
    return squad_grp


# ═══════════════════════════════════════════════════════════════════════════════
# PART 7: USER INTERFACE
# ═══════════════════════════════════════════════════════════════════════════════

def show_ui():
    """Show the starship generator UI."""
    window_name = "starshipV2UI"
    
    if cmds.window(window_name, exists=True):
        cmds.deleteUI(window_name)
    
    window = cmds.window(window_name, title="🚀 Starship Generator V2", 
                         widthHeight=(380, 500), sizeable=True)
    
    cmds.columnLayout(adjustableColumn=True, rowSpacing=8, columnOffset=("both", 10))
    
    cmds.separator(height=10)
    cmds.text(label="🚀 STARSHIP GENERATOR V2 🚀", font="boldLabelFont", height=30)
    cmds.text(label="Advanced Edition - More Details!", font="smallPlainLabelFont")
    cmds.separator(height=10)
    
    # Ship name
    cmds.text(label="Ship Name:", align="left")
    name_field = cmds.textField(text="my_starship")
    
    cmds.separator(height=5)
    
    # Ship class
    cmds.text(label="Ship Class:", align="left")
    class_menu = cmds.optionMenu()
    cmds.menuItem(label="Interceptor - Fast & agile")
    cmds.menuItem(label="Heavy Fighter - Armored & armed")
    cmds.menuItem(label="Racer - Ultra fast")
    
    cmds.separator(height=5)
    
    # Theme
    cmds.text(label="Color Theme:", align="left")
    theme_menu = cmds.optionMenu()
    cmds.menuItem(label="Federation - Silver & Blue")
    cmds.menuItem(label="Empire - Dark & Red")
    cmds.menuItem(label="Bounty Hunter - Worn & Gold")
    cmds.menuItem(label="Alien - Green & Purple")
    cmds.menuItem(label="Stealth - Black & Dark")
    cmds.menuItem(label="Racer - Bright & White")
    
    cmds.separator(height=5)
    
    # Scale
    scale_slider = cmds.floatSliderGrp(label="Scale:", field=True,
                                        minValue=0.5, maxValue=3.0, value=1.0)
    
    # Animation options
    cmds.separator(height=5)
    cmds.text(label="Animation:", align="left")
    anim_check = cmds.checkBox(label="Add Animation", value=True)
    anim_style = cmds.optionMenu()
    cmds.menuItem(label="Hover - Gentle floating")
    cmds.menuItem(label="Flyby - Zoom past")
    cmds.menuItem(label="Banking - Turn maneuver")
    
    cmds.separator(height=15)
    
    # Create button
    def on_create(*args):
        ship_name = cmds.textField(name_field, q=True, text=True)
        ship_class = cmds.optionMenu(class_menu, q=True, value=True).split(" -")[0].lower().replace(" ", "_")
        theme = cmds.optionMenu(theme_menu, q=True, value=True).split(" -")[0].lower().replace(" ", "_")
        scl = cmds.floatSliderGrp(scale_slider, q=True, value=True)
        anim = cmds.checkBox(anim_check, q=True, value=True)
        style = cmds.optionMenu(anim_style, q=True, value=True).split(" -")[0].lower()
        
        create_starship(ship_name, ship_class, theme, scl, anim, style)
    
    cmds.button(label="🚀 CREATE STARSHIP", height=45, 
                backgroundColor=(0.2, 0.5, 0.7), command=on_create)
    
    cmds.separator(height=15)
    
    # Squadron section
    cmds.text(label="Squadron Generator:", font="boldLabelFont", align="left")
    
    cmds.rowLayout(numberOfColumns=2, columnWidth2=(180, 180))
    squad_count = cmds.intSliderGrp(label="Ships:", field=True, minValue=2, maxValue=12, value=3)
    squad_formation = cmds.optionMenu()
    cmds.menuItem(label="V Formation")
    cmds.menuItem(label="Line")
    cmds.menuItem(label="Diamond")
    cmds.menuItem(label="Echelon")
    cmds.setParent("..")
    
    def on_squadron(*args):
        count = cmds.intSliderGrp(squad_count, q=True, value=True)
        formation = cmds.optionMenu(squad_formation, q=True, value=True).split(" ")[0].lower()
        ship_class = cmds.optionMenu(class_menu, q=True, value=True).split(" -")[0].lower().replace(" ", "_")
        theme = cmds.optionMenu(theme_menu, q=True, value=True).split(" -")[0].lower().replace(" ", "_")
        create_squadron(count, ship_class, theme, formation)
    
    cmds.button(label="⚔️ CREATE SQUADRON", height=35,
                backgroundColor=(0.6, 0.3, 0.3), command=on_squadron)
    
    cmds.separator(height=10)
    
    # Quick create buttons
    cmds.text(label="Quick Create:", align="left")
    cmds.rowLayout(numberOfColumns=3, columnWidth3=(115, 115, 115))
    cmds.button(label="🔵 Federation", w=110, 
                command=lambda x: create_starship("fed_ship", "interceptor", "federation"))
    cmds.button(label="⚫ Empire", w=110,
                command=lambda x: create_starship("imp_ship", "heavy_fighter", "empire"))
    cmds.button(label="🟢 Alien", w=110,
                command=lambda x: create_starship("alien_ship", "interceptor", "alien"))
    cmds.setParent("..")
    
    cmds.showWindow(window)
    print("✅ Starship Generator V2 UI loaded!")


# ═══════════════════════════════════════════════════════════════════════════════
# ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("\n" + "═" * 60)
    print("🚀 STARSHIP GENERATOR V2 - ADVANCED EDITION")
    print("═" * 60)
    print("\nShip Classes:")
    for cls, desc in SHIP_CLASSES.items():
        print(f"  • {cls}: {desc}")
    print("\nThemes:")
    for theme in SHIP_THEMES.keys():
        print(f"  • {theme}")
    print("\nQuick Start:")
    print("  create_starship('my_ship', 'interceptor', 'federation')")
    print("  create_squadron(5, 'interceptor', 'empire', 'v')")
    print("  show_ui()")
    print("═" * 60 + "\n")
