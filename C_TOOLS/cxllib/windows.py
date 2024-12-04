#c的一些常用窗口
#240120添加工具集CXL_VIEW_OT_C_TOOL
import bpy

class CXL_VIEW_OT_C_TOOl_SET :
    bl_space_type ='VIEW_3D'
    bl_region_type = 'UI'
    #bl_context ='objectmode'

class CXL_VIEW_PT_C_TOOL (CXL_VIEW_OT_C_TOOl_SET,bpy.types.Panel):#工具面板
    bl_idname = "CXL_PT_object_tools"
    bl_label = "物体工具"
    bl_category = 'C_TOOL'

    def draw(self,context):
        layout=self.layout
        col = layout.column()
        row=col.row()
        row.operator('view3d.cxl_freeze',text="冻结选择")
        row.operator('view3d.cxl_unfreeze_all',text="全部解冻")
        row=col.row()
        row.operator('view3d.cxl_objects_color_random',text="随机颜色")
        row.operator('view3d.cxl_objects_color_random_unify',text="统一颜色")

 #------------------------------------------------------       
class CXL_VIEW_PT_C_TOOL_EDIT (CXL_VIEW_OT_C_TOOl_SET,bpy.types.Panel):#工具面板
    bl_idname = "CXL_PT_object_tools_edit"
    bl_label = "内部设置"
    bl_category = 'C_TOOL'

    def draw(self,context):
        layout=self.layout
        col = layout.column()
        row=col.row()
        row.prop(context.scene, "cc_weld",text='焊接：')
        row.prop(context.scene, "snap_guolv",text='捕捉过滤：')

    

def draw_cxl_extendHeader(self,context): #捕捉提示视口提示
    layout =self.layout
    cxl_snap_state=context.scene.cxl_snap_state
    cxl_snaptoggle=context.scene.cxl_snaptoggle
    if cxl_snaptoggle==True:
        layout.label(text=" C_snap: ON")
    else:
        layout.label(text=" C_snap:OFF")
    layout.label(text=('-'+cxl_snap_state+'-'))




class CXL_VIEW_MT_JINGGAO (bpy.types.Operator):#一般性提示窗口
    bl_idname = "cwindow.jinggao"
    bl_label = "重要提示"
    bl_options = {'REGISTER','UNDO'}

    jinggaotxt='警告：'
    def invoke(self, context, event):
        self.jinggaotxt=self.jinggaotxt+context.scene.cc_jinggao
        return context.window_manager.invoke_props_popup(self, event)
    def execute(self, context):
        return {'FINISHED'}
    def draw(self, context):
        col = self.layout.column()
        row = col.row()
        row.label(text=self.jinggaotxt)


#-------------------------------------------------

class CXL_VIEW_PT_CHUANGJIAN(bpy.types.Panel):#快速创建面板
    bl_space_type ='VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_idname = "CXL_PT_CHUANGJIAN"
    bl_label = "创建"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_DEFAULT' #这句话必须要添加  否则调用操作符会因为上下文不正确而无法执行
        col = layout.column()
        row = col.row()
        row.label(text='创建',translate=False)
        row = col.row()
        row.operator("view3d.cxl_create_line", text="Line",translate=False)
        row.operator("view3d.cxl_create_rectangle", text="Rectangle",translate=False)
        row.operator("view3d.cxl_create_circle", text="Circle",translate=False)
        row = col.row()
        row.operator("view3d.cxl_create_plane", text="Plane",translate=False)
        row.operator("view3d.cxl_create_box", text="Box",translate=False)
        row.operator("view3d.cxl_create_sphere", text="Sphere",translate=False)
        
class CXL_VIEW_PT_XUGAIQI(bpy.types.Panel):#节点修改器面板
    bl_space_type ='VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_idname = "CXL_PT_XUGAIQI"
    bl_label = "快速修改器面板"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_DEFAULT' #这句话必须要添加  否则调用操作符会因为上下文不正确而无法执行
        col = layout.column()
        row = col.row()
        row.label(text='材质调整', text_ctxt='Change_Material', translate=False)
        row.operator("view3d.cxl_caizhi_c_uv_tianjia", text="c_uv",translate=False)
        row = col.row()
        row.label(text='修改器', text_ctxt='Modifiers', translate=False)
        row = col.row()
        row.operator("view3d.cxl_extrude_spline", text="Extrude",translate=False)
        row.operator("view3d.cxl_pinmian_modfier", text="Face",translate=False)
        row.operator("view3d.cxl_xyz_uvwmap", text="UVW_map",translate=False)
        row = col.row()
        row.operator("view3d.cxl_zhuankuai_modfier", text="Brick",translate=False)
        row = col.row()
        




#------------------------------------------------
