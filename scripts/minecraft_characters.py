"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   🟫 MINECRAFT CHARACTER GENERATOR 🟫                                        ║
║   Create blocky voxel-style characters in Maya!                              ║
║                                                                              ║
║   Author: Douglas's Learning Project                                         ║
║   Version: 1.0.0                                                             ║
║                                                                              ║
║   Usage in Maya:                                                             ║
║       from minecraft_characters import create_character, create_village      ║
║       create_character("steve")    # Create Steve                            ║
║       create_village()             # Create a village of characters          ║
║       show_ui()                    # Open the UI                             ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import maya.cmds as cmds
import random
import math

# ═══════════════════════════════════════════════════════════════════════════════
# CHARACTER CONFIGURATIONS
# ═══════════════════════════════════════════════════════════════════════════════

CHARACTERS = {
    "steve": {
        "name": "Steve",
        "description": "The classic Minecraft player",
        "skin": (0.72, 0.53, 0.4),      # Skin tone
        "shirt": (0.0, 0.65, 0.65),      # Cyan shirt
        "pants": (0.2, 0.2, 0.6),        # Blue jeans
        "hair": (0.25, 0.15, 0.1),       # Brown hair
        "eyes": (0.3, 0.2, 0.5),         # Purple eyes
        "shoes": (0.3, 0.3, 0.3),        # Gray shoes
    },
    "alex": {
        "name": "Alex",
        "description": "The alternate player character",
        "skin": (0.78, 0.58, 0.45),      # Lighter skin
        "shirt": (0.3, 0.55, 0.2),       # Green shirt
        "pants": (0.4, 0.3, 0.2),        # Brown pants
        "hair": (0.85, 0.45, 0.15),      # Orange hair
        "eyes": (0.2, 0.5, 0.2),         # Green eyes
        "shoes": (0.35, 0.25, 0.15),     # Brown shoes
    },
    "zombie": {
        "name": "Zombie",
        "description": "Undead mob that spawns at night",
        "skin": (0.3, 0.5, 0.35),        # Green zombie skin
        "shirt": (0.0, 0.45, 0.45),      # Tattered cyan
        "pants": (0.15, 0.15, 0.4),      # Dark blue
        "hair": (0.2, 0.25, 0.2),        # Dark green hair
        "eyes": (0.1, 0.1, 0.1),         # Black eyes
        "shoes": (0.25, 0.25, 0.25),     # Dark shoes
    },
    "creeper": {
        "name": "Creeper",
        "description": "Explosive green mob - SSSSSS!",
        "skin": (0.3, 0.65, 0.3),        # Creeper green
        "shirt": (0.25, 0.55, 0.25),     # Slightly darker green
        "pants": (0.2, 0.45, 0.2),       # Even darker
        "hair": (0.3, 0.65, 0.3),        # Same as skin (no hair)
        "eyes": (0.0, 0.0, 0.0),         # Black eyes
        "shoes": (0.2, 0.45, 0.2),       # Dark green feet
        "special": "creeper_face"
    },
    "skeleton": {
        "name": "Skeleton",
        "description": "Bow-wielding undead archer",
        "skin": (0.85, 0.85, 0.8),       # Bone white
        "shirt": (0.8, 0.8, 0.75),       # Off-white
        "pants": (0.75, 0.75, 0.7),      # Light gray
        "hair": (0.85, 0.85, 0.8),       # No hair (skull)
        "eyes": (0.1, 0.1, 0.1),         # Dark eye sockets
        "shoes": (0.7, 0.7, 0.65),       # Bone feet
    },
    "enderman": {
        "name": "Enderman",
        "description": "Tall mysterious mob from The End",
        "skin": (0.1, 0.1, 0.12),        # Near black
        "shirt": (0.08, 0.08, 0.1),      # Very dark
        "pants": (0.06, 0.06, 0.08),     # Even darker
        "hair": (0.1, 0.1, 0.12),        # Same as skin
        "eyes": (0.8, 0.2, 0.8),         # Purple eyes
        "shoes": (0.05, 0.05, 0.06),     # Dark feet
        "special": "tall"
    },
    "villager": {
        "name": "Villager",
        "description": "Friendly NPC trader",
        "skin": (0.72, 0.55, 0.42),      # Skin tone
        "shirt": (0.5, 0.35, 0.2),       # Brown robe
        "pants": (0.45, 0.3, 0.15),      # Brown robe bottom
        "hair": (0.4, 0.25, 0.15),       # Brown hair
        "eyes": (0.2, 0.4, 0.2),         # Green eyes
        "shoes": (0.3, 0.2, 0.1),        # Brown shoes
        "special": "big_nose"
    },
    "pigman": {
        "name": "Zombie Piglin",
        "description": "Undead Nether mob",
        "skin": (0.75, 0.55, 0.5),       # Pinkish
        "shirt": (0.5, 0.35, 0.25),      # Brown cloth
        "pants": (0.4, 0.3, 0.2),        # Darker brown
        "hair": (0.3, 0.2, 0.15),        # Dark hair
        "eyes": (0.8, 0.1, 0.1),         # Red eyes
        "shoes": (0.35, 0.25, 0.15),     # Brown hooves
        "special": "pig_snout"
    },
    "witch": {
        "name": "Witch",
        "description": "Potion-throwing hostile mob",
        "skin": (0.6, 0.55, 0.5),        # Pale skin
        "shirt": (0.25, 0.1, 0.3),       # Purple robe
        "pants": (0.2, 0.08, 0.25),      # Darker purple
        "hair": (0.3, 0.3, 0.3),         # Gray hair
        "eyes": (0.5, 0.1, 0.5),         # Purple eyes
        "shoes": (0.15, 0.05, 0.2),      # Dark purple
        "special": "witch_hat"
    },
    "iron_golem": {
        "name": "Iron Golem",
        "description": "Powerful village protector",
        "skin": (0.7, 0.7, 0.68),        # Iron color
        "shirt": (0.65, 0.65, 0.62),     # Darker iron
        "pants": (0.6, 0.6, 0.58),       # Even darker
        "hair": (0.7, 0.7, 0.68),        # Same (no hair)
        "eyes": (0.4, 0.15, 0.15),       # Reddish
        "shoes": (0.55, 0.55, 0.52),     # Dark iron feet
        "special": "large"
    },
}

# Armor colors for equipped gear
ARMOR_TYPES = {
    "leather": (0.55, 0.35, 0.2),
    "chainmail": (0.6, 0.6, 0.65),
    "iron": (0.75, 0.75, 0.72),
    "gold": (0.9, 0.75, 0.2),
    "diamond": (0.3, 0.85, 0.85),
    "netherite": (0.25, 0.22, 0.25),
}


# ═══════════════════════════════════════════════════════════════════════════════
# MATERIAL CREATION
# ═══════════════════════════════════════════════════════════════════════════════

def create_material(name, color, emission=0.0):
    """Create a Lambert material with optional emission."""
    # Check if material already exists
    if cmds.objExists(f"{name}_mat"):
        return f"{name}_SG"
    
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
    """Apply material to an object."""
    cmds.sets(obj, edit=True, forceElement=shading_group)


# ═══════════════════════════════════════════════════════════════════════════════
# BODY PART BUILDERS
# ═══════════════════════════════════════════════════════════════════════════════

def create_head(name, colors, scale=1.0, y_offset=0):
    """Create the blocky Minecraft head."""
    parts = []
    
    # Head cube (8x8x8 in Minecraft pixels, scaled)
    head_size = 0.8 * scale
    head = cmds.polyCube(w=head_size, h=head_size, d=head_size, name=f"{name}_head")[0]
    cmds.move(0, (1.6 + y_offset) * scale, 0, head)
    
    head_mat = create_material(f"{name}_skin", colors["skin"])
    apply_material(head, head_mat)
    parts.append(head)
    
    # Hair (top of head)
    hair = cmds.polyCube(w=head_size * 1.02, h=0.15 * scale, d=head_size * 1.02, name=f"{name}_hair")[0]
    cmds.move(0, (2.0 + y_offset) * scale + 0.07 * scale, 0, hair)
    
    hair_mat = create_material(f"{name}_hair", colors["hair"])
    apply_material(hair, hair_mat)
    parts.append(hair)
    
    # Eyes
    eye_mat = create_material(f"{name}_eyes", colors["eyes"])
    for side in [-1, 1]:
        eye = cmds.polyCube(w=0.12 * scale, h=0.1 * scale, d=0.05 * scale, name=f"{name}_eye_{side}")[0]
        cmds.move(side * 0.15 * scale, (1.65 + y_offset) * scale, 0.38 * scale, eye)
        apply_material(eye, eye_mat)
        parts.append(eye)
    
    # Pupil (white part)
    pupil_mat = create_material(f"{name}_pupil", (0.9, 0.9, 0.9))
    for side in [-1, 1]:
        pupil = cmds.polyCube(w=0.06 * scale, h=0.06 * scale, d=0.02 * scale, name=f"{name}_pupil_{side}")[0]
        cmds.move(side * 0.15 * scale, (1.65 + y_offset) * scale, 0.41 * scale, pupil)
        apply_material(pupil, pupil_mat)
        parts.append(pupil)
    
    return parts


def create_body(name, colors, scale=1.0, y_offset=0):
    """Create the torso."""
    parts = []
    
    # Body (8x12x4 pixels scaled)
    body_w = 0.8 * scale
    body_h = 1.0 * scale
    body_d = 0.4 * scale
    
    body = cmds.polyCube(w=body_w, h=body_h, d=body_d, name=f"{name}_body")[0]
    cmds.move(0, (0.7 + y_offset) * scale, 0, body)
    
    shirt_mat = create_material(f"{name}_shirt", colors["shirt"])
    apply_material(body, shirt_mat)
    parts.append(body)
    
    return parts


def create_arms(name, colors, scale=1.0, y_offset=0, arm_pose="down"):
    """Create both arms."""
    parts = []
    
    arm_mat = create_material(f"{name}_skin", colors["skin"])
    shirt_mat = create_material(f"{name}_shirt", colors["shirt"])
    
    for side in [-1, 1]:
        # Upper arm (shirt)
        upper_arm = cmds.polyCube(w=0.35 * scale, h=0.5 * scale, d=0.35 * scale, 
                                   name=f"{name}_upper_arm_{side}")[0]
        cmds.move(side * 0.575 * scale, (0.95 + y_offset) * scale, 0, upper_arm)
        apply_material(upper_arm, shirt_mat)
        parts.append(upper_arm)
        
        # Lower arm (skin)
        lower_arm = cmds.polyCube(w=0.35 * scale, h=0.5 * scale, d=0.35 * scale,
                                   name=f"{name}_lower_arm_{side}")[0]
        cmds.move(side * 0.575 * scale, (0.45 + y_offset) * scale, 0, lower_arm)
        apply_material(lower_arm, arm_mat)
        parts.append(lower_arm)
        
        # Apply pose
        if arm_pose == "wave" and side == 1:
            cmds.rotate(0, 0, -45, upper_arm, lower_arm)
            cmds.move(side * 0.7 * scale, (1.1 + y_offset) * scale, 0, upper_arm)
            cmds.move(side * 0.9 * scale, (1.5 + y_offset) * scale, 0, lower_arm)
        elif arm_pose == "zombie":
            cmds.rotate(0, 0, -side * 80, upper_arm, lower_arm)
            cmds.move(side * 0.3 * scale, (0.95 + y_offset) * scale, 0.6 * scale, upper_arm)
            cmds.move(side * 0.3 * scale, (0.95 + y_offset) * scale, 1.1 * scale, lower_arm)
    
    return parts


def create_legs(name, colors, scale=1.0, y_offset=0, leg_pose="standing"):
    """Create both legs."""
    parts = []
    
    pants_mat = create_material(f"{name}_pants", colors["pants"])
    shoes_mat = create_material(f"{name}_shoes", colors["shoes"])
    
    for side in [-1, 1]:
        # Upper leg (pants)
        upper_leg = cmds.polyCube(w=0.35 * scale, h=0.5 * scale, d=0.35 * scale,
                                   name=f"{name}_upper_leg_{side}")[0]
        apply_material(upper_leg, pants_mat)
        
        # Lower leg (pants)
        lower_leg = cmds.polyCube(w=0.35 * scale, h=0.4 * scale, d=0.35 * scale,
                                   name=f"{name}_lower_leg_{side}")[0]
        apply_material(lower_leg, pants_mat)
        
        # Shoe
        shoe = cmds.polyCube(w=0.38 * scale, h=0.12 * scale, d=0.42 * scale,
                             name=f"{name}_shoe_{side}")[0]
        apply_material(shoe, shoes_mat)
        
        if leg_pose == "walking":
            angle = 25 * side
            cmds.move(side * 0.2 * scale, -0.05 * scale, side * 0.15 * scale, upper_leg)
            cmds.move(side * 0.2 * scale, -0.5 * scale, side * 0.25 * scale, lower_leg)
            cmds.move(side * 0.2 * scale, -0.85 * scale, side * 0.3 * scale, shoe)
            cmds.rotate(angle, 0, 0, upper_leg, lower_leg, shoe)
        else:
            cmds.move(side * 0.2 * scale, -0.05 * scale, 0, upper_leg)
            cmds.move(side * 0.2 * scale, -0.5 * scale, 0, lower_leg)
            cmds.move(side * 0.2 * scale, -0.85 * scale, 0.02 * scale, shoe)
        
        parts.extend([upper_leg, lower_leg, shoe])
    
    return parts


# ═══════════════════════════════════════════════════════════════════════════════
# SPECIAL FEATURES
# ═══════════════════════════════════════════════════════════════════════════════

def add_creeper_face(name, scale=1.0, y_offset=0):
    """Add the iconic creeper face."""
    parts = []
    black_mat = create_material(f"{name}_black", (0.05, 0.05, 0.05))
    
    # Eyes (two squares)
    for side in [-1, 1]:
        eye = cmds.polyCube(w=0.18 * scale, h=0.18 * scale, d=0.05 * scale, 
                            name=f"{name}_creeper_eye_{side}")[0]
        cmds.move(side * 0.18 * scale, (1.7 + y_offset) * scale, 0.38 * scale, eye)
        apply_material(eye, black_mat)
        parts.append(eye)
    
    # Mouth (sad face shape)
    mouth_top = cmds.polyCube(w=0.15 * scale, h=0.12 * scale, d=0.05 * scale,
                               name=f"{name}_mouth_top")[0]
    cmds.move(0, (1.5 + y_offset) * scale, 0.38 * scale, mouth_top)
    apply_material(mouth_top, black_mat)
    parts.append(mouth_top)
    
    # Mouth sides
    for side in [-1, 1]:
        mouth_side = cmds.polyCube(w=0.1 * scale, h=0.2 * scale, d=0.05 * scale,
                                    name=f"{name}_mouth_side_{side}")[0]
        cmds.move(side * 0.12 * scale, (1.35 + y_offset) * scale, 0.38 * scale, mouth_side)
        apply_material(mouth_side, black_mat)
        parts.append(mouth_side)
    
    return parts


def add_villager_nose(name, scale=1.0, y_offset=0):
    """Add the big villager nose."""
    skin_mat = create_material(f"{name}_nose", (0.65, 0.48, 0.35))
    
    nose = cmds.polyCube(w=0.2 * scale, h=0.25 * scale, d=0.35 * scale,
                         name=f"{name}_big_nose")[0]
    cmds.move(0, (1.55 + y_offset) * scale, 0.5 * scale, nose)
    apply_material(nose, skin_mat)
    
    return [nose]


def add_pig_snout(name, scale=1.0, y_offset=0):
    """Add pig-like snout."""
    snout_mat = create_material(f"{name}_snout", (0.85, 0.65, 0.6))
    
    snout = cmds.polyCube(w=0.3 * scale, h=0.2 * scale, d=0.2 * scale,
                          name=f"{name}_snout")[0]
    cmds.move(0, (1.5 + y_offset) * scale, 0.45 * scale, snout)
    apply_material(snout, snout_mat)
    
    # Nostrils
    nostril_mat = create_material(f"{name}_nostril", (0.3, 0.2, 0.2))
    nostrils = []
    for side in [-1, 1]:
        nostril = cmds.polyCube(w=0.06 * scale, h=0.08 * scale, d=0.05 * scale,
                                 name=f"{name}_nostril_{side}")[0]
        cmds.move(side * 0.08 * scale, (1.5 + y_offset) * scale, 0.56 * scale, nostril)
        apply_material(nostril, nostril_mat)
        nostrils.append(nostril)
    
    return [snout] + nostrils


def add_witch_hat(name, scale=1.0, y_offset=0):
    """Add a witch hat."""
    hat_mat = create_material(f"{name}_hat", (0.15, 0.05, 0.2))
    buckle_mat = create_material(f"{name}_buckle", (0.4, 0.6, 0.2))
    
    # Hat brim
    brim = cmds.polyCylinder(r=0.6 * scale, h=0.08 * scale, sx=8, name=f"{name}_brim")[0]
    cmds.move(0, (2.15 + y_offset) * scale, 0, brim)
    apply_material(brim, hat_mat)
    
    # Hat cone
    cone = cmds.polyCone(r=0.35 * scale, h=0.7 * scale, sx=8, name=f"{name}_hat_cone")[0]
    cmds.move(0, (2.55 + y_offset) * scale, 0, cone)
    # Bend the tip
    cmds.rotate(0, 0, 15, cone)
    cmds.move(0.1 * scale, 0, 0, cone, r=True)
    apply_material(cone, hat_mat)
    
    # Green buckle
    buckle = cmds.polyCube(w=0.15 * scale, h=0.12 * scale, d=0.4 * scale,
                           name=f"{name}_buckle")[0]
    cmds.move(0, (2.25 + y_offset) * scale, 0, buckle)
    apply_material(buckle, buckle_mat)
    
    return [brim, cone, buckle]


def add_held_item(name, item_type, scale=1.0, y_offset=0):
    """Add an item to the character's hand."""
    parts = []
    
    if item_type == "sword":
        # Diamond sword
        blade_mat = create_material(f"{name}_blade", (0.3, 0.85, 0.85))
        handle_mat = create_material(f"{name}_handle", (0.4, 0.25, 0.15))
        
        blade = cmds.polyCube(w=0.08 * scale, h=0.8 * scale, d=0.15 * scale,
                              name=f"{name}_blade")[0]
        cmds.move(0.8 * scale, (0.8 + y_offset) * scale, 0, blade)
        cmds.rotate(0, 0, -45, blade)
        apply_material(blade, blade_mat)
        parts.append(blade)
        
        handle = cmds.polyCube(w=0.1 * scale, h=0.25 * scale, d=0.1 * scale,
                               name=f"{name}_sword_handle")[0]
        cmds.move(0.6 * scale, (0.5 + y_offset) * scale, 0, handle)
        cmds.rotate(0, 0, -45, handle)
        apply_material(handle, handle_mat)
        parts.append(handle)
        
    elif item_type == "pickaxe":
        # Iron pickaxe
        head_mat = create_material(f"{name}_pick_head", (0.7, 0.7, 0.68))
        stick_mat = create_material(f"{name}_stick", (0.55, 0.35, 0.2))
        
        stick = cmds.polyCube(w=0.08 * scale, h=0.9 * scale, d=0.08 * scale,
                              name=f"{name}_pick_stick")[0]
        cmds.move(0.75 * scale, (0.6 + y_offset) * scale, 0, stick)
        cmds.rotate(0, 0, -45, stick)
        apply_material(stick, stick_mat)
        parts.append(stick)
        
        head = cmds.polyCube(w=0.6 * scale, h=0.15 * scale, d=0.1 * scale,
                             name=f"{name}_pick_head")[0]
        cmds.move(0.95 * scale, (1.0 + y_offset) * scale, 0, head)
        cmds.rotate(0, 0, -45, head)
        apply_material(head, head_mat)
        parts.append(head)
        
    elif item_type == "bow":
        bow_mat = create_material(f"{name}_bow", (0.5, 0.35, 0.2))
        string_mat = create_material(f"{name}_string", (0.9, 0.9, 0.9))
        
        # Bow curve (simplified)
        bow = cmds.polyCylinder(r=0.03 * scale, h=0.8 * scale, sx=6,
                                name=f"{name}_bow")[0]
        cmds.move(0.7 * scale, (0.7 + y_offset) * scale, 0.3 * scale, bow)
        cmds.rotate(0, 45, 0, bow)
        apply_material(bow, bow_mat)
        parts.append(bow)
        
        string = cmds.polyCube(w=0.02 * scale, h=0.7 * scale, d=0.02 * scale,
                               name=f"{name}_string")[0]
        cmds.move(0.75 * scale, (0.7 + y_offset) * scale, 0.15 * scale, string)
        apply_material(string, string_mat)
        parts.append(string)
    
    return parts


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN CHARACTER CREATION
# ═══════════════════════════════════════════════════════════════════════════════

def create_character(char_type="steve", name=None, scale=1.0, position=(0, 0, 0),
                     pose="standing", held_item=None, armor=None):
    """
    Create a Minecraft-style character.
    
    Args:
        char_type (str): Character type from CHARACTERS dict
        name (str): Custom name (auto-generated if None)
        scale (float): Size multiplier
        position (tuple): (x, y, z) world position
        pose (str): "standing", "walking", "wave", "zombie"
        held_item (str): "sword", "pickaxe", "bow", or None
        armor (str): Armor type or None
    
    Returns:
        str: Name of the character group
    """
    if char_type not in CHARACTERS:
        print(f"⚠️ Unknown character '{char_type}'. Available: {list(CHARACTERS.keys())}")
        char_type = "steve"
    
    config = CHARACTERS[char_type]
    
    if name is None:
        name = f"{char_type}_{random.randint(100, 999)}"
    
    print(f"\n{'═' * 50}")
    print(f"🟫 Creating {config['name']}: {name}")
    print(f"   {config['description']}")
    print(f"{'═' * 50}")
    
    all_parts = []
    
    # Handle special sizing
    y_offset = 0
    char_scale = scale
    
    if config.get("special") == "tall":  # Enderman
        char_scale = scale * 1.5
        y_offset = 0.5
    elif config.get("special") == "large":  # Iron Golem
        char_scale = scale * 1.8
        y_offset = 0.8
    
    # Build the character
    arm_pose = pose if pose in ["wave", "zombie"] else "down"
    leg_pose = "walking" if pose == "walking" else "standing"
    
    all_parts.extend(create_head(name, config, char_scale, y_offset))
    all_parts.extend(create_body(name, config, char_scale, y_offset))
    all_parts.extend(create_arms(name, config, char_scale, y_offset, arm_pose))
    all_parts.extend(create_legs(name, config, char_scale, y_offset, leg_pose))
    
    # Add special features
    special = config.get("special")
    if special == "creeper_face":
        all_parts.extend(add_creeper_face(name, char_scale, y_offset))
    elif special == "big_nose":
        all_parts.extend(add_villager_nose(name, char_scale, y_offset))
    elif special == "pig_snout":
        all_parts.extend(add_pig_snout(name, char_scale, y_offset))
    elif special == "witch_hat":
        all_parts.extend(add_witch_hat(name, char_scale, y_offset))
    
    # Add held item
    if held_item:
        all_parts.extend(add_held_item(name, held_item, char_scale, y_offset))
    
    # Add armor highlights
    if armor and armor in ARMOR_TYPES:
        armor_mat = create_material(f"{name}_armor", ARMOR_TYPES[armor])
        # Simple armor overlay on body
        chest = cmds.polyCube(w=0.82 * char_scale, h=0.85 * char_scale, d=0.42 * char_scale,
                              name=f"{name}_chestplate")[0]
        cmds.move(0, (0.75 + y_offset) * char_scale, 0, chest)
        apply_material(chest, armor_mat)
        all_parts.append(chest)
    
    # Group everything
    char_group = cmds.group(all_parts, name=f"{name}_grp")
    
    # Position
    cmds.move(position[0], position[1], position[2], char_group)
    cmds.xform(char_group, centerPivots=True)
    
    print(f"✅ {config['name']} created with {len(all_parts)} parts!")
    
    return char_group


# ═══════════════════════════════════════════════════════════════════════════════
# VILLAGE / GROUP CREATION
# ═══════════════════════════════════════════════════════════════════════════════

def create_village(character_count=6, radius=10):
    """
    Create a village scene with multiple characters.
    
    Args:
        character_count (int): Number of characters
        radius (float): Spread radius
    
    Returns:
        str: Name of the village group
    """
    print(f"\n{'═' * 60}")
    print(f"🏘️ CREATING MINECRAFT VILLAGE - {character_count} characters")
    print(f"{'═' * 60}")
    
    characters = []
    
    # Ensure variety
    char_types = list(CHARACTERS.keys())
    poses = ["standing", "walking", "wave"]
    items = [None, None, "sword", "pickaxe", "bow"]
    
    for i in range(character_count):
        char_type = char_types[i % len(char_types)]
        
        # Calculate position in a rough circle
        angle = (i / character_count) * 360
        x = radius * math.cos(math.radians(angle)) * random.uniform(0.6, 1.0)
        z = radius * math.sin(math.radians(angle)) * random.uniform(0.6, 1.0)
        
        pose = random.choice(poses)
        item = random.choice(items) if char_type in ["steve", "alex", "skeleton"] else None
        
        # Face center
        char = create_character(
            char_type=char_type,
            position=(x, 0, z),
            pose=pose,
            held_item=item
        )
        
        # Rotate to face center
        cmds.rotate(0, -angle + 90, 0, char)
        
        characters.append(char)
    
    # Group all characters
    village_grp = cmds.group(characters, name="minecraft_village_grp")
    
    print(f"\n{'═' * 60}")
    print(f"✅ VILLAGE CREATED - {character_count} characters!")
    print(f"{'═' * 60}\n")
    
    return village_grp


def create_mob_horde(mob_type="zombie", count=8, formation="swarm"):
    """
    Create a horde of hostile mobs.
    
    Args:
        mob_type (str): "zombie", "skeleton", "creeper"
        count (int): Number of mobs
        formation (str): "swarm", "line", "ambush"
    
    Returns:
        str: Name of the horde group
    """
    print(f"\n{'═' * 60}")
    print(f"👾 CREATING {mob_type.upper()} HORDE - {count} mobs!")
    print(f"{'═' * 60}")
    
    mobs = []
    
    for i in range(count):
        if formation == "line":
            x = i * 2
            z = 0
        elif formation == "ambush":
            # Semi-circle
            angle = (i / count) * 180 - 90
            x = 8 * math.cos(math.radians(angle))
            z = 8 * math.sin(math.radians(angle))
        else:  # swarm
            x = random.uniform(-8, 8)
            z = random.uniform(-8, 8)
        
        pose = "zombie" if mob_type == "zombie" else "walking"
        item = "bow" if mob_type == "skeleton" else None
        
        mob = create_character(
            char_type=mob_type,
            position=(x, 0, z),
            pose=pose,
            held_item=item
        )
        
        # Rotate to face forward
        if formation == "ambush":
            cmds.rotate(0, -angle, 0, mob)
        
        mobs.append(mob)
    
    horde_grp = cmds.group(mobs, name=f"{mob_type}_horde_grp")
    
    print(f"✅ {mob_type.upper()} HORDE CREATED!")
    
    return horde_grp


# ═══════════════════════════════════════════════════════════════════════════════
# USER INTERFACE
# ═══════════════════════════════════════════════════════════════════════════════

def show_ui():
    """Show the Minecraft Character Generator UI."""
    window_name = "minecraftCharUI"
    
    if cmds.window(window_name, exists=True):
        cmds.deleteUI(window_name)
    
    window = cmds.window(window_name, title="🟫 Minecraft Character Generator",
                         widthHeight=(420, 550), sizeable=True)
    
    cmds.columnLayout(adjustableColumn=True, rowSpacing=10, columnOffset=["both", 10])
    
    cmds.separator(height=10)
    cmds.text(label="🟫 MINECRAFT CHARACTER GENERATOR 🟫", font="boldLabelFont", height=30)
    cmds.text(label="Create blocky voxel-style characters!", font="smallPlainLabelFont")
    cmds.separator(height=10)
    
    # Single character section
    cmds.frameLayout(label="Create Single Character", collapsable=True, collapse=False)
    cmds.columnLayout(adjustableColumn=True, rowSpacing=5)
    
    cmds.text(label="Character Type:", align="left")
    char_menu = cmds.optionMenu(width=300)
    for char_type, config in CHARACTERS.items():
        cmds.menuItem(label=f"{char_type.upper()} - {config['name']}")
    
    cmds.text(label="Pose:", align="left")
    pose_menu = cmds.optionMenu(width=300)
    cmds.menuItem(label="Standing")
    cmds.menuItem(label="Walking")
    cmds.menuItem(label="Wave")
    cmds.menuItem(label="Zombie Arms")
    
    cmds.text(label="Held Item:", align="left")
    item_menu = cmds.optionMenu(width=300)
    cmds.menuItem(label="None")
    cmds.menuItem(label="Diamond Sword")
    cmds.menuItem(label="Iron Pickaxe")
    cmds.menuItem(label="Bow")
    
    cmds.text(label="Armor:", align="left")
    armor_menu = cmds.optionMenu(width=300)
    cmds.menuItem(label="None")
    for armor_type in ARMOR_TYPES.keys():
        cmds.menuItem(label=armor_type.title())
    
    scale_slider = cmds.floatSliderGrp(label="Scale:", field=True,
                                        minValue=0.5, maxValue=3.0, value=1.0)
    
    def create_single(*args):
        char_type = cmds.optionMenu(char_menu, q=True, value=True).split(" - ")[0].lower()
        pose_map = {"Standing": "standing", "Walking": "walking", 
                    "Wave": "wave", "Zombie Arms": "zombie"}
        pose = pose_map[cmds.optionMenu(pose_menu, q=True, value=True)]
        
        item_map = {"None": None, "Diamond Sword": "sword", 
                    "Iron Pickaxe": "pickaxe", "Bow": "bow"}
        item = item_map[cmds.optionMenu(item_menu, q=True, value=True)]
        
        armor = cmds.optionMenu(armor_menu, q=True, value=True).lower()
        armor = None if armor == "none" else armor
        
        scale = cmds.floatSliderGrp(scale_slider, q=True, value=True)
        
        create_character(char_type, scale=scale, pose=pose, held_item=item, armor=armor)
    
    cmds.button(label="🧱 Create Character", command=create_single, height=35)
    cmds.setParent("..")
    cmds.setParent("..")
    
    cmds.separator(height=10)
    
    # Village section
    cmds.frameLayout(label="Create Groups", collapsable=True, collapse=False)
    cmds.columnLayout(adjustableColumn=True, rowSpacing=5)
    
    village_slider = cmds.intSliderGrp(label="Village Size:", field=True,
                                        minValue=3, maxValue=12, value=6)
    
    def create_village_cmd(*args):
        count = cmds.intSliderGrp(village_slider, q=True, value=True)
        create_village(count)
    
    cmds.button(label="🏘️ Create Village", command=create_village_cmd, height=30)
    
    cmds.separator(height=5)
    
    cmds.text(label="Mob Horde Type:", align="left")
    horde_menu = cmds.optionMenu(width=300)
    cmds.menuItem(label="Zombie Horde")
    cmds.menuItem(label="Skeleton Army")
    cmds.menuItem(label="Creeper Swarm")
    
    horde_slider = cmds.intSliderGrp(label="Horde Size:", field=True,
                                      minValue=3, maxValue=15, value=8)
    
    def create_horde_cmd(*args):
        horde_map = {"Zombie Horde": "zombie", "Skeleton Army": "skeleton", 
                     "Creeper Swarm": "creeper"}
        mob_type = horde_map[cmds.optionMenu(horde_menu, q=True, value=True)]
        count = cmds.intSliderGrp(horde_slider, q=True, value=True)
        create_mob_horde(mob_type, count)
    
    cmds.button(label="👾 Create Mob Horde", command=create_horde_cmd, height=30)
    cmds.setParent("..")
    cmds.setParent("..")
    
    cmds.separator(height=10)
    
    # Quick buttons
    cmds.frameLayout(label="Quick Create", collapsable=True, collapse=True)
    cmds.columnLayout(adjustableColumn=True, rowSpacing=3)
    
    cmds.button(label="👤 Steve", command=lambda x: create_character("steve"))
    cmds.button(label="👩 Alex", command=lambda x: create_character("alex"))
    cmds.button(label="🧟 Zombie", command=lambda x: create_character("zombie", pose="zombie"))
    cmds.button(label="💀 Skeleton", command=lambda x: create_character("skeleton", held_item="bow"))
    cmds.button(label="💚 Creeper", command=lambda x: create_character("creeper"))
    cmds.button(label="👁️ Enderman", command=lambda x: create_character("enderman"))
    cmds.button(label="👃 Villager", command=lambda x: create_character("villager"))
    cmds.button(label="🐷 Zombie Piglin", command=lambda x: create_character("pigman"))
    cmds.button(label="🧙 Witch", command=lambda x: create_character("witch"))
    cmds.button(label="🤖 Iron Golem", command=lambda x: create_character("iron_golem"))
    
    cmds.setParent("..")
    cmds.setParent("..")
    
    cmds.separator(height=10)
    cmds.text(label="Block by block! 🟫", font="smallObliqueLabelFont")
    
    cmds.showWindow(window)


# ═══════════════════════════════════════════════════════════════════════════════
# DEMO
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("Creating Minecraft character demo...")
    create_village(6)
