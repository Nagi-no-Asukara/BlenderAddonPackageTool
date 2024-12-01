import bpy

from addons.expression_addon.config import __addon_name__
from addons.expression_addon.preference.expression_key import expression_map, expression_name_to_chinese
from common.i18n.i18n import i18n


class ExampleAddonPanel(bpy.types.Panel):
    bl_label = "表情控制面板"
    bl_idname = "VIEW3D_PT_expression_control"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "表情控制"


    def draw(self, context: bpy.types.Context):
        layout = self.layout
        scene = context.scene
        expr_props = scene.expression_properties

        # 显示选项卡
        layout.prop(expr_props, "expression_name")
        layout.operator("object.apply_expression", text="应用表情")
        layout.operator("object.reset_expression", text="恢复初始表情")
        layout.operator("object.animate_expression", text="生成表情动画")

    @classmethod
    def poll(cls, context: bpy.types.Context):
        return True

# 定义一个属性组，用于存储可选的表情名称
class ExpressionProperties(bpy.types.PropertyGroup):
    expression_name: bpy.props.EnumProperty(
        name="表情",
        description="选择一个表情",
        items=[
            (name, expression_name_to_chinese.get(name, name), f"应用 {expression_name_to_chinese.get(name, name)} 表情")
            for name in expression_map.keys()
        ],
    )
