#---通用代码库
#240104加入获取插件目录
#241126 修改捕捉  加入过滤顶点过多对象 并可以自由调整该数值


import bpy
import bpy_extras
from bpy_extras import view3d_utils
import gpu
from gpu_extras.batch import batch_for_shader
import mathutils
from mathutils import Vector
import math
import os
import random
import bmesh

def cxl_jia (lista,listb): #数组相加
    if type(lista)==list:tempa=lista
    else:tempa=list(lista)
    if type (listb) == list:tempb=listb
    else:tempb=list(listb)
    #防止传送元组无法操作，将其转化为数组
    xiangcha=len(tempa)-len(tempb)
    if xiangcha>0:
        for i in range(xiangcha):tempb.append(0)
    elif xiangcha < 0 :
        for i in range(abs(xiangcha)):tempa.append(0)
        #若有数组数量不同 将其补足
    tempc=[]
    for i in range(len(tempa)):
        tempc.append(tempa[i]+tempb[i])
    return (tempc)
#----------------------------------------------     
def cxl_jian (lista,listb): #数组相减
    if type(lista)==list:tempa=lista
    else:tempa=list(lista)
    if type (listb) == list:tempb=listb
    else:tempb=list(listb)
    #防止传送元组无法操作，将其转化为数组
    xiangcha=len(tempa)-len(tempb)
    if xiangcha>0:
        for i in range(xiangcha):tempb.append(0)
    elif xiangcha < 0 :
        for i in range(abs(xiangcha)):tempa.append(0)
        #若有数组数量不同 将其补足
    tempc=[]
    for i in range(len(tempa)):
        tempc.append(tempa[i]-tempb[i])
    return (tempc)
#---------------------------------------------- 
def cxl_chen (lista,listb): #数组相乘
    if type(lista)==list:tempa=lista
    else:tempa=list(lista)
    if type (listb) == list:tempb=listb
    else:tempb=list(listb)
    #防止传送元组无法操作，将其转化为数组
    xiangcha=len(tempa)-len(tempb)
    if xiangcha>0:
        for i in range(xiangcha):tempb.append(0)
    elif xiangcha < 0 :
        for i in range(abs(xiangcha)):tempa.append(0)
        #若有数组数量不同 将其补足
    tempc=[]
    for i in range(len(tempa)):
        tempc.append(tempa[i]*tempb[i])
    return (tempc)
#----------------------------------------------  
def cxl_chu (lista,listb): #数组相除
    if type(lista)==list:tempa=lista
    else:tempa=list(lista)
    if type (listb) == list:tempb=listb
    else:tempb=list(listb)
    #防止传送元组无法操作，将其转化为数组
    xiangcha=len(tempa)-len(tempb)
    if xiangcha>0:
        for i in range(xiangcha):tempb.append(0)
    elif xiangcha < 0 :
        for i in range(abs(xiangcha)):tempa.append(0)
        #若有数组数量不同 将其补足
    tempc=[]
    for i in range(len(tempa)):
        tempc.append(tempa[i]/tempb[i])
    return (tempc)
#---------------------------------------------- 
def cc_objec_color ():
    colors=[[156,156,156,1.0],[242,202,202,1.0],[243,220,202,1.0],[243,236,202,1.0],[236,243,202,1.0],[220,243,202,1.0],[202,243,202,1.0],\
            [202,243,220,1.0],[202,243,236,1.0],[203,236,243,1.0],[203,221,243,1.0],[203,203,243,1.0],[220,204,243,1.0],[235,203,243,1.0],\
            [243,203,236,1.0],[243,202,220,1.0],[243,210,236,1.0],[241,156,156,1.0],[241,196,157,1.0],[241,228,157,1.0],[228,241,157,1.0],\
            [196,241,157,1.0],[157,241,157,1.0],[157,241,196,1.0],[157,241,228,1.0],[157,228,241,1.0],[157,197,241,1.0],[157,157,241,1.0],\
            [194,157,241,1.0],[227,157,241,1.0],[241,157,228,1.0],[241,157,196,1.0],[236,243,210,1.0],[216,90,90,1.0],[216,157,92,1.0],\
            [216,199,92,1.0],[199,216,92,1.0],[157,216,92,1.0],[92,216,92,1.0],[92,216,157,1.0],[92,516,199,1.0],[93,200,216,1.0],[93,158,216,1.0],\
            [93,93,216,1.0],[155,93,216,1.0],[198,93,216,1.0],[216,93,200,1.0],[216,92,157,1.0],[210,243,243,1.0],[191,46,46,1.0],[191,131,53,1.0],\
            [191,174,53,1.0],[176,191,46,1.0],[133,191,46,1.0],[46,191,46,1.0],[46,191,130,1.0],[46,191,176,1.0],[53,174,191,1.0],[53,133,193,1.0],\
            [53,53,192,1.0],[129,53,192,1.0],[173,53,192,1.0],[193,53,174,1.0],[195,49,130,1.0]
            ]
    
    col=random.choice(colors)
    col=cxl_chu(col,[250,250,250,1])
    return(col)
#----------------------------------------------
def cxl_randomcolor ():#获取一个随机颜色
            temp=[]
            for i in range(3):
                rgb=random.random()
                temp.append(rgb)
            temp.append(1.0)
            return (temp)
#----------------------------------------------
def cc_user_addon_path():#获取用户插件目录
    addon_path = bpy.utils.resource_path("USER")
    plugins_directory = os.path.join(addon_path, "scripts", "addons")
    return plugins_directory
#----------------------------------------------
def cc_snapstate_set(zhouxiang):#轴向控制调用
    bpy.context.scene.cxl_snap_state=zhouxiang
#----------------------------------------------
def cc_snaptoggle ():#--捕捉开关调用
    if bpy.context.scene.cxl_snaptoggle ==True:
       bpy.context.scene.cxl_snaptoggle=False
    else:
        bpy.context.scene.cxl_snaptoggle=True
#----------------------------------------------
cxl_snap_radius=50
cxl_snapobject_radius=1000
cxlshizi=[]
#-----------------------------------------------------------
def cxl_hqsbpmzb(event):  #获取鼠标位置
     coord = [event.mouse_region_x, event.mouse_region_y]
     return (coord)
#----------------------------------------------
def cxlgetv3dregion(): # 获取三维工作区   
    workarea=bpy.context.window_manager.windows[0].screen.areas
    for i in workarea :
        if i.type=='VIEW_3D':#找到三维区域
            temp=i.regions
            for i2 in temp :
                if i2.type=='WINDOW':
                    return i2 #找到工作窗口
#----------------------------------------------
def cxl_shizixingyichu ():#十字星移除
        global cxlshizi
        for i in range(len(cxlshizi)) : # 直接用i 会在一些情况下出错
            ii=cxlshizi[0]
            ii[0].draw_handler_remove(ii[1],'WINDOW')
            cxlshizi.remove (ii)
            Update3DViewPorts()
#----------------------------------------------        
def Update3DViewPorts():#--3d视口更新
    for area in bpy.context.window.screen.areas:
        if area.type == 'VIEW_3D':
            area.tag_redraw()
#----------------------------------------------
def cxl_shizixing (screenvert): #再视口中的某个点上显示一个十字星
    if screenvert!=None :
        shizixingdaxiao=10.0
        tempx=screenvert[0]
        tempy=screenvert[1]
        vertices = ((tempx-shizixingdaxiao, tempy), (tempx+shizixingdaxiao, tempy),(tempx, tempy-shizixingdaxiao), (tempx, tempy+shizixingdaxiao))
        indices = ((0, 1 ), ( 2, 3))
        shader = gpu.shader.from_builtin('UNIFORM_COLOR')
        batch = batch_for_shader(shader, 'LINES', {"pos": vertices}, indices=indices)
        def drawshizixing():
            shader.bind()
            shader.uniform_float("color", (0.3, 1, 1,1))
            batch.draw(shader)
        thespace=bpy.context.space_data
        if thespace.type=='VIEW_3D':
            cxlline_shizixing=thespace.draw_handler_add(drawshizixing, (), 'WINDOW', 'POST_PIXEL')
            global cxlshizi
            cxlshizi.append([thespace,cxlline_shizixing])
            Update3DViewPorts()
#----------------------------------------------
def cxl2dto3d(coord):#将屏幕坐标投射到三维-
    viewport=bpy.context.region
    thespace=bpy.context.space_data
    if thespace.type=='VIEW_3D':
        rv3d=thespace.region_3d
        viewdirection =bpy_extras.view3d_utils.region_2d_to_vector_3d(viewport,rv3d,coord)
        the3d = bpy_extras.view3d_utils.region_2d_to_location_3d(viewport,rv3d,coord,viewdirection)
        return (the3d)
    else :
        return(None)
#----------------------------------------------
def cxl3dto2d(coord):#将视口中三维点投影到屏幕
    viewport=bpy.context.region 
    thespace=bpy.context.space_data   
    if thespace.type=='VIEW_3D':
        rv3d=thespace.region_3d
        the2d = bpy_extras.view3d_utils.location_3d_to_region_2d(viewport, rv3d, coord,default=None)
        return (the2d)
    else :
        return(None)  
#----------------------------------------------
def cxlshikoupanduan():#判断当前视口处于什么视图
    #判断视口再哪个视图中
    point=cxl2dto3d((10,10))
    if point[2]==-1.0000:
        return "top"
    elif point[2]==1.0000:
        return "bottom"
    elif point[1]==1.0000:
        return "front"
    elif point[1]==-1.0000:
        return "back"
    elif point[0]==-1.0000:
        return "right"
    elif point[0]==1.0000:
        return "left"
    else:
        return "user"
#----------------------------------------------
def cc_move_xyz (pointa,pointb):#捕捉轴向修改
    cxl_snap_state = bpy.context.scene.cxl_snap_state
    temp=[0,0,0]
    shikou=cxlshikoupanduan()
    if cxl_snap_state=='X':
        if shikou in ["front","back","user","top","bottom"]:temp=[pointb[0],pointa[1],pointa[2]]
        elif shikou in ["right","left"]:temp=[pointa[0],pointb[1],pointa[2]]
    elif cxl_snap_state =='Y':
        if shikou in ["top","bottom","user"]:temp=[pointa[0],pointb[1],pointa[2]]
        elif shikou in ["front","back","right","left"]:temp=[pointa[0],pointa[1],pointb[2]]
    elif cxl_snap_state == 'Z':
        if shikou in ["user"]:temp=[pointa[0],pointa[1],pointb[2]]
        else:temp=pointa
    elif cxl_snap_state =='XY':
        if shikou in ["top","bottom","user"]:temp=[pointb[0],pointb[1],pointa[2]]
        elif shikou in ["front","back"]:temp=[pointb[0],pointa[1],pointb[2]]
        else:temp=[pointa[0],pointb[1],pointb[2]]
        
    else:
        temp=pointb
    return(temp)  
#----------------------------------------------
def cc_point_to_top (ccpoint):#将其他视图顶点位置转换到顶视图
    shikou=cxlshikoupanduan()
    if shikou == "front":
        return([ccpoint[0],ccpoint[2],-ccpoint[1]])
    elif shikou== "bottom":
        return([ccpoint[0],-ccpoint[1],-ccpoint[2]])
    elif shikou== "back":
        return([-ccpoint[0],ccpoint[2],ccpoint[1]])
    elif shikou== "right":
        return([ccpoint[1],ccpoint[2],ccpoint[0]])
    elif shikou== "left":
        return([-ccpoint[1],ccpoint[2],-ccpoint[0]])
    else:
        return([ccpoint[0],ccpoint[1],ccpoint[2]])
#----------------------------------------------
def cc_point_top_to_view (ccpoint): #将从顶视图计算而来的顶点数据转回当前视图 
    shikou=cxlshikoupanduan()
    if shikou == "front":
        return([ccpoint[0],-ccpoint[2],ccpoint[1]])
    elif shikou== "bottom":
        return([ccpoint[0],-ccpoint[1],-ccpoint[2]])
    elif shikou== "back":
        return([-ccpoint[0],ccpoint[2],ccpoint[1]])
    elif shikou== "right":
        return([ccpoint[2],ccpoint[0],ccpoint[1]])
    elif shikou== "left":
        return([-ccpoint[2],-ccpoint[0],ccpoint[1]])
    else:
        return([ccpoint[0],ccpoint[1],ccpoint[2]])
#---------------------------------------------- 
def cc_obj_rorate_to_view (obj):#将对象的默认旋转属性调整至视口
    shikou=cxlshikoupanduan()
    if shikou == "front":
        obj.rotation_euler=mathutils.Euler((1.5707963, 0.0, 0.0), 'XYZ')
    elif shikou == "bottom":
        obj.rotation_euler=mathutils.Euler((3.1415927, 0.0, 0.0), 'XYZ')
    elif shikou == "back":
        obj.rotation_euler=mathutils.Euler((4.7123889, 3.1415927, 0.0), 'XYZ')
    elif shikou == "right":
        obj.rotation_euler=mathutils.Euler((4.7123889, 3.1415927, -1.5707963), 'XYZ')
    elif shikou == "left":
        obj.rotation_euler=mathutils.Euler((4.7123889, 3.1415927, -4.7123889), 'XYZ')
    else:
        obj.rotation_euler=mathutils.Euler((0.0, 0.0, 0.0), 'XYZ')
    # 需要将新建顶点转换到的顶视图
#----------------------------------------------
def cc_shikou_z_o (ccpoint): #根据视口将顶点Z轴归零
    shikou=cxlshikoupanduan()
    if shikou == "top":
        return([ccpoint[0],ccpoint[1],0])
    elif shikou == "front":
        return([ccpoint[0],0,ccpoint[2]])
    elif shikou== "bottom":
        return([ccpoint[0],ccpoint[1],0])
    elif shikou== "back":
        return([ccpoint[0],0,ccpoint[2]])
    elif shikou== "right":
        return([0,ccpoint[1],ccpoint[2]])
    elif shikou== "left":
        return([0,ccpoint[1],ccpoint[2]])
    else:
        return([ccpoint[0],ccpoint[1],ccpoint[2]])
def distance(point1, point2): # 三维点测距
    #-------------计算两点间的距离
    """Calculate distance between two points in 3D."""
    return math.sqrt((point2[0] - point1[0]) ** 2 +
                     (point2[1] - point1[1]) ** 2 +
                     (point2[2] - point1[2]) ** 2)
#----------------------------------------------
def distance2d(point1, point2): #二维点测距
    #-------------计算两点间的距离
    """Calculate distance between two points in 2D."""
    return math.sqrt((point2[0] - point1[0]) ** 2 +
                     (point2[1] - point1[1]) ** 2 )
#----------------------------------------------

def cxlshikoudx(): #获取视口大小
    #获取视口再三维空间中的最小点和最大点-------------------
    workarea=bpy.context.window_manager.windows[0].screen.areas
    for i in workarea :
        if i.type=='VIEW_3D':#找到三维区域
            temp=i.regions
            for i2 in temp :
                if i2.type=='WINDOW':
                    viewport=i2 #找到工作窗口
    pointa=[0,0]
    pointb=[viewport.width,viewport.height]
    return((pointa,pointb))
#----------------------------------------------
#----------------------------------------------

def cxlzuijijngdian(lista,point): #找到数组中距离点最近的点序列编号 lista 为二维点集合  point 二维点
    js=0
    cd=10000000000
    for i in range(len(lista)):
        jl=distance2d(lista[i],point)
        if jl < cd:
            cd=jl
            js=i
    return(js)
#----------------------------------------------
#----------------------------------------------
def cxl_getapoint(event): # 获取鼠标位置三维坐标  无捕捉
    mousecoord = event.mouse_region_x, event.mouse_region_y #区域坐标
    temp=cxl2dto3d(mousecoord)
    if temp != None:
        temp=cc_shikou_z_o(temp)
    return (temp)
#----------------------------------------------

# #----------------------------------------------
cxl_shikoudingdian=[]
cxl_shikoudingdian_2d=[]

def cc_shuaxing_shikou_dingdian_2d ():
    global cxl_shikoudingdian
    global cxl_shikoudingdian_2d
    cxl_shikoudingdian_2d=[cxl3dto2d(i) for i in cxl_shikoudingdian]
#----------
def cc_shuaxing_shikou_dingdian ():#获取视口中的顶点数据
    global cxl_shikoudingdian
    global cxl_shikoudingdian_2d
    cxl_shikoudingdian=[]
    cxl_shikoudingdian_2d=[] #初始化
    guolv=bpy.context.scene.snap_guolv

    objs=[]
    for obj in bpy.context.visible_objects :
        if obj.type=='CURVE':
            objs.append(obj)
        elif obj.type=='MESH' :
            if len(obj.data.vertices)<guolv:#过滤顶点过多的对象
                objs.append(obj)
    depsgraph = bpy.context.evaluated_depsgraph_get() #当前关系图 方便修改顶点获取
    for i in objs :
        imatrix=i.matrix_world
        evaluated_object=i.evaluated_get(depsgraph)
        tempdata=evaluated_object.to_mesh()
        if tempdata :
            thisobjverts=tempdata.vertices
            for i2 in thisobjverts:
                i2_co=imatrix @ i2.co
                i2_2d=cxl3dto2d(i2_co)
                if i2_2d !=None:
                    cxl_shikoudingdian.append(i2_co)#添加顶点绝对坐标
                    cxl_shikoudingdian_2d.append(i2_2d)
            for i3 in tempdata.edges:
                temp=i3.vertices
                temp_zd=(imatrix @ ((thisobjverts[temp[0]].co+thisobjverts[temp[1]].co)/2))
                temp_zd_2d=cxl3dto2d(temp_zd)
                if temp_zd_2d !=None:
                    cxl_shikoudingdian.append(temp_zd)#添加边中点
                    cxl_shikoudingdian_2d.append(temp_zd_2d)
#----------------------------------------------
def cxl_snaptopoint(event): #(视口顶点数据,鼠标事件) 获取距离鼠标位置最近的顶点 捕捉
    global cxl_shikoudingdian
    global cxl_shikoudingdian_2d
    global cxl_snap_radius
    zuijingdian=None
    mousecoord = event.mouse_region_x, event.mouse_region_y #区域坐标
    bh=cxlzuijijngdian(cxl_shikoudingdian_2d,mousecoord)#获取最近点的编号
    if len(cxl_shikoudingdian)!=0: 
        if  distance2d(cxl_shikoudingdian_2d[bh],mousecoord)<=cxl_snap_radius :
            zuijingdian=cxl_shikoudingdian[bh] #三维点
    if zuijingdian != None:
        zuijingdian=cc_shikou_z_o(zuijingdian)
    return(zuijingdian)
#---------------------------------------------- 
def cxl_namebytime(): #获取时间数据
    import datetime
    sjm=datetime.datetime.now().strftime('%y%m%d%H%M%S')
    return (sjm)
#----------------------------------------------
def cxl_clean_selection ():#清楚选择对象
    selection=bpy.context.selected_objects
    for i in selection:
        i.select_set(False)

def cxl_select (objects):
    for i in objects:
        i.select_set(True)
#---------------------------------------------- 
def cc_create_rectangle (pointa,pointb): #创建矩形  需提供两个坐标  
    pointb[2]=pointa[2] #以顶视图为基准 同化Z轴 后期其他视图均通过坐标转换获得 
    cc_coords_list=[pointa,[pointa[0],pointb[1],pointa[2]],pointb,[pointb[0],pointa[1],pointa[2]]]
    cc_pointnum=(len(cc_coords_list)) 
    cc_curve=bpy.data.curves.new ("rectangle",'CURVE')
    cc_curve.dimensions='3D'
    cc_spline=cc_curve.splines.new(type='BEZIER')
    cc_spline.bezier_points.add(cc_pointnum-1)
    cc_spline.use_cyclic_u =True
    for i in range(cc_pointnum) :
        cc_spline.bezier_points[i].co =cc_coords_list[i]
        cc_spline.bezier_points[i].handle_left_type='VECTOR'
        cc_spline.bezier_points[i].handle_right_type='VECTOR'
    cc_rectangle=bpy.data.objects.new (('rectangle'+cxl_namebytime()),cc_curve)
    bpy.context.scene.collection.objects.link(cc_rectangle)
    cxl_clean_selection ()
    cc_rectangle.select_set(True)
    bpy.context.view_layer.objects.active = cc_rectangle
    cc_obj_rorate_to_view(cc_rectangle)
    cc_rectangle.show_wire=True
    cc_rectangle.color=cc_objec_color()
    return (cc_rectangle)
#---------------------------------------------- 
def cc_newline (): #创建一个空的曲线 
    cc_curve=bpy.data.curves.new ("Line",'CURVE')
    cc_curve.dimensions='3D'
    cc_spline=cc_curve.splines.new(type='BEZIER')
    cc_spline.bezier_points[0].handle_left_type='VECTOR'
    cc_spline.bezier_points[0].handle_right_type='VECTOR'
    cc_spline.use_cyclic_u =False
    cc_line=bpy.data.objects.new (('Line'+cxl_namebytime()),cc_curve)
    bpy.context.scene.collection.objects.link(cc_line)
    cxl_clean_selection ()
    cc_line.select_set(True)
    bpy.context.view_layer.objects.active = cc_line
    cc_line.show_wire=True
    cc_line.color=cc_objec_color()
    cc_obj_rorate_to_view(cc_line)
    return (cc_line)
#----------------------------------------------
def cc_clean_shape_points_selected (shapeobject): #清除曲线对象顶点选中状态
    js=len(shapeobject.data.splines)
    for i in range(js):
        spvert=shapeobject.data.splines[i].bezier_points
        for i2 in spvert:
            i2.select_control_point=False
#----------------------------------------------
def cc_change_shape (shapeobject,sp_sn,vertlist): #对图像bezier顶点进行调整 图形对象 线条序号 顶点列表
    objvert=shapeobject.data.splines[sp_sn].bezier_points
    tempa=len(objvert)
    tempb=len(vertlist)
    chaju=tempb-tempa
    if chaju>0 :
        shapeobject.data.splines[sp_sn].bezier_points.add(chaju)
        for i in range(chaju):
            shapeobject.data.splines[sp_sn].bezier_points[tempa+i].handle_left_type='VECTOR'
            shapeobject.data.splines[sp_sn].bezier_points[tempa+i].handle_right_type='VECTOR'
    elif chaju<0 :
        cxl_clean_selection ()
        cc_clean_shape_points_selected(shapeobject)
        shapeobject.select_set(True)
        bpy.context.view_layer.objects.active = shapeobject
        bpy.ops.object.mode_set(mode='EDIT')
        for i in range(1,tempa):
            shapeobject.data.splines[sp_sn].bezier_points[i].select_control_point=True
        bpy.ops.curve.delete(type='VERT')
        bpy.ops.object.mode_set(mode='OBJECT')
        shapeobject.data.splines[sp_sn].bezier_points.add(tempb-1)
        for i in range(tempb) :
         shapeobject.data.splines[sp_sn].bezier_points[i].handle_left_type='VECTOR'
         shapeobject.data.splines[sp_sn].bezier_points[i].handle_right_type='VECTOR'
    objvert=shapeobject.data.splines[sp_sn].bezier_points
    js=0
    for i in vertlist:
        objvert[js].co=i
        js+=1
    #Update3DViewPorts()
#----------------------------------------------
def cc_jinggao (mystring):
     bpy.context.scene.cc_jinggao=mystring
     bpy.ops.cwindow.jinggao('INVOKE_DEFAULT')
#----------------------------------------------
def cc_newbox():#---创建一个立方体
    cxl_clean_selection ()
    cc_box=bpy.data.meshes.new(name=("Mesh"+cxl_namebytime()))
    cc_boxobj=bpy.data.objects.new (('Box'+cxl_namebytime()),cc_box)
    verts = [Vector((0,0,0)),Vector((0,1,0)),Vector((1,1,0)),Vector((1,0,0)),Vector((0,0,1)),Vector((0,1,1)),Vector((1,1,1)),Vector((1,0,1))]
    edges = []
    faces = [[0,1,2,3],[7,6,5,4],[3,7,4,0],[2,6,7,3],[1,5,6,2],[0,4,5,1]]
    cc_box.from_pydata(verts,edges,faces,shade_flat=True)
    bpy.context.scene.collection.objects.link(cc_boxobj)
    bpy.context.view_layer.objects.active = cc_boxobj
    cc_boxobj.select_set(True)
    cc_obj_rorate_to_view(cc_boxobj)
    cc_boxobj.show_wire=True
    cc_boxobj.color=cc_objec_color()
    return(cc_boxobj)
#----------------------------------------------
def cc_duixiangshiliang (duixiang):#获取对象Z朝向矢量
    shiliang=duixiang.matrix_world @ mathutils.Vector((0, 0, 1)) #@符号表示矩阵乘法 
    shiliang=shiliang-duixiang.location
    return(shiliang)
#----------------------------------------------
def cc_danweishipei (zhi): #  输入单位换算成系统显示单位
    danwei=bpy.context.scene.unit_settings.length_unit
    if danwei == 'MILLIMETERS':
        temp=zhi/1000
    elif danwei == 'KILOMETERS':
        temp=zhi*1000
    elif danwei=='CENTIMETERS':
        temp=zhi/100
    elif danwei == 'MICROMETERS':
        temp =zhi /1000000
    else:
        temp = zhi
    return (temp)
#----------------------------------------------
def c_huoqujianpanzhi (event): #获取输入数值
     if event.type in ['NUMPAD_0','ZERO']:
          return('0')
     elif event.type in ['NUMPAD_1','ONE']:
          return('1')
     elif event.type in ['NUMPAD_2','TWO']:
          return('2')
     elif event.type in ['NUMPAD_3','THREE']:
          return('3')
     elif event.type in ['NUMPAD_4','FOUR']:
          return('4')
     elif event.type in ['NUMPAD_5','FIVE']:
          return('5')
     elif event.type in ['NUMPAD_6','SIX']:
          return('6')
     elif event.type in ['NUMPAD_7','SEVEN']:
          return('7')
     elif event.type in ['NUMPAD_8','EIGHT']:
          return('8')
     elif event.type in ['NUMPAD_9','NINE']:
          return('9')
     elif event.type in ['NUMPAD_PERIOD','PERIOD']:
          return('.')
     elif event.type in ['MINUS','NUMPAD_MINUS']:
          return('-')

#-------------------------------
cxl_tishicaizhi = None
def cxl_tishicaizhi_get(): #获取一个提示材质
    global cxl_tishicaizhi
    new=False
    if cxl_tishicaizhi==None:
        new=True
    else:
        thecolor=[i for i in cxl_tishicaizhi.node_tree.nodes[0].inputs[0].default_value]
        if thecolor!=[1.0,0,0,1.0]:
            new=True
    if new==True:

        cxl_tishicaizhi=bpy.data.materials.new('c_mat_'+ cxl_namebytime())
        cxl_tishicaizhi.use_nodes=True
        shuxing=cxl_tishicaizhi.node_tree.nodes[0].inputs
        shuxing[0].default_value=(1.0,0,0,1.0)
    return(cxl_tishicaizhi)
#----------------------------------------
def cc_jisuanzhongxingdian(dianjihe):#计算中心点
    thex, zhey, zhez = 0.0, 0.0, 0.0
    num = len(dianjihe)
    for vertex in dianjihe:
        thex += vertex[0]
        zhey += vertex[1]
        zhez += vertex[2]
    zhongxingdian = (thex / num, zhey / num, zhez / num)
    return (zhongxingdian)
#----------------------------------
def cc_jisuanxuanzheduixiantijikuang(): #计算选中对象的体积块绝对值
    selection=bpy.context.selected_objects
    if len(selection)!=0:
        themax=[]
        themin=[]
        for i in selection:
            imatrix=i.matrix_world
            themax.append(imatrix @ i.dimensions)
            themin.append(imatrix @ mathutils.Vector([0,0,0]))
        maxx,maxy,maxz=[themax[0][0],themax[0][1],themax[0][2]]
        for i in themax:
            if i[0]>maxx:maxx=i[0]
            if i[1]>maxy:maxy=i[1]
            if i[2]>maxz:maxz=i[2]
        minx,miny,minz=[themin[0][0],themin[0][1],themin[0][2]]
        for i in themin:
            if i[0]<minx:minx=i[0]
            if i[1]<miny:miny=i[1]
            if i[2]<minz:minz=i[2]
        return([[maxx,maxy,maxz],[minx,miny,minz]])
    else:return([mathutils.Vector([0,0,0]),mathutils.Vector([0,0,0])])

def cc_jisuan_liangdian_jiaodu_2d(pointa,pointb): #计算两点间的角度
    dx = pointb[0] - pointa[0]
    dy = pointb[1] - pointa[1]
    angle_radians = math.atan2(dy, dx)
    return(angle_radians)

def cc_huoquliangdianjiaodu(pointa,pointb): #根据视口计算两点对应角度
    jiaodu=cc_jisuan_liangdian_jiaodu_2d(pointa,pointb)
    shikou=cxlshikoupanduan()
    if shikou == "top":
        return([0,0,jiaodu])
    elif shikou == "front":
        return([math.pi/2,-jiaodu,0])
    elif shikou== "bottom":
         return([math.pi,0,jiaodu])
    elif shikou== "back":
        return([3*math.pi/2,-jiaodu,0])
    elif shikou== "right":
        return([math.pi/2,-jiaodu,math.pi/2])
    elif shikou== "left":
        return([3*math.pi/2,jiaodu,math.pi/2])
    else:
        return([0,0,jiaodu])

#------------------------
def cc_huoquliangdiansuofang(pointa,pointb,cankaozhi): #根据视口计算两点对应缩放值
    thescalea=abs(pointb[0]-pointa[0])/cankaozhi
    thescaleb=abs(pointb[1]-pointa[1])/cankaozhi
    thescalec=abs(pointb[2]-pointa[2])/cankaozhi
    shikou=cxlshikoupanduan()
    if shikou == "top":
        return([thescalea,thescaleb,1])
    elif shikou == "front":
        return([thescalea,thescalec,1])
    elif shikou== "bottom":
         return([thescalea,thescaleb,1])
    elif shikou== "back":
        return([thescalea,thescalec,1])
    elif shikou== "right":
        return([thescaleb,thescalec,1])
    elif shikou== "left":
        return([thescaleb,thescalec,1])
    else:
        return([thescalea,thescaleb,1])
#------------------------

def cxl_obj_tex_image_shuxing_tianjia (obj): #为对象贴图添加UV属性
    mat=obj.active_material
    if mat :
        if mat.use_nodes==True:
            mat_node_tree=mat.node_tree
            mat_nodes=mat_node_tree.nodes
            mat_links=mat_node_tree.links
            mat_nodes_name=[i.name for i in mat_nodes ]
            new_location = [0,0]
            if 'c_uv_shuxing' not in mat_nodes_name:
                new_shuxing=mat_nodes.new('ShaderNodeAttribute')
                new_shuxing.name='c_uv_shuxing'
                new_shuxing.attribute_type = 'GEOMETRY'
                new_shuxing.attribute_name = "c_uv"
                mat_image=[]
                for i in mat_nodes :
                    if i.type=='TEX_IMAGE':mat_image.append(i)
                    if i.location[0]<new_location[0]:new_location[0]=i.location[0]
                    if i.location[1]<new_location[1]:new_location[1]=i.location[1]
                    new_location[0]= new_location[0]-120
                new_shuxing.location=new_location
                for i in mat_image:
                    mat_links.new(new_shuxing.outputs[1],i.inputs[0])



 

