import bpy

from bpy.types import PropertyGroup
from bpy.props import *


class prefs(PropertyGroup):
    alt_drawing: BoolProperty(
        default=False, description='备用绘制着色器。对Mac用户有用')
    individual_loops: BoolProperty(default=False)
    rotate_gizmo_use: BoolProperty(default=True)
    rotate_panel_use: BoolProperty(default=True)


def label_row(path, prop, row, label):
    row.label(text=label)
    row.prop(path, prop, text='')


def draw(preference, context, layout):
    label_row(preference.behavior, 'alt_drawing',
              layout.row(), '使用备用绘制')
    label_row(preference.behavior, 'rotate_gizmo_use',
              layout.row(), '使用旋转操作器')
    label_row(preference.behavior, 'rotate_panel_use',
              layout.row(), '使用旋转面板')
    label_row(preference.behavior, 'individual_loops',
              layout.row(), '编辑分离的单个循环')


def register():
    bpy.utils.register_class(prefs)
    return


def unregister():
    bpy.utils.unregister_class(prefs)
    return
