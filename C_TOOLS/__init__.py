'''一些小工具
一种类似于3dmax的移动捕捉方式, 互交式创建基本对象，对象批量操作
241126 修改注册快捷键方式,注册快捷键功能借鉴了quick_groups 插件
开发者：陈兴良'''

import bpy
import rna_keymap_ui


bl_info = {
    "name": "CXL_tools",
    "author": "chen_xing_liang (kkmya@qq.com)",
    "version": (24,11,25),
    "blender": (4,2,0),
    "description": "一些常用小工具集"
    }

from .cxllib.registration import cxl_register_keymaps, cxl_unregister_keymaps 
from .cxllib.cxl_object_set import cxl_freeze_objects,cxl_unfreeze_all,cxl_objects_color_random,cxl_objects_color_random_unify,cxl_objects_material_set
from .cxllib.cxl_toos import cxl_zomm,cxl_wireframe_switch,cxl_snap,cxl_shikouqiehuan,cxl_move_tool,cxl_snapstate_x,cxl_snapstate_y,cxl_snapstate_z,cxl_snapstate_xy,cxl_snap_shuaxing,cxl_convert_to_mesh
from .cxllib.cxl_create import cxl_create_line,cxl_create_box,cxl_create_rectangle,cxl_create_circle,cxl_create_sphere,cxl_create_plane
from .cxllib.windows import CXL_VIEW_PT_C_TOOL,CXL_VIEW_PT_C_TOOL_EDIT,CXL_VIEW_MT_JINGGAO,CXL_VIEW_PT_CHUANGJIAN ,CXL_VIEW_PT_XUGAIQI
from .cxllib.windows import draw_cxl_extendHeader
from .cxllib.cxl_modifiers import cxl_flip,cxl_extrude_modfier,cxl_xyz_uvwmap_modfier,cxl_pinmian_modfier,cxl_zhuankuai_modfier,cxl_caizhi_c_uv_tianjia
from .cxllib.cxl_spline import cxl_weld


class cxl_chajianshuxingxianshi(bpy.types.AddonPreferences): #这个貌似必须写在 _init_ 文件内  不然识别不出来
    bl_idname = __package__
    def draw(self, context):
        layout = self.layout
        wm = bpy.context.window_manager
        kc = wm.keyconfigs.addon

        from .cxllib.keys import cxl_keys
        cxl_keylists = [cxl_keys ["MENU"]]

        for idx, item in enumerate(cxl_keylists[0]):
            keymap = item.get("keymap")
            if not keymap:
                continue
            km = kc.keymaps.get(keymap)
            kmi = None
            if km:
                idname = item.get("idname")
                for kmitem in km.keymap_items:
                    if kmitem.idname != idname:
                        continue
                    properties = item.get("properties")
                    if properties:
                        if all([getattr(kmitem.properties, name, None) == value for name, value in properties]):
                            kmi = kmitem
                            break
                    else:
                        kmi = kmitem
                        break
            if kmi:
                row = layout.row()
                rna_keymap_ui.draw_kmi(
                    ["ADDON", "USER", "DEFAULT"], kc, km, kmi, row, 0)
                drawn = True

cxl_classs = (
    cxl_freeze_objects,cxl_unfreeze_all,
    cxl_zomm,cxl_wireframe_switch, cxl_shikouqiehuan,
    cxl_create_rectangle,cxl_create_line,cxl_create_box,cxl_snap_shuaxing,cxl_create_circle,cxl_create_sphere,cxl_create_plane,
    cxl_extrude_modfier,cxl_flip,
    cxl_snap,cxl_snapstate_x,cxl_snapstate_y,cxl_snapstate_z,cxl_snapstate_xy,
    CXL_VIEW_PT_C_TOOL,CXL_VIEW_PT_C_TOOL_EDIT,CXL_VIEW_MT_JINGGAO,CXL_VIEW_PT_CHUANGJIAN,CXL_VIEW_PT_XUGAIQI,
    cxl_objects_color_random_unify,cxl_objects_color_random,cxl_objects_material_set,
    cxl_move_tool,cxl_weld,cxl_xyz_uvwmap_modfier,cxl_pinmian_modfier,cxl_chajianshuxingxianshi,cxl_convert_to_mesh,cxl_zhuankuai_modfier,
    cxl_caizhi_c_uv_tianjia
    )
#--------------------------------


#

cxl_sence_set = [] #一些参数设置
def register():
    global cxl_classs , cxl_sence_set
    for cls in cxl_classs:
        bpy.utils.register_class(cls)
        #将上面用到的功能全部注册
    #------------------  
    cxl_register_keymaps() #注册快捷键

    #脚本中用到的一些设置参数
    thesence=bpy.types.Scene
    thesence.cxl_snaptoggle = bpy.props.BoolProperty(name="cxl_snaptoggle",default=True) #轴向
    thesence.cxl_snap_state = bpy.props.StringProperty(name="cxl_snap_state",default="XYZ") #轴向
    thesence.cc_weld = bpy.props.FloatProperty(name="cc_weld",default=0.01,description='焊接命令的阈值')
    thesence.cc_jinggao = bpy.props.StringProperty(name="cc_jinggao",default='警告：')
    thesence.c_jichu = bpy.props.FloatProperty(name="c_jichu",default=200) #轴向
    thesence.snap_guolv = bpy.props.IntProperty(name="snap_guolv",default=1000,description='捕捉将过滤掉点数大于此数值的对象')
    
    cxl_sence_set=[thesence.cxl_snaptoggle , thesence.cxl_snap_state , thesence.cc_weld , thesence.cc_jinggao , thesence.c_jichu , thesence.snap_guolv]
    #-------------窗口扩展
    bpy.types.VIEW3D_HT_tool_header.append(draw_cxl_extendHeader)



def unregister():
    global cxl_classs
    for cls2 in cxl_classs:
        bpy.utils.unregister_class(cls2)  
    #---卸载类
    cxl_unregister_keymaps()    #卸载快捷键  

    #卸载窗口扩展
    bpy.types.VIEW3D_HT_tool_header.remove(draw_cxl_extendHeader)
    #-----------------------------------------------------
    for cc_set_i in cxl_sence_set : del cc_set_i
    #卸载所有设置参数

if __name__ == "__main__":
    register()



