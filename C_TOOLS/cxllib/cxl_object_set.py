#基于对象状态的一些操作
import bpy
from .cxl import cxl_randomcolor ,cxl_hqsbpmzb,cxl_clean_selection,cxl_select

class cxl_freeze_objects (bpy.types.Operator):#冻结对象
    bl_idname = "view3d.cxl_freeze"  #这里的名称要小写
    bl_label = "objects_freeze"

    def execute(self,context):        
        selection= bpy.context.selected_objects
        for i in selection:
            i.hide_select = True
        return {'FINISHED'}   
#-------------------------------------------------------------------------------------------    
class cxl_unfreeze_all (bpy.types.Operator):#全部解冻
    bl_idname = "view3d.cxl_unfreeze_all"  #这里的名称要小写
    bl_label = "objects_unfreeze_all"

    def execute(self,context):        
        obj= bpy.data.objects
        for i in obj:
            i.hide_select = False
        return {'FINISHED'} 
#-------------------------------------------------------------------------------------------     
class cxl_objects_color_random (bpy.types.Operator):#选择对象随机线框颜色
    bl_idname = "view3d.cxl_objects_color_random"  
    bl_label = "objects_color_random"

    def execute(self,context):    
        selection= bpy.context.selected_objects 
        for i in selection :
            i.color= cxl_randomcolor()   
        return {'FINISHED'} 
#-------------------------------------------------------------------------------------------
class cxl_objects_color_random_unify (bpy.types.Operator):#选择对象线框颜色统一为随机值
    bl_idname = "view3d.cxl_objects_color_random_unify"  
    bl_label = "objects_color_unify"

    def execute(self,context):    
        selection= bpy.context.selected_objects
        mycolor= cxl_randomcolor()
        for i in selection :
            i.color= mycolor   
        return {'FINISHED'} 
#-------------------------------------------------------------------------------------------
class cxl_objects_material_set (bpy.types.Operator):#快速材质
    bl_idname = "view3d.cxl_kuai_su_cai_zhi"  
    bl_label = "objects_material_set"

    selectedobj=[]

    def modal(self, context, event):
        if event.type == 'MOUSEMOVE':
            return{'RUNNING_MODAL'}
        elif event.type == 'LEFTMOUSE':
            cxl_clean_selection()
            mousepos=cxl_hqsbpmzb(event)
            bpy.ops.view3d.select(location=mousepos)
            me=bpy.context.selected_objects #获取最新数据
            themat=me[0].active_material
            thecolor=me[0].color
            for i in self.selectedobj:
                i.active_material=themat
                i.color=thecolor
                for i2 in i.modifiers : 
                    if i2.type=='NODES':
                        if 'c_extrude' in i2.node_group.name:      
                            for o in i2.node_group.nodes :
                                if o.name =='c_setMaterial_value':
                                    o.inputs[2].default_value=themat
            cxl_clean_selection()
            cxl_select(self.selectedobj)
            context.window.cursor_set('DEFAULT')
            return{'CANCELLED'} 
        else:
            return{'PASS_THROUGH'}
    def invoke(self, context, event):
        if context.space_data.type == 'VIEW_3D':
            self.selectedobj=context.selected_objects
            context.window.cursor_set('EYEDROPPER')
            context.window_manager.modal_handler_add(self) 
            return {'RUNNING_MODAL'} 
        else:
            self.report({'WARNING'}, "请在3D视图操作")
            return {'CANCELLED'} 

 #self.report({'INFO'},'aaaaa')