import bpy

from . import data


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


class AddMarker(bpy.types.Operator):
    """Add Timeline Marker at current frame"""
    bl_idname = "marker.add_global"
    bl_label = "Add Marker"
    bl_options = {'INTERNAL', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        scn = context.scene
        current_frame = scn.frame_current
        scn.timeline_markers.new(name="F_{}".format(current_frame), frame=current_frame)
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


class RenameSelectedMarker(bpy.types.Operator):
    """Rename selected Timeline Markers"""
    bl_idname = "marker.rename_selected"
    bl_label = "Rename Selected Marker"
    bl_options = {'INTERNAL', 'UNDO'}

    @classmethod
    def poll(cls, context):
        props: data.Properties = context.scene.markerlist_props
        return props.name_pattern_ok

    def execute(self, context):
        scn = context.scene
        marker_list = scn.timeline_markers
        props: data.Properties = context.scene.markerlist_props

        index = props.name_indexstart
        sort_key = (lambda it: it.frame) if props.sort_field == "frame" else (lambda it: it.name)
        for marker in sorted(marker_list.values(), key=sort_key, reverse=props.sort_reversed):
            if not marker.select:
                continue

            new_name = props.name_formatstr.format(**{"num": index, "frm": marker.frame})
            marker.name = new_name
            index += 1

        return {'FINISHED'}


class SelectAll(bpy.types.Operator):
    """Change selection of time markers, active on all areas"""
    bl_idname = "marker.select_all_global"
    bl_label = "(De)select all Markers"
    bl_options = {'INTERNAL', 'UNDO'}

    action: bpy.props.EnumProperty(items=[("TOGGLE", "Toggle", "", 0), ])

    @classmethod
    def poll(cls, context):
        return context.scene.timeline_markers

    def execute(self, context):
        scn = context.scene
        if self.action == "TOGGLE":
            value = not scn.timeline_markers[0].select
            for marker in scn.timeline_markers:
                marker.select = value
        return {'FINISHED'}
