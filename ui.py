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

    col = layout.column(align=True)
    if scn.tool_settings.lock_markers:
        col.enabled = False
    else:
        col.enabled = True

    sort_key = (lambda it: it[1].frame) if props.sort_field == "frame" else (lambda it: it[1].name)
    row = col.row(align=True)
    row.scale_x = 40
    row.label(text=" ")
    row.scale_x = 1
    o = row.operator("marker.select_all_global", icon="RESTRICT_SELECT_OFF", text="")
    o.action = "TOGGLE"
    for k, marker in sorted(marker_list.items(), key=sort_key, reverse=props.sort_reversed):
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

    row = layout.row(align=True)
    row.prop(scn, 'frame_current', text='Frame')
    row.separator()
    op = row.operator('screen.marker_jump', text='', icon='TRIA_LEFT')
    op.next = False
    op = row.operator('screen.marker_jump', text='', icon='TRIA_RIGHT')
    op.next = True
    row.separator()
    if tool_settings.lock_markers:
        icon = 'LOCKED'
    else:
        icon = 'UNLOCKED'
    row.prop(tool_settings, 'lock_markers', text='', icon=icon)
    row.separator()
    row.operator('marker.remove_selected', text='Selected', icon='X')


def marker_list_function(self, context):
    self.layout.operator('marker.list')
