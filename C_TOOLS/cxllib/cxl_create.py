
#互交式创建对象 -23.10.26 创建
#23.12.23 画线时添加按shift正交 添加退格键后退 修改bug
#24.01.03增加对捕捉开关 正交视图归零的支持
#------------------------------------------------------------
import bpy
import time
import random
import mathutils
from mathutils import Vector
from .cxl import cc_shuaxing_shikou_dingdian,cc_shuaxing_shikou_dingdian_2d,cxl_snaptopoint ,cxl_getapoint,cxl_shizixingyichu,cxl_shizixing,cxl3dto2d,cc_create_rectangle,\
    cc_change_shape,cc_newline,cc_point_to_top,cc_newbox,cc_shuaxing_shikou_dingdian,cc_jisuanzhongxingdian,distance,cc_point_top_to_view,cc_huoquliangdianjiaodu,cc_obj_rorate_to_view,\
    cc_huoquliangdiansuofang

#----------------------------------------------
 #用于存储数据
#---------------------------------------------- 
class cxl_create_box (bpy.types.Operator):#创建立方体
    bl_idname = "view3d.cxl_create_box"  #名称不能有大写
    bl_label = "create_box"

    pointa=None
    pointb=None
    pointc=None
    cc_box =None
    shubiao=0
    shikoushuaxing=False
    snapshuaxing=False

    def modal(self, context, event):
        cxl_snaptoggle =context.scene.cxl_snaptoggle#捕捉
        if event.type == 'MOUSEMOVE':
            if self.shikoushuaxing==True:cc_shuaxing_shikou_dingdian_2d() ; self.shikoushuaxing=False #视口刷新操作不能放在滚轮处  那相当于先刷新 后移动视口 
            if self.snapshuaxing==True:cc_shuaxing_shikou_dingdian() ; self.snapshuaxing=False
            if cxl_snaptoggle ==True :
                temp=cxl_snaptopoint(event)
                if temp ==None :temp=cxl_getapoint(event)
            else:
                temp=cxl_getapoint(event)
            cxl_shizixingyichu() #---先移除现有的十字星
            if  temp !=None:
                if cxl_snaptoggle ==True :cxl_shizixing(cxl3dto2d(temp))
                 #先显示捕捉的点
                if self.shubiao==1:
                    self.pointb=temp
                    if self.pointa !=None:
                        if self.cc_box != None:
                            self.pointb=cc_point_to_top(self.pointb)#顶点转换到顶视图
                            self.pointb[2]=self.pointa[2]
                            coords_list=[self.pointa,[self.pointa[0],self.pointb[1],self.pointa[2]],self.pointb,[self.pointb[0],self.pointa[1],self.pointa[2]],
                                        self.pointa,[self.pointa[0],self.pointb[1],self.pointa[2]],self.pointb,[self.pointb[0],self.pointa[1],self.pointa[2]]]
                            #绘制过程中有重面的情况 ，
                            for i in range(8):
                                self.cc_box.data.vertices[i].co=coords_list[i]
                            #更新图形
                elif self.shubiao==2:
                    self.pointc=temp
                    if self.pointa !=None:
                        if self.cc_box != None:
                            self.pointc=cc_point_to_top(self.pointc)#顶点转换到顶视图
                            coords_list=[self.pointa,[self.pointa[0],self.pointb[1],self.pointa[2]],self.pointb,[self.pointb[0],self.pointa[1],self.pointa[2]],
                                        [self.pointa[0],self.pointa[1],self.pointc[2]],[self.pointa[0],self.pointb[1],self.pointc[2]],[self.pointb[0],self.pointb[1],self.pointc[2]],[self.pointb[0],self.pointa[1],self.pointc[2]]]
                            #绘制过程中有重面的情况 ，
                            for i in range(8):
                                self.cc_box.data.vertices[i].co=coords_list[i]
                            #更新图形
            return{'RUNNING_MODAL'} 
        elif event.type == 'LEFTMOUSE':
                cxl_shizixingyichu() #---先移除现有的十字星
                if event.value=='PRESS':
                    if self.shubiao==0:
                        if cxl_snaptoggle ==True :
                            self.pointa=cxl_snaptopoint(event)
                            if self.pointa ==None :self.pointa=cxl_getapoint(event)
                        else:
                            self.pointa=cxl_getapoint(event)
                        if self.pointa!=None:self.pointa=cc_point_to_top(self.pointa)
                        self.cc_box=cc_newbox()
                        self.shubiao+=1
                        return{'RUNNING_MODAL'}
                    elif self.shubiao==2:
                        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
                        context.window.cursor_set('DEFAULT')
                        bpy.ops.wm.tool_set_by_id(name="builtin.select_box")
                        self.shubiao=0
                        return {'CANCELLED'} #主循环
                else:
                    self.shubiao+=1
                    return{'RUNNING_MODAL'}
        elif event.type in {'RIGHTMOUSE', 'ESC'}:
            context.window.cursor_set('DEFAULT')
            cxl_shizixingyichu() #移除可能存在的辅助显示十字星
            bpy.ops.wm.tool_set_by_id(name="builtin.select_box")
            return {'CANCELLED'} #结束
        elif event.type in { 'WHEELUPMOUSE', 'WHEELDOWNMOUSE'}:
            self.shikoushuaxing=True
            return {'PASS_THROUGH'}#滚轮刷新坐标显示
        elif event.type == 'MIDDLEMOUSE':
            self.snapshuaxing=True
            return {'PASS_THROUGH'} #中键刷新视口坐标参数
        return {'PASS_THROUGH'}#其他继续
         #######鼠标操作循环
    def invoke(self, context, event):
        
        if context.space_data.type == 'VIEW_3D':
            if context.mode != 'OBJECT':bpy.ops.object.mode_set(mode='OBJECT')#暂时强制回到物体模式
            if context.scene.cxl_snaptoggle == True :cc_shuaxing_shikou_dingdian()
            context.window_manager.modal_handler_add(self)
            context.window.cursor_set('CROSSHAIR')
            return {'RUNNING_MODAL'}  
        else:
            self.report({'WARNING'}, "Active space must be a View3d")
            return {'CANCELLED'}  
    #如果不是3D视口就结束

#---------------------------------------------- 
class cxl_create_rectangle (bpy.types.Operator):#创建矩形
    bl_idname = "view3d.cxl_create_rectangle"  #名称不能有大写
    bl_label = "create_rectangle"

    pointa=None
    pointb=None
    cc_rectangle =None
    shikoushuaxing=False
    snapshuaxing=False

    def modal(self, context, event):
        cxl_snaptoggle =context.scene.cxl_snaptoggle#捕捉
        if event.type == 'MOUSEMOVE':
            if self.shikoushuaxing==True:cc_shuaxing_shikou_dingdian_2d() ; self.shikoushuaxing=False #视口刷新操作不能放在滚轮处  那相当于先刷新 后移动视口 
            if self.snapshuaxing==True:cc_shuaxing_shikou_dingdian() ; self.snapshuaxing=False
            if cxl_snaptoggle ==True :
                self.pointb=cxl_snaptopoint(event)
                if self.pointb ==None:self.pointb=cxl_getapoint(event)
            else:
                self.pointb=cxl_getapoint(event)
            cxl_shizixingyichu() #---先移除现有的十字星
            if  self.pointb !=None:
                if cxl_snaptoggle ==True :cxl_shizixing(cxl3dto2d(self.pointb))
                if self.pointa !=None:
                    
                    if self.cc_rectangle != None:
                        self.pointb=cc_point_to_top(self.pointb)#顶点转换到顶视图
                        self.pointb[2]=self.pointa[2]
                        coords_list=[self.pointa,[self.pointa[0],self.pointb[1],self.pointa[2]],self.pointb,[self.pointb[0],self.pointa[1],self.pointa[2]]]
                        cc_change_shape(self.cc_rectangle,0,coords_list)
                        #更新图形
            return{'RUNNING_MODAL'} 
        elif event.type == 'LEFTMOUSE':
                cxl_shizixingyichu() #---先移除现有的十字星
                if event.value=='PRESS':
                    if cxl_snaptoggle ==True :
                        self.pointa=cxl_snaptopoint(event)
                        if self.pointa==None :self.pointa=cxl_getapoint(event)
                    else:
                        self.pointa=cxl_getapoint(event)
                    if self.pointa!=None:self.pointa=cc_point_to_top(self.pointa)
                    self.cc_rectangle=cc_create_rectangle([0,0,0],[0,0,0])
                    return{'RUNNING_MODAL'}
                else:
                    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
                    context.window.cursor_set('DEFAULT')
                    bpy.ops.wm.tool_set_by_id(name="builtin.select_box")
                    return {'CANCELLED'} #主循环
        elif event.type in {'RIGHTMOUSE', 'ESC'}:
            context.window.cursor_set('DEFAULT')
            cxl_shizixingyichu() #移除可能存在的辅助显示十字星
            bpy.ops.wm.tool_set_by_id(name="builtin.select_box")
            return {'CANCELLED'} #结束
        elif event.type in { 'WHEELUPMOUSE', 'WHEELDOWNMOUSE'}:
            self.shikoushuaxing=True
            return {'PASS_THROUGH'}#滚轮刷新坐标显示
        elif event.type == 'MIDDLEMOUSE':
            self.snapshuaxing=True
            return {'PASS_THROUGH'} #中键刷新视口坐标参数
        return {'PASS_THROUGH'}#其他继续
         #######鼠标操作循环
    def invoke(self, context, event):
        if context.space_data.type == 'VIEW_3D':
            if context.mode != 'OBJECT':bpy.ops.object.mode_set(mode='OBJECT')#暂时强制回到物体模式
            if context.scene.cxl_snaptoggle == True :cc_shuaxing_shikou_dingdian()
            context.window_manager.modal_handler_add(self)
            context.window.cursor_set('CROSSHAIR')
            return {'RUNNING_MODAL'}  
        else:
            self.report({'WARNING'}, "Active space must be a View3d")
            return {'CANCELLED'}  
    #如果不是3D视口就结束

#  line  绘制中，按shift键正交绘制，esc 右键 结束绘制  双击鼠标左键结束并首尾闭合
class cxl_create_line (bpy.types.Operator):#创建线段
    bl_idname = "view3d.cxl_create_line"  #名称不能有大写
    bl_label = "create_line"

    points=[]
    pointa=None
    cc_lineobj=None
    shift=None
    shikoushuaxing=False
    snapshuaxing=False


    last_click_time=time.time()

    def modal(self, context, event):
        cxl_snaptoggle =context.scene.cxl_snaptoggle#捕捉
        if cxl_snaptoggle ==True :
            self.pointa=cxl_snaptopoint(event)
        if self.pointa==None :self.pointa=cxl_getapoint(event) 
        shizixingweizhi=cxl3dto2d(self.pointa) #捕捉点显示位置
        self.pointa=cc_point_to_top (self.pointa) #匹配视图  
        
        if self.shift==True and self.pointa !=None : #正交操作
             last=self.points[-1]
             lx=abs(self.pointa[0]-last[0])
             ly=abs(self.pointa[1]-last[1])
             lz=abs(self.pointa[2]-last[2])
             tempa=[lx,ly,lz]
             tempa.sort()
             if tempa[-1]==lx :
                 self.pointa[1]=last[1]
                 self.pointa[2]=last[2]
             elif tempa[-1]==ly :
                 self.pointa[0]=last[0]
                 self.pointa[2]=last[2]
             else:
                 self.pointa[0]=last[0]
                 self.pointa[1]=last[1]
        #------------------------------------------
        
        if event.type == 'MOUSEMOVE':
            if self.shikoushuaxing==True:cc_shuaxing_shikou_dingdian_2d() ; self.shikoushuaxing=False #视口刷新操作不能放在滚轮处  那相当于先刷新 后移动视口 
            if self.snapshuaxing==True:cc_shuaxing_shikou_dingdian() ; self.snapshuaxing=False
            cxl_shizixingyichu() #---先移除现有的十字星
            if  self.pointa !=None:
                if cxl_snaptoggle ==True : cxl_shizixing(shizixingweizhi)#显示捕捉点
                if self.cc_lineobj != None:
                    cc_change_shape(self.cc_lineobj,0,self.points + [self.pointa])
                    #更新图形
            return{'RUNNING_MODAL'} 
        elif event.type == 'LEFTMOUSE': #增加点
                cxl_shizixingyichu() #---先移除现有的十字星
                if event.value=='PRESS':
                    thetime=time.time()
                    if thetime-self.last_click_time <0.2:
                        #双击
                        if self.cc_lineobj != None:
                            temppointscount=len(self.points)
                            if temppointscount>1:
                                self.points.pop()#移除最后一个点
                            cc_change_shape(self.cc_lineobj,0,self.points)
                            self.cc_lineobj.data.splines[0].use_cyclic_u=True #闭合图形
                        context.window.cursor_set('DEFAULT')
                        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
                        bpy.ops.wm.tool_set_by_id(name="builtin.select_box")
                        return {'CANCELLED'} #结束
                    else:
                        if self.pointa !=None :
                            if self.cc_lineobj == None:
                                self.cc_lineobj=cc_newline()
                                self.points=[]#初始化新图形顶点集合  否则会延续上次形状
                            self.points.append(self.pointa)
                            cc_change_shape(self.cc_lineobj,0,self.points)
                    context.window.cursor_set('CROSSHAIR')
                    self.last_click_time=thetime
                    return {'RUNNING_MODAL'} #主循环
        elif event.type in {'RIGHTMOUSE', 'ESC'}:#结束
            context.window.cursor_set('DEFAULT')
            cxl_shizixingyichu() #移除可能存在的辅助显示十字星
            if self.cc_lineobj!=None :
                cc_change_shape(self.cc_lineobj,0,self.points)
            self.cc_lineobj=None
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
            bpy.ops.wm.tool_set_by_id(name="builtin.select_box")
            return {'CANCELLED'} #结束
        elif event.type =='BACK_SPACE': #后退
             if event.value=='PRESS':
                 temppointscount=len(self.points)
                 if temppointscount>1:
                     self.points.pop()
        elif event.type in {'LEFT_SHIFT','RIGHT_SHIFT'}: #正交开启
            if event.value=='PRESS':
                self.shift=True
            else:
                self.shift=False
            return {'RUNNING_MODAL'}
        elif event.type in { 'WHEELUPMOUSE', 'WHEELDOWNMOUSE'}:
            self.shikoushuaxing=True
            return {'PASS_THROUGH'}#滚轮刷新坐标显示
        elif event.type == 'MIDDLEMOUSE':
            self.snapshuaxing=True
            return {'PASS_THROUGH'} #中键刷新视口坐标参数
        
        return {'PASS_THROUGH'}#其他继续
         #######鼠标操作循环
    def invoke(self, context, event):
        if context.space_data.type == 'VIEW_3D':
            if context.mode != 'OBJECT':bpy.ops.object.mode_set(mode='OBJECT')#暂时强制回到物体模式
            if context.scene.cxl_snaptoggle == True :cc_shuaxing_shikou_dingdian()
            context.window_manager.modal_handler_add(self)
            context.window.cursor_set('CROSSHAIR')
            return {'RUNNING_MODAL'}  
        else:
            self.report({'WARNING'}, "Active space must be a View3d")
            return {'CANCELLED'}  
    #如果不是3D视口就结束
#------------------------------------------
class cxl_create_circle (bpy.types.Operator):#创建圆形
    bl_idname = "view3d.cxl_create_circle"  #名称不能有大写
    bl_label = "绘制圆形"

    pointa=None
    pointb=None
    cc_circle =None
    shikoushuaxing=False
    snapshuaxing=False
    mode=0

    def modal(self, context, event):
        cxl_snaptoggle =context.scene.cxl_snaptoggle#捕捉
        if event.type == 'MOUSEMOVE':
            if self.shikoushuaxing==True:cc_shuaxing_shikou_dingdian_2d() ; self.shikoushuaxing=False #视口刷新操作不能放在滚轮处  那相当于先刷新 后移动视口 
            if self.snapshuaxing==True:cc_shuaxing_shikou_dingdian() ; self.snapshuaxing=False
            if cxl_snaptoggle ==True :
                self.pointb=cxl_snaptopoint(event)
                if self.pointb ==None:self.pointb=cxl_getapoint(event)
            else:
                self.pointb=cxl_getapoint(event)
            cxl_shizixingyichu() #---先移除现有的十字星
            if  self.pointb !=None:
                if cxl_snaptoggle ==True :cxl_shizixing(cxl3dto2d(self.pointb))
                if self.pointa !=None:
                    
                    if self.cc_circle != None:
                        self.pointa=cc_point_to_top(self.pointa)#顶点转换到顶视图
                        self.pointb=cc_point_to_top(self.pointb)#顶点转换到顶视图
                        self.pointb[2]=self.pointa[2]
                        #--------------------------------
                        jiaodu=cc_huoquliangdianjiaodu(self.pointa,self.pointb) #获取角度

                        self.pointa= cc_point_top_to_view(self.pointa);self.pointb= cc_point_top_to_view(self.pointb) #转换视图
                        if self.mode==0: #两点画圆
                            self.cc_circle.location=(cc_jisuanzhongxingdian([self.pointa,self.pointb]))
                            thescale=distance(self.pointa,self.pointb)/2
                            self.cc_circle.scale = [thescale,thescale,thescale]
                            self.cc_circle.rotation_euler=jiaodu
                        if self.mode==1: #中心画圆
                            self.cc_circle.location=self.pointa
                            thescale=distance(self.pointa,self.pointb)
                            self.cc_circle.scale = [thescale,thescale,thescale]
                            self.cc_circle.rotation_euler=jiaodu
                        #-----这个角度始终有点问题
                        #更新图形
            return{'RUNNING_MODAL'} 
        elif event.type == 'LEFTMOUSE':
                cxl_shizixingyichu() #---先移除现有的十字星
                if event.value=='PRESS':
                    if cxl_snaptoggle ==True :
                        self.pointa=cxl_snaptopoint(event)
                        if self.pointa==None :self.pointa=cxl_getapoint(event)
                    else:
                        self.pointa=cxl_getapoint(event)
                    bpy.ops.curve.primitive_bezier_circle_add()
                    self.cc_circle=bpy.context.selected_objects[0]
                    self.cc_circle.scale=[0,0,0] #可以让创建时的闪烁没那么明显
                    return{'RUNNING_MODAL'}
                else:
                    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)#应用缩放
                    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
                    context.window.cursor_set('DEFAULT')
                    bpy.ops.wm.tool_set_by_id(name="builtin.select_box")
                    return {'CANCELLED'} #主循环
        elif event.type in {'RIGHTMOUSE', 'ESC'}:
            context.window.cursor_set('DEFAULT')
            cxl_shizixingyichu() #移除可能存在的辅助显示十字星
            bpy.ops.wm.tool_set_by_id(name="builtin.select_box")
            return {'CANCELLED'} #结束
        elif event.type in { 'WHEELUPMOUSE', 'WHEELDOWNMOUSE'}:
            self.shikoushuaxing=True
            return {'PASS_THROUGH'}#滚轮刷新坐标显示
        elif event.type == 'MIDDLEMOUSE':
            self.snapshuaxing=True
            return {'PASS_THROUGH'} #中键刷新视口坐标参数
        elif event.type == 'M':#按M键切换模式
            if event.value=='PRESS':
                self.mode = self.mode + 1
                if self.mode>=2: #循环变化
                    self.mode=0
            return {'PASS_THROUGH'} #中键刷新视口坐标参数
        return {'PASS_THROUGH'}#其他继续
         #######鼠标操作循环
    def invoke(self, context, event):
        if context.space_data.type == 'VIEW_3D':
            if context.mode != 'OBJECT':bpy.ops.object.mode_set(mode='OBJECT')#暂时强制回到物体模式
            if context.scene.cxl_snaptoggle == True :cc_shuaxing_shikou_dingdian()
            context.window_manager.modal_handler_add(self)
            context.window.cursor_set('CROSSHAIR')
            return {'RUNNING_MODAL'}  
        else:
            self.report({'WARNING'}, "Active space must be a View3d")
            return {'CANCELLED'}  
    #如果不是3D视口就结束

#------------------------------------------


class cxl_create_sphere (bpy.types.Operator):#创建球体
    bl_idname = "view3d.cxl_create_sphere"  #名称不能有大写
    bl_label = "绘制球体"

    pointa=None
    pointb=None
    cc_sphere =None
    shikoushuaxing=False
    snapshuaxing=False
    mode=0

    def modal(self, context, event):
        cxl_snaptoggle =context.scene.cxl_snaptoggle#捕捉
        if event.type == 'MOUSEMOVE':
            if self.shikoushuaxing==True:cc_shuaxing_shikou_dingdian_2d() ; self.shikoushuaxing=False #视口刷新操作不能放在滚轮处  那相当于先刷新 后移动视口 
            if self.snapshuaxing==True:cc_shuaxing_shikou_dingdian() ; self.snapshuaxing=False
            if cxl_snaptoggle ==True :
                self.pointb=cxl_snaptopoint(event)
                if self.pointb ==None:self.pointb=cxl_getapoint(event)
            else:
                self.pointb=cxl_getapoint(event)
            cxl_shizixingyichu() #---先移除现有的十字星
            if  self.pointb !=None:
                if cxl_snaptoggle ==True :cxl_shizixing(cxl3dto2d(self.pointb))
                if self.pointa !=None:
                    
                    if self.cc_sphere != None:
                        self.pointa=cc_point_to_top(self.pointa)#顶点转换到顶视图
                        self.pointb=cc_point_to_top(self.pointb)#顶点转换到顶视图
                        self.pointb[2]=self.pointa[2]
                        #--------------------------------
                        jiaodu=cc_huoquliangdianjiaodu(self.pointa,self.pointb) #获取角度

                        self.pointa= cc_point_top_to_view(self.pointa);self.pointb= cc_point_top_to_view(self.pointb) #转换视图
                        if self.mode==0: #两点画圆
                            self.cc_sphere.location=(cc_jisuanzhongxingdian([self.pointa,self.pointb]))
                            thescale=distance(self.pointa,self.pointb)/2
                            self.cc_sphere.scale = [thescale,thescale,thescale]
                            self.cc_sphere.rotation_euler=jiaodu
                        if self.mode==1: #中心画圆
                            self.cc_sphere.location=self.pointa
                            thescale=distance(self.pointa,self.pointb)
                            self.cc_sphere.scale = [thescale,thescale,thescale]
                            self.cc_sphere.rotation_euler=jiaodu
                        #-----这个角度始终有点问题
                        #更新图形
            return{'RUNNING_MODAL'} 
        elif event.type == 'LEFTMOUSE':
                cxl_shizixingyichu() #---先移除现有的十字星
                if event.value=='PRESS':
                    if cxl_snaptoggle ==True :
                        self.pointa=cxl_snaptopoint(event)
                        if self.pointa==None :self.pointa=cxl_getapoint(event)
                    else:
                        self.pointa=cxl_getapoint(event)
                    bpy.ops.mesh.primitive_uv_sphere_add()
                    self.cc_sphere=bpy.context.selected_objects[0]
                    self.cc_sphere.scale=[0,0,0] #可以让创建时的闪烁没那么明显
                    return{'RUNNING_MODAL'}
                else:
                    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)#应用缩放
                    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
                    context.window.cursor_set('DEFAULT')
                    bpy.ops.wm.tool_set_by_id(name="builtin.select_box")
                    return {'CANCELLED'} #主循环
        elif event.type in {'RIGHTMOUSE', 'ESC'}:
            context.window.cursor_set('DEFAULT')
            cxl_shizixingyichu() #移除可能存在的辅助显示十字星
            bpy.ops.wm.tool_set_by_id(name="builtin.select_box")
            return {'CANCELLED'} #结束
        elif event.type in { 'WHEELUPMOUSE', 'WHEELDOWNMOUSE'}:
            self.shikoushuaxing=True
            return {'PASS_THROUGH'}#滚轮刷新坐标显示
        elif event.type == 'MIDDLEMOUSE':
            self.snapshuaxing=True
            return {'PASS_THROUGH'} #中键刷新视口坐标参数
        elif event.type == 'M':#按M键切换模式
            if event.value=='PRESS':
                self.mode = self.mode + 1
                if self.mode>=2: #循环变化
                    self.mode=0
            return {'PASS_THROUGH'} #中键刷新视口坐标参数
        return {'PASS_THROUGH'}#其他继续
         #######鼠标操作循环
    def invoke(self, context, event):
        if context.space_data.type == 'VIEW_3D':
            if context.mode != 'OBJECT':bpy.ops.object.mode_set(mode='OBJECT')#暂时强制回到物体模式
            if context.scene.cxl_snaptoggle == True :cc_shuaxing_shikou_dingdian()
            context.window_manager.modal_handler_add(self)
            context.window.cursor_set('CROSSHAIR')
            return {'RUNNING_MODAL'}  
        else:
            self.report({'WARNING'}, "Active space must be a View3d")
            return {'CANCELLED'}  
    #如果不是3D视口就结束


#--------------------------------------------
class cxl_create_plane (bpy.types.Operator):#创建平面
    bl_idname = "view3d.cxl_create_plane"  #名称不能有大写
    bl_label = "绘制平面"

    pointa=None
    pointb=None
    cc_plane =None
    shikoushuaxing=False
    snapshuaxing=False

    def modal(self, context, event):
        cxl_snaptoggle =context.scene.cxl_snaptoggle#捕捉
        if event.type == 'MOUSEMOVE':
            if self.shikoushuaxing==True:cc_shuaxing_shikou_dingdian_2d() ; self.shikoushuaxing=False #视口刷新操作不能放在滚轮处  那相当于先刷新 后移动视口 
            if self.snapshuaxing==True:cc_shuaxing_shikou_dingdian() ; self.snapshuaxing=False
            if cxl_snaptoggle ==True :
                self.pointb=cxl_snaptopoint(event)
                if self.pointb ==None:self.pointb=cxl_getapoint(event)
            else:
                self.pointb=cxl_getapoint(event)
            cxl_shizixingyichu() #---先移除现有的十字星
            if  self.pointb !=None:
                if cxl_snaptoggle ==True :cxl_shizixing(cxl3dto2d(self.pointb))
                if self.pointa !=None:
                    
                    if self.cc_plane != None:
                        self.pointa=cc_point_to_top(self.pointa)#顶点转换到顶视图
                        self.pointb=cc_point_to_top(self.pointb)#顶点转换到顶视图
                        self.pointb[2]=self.pointa[2]
                        #--------------------------------
                        self.pointa= cc_point_top_to_view(self.pointa);self.pointb= cc_point_top_to_view(self.pointb) #转换视图
     
                        self.cc_plane.location=(cc_jisuanzhongxingdian([self.pointa,self.pointb]))
                        thesuofang=cc_huoquliangdiansuofang(self.pointa,self.pointb,2)
                        self.cc_plane.scale = thesuofang
                        #-----这个角度始终有点问题
                        #更新图形
            return{'RUNNING_MODAL'} 
        elif event.type == 'LEFTMOUSE':
                cxl_shizixingyichu() #---先移除现有的十字星
                if event.value=='PRESS':
                    if cxl_snaptoggle ==True :
                        self.pointa=cxl_snaptopoint(event)
                        if self.pointa==None :self.pointa=cxl_getapoint(event)
                    else:
                        self.pointa=cxl_getapoint(event)
                    bpy.ops.mesh.primitive_plane_add()
                    self.cc_plane=bpy.context.selected_objects[0]
                    self.cc_plane.scale=[0,0,0] #可以让创建时的闪烁没那么明显
                    cc_obj_rorate_to_view(self.cc_plane)
                    return{'RUNNING_MODAL'}
                else:
                    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)#应用缩放
                    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
                    context.window.cursor_set('DEFAULT')
                    bpy.ops.wm.tool_set_by_id(name="builtin.select_box")
                    return {'CANCELLED'} #主循环
        elif event.type in {'RIGHTMOUSE', 'ESC'}:
            context.window.cursor_set('DEFAULT')
            cxl_shizixingyichu() #移除可能存在的辅助显示十字星
            bpy.ops.wm.tool_set_by_id(name="builtin.select_box")
            return {'CANCELLED'} #结束
        elif event.type in { 'WHEELUPMOUSE', 'WHEELDOWNMOUSE'}:
            self.shikoushuaxing=True
            return {'PASS_THROUGH'}#滚轮刷新坐标显示
        elif event.type == 'MIDDLEMOUSE':
            self.snapshuaxing=True
            return {'PASS_THROUGH'} #中键刷新视口坐标参数
        elif event.type == 'M':#按M键切换模式
            if event.value=='PRESS':
                self.mode = self.mode + 1
                if self.mode>=2: #循环变化
                    self.mode=0
            return {'PASS_THROUGH'} #中键刷新视口坐标参数
        return {'PASS_THROUGH'}#其他继续
         #######鼠标操作循环
    def invoke(self, context, event):
        if context.space_data.type == 'VIEW_3D':
            if context.mode != 'OBJECT':bpy.ops.object.mode_set(mode='OBJECT')#暂时强制回到物体模式
            if context.scene.cxl_snaptoggle == True :cc_shuaxing_shikou_dingdian()
            context.window_manager.modal_handler_add(self)
            context.window.cursor_set('CROSSHAIR')
            return {'RUNNING_MODAL'}  
        else:
            self.report({'WARNING'}, "Active space must be a View3d")
            return {'CANCELLED'}  
    #如果不是3D视口就结束
