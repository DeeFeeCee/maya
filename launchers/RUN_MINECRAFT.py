"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   🟫 MINECRAFT CHARACTER LAUNCHER 🟫                                         ║
║   Create blocky voxel-style characters in Maya!                              ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 FUNCTION SIGNATURES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

create_character(char_type, name=None, scale=1.0, position=(0,0,0), 
                 pose="standing", held_item=None, armor=None)
    char_type : str    - Character type (see CHARACTER TYPES below)
    name      : str    - Custom name (auto-generated if None)
    scale     : float  - Size multiplier (default: 1.0)
    position  : tuple  - (x, y, z) world position
    pose      : str    - "standing", "walking", "wave", "zombie"
    held_item : str    - "sword", "pickaxe", "bow", or None
    armor     : str    - Armor type or None

create_village(character_count=6, radius=10)
    character_count : int   - Number of villagers (3-12)
    radius         : float  - Spread radius

create_mob_horde(mob_type, count=8, formation="swarm")
    mob_type  : str    - "zombie", "skeleton", "creeper"
    count     : int    - Number of mobs
    formation : str    - "swarm", "line", "ambush"

show_ui()
    Opens the Minecraft Character Generator UI window

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🧱 CHARACTER TYPES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PLAYERS:
  "steve"       - Classic Minecraft player (cyan shirt, blue pants)
  "alex"        - Alternate player (green shirt, orange hair)

HOSTILE MOBS:
  "zombie"      - Green undead mob (arms out pose available)
  "skeleton"    - Bone archer (give it a bow!)
  "creeper"     - Explosive green mob with iconic face
  "enderman"    - Tall dark mob with purple eyes
  "witch"       - Purple-robed mob with hat

NEUTRAL/FRIENDLY:
  "villager"    - Friendly NPC trader with big nose
  "pigman"      - Zombie Piglin from the Nether
  "iron_golem"  - Large village protector

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚔️ EQUIPMENT OPTIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

HELD ITEMS (held_item=):
  "sword"    - Diamond sword
  "pickaxe"  - Iron pickaxe
  "bow"      - Wooden bow

ARMOR TYPES (armor=):
  "leather"    - Brown leather armor
  "chainmail"  - Gray chain armor
  "iron"       - Silver iron armor
  "gold"       - Golden armor
  "diamond"    - Cyan diamond armor
  "netherite"  - Dark netherite armor

POSES (pose=):
  "standing"  - Default standing pose
  "walking"   - Legs apart, walking motion
  "wave"      - Right arm raised waving
  "zombie"    - Both arms extended forward

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📝 USAGE EXAMPLES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Create individual characters:
create_character("steve")                                    # Basic Steve
create_character("alex", pose="wave")                        # Alex waving
create_character("zombie", pose="zombie")                    # Zombie with arms out
create_character("skeleton", held_item="bow")                # Skeleton archer
create_character("steve", armor="diamond", held_item="sword") # Diamond warrior

# Create groups:
create_village(6)                                            # Village with 6 characters
create_mob_horde("zombie", count=10)                         # Zombie swarm
create_mob_horde("skeleton", count=6, formation="line")      # Skeleton line
create_mob_horde("creeper", count=8, formation="ambush")     # Creeper ambush!

# Battle scene:
create_character("steve", armor="iron", held_item="sword", position=(0, 0, 0))
create_mob_horde("zombie", count=6, formation="ambush")

# Open the UI:
show_ui()

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⬇️ COPY CODE BELOW TO MAYA SCRIPT EDITOR ⬇️
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import sys
import os

# Add scripts folder to path
scripts_path = r"c:\Development\maya\scripts"
if scripts_path not in sys.path:
    sys.path.insert(0, scripts_path)

# Import and reload for development
import minecraft_characters
import importlib
importlib.reload(minecraft_characters)

# Import functions for easy access
from minecraft_characters import create_character, create_village, create_mob_horde, show_ui

# ═══════════════════════════════════════════════════════════════════════════════
# 🧱 QUICK START - Uncomment what you want!
# ═══════════════════════════════════════════════════════════════════════════════

# --- OPTION 1: Open the UI ---
show_ui()

# --- OPTION 2: Create Steve and Alex ---
# create_character("steve")
# create_character("alex", position=(3, 0, 0), pose="wave")

# --- OPTION 3: Create a village scene ---
# create_village(8)

# --- OPTION 4: Create a zombie horde! ---
# create_mob_horde("zombie", count=10)

# --- OPTION 5: Skeleton army ---
# create_mob_horde("skeleton", count=8, formation="line")

# --- OPTION 6: Epic battle scene ---
# create_character("steve", armor="diamond", held_item="sword", position=(0, 0, 0))
# create_character("alex", armor="iron", held_item="sword", position=(2, 0, 0))
# create_mob_horde("zombie", count=8, formation="ambush")

# --- OPTION 7: One of each character ---
# chars = ["steve", "alex", "zombie", "skeleton", "creeper", "enderman", 
#          "villager", "pigman", "witch", "iron_golem"]
# for i, char in enumerate(chars):
#     create_character(char, position=(i * 3, 0, 0))

# --- OPTION 8: Creeper army (DANGER!) ---
# create_mob_horde("creeper", count=12, formation="swarm")
