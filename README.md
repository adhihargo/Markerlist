# Marker List

**Marker List** is a Blender addon designed to allow user to quickly interact with all markers in the scene. It is presented as menu item accessible from the **Marker** menu in the Timeline, VSE, Dopesheet, NLA Editor and Graph Editor areas. Optionally, it's also accessible in the same areas' sidepanel (configurable in this addon's user preferences).

1. (De)select All Markers. If `CTRL` key is pressed, it inverts selection state of all markers instead.

1. Rename Selected Marker. Currently, only two patterns are recognized: 
   
   - `#[DIGITS][,[START]]n`: Numbering incrementally added, starting from `START` (default: 1). `DIGITS` specify the number of digits (default: 3). 
     
     Example: `SHOT_#4,2n` will rename markers into `SHOT_0002`, `SHOT_0003`, etc.
     
   - `#[DIGITS]f`: Frame number where marker is located.
