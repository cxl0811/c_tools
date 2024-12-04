#常用整体操作工具 
#20240120尝试添加移动捕捉功能
import bpy
from .cxl import cxl_hqsbpmzb,Update3DViewPorts,cc_snaptoggle,cxl_snaptopoint,cxl_getapoint,cxl_shizixingyichu,cc_snapstate_set,cc_jisuanzhongxingdian,cxl_namebytime,c_huoqujianpanzhi,cc_danweishipei,cxlshikoupanduan
from .cxl import cxl_shizixing,cxl3dto2d,cxl_jian,cxl_jia,cxl_clean_selection,Update3DViewPorts,cc_move_xyz,cc_shuaxing_shikou_dingdian_2d,cc_shuaxing_shikou_dingdian,cxl_select
import copy
import mathutils 
import bmesh

#----------------------------------------------------
class cxl_wireframe_switch (bpy.types.Operator):#线框与实体显示切换
    bl_idname = "view3d.cxl_wireframe_switch"  #这里的名称要小写
    bl_label = "wireframe_switch"

    def execute(self, context):
         if context.area.type=='VIEW_3D' :
            itype=context.space_data.shading.type
            if itype=='WIREFRAME':
                context.space_data.shading.type='MATERIAL'
            else:
                context.space_data.shading.type='WIREFRAME'
         return {'FINISHED'}
#-------------------------------------------------------------------------------------------     
class cxl_zomm (bpy.types.Operator):#视口缩放
    bl_idname = "view3d.cxl_zoom"  #这里的名称要小写
    bl_label = "cxl zoom"
    
    sbzjax= 0 #鼠标左键是否按下,按下为1 否则为0
    sbwza=[0,0] #用于记录鼠标滑动初始位置

    def modal(self, context, event):
        if self.sbzjax==0:
           self.sbwza=cxl_hqsbpmzb(event)
        #如果鼠标左键未按下,则事实更新鼠标位置

        if event.type in {'MIDDLEMOUSE', 'WHEELUPMOUSE', 'WHEELDOWNMOUSE','Q'}:
            self.sbzjax= 0 #防止下次运行时出错
            return{'PASS_THROUGH'}#中键跳过
        elif event.type == 'MOUSEMOVE':
            if self.sbzjax ==1 :
                sbwzb=cxl_hqsbpmzb(event) #当鼠标按下时的位置
                wicj=sbwzb[1]-self.sbwza[1]
                if wicj>2:   #在2屏幕像素内控制缩放操作
                    bpy.ops.view3d.zoom(delta=+1)
                    context.window.cursor_set('ZOOM_IN')
                    self.sbwza=sbwzb
                elif wicj<-2:
                    bpy.ops.view3d.zoom(delta=-1)
                    context.window.cursor_set('ZOOM_OUT')
                    self.sbwza=sbwzb
            return {'RUNNING_MODAL'} #未按下时不操作
        elif event.type == 'LEFTMOUSE': 
            if event.value=='PRESS':
                self.sbzjax=1
            elif event.value=='RELEASE':
                self.sbzjax=0
                 #记录鼠标状态
            return {'RUNNING_MODAL'} 
        elif event.type in {'RIGHTMOUSE', 'ESC'}:
             self.sbzjax=0#防止下次运行时出错
             bpy.ops.wm.tool_set_by_id(name="builtin.select_box")
             context.window.cursor_set('DEFAULT')
             return {'CANCELLED'} #结束后切换到框选模式
        elif event.type in {'NONE','INBETWEEN_MOUSEMOVE'}:
            self.sbzjax= 0 #防止下次运行时出错
            return {'RUNNING_MODAL'} #这两种情况不打断
        else:
            self.sbzjax= 0 #防止下次运行时出错
            return {'PASS_THROUGH'}
    #######被其他操作打断
        
    def invoke(self, context, event):
        if context.space_data.type == 'VIEW_3D':
            context.window_manager.modal_handler_add(self)
            context.window.cursor_set('ZOOM_OUT')
            return {'RUNNING_MODAL'}  
        else:
            self.report({'WARNING'}, "请在3D视口中使用该操作")
            return {'CANCELLED'}     
#-------------------------------------------------------------------------------------------    
class cxl_snap (bpy.types.Operator):#捕捉开关
    bl_idname = "view3d.cxl_snaptooggle"
    bl_label = "捕捉开关"

    def execute(self, context):
        cc_snaptoggle ()
        Update3DViewPorts()
        return {'FINISHED'}
#----------------------------------------------------------
class cxl_snapstate_x (bpy.types.Operator):#启用X轴
    bl_idname = "view3d.cxl_snap_x"
    bl_label = "启用X轴"
    def execute(self, context):
        cc_snapstate_set("X")
        Update3DViewPorts()
        return {'FINISHED'}
#----------------------------------------------------------
class cxl_snapstate_y (bpy.types.Operator):#启用Y轴
    bl_idname = "view3d.cxl_snap_y"
    bl_label = "启用Y轴"
    def execute(self, context):
        cc_snapstate_set("Y")
        Update3DViewPorts()
        return {'FINISHED'}
#----------------------------------------------------------
class cxl_snapstate_z (bpy.types.Operator):#启用Z轴
    bl_idname = "view3d.cxl_snap_z"
    bl_label = "启用Z轴"
    def execute(self, context):
        cc_snapstate_set("Z")
        Update3DViewPorts()
        return {'FINISHED'}
#----------------------------------------------------------
class cxl_snapstate_xy (bpy.types.Operator):#启用XY轴 或者 XYZ轴
    bl_idname = "view3d.cxl_snap_xy"
    bl_label = "启用XY轴"
    def execute(self, context):
        cxl_snap_state=bpy.context.scene.cxl_snap_state
        if cxl_snap_state=="XYZ":
            cc_snapstate_set("XY")
        else:
            cc_snapstate_set("XYZ")
        Update3DViewPorts()
        return {'FINISHED'}
#----------------------------------------------------------
class cxl_shikouqiehuan (bpy.types.Operator):#视口切换
    bl_idname = "view3d.cxl_shikouqiehuan"
    bl_label = "视口切换"

    def execute(self, context):
        from .cxl import cc_user_addon_path
        window=bpy.context.window
        wk=bpy.data.workspaces
        havelens=False
        dqlayout=None
        for i in wk :
            if i.name =='Lens' :havelens=True
            if i.name in ['布局','Layout']:dqlayout=i
        if havelens ==False:
                setfilename=(cc_user_addon_path()+'\\C_TOOLS\\cxllib\\cxl_scene_set.blend')
                bpy.ops.workspace.append_activate(idname='Lens', filepath=setfilename)
                wk=bpy.data.workspaces
                for i in wk :
                    if i.name==(dqlayout.name+".001"):
                        i.name='Lens'
        else:
            dqworkspace=bpy.context.window.workspace.name
            wk=bpy.data.workspaces
            for i in wk:
                if i.name =='Lens':
                    thelens=i
            if dqworkspace in ['布局','Layout','Lens']:
                if dqworkspace !='Lens':
                    window.workspace=thelens
                else:
                    window.workspace=dqlayout     
            else:
                window.workspace=dqlayout #切换到布局
        return {'FINISHED'}
#----------------------------------------------------------




def cc_copymodifier_to_obj (obj,modifier): #复制某个修改器到另一个个对象上
    modifier_add = obj.modifiers.new(name=modifier.name, type=modifier.type)
    for i in modifier.bl_rna.properties:
        if not hasattr(i, 'is_readonly') or not i.is_readonly:
            if not hasattr(i, 'is_pointer') or not i.is_pointer:
                setattr(modifier_add, i.identifier, getattr(modifier, i.identifier))
#----------------------------------------------------------
def cc_genju_shikou_suoding_yidong_jisuan (yuanzuobiao, zhouxiang ,yidongzhi):#根据视口判断移动方向并计算数值
    shikou=cxlshikoupanduan()
    xingzuobiao=yuanzuobiao
    temppos=[0,0,0]

    if shikou in "front":
        if zhouxiang=='X':
            temppos=[yidongzhi,0,0]
        elif zhouxiang =='Y':
            temppos=[0,0,yidongzhi]
        elif zhouxiang =='Z':
            temppos=[0,yidongzhi,0]
        elif zhouxiang =='XY':
            temppos=[yidongzhi,0,yidongzhi]
        elif zhouxiang =='XYZ':
            temppos=[yidongzhi,yidongzhi,yidongzhi] 
    elif shikou== "bottom":
        if zhouxiang=='X':
            temppos=[yidongzhi,0,0]
        elif zhouxiang =='Y':
            temppos=[0,-yidongzhi,0]
        elif zhouxiang =='Z':
            temppos=[0,0,-yidongzhi]
        elif zhouxiang =='XY':
            temppos=[yidongzhi,-yidongzhi,0]
        elif zhouxiang =='XYZ':
            temppos=[yidongzhi,-yidongzhi,-yidongzhi]
    elif shikou== "back":
        if zhouxiang=='X':
            temppos=[-yidongzhi,0,0]
        elif zhouxiang =='Y':
            temppos=[0,0,yidongzhi]
        elif zhouxiang =='Z':
            temppos=[0,yidongzhi,0]
        elif zhouxiang =='XY':
            temppos=[-yidongzhi,0,yidongzhi]
        elif zhouxiang =='XYZ':
            temppos=[-yidongzhi,yidongzhi,yidongzhi] 
    elif shikou== "right":
        if zhouxiang=='X':
            temppos=[0,yidongzhi,0]
        elif zhouxiang =='Y':
            temppos=[0,0,yidongzhi]
        elif zhouxiang =='Z':
            temppos=[yidongzhi,0,0]
        elif zhouxiang =='XY':
            temppos=[0,yidongzhi,yidongzhi]
        elif zhouxiang =='XYZ':
            temppos=[yidongzhi,yidongzhi,yidongzhi] 
    elif shikou== "left":
        if zhouxiang=='X':
            temppos=[0,-yidongzhi,0]
        elif zhouxiang =='Y':
            temppos=[0,0,yidongzhi]
        elif zhouxiang =='Z':
            temppos=[-yidongzhi,0,0]
        elif zhouxiang =='XY':
            temppos=[0,yidongzhi,yidongzhi]
        elif zhouxiang =='XYZ':
            temppos=[-yidongzhi,yidongzhi,yidongzhi] 
    else:
        if zhouxiang=='X':
            temppos=[yidongzhi,0,0]
        elif zhouxiang =='Y':
            temppos=[0,yidongzhi,0]
        elif zhouxiang =='Z':
            temppos=[0,0,yidongzhi]
        elif zhouxiang =='XY':
            temppos=[yidongzhi,yidongzhi,0]
        elif zhouxiang =='XYZ':
            temppos=[yidongzhi,yidongzhi,yidongzhi]
    xingzuobiao=cxl_jia(yuanzuobiao,temppos) 
    return(xingzuobiao)
class cxl_move_tool(bpy.types.Operator):#移动工具
    bl_idname = "view3d.cxl_move"
    bl_label = "移动工具"

    mode="OBJECT" #  OBJECT   EDIT_MESH   EDIT_CURVES
    pointa=None
    pointb=None

    selection=[]
    selectionpos=[]
    copyobj=[]

    shift=False
    ctrl =False
    
    move_value=''

    def modal(self, context, event):
        cxl_snaptoggle =context.scene.cxl_snaptoggle #捕捉
        cxl_snap_state=bpy.context.scene.cxl_snap_state

        #----------------------------------------
        temp = c_huoqujianpanzhi(event) #数值移动
        if temp in {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.', '-'}:
            if event.value == 'PRESS':
                if len(self.move_value) == 0:
                    self.move_value = self.move_value + temp
                elif temp != '-':
                    self.move_value = self.move_value + temp
            self.report({'INFO'}, "移动"+cxl_snap_state+':'+self.move_value)
            return {'RUNNING_MODAL'}
        elif event.type == "BACK_SPACE":
            self.move_value = self.move_value[:-1]  # 退格
            self.report({'INFO'}, "移动"+cxl_snap_state+':'+self.move_value)
            return {'RUNNING_MODAL'}
        elif event.type in {'RET', 'NUMPAD_ENTER'}:
            if self.move_value != "":
                move_value_s=cc_danweishipei(float(self.move_value))
                for i in range (len(self.selection)):
                    if self.mode=="OBJECT":
                        self.selection[i].location=cc_genju_shikou_suoding_yidong_jisuan(self.selectionpos[i],cxl_snap_state,move_value_s)
                    elif self.mode=="EDIT_MESH": #编辑模式移动
                        meshverts=(bpy.context.active_object.data.vertices)
                        meshverts[self.selection[i]].co=cc_genju_shikou_suoding_yidong_jisuan(self.selectionpos[i],cxl_snap_state,move_value_s)
                    elif self.mode=="EDIT_CURVE": #曲线编辑模式
                        spl=bpy.context.active_object.data.splines
                        for o in range(len(self.selection[i])):
                            if spl[i].type=="BEZIER":
                                thepiont=spl[i].bezier_points[self.selection[i][o]]
                                
                                thepiont.co= cc_genju_shikou_suoding_yidong_jisuan(self.selectionpos[i][o][0],cxl_snap_state,move_value_s)
                                thepiont.handle_left= cc_genju_shikou_suoding_yidong_jisuan(self.selectionpos[i][o][1],cxl_snap_state,move_value_s)
                                thepiont.handle_right= cc_genju_shikou_suoding_yidong_jisuan(self.selectionpos[i][o][2],cxl_snap_state,move_value_s)
                            else:
                                thepiont=spl[i].points[self.selection[i][o]]
                                thepiont.co= cc_genju_shikou_suoding_yidong_jisuan(self.selectionpos[i][o],cxl_snap_state,move_value_s)
            #self.move_value=''
            #self.cc_xuanzhe_shuaxing (context)
            cxl_shizixingyichu()
            if self.mode!="OBJECT":
                        bpy.ops.object.mode_set(mode="EDIT")
            return {'CANCELLED'}
        #----------------------------------------
        if event.type == 'MOUSEMOVE':
            if cxl_snaptoggle ==True :
                self.pointb=cxl_snaptopoint(event)
                if self.pointb==None:self.pointb=cxl_getapoint(event)
            else:
                self.pointb=cxl_getapoint(event)
            cxl_shizixingyichu() #---先移除现有的十字星
            if  self.pointb !=None:
                if cxl_snaptoggle ==True :cxl_shizixing(cxl3dto2d(self.pointb))
                if self.pointa !=None:
                    self.pointb=cc_move_xyz(self.pointa,self.pointb)#轴向锁定
                    movespace=cxl_jian(self.pointb,self.pointa)
                    for i in range(len(self.selection)) :
                        if len(self.copyobj)==0 : #shift 功能切换
                            if self.mode=="OBJECT":
                                self.selection[i].location=cxl_jia(self.selectionpos[i],movespace)#移动对象
                            elif self.mode=="EDIT_MESH": #编辑模式移动
                                temp=mathutils.Vector(cxl_jia(self.selectionpos[i],movespace))
                                meshverts=(bpy.context.active_object.data.vertices)
                                meshverts[self.selection[i]].co=temp 
                            elif self.mode=="EDIT_CURVE": #曲线编辑模式
                                spl=bpy.context.active_object.data.splines
                                for o in range(len(self.selection[i])):
                                    if spl[i].type=="BEZIER":
                                        thepiont=spl[i].bezier_points[self.selection[i][o]]
                                        thepiont.co=mathutils.Vector(cxl_jia(self.selectionpos[i][o][0],movespace))
                                        thepiont.handle_left=mathutils.Vector(cxl_jia(self.selectionpos[i][o][1],movespace))
                                        thepiont.handle_right=mathutils.Vector(cxl_jia(self.selectionpos[i][o][2],movespace))
                                    else:
                                        thepiont=spl[i].points[self.selection[i][o]]
                                        thepiont.co=mathutils.Vector(cxl_jia(self.selectionpos[i][o],movespace))
                        else: #shift 功能切换
                            self.copyobj[i].location=cxl_jia(self.selectionpos[i],movespace)#复制并移动对象
                        #切换移动对象
                    return{'RUNNING_MODAL'} 
        #----------------------------------------
        elif event.type == 'LEFTMOUSE':
                cxl_shizixingyichu() #---先移除现有的十字星
                if event.value=='PRESS':
                    if cxl_snaptoggle ==True :
                        self.pointa=cxl_snaptopoint(event)
                    else:
                        self.pointa=cxl_getapoint(event)
                        #--------------------------------------------------------自动捕捉中心点功能
                    if self.pointa ==None:  
                        temppos=[]
                        if self.mode=="OBJECT":
                            temppos=self.selectionpos
                        elif self.mode == 'EDIT_MESH':
                            me=context.active_object #当前编辑对象
                            mematrix=me.matrix_world
                            temppos=[(i @ mematrix)+me.location for i in self.selectionpos]
                        elif self.mode == 'EDIT_CURVE':
                            me=context.active_object #当前编辑对象
                            mematrix=me.matrix_world
                            for i in self.selectionpos:
                                if isinstance(i, list):
                                    for i2 in i :
                                        if isinstance(i2, list):
                                            temppos.append((i2[0] @ mematrix)+me.location)
                                        else:
                                            temppos.append((i2 @ mematrix)+me.location.to_4d())
                        self.pointa=cc_jisuanzhongxingdian(temppos) 
                    #-------------------------------------------------------------- shift  关联复制功能           
                    if self.shift==True and self.ctrl==False:
                         if self.mode=="OBJECT":
                            cxl_clean_selection ()
                            for i in range(len(self.selection)):# 移动关联复制功能
                                tempobj= bpy.data.objects.new(name=(self.selection[i].name), object_data=self.selection[i].data)
                                bpy.context.scene.collection.objects.link(tempobj)
                                tempobj.rotation_euler=self.selection[i].rotation_euler
                                tempobj.scale=self.selection[i].scale
                                
                                tempobj.select_set(True)
                                self.copyobj.append(tempobj)
                                bpy.context.view_layer.objects.active=self.copyobj[-1]
                                for i2 in self.selection[i].modifiers:
                                    cc_copymodifier_to_obj(tempobj,i2)
                    #----------------------------------------------------------ctrl shift  复制功能 
                    elif self.shift==True and self.ctrl==True:
                        if self.mode=="OBJECT":
                            cxl_clean_selection ()
                            for i in range(len(self.selection)):# 移动关联复制功能 深度复制
                                tempobj= bpy.data.objects.new(name=(self.selection[i].name), object_data=self.selection[i].data.copy())
                                bpy.context.scene.collection.objects.link(tempobj)
                                tempobj.rotation_euler=self.selection[i].rotation_euler
                                tempobj.scale=self.selection[i].scale
                                
                                tempobj.select_set(True)
                                self.copyobj.append(tempobj)
                                bpy.context.view_layer.objects.active=self.copyobj[-1]
                                for i2 in self.selection[i].modifiers:
                                    cc_copymodifier_to_obj(tempobj,i2)
                    #-------------------------------------------------------------------------------------------------------------   
                    return{'RUNNING_MODAL'}
                else:
                    context.window.cursor_set('DEFAULT')
                    if self.mode!="OBJECT":
                        bpy.ops.object.mode_set(mode="EDIT")
                    return {'CANCELLED'} #主循环
        #----------------------------------------     
        elif event.type in {'RIGHTMOUSE', 'ESC'}:#放弃操作时恢复原样
            if self.mode=="OBJECT":
                for i in range(len(self.selection)) :
                            self.selection[i].location=self.selectionpos[i]
                if len(self.copyobj)!=0: #删除复制对象
                    for i in self.copyobj:
                        bpy.data.objects.remove(i)
                    for i in self.selection:
                        i.select_set(True)
                    bpy.context.view_layer.objects.active=self.selection[-1]
            elif self.mode=="EDIT_MESH":
                for i in range(len(self.selection)) :
                    meshverts=(bpy.context.active_object.data.vertices)
                    meshverts[self.selection[i]].co=self.selectionpos[i]
            elif self.mode=="EDIT_CURVE": #曲线编辑模式
                for i in range(len(self.selection)) :
                    spl=bpy.context.active_object.data.splines
                    for o in range(len(self.selection[i])):
                        if spl[i].type=="BEZIER":
                            thepiont=spl[i].bezier_points[self.selection[i][o]]
                            thepiont.co=self.selectionpos[i][o][0]
                            thepiont.handle_left=self.selectionpos[i][o][1]
                            thepiont.handle_right=self.selectionpos[i][o][2]
                        else:
                            thepiont=spl[i].points[self.selection[i][o]]
                            thepiont.co=self.selectionpos[i][o]
            #------------------------------- 以下为状态复位操作
            context.window.cursor_set('DEFAULT')
            if self.mode!="OBJECT":
                        bpy.ops.object.mode_set(mode="EDIT")
            cxl_shizixingyichu() #移除可能存在的辅助显示十字星
            return {'CANCELLED'} #结束
        #----------------------------------------
        elif event.type in {'LEFT_SHIFT','RIGHT_SHIFT'}:
            if event.value=='PRESS':
                self.shift=True
            else:
                self.shift=False
            return {'RUNNING_MODAL'}
        #----------------------------------------
        elif event.type in {'LEFT_CTRL','RIGHT_CTRL'}:
            if event.value=='PRESS':
                self.ctrl=True
            else:
                self.ctrl=False
            return {'RUNNING_MODAL'}
        #----------------------------------------
        elif event.type in {'MIDDLEMOUSE', 'WHEELUPMOUSE', 'WHEELDOWNMOUSE'}:
            cc_shuaxing_shikou_dingdian_2d()
            return {'PASS_THROUGH'}#中键不管

        return {'PASS_THROUGH'}#其他继续
         #######鼠标操作循环
    #----------------------------------------------------------------------------------------------------------
    def cc_xuanzhe_shuaxing (self, context): #选中对象的数据更新
        self.selection=[]
        self.selectionpos=[]
        self.copyobj=[]
        if  bpy.context.mode=="OBJECT":
            self.selection= bpy.context.selected_objects 
            for i in self.selection:
                self.selectionpos.append(copy.copy(i.location))#此处必须为复制  否则坐标会实时更新，出现错误
        elif bpy.context.mode=="EDIT_MESH":  #标记网格对象顶点位置
            self.mode="EDIT_MESH"
            bpy.ops.object.mode_set(mode='OBJECT')#暂时回到物体模式并记录 
            #将对象顶点编号加入selection，再将对应坐标加入selectionpos
            for i in (context.active_object.data.vertices):
                if i.select==True:
                    self.selection.append(i.index)
                    self.selectionpos.append(copy.copy(i.co))
        elif bpy.context.mode=="EDIT_CURVE":  #标记线条对象选择的顶点位置
            self.mode="EDIT_CURVE"
            bpy.ops.object.mode_set(mode='OBJECT')#暂时回到物体模式并记录 不知为何添加该指令后 鼠标图标无法变成移动状态
            for i in (context.active_object.data.splines):
                temp=[]
                temppos=[]
                if i.type=="BEZIER":
                    for i2 in range (len(i.bezier_points)):
                        if i.bezier_points[i2].select_control_point==True:
                            temp.append (i2)
                            temppos.append ([copy.copy(i.bezier_points[i2].co),copy.copy(i.bezier_points[i2].handle_left),copy.copy(i.bezier_points[i2].handle_right)])
                else: #poly nurbs  共用
                    for i2 in range(len(i.points)):
                        if i.points[i2].select==True:
                            temp.append (i2)
                            temppos.append (copy.copy(i.points[i2].co))
                self.selection.append(temp)
                self.selectionpos.append(temppos) 
        #初始化坐标位置
    #----------------------------------------------------------------------------------------------------------
    def invoke(self, context, event):
        if context.space_data.type == 'VIEW_3D':
            self.cc_xuanzhe_shuaxing (context)
            if len(self.selection)>0:
                context.window_manager.modal_handler_add(self)
                context.window.cursor_set('SCROLL_XY')
                if context.scene.cxl_snaptoggle == True :
                    cc_shuaxing_shikou_dingdian()
                return {'RUNNING_MODAL'} 
            else: 
                self.report({'WARNING'}, "请选择对象")
                return {'CANCELLED'}  
        else:
            self.report({'WARNING'}, "请在3D视图操作")
            return {'CANCELLED'}  
    #如果不是3D视口就结束
#----------------------------
class cxl_snap_shuaxing (bpy.types.Operator):#手动刷新捕捉点数据
    bl_idname = "view3d.cxl_snap_shuaxing"  #名称不能有大写
    bl_label = "刷新捕捉数据"

    def execute(self,context):        
        cc_shuaxing_shikou_dingdian()
        return {'FINISHED'}   
    
#-----------------------------
class cxl_convert_to_mesh (bpy.types.Operator): # 转换为网格对象
    bl_idname = "view3d.cxl_convert_obj_to_mesh"  #名称不能有大写
    bl_label = "转换为网格"

    def execute(self,context):        
        selection=[i for i in bpy.context.selected_objects if i.type in ['CURVE','MESH'] ]
        if len(selection) != 0 :
            newobj=[]
            depsgraph = bpy.context.evaluated_depsgraph_get()
            needdeleteobj=[]
            for i in selection:
                evaluated_object=i.evaluated_get(depsgraph)
                tempdata=bpy.data.meshes.new_from_object(evaluated_object, depsgraph=depsgraph)
                tempobjcet=bpy.data.objects.new (('C_Mesh'+cxl_namebytime()),tempdata)
                bpy.context.scene.collection.objects.link(tempobjcet)
                tempobjcet.location=i.location
                tempobjcet.rotation_euler=i.rotation_euler
                tempobjcet.scale=i.scale
                newobj.append(tempobjcet)
                needdeleteobj.append(i)
            for i in  needdeleteobj :
                bpy.data.objects.remove(i)
            cxl_clean_selection()
            cxl_select(newobj) 
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)#应用缩放 
        return {'FINISHED'}   
    
    
