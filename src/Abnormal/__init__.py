import bpy
from . import operators_modal
from . import operators
from . import properties
from . import ui
from . import keymap
from . import classes
from . import functions_modal
from . import functions_tools
from . import translations
from bpy.props import *

bl_info = {
    "name": "Abnormal",
    "author": "Cody Winchester (CodyWinch), Tyler Walker (BeyondDev)",
    "version": (1, 1, 6),
    "blender": (4, 5, 0),
    "location": "3D View > N Panel/Header > BNPR Abnormal Tab",
    "description": "BNPR Normal Editing Tools",
    "warning": "",
    "wiki_url": "",
    "category": "3D View"
}

if "bpy" in locals():
    import importlib
    if "__init__" in locals():
        importlib.reload(__init__)
    if "ui" in locals():
        importlib.reload(ui)
    if "keymap" in locals():
        importlib.reload(keymap)
    if "properties" in locals():
        importlib.reload(properties)
    if "classes" in locals():
        importlib.reload(classes)
    if "functions_modal" in locals():
        importlib.reload(functions_modal)
    if "functions_tools" in locals():
        importlib.reload(functions_tools)
    if "operators_modal" in locals():
        importlib.reload(operators_modal)
    if "operators" in locals():
        importlib.reload(operators)


def register():
    # 注册翻译
    try:
        bpy.app.translations.register(__name__, translations.translation_dict)
        print("[Abnormal] 翻译系统注册成功")
        print(f"[Abnormal] 当前 Blender 语言: {bpy.app.translations.locale}")
        print(f"[Abnormal] 翻译条目数: {len(translations.translation_dict.get('zh_CN', {}))}")
    except Exception as e:
        print(f"[Abnormal] 翻译系统注册失败: {e}")

    ui.register()
    keymap.register()
    properties.register()
    operators_modal.register()
    operators.register()


def unregister():
    # 取消注册翻译
    try:
        bpy.app.translations.unregister(__name__)
        print("[Abnormal] 翻译系统取消注册成功")
    except Exception as e:
        print(f"[Abnormal] 翻译系统取消注册失败: {e}")

    ui.unregister()
    keymap.unregister()
    properties.unregister()
    operators_modal.unregister()
    operators.unregister()


if __name__ == "__main__":
    register()
