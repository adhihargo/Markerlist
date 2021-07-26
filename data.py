import bpy


class Properties(bpy.types.PropertyGroup):
    sort_field: bpy.props.EnumProperty(items=[("name", "Name", "", 0),
                                              ("frame", "Frame", "", 1)],
                                       name="Sort Field", default="frame")

    sort_reversed: bpy.props.BoolProperty(name="Sort Reversed", default=False)
