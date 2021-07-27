'''
Copyright (C) 2018 Samy Tichadou (tonton)
samytichadou@gmail.com

Created by Samy Tichadou (tonton)

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''
bl_info = {
    "name": "Marker List",
    "author": "Samy Tichadou (tonton), Adhi Hargo",
    "version": (1, 0),
    "blender": (2, 82, 0),
    "location": "Timeline",
    "description": "Utilities to help with Timeline Markers handling",
    "wiki_url": "https://github.com/samytichadou/Markerlist",
    "tracker_url": "https://github.com/samytichadou/Markerlist/issues/new",
    "category": "Animation"}

import bpy

# IMPORT SPECIFICS
##################################
from . import data, operators, ui

# register
##################################
classes = (operators.GoToMarker,
           operators.RemoveMarker,
           operators.RemoveSelectedMarker,
           operators.SelectAll,
           ui.MarkerList,
           data.Properties,
           )

def register():
    ### OPERATORS ###
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    ### MENU ###
    bpy.types.TIME_MT_marker.prepend(ui.marker_list_function)
    bpy.types.SEQUENCER_MT_marker.prepend(ui.marker_list_function)
    bpy.types.DOPESHEET_MT_marker.prepend(ui.marker_list_function)
    bpy.types.GRAPH_MT_marker.prepend(ui.marker_list_function)
    bpy.types.NLA_MT_marker.prepend(ui.marker_list_function)
    bpy.types.Scene.markerlist_props = bpy.props.PointerProperty(type=data.Properties)


def unregister():
    ### OPERATORS ###
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)

    ### MENU ###
    bpy.types.TIME_MT_marker.remove(ui.marker_list_function)
    bpy.types.SEQUENCER_MT_marker.remove(ui.marker_list_function)
    bpy.types.DOPESHEET_MT_marker.remove(ui.marker_list_function)
    bpy.types.GRAPH_MT_marker.remove(ui.marker_list_function)
    bpy.types.NLA_MT_marker.remove(ui.marker_list_function)
    del bpy.types.Scene.markerlist_props
