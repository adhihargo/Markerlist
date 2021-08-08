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
    bl_idname = "marker.ml_add"
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
    """Change selection of all time markers. Inverts selection instead, if CTRL key is pressed."""
    bl_idname = "marker.ml_select_all"
    bl_label = "(De)select all Markers"
    bl_options = {'INTERNAL', 'UNDO'}

    action: bpy.props.EnumProperty(items=[("TOGGLE", "Toggle", "", 0),
                                          ("INVERT", "Invert", "", 1)])

    @classmethod
    def poll(cls, context):
        return context.scene.timeline_markers

    def invoke(self, context, event):
        if event.ctrl:
            self.action = "INVERT"
        return self.execute(context)

    def execute(self, context):
        scn = context.scene
        if self.action == "TOGGLE":
            value = not scn.timeline_markers[0].select
            for marker in scn.timeline_markers:
                marker.select = value
        elif self.action == "INVERT":
            for marker in scn.timeline_markers:
                marker.select = not marker.select
        return {'FINISHED'}


class CameraBind(bpy.types.Operator):
    """"""
    bl_idname = "marker.ml_camera_bind"
    bl_label = "Bind Camera to Markers"
    bl_options = {'INTERNAL', 'UNDO'}

    @classmethod
    def poll(cls, context):
        obj = context.object
        return obj and obj.type == "CAMERA"

    def execute(self, context):
        camera = context.object
        scn = context.scene
        frame_current = scn.frame_current
        marker_list = [m for m in scn.timeline_markers if m.frame == frame_current]
        if not marker_list:
            m = scn.timeline_markers.new(name="F_{}".format(frame_current), frame=frame_current)
            marker_list = [m]

        for marker in marker_list:
            marker.camera = camera
        return {'FINISHED'}
