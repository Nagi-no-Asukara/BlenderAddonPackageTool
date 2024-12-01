import bpy

from addons.expression_addon.config import __addon_name__
from addons.expression_addon.preference.AddonPreferences import ExampleAddonPreferences
from addons.expression_addon.preference.expression_key import expression_map


#bpy.data.shape_keys["Key"].key_blocks["じと目"].value = 0.383


# 应用表情操作
class ApplyExpressionOperator(bpy.types.Operator):
    bl_idname = "object.apply_expression"
    bl_label = "应用表情"

    def execute(self, context):
        scene = context.scene
        expr_props = scene.expression_properties
        expression_name = expr_props.expression_name

        if expression_name not in expression_map:
            self.report({'ERROR'}, f"表情 '{expression_name}' 不存在")
            return {'CANCELLED'}

        # 获取当前对象的形态键
        obj = bpy.context.object
        if not obj.data.shape_keys:
            self.report({'ERROR'}, "当前对象没有形态键数据。")
            return {'CANCELLED'}

        shape_keys = obj.data.shape_keys.key_blocks
        expression = expression_map[expression_name]

        # 应用形态键值
        for key, value in expression.items():
            if key in shape_keys:
                shape_keys[key].value = value
            else:
                self.report({'ERROR'}, f"形态键 '{key}' 不存在于当前对象。")
                return {'CANCELLED'}

        return {'FINISHED'}


class ResetExpressionOperator(bpy.types.Operator):
    bl_idname = "object.reset_expression"
    bl_label = "恢复初始表情"

    def execute(self, context):
        obj = bpy.context.object
        if not obj.data.shape_keys:
            self.report({'ERROR'}, "当前对象没有形态键数据。")
            return {'CANCELLED'}

        shape_keys = obj.data.shape_keys.key_blocks

        # 将所有形态键的值归零
        for key in shape_keys:
            key.value = 0.0

        self.report({'INFO'}, "已恢复初始表情")
        return {'FINISHED'}


# 生成表情动画操作
class AnimateExpressionOperator(bpy.types.Operator):
    bl_idname = "object.animate_expression"
    bl_label = "生成表情动画"

    def execute(self, context):
        scene = context.scene
        expr_props = scene.expression_properties
        expression_name = expr_props.expression_name

        if expression_name not in expression_map:
            self.report({'ERROR'}, f"表情 '{expression_name}' 不存在")
            return {'CANCELLED'}

        obj = bpy.context.object
        if not obj.data.shape_keys:
            self.report({'ERROR'}, "当前对象没有形态键数据。")
            return {'CANCELLED'}

        shape_keys = obj.data.shape_keys.key_blocks
        expression = expression_map[expression_name]

        current_frame = scene.frame_current

        # 设置初始帧
        scene.frame_set(0)
        for key in expression.keys():
            if key in shape_keys:
                shape_keys[key].value = 0.0
                shape_keys[key].keyframe_insert(data_path="value", frame=0)

        # 设置目标帧
        scene.frame_set(current_frame)
        for key, value in expression.items():
            if key in shape_keys:
                shape_keys[key].value = value
                shape_keys[key].keyframe_insert(data_path="value", frame=current_frame)

        self.report({'INFO'}, f"生成了从第0帧到第{current_frame}帧的表情动画")
        return {'FINISHED'}
