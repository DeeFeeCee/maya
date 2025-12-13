# Domain Knowledge: Game Design & Maya Integration

**Version**: 1.0.0
**Created**: 2025-12-12
**Domain**: Game Design, Procedural Content Generation, Technical Art
**Identity**: Alex Game Designer

---

## Core Expertise

### Procedural Content Generation for Games

| Concept | Implementation | Game Application |
|---------|----------------|------------------|
| **Parametric Modeling** | Functions with tunable parameters | Infinite asset variations from single template |
| **Theme Systems** | Color/material dictionaries | Faction identity, visual storytelling |
| **Class Hierarchies** | Ship types with distinct stats | Gameplay roles, balanced archetypes |
| **Formation Systems** | Spatial arrangement algorithms | AI squad behaviors, RTS mechanics |
| **Animation States** | Keyframe-based state machines | Game feel, juice, polish |

### Maya-to-Game Pipeline Knowledge

```
Maya Python Script → Procedural Assets → Export → Game Engine
     ↓                    ↓                         ↓
  Parameters          Variations              Runtime spawning
  (ship_class,        (1000s of unique        (enemy waves,
   theme, scale)       combinations)           loot drops)
```

### Technical Art Principles

1. **Content Scaling**: One well-designed generator > 100 hand-made assets
2. **Artist Empowerment**: UI tools that hide complexity, expose creativity
3. **Consistency Through Systems**: Themes ensure visual coherence across variations
4. **Performance Awareness**: Primitive-based geometry = predictable poly counts

---

## Starship Generator as Game Design Teaching Tool

### Design Decisions That Teach

| Script Feature | Game Design Lesson |
|----------------|-------------------|
| `SHIP_THEMES` dictionary | Data-driven design, easy iteration |
| `SHIP_CLASSES` with descriptions | Role clarity, player communication |
| `create_squadron()` formations | Emergent complexity from simple rules |
| `animation_style` parameter | State machines, behavior variety |
| `show_ui()` function | Accessibility, onboarding |

### Faction Design Framework

```python
# Pattern for game-ready faction systems
FACTION_TEMPLATE = {
    "name": str,           # Identity
    "colors": {            # Visual language
        "primary": tuple,
        "secondary": tuple,
        "accent": tuple,
        "glow": tuple,
    },
    "ship_classes": [],    # Available units
    "formation_style": str,# AI personality
    "lore_notes": str,     # Worldbuilding hook
}
```

---

## Teaching Methodology: Learning Through Making

### Douglas's Learning Path (Validated)
1. **Start concrete**: Working starship script → immediate gratification
2. **Explore parameters**: Change values, see results → experimentation
3. **Read documentation**: Understand what each parameter does → comprehension
4. **Modify code**: Add new ship type or theme → application
5. **Create original**: Design own generator → mastery

### Key Pedagogical Insights
- **Fun first**: Starships > abstract cubes for engagement
- **Visual feedback**: Maya viewport = instant reward loop
- **Scaffolded complexity**: V1 simple → V2 advanced → natural progression
- **Documentation as learning**: README doubles as tutorial

---

## Cross-Domain Applications

### This Knowledge Transfers To:
- **Unity/Unreal Tool Development**: Same patterns, different API
- **Roguelike Item Generation**: Parametric weapons, armor, artifacts
- **Level Design Tools**: Room generators, terrain systems
- **Character Customization**: Modular character systems
- **VFX Pipelines**: Procedural particle system setup

### Related Game Design Domains
- Systems Design (interconnected mechanics)
- Economy Design (resource → crafting → items pipeline)
- AI Design (behavior trees, state machines)
- UX Design (tool usability, artist workflows)

---

## Synapses

### High-Strength Bidirectional Connections
- [DK-MAYA-PYTHON-SCRIPTING-v1.0.0.md](DK-MAYA-PYTHON-SCRIPTING-v1.0.0.md) (Critical, Implements, Bidirectional) - "Technical foundation for game asset creation"
- [alex-identity-integration.instructions.md](../.github/instructions/alex-identity-integration.instructions.md) (High, Embodies, Bidirectional) - "Alex Game Designer identity specialization"

### Medium-Strength Output Connections
- [bootstrap-learning.instructions.md](../.github/instructions/bootstrap-learning.instructions.md) (High, Applies, Forward) - "Teaching through making methodology"
- [DK-DOCUMENTATION-EXCELLENCE-v1.1.0.md](DK-DOCUMENTATION-EXCELLENCE-v1.1.0.md) (Medium, Guides, Forward) - "README as learning tool pattern"

### Contextual Activation Connections
- [worldview-integration.instructions.md](../.github/instructions/worldview-integration.instructions.md) (Medium, Informs, Forward) - "Ethical game design considerations"

**Primary Function**: Connect procedural content generation expertise with game design principles and Maya technical art workflows.

**Activation Triggers**:
- Game asset pipeline discussions
- Procedural generation requests
- Technical art tool development
- Teaching programming through visual/creative projects
- Maya-to-game-engine workflow questions

---

## Session Artifacts

### Files Created (2025-12-12)
- `scripts/starship.py` - V1 generator (586 lines)
- `scripts/starship_v2.py` - V2 advanced generator (967 lines)
- `scripts/fancy_3d_text_v2.py` - 3D text tool (480 lines)
- `README.md` - Complete documentation with parameter tables
- Launcher scripts for Maya execution

### Repository
- **GitHub**: fabioc-aloha/maya
- **Topics**: maya, python, autodesk, 3d-modeling, maya-python, scripting, automation, game-dev, vfx, tutorial

---

*Alex Game Designer - Where code meets creativity meets play* 🎮
