import bpy
from OpenImageIO import VECTOR
from bpy_extras.view3d_utils import region_2d_to_vector_3d, region_2d_to_location_3d
from mathutils import Vector

from addons.miuna_addon.config import __addon_name__
from addons.miuna_addon.preference.AddonPreferences import ExampleAddonPreferences


# This Example Operator will scale up the selected object
class ExampleOperator(bpy.types.Operator):
    """
    ExampleAddon
    """
    bl_idname = "object.example_ops"
    bl_label = "ExampleOperator"

    # 确保在操作之前备份数据，用户撤销操作时可以恢复
    bl_options = {'REGISTER', 'UNDO'}
    action: bpy.props.EnumProperty(items =
                                   [('SCALE',"Scale",'Scale'),
                                    ('Translate','Translate',"Translate"),
                                    ('Rotate','Rotate','Rotate')],
                                   name = 'action', default='SCALE')
    scale: bpy.props.FloatProperty(name="Scale", description="Scale factor", default=1.0, min=0.0, max=5.0)

    mouse = {'x':0 , 'y':0}
    initial_location = None

    @classmethod
    def poll(cls, context: bpy.types.Context):
        """
        可以执行的前提条件
        不满足插件就是灰色的
        """
        return context.active_object is not None

    def execute(self, context: bpy.types.Context):
        # match self.action:
        #     case 'SCALE':
        #         context.active_object.scale *= self.scale
        #     case 'Translate':
        #         context.active_object.location.x += self.scale
        #     case 'Rotate':
        #         context.active_object.rotation_euler[2] +=self.scale
        mouse_coord = Vector((self.mouse['x'], self.mouse['y']))
        vec = region_2d_to_vector_3d(context.region,context.space_data.region_3d, mouse_coord)
        loc = region_2d_to_location_3d(context.region, context.space_data.region_3d, mouse_coord, vec)
        context.active_object.location = loc

        #bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1) 刷新界面操作
        return {'FINISHED'}
    def invoke(self, context: bpy.types.Context, event: bpy.types.Event):
        """
        execute执行之前执行的方法 有点类似于aop
        """
        #初始化一些参数
        self.scale = 2
        #弹窗询问是否确定

        #MODAL必加 页面每刷新一次就触发
        context.window_manager.modal_handler_add(self)
        self.initial_location = context.active_object.location.copy()
        #定时器
        return {'RUNNING_MODAL'}
        #调用一个对话框 内部把参数都列好
        #return context.window_manager.invoke_props_dialog(self)

    def modal(self, context: bpy.types.Context, event: bpy.types.Event):
        """
        持续方法触发器
        比如按G不断移动物体，对应物体也在不断地变化
        """
        match event.type:
            case 'MOUSEMOVE':
                self.mouse['x'] = event.mouse_x
                self.mouse['y'] = event.mouse_y
                #也可以不要execute 用一般方法也行
                self.execute(context)
            case 'LEFTMOUSE':
                return {"FINISHED"}
            case 'RIGHTMOUSE'| 'ESC':
                #取消操作
                context.active_object.location = self.initial_location.copy()
                return {'CANCELLED'}
            case _:
                return {'PASS_THROUGH'}
        return {'RUNNING_MODAL'}


class ExampleOperatorTwo(bpy.types.Operator):
    """
    ExampleAddon
    """
    bl_idname = "object.example_ops2"
    bl_label = "ExampleOperator2"
    @classmethod
    def poll(cls, context: bpy.types.Context):
        return context.active_object is not None

    def execute(self, context: bpy.types.Context):
        """
        为什么这样行得通
        我的看法是blender底层是c++实现的，所以python接口会进行一次编译，然后用c++去运行
        像上面那个接口会被转换为一个函数接收两个参数
        """
        bpy.ops.object.example_ops(scale =3,action = 'SCALE')
        #bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1) 刷新界面操作
        return {'FINISHED'}