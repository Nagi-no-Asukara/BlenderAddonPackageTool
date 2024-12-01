import bpy
import bpy.props
from addons.sec_day_addon.config import __addon_name__
from addons.sec_day_addon.preference.AddonPreferences import ExampleAddonPreferences


# This Example Operator will scale up the selected object
class ExampleOperator(bpy.types.Operator):
    """
    ExampleAddon
    """
    bl_idname = "object.example_ops"
    bl_label = "ExampleOperator"

    # 确保在操作之前备份数据，用户撤销操作时可以恢复
    bl_options = {'REGISTER', 'UNDO'}

    # 注意 这里是定义 不能是 =
    filepath : bpy.props.StringProperty(subtype='FILE_PATH')

    @classmethod
    def poll(cls, context: bpy.types.Context):
        return context.active_object is not None

    def execute(self, context: bpy.types.Context):
        print(self.filepath)
        with open(self.filepath, 'r', encoding = 'UTF-8') as f:
            content = f.read()
            print('content', content)
        return {'FINISHED'}

    def invoke(self, context: bpy.types.Context, event: bpy.types.Event):
        #弹出一个文件选取框
        context.window_manager.fileselect_add(self)

        #没有modal方法也要返回 因为这是modal方法
        return {'RUNNING_MODAL'}
