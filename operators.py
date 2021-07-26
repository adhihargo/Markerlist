import bpy


class GoToMarker(bpy.types.Operator):
    """Go to specific Timeline Marker frame"""
    bl_idname = "marker.go_to"
    bl_label = "Go to Marker"
    bl_options = {'INTERNAL', 'UNDO'}

    frame: bpy.props.IntProperty()

    @classmethod
    def poll(cls, context):
        return context.scene.timeline_markers

    def execute(self, context):
        context.scene.frame_current = self.frame
        return {'FINISHED'}


class RemoveMarker(bpy.types.Operator):
    """Remove specific Timeline Marker"""
    bl_idname = "marker.remove"
    bl_label = "Remove Marker"
    bl_options = {'INTERNAL', 'UNDO'}

    frame: bpy.props.IntProperty()

    @classmethod
    def poll(cls, context):
        return context.scene.timeline_markers

    def execute(self, context):
        scn = context.scene
        for marker in scn.timeline_markers:
            if marker.frame == self.frame:
                scn.timeline_markers.remove(marker)
                break
        return {'FINISHED'}


class RemoveSelectedMarker(bpy.types.Operator):
    """Remove selected Timeline Markers"""
    bl_idname = "marker.remove_selected"
    bl_label = "Remove Selected Marker"
    bl_options = {'INTERNAL', 'UNDO'}

    @classmethod
    def poll(cls, context):
        for marker in context.scene.timeline_markers:
            if marker.select:
                return True

    def execute(self, context):
        scn = context.scene
        for marker in scn.timeline_markers:
            if marker.select:
                scn.timeline_markers.remove(marker)
        return {'FINISHED'}
