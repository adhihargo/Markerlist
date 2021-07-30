import bpy

from . import data


class MarkerList(bpy.types.Operator):
    """Timeline Markers list"""
    bl_idname = "marker.list"
    bl_label = "Marker List"

    @classmethod
    def poll(cls, context):
        return True

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=500)

    def draw(self, context):
        layout = self.layout
        draw_panel(layout, context)

    def execute(self, context):
        return {'FINISHED'}


class VIEW3D_PT_MarkerList(bpy.types.Panel):
    """Creates a Panel in the 3D View area"""
    bl_label = "Marker List"
    bl_category = "Marker List"
    bl_idname = "VIEW3D_PT_MarkerList"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    def draw(self, context):
        layout = self.layout
        draw_panel(layout, context)


class SEQUENCER_PT_MarkerList(bpy.types.Panel):
    """Creates a Panel in the Video Sequencer area"""
    bl_label = "Marker List"
    bl_category = "Marker List"
    bl_idname = "SEQUENCER_PT_MarkerList"
    bl_space_type = 'SEQUENCE_EDITOR'
    bl_region_type = 'UI'

    def draw(self, context):
        layout = self.layout
        draw_panel(layout, context)


class DOPESHEET_PT_MarkerList(bpy.types.Panel):
    """Creates a Panel in the Dopesheet area"""
    bl_label = "Marker List"
    bl_category = "Marker List"
    bl_idname = "DOPESHEET_PT_MarkerList"
    bl_space_type = 'DOPESHEET_EDITOR'
    bl_region_type = 'UI'

    def draw(self, context):
        layout = self.layout
        draw_panel(layout, context)


class GRAPH_PT_MarkerList(bpy.types.Panel):
    """Creates a Panel in the Graph Editor area"""
    bl_label = "Marker List"
    bl_category = "Marker List"
    bl_idname = "GRAPH_PT_MarkerList"
    bl_space_type = 'GRAPH_EDITOR'
    bl_region_type = 'UI'

    def draw(self, context):
        layout = self.layout
        draw_panel(layout, context)


class NLA_PT_MarkerList(bpy.types.Panel):
    """Creates a Panel in the NLA Editor area"""
    bl_label = "Marker List"
    bl_category = "Marker List"
    bl_idname = "NLA_PT_MarkerList"
    bl_space_type = 'NLA_EDITOR'
    bl_region_type = 'UI'

    def draw(self, context):
        layout = self.layout
        draw_panel(layout, context)


def draw_panel(layout, context):
    scn = context.scene
    tool_settings = scn.tool_settings
    marker_list = scn.timeline_markers
    props: data.Properties = scn.markerlist_props

    row = layout.row(align=True)
    row.scale_x = 2
    row.label(text="Sort Field:")
    row.scale_x = 1
    row.prop(props, "sort_field", expand=True)
    row.prop(props, "sort_reversed", icon_only=True, icon="SORT_DESC")
    row.separator()
    o = row.operator("marker.ml_select_all", icon="RESTRICT_SELECT_OFF", text="")
    o.action = "TOGGLE"

    col = layout.column(align=True)
    col.enabled = not tool_settings.lock_markers

    sort_key = (lambda it: it.frame) if props.sort_field == "frame" else (lambda it: it.name)
    for marker in sorted(marker_list.values(), key=sort_key, reverse=props.sort_reversed):
        row = col.row(align=True)
        # go to frame
        if scn.frame_current == marker.frame:
            icon = 'RADIOBUT_ON'
        else:
            icon = 'RADIOBUT_OFF'
        op = row.operator('marker.go_to', text='', icon=icon, emboss=False)
        op.frame = marker.frame
        # name
        row.scale_x = 4
        row.prop(marker, "name", text="")
        row.scale_x = 1
        # selection
        if marker.select:
            icon = 'RESTRICT_SELECT_OFF'
        else:
            icon = 'RESTRICT_SELECT_ON'
        row.prop(marker, "select", text="", icon=icon)
        # frame
        row.prop(marker, "frame", text="")

        # delete
        op = row.operator('marker.remove', text='', icon='X')
        op.frame = marker.frame
        # camera
        if marker.camera:
            icon = 'VIEW_CAMERA'
        else:
            icon = 'CAMERA_DATA'
        row.label(text="", icon=icon)

    first_column_scale = 0.3
    grid = layout.grid_flow(columns=2, row_major=True)
    grid.scale_x = first_column_scale
    grid.operator("marker.ml_add", text="Add")
    grid.scale_x = 1
    sub_row = grid.row(align=True)
    sub_row.prop(scn, 'frame_current', text='Frame')
    sub_row.separator()
    op = sub_row.operator('screen.marker_jump', text='', icon='TRIA_LEFT')
    op.next = False
    op = sub_row.operator('screen.marker_jump', text='', icon='TRIA_RIGHT')
    op.next = True
    sub_row.separator()
    if tool_settings.lock_markers:
        icon = 'LOCKED'
    else:
        icon = 'UNLOCKED'
    sub_row.prop(tool_settings, 'lock_markers', text='', icon=icon)
    sub_row.separator()
    sub_row.operator('marker.remove_selected', text='Remove', icon='X')

    grid.scale_x = first_column_scale
    grid.operator("marker.rename_selected", text="Rename")
    grid.scale_x = 1
    sub_row = grid.row(align=True)
    sub_row.prop(props, "name_pattern", text="")
    sub_row.prop(props, "name_sample", text="")

    grid.scale_x = first_column_scale
    grid.label(text="")
    grid.scale_x = 1
    grid.operator("marker.ml_camera_bind")


def marker_list_function(self, context):
    self.layout.operator('marker.list')


panel_classes = (
    VIEW3D_PT_MarkerList,
    SEQUENCER_PT_MarkerList,
    DOPESHEET_PT_MarkerList,
    GRAPH_PT_MarkerList,
    NLA_PT_MarkerList,
)


def register_panels():
    from bpy.utils import register_class
    for cls in panel_classes:
        register_class(cls)


def unregister_panels():
    from bpy.utils import unregister_class
    for cls in reversed(panel_classes):
        unregister_class(cls)
