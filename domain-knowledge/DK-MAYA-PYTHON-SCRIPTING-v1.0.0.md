# DK-MAYA-PYTHON-SCRIPTING-v1.0.0.md
**Domain**: Autodesk Maya Python Scripting and Automation
**Version**: 1.0.0 UNNILNILIUM
**Creation Date**: December 12, 2025
**Learning Method**: Conversational assistance for Maya scripting and tool development
**Research Foundation**: Autodesk Documentation, PyMEL, OpenMaya API, Industry Best Practices
**Expertise Level**: Foundation → Production Pipeline Mastery

---

## 📚 Research Foundation

### **Official Documentation & API References**
- **Maya Python API**: Autodesk Maya Developer Documentation
- **PyMEL Documentation**: PyMEL 1.0+ Object-Oriented Python for Maya
- **OpenMaya API 1.0**: Traditional Maya Python API (maya.OpenMaya)
- **OpenMaya API 2.0**: Modern Maya Python API (maya.api.OpenMaya)
- **MEL Reference**: Maya Embedded Language Command Reference
- **Maya DevKit**: Official Autodesk SDK samples and examples

### **Industry Resources**
- **Chad Vernon's Maya API Programming**: Comprehensive API tutorials and production examples
- **CGCircuit Tutorials**: Professional Maya scripting courses
- **Tech-Artists.org**: Pipeline development best practices
- **Python Inside Maya**: Google Groups community knowledge base

---

## 🎯 Core Scripting Approaches

### **1. maya.cmds - Command Module (Beginner-Friendly)**

The `maya.cmds` module provides direct Python access to MEL commands. It's the most straightforward way to script Maya.

```python
import maya.cmds as cmds

# Create objects
sphere = cmds.polySphere(name="mySphere", radius=2)[0]
cube = cmds.polyCube(name="myCube", width=1, height=2, depth=1)[0]

# Transform objects
cmds.move(5, 0, 0, sphere)
cmds.rotate(0, 45, 0, cube)
cmds.scale(2, 2, 2, sphere)

# Query and set attributes
tx = cmds.getAttr(f"{sphere}.translateX")
cmds.setAttr(f"{sphere}.translateY", 3.0)

# Select objects
cmds.select(sphere, cube)

# List objects
all_meshes = cmds.ls(type='mesh')
selected = cmds.ls(selection=True)
```

**Best Practices for maya.cmds**:
- Use short flag names for concise code (`r=` vs `radius=`)
- Always check return values (commands often return lists)
- Use `cmds.ls()` with specific types for targeted queries
- Handle undo with `cmds.undoInfo()` for tool development

### **2. PyMEL - Object-Oriented Approach (Recommended)**

PyMEL wraps `maya.cmds` with a Pythonic, object-oriented interface. Objects returned are PyNodes with methods attached.

```python
from pymel.core import *

# Create and work with objects
sphere = polySphere(name="mySphere", radius=2)[0]
cube = polyCube(name="myCube")[0]

# Object-oriented access
sphere.translateX.set(5.0)
sphere.translateY.get()
sphere.getShape()  # Returns the shape node

# Connections
sphere.translateX.connect(cube.translateX)

# Chained operations (highly readable)
camera = ls(type='camera')[0]
focal_length = camera.getFocalLength()

# Parent/child navigation
parent = sphere.getParent()
children = parent.getChildren()

# Attribute access
sphere.translateX.isLocked()
sphere.translateX.setKeyable(True)
```

**Why PyMEL?**
- Object-oriented: `node.method()` instead of `command(node)`
- Type-safe: Returns proper PyNode objects, not strings
- Pythonic: Follows Python conventions and best practices
- Readable: Chaining operations reads left-to-right naturally

**Warning**: Don't mix `maya.cmds` and `pymel.core` in the same script - use one or the other.

### **3. OpenMaya API 1.0 - Low-Level Performance**

The OpenMaya API provides direct access to Maya's internal libraries for maximum performance.

```python
import maya.OpenMaya as om
import maya.OpenMayaMPx as ompx

# Get selection
selection = om.MSelectionList()
om.MGlobal.getActiveSelectionList(selection)

# Iterate through selection
iter = om.MItSelectionList(selection)
while not iter.isDone():
    dag_path = om.MDagPath()
    iter.getDagPath(dag_path)
    print(dag_path.fullPathName())
    iter.next()

# Work with meshes
mesh_fn = om.MFnMesh(dag_path)
points = om.MPointArray()
mesh_fn.getPoints(points, om.MSpace.kWorld)

# Vectors and math
vec1 = om.MVector(1, 0, 0)
vec2 = om.MVector(0, 1, 0)
cross = vec1 ^ vec2  # Cross product
dot = vec1 * vec2    # Dot product
```

**Key OpenMaya Concepts**:
- **MObject**: Generic handle to any Maya object (nodes, attributes)
- **MFn* (Function Sets)**: Classes to operate on MObjects (MFnMesh, MFnTransform, MFnDagNode)
- **MIt* (Iterators)**: Classes to traverse data (MItMeshVertex, MItDependencyGraph)
- **MPx* (Proxies)**: Base classes for custom plugins (MPxCommand, MPxNode, MPxDeformerNode)

### **4. OpenMaya API 2.0 - Modern Python API (Maya 2016+)**

API 2.0 is more Pythonic, eliminates MScriptUtil, and provides better performance.

```python
import maya.api.OpenMaya as om2

# Get selection (cleaner than API 1.0)
selection = om2.MGlobal.getActiveSelectionList()

# Iterate selection
for i in range(selection.length()):
    dag_path = selection.getDagPath(i)
    print(dag_path.fullPathName())

# Mesh operations
mesh_fn = om2.MFnMesh(dag_path)
points = mesh_fn.getPoints(om2.MSpace.kWorld)

# Direct Python list returns (no MPointArray needed)
for point in points:
    print(point.x, point.y, point.z)
```

**API 2.0 Advantages**:
- No MScriptUtil needed for pointers/references
- Returns Python-native types where possible
- Better memory management
- Improved performance over API 1.0

---

## 🛠️ Common Scripting Tasks

### **Scene Management**

```python
import maya.cmds as cmds

# New scene
cmds.file(new=True, force=True)

# Open/Save scenes
cmds.file("path/to/file.ma", open=True, force=True)
cmds.file(rename="new_scene.ma")
cmds.file(save=True, type="mayaAscii")

# Import/Export
cmds.file("path/to/import.fbx", i=True)  # Import
cmds.file("path/to/export.fbx", exportSelected=True, type="FBX export")

# References
cmds.file("path/to/ref.ma", reference=True, namespace="char")
refs = cmds.file(query=True, reference=True)
```

### **Object Creation & Manipulation**

```python
import maya.cmds as cmds

# Create primitives
sphere = cmds.polySphere(r=1, sx=20, sy=20, name="mySphere")[0]
cube = cmds.polyCube(w=2, h=2, d=2, name="myCube")[0]
plane = cmds.polyPlane(w=10, h=10, sx=10, sy=10)[0]
curve = cmds.curve(d=3, p=[(0,0,0), (1,1,0), (2,0,0), (3,1,0)])

# Grouping and parenting
group = cmds.group(sphere, cube, name="myGroup")
cmds.parent(plane, group)

# Duplicating
dupe = cmds.duplicate(sphere, name="sphereCopy")[0]
instance = cmds.instance(cube, name="cubeInstance")[0]

# Freeze transformations
cmds.makeIdentity(sphere, apply=True, t=1, r=1, s=1)

# Delete history
cmds.delete(sphere, constructionHistory=True)
```

### **Attribute Operations**

```python
import maya.cmds as cmds

node = "pSphere1"

# Get/Set attributes
tx = cmds.getAttr(f"{node}.translateX")
cmds.setAttr(f"{node}.translateY", 5.0)

# Add custom attributes
cmds.addAttr(node, longName="customFloat", attributeType="float", defaultValue=0.0)
cmds.addAttr(node, longName="customEnum", attributeType="enum", enumName="A:B:C:")
cmds.addAttr(node, longName="customString", dataType="string")
cmds.setAttr(f"{node}.customString", "Hello", type="string")

# Lock/Unlock attributes
cmds.setAttr(f"{node}.translateX", lock=True)
cmds.setAttr(f"{node}.translateX", lock=False)

# Connect attributes
cmds.connectAttr(f"{node}.translateX", "pCube1.translateX")
cmds.disconnectAttr(f"{node}.translateX", "pCube1.translateX")

# List connections
inputs = cmds.listConnections(node, source=True, destination=False)
outputs = cmds.listConnections(node, source=False, destination=True)
```

### **Animation**

```python
import maya.cmds as cmds

node = "pSphere1"

# Set keyframes
cmds.setKeyframe(node, attribute="translateX", time=1, value=0)
cmds.setKeyframe(node, attribute="translateX", time=24, value=10)

# Query keyframes
keys = cmds.keyframe(f"{node}.translateX", query=True, timeChange=True)

# Set tangent types
cmds.keyTangent(f"{node}.translateX", inTangentType="spline", outTangentType="spline")

# Bake animation
cmds.bakeResults(node, time=(1, 100), simulation=True)

# Animation curves
anim_curves = cmds.listConnections(node, type="animCurve")
```

### **Rigging Utilities**

```python
import maya.cmds as cmds

# Create joints
cmds.select(clear=True)
root = cmds.joint(name="root_jnt", p=(0, 0, 0))
mid = cmds.joint(name="mid_jnt", p=(0, 5, 0))
end = cmds.joint(name="end_jnt", p=(0, 10, 0))

# Orient joints
cmds.joint(root, edit=True, orientJoint="xyz", secondaryAxisOrient="yup")

# Create IK
ik_handle = cmds.ikHandle(startJoint=root, endEffector=end, solver="ikRPsolver")[0]

# Create control curves
ctrl = cmds.circle(name="main_ctrl", normal=(0, 1, 0), radius=2)[0]

# Parent constraint
cmds.parentConstraint(ctrl, root, maintainOffset=True)

# Point and orient constraints
cmds.pointConstraint("locator1", "joint1")
cmds.orientConstraint("locator1", "joint1")

# Skin cluster
skin = cmds.skinCluster(root, mid, end, "pCylinder1", toSelectedBones=True)[0]
```

### **UI Development**

```python
import maya.cmds as cmds

def create_simple_ui():
    """Create a simple tool window."""

    window_name = "myToolWindow"

    # Delete existing window
    if cmds.window(window_name, exists=True):
        cmds.deleteUI(window_name)

    # Create window
    window = cmds.window(window_name, title="My Tool", widthHeight=(300, 200))

    # Layout
    cmds.columnLayout(adjustableColumn=True, rowSpacing=5)

    # UI elements
    cmds.text(label="My Custom Tool")
    cmds.separator(height=10)

    name_field = cmds.textFieldGrp(label="Name:", text="default")
    radius_slider = cmds.floatSliderGrp(label="Radius:", field=True,
                                         minValue=0.1, maxValue=10, value=1)

    cmds.separator(height=10)

    def on_create(*args):
        name = cmds.textFieldGrp(name_field, query=True, text=True)
        radius = cmds.floatSliderGrp(radius_slider, query=True, value=True)
        cmds.polySphere(name=name, radius=radius)

    cmds.button(label="Create Sphere", command=on_create)
    cmds.button(label="Close", command=lambda x: cmds.deleteUI(window))

    cmds.showWindow(window)

# Run the UI
create_simple_ui()
```

---

## 🔌 Plugin Development

### **Custom Command Plugin**

```python
"""
HelloWorld Command Plugin
Save as helloWorldCmd.py in Maya's plug-ins folder
"""
import maya.api.OpenMaya as om

def maya_useNewAPI():
    """Tell Maya this plugin uses API 2.0"""
    pass

class HelloWorldCmd(om.MPxCommand):
    kPluginCmdName = "helloWorld"

    def __init__(self):
        om.MPxCommand.__init__(self)

    @staticmethod
    def creator():
        return HelloWorldCmd()

    def doIt(self, args):
        print("Hello World from Python!")

def initializePlugin(plugin):
    pluginFn = om.MFnPlugin(plugin, "Author", "1.0")
    try:
        pluginFn.registerCommand(
            HelloWorldCmd.kPluginCmdName,
            HelloWorldCmd.creator
        )
    except:
        om.MGlobal.displayError(f"Failed to register command: {HelloWorldCmd.kPluginCmdName}")

def uninitializePlugin(plugin):
    pluginFn = om.MFnPlugin(plugin)
    try:
        pluginFn.deregisterCommand(HelloWorldCmd.kPluginCmdName)
    except:
        om.MGlobal.displayError(f"Failed to deregister command: {HelloWorldCmd.kPluginCmdName}")
```

### **Custom Dependency Node**

```python
"""
Doubler Node Plugin - doubles input value
Save as doublerNode.py
"""
import maya.api.OpenMaya as om

def maya_useNewAPI():
    pass

class DoublerNode(om.MPxNode):
    kPluginNodeId = om.MTypeId(0x00127000)  # Get unique ID from Autodesk
    kPluginNodeName = "doublerNode"

    # Attributes
    aInput = None
    aOutput = None

    def __init__(self):
        om.MPxNode.__init__(self)

    @staticmethod
    def creator():
        return DoublerNode()

    @staticmethod
    def initialize():
        nAttr = om.MFnNumericAttribute()

        # Create output attribute first
        DoublerNode.aOutput = nAttr.create("output", "out", om.MFnNumericData.kFloat, 0.0)
        nAttr.writable = False
        nAttr.storable = False

        # Create input attribute
        DoublerNode.aInput = nAttr.create("input", "in", om.MFnNumericData.kFloat, 0.0)
        nAttr.keyable = True

        # Add attributes
        DoublerNode.addAttribute(DoublerNode.aInput)
        DoublerNode.addAttribute(DoublerNode.aOutput)

        # Set attribute dependencies
        DoublerNode.attributeAffects(DoublerNode.aInput, DoublerNode.aOutput)

    def compute(self, plug, data):
        if plug == DoublerNode.aOutput:
            # Get input
            inputValue = data.inputValue(DoublerNode.aInput).asFloat()

            # Compute
            outputValue = inputValue * 2.0

            # Set output
            outputHandle = data.outputValue(DoublerNode.aOutput)
            outputHandle.setFloat(outputValue)
            data.setClean(plug)

        return None

def initializePlugin(plugin):
    pluginFn = om.MFnPlugin(plugin, "Author", "1.0")
    try:
        pluginFn.registerNode(
            DoublerNode.kPluginNodeName,
            DoublerNode.kPluginNodeId,
            DoublerNode.creator,
            DoublerNode.initialize
        )
    except:
        om.MGlobal.displayError(f"Failed to register node: {DoublerNode.kPluginNodeName}")

def uninitializePlugin(plugin):
    pluginFn = om.MFnPlugin(plugin)
    try:
        pluginFn.deregisterNode(DoublerNode.kPluginNodeId)
    except:
        om.MGlobal.displayError(f"Failed to deregister node: {DoublerNode.kPluginNodeName}")
```

---

## ⚡ Performance Best Practices

### **General Optimization**

```python
import maya.cmds as cmds

# 1. Disable undo for batch operations
cmds.undoInfo(stateWithoutFlush=False)
try:
    # Batch operations here
    for i in range(100):
        cmds.polySphere()
finally:
    cmds.undoInfo(stateWithoutFlush=True)

# 2. Suspend viewport refresh
cmds.refresh(suspend=True)
try:
    # Heavy operations
    pass
finally:
    cmds.refresh(suspend=False)

# 3. Use API for heavy computation
# maya.cmds = ~1x speed
# PyMEL = ~0.8x speed (slightly slower than cmds)
# OpenMaya API 1.0 = ~5-10x speed
# OpenMaya API 2.0 = ~10-20x speed

# 4. Batch attribute setting
cmds.setAttr("node.tx", 1, "node.ty", 2, "node.tz", 3)  # Single call

# 5. Use ls() wisely - be specific
meshes = cmds.ls(type='mesh')  # Fast
everything = cmds.ls()  # Slow on large scenes
```

### **Memory Management**

```python
# Clear selection to prevent memory bloat
cmds.select(clear=True)

# Delete unused nodes
cmds.delete(cmds.ls(type='unknown'))

# Optimize scene size
cmds.optimizeScene()

# Remove unused plugins
unknown_plugins = cmds.unknownPlugin(query=True, list=True) or []
for plugin in unknown_plugins:
    cmds.unknownPlugin(plugin, remove=True)
```

---

## 🏗️ Project Structure Best Practices

### **Recommended Tool Structure**

```
my_maya_tools/
├── __init__.py
├── core/
│   ├── __init__.py
│   ├── utils.py          # Utility functions
│   ├── constants.py      # Constants and configuration
│   └── decorators.py     # Common decorators
├── tools/
│   ├── __init__.py
│   ├── modeling/
│   │   └── cleanup.py
│   ├── rigging/
│   │   └── auto_rig.py
│   └── animation/
│       └── bake_tools.py
├── ui/
│   ├── __init__.py
│   └── main_window.py
├── plugins/
│   └── custom_node.py
└── tests/
    └── test_utils.py
```

### **userSetup.py Configuration**

```python
# Place in: ~/maya/<version>/scripts/userSetup.py
import sys
import maya.cmds as cmds
import maya.utils

# Add custom script paths
CUSTOM_PATHS = [
    "C:/Users/username/maya_tools",
    "//server/pipeline/maya/scripts",
]

for path in CUSTOM_PATHS:
    if path not in sys.path:
        sys.path.insert(0, path)

def setup_environment():
    """Run after Maya fully loads."""
    print("Custom environment loaded!")
    # Import custom menus, shelves, etc.

# Defer execution until Maya is ready
maya.utils.executeDeferred(setup_environment)
```

---

## 🐛 Debugging & Error Handling

### **Logging Setup**

```python
import logging
import maya.cmds as cmds

# Create logger
logger = logging.getLogger("MyTool")
logger.setLevel(logging.DEBUG)

# Create handler that outputs to Maya's Script Editor
class MayaHandler(logging.Handler):
    def emit(self, record):
        msg = self.format(record)
        if record.levelno >= logging.ERROR:
            cmds.error(msg)
        elif record.levelno >= logging.WARNING:
            cmds.warning(msg)
        else:
            print(msg)

handler = MayaHandler()
handler.setFormatter(logging.Formatter('%(name)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)

# Usage
logger.info("Starting operation...")
logger.warning("This might be slow")
logger.error("Something went wrong!")
```

### **Exception Handling**

```python
import maya.cmds as cmds
import traceback

def safe_operation():
    """Example of proper exception handling."""
    try:
        # Your code here
        result = cmds.polySphere(name="test")[0]
        return result
    except RuntimeError as e:
        cmds.warning(f"Maya error: {e}")
        return None
    except Exception as e:
        cmds.error(f"Unexpected error: {e}")
        traceback.print_exc()
        return None
    finally:
        # Cleanup code that always runs
        cmds.select(clear=True)
```

---

## 📖 Quick Reference Card

### **Common Commands Cheat Sheet**

| Task | maya.cmds | PyMEL |
|------|-----------|-------|
| List selected | `cmds.ls(sl=True)` | `ls(sl=True)` or `selected()` |
| Create sphere | `cmds.polySphere()` | `polySphere()` |
| Get attribute | `cmds.getAttr('node.attr')` | `node.attr.get()` |
| Set attribute | `cmds.setAttr('node.attr', val)` | `node.attr.set(val)` |
| Connect attrs | `cmds.connectAttr('a.out', 'b.in')` | `a.out.connect(b.in)` |
| Get parent | `cmds.listRelatives(p=True)` | `node.getParent()` |
| Get shape | `cmds.listRelatives(s=True)` | `node.getShape()` |

### **API Object Types**

| Prefix | Purpose | Example |
|--------|---------|---------|
| M | Wrapper/Math | MVector, MMatrix, MPoint |
| MFn | Function Set | MFnMesh, MFnTransform |
| MIt | Iterator | MItMeshVertex, MItDag |
| MPx | Proxy (Plugin Base) | MPxCommand, MPxNode |

---

## Synapses

### High-Strength Learning Connections
- [bootstrap-learning.instructions.md] (High, Enables, Forward) - "Maya scripting domain knowledge acquisition"
- [DK-HUMAN-LEARNING-PSYCHOLOGY-v1.0.0.md] (Medium, Informs, Forward) - "Conversational teaching approach for Maya concepts"
- [DK-GAME-DESIGN-MAYA-INTEGRATION-v1.0.0.md](DK-GAME-DESIGN-MAYA-INTEGRATION-v1.0.0.md) (High, Enables, Bidirectional) - "Procedural content generation for games"

### Technical Integration Points
- [alex-core.instructions.md] (Medium, Integrates, Forward) - "Core cognitive support for Maya assistance tasks"
- [worldview-integration.instructions.md] (Medium, Guides, Forward) - "Ethical considerations in tool development guidance"

### Cross-Domain Potential
- [DK-DOCUMENTATION-EXCELLENCE-v1.1.0.md] (Medium, Applies, Forward) - "Documentation standards for Maya tool development"

**Primary Function**: Provide comprehensive Maya Python scripting knowledge for conversational assistance in tool development, automation, and pipeline integration.

**Activation Triggers**:
- User requests Maya scripting help
- Tool development discussions
- Pipeline automation requirements
- Plugin development questions
- Animation/Rigging automation needs

---

## 🎓 Learning Pathways

### **Beginner Path**
1. Start with `maya.cmds` basics
2. Learn object creation and manipulation
3. Practice attribute operations
4. Build simple UI tools

### **Intermediate Path**
1. Transition to PyMEL for cleaner code
2. Develop reusable utility modules
3. Create production-ready tools with UI
4. Learn animation and rigging automation

### **Advanced Path**
1. Master OpenMaya API 2.0
2. Develop custom nodes and deformers
3. Build pipeline integration tools
4. Optimize for performance-critical applications

---

*Domain knowledge supporting Maya Python scripting assistance and tool development guidance.*
