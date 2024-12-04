#测试用
import bpy
import math
import mathutils
import copy
#---------------------------------------------
from .cxl import distance,cc_danweishipei
def cc_lianxuxingfenduan (thelist): #将列表数值进行连续性检查  并分段
    fenduan=[]
    temp=[]
    for i in thelist:
        if len(temp)==0 :
            temp.append(i)
        elif i-1 ==temp[-1]:
            temp.append(i)
        else:
            fenduan.append(temp)
            temp=[]
            temp.append(i)
    fenduan.append(temp)
    return(fenduan)
#---------------------------------------------------------------------
def cc_bezier_sp_fanzhuan (vertlist): #翻转bezier曲线点
    temparray=vertlist
    temparray.reverse()
    for i in temparray:
        ll=i[1];rr=i[2];lt=i[3];rt=i[4]
        i[1]=rr;i[2]=ll;i[3]=rt;i[4]=lt
    return(temparray)

def cc_huoqu_sp_verts (spline): #获取一个线条的顶点数据
    if spline.type=='BEZIER':
        verts=[[i.co,i.handle_left,i.handle_right,i.handle_left_type,i.handle_right_type,i.hide,i.radius,i.select_control_point,i.select_left_handle,i.select_right_handle,i.tilt,i.weight_softbody] for i in  spline.bezier_points]
    else:
        verts=[[i.co,i.hide,i.radius,i.select,i.tilt,i.weight,i.weight_softbody] for i in spline.points]
    return(verts)


def cc_gouzao_bezier_sp(obj,vertlist,sp_bihe):   #构造一条bezier曲线     
    newsp=obj.data.splines.new('BEZIER') 
    newspdiansu=len(vertlist)
    newsp.bezier_points.add(newspdiansu-1)
    newsp.use_cyclic_u = sp_bihe
    for i in range(newspdiansu):
        temp=newsp.bezier_points[i] 
        temp.co=vertlist[i][0];temp.handle_left=vertlist[i][1];temp.handle_right=vertlist[i][2];temp.handle_left_type=vertlist[i][3];temp.handle_right_type=vertlist[i][4]
        temp.hide=vertlist[i][5];temp.radius=vertlist[i][6];temp.select_control_point=vertlist[i][7];temp.select_left_handle=vertlist[i][8];temp.select_right_handle=vertlist[i][9]
        temp.tilt=vertlist[i][10];temp.weight_softbody=vertlist[i][11]
    return(newsp)

def cc_gouzao_sp (obj,vertlist,sp_bihe,thetype): #构造一条曲线  内型可以是 poly 或nurbs
    newsp=obj.data.splines.new(thetype)
    newspdiansu=len(vertlist)
    newsp.points.add(newspdiansu-1)
    newsp.use_cyclic_u = sp_bihe
    for i in range(newspdiansu):
        temp=newsp.points[i] 
        temp.co=vertlist[i][0];temp.hide=vertlist[i][1];temp.radius=vertlist[i][2];temp.select=vertlist[i][3];temp.tilt=vertlist[i][4];temp.weight=vertlist[i][5];temp.weight_softbody=vertlist[i][6]
    return(newsp)

#---------------------------------------------'''
def cc_weld_sp (obj) : #对曲线单条内选择顶点进行焊接
    needdeletesp=[]
    for thespline in obj.data.splines:
        yuzhi=cc_danweishipei(bpy.context.scene.cc_weld) #调整焊接单位
        if thespline.type=='BEZIER':
            points=thespline.bezier_points
            thevert=cc_huoqu_sp_verts(thespline)
            #信息收集
            sp_bihe = thespline.use_cyclic_u
            needdelete=[] ; pointsnum=len(points) ; selectedpoint=[i for i in range(pointsnum) if points[i].select_control_point == True ]
            if 0 in selectedpoint and pointsnum-1 in selectedpoint: #优先处理首尾  01
                if distance(thevert[0][0],thevert[-1][0])<yuzhi:
                    thevert[0][3]='FREE'
                    thevert[0][4]='FREE'
                    thevert[0][1]= thevert[0][0]+thevert[-1][1]-thevert[-1][0] #修改第一元素 左侧手柄为末尾元素左侧手柄
                    del selectedpoint[-1] 
                    needdelete.append(pointsnum-1)
                    sp_bihe=True
                    #删除末尾元素  修改数组使之对应  
            chushifenduan=cc_lianxuxingfenduan(selectedpoint)  #对选中顶点进行连续性划分
            fenduan=[] #fenduan数组的首尾用于后面区分哪些点的手柄需要调整 
            for i in chushifenduan: #对在阈值内的顶点进行记录,后期直接在总集合中抽出
                tempss=[]
                if len(i)>1 :
                    d_a=-1
                    for i2 in i :
                        if d_a==-1 :
                            d_a=i2
                        elif distance(thevert[d_a][0],thevert[i2][0])<yuzhi:
                            needdelete.append(i2) ; tempss.append(i2)
                        else:
                            d_a=i2
                if tempss!=[]:fenduan.append(tempss)
            #------------------------------------------------
            for i in fenduan:
                if len (i) !=0:
                    thevert[i[0]-1][4]='FREE';thevert[i[0]-1][3]='FREE'
                    thevert[i[0]-1][2]=(thevert[i[-1]][2] - thevert[i[-1]][0]) + thevert[i[0]-1][0]
                    #提前预改部分顶点数据 
            if len(needdelete)>0 :
                ii= needdelete[0];del needdelete[0];needdelete.append(ii);needdelete.reverse()
                for i in needdelete: del thevert[i]  #删除被焊接的顶点
                cc_gouzao_bezier_sp(obj,thevert,sp_bihe) #依据顶点构造一条新曲线
                needdeletesp.append (thespline)   
            #----------------------------------------------------------------------------------------------------------------------  
        else:
            points=thespline.points
            thevert=cc_huoqu_sp_verts(thespline)
            #信息收集
            sp_bihe = thespline.use_cyclic_u
            needdelete=[] ; pointsnum=len(points) ; selectedpoint=[i for i in range(pointsnum) if points[i].select == True ]
            if 0 in selectedpoint and pointsnum-1 in selectedpoint: #优先处理首尾  01
                if distance(thevert[0][0],thevert[-1][0])<yuzhi:
                    del selectedpoint[-1] 
                    needdelete.append(pointsnum-1)
                    sp_bihe=True
                    #删除末尾元素  修改数组使之对应  
            chushifenduan=cc_lianxuxingfenduan(selectedpoint)  #对选中顶点进行连续性划分
            fenduan=[] #fenduan数组的首尾用于后面区分哪些点的手柄需要调整 
            for i in chushifenduan: #对在阈值内的顶点进行记录,后期直接在总集合中抽出
                tempss=[]
                if len(i)>1 :
                    d_a=-1
                    for i2 in i :
                        if d_a==-1 :
                            d_a=i2
                        elif distance(thevert[d_a][0],thevert[i2][0])<yuzhi:
                            needdelete.append(i2) ; tempss.append(i2)
                        else:
                            d_a=i2
                if tempss!=[]:fenduan.append(tempss)
            #------------------------------------------------
            if len(needdelete)>0 :
                ii= needdelete[0];del needdelete[0];needdelete.append(ii);needdelete.reverse()
                for i in needdelete: del thevert[i]  #删除被焊接的顶点
                cc_gouzao_sp(obj,thevert,sp_bihe,thespline.type) #生成新的线条
                needdeletesp.append (thespline) 
    #----------------------------------------------------------------
    for i in needdeletesp :
        obj.data.splines.remove(i) 
    #----------------------------------------------------------------以下焊接相连曲线
    polysp=[];beziersp=[];nurbssp=[];needdeletesp=[]
    #01  线条种类划分 在不同种类间进行焊接
    #02  收集被选择首位的线条序列号 和顶点
    #03  从第一条线开始，逐步向后排查选中的末尾点与靠近的选中点 找到要焊接的最近对象 检查对象是否需要翻转  创建新的对象 拟合数据 并将其添加到该种类中 并将原始线条添加到待删除 如果没有找到，将其从列表移除 直到列表清空
    for i in obj.data.splines:
        if i.use_cyclic_u==False: #闭环直接跳过
            if i.type == 'BEZIER':
                points=i.bezier_points
                if points[0].select_control_point==True or points[-1].select_control_point==True: beziersp.append(i)
            elif i.type == 'POLY':
                points=i.points
                if points[0].select==True or points[-1].select==True: polysp.append(i)
            else:
                points=i.points
                if points[0].select==True or points[-1].select==True: nurbssp.append(i)
    #----------------------
    
    yuzhi=cc_danweishipei(bpy.context.scene.cc_weld) #调整焊接单位
    while len(beziersp)>1:
        points =beziersp[0].bezier_points
        lianjiequxiandian=[]
        xuyaoshanhu=False
        if points[0].select_control_point==True :
            jl=copy.copy(yuzhi)
            sp=None ;thea_d=None;sp_suoyin=None
            for i in range(1,len(beziersp)):
                points22=beziersp[i].bezier_points
                a_d=distance(points22[0].co,points[0].co)
                b_d=distance(points22[-1].co,points[0].co)
                if a_d <= jl :jl=a_d;sp=beziersp[i];sp_suoyin=i;thea_d=a_d #此时线条需要翻转
                if b_d <= jl :jl=b_d;sp=beziersp[i] ;sp_suoyin=i
            if sp!=None :
                
                thespvert=cc_huoqu_sp_verts(sp)
                if jl== thea_d :  #判断该条曲线是否需要翻转
                    thespvert=cc_bezier_sp_fanzhuan(thespvert)
                lianjiequxiandian=thespvert
                mespvert=cc_huoqu_sp_verts(beziersp[0])
                #mespvert首点需要删除 thespvert尾点 手柄需要调整
                lianjiequxiandian[-1][3]='FREE';lianjiequxiandian[-1][4]='FREE';lianjiequxiandian[-1][2]=mespvert[0][2]
                del mespvert[0]
                lianjiequxiandian=lianjiequxiandian+mespvert
                needdeletesp.append(sp);xuyaoshanhu=True #将该线条加入待删除对象
                del beziersp[sp_suoyin] #移除数组
            ###########首点链接其他线的情况
        if points[-1].select_control_point==True :
            jl=copy.copy(yuzhi)
            sp_end=None ;theb_d=None ;sp_end_suoyin=i
            for i in range(1,len(beziersp)):
                points22=beziersp[i].bezier_points
                a_d=distance(points22[0].co,points[-1].co)
                b_d=distance(points22[-1].co,points[-1].co)
                if a_d <= jl :jl=a_d;sp_end=beziersp[i];sp_end_suoyin=i
                if b_d <= jl :jl=b_d;sp_end=beziersp[i] ;sp_end_suoyin=i;theb_d=b_d #此时线条需要翻转
            if sp_end!=None : 
                thespvert=cc_huoqu_sp_verts(sp_end)
                if jl== theb_d :  #判断该条曲线是否需要翻转
                    thespvert=cc_bezier_sp_fanzhuan(thespvert)
                if len(lianjiequxiandian)==0:
                    lianjiequxiandian=cc_huoqu_sp_verts(beziersp[0])
                lianjiequxiandian[-1][3]='FREE';lianjiequxiandian[-1][4]='FREE';lianjiequxiandian[-1][2]=thespvert[0][2]
                del thespvert[0]
                lianjiequxiandian=lianjiequxiandian + thespvert
                needdeletesp.append(sp_end) ; xuyaoshanhu =True #将该线条加入待删除对象
                del beziersp[sp_end_suoyin] #移除数组
        #--------------构造新曲线
        if len(lianjiequxiandian)!=0:
            newsp=cc_gouzao_bezier_sp(obj,lianjiequxiandian,False)
            beziersp.append(newsp)
        if xuyaoshanhu==True:needdeletesp.append(beziersp[0]) #将该线条加入待删除对象
        del beziersp[0]
#__________________________________________________________________________________________________________________________
    for zhonglei in [polysp,nurbssp]:
        while len(zhonglei)>1:
            points =zhonglei[0].points
            lianjiequxiandian=[]
            xuyaoshanhu=False
            if points[0].select==True :
                jl=copy.copy(yuzhi)
                sp=None ;thea_d=None;sp_suoyin=None
                for i in range(1,len(zhonglei)):
                    points22=zhonglei[i].points
                    a_d=distance(points22[0].co,points[0].co)
                    b_d=distance(points22[-1].co,points[0].co)
                    if a_d <= jl :jl=a_d;sp=zhonglei[i];sp_suoyin=i;thea_d=a_d #此时线条需要翻转
                    if b_d <= jl :jl=b_d;sp=zhonglei[i] ;sp_suoyin=i
                if sp!=None :
                    
                    thespvert=cc_huoqu_sp_verts(sp)
                    if jl== thea_d :  #判断该条曲线是否需要翻转
                        thespvert=thespvert.reverse()
                    lianjiequxiandian=thespvert
                    mespvert=cc_huoqu_sp_verts(zhonglei[0])
                    #mespvert首点需要删除 
                    del mespvert[0]
                    lianjiequxiandian=lianjiequxiandian+mespvert
                    needdeletesp.append(sp);xuyaoshanhu=True #将该线条加入待删除对象
                    del zhonglei[sp_suoyin] #移除数组
                ###########首点链接其他线的情况
            if points[-1].select==True :
                jl=copy.copy(yuzhi)
                sp_end=None ;theb_d=None ;sp_end_suoyin=i
                for i in range(1,len(zhonglei)):
                    points22=zhonglei[i].points
                    a_d=distance(points22[0].co,points[-1].co)
                    b_d=distance(points22[-1].co,points[-1].co)
                    if a_d <= jl :jl=a_d;sp_end=zhonglei[i];sp_end_suoyin=i
                    if b_d <= jl :jl=b_d;sp_end=zhonglei[i] ;sp_end_suoyin=i;theb_d=b_d #此时线条需要翻转
                if sp_end!=None : 
                    thespvert=cc_huoqu_sp_verts(sp_end)
                    if jl== theb_d :  #判断该条曲线是否需要翻转
                        thespvert=thespvert.reverse()
                    if len(lianjiequxiandian)==0:
                        lianjiequxiandian=cc_huoqu_sp_verts(zhonglei[0])
                    del thespvert[0]
                    lianjiequxiandian=lianjiequxiandian + thespvert
                    needdeletesp.append(sp_end) ; xuyaoshanhu =True #将该线条加入待删除对象
                    del zhonglei[sp_end_suoyin] #移除数组
            #--------------构造新曲线
            if len(lianjiequxiandian)!=0:
                newsp=cc_gouzao_sp(obj,lianjiequxiandian,False,zhonglei[0].type)
                zhonglei.append(newsp)
            if xuyaoshanhu==True:needdeletesp.append(zhonglei[0]) #将该线条加入待删除对象
            del zhonglei[0]

    for i in needdeletesp :
         obj.data.splines.remove(i)
#---------------------------------------------

class cxl_weld (bpy.types.Operator): #焊接命令  争取今后对曲线和网格对象一并支持  暂时只支持曲线
    bl_idname = "view3d.cxl_weld"
    bl_label = "焊接"

    def execute(self, context):
        selection=bpy.context.selected_objects
        if bpy.context.mode=='EDIT_CURVE':
            if context.mode != 'OBJECT':bpy.ops.object.mode_set(mode='OBJECT')#暂时强制回到物体模式
            me=selection[0]
            cc_weld_sp (me)
            bpy.ops.object.mode_set(mode="EDIT")
        return {'FINISHED'}