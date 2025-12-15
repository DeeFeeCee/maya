"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   ⭐ STAR WARS INSPIRED FLEET GENERATOR ⭐                                    ║
║   Create iconic sci-fi starship designs in Maya!                             ║
║                                                                              ║
║   Author: Douglas's Learning Project                                         ║
║   Version: 1.0.0                                                             ║
║                                                                              ║
║   Usage in Maya:                                                             ║
║       from starwars_fleet import create_fleet, create_ship, show_ui         ║
║       create_fleet()           # Create a mixed fleet                        ║
║       create_ship("xwing")     # Create specific ship                        ║
║       show_ui()                # Open the UI                                 ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import maya.cmds as cmds
import maya.mel as mel
import random
import math

# ═══════════════════════════════════════════════════════════════════════════════
# SHIP CONFIGURATIONS
# ═══════════════════════════════════════════════════════════════════════════════

SHIP_TYPES = {
    "xwing": {
        "name": "X-Wing Fighter",
        "description": "Rebel Alliance starfighter with S-foils",
        "colors": {
            "hull": (0.85, 0.85, 0.8),      # Off-white
            "accent": (1.0, 0.3, 0.0),       # Orange stripes
            "engine": (1.0, 0.4, 0.2),       # Orange-red glow
            "cockpit": (0.1, 0.15, 0.2),     # Dark glass
        }
    },
    "tie": {
        "name": "TIE Fighter",
        "description": "Imperial fighter with twin ion engines",
        "colors": {
            "hull": (0.2, 0.2, 0.22),        # Dark gray
            "accent": (0.1, 0.1, 0.1),       # Black
            "engine": (0.0, 0.5, 1.0),       # Blue glow
            "cockpit": (0.05, 0.05, 0.08),   # Very dark
        }
    },
    "ywing": {
        "name": "Y-Wing Bomber",
        "description": "Rebel bomber with exposed machinery",
        "colors": {
            "hull": (0.6, 0.55, 0.4),        # Tan/gold
            "accent": (0.4, 0.35, 0.25),     # Brown
            "engine": (0.0, 0.7, 1.0),       # Cyan glow
            "cockpit": (0.1, 0.1, 0.15),     # Dark
        }
    },
    "awing": {
        "name": "A-Wing Interceptor",
        "description": "Fast rebel interceptor",
        "colors": {
            "hull": (0.8, 0.15, 0.1),        # Red
            "accent": (0.9, 0.9, 0.85),      # White
            "engine": (0.0, 0.8, 1.0),       # Cyan
            "cockpit": (0.1, 0.1, 0.12),     # Dark
        }
    },
    "falcon": {
        "name": "Light Freighter",
        "description": "Modified YT-1300 freighter",
        "colors": {
            "hull": (0.6, 0.58, 0.55),       # Weathered gray
            "accent": (0.4, 0.38, 0.35),     # Darker gray
            "engine": (0.0, 0.6, 1.0),       # Blue glow
            "cockpit": (0.15, 0.12, 0.1),    # Brown glass
        }
    },
    "shuttle": {
        "name": "Imperial Shuttle",
        "description": "Lambda-class shuttle with folding wings",
        "colors": {
            "hull": (0.85, 0.85, 0.88),      # Light gray
            "accent": (0.2, 0.2, 0.22),      # Dark trim
            "engine": (1.0, 0.3, 0.1),       # Orange glow
            "cockpit": (0.1, 0.1, 0.12),     # Dark
        }
    },
    "interceptor": {
        "name": "TIE Interceptor",
        "description": "Advanced Imperial fighter with angled wings",
        "colors": {
            "hull": (0.15, 0.15, 0.18),      # Dark gray
            "accent": (0.1, 0.1, 0.1),       # Black
            "engine": (0.0, 0.6, 1.0),       # Blue glow
            "cockpit": (0.05, 0.05, 0.08),   # Very dark
        }
    },
    "slave1": {
        "name": "Firespray Gunship",
        "description": "Bounty hunter patrol craft",
        "colors": {
            "hull": (0.3, 0.4, 0.35),        # Green-gray
            "accent": (0.6, 0.1, 0.1),       # Dark red
            "engine": (1.0, 0.5, 0.0),       # Orange glow
            "cockpit": (0.1, 0.15, 0.12),    # Dark green
        }
    },
}


# ═══════════════════════════════════════════════════════════════════════════════
# MATERIAL CREATION
# ═══════════════════════════════════════════════════════════════════════════════

def create_material(name, color, emission=0.0):
    """Create a material with optional glow."""
    shader = cmds.shadingNode('lambert', asShader=True, name=f"{name}_mat")
    sg = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=f"{name}_SG")
    cmds.connectAttr(f"{shader}.outColor", f"{sg}.surfaceShader", force=True)
    cmds.setAttr(f"{shader}.color", *color, type="double3")
    
    if emission > 0:
        cmds.setAttr(f"{shader}.incandescence", 
                     color[0] * emission, 
                     color[1] * emission, 
                     color[2] * emission, 
                     type="double3")
    
    return sg


def apply_material(obj, shading_group):
    """Apply a material to an object."""
    cmds.sets(obj, edit=True, forceElement=shading_group)


# ═══════════════════════════════════════════════════════════════════════════════
# X-WING FIGHTER
# ═══════════════════════════════════════════════════════════════════════════════

def build_xwing(name, colors, scale=1.0):
    """Build an X-Wing fighter with S-foils in attack position."""
    parts = []
    
    # Materials
    hull_mat = create_material(f"{name}_hull", colors["hull"])
    accent_mat = create_material(f"{name}_accent", colors["accent"])
    engine_mat = create_material(f"{name}_engine", colors["engine"], emission=0.8)
    cockpit_mat = create_material(f"{name}_cockpit", colors["cockpit"])
    
    # Main fuselage - elongated body
    fuselage = cmds.polyCylinder(r=0.3*scale, h=4*scale, sx=8, name=f"{name}_fuselage")[0]
    cmds.rotate(0, 0, 90, fuselage)
    apply_material(fuselage, hull_mat)
    parts.append(fuselage)
    
    # Nose cone
    nose = cmds.polyCone(r=0.3*scale, h=1.2*scale, sx=8, name=f"{name}_nose")[0]
    cmds.rotate(0, 0, -90, nose)
    cmds.move(2.6*scale, 0, 0, nose)
    apply_material(nose, hull_mat)
    parts.append(nose)
    
    # Cockpit canopy
    cockpit = cmds.polySphere(r=0.35*scale, sx=8, sy=8, name=f"{name}_cockpit")[0]
    cmds.scale(1, 0.6, 0.8, cockpit)
    cmds.move(0.5*scale, 0.2*scale, 0, cockpit)
    apply_material(cockpit, cockpit_mat)
    parts.append(cockpit)
    
    # S-foils (4 wings in X pattern)
    wing_positions = [
        (0, 0.4, 0.8, 25),    # Top right
        (0, 0.4, -0.8, -25),  # Top left
        (0, -0.4, 0.8, -25),  # Bottom right
        (0, -0.4, -0.8, 25),  # Bottom left
    ]
    
    for i, (wx, wy, wz, angle) in enumerate(wing_positions):
        # Wing strut
        wing = cmds.polyCube(w=2.5*scale, h=0.08*scale, d=0.4*scale, name=f"{name}_wing_{i}")[0]
        cmds.move(wx*scale, wy*scale, wz*scale, wing)
        cmds.rotate(angle, 0, 0, wing)
        apply_material(wing, hull_mat)
        parts.append(wing)
        
        # Engine nacelle at wing tip
        engine_x = 1.2 * scale
        engine_y = wy * scale + (0.5 if wy > 0 else -0.5) * scale * math.sin(math.radians(abs(angle)))
        engine_z = wz * scale + (0.8 if wz > 0 else -0.8) * scale
        
        engine = cmds.polyCylinder(r=0.12*scale, h=1.5*scale, sx=8, name=f"{name}_engine_{i}")[0]
        cmds.rotate(0, 0, 90, engine)
        cmds.move(engine_x, engine_y, engine_z, engine)
        apply_material(engine, hull_mat)
        parts.append(engine)
        
        # Engine glow
        glow = cmds.polyCylinder(r=0.1*scale, h=0.1*scale, sx=8, name=f"{name}_glow_{i}")[0]
        cmds.rotate(0, 0, 90, glow)
        cmds.move(engine_x - 0.8*scale, engine_y, engine_z, glow)
        apply_material(glow, engine_mat)
        parts.append(glow)
        
        # Laser cannon
        cannon = cmds.polyCylinder(r=0.03*scale, h=1.8*scale, sx=6, name=f"{name}_cannon_{i}")[0]
        cmds.rotate(0, 0, 90, cannon)
        cmds.move(1.5*scale, engine_y, engine_z, cannon)
        apply_material(cannon, accent_mat)
        parts.append(cannon)
    
    # Orange accent stripes on fuselage
    stripe = cmds.polyCube(w=1*scale, h=0.32*scale, d=0.02*scale, name=f"{name}_stripe")[0]
    cmds.move(0, 0, 0.31*scale, stripe)
    apply_material(stripe, accent_mat)
    parts.append(stripe)
    
    # Astromech droid socket
    droid = cmds.polyCylinder(r=0.15*scale, h=0.25*scale, sx=8, name=f"{name}_droid")[0]
    cmds.move(-0.5*scale, 0.35*scale, 0, droid)
    apply_material(droid, accent_mat)
    parts.append(droid)
    
    return parts


# ═══════════════════════════════════════════════════════════════════════════════
# TIE FIGHTER
# ═══════════════════════════════════════════════════════════════════════════════

def build_tie(name, colors, scale=1.0):
    """Build a TIE Fighter with hexagonal solar panels."""
    parts = []
    
    # Materials
    hull_mat = create_material(f"{name}_hull", colors["hull"])
    accent_mat = create_material(f"{name}_accent", colors["accent"])
    engine_mat = create_material(f"{name}_engine", colors["engine"], emission=0.8)
    cockpit_mat = create_material(f"{name}_cockpit", colors["cockpit"])
    
    # Central ball cockpit
    cockpit = cmds.polySphere(r=0.8*scale, sx=12, sy=12, name=f"{name}_cockpit")[0]
    apply_material(cockpit, hull_mat)
    parts.append(cockpit)
    
    # Cockpit window (front viewport)
    window = cmds.polyCylinder(r=0.4*scale, h=0.1*scale, sx=8, name=f"{name}_window")[0]
    cmds.rotate(0, 0, 90, window)
    cmds.move(0.75*scale, 0, 0, window)
    apply_material(window, cockpit_mat)
    parts.append(window)
    
    # Wing struts
    for side in [-1, 1]:
        strut = cmds.polyCylinder(r=0.08*scale, h=1.2*scale, sx=6, name=f"{name}_strut_{side}")[0]
        cmds.rotate(0, 0, 90, strut)
        cmds.rotate(90, 0, 0, strut)
        cmds.move(0, 0, side * 1.0 * scale, strut)
        apply_material(strut, accent_mat)
        parts.append(strut)
    
    # Hexagonal solar panel wings
    for side in [-1, 1]:
        # Create hexagonal wing
        wing = cmds.polyPipe(r=1.8*scale, h=0.05*scale, t=0.02*scale, sa=6, name=f"{name}_wing_{side}")[0]
        cmds.rotate(90, 0, 0, wing)
        cmds.move(0, 0, side * 1.6 * scale, wing)
        apply_material(wing, hull_mat)
        parts.append(wing)
        
        # Wing panel fill
        panel = cmds.polyCylinder(r=1.75*scale, h=0.03*scale, sx=6, name=f"{name}_panel_{side}")[0]
        cmds.rotate(90, 0, 0, panel)
        cmds.move(0, 0, side * 1.6 * scale, panel)
        apply_material(panel, accent_mat)
        parts.append(panel)
        
        # Solar panel lines (decorative)
        for i in range(3):
            line = cmds.polyCube(w=3.2*scale, h=0.08*scale, d=0.02*scale, name=f"{name}_line_{side}_{i}")[0]
            cmds.rotate(0, i * 60, 0, line)
            cmds.rotate(90, 0, 0, line, r=True)
            cmds.move(0, 0, side * 1.65 * scale, line)
            apply_material(line, hull_mat)
            parts.append(line)
    
    # Rear engine glow
    engine = cmds.polySphere(r=0.3*scale, sx=8, sy=8, name=f"{name}_engine")[0]
    cmds.move(-0.7*scale, 0, 0, engine)
    apply_material(engine, engine_mat)
    parts.append(engine)
    
    return parts


# ═══════════════════════════════════════════════════════════════════════════════
# Y-WING BOMBER
# ═══════════════════════════════════════════════════════════════════════════════

def build_ywing(name, colors, scale=1.0):
    """Build a Y-Wing bomber with exposed engine machinery."""
    parts = []
    
    # Materials
    hull_mat = create_material(f"{name}_hull", colors["hull"])
    accent_mat = create_material(f"{name}_accent", colors["accent"])
    engine_mat = create_material(f"{name}_engine", colors["engine"], emission=0.8)
    cockpit_mat = create_material(f"{name}_cockpit", colors["cockpit"])
    
    # Main cockpit module
    cockpit_body = cmds.polyCylinder(r=0.4*scale, h=2*scale, sx=8, name=f"{name}_body")[0]
    cmds.rotate(0, 0, 90, cockpit_body)
    apply_material(cockpit_body, hull_mat)
    parts.append(cockpit_body)
    
    # Cockpit canopy
    canopy = cmds.polySphere(r=0.35*scale, sx=8, sy=8, name=f"{name}_canopy")[0]
    cmds.scale(1.2, 0.7, 0.8, canopy)
    cmds.move(0.5*scale, 0.2*scale, 0, canopy)
    apply_material(canopy, cockpit_mat)
    parts.append(canopy)
    
    # Nose
    nose = cmds.polyCone(r=0.4*scale, h=1*scale, sx=8, name=f"{name}_nose")[0]
    cmds.rotate(0, 0, -90, nose)
    cmds.move(1.5*scale, 0, 0, nose)
    apply_material(nose, hull_mat)
    parts.append(nose)
    
    # Twin engine nacelles
    for side in [-1, 1]:
        # Engine housing (exposed framework look)
        nacelle = cmds.polyCylinder(r=0.25*scale, h=3*scale, sx=8, name=f"{name}_nacelle_{side}")[0]
        cmds.rotate(0, 0, 90, nacelle)
        cmds.move(-0.5*scale, 0, side * 1.2 * scale, nacelle)
        apply_material(nacelle, accent_mat)
        parts.append(nacelle)
        
        # Engine front intake
        intake = cmds.polyTorus(r=0.3*scale, sr=0.08*scale, sx=8, sy=8, name=f"{name}_intake_{side}")[0]
        cmds.rotate(0, 90, 0, intake)
        cmds.move(1*scale, 0, side * 1.2 * scale, intake)
        apply_material(intake, hull_mat)
        parts.append(intake)
        
        # Engine rear glow
        glow = cmds.polyCylinder(r=0.22*scale, h=0.15*scale, sx=8, name=f"{name}_glow_{side}")[0]
        cmds.rotate(0, 0, 90, glow)
        cmds.move(-2.1*scale, 0, side * 1.2 * scale, glow)
        apply_material(glow, engine_mat)
        parts.append(glow)
        
        # Support strut connecting cockpit to engines
        strut = cmds.polyCube(w=1*scale, h=0.1*scale, d=0.6*scale, name=f"{name}_strut_{side}")[0]
        cmds.move(-0.3*scale, 0, side * 0.6 * scale, strut)
        apply_material(strut, hull_mat)
        parts.append(strut)
    
    # Ion cannon turret on top
    turret_base = cmds.polyCylinder(r=0.2*scale, h=0.15*scale, sx=8, name=f"{name}_turret_base")[0]
    cmds.move(-0.3*scale, 0.45*scale, 0, turret_base)
    apply_material(turret_base, hull_mat)
    parts.append(turret_base)
    
    turret_gun = cmds.polyCylinder(r=0.06*scale, h=0.6*scale, sx=6, name=f"{name}_turret_gun")[0]
    cmds.rotate(0, 0, 90, turret_gun)
    cmds.move(0, 0.55*scale, 0, turret_gun)
    apply_material(turret_gun, accent_mat)
    parts.append(turret_gun)
    
    return parts


# ═══════════════════════════════════════════════════════════════════════════════
# A-WING INTERCEPTOR
# ═══════════════════════════════════════════════════════════════════════════════

def build_awing(name, colors, scale=1.0):
    """Build an A-Wing interceptor - small and fast."""
    parts = []
    
    # Materials
    hull_mat = create_material(f"{name}_hull", colors["hull"])
    accent_mat = create_material(f"{name}_accent", colors["accent"])
    engine_mat = create_material(f"{name}_engine", colors["engine"], emission=0.8)
    cockpit_mat = create_material(f"{name}_cockpit", colors["cockpit"])
    
    # Wedge-shaped main body
    body = cmds.polyCube(w=2.5*scale, h=0.4*scale, d=1.2*scale, name=f"{name}_body")[0]
    # Taper the front
    cmds.polyMoveVertex(f"{body}.vtx[0:1]", f"{body}.vtx[4:5]", tz=0.3*scale)
    cmds.polyMoveVertex(f"{body}.vtx[0]", f"{body}.vtx[2]", f"{body}.vtx[4]", f"{body}.vtx[6]", tx=0.5*scale)
    apply_material(body, hull_mat)
    parts.append(body)
    
    # Cockpit
    cockpit = cmds.polyCube(w=0.8*scale, h=0.35*scale, d=0.6*scale, name=f"{name}_cockpit")[0]
    cmds.move(0.3*scale, 0.3*scale, 0, cockpit)
    apply_material(cockpit, cockpit_mat)
    parts.append(cockpit)
    
    # Twin engines at rear
    for side in [-1, 1]:
        engine = cmds.polyCylinder(r=0.2*scale, h=0.8*scale, sx=8, name=f"{name}_engine_{side}")[0]
        cmds.rotate(0, 0, 90, engine)
        cmds.move(-1.0*scale, 0, side * 0.4 * scale, engine)
        apply_material(engine, hull_mat)
        parts.append(engine)
        
        # Engine glow
        glow = cmds.polyCylinder(r=0.18*scale, h=0.1*scale, sx=8, name=f"{name}_glow_{side}")[0]
        cmds.rotate(0, 0, 90, glow)
        cmds.move(-1.45*scale, 0, side * 0.4 * scale, glow)
        apply_material(glow, engine_mat)
        parts.append(glow)
    
    # Laser cannons on wingtips
    for side in [-1, 1]:
        cannon = cmds.polyCylinder(r=0.04*scale, h=1*scale, sx=6, name=f"{name}_cannon_{side}")[0]
        cmds.rotate(0, 0, 90, cannon)
        cmds.move(0.8*scale, 0, side * 0.6 * scale, cannon)
        apply_material(cannon, accent_mat)
        parts.append(cannon)
    
    # White accent stripe
    stripe = cmds.polyCube(w=2*scale, h=0.02*scale, d=0.15*scale, name=f"{name}_stripe")[0]
    cmds.move(0, 0.22*scale, 0, stripe)
    apply_material(stripe, accent_mat)
    parts.append(stripe)
    
    return parts


# ═══════════════════════════════════════════════════════════════════════════════
# MILLENNIUM FALCON STYLE FREIGHTER
# ═══════════════════════════════════════════════════════════════════════════════

def build_falcon(name, colors, scale=1.0):
    """Build a YT-1300 style light freighter."""
    parts = []
    
    # Materials
    hull_mat = create_material(f"{name}_hull", colors["hull"])
    accent_mat = create_material(f"{name}_accent", colors["accent"])
    engine_mat = create_material(f"{name}_engine", colors["engine"], emission=0.8)
    cockpit_mat = create_material(f"{name}_cockpit", colors["cockpit"])
    
    # Main disc body
    body = cmds.polyCylinder(r=2.5*scale, h=0.6*scale, sx=24, name=f"{name}_body")[0]
    apply_material(body, hull_mat)
    parts.append(body)
    
    # Front mandibles (the "forks")
    for side in [-1, 1]:
        mandible = cmds.polyCube(w=1.5*scale, h=0.5*scale, d=0.6*scale, name=f"{name}_mandible_{side}")[0]
        cmds.move(2.8*scale, 0, side * 0.8 * scale, mandible)
        apply_material(mandible, hull_mat)
        parts.append(mandible)
    
    # Gap between mandibles (cargo bay area)
    gap_cover = cmds.polyCube(w=1*scale, h=0.3*scale, d=1*scale, name=f"{name}_gap")[0]
    cmds.move(2.5*scale, -0.15*scale, 0, gap_cover)
    apply_material(gap_cover, accent_mat)
    parts.append(gap_cover)
    
    # Cockpit tube (offset to starboard)
    cockpit_tube = cmds.polyCylinder(r=0.4*scale, h=1.5*scale, sx=8, name=f"{name}_cockpit_tube")[0]
    cmds.rotate(0, 0, 90, cockpit_tube)
    cmds.move(1.5*scale, 0.2*scale, -2*scale, cockpit_tube)
    apply_material(cockpit_tube, hull_mat)
    parts.append(cockpit_tube)
    
    # Cockpit
    cockpit = cmds.polySphere(r=0.45*scale, sx=8, sy=8, name=f"{name}_cockpit")[0]
    cmds.scale(1.2, 0.8, 1, cockpit)
    cmds.move(2.3*scale, 0.2*scale, -2*scale, cockpit)
    apply_material(cockpit, cockpit_mat)
    parts.append(cockpit)
    
    # Radar dish on top
    dish = cmds.polyCylinder(r=0.6*scale, h=0.08*scale, sx=16, name=f"{name}_dish")[0]
    cmds.move(0.8*scale, 0.4*scale, 0.8*scale, dish)
    apply_material(dish, hull_mat)
    parts.append(dish)
    
    dish_arm = cmds.polyCylinder(r=0.05*scale, h=0.3*scale, sx=6, name=f"{name}_dish_arm")[0]
    cmds.move(0.8*scale, 0.5*scale, 0.8*scale, dish_arm)
    apply_material(dish_arm, accent_mat)
    parts.append(dish_arm)
    
    # Engine bank at rear (3 large engines)
    for i, offset in enumerate([-0.8, 0, 0.8]):
        engine = cmds.polyCylinder(r=0.4*scale, h=0.3*scale, sx=12, name=f"{name}_engine_{i}")[0]
        cmds.rotate(90, 0, 0, engine)
        cmds.move(-2.3*scale, 0, offset*scale, engine)
        apply_material(engine, hull_mat)
        parts.append(engine)
        
        # Engine glow
        glow = cmds.polyCylinder(r=0.35*scale, h=0.1*scale, sx=12, name=f"{name}_engine_glow_{i}")[0]
        cmds.rotate(90, 0, 0, glow)
        cmds.move(-2.5*scale, 0, offset*scale, glow)
        apply_material(glow, engine_mat)
        parts.append(glow)
    
    # Top turret
    turret = cmds.polySphere(r=0.3*scale, sx=8, sy=8, name=f"{name}_turret")[0]
    cmds.move(-0.5*scale, 0.5*scale, 0, turret)
    apply_material(turret, hull_mat)
    parts.append(turret)
    
    turret_gun = cmds.polyCylinder(r=0.05*scale, h=0.8*scale, sx=6, name=f"{name}_turret_gun")[0]
    cmds.move(-0.5*scale, 0.9*scale, 0, turret_gun)
    apply_material(turret_gun, accent_mat)
    parts.append(turret_gun)
    
    # Surface detail boxes
    for i in range(5):
        detail = cmds.polyCube(w=random.uniform(0.3, 0.6)*scale, 
                               h=random.uniform(0.1, 0.2)*scale, 
                               d=random.uniform(0.3, 0.6)*scale, 
                               name=f"{name}_detail_{i}")[0]
        angle = random.uniform(0, 360)
        dist = random.uniform(0.8, 1.8)
        x = dist * math.cos(math.radians(angle)) * scale
        z = dist * math.sin(math.radians(angle)) * scale
        cmds.move(x, 0.4*scale, z, detail)
        apply_material(detail, accent_mat)
        parts.append(detail)
    
    return parts


# ═══════════════════════════════════════════════════════════════════════════════
# IMPERIAL SHUTTLE
# ═══════════════════════════════════════════════════════════════════════════════

def build_shuttle(name, colors, scale=1.0):
    """Build a Lambda-class Imperial shuttle."""
    parts = []
    
    # Materials
    hull_mat = create_material(f"{name}_hull", colors["hull"])
    accent_mat = create_material(f"{name}_accent", colors["accent"])
    engine_mat = create_material(f"{name}_engine", colors["engine"], emission=0.8)
    cockpit_mat = create_material(f"{name}_cockpit", colors["cockpit"])
    
    # Main body
    body = cmds.polyCube(w=2.5*scale, h=1*scale, d=1.2*scale, name=f"{name}_body")[0]
    apply_material(body, hull_mat)
    parts.append(body)
    
    # Tapered nose
    nose = cmds.polyCube(w=1.5*scale, h=0.8*scale, d=1*scale, name=f"{name}_nose")[0]
    cmds.polyMoveVertex(f"{nose}.vtx[0:1]", f"{nose}.vtx[4:5]", tx=0.5*scale)
    cmds.move(2*scale, 0, 0, nose)
    apply_material(nose, hull_mat)
    parts.append(nose)
    
    # Cockpit windows
    for side in [-1, 1]:
        window = cmds.polyCube(w=0.6*scale, h=0.3*scale, d=0.05*scale, name=f"{name}_window_{side}")[0]
        cmds.move(2.5*scale, 0.1*scale, side * 0.35 * scale, window)
        apply_material(window, cockpit_mat)
        parts.append(window)
    
    # Dorsal fin (tall vertical wing)
    dorsal = cmds.polyCube(w=2*scale, h=4*scale, d=0.08*scale, name=f"{name}_dorsal")[0]
    # Taper to point
    cmds.polyMoveVertex(f"{dorsal}.vtx[2:3]", f"{dorsal}.vtx[6:7]", tx=1*scale)
    cmds.move(0, 2.5*scale, 0, dorsal)
    apply_material(dorsal, hull_mat)
    parts.append(dorsal)
    
    # Lower folding wings (in flight position - angled down)
    for side in [-1, 1]:
        wing = cmds.polyCube(w=2.5*scale, h=3*scale, d=0.06*scale, name=f"{name}_wing_{side}")[0]
        cmds.polyMoveVertex(f"{wing}.vtx[2:3]", f"{wing}.vtx[6:7]", tx=1.2*scale)
        cmds.rotate(0, 0, side * 45, wing)
        cmds.move(0, -1*scale, side * 1.5 * scale, wing)
        apply_material(wing, hull_mat)
        parts.append(wing)
    
    # Engine block at rear
    engine_block = cmds.polyCube(w=0.5*scale, h=0.8*scale, d=1*scale, name=f"{name}_engine_block")[0]
    cmds.move(-1.5*scale, 0, 0, engine_block)
    apply_material(engine_block, accent_mat)
    parts.append(engine_block)
    
    # Engine glows
    for i, offset in enumerate([-0.3, 0, 0.3]):
        glow = cmds.polyCylinder(r=0.12*scale, h=0.1*scale, sx=8, name=f"{name}_glow_{i}")[0]
        cmds.rotate(0, 0, 90, glow)
        cmds.move(-1.8*scale, 0, offset*scale, glow)
        apply_material(glow, engine_mat)
        parts.append(glow)
    
    return parts


# ═══════════════════════════════════════════════════════════════════════════════
# TIE INTERCEPTOR
# ═══════════════════════════════════════════════════════════════════════════════

def build_interceptor(name, colors, scale=1.0):
    """Build a TIE Interceptor with angled dagger wings."""
    parts = []
    
    # Materials
    hull_mat = create_material(f"{name}_hull", colors["hull"])
    accent_mat = create_material(f"{name}_accent", colors["accent"])
    engine_mat = create_material(f"{name}_engine", colors["engine"], emission=0.8)
    cockpit_mat = create_material(f"{name}_cockpit", colors["cockpit"])
    
    # Central ball cockpit (same as TIE Fighter)
    cockpit = cmds.polySphere(r=0.7*scale, sx=12, sy=12, name=f"{name}_cockpit")[0]
    apply_material(cockpit, hull_mat)
    parts.append(cockpit)
    
    # Cockpit window
    window = cmds.polyCylinder(r=0.35*scale, h=0.08*scale, sx=8, name=f"{name}_window")[0]
    cmds.rotate(0, 0, 90, window)
    cmds.move(0.65*scale, 0, 0, window)
    apply_material(window, cockpit_mat)
    parts.append(window)
    
    # Wing struts
    for side in [-1, 1]:
        strut = cmds.polyCylinder(r=0.06*scale, h=0.8*scale, sx=6, name=f"{name}_strut_{side}")[0]
        cmds.rotate(90, 0, 0, strut)
        cmds.move(0, 0, side * 0.8 * scale, strut)
        apply_material(strut, accent_mat)
        parts.append(strut)
    
    # Dagger-shaped wings (pointed, with cutouts)
    for side in [-1, 1]:
        # Main wing body - tall triangle
        wing = cmds.polyCube(w=0.6*scale, h=2.5*scale, d=0.04*scale, name=f"{name}_wing_{side}")[0]
        # Taper to dagger point
        cmds.polyMoveVertex(f"{wing}.vtx[2:3]", f"{wing}.vtx[6:7]", tz=side * 0.2 * scale)
        cmds.move(0, 0, side * 1.2 * scale, wing)
        apply_material(wing, hull_mat)
        parts.append(wing)
        
        # Laser cannons at wing tips (4 total - 2 per wing)
        for tip_y in [1.2, -1.2]:
            cannon = cmds.polyCylinder(r=0.03*scale, h=0.8*scale, sx=6, name=f"{name}_cannon_{side}_{tip_y}")[0]
            cmds.rotate(0, 0, 90, cannon)
            cmds.move(0.4*scale, tip_y*scale, side * 1.4 * scale, cannon)
            apply_material(cannon, accent_mat)
            parts.append(cannon)
    
    # Rear engine glow
    engine = cmds.polySphere(r=0.25*scale, sx=8, sy=8, name=f"{name}_engine")[0]
    cmds.move(-0.6*scale, 0, 0, engine)
    apply_material(engine, engine_mat)
    parts.append(engine)
    
    return parts


# ═══════════════════════════════════════════════════════════════════════════════
# SLAVE I / FIRESPRAY GUNSHIP
# ═══════════════════════════════════════════════════════════════════════════════

def build_slave1(name, colors, scale=1.0):
    """Build a Firespray-class patrol craft (Slave I style)."""
    parts = []
    
    # Materials
    hull_mat = create_material(f"{name}_hull", colors["hull"])
    accent_mat = create_material(f"{name}_accent", colors["accent"])
    engine_mat = create_material(f"{name}_engine", colors["engine"], emission=0.8)
    cockpit_mat = create_material(f"{name}_cockpit", colors["cockpit"])
    
    # Main body - tall and flat (flies vertically)
    body = cmds.polyCube(w=1.5*scale, h=3*scale, d=2*scale, name=f"{name}_body")[0]
    apply_material(body, hull_mat)
    parts.append(body)
    
    # Rounded front
    front = cmds.polyCylinder(r=0.75*scale, h=2*scale, sx=12, name=f"{name}_front")[0]
    cmds.rotate(90, 0, 0, front)
    cmds.move(0, 0, 1.5*scale, front)
    apply_material(front, hull_mat)
    parts.append(front)
    
    # Cockpit (at the top when flying)
    cockpit = cmds.polySphere(r=0.4*scale, sx=8, sy=8, name=f"{name}_cockpit")[0]
    cmds.scale(1.2, 0.8, 1, cockpit)
    cmds.move(0, 1.6*scale, 0.5*scale, cockpit)
    apply_material(cockpit, cockpit_mat)
    parts.append(cockpit)
    
    # Wing stabilizers
    for side in [-1, 1]:
        wing = cmds.polyCube(w=0.5*scale, h=2*scale, d=1.5*scale, name=f"{name}_wing_{side}")[0]
        cmds.move(side * 1 * scale, 0, 0, wing)
        apply_material(wing, hull_mat)
        parts.append(wing)
        
        # Wing tip detail
        tip = cmds.polyCone(r=0.15*scale, h=0.4*scale, sx=8, name=f"{name}_tip_{side}")[0]
        cmds.rotate(0, 0, side * 90, tip)
        cmds.move(side * 1.4 * scale, 0, 0, tip)
        apply_material(tip, accent_mat)
        parts.append(tip)
    
    # Engine array at bottom
    for i, offset in enumerate([-0.4, 0, 0.4]):
        engine = cmds.polyCylinder(r=0.2*scale, h=0.4*scale, sx=8, name=f"{name}_engine_{i}")[0]
        cmds.move(offset*scale, -1.7*scale, 0, engine)
        apply_material(engine, hull_mat)
        parts.append(engine)
        
        glow = cmds.polyCylinder(r=0.18*scale, h=0.1*scale, sx=8, name=f"{name}_glow_{i}")[0]
        cmds.move(offset*scale, -1.95*scale, 0, glow)
        apply_material(glow, engine_mat)
        parts.append(glow)
    
    # Weapon hardpoints
    for side in [-1, 1]:
        weapon = cmds.polyCylinder(r=0.08*scale, h=0.8*scale, sx=6, name=f"{name}_weapon_{side}")[0]
        cmds.move(side * 0.5 * scale, 0, 1.8*scale, weapon)
        cmds.rotate(90, 0, 0, weapon)
        apply_material(weapon, accent_mat)
        parts.append(weapon)
    
    # Accent stripe
    stripe = cmds.polyCube(w=1.6*scale, h=0.5*scale, d=0.05*scale, name=f"{name}_stripe")[0]
    cmds.move(0, 0.5*scale, 1.05*scale, stripe)
    apply_material(stripe, accent_mat)
    parts.append(stripe)
    
    return parts


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN SHIP CREATION FUNCTION
# ═══════════════════════════════════════════════════════════════════════════════

def create_ship(ship_type="xwing", name=None, scale=1.0, position=(0, 0, 0)):
    """
    Create a Star Wars inspired starship.
    
    Args:
        ship_type (str): Type of ship - "xwing", "tie", "ywing", "awing", 
                        "falcon", "shuttle", "interceptor", "slave1"
        name (str): Custom name for the ship (auto-generated if None)
        scale (float): Size multiplier
        position (tuple): (x, y, z) position
    
    Returns:
        str: Name of the created ship group
    """
    if ship_type not in SHIP_TYPES:
        print(f"⚠️ Unknown ship type '{ship_type}'. Available: {list(SHIP_TYPES.keys())}")
        ship_type = "xwing"
    
    config = SHIP_TYPES[ship_type]
    
    if name is None:
        name = f"{ship_type}_{random.randint(1, 999)}"
    
    print(f"\n{'═' * 50}")
    print(f"⭐ Creating {config['name']}: {name}")
    print(f"   {config['description']}")
    print(f"{'═' * 50}")
    
    # Build the ship
    builders = {
        "xwing": build_xwing,
        "tie": build_tie,
        "ywing": build_ywing,
        "awing": build_awing,
        "falcon": build_falcon,
        "shuttle": build_shuttle,
        "interceptor": build_interceptor,
        "slave1": build_slave1,
    }
    
    parts = builders[ship_type](name, config["colors"], scale)
    
    # Group all parts
    ship_group = cmds.group(parts, name=f"{name}_grp")
    
    # Position the ship
    cmds.move(position[0], position[1], position[2], ship_group)
    
    # Center pivot
    cmds.xform(ship_group, centerPivots=True)
    
    print(f"✅ {config['name']} created with {len(parts)} parts!")
    
    return ship_group


# ═══════════════════════════════════════════════════════════════════════════════
# FLEET CREATION
# ═══════════════════════════════════════════════════════════════════════════════

def create_fleet(faction="rebel", count=5, formation="attack"):
    """
    Create a fleet of ships.
    
    Args:
        faction (str): "rebel", "imperial", "mixed", or "bounty_hunter"
        count (int): Number of ships
        formation (str): "attack" (V), "patrol" (line), "escort" (diamond)
    
    Returns:
        str: Name of the fleet group
    """
    print(f"\n{'═' * 60}")
    print(f"⭐ CREATING {faction.upper()} FLEET - {count} ships in {formation} formation")
    print(f"{'═' * 60}")
    
    faction_ships = {
        "rebel": ["xwing", "xwing", "ywing", "awing", "falcon"],
        "imperial": ["tie", "tie", "tie", "interceptor", "shuttle"],
        "mixed": ["xwing", "tie", "falcon", "shuttle", "awing", "interceptor"],
        "bounty_hunter": ["slave1", "ywing", "falcon"],
    }
    
    ships_list = faction_ships.get(faction, faction_ships["mixed"])
    ships = []
    
    for i in range(count):
        ship_type = ships_list[i % len(ships_list)]
        
        # Calculate position based on formation
        if formation == "attack":  # V formation
            row = i // 2
            side = 1 if i % 2 == 0 else -1
            if i == 0:
                x, y, z = 0, 0, 0
            else:
                x = -row * 5
                z = side * row * 4
                y = 0
        elif formation == "patrol":  # Line
            x = i * 6
            y = 0
            z = 0
        elif formation == "escort":  # Diamond around center
            if i == 0:
                x, y, z = 0, 0, 0
            else:
                angle = ((i - 1) / (count - 1)) * 360 if count > 1 else 0
                radius = 8
                x = radius * math.cos(math.radians(angle))
                z = radius * math.sin(math.radians(angle))
                y = 0
        else:  # Random
            x = random.uniform(-15, 15)
            y = random.uniform(-3, 3)
            z = random.uniform(-15, 15)
        
        ship = create_ship(ship_type, position=(x, y, z))
        
        # Rotate to face forward
        if formation == "attack" and i > 0:
            cmds.rotate(0, 0, 0, ship)
        
        ships.append(ship)
    
    # Group the fleet
    fleet_grp = cmds.group(ships, name=f"{faction}_fleet_grp")
    
    print(f"\n{'═' * 60}")
    print(f"✅ {faction.upper()} FLEET CREATED!")
    print(f"   Ships: {count}")
    print(f"   Formation: {formation}")
    print(f"{'═' * 60}\n")
    
    return fleet_grp


# ═══════════════════════════════════════════════════════════════════════════════
# USER INTERFACE
# ═══════════════════════════════════════════════════════════════════════════════

def show_ui():
    """Show the Star Wars Fleet Generator UI."""
    window_name = "starwarsFleetUI"
    
    if cmds.window(window_name, exists=True):
        cmds.deleteUI(window_name)
    
    window = cmds.window(window_name, title="⭐ Star Wars Fleet Generator", 
                         widthHeight=(400, 500), sizeable=True)
    
    cmds.columnLayout(adjustableColumn=True, rowSpacing=10, columnOffset=["both", 10])
    
    cmds.separator(height=10)
    cmds.text(label="⭐ STAR WARS FLEET GENERATOR ⭐", font="boldLabelFont", height=30)
    cmds.text(label="Create iconic sci-fi starships!", font="smallPlainLabelFont")
    cmds.separator(height=10)
    
    # Single ship section
    cmds.frameLayout(label="Create Single Ship", collapsable=True, collapse=False)
    cmds.columnLayout(adjustableColumn=True, rowSpacing=5)
    
    cmds.text(label="Ship Type:", align="left")
    ship_menu = cmds.optionMenu(width=300)
    for ship_type, config in SHIP_TYPES.items():
        cmds.menuItem(label=f"{ship_type.upper()} - {config['name']}")
    
    cmds.text(label="Ship Name (optional):", align="left")
    name_field = cmds.textField(text="", width=300)
    
    scale_slider = cmds.floatSliderGrp(label="Scale:", field=True, 
                                        minValue=0.5, maxValue=3.0, value=1.0)
    
    def create_single(*args):
        ship_type = cmds.optionMenu(ship_menu, q=True, value=True).split(" - ")[0].lower()
        name = cmds.textField(name_field, q=True, text=True)
        scale = cmds.floatSliderGrp(scale_slider, q=True, value=True)
        create_ship(ship_type, name if name else None, scale)
    
    cmds.button(label="🚀 Create Ship", command=create_single, height=35)
    cmds.setParent("..")
    cmds.setParent("..")
    
    cmds.separator(height=10)
    
    # Fleet section
    cmds.frameLayout(label="Create Fleet", collapsable=True, collapse=False)
    cmds.columnLayout(adjustableColumn=True, rowSpacing=5)
    
    cmds.text(label="Faction:", align="left")
    faction_menu = cmds.optionMenu(width=300)
    cmds.menuItem(label="Rebel Alliance")
    cmds.menuItem(label="Galactic Empire")
    cmds.menuItem(label="Mixed Battle")
    cmds.menuItem(label="Bounty Hunters")
    
    cmds.text(label="Formation:", align="left")
    formation_menu = cmds.optionMenu(width=300)
    cmds.menuItem(label="Attack (V-formation)")
    cmds.menuItem(label="Patrol (Line)")
    cmds.menuItem(label="Escort (Diamond)")
    
    count_slider = cmds.intSliderGrp(label="Ship Count:", field=True,
                                      minValue=2, maxValue=12, value=5)
    
    def create_fleet_cmd(*args):
        faction_map = {
            "Rebel Alliance": "rebel",
            "Galactic Empire": "imperial",
            "Mixed Battle": "mixed",
            "Bounty Hunters": "bounty_hunter"
        }
        formation_map = {
            "Attack (V-formation)": "attack",
            "Patrol (Line)": "patrol",
            "Escort (Diamond)": "escort"
        }
        faction = faction_map[cmds.optionMenu(faction_menu, q=True, value=True)]
        formation = formation_map[cmds.optionMenu(formation_menu, q=True, value=True)]
        count = cmds.intSliderGrp(count_slider, q=True, value=True)
        create_fleet(faction, count, formation)
    
    cmds.button(label="⭐ Create Fleet", command=create_fleet_cmd, height=35)
    cmds.setParent("..")
    cmds.setParent("..")
    
    cmds.separator(height=10)
    
    # Quick buttons
    cmds.frameLayout(label="Quick Create", collapsable=True, collapse=True)
    cmds.columnLayout(adjustableColumn=True, rowSpacing=5)
    
    cmds.button(label="🔴 X-Wing", command=lambda x: create_ship("xwing"))
    cmds.button(label="⬛ TIE Fighter", command=lambda x: create_ship("tie"))
    cmds.button(label="🟡 Y-Wing", command=lambda x: create_ship("ywing"))
    cmds.button(label="🔴 A-Wing", command=lambda x: create_ship("awing"))
    cmds.button(label="⚪ Millennium Falcon", command=lambda x: create_ship("falcon"))
    cmds.button(label="⬜ Imperial Shuttle", command=lambda x: create_ship("shuttle"))
    cmds.button(label="⬛ TIE Interceptor", command=lambda x: create_ship("interceptor"))
    cmds.button(label="🟢 Slave I", command=lambda x: create_ship("slave1"))
    
    cmds.setParent("..")
    cmds.setParent("..")
    
    cmds.separator(height=10)
    cmds.text(label="May the Force be with you! ⭐", font="smallObliqueLabelFont")
    
    cmds.showWindow(window)


# ═══════════════════════════════════════════════════════════════════════════════
# QUICK TEST
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    # Quick test - create one of each
    print("Creating Star Wars fleet demo...")
    create_fleet("rebel", 5, "attack")
