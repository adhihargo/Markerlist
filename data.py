import bpy

from . import ui


def upd_show_sidepanel(self, _):
    if self.show_sidepanel:
        ui.register_panels()
    else:
        ui.unregister_panels()


def get_prefs(context: bpy.types.Context) -> bpy.types.AddonPreferences:
    return context.preferences.addons[__package__].preferences


class Preferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    show_sidepanel: bpy.props.BoolProperty(name="Show in Sidepanel", update=upd_show_sidepanel)

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.prop(self, "show_sidepanel")


class Properties(bpy.types.PropertyGroup):
    sort_field: bpy.props.EnumProperty(items=[("name", "Name", "", 0),
                                              ("frame", "Frame", "", 1)],
                                       name="Sort Field", default="frame")

    sort_reversed: bpy.props.BoolProperty(name="Sort Reversed", default=False)
