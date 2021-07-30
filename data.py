import re

import bpy

from . import ui

NAME_PATTERN_REGEX_STR = r"#(?P<digits>\d+)?(,(?P<start>\d+)?)?(?P<op>[nf])"
n_re = re.compile(NAME_PATTERN_REGEX_STR)


def upd_show_sidepanel(self, _):
    if self.show_sidepanel:
        ui.register_panels()
    else:
        ui.unregister_panels()


def upd_name_pattern(self, _):
    self.name_formatstr = self.pattern_to_formatstr(self.name_pattern)


def get_name_sample(self):
    return self.name_formatstr.format(**{"num": self.name_indexstart, "frm": 10}) or "<invalid>"


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
                                       name="Sort Field", default="frame", options={"SKIP_SAVE"})

    sort_reversed: bpy.props.BoolProperty(name="Sort Reversed", default=False, options={"SKIP_SAVE"})
    name_filter: bpy.props.StringProperty(name="Name Filter", default="",
                                          description="String to filter markers displayed by name.",
                                          options={"SKIP_SAVE", "TEXTEDIT_UPDATE"})
    name_pattern: bpy.props.StringProperty(name="Name Pattern", default="",
                                           options={"SKIP_SAVE", "TEXTEDIT_UPDATE"}, update=upd_name_pattern)
    name_sample: bpy.props.StringProperty(name="Name Sample", default="", options={"SKIP_SAVE"},
                                          get=get_name_sample)
    name_formatstr: bpy.props.StringProperty(name="Name Format String", default="", options={"HIDDEN", "SKIP_SAVE"})
    name_indexstart: bpy.props.IntProperty(name="Name Index Start", default=1, options={"HIDDEN", "SKIP_SAVE"})
    name_pattern_ok: bpy.props.BoolProperty(name="", default=False, options={"HIDDEN", "SKIP_SAVE"})

    def pattern_to_formatstr(self, pattern):
        formatstr = ""
        pos = 0
        matchobj = n_re.search(pattern, pos=pos)
        while matchobj is not None:
            formatstr += pattern[:matchobj.start()]

            matchdict = matchobj.groupdict()
            pat_digit = matchdict.get("digits")
            pat_start = matchdict.get("start")
            pat_op = matchdict["op"]
            field = "num"  # pat_op == "n"
            if pat_op == "f":
                field = "frm"
            formatstr += "{" + field + (":0{}".format(pat_digit) if pat_digit else ":03") + "}"
            if pat_start:
                self.name_indexstart = int(pat_start)

            pos = matchobj.end()
            matchobj = n_re.search(pattern, pos=pos)

        self.name_pattern_ok = formatstr != ""
        return formatstr
