
# 类似于3dmax的基于曲线生成实体对象  -23.11.10 创建
# 先看是否可以用脚本控制节点实现
# ------------------------------------------------------------

import bpy
from .cxl import Update3DViewPorts, cxl_namebytime, cc_jinggao, cxl_snaptopoint, cxl_shizixingyichu, cxl_shizixing, cxl3dto2d, cc_duixiangshiliang, distance, cxl_chu, cxl_jian, cxl_jia, cc_danweishipei, c_huoqujianpanzhi, cxl_tishicaizhi_get, \
    cc_shuaxing_shikou_dingdian_2d, cc_shuaxing_shikou_dingdian, cc_jisuanxuanzheduixiantijikuang, cc_jisuanzhongxingdian,cxl_obj_tex_image_shuxing_tianjia
from math import degrees, sin
import math
import mathutils
from mathutils import Vector

def c_extrude_node_tree(obj):  # 平面修改器节点数据,
    newname = 'c_extrude' + cxl_namebytime()
    thenodetree = bpy.data.node_groups.new(newname, 'GeometryNodeTree')
    thenodetree.interface.new_socket(name='Geometry', description='c_extrude_in',in_out='INPUT', socket_type='NodeSocketGeometry', parent=None)
    thenodetree.interface.new_socket(name='Geometry', description='c_extrude_out',in_out='OUTPUT', socket_type='NodeSocketGeometry', parent=None)
    thenodetree.interface.new_socket(name='上截面', description='是否封上口',in_out='INPUT', socket_type='NodeSocketBool', parent=None)
    thenodetree.interface.items_tree[2].default_value=True
    thenodetree.interface.new_socket(name='下截面', description='是否封下口',in_out='INPUT', socket_type='NodeSocketBool', parent=None)
    thenodetree.interface.items_tree[3].default_value=True
    # 节点
    thenodes = ["NodeGroupInput","ShaderNodeCombineXYZ","GeometryNodeJoinGeometry","GeometryNodeMergeByDistance","GeometryNodeSetMaterial",\
                "GeometryNodeSetShadeSmooth","NodeGroupOutput","GeometryNodeFillCurve","GeometryNodeSetPosition","GeometryNodeSampleIndex",\
                    "GeometryNodeInputPosition","GeometryNodeInputIndex","GeometryNodeFlipFaces","GeometryNodeTransform","GeometryNodeCurveToMesh",\
                        "GeometryNodeMeshToCurve","GeometryNodeDeleteGeometry","GeometryNodeInputSplineCyclic","GeometryNodeSwitch","GeometryNodeDeleteGeometry",\
                            "GeometryNodeSwitch","GeometryNodeDeleteGeometry","GeometryNodeSwitch","GeometryNodeExtrudeMesh","GeometryNodeSeparateGeometry",\
                                "GeometryNodeCurveToMesh","GeometryNodeExtrudeMesh","GeometryNodeDeleteGeometry","GeometryNodeInputSplineCyclic","GeometryNodeSwitch","NodeReroute"]
    # 坐标
    thelocations =[ (-1217.6104, 429.0013), (965.9824, 1460.8969), (2490.0681, 638.2073), (2750.3367, 684.3394), (3033.3462, 615.6371), (3346.3958, 621.8500), (3660.6313, 625.7468),\
                    (348.3249, 678.1884), (665.5990, 718.0831), (446.6449, 497.1860), (124.0737, 406.9911), (131.2402, 333.7231), (968.9359, 603.9511), (1615.6974, 1044.3490), \
                        (-215.9678, 632.5397), (20.3124, 615.6544), (-458.7238, 602.8802), (-842.8842, 408.5638), (-633.5287, 452.1057), (2117.6992, 689.7935), (-383.5128, 158.5413),\
                              (2110.2031, 971.0463), (-383.3685, -31.8227), (1696.9326, 397.1727), (2109.6001, 449.7016), (320.4860, -291.8310), (1377.5010, -229.0836), \
                                (-396.4281, -285.7791), (-911.2039, -393.6706), (-701.8484, -350.1287), (2208.1235, -186.1346)]
    # 连线
    thelianxian = [[2, 3],[3, 4],[5, 6],[8, 12],[15, 7],[10, 9],[11, 9],[9, 8],[7, 8],[8, 13],[1, 13],[15, 9],[14, 15],[16, 14],[0, 16],[18, 16],[17, 18],[0, 20],\
                   [4, 5],[13, 21],[12, 19],[0, 22],[20, 21],[22, 19],[12, 23],[1, 23],[23, 24],[23, 24],[25, 26],[1, 26],[29, 27],[28, 29],[27, 25],[0, 27],[30, 2],\
                    [24, 2],[19, 2],[21, 2],[26, 30]]
    # 插槽位置
    thechacao = [[0, 0],[0, 0],[0, 0],[0, 0],[0, 0],[0, 1],[0, 2],[0, 2],[0, 0],[0, 0],[0, 1],[0, 0],[0, 0],[0, 0],[0, 0],[0, 1],[0, 0],[1, 0],[0, 0],[0, 0],[0, 0],[2, 0],\
                 [0, 1],[0, 1],[0, 0],[0, 2],[2, 1],[0, 0],[0, 0],[0, 2],[0, 1],[0, 0],[0, 0],[0, 0],[0, 0],[0, 0],[0, 0],[0, 0],[0, 0]]

    nds = []
    for i in range(len(thenodes)):
        temp = thenodetree.nodes.new(thenodes[i])
        temp.location = thelocations[i]
        nds.append(temp)
    #-------------
    nds[1].name = 'c_extrude_value'
    nds[1].inputs[0].default_value=0.0
    nds[1].inputs[1].default_value=0.0
    nds[1].inputs[2].default_value=cc_danweishipei(bpy.context.scene.c_jichu)
    nds[4].name = 'c_setMaterial_value'
    if obj.active_material == None:
        nds[4].inputs[2].default_value = cxl_tishicaizhi_get()
    else:
        nds[4].inputs[2].default_value = obj.active_material
    #--------
    nds[3].mode='ALL'
    nds[3].inputs[2].default_value=9.999999974752427e-07
    nds[5].domain='FACE'
    nds[5].inputs[2].default_value=False
    nds[7].mode='NGONS'
    nds[8].inputs[3].default_value[0]=0.0
    nds[8].inputs[3].default_value[1]=0.0
    nds[8].inputs[3].default_value[2]=0.0
    nds[9].data_type='FLOAT_VECTOR'
    nds[9].domain='POINT'
    nds[9].clamp=False
    nds[9].inputs[2].default_value=0
    nds[13].mode='COMPONENTS'
    nds[13].inputs[1].default_value[0]=0.0
    nds[13].inputs[1].default_value[1]=0.0
    nds[13].inputs[1].default_value[2]=0.0
    nds[13].inputs[2].default_value[0]=0.0
    nds[13].inputs[2].default_value[1]=0.0
    nds[13].inputs[2].default_value[2]=0.0
    nds[13].inputs[3].default_value[0]=1.0
    nds[13].inputs[3].default_value[1]=1.0
    nds[13].inputs[3].default_value[2]=1.0
    nds[14].inputs[2].default_value=False
    nds[16].domain='CURVE'
    nds[16].mode='ALL'
    nds[18].input_type='BOOLEAN'
    nds[18].inputs[1].default_value=True
    nds[18].inputs[2].default_value=False
    nds[19].domain='FACE'
    nds[19].mode='ALL'
    nds[20].input_type='BOOLEAN'
    nds[20].inputs[1].default_value=True
    nds[20].inputs[2].default_value=False
    nds[21].domain='FACE'
    nds[21].mode='ALL'
    nds[22].input_type='BOOLEAN'
    nds[22].inputs[1].default_value=True
    nds[22].inputs[2].default_value=False
    nds[23].mode='EDGES'
    nds[23].inputs[3].default_value=1.0
    nds[24].domain='FACE'
    nds[25].inputs[2].default_value=False
    nds[26].mode='EDGES'
    nds[26].inputs[3].default_value=1.0
    nds[27].domain='CURVE'
    nds[27].mode='ALL'
    nds[29].input_type='BOOLEAN'
    nds[29].inputs[1].default_value=False
    nds[29].inputs[2].default_value=True
    #---------
    for i in range(len(thelianxian)):
        thenodetree.links.new(nds[thelianxian[i][0]].outputs[thechacao[i][0]],nds[thelianxian[i][1]].inputs[thechacao[i][1]])
    # ---------------------
    return (thenodetree)
##########################################################################


def c_xyz_uvmap_node_tree():  # uvwmap修改器节点数据,
    newname = 'c_xyz_uvwmap' + cxl_namebytime()
    thenodetree = bpy.data.node_groups.new(newname, 'GeometryNodeTree')
    thenodetree.interface.new_socket(name='Geometry', description='c_xyz_uvwmap_in',
                                     in_out='INPUT', socket_type='NodeSocketGeometry', parent=None)
    c_xyz_uvmap_size = thenodetree.interface.new_socket(name='size', description='各方向大小', in_out='INPUT', socket_type='NodeSocketVector', parent=None)
    c_xyz_uvmap_size.default_value = [2, 2, 2]
    thenodetree.interface.new_socket(name='offset', description='各方向偏移', in_out='INPUT', socket_type='NodeSocketVector', parent=None)
    thenodetree.interface.new_socket(name='rotate', description='旋转', in_out='INPUT', socket_type='NodeSocketFloat', parent=None)

    thenodetree.interface.new_socket(name='Geometry', description='c_xyz_uvwmap_out',in_out='OUTPUT', socket_type='NodeSocketGeometry', parent=None)
    thenodetree.interface.new_socket(name='c_uv', description='uv属性名称', in_out='OUTPUT', socket_type='NodeSocketVector', parent=None)
    thenodetree.interface.items_tree[1].attribute_domain = 'CORNER'

    # 节点
    thenodes = ["NodeGroupInput", "NodeGroupOutput", "GeometryNodeSeparateGeometry", "GeometryNodeSampleIndex", "GeometryNodeInputNormal", "GeometryNodeInputIndex", "ShaderNodeSeparateXYZ",
                "GeometryNodeSampleIndex", "ShaderNodeSeparateXYZ", "GeometryNodeSeparateGeometry", "FunctionNodeCompare", "FunctionNodeCompare", "GeometryNodeJoinGeometry", "GeometryNodeSampleIndex",
                "ShaderNodeSeparateXYZ", "GeometryNodeSeparateGeometry", "FunctionNodeCompare", "GeometryNodeSampleIndex", "ShaderNodeSeparateXYZ", "GeometryNodeSeparateGeometry", "FunctionNodeCompare",
                "GeometryNodeSampleIndex", "ShaderNodeSeparateXYZ", "GeometryNodeSeparateGeometry", "FunctionNodeCompare", "GeometryNodeSampleIndex", "GeometryNodeInputIndex", "GeometryNodeInputPosition",
                "GeometryNodeCaptureAttribute", "GeometryNodeTransform", "GeometryNodeTransform", "GeometryNodeTransform", "GeometryNodeTransform", "GeometryNodeTransform", "GeometryNodeSetPosition",
                "ShaderNodeSeparateXYZ", "ShaderNodeCombineXYZ", "GeometryNodeSampleIndex", "GeometryNodeInputIndex", "GeometryNodeInputPosition", "GeometryNodeJoinGeometry", "GeometryNodeSetPosition",
                "GeometryNodeCaptureAttribute", "GeometryNodeSampleIndex", "GeometryNodeInputIndex", "GeometryNodeInputPosition", "GeometryNodeMergeByDistance", "ShaderNodeVectorMath", "ShaderNodeSeparateXYZ",
                "ShaderNodeCombineXYZ", "NodeReroute", "GeometryNodeBoundBox", "ShaderNodeVectorMath", "NodeReroute", "NodeReroute", "NodeReroute", "NodeReroute", "NodeReroute", "NodeReroute", "GeometryNodeTransform",
                "ShaderNodeVectorMath", "NodeReroute", "ShaderNodeVectorMath", "NodeReroute", "GeometryNodeTransform", "NodeReroute", "FunctionNodeAxisAngleToRotation", "NodeReroute", "NodeReroute",
                "FunctionNodeAxisAngleToRotation"]
    # 坐标
    thelocations = [(-1509.0465, 65.5321), (11193.5762, 799.5044), (100.8226, 9.0865), (-622.5876, -156.9762), (643.3940, -1691.9442), (742.5425, -1811.4413), (-427.8847, -114.9044),
                    (523.3555, -299.0011), (717.1189, -281.3267), (1195.9301, -101.1758), (-237.0791, -
                                                                                           95.1210), (908.6854, -206.8474), (6470.7969, 125.3131), (1660.9381, -503.5198),
                    (1854.7015, -485.8453), (2340.8909, -327.8687), (2075.7842, -460.1529), (2718.3599, -
                                                                                             719.4527), (2937.8203, -720.4993), (3398.3130, -543.8016), (3157.4714, -638.7418),
                    (3850.3713, -774.0428), (4044.1345, -756.3684), (4530.3242, -514.9097), (4247.5068, -
                                                                                             686.3240), (7727.0806, 343.8826), (7459.9780, 90.6251), (7452.2646, 189.5261),
                    (9734.0752, 503.2246), (1788.8618, 327.0441), (2957.4873, 117.7667), (4098.7905, -
                                                                                          94.9672), (5353.2676, -86.6824), (5818.5122, -643.1206), (8641.8643, 391.0946),
                    (7979.3086, 351.4726), (8226.0322, 377.9619), (9468.3066, 347.7202), (9137.7627,
                                                                                          98.2950), (9135.0527, 153.7412), (6708.5000, 866.5479), (10233.0576, 979.0088),
                    (9975.6152, 938.6669), (9601.5791, 984.4504), (9352.7256, 756.1743), (9356.5303,
                                                                                          825.2213), (10628.7949, 946.7064), (7832.2246, -194.9925), (8259.3037, 4.5660),
                    (8461.2998, 43.6206), (8357.2998, 487.9318), (7569.0957, -270.9967), (8050.4121, -
                                                                                          78.9574), (3958.8347, -30.4162), (2860.9263, 212.7270), (1675.8870, 442.3549),
                    (1242.1310, 745.5565), (5287.7109, -58.1743), (5741.9297, -598.2665), (1469.8275,
                                                                                           742.8792), (-689.7462, -895.7885), (-455.2716, -947.6199), (-685.0162, -1163.0828),
                    (-461.8468, -1190.7499), (6801.3872, 147.2761), (7034.7964, 94.4988), (6440.2539, -328.9354), (6263.7480, -2001.3794), (-730.6099, -2349.5610), (6854.7993, -408.2227)]
    # 连线
    thelianxian = [[5, 3], [4, 3], [3, 6], [7, 8], [11, 9], [10, 2], [2, 9], [2, 7], [13, 14], [16, 15], [9, 15], [9, 13], [17, 18], [20, 19], [15, 17], [15, 19], [21, 22], [24, 23],
                   [19, 21], [19, 23], [6, 10], [8, 11], [22, 24], [14, 16], [18, 20], [0, 3], [0, 2], [
        26, 25], [27, 25], [65, 25], [54, 30], [58, 33], [57, 32], [5, 7], [4, 7], [4, 13],
        [5, 13], [4, 17], [5, 17], [4, 21], [5, 21], [50, 34], [25, 35], [35, 36], [35, 36], [
            36, 34], [38, 37], [39, 37], [37, 28], [34, 28], [34, 37], [55, 29], [53, 31], [28, 1],
        [44, 43], [45, 43], [43, 42], [42, 41], [42, 41], [28, 42], [40, 43], [33, 12], [32, 12], [
            31, 12], [30, 12], [29, 12], [59, 12], [58, 40], [57, 40], [53, 40], [54, 40], [55, 40],
        [56, 40], [41, 46], [49, 34], [48, 49], [48, 49], [65, 50], [65, 51], [51, 47], [51, 47], [
            47, 52], [52, 48], [19, 53], [15, 54], [9, 55], [2, 56], [23, 57], [23, 58], [56, 59],
        [61, 59], [61, 29], [61, 30], [61, 31], [61, 32], [61, 33], [60, 61], [46, 1], [0, 60], [
            0, 62], [63, 59], [63, 29], [63, 30], [63, 31], [63, 32], [63, 33], [62, 63], [12, 64],
        [64, 65], [68, 67], [67, 66], [66, 64], [0, 68]]
    # 插槽位置
    thechacao = [[0, 2], [0, 1], [0, 0], [0, 0], [0, 1], [0, 1], [1, 0], [1, 0], [0, 0], [0, 1], [1, 0], [1, 0], [0, 0], [0, 1], [1, 0], [1, 0], [0, 0], [0, 1], [1, 0], [1, 0], [2, 0], [2, 0],
                 [0, 0], [1, 0], [1, 0], [0, 0], [0, 0], [0, 2], [0, 1], [0, 0], [0, 0], [0, 0], [0, 0], [
        0, 2], [0, 1], [0, 1], [0, 2], [0, 1], [0, 2], [0, 1], [0, 2], [0, 0], [0, 0], [0, 0],
        [1, 1], [0, 2], [0, 2], [0, 1], [0, 1], [0, 0], [0, 0], [0, 0], [0, 0], [1, 1], [0, 2], [
            0, 1], [0, 1], [1, 2], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0],
        [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 3], [0, 0], [1, 1], [0, 0], [
            0, 0], [2, 0], [1, 1], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [1, 0], [0, 0],
        [0, 3], [0, 3], [0, 3], [0, 3], [0, 3], [0, 3], [0, 0], [0, 0], [1, 1], [2, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 0], [0, 0], [0, 0], [0, 0], [0, 1], [0, 2], [3, 0]]
    nds = []
    for i in range(len(thenodes)):
        temp = thenodetree.nodes.new(thenodes[i])
        temp.location = thelocations[i]
        nds.append(temp)

    nds[0].output_template(4)
    nds[1].input_template(2)
    nds[2].domain = 'FACE'
    nds[10].data_type = 'FLOAT'
    nds[10].operation = 'GREATER_THAN'
    nds[10].inputs[
        1].default_value = 0.6
    nds[3].data_type = 'FLOAT_VECTOR'
    nds[3].domain = 'FACE'
    nds[9].domain = 'FACE'
    nds[11].data_type = 'FLOAT'
    nds[11].operation = 'LESS_EQUAL'
    nds[11].inputs[1].default_value = -0.6
    nds[7].data_type = 'FLOAT_VECTOR'
    nds[7].domain = 'FACE'
    nds[15].domain = 'FACE'
    nds[16].data_type = 'FLOAT'
    nds[16].operation = 'LESS_EQUAL'
    nds[16].inputs[1].default_value = -0.65
    nds[13].data_type = 'FLOAT_VECTOR'
    nds[13].domain = 'FACE'
    nds[19].domain = 'FACE'
    nds[20].data_type = 'FLOAT'
    nds[20].operation = 'GREATER_EQUAL'
    nds[20].inputs[
        1].default_value = 0.65
    nds[17].data_type = 'FLOAT_VECTOR'
    nds[17].domain = 'FACE'
    nds[23].domain = 'FACE'
    nds[24].data_type = 'FLOAT'
    nds[24].operation = 'GREATER_EQUAL'
    nds[24].inputs[
        1].default_value = 0
    nds[21].data_type = 'FLOAT_VECTOR'
    nds[21].domain = 'FACE'
    nds[29].inputs[2].default_value[0] = 3.14159
    nds[30].inputs[2].default_value[0] = -1.5708
    nds[31].inputs[2].default_value[0] = 1.5708
    nds[31].inputs[2].default_value[2] = 3.14159
    nds[32].inputs[2].default_value[1] = -1.5708
    nds[32].inputs[2].default_value[2] = 4.71239
    nds[33].inputs[2].default_value[1] = 1.5708
    nds[33].inputs[2].default_value[2] = 1.5708
    nds[36].inputs[2].default_value = 0
    nds[25].data_type = 'FLOAT_VECTOR'
    nds[25].domain = 'POINT'
    nds[49].inputs[2].default_value = 0
    nds[52].operation = 'DIVIDE'
    nds[52].inputs[1].default_value[0] = 2
    nds[
        52].inputs[1].default_value[1] = 2
    nds[52].inputs[1].default_value[2] = 2
    nds[47].operation = 'SUBTRACT'
    nds[28].domain = 'CORNER'
    nds[28].capture_items.new(
        'VECTOR', 'value')
    nds[37].data_type = 'FLOAT_VECTOR'
    nds[37].domain = 'CORNER'
    nds[43].data_type = 'FLOAT_VECTOR'
    nds[43].domain = 'POINT'
    nds[42].domain = 'POINT'
    nds[42].capture_items.new(
        'VECTOR', 'value')
    nds[46].inputs[2].default_value = 1e-06
    nds[60].operation = 'DIVIDE'
    nds[60].inputs[0].default_value[0] = 1
    nds[60].inputs[0].default_value[1] = 1
    nds[60].inputs[0].default_value[2] = 1

    for i in range(len(thelianxian)):
        thenodetree.links.new(nds[thelianxian[i][0]].outputs[thechacao[i][0]],
                              nds[thelianxian[i][1]].inputs[thechacao[i][1]])
    # ---------------------
    return (thenodetree)
 ##########################################################################
##########################################################################


def c_pingmian_node_tree(obj):  # 平面修改器节点数据,
    newname = 'c_pingmian' + cxl_namebytime()
    thenodetree = bpy.data.node_groups.new(newname, 'GeometryNodeTree')
    thenodetree.interface.new_socket(name='Geometry', description='c_pingmian_in',in_out='INPUT', socket_type='NodeSocketGeometry', parent=None)
    thenodetree.interface.new_socket(name='Geometry', description='c_pingmian_out',in_out='OUTPUT', socket_type='NodeSocketGeometry', parent=None)
    thenodetree.interface.new_socket(name='翻转面', description='翻转',in_out='INPUT', socket_type='NodeSocketBool', parent=None)
    thenodetree.interface.items_tree[2].default_value=False
    thenodetree.interface.new_socket(name='c_uv', description='uv属性名称', in_out='OUTPUT', socket_type='NodeSocketVector', parent=None)
    # 节点
    thenodes = ["NodeGroupInput","GeometryNodeSetMaterial","GeometryNodeSetShadeSmooth","NodeGroupOutput","GeometryNodeFillCurve","GeometryNodeSetPosition",\
        "GeometryNodeSampleIndex","GeometryNodeInputPosition","GeometryNodeInputIndex","GeometryNodeCurveToMesh","GeometryNodeMeshToCurve",\
        "GeometryNodeFlipFaces","NodeReroute","GeometryNodeUVUnwrap"]
    # 坐标
    thelocations = [(-564.3056, 509.1470),(1128.8467, 591.0974),(1471.5374, 636.9893),(1851.4609, 586.4739),(227.5960, 847.6855),(597.5959, 797.6855),\
        (299.9417, 666.5305),(84.3009, 505.3672),(77.0798, 441.8768),(-161.2861, 656.2795),(31.0906, 796.5994),(855.8383, 587.9818),\
        (212.6931, 255.8903),(1487.7627, 422.0424)]
    # 连线
    thelianxian = [[1, 2],[2, 3],[10, 4],[7, 6],[8, 6],[6, 5],[4, 5],[0, 9],[9, 10],[11, 1],[9, 6],[5, 11],[12, 11],[0, 12],[13, 3]]
    # 插槽位置
    thechacao = [[0, 0],[0, 0],[0, 0],[0, 1],[0, 2],[0, 2],[0, 0],[0, 0],[0, 0],[0, 0],[0, 0],[0, 0],[0, 1],[1, 0],[0, 1]]

    nds = []
    for i in range(len(thenodes)):
        temp = thenodetree.nodes.new(thenodes[i])
        temp.location = thelocations[i]
        nds.append(temp)

    nds[1].name = 'c_setMaterial_value'
    if obj.active_material == None:
        nds[1].inputs[2].default_value = cxl_tishicaizhi_get()
    else:
        nds[1].inputs[2].default_value = obj.active_material
    nds[2].domain='FACE'
    nds[2].inputs[2].default_value=False
    nds[4].mode='NGONS'
    nds[5].inputs[3].default_value[0]=0.0
    nds[5].inputs[3].default_value[1]=0.0
    nds[5].inputs[3].default_value[2]=0.0
    nds[6].data_type='FLOAT_VECTOR'
    nds[6].domain='POINT'
    nds[6].clamp=False
    nds[6].inputs[2].default_value=0
    nds[9].inputs[2].default_value=False
    nds[13].method='ANGLE_BASED'
    nds[13].inputs[2].default_value=0.0010000000474974513
    nds[13].inputs[3].default_value=True


    for i in range(len(thelianxian)):
        thenodetree.links.new(nds[thelianxian[i][0]].outputs[thechacao[i][0]],nds[thelianxian[i][1]].inputs[thechacao[i][1]])
    # ---------------------
    return (thenodetree)
#-------------------------------------------------------------------------------------------------------------------------------------

def c_zhuankuai_node_tree(obj):  # 砖块修改器节点数据,
    newname = 'c_zhuankuai' + cxl_namebytime()
    thenodetree = bpy.data.node_groups.new(newname, 'GeometryNodeTree')
    thenodetree.interface.new_socket(name='Geometry', description='c_zhuankuai',in_out='INPUT', socket_type='NodeSocketGeometry', parent=None)
    thenodetree.interface.new_socket(name='Geometry', description='c_zhuankuai',in_out='OUTPUT', socket_type='NodeSocketGeometry', parent=None)
    temp=thenodetree.interface.new_socket(name='长', description='length',in_out='INPUT', socket_type='NodeSocketFloat', parent=None)
    temp.subtype='DISTANCE';temp.default_value=1.5
    temp=thenodetree.interface.new_socket(name='宽', description='width',in_out='INPUT', socket_type='NodeSocketFloat', parent=None)
    temp.subtype='DISTANCE';temp.default_value=0.75
    temp=thenodetree.interface.new_socket(name='高', description='height',in_out='INPUT', socket_type='NodeSocketFloat', parent=None)
    temp.subtype='DISTANCE';temp.default_value=0.007
    temp=thenodetree.interface.new_socket(name='倒角', description='Chamfer',in_out='INPUT', socket_type='NodeSocketFloat', parent=None)
    temp.default_value=3
    temp=thenodetree.interface.new_socket(name='偏移', description='offset',in_out='INPUT', socket_type='NodeSocketFloat', parent=None)
    temp.default_value=0.5 ; temp.min_value=0 ; temp.max_value=1
    temp=thenodetree.interface.new_socket(name='缝隙', description='gap',in_out='INPUT', socket_type='NodeSocketFloat', parent=None)
    temp.default_value=3 ; temp.min_value=0 ; temp.max_value=1

    thenodetree.interface.new_socket(name='c_uv', description='uv属性名称', in_out='OUTPUT', socket_type='NodeSocketVector', parent=None)

    # 节点
    thenodes = ["NodeGroupInput","NodeGroupOutput","GeometryNodeCurvePrimitiveQuadrilateral","GeometryNodeBoundBox","ShaderNodeSeparateXYZ","ShaderNodeVectorMath","ShaderNodeMath","GeometryNodePoints","ShaderNodeMath","GeometryNodeInputIndex","ShaderNodeMath","ShaderNodeCombineXYZ","GeometryNodeInstanceOnPoints","ShaderNodeMath","ShaderNodeMath","ShaderNodeSeparateXYZ","ShaderNodeMath","ShaderNodeMath","ShaderNodeMath","NodeReroute","ShaderNodeMath","ShaderNodeMath","NodeReroute","NodeReroute","ShaderNodeMath","ShaderNodeMath","ShaderNodeMath","ShaderNodeMath","NodeReroute","ShaderNodeMath","NodeReroute","ShaderNodeMath","ShaderNodeMath","ShaderNodeMath","NodeReroute","GeometryNodeFillCurve","GeometryNodeScaleElements","GeometryNodeExtrudeMesh","ShaderNodeCombineXYZ","GeometryNodeExtrudeMesh","GeometryNodeScaleElements","ShaderNodeCombineXYZ","NodeReroute","GeometryNodeCurveToMesh","GeometryNodeMeshToCurve","GeometryNodeFillCurve","GeometryNodeExtrudeMesh","ShaderNodeCombineXYZ","GeometryNodeTransform","ShaderNodeCombineXYZ","GeometryNodeFlipFaces","GeometryNodeTransform","GeometryNodeJoinGeometry","GeometryNodeMergeByDistance","GeometryNodeMeshBoolean","GeometryNodeFlipFaces","GeometryNodeJoinGeometry","GeometryNodeMergeByDistance","NodeReroute","GeometryNodeRealizeInstances","ShaderNodeMath","NodeReroute","ShaderNodeMath","ShaderNodeMath","ShaderNodeMath","GeometryNodeSwitch","ShaderNodeMath","FunctionNodeCompare","ShaderNodeMath","NodeReroute","NodeReroute","NodeReroute","GeometryNodeScaleElements","GeometryNodeScaleElements","ShaderNodeMath","ShaderNodeMath","ShaderNodeMath","ShaderNodeMath","NodeReroute","ShaderNodeValue","ShaderNodeMath","ShaderNodeMath","ShaderNodeMath","GeometryNodeSetMaterial","GeometryNodeInputPosition","ShaderNodeSeparateXYZ","ShaderNodeMath","NodeReroute","NodeReroute","ShaderNodeMath","ShaderNodeCombineXYZ","GeometryNodeSampleIndex","GeometryNodeInputIndex","NodeReroute","ShaderNodeVectorMath","GeometryNodeDuplicateElements","GeometryNodeMergeByDistance","ShaderNodeMath","ShaderNodeMath","ShaderNodeMath","ShaderNodeMath","NodeReroute","ShaderNodeMath","ShaderNodeMath","ShaderNodeMath","FunctionNodeCompare","ShaderNodeMath","GeometryNodeSwitch","ShaderNodeMath","NodeReroute","NodeReroute","NodeReroute","NodeReroute","NodeReroute","NodeReroute","ShaderNodeMath","ShaderNodeMath","ShaderNodeMath"]
    # 坐标
    thelocations = [(-2929.4067, 495.9701), (11666.4082, 1762.7635), (186.9068, -58.8816), (-1165.2179, 2498.3774), (-728.6229, 2496.5398), (-951.5089, 2513.4236), (35.5220, 2625.6355), (4530.0601, 2316.4570), (-233.2426, 2593.3438), (1880.2579, 1765.8936), (2649.6045, 2075.5876), (4270.9214, 2019.8867), (4927.0034, 1755.5188), (2835.0334, 668.0764), (3252.4387, 830.8051), (1163.9688, 2446.6108), (2413.9946, 2180.7908), (2893.7480, 2316.0703), (3204.4546, 2109.0693), (-855.7649, 2957.1040), (59.1958, 2384.8533), (-168.7966, 2376.5906), (-644.8998, 1299.0365), (-681.0065, 854.3154), (809.0980, 2869.7524), (2096.6963, 1509.2520), (2424.4902, 1544.8405), (3178.8179, 1141.8464), (2074.3684, 762.9046), (4067.9897, 1500.2817), (4713.7993, -24.7017), (2777.3215, 1825.8768), (3228.0906, 1892.7858), (3568.3306, 2005.6588), (121.2588, -1135.6410), (509.7087, -61.8772), (1088.2268, -87.3779), (2129.8176, -222.3726), (1265.5165, -880.8890), (2595.3152, -178.1118), (3126.8237, -121.8509), (1351.5352, -1099.3302), (114.3228, -1229.2782), (561.0939, -2359.4761), (820.2743, -2347.8486), (1079.3566, -2334.9275), (1549.3787, -2476.6763), (1223.6865, -2624.1567), (2128.6008, -2452.3572), (1813.0015, -2285.7366), (1510.9749, -2090.6584), (2140.6912, -2022.5192), (2764.0781, -2132.2305), (3138.2144, -2105.8662), (5850.4004, 1888.3627), (1937.0771, 14.3710), (3813.5542, -32.3131), (4104.1255, -31.6076), (5724.6016, -929.3169), (5191.6621, 1775.8710), (268.7684, 2692.1702), (588.9971, 2472.4185), (274.9197, 2410.0864), (3946.2622, 2002.9446), (2973.7034, 1398.1105), (3579.7708, 1709.5715), (2907.0581, 1596.7627), (3222.8560, 1655.4028), (382.9257, -699.0284), (121.2588, -1135.6410), (513.9174, -448.5112), (513.9174, -448.5112), (1352.3927, -96.8690), (3468.4668, -220.0506), (674.6951, -568.6982), (886.3536, -598.4311), (1154.2208, -526.2344), (658.8864, -735.4658), (1009.0162, -559.8973), (2470.2524, -499.8316), (2728.9019, -622.4915), (3000.2490, -744.6679), (3198.6045, -541.3414), (11148.7812, 1784.1393), (6328.5830, 1127.3391), (7297.4780, 904.8206), (9426.1172, 986.6379), (7323.6934, 213.2976), (7311.1514, 79.3019), (9883.8682, 540.6947), (10594.7881, 956.0269), (6751.0103, 1217.5261), (6330.4033, 1034.6160), (6914.9253, 2920.9785), (7013.0161, 1212.9691), (6062.2627, 1906.4653), (6292.6274, 1905.8110), (9903.2256, 994.6819), (9450.8838, 760.3630), (10202.7842, 680.6830), (9900.5391, 225.5296), (7319.6226, 524.3386), (7828.8203, 1227.2506), (8226.5410, 1262.3857), (8016.9961, 1244.8557), (8436.3604, 1279.1383), (10228.2646, 1023.2164), (8685.7061, 1208.7509), (9031.8818, 1032.0461), (383.4409, 2823.7961), (2026.8809, 369.2538), (1104.8041, 1291.4377), (1283.5378, 1914.0181), (-686.6010, 1100.1462), (-469.9218, -361.5779), (-1791.2787, 446.1364), (-2010.8390, 413.4064), (1108.5917, -1159.2837)]
    # 连线
    thelianxian = [[0, 3],[5, 4],[3, 5],[3, 5],[22, 2],[23, 2],[8, 6],[0, 6],[4, 8],[22, 8],[111, 10],[9, 10],[11, 7],[30, 12],[110, 13],[13, 14],[109, 15],[111, 16],[15, 17],[16, 17],[17, 18],[10, 18],[3, 19],[21, 20],[4, 21],[23, 21],[7, 12],[0, 22],[0, 23],[62, 24],[61, 24],[24, 7],[9, 25],[112, 25],[25, 26],[110, 27],[26, 27],[15, 28],[28, 14],[27, 29],[14, 29],[29, 11],[57, 30],[111, 31],[112, 31],[26, 32],[31, 32],[18, 33],[32, 33],[63, 11],[0, 34],[2, 35],[35, 36],[72, 37],[38, 37],[37, 39],[37, 39],[39, 40],[39, 40],[41, 39],[34, 38],[117, 41],[0, 42],[0, 43],[43, 44],[44, 45],[45, 46],[47, 46],[46, 48],[49, 48],[45, 50],[50, 51],[49, 51],[48, 52],[51, 52],[52, 53],[73, 56],[55, 56],[56, 57],[53, 58],[12, 59],[59, 54],[58, 54],[6, 60],[60, 61],[20, 62],[33, 63],[113, 64],[64, 65],[65, 63],[26, 66],[66, 67],[67, 65],[111, 64],[22, 68],[23, 68],[114, 71],[36, 72],[40, 73],[71, 74],[74, 75],[75, 76],[78, 76],[71, 36],[68, 77],[77, 75],[76, 72],[71, 78],[72, 55],[79, 40],[80, 81],[81, 82],[77, 81],[79, 80],[79, 82],[82, 73],[39, 73],[83, 1],[59, 54],[111, 87],[110, 88],[92, 91],[84, 91],[87, 86],[91, 94],[93, 94],[94, 85],[85, 89],[88, 89],[90, 1],[54, 95],[95, 96],[86, 97],[87, 98],[98, 97],[100, 99],[89, 99],[99, 90],[88, 100],[96, 91],[96, 83],[64, 101],[85, 102],[88, 102],[102, 104],[104, 103],[103, 105],[105, 107],[97, 106],[106, 90],[108, 86],[85, 108],[101, 107],[107, 108],[19, 93],[19, 109],[23, 110],[22, 111],[61, 112],[0, 113],[115, 114],[116, 115],[0, 116],[42, 117]]
    # 插槽位置
    thechacao = [[0, 0],[0, 0],[1, 1],[2, 0],[0, 0],[0, 1],[0, 0],[1, 1],[0, 0],[0, 1],[0, 0],[0, 1],[0, 1],[0, 2],[0, 0],[0, 1],[0, 0],[0, 0],[0, 0],[0, 1],[0, 0],[0, 1],[1, 0],[0, 0],[1, 0],[0, 1],[0, 0],[1, 0],[2, 0],[0, 1],[0, 0],[0, 0],[0, 0],[0, 1],[0, 0],[0, 1],[0, 0],[1, 0],[0, 0],[0, 0],[0, 1],[0, 1],[0, 0],[0, 0],[0, 1],[0, 1],[0, 0],[0, 0],[0, 1],[0, 0],[3, 0],[0, 0],[0, 0],[0, 0],[0, 2],[0, 0],[1, 1],[0, 0],[1, 1],[0, 2],[0, 2],[0, 2],[4, 0],[0, 0],[0, 0],[0, 0],[0, 0],[0, 2],[0, 0],[0, 1],[0, 0],[0, 0],[0, 1],[0, 0],[0, 0],[0, 0],[0, 0],[0, 0],[0, 0],[0, 0],[0, 0],[0, 0],[0, 1],[0, 0],[0, 0],[0, 0],[0, 0],[0, 0],[0, 1],[0, 1],[0, 0],[0, 0],[0, 0],[0, 1],[0, 0],[0, 1],[0, 0],[0, 0],[0, 0],[0, 1],[0, 0],[0, 1],[0, 0],[0, 2],[0, 1],[0, 1],[0, 2],[0, 0],[0, 0],[0, 2],[0, 0],[0, 1],[0, 1],[0, 1],[0, 0],[0, 2],[1, 1],[0, 0],[0, 1],[0, 0],[0, 0],[0, 2],[0, 1],[0, 1],[0, 0],[0, 1],[0, 0],[1, 0],[0, 1],[0, 1],[0, 0],[0, 0],[0, 0],[0, 1],[0, 1],[0, 1],[0, 0],[0, 1],[0, 1],[0, 0],[0, 0],[0, 0],[1, 0],[0, 1],[0, 0],[0, 0],[0, 0],[0, 0],[0, 0],[0, 0],[0, 0],[0, 1],[0, 1],[0, 0],[0, 0],[0, 0],[0, 0],[0, 0],[0, 0],[5, 0],[0, 0],[0, 1],[6, 0],[0, 0]]

    nds = []
    for i in range(len(thenodes)):
        temp = thenodetree.nodes.new(thenodes[i])
        temp.location = thelocations[i]
        nds.append(temp)

    nds[83].name = 'c_setMaterial_value'
    if obj.active_material == None:
        nds[83].inputs[2].default_value = cxl_tishicaizhi_get()
    else:
        nds[83].inputs[2].default_value = obj.active_material
    nds[2].mode='RECTANGLE'; nds[2].inputs[0].default_value=2.0; nds[2].inputs[1].default_value=2.0; nds[4].inputs[0].default_value[0]=0.0; nds[4].inputs[0].default_value[1]=0.0; nds[4].inputs[0].default_value[2]=0.0; nds[5].operation='SUBTRACT'; nds[5].inputs[0].default_value[0]=0.0; nds[5].inputs[0].default_value[1]=0.0; nds[5].inputs[0].default_value[2]=0.0; nds[5].inputs[1].default_value[0]=0.0; nds[5].inputs[1].default_value[1]=0.0; nds[5].inputs[1].default_value[2]=0.0; nds[6].operation='CEIL'; nds[6].use_clamp=False; nds[6].inputs[0].default_value=0.5; nds[7].inputs[0].default_value=1; nds[7].inputs[1].default_value[0]=0.0; nds[7].inputs[1].default_value[1]=0.0; nds[7].inputs[1].default_value[2]=0.0; nds[7].inputs[2].default_value=0.10000000149011612; nds[8].operation='DIVIDE'; nds[8].use_clamp=False; nds[8].inputs[0].default_value=0.5; nds[8].inputs[1].default_value=0.5; nds[10].operation='MULTIPLY'; nds[10].use_clamp=False; nds[10].inputs[0].default_value=0.5; nds[10].inputs[1].default_value=0.5; nds[11].inputs[0].default_value=0.0; nds[11].inputs[1].default_value=0.0; nds[11].inputs[2].default_value=0.0; nds[12].inputs[3].default_value=False; nds[12].inputs[5].default_value[0]=0.0; nds[12].inputs[5].default_value[1]=0.0; nds[12].inputs[5].default_value[2]=0.0; nds[12].inputs[6].default_value[0]=1.0; nds[12].inputs[6].default_value[1]=1.0; nds[12].inputs[6].default_value[2]=1.0; nds[13].operation='DIVIDE'; nds[13].use_clamp=False; nds[13].inputs[0].default_value=0.5; nds[13].inputs[1].default_value=2.0; nds[14].operation='ADD'; nds[14].use_clamp=False; nds[14].inputs[0].default_value=0.5; nds[14].inputs[1].default_value=2.0; nds[15].inputs[0].default_value[0]=0.0; nds[15].inputs[0].default_value[1]=0.0; nds[15].inputs[0].default_value[2]=0.0; nds[16].operation='DIVIDE'; nds[16].use_clamp=False; nds[16].inputs[0].default_value=0.5; nds[16].inputs[1].default_value=2.0; nds[17].operation='ADD'; nds[17].use_clamp=False; nds[17].inputs[0].default_value=0.5; nds[17].inputs[1].default_value=2.0; nds[18].operation='ADD'; nds[18].use_clamp=False; nds[18].inputs[0].default_value=0.5; nds[18].inputs[1].default_value=2.0; nds[20].operation='CEIL'; nds[20].use_clamp=False; nds[20].inputs[0].default_value=0.5; nds[21].operation='DIVIDE'; nds[21].use_clamp=False; nds[21].inputs[0].default_value=0.5; nds[21].inputs[1].default_value=0.5; nds[24].operation='MULTIPLY'; nds[24].use_clamp=False; nds[24].inputs[0].default_value=0.5; nds[24].inputs[1].default_value=0.5; nds[25].operation='DIVIDE'; nds[25].use_clamp=False; nds[25].inputs[0].default_value=0.5; nds[25].inputs[1].default_value=0.5; nds[26].operation='FLOOR'; nds[26].use_clamp=False; nds[26].inputs[0].default_value=0.5; nds[27].operation='MULTIPLY'; nds[27].use_clamp=False; nds[27].inputs[0].default_value=0.5; nds[27].inputs[1].default_value=2.0; nds[29].operation='ADD'; nds[29].use_clamp=False; nds[29].inputs[0].default_value=0.5; nds[29].inputs[1].default_value=2.0; nds[31].operation='MULTIPLY'; nds[31].use_clamp=False; nds[31].inputs[0].default_value=0.5; nds[31].inputs[1].default_value=2.0; nds[32].operation='MULTIPLY'; nds[32].use_clamp=False; nds[32].inputs[0].default_value=0.5; nds[32].inputs[1].default_value=2.0; nds[33].operation='SUBTRACT'; nds[33].use_clamp=False; nds[33].inputs[0].default_value=0.5; nds[33].inputs[1].default_value=2.0; nds[35].mode='NGONS'; nds[36].domain='FACE'; nds[36].scale_mode='SINGLE_AXIS'; nds[36].inputs[2].default_value=1.0; nds[36].inputs[4].default_value[0]=1.0; nds[36].inputs[4].default_value[1]=0.0; nds[36].inputs[4].default_value[2]=0.0; nds[37].mode='FACES'; nds[37].inputs[3].default_value=1.0; nds[38].inputs[0].default_value=0.0; nds[38].inputs[1].default_value=0.0; nds[38].inputs[2].default_value=0.0010000000474974513; nds[39].mode='FACES'; nds[39].inputs[3].default_value=1.0; nds[40].domain='FACE'; nds[40].scale_mode='SINGLE_AXIS'; nds[40].inputs[2].default_value=1.0; nds[40].inputs[4].default_value[0]=1.0; nds[40].inputs[4].default_value[1]=0.0; nds[40].inputs[4].default_value[2]=0.0; nds[41].inputs[0].default_value=0.0; nds[41].inputs[1].default_value=0.0; nds[41].inputs[2].default_value=0.003000000026077032; nds[43].inputs[2].default_value=False; nds[45].mode='NGONS'; nds[46].mode='FACES'; nds[46].inputs[3].default_value=1.0; nds[47].inputs[0].default_value=0.0; nds[47].inputs[1].default_value=0.0; nds[47].inputs[2].default_value=1.0; nds[48].mode='COMPONENTS'; nds[48].inputs[1].default_value[0]=0.0; nds[48].inputs[1].default_value[1]=0.0; nds[48].inputs[1].default_value[2]=0.0; nds[48].inputs[2].default_value[0]=0.0; nds[48].inputs[2].default_value[1]=0.0; nds[48].inputs[2].default_value[2]=0.0; nds[48].inputs[3].default_value[0]=1.0; nds[48].inputs[3].default_value[1]=1.0; nds[48].inputs[3].default_value[2]=1.0; nds[49].inputs[0].default_value=0.0; nds[49].inputs[1].default_value=0.0; nds[49].inputs[2].default_value=-0.5; nds[51].mode='COMPONENTS'; nds[51].inputs[1].default_value[0]=0.0; nds[51].inputs[1].default_value[1]=0.0; nds[51].inputs[1].default_value[2]=0.0; nds[51].inputs[2].default_value[0]=0.0; nds[51].inputs[2].default_value[1]=0.0; nds[51].inputs[2].default_value[2]=0.0; nds[51].inputs[3].default_value[0]=1.0; nds[51].inputs[3].default_value[1]=1.0; nds[51].inputs[3].default_value[2]=1.0; nds[53].mode='ALL'; nds[53].inputs[2].default_value=9.999999974752427e-07; nds[54].operation='INTERSECT'; nds[54].solver='EXACT'; nds[54].inputs[2].default_value=False; nds[54].inputs[3].default_value=False; nds[57].mode='ALL'; nds[57].inputs[2].default_value=1.0000000656873453e-05; nds[59].inputs[2].default_value=True; nds[59].inputs[3].default_value=0; nds[60].operation='ADD'; nds[60].use_clamp=False; nds[60].inputs[0].default_value=0.5; nds[60].inputs[1].default_value=1.0; nds[62].operation='ADD'; nds[62].use_clamp=False; nds[62].inputs[0].default_value=0.5; nds[62].inputs[1].default_value=1.0; nds[63].operation='SUBTRACT'; nds[63].use_clamp=False; nds[63].inputs[0].default_value=0.5; nds[63].inputs[1].default_value=0.0; nds[64].operation='MULTIPLY'; nds[64].use_clamp=False; nds[64].inputs[0].default_value=0.5; nds[64].inputs[1].default_value=0.5; nds[65].input_type='FLOAT'; nds[65].inputs[1].default_value=False; nds[65].inputs[2].default_value=False; nds[66].operation='FLOORED_MODULO'; nds[66].use_clamp=False; nds[66].inputs[0].default_value=0.5; nds[66].inputs[1].default_value=2.0; nds[67].data_type='FLOAT'; nds[67].operation='GREATER_THAN'; nds[67].inputs[0].default_value=0.0; nds[67].inputs[1].default_value=0.0; nds[68].operation='DIVIDE'; nds[68].use_clamp=False; nds[68].inputs[0].default_value=0.5; nds[68].inputs[1].default_value=1000.0; nds[72].domain='FACE'; nds[72].scale_mode='SINGLE_AXIS'; nds[72].inputs[2].default_value=1.0; nds[72].inputs[4].default_value[0]=0.0; nds[72].inputs[4].default_value[1]=1.0; nds[72].inputs[4].default_value[2]=0.0; nds[73].domain='FACE'; nds[73].scale_mode='SINGLE_AXIS'; nds[73].inputs[2].default_value=1.0; nds[73].inputs[4].default_value[0]=0.0; nds[73].inputs[4].default_value[1]=1.0; nds[73].inputs[4].default_value[2]=0.0; nds[74].operation='SUBTRACT'; nds[74].use_clamp=False; nds[74].inputs[0].default_value=1.0; nds[74].inputs[1].default_value=0.0; nds[75].operation='MULTIPLY'; nds[75].use_clamp=False; nds[75].inputs[0].default_value=1.0; nds[75].inputs[1].default_value=0.0; nds[76].operation='ADD'; nds[76].use_clamp=False; nds[76].inputs[0].default_value=1.0; nds[76].inputs[1].default_value=0.0; nds[77].operation='SUBTRACT'; nds[77].use_clamp=False; nds[77].inputs[0].default_value=1.0; nds[77].inputs[1].default_value=0.0; nds[79].outputs[0].default_value=0.9900000095367432; nds[80].operation='SUBTRACT'; nds[80].use_clamp=False; nds[80].inputs[0].default_value=1.0; nds[80].inputs[1].default_value=0.0; nds[81].operation='MULTIPLY'; nds[81].use_clamp=False; nds[81].inputs[0].default_value=1.0; nds[81].inputs[1].default_value=0.0; nds[82].operation='ADD'; nds[82].use_clamp=False; nds[82].inputs[0].default_value=1.0; nds[82].inputs[1].default_value=0.0; nds[85].inputs[0].default_value[0]=0.0; nds[85].inputs[0].default_value[1]=0.0; nds[85].inputs[0].default_value[2]=0.0; nds[86].operation='MODULO'; nds[86].use_clamp=False; nds[86].inputs[0].default_value=0.5; nds[86].inputs[1].default_value=2.0; nds[89].operation='MODULO'; nds[89].use_clamp=False; nds[89].inputs[0].default_value=0.5; nds[89].inputs[1].default_value=2.0; nds[90].inputs[0].default_value=0.0; nds[90].inputs[1].default_value=0.0; nds[90].inputs[2].default_value=0.0; nds[91].data_type='FLOAT_VECTOR'; nds[91].domain='POINT'; nds[91].clamp=False; nds[91].inputs[2].default_value=0; nds[94].operation='SUBTRACT'; nds[94].inputs[0].default_value[0]=0.0; nds[94].inputs[0].default_value[1]=0.0; nds[94].inputs[0].default_value[2]=0.0; nds[94].inputs[1].default_value[0]=0.0; nds[94].inputs[1].default_value[1]=0.0; nds[94].inputs[1].default_value[2]=0.0; nds[95].domain='FACE'; nds[95].inputs[2].default_value=1; nds[96].mode='ALL'; nds[96].inputs[2].default_value=1.0000000656873453e-05; nds[97].operation='MULTIPLY'; nds[97].use_clamp=False; nds[97].inputs[0].default_value=0.5; nds[97].inputs[1].default_value=0.5; nds[98].operation='DIVIDE'; nds[98].use_clamp=False; nds[98].inputs[0].default_value=1.0; nds[98].inputs[1].default_value=0.5; nds[99].operation='MULTIPLY'; nds[99].use_clamp=False; nds[99].inputs[0].default_value=0.5; nds[99].inputs[1].default_value=0.5; nds[100].operation='DIVIDE'; nds[100].use_clamp=False; nds[100].inputs[0].default_value=1.0; nds[100].inputs[1].default_value=0.5; nds[102].operation='DIVIDE'; nds[102].use_clamp=False; nds[102].inputs[0].default_value=0.5; nds[102].inputs[1].default_value=2.0; nds[103].operation='FLOOR'; nds[103].use_clamp=False; nds[103].inputs[0].default_value=0.5; nds[104].operation='MODULO'; nds[104].use_clamp=False; nds[104].inputs[0].default_value=0.5; nds[104].inputs[1].default_value=2.0; nds[105].data_type='FLOAT'; nds[105].operation='GREATER_EQUAL'; nds[105].inputs[0].default_value=0.0; nds[105].inputs[1].default_value=1.0; nds[106].operation='ADD'; nds[106].use_clamp=False; nds[106].inputs[0].default_value=0.5; nds[106].inputs[1].default_value=2.0; nds[107].input_type='FLOAT'; nds[107].inputs[1].default_value=False; nds[107].inputs[2].default_value=False; nds[108].operation='ADD'; nds[108].use_clamp=False; nds[108].inputs[0].default_value=0.0; nds[108].inputs[1].default_value=0.0; nds[115].operation='SUBTRACT'; nds[115].use_clamp=False; nds[115].inputs[0].default_value=1.0; nds[115].inputs[1].default_value=0.5; nds[116].operation='DIVIDE'; nds[116].use_clamp=False; nds[116].inputs[0].default_value=1.0; nds[116].inputs[1].default_value=1000.0; nds[117].operation='DIVIDE'; nds[117].use_clamp=False; nds[117].inputs[0].default_value=1.0; nds[117].inputs[1].default_value=1000.0



    for i in range(len(thelianxian)):
        thenodetree.links.new(nds[thelianxian[i][0]].outputs[thechacao[i][0]],nds[thelianxian[i][1]].inputs[thechacao[i][1]])
    # ---------------------
    return (thenodetree)

class cxl_extrude_modfier (bpy.types.Operator):  # 挤出
    bl_idname = "view3d.cxl_extrude_spline"  # 名称不能有大写
    bl_label = "挤出"
    suzhitiaozheng = []
    jichuobj = []
    jichuzhi = ""  # 记录挤出数值 已字符串形式  方便叠加
    pointA = None
    shikoushuaxing = False
    snapshuaxing = False

    def modal(self, context, event):
        temp = c_huoqujianpanzhi(event)
        if temp in {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.', '-'}:
            if event.value == 'PRESS':
                if len(self.jichuzhi) == 0:
                    self.jichuzhi = self.jichuzhi + temp
                elif temp != '-':
                    self.jichuzhi = self.jichuzhi + temp
            self.report({'INFO'}, "挤出值："+self.jichuzhi)
            return {'RUNNING_MODAL'}
        elif event.type == "BACK_SPACE":
            self.jichuzhi = self.jichuzhi[:-1]  # 退格
            self.report({'INFO'}, "挤出值："+self.jichuzhi)
            return {'RUNNING_MODAL'}
        elif event.type in {'RET', 'NUMPAD_ENTER'}:
            if self.jichuzhi != "":
                for i in self.suzhitiaozheng:
                    for o in i.nodes:
                        if o.name == 'c_extrude_value':
                            o.inputs[2].default_value = cc_danweishipei(
                                float(self.jichuzhi))
                context.window.cursor_set('DEFAULT')
                bpy.context.scene.c_jichu = float(self.jichuzhi)
            cxl_shizixingyichu()
            return {'CANCELLED'}
        elif event.type == 'MOUSEMOVE':
            if self.shikoushuaxing == True:
                cc_shuaxing_shikou_dingdian_2d()
                self.shikoushuaxing = False  # 视口刷新操作不能放在滚轮处  那相当于先刷新 后移动视口
            if self.snapshuaxing == True:
                cc_shuaxing_shikou_dingdian()
                self.snapshuaxing = False
            self.pointA = cxl_snaptopoint(event)
            if self.pointA != None:
                cxl_shizixingyichu()  # ---先移除现有的十字星
                cxl_shizixing(cxl3dto2d(self.pointA))
        elif event.type == "LEFTMOUSE":
            cxl_shizixingyichu()
            if self.pointA != None:
                if event.value == 'PRESS':
                    for i in self.jichuobj:
                        pos = i.location
                        duixiangshiliang = cc_duixiangshiliang(i)
                        temp = distance(self.pointA, pos)
                        dianshiliang = (Vector(cxl_jian(self.pointA, pos)))
                        # 向量间的夹角  这个值是弧度制的  math.degrees()可转换为角度 math.radians()角度转换为弧度
                        jiaodu = (duixiangshiliang.angle(dianshiliang))
                        jiaodu = (math.pi/2-jiaodu)
                        chuizhigaodu = temp*math.sin(jiaodu)
                        for i in self.suzhitiaozheng:
                            for o in i.nodes:
                                if o.name == 'c_extrude_value':
                                    o.inputs[2].default_value = chuizhigaodu
                        context.window.cursor_set('DEFAULT')
                self.report({'INFO'}, '已调整：'+str(chuizhigaodu))
            return {'CANCELLED'}
        # --------------------------------------------------------
        elif event.type in {'WHEELUPMOUSE', 'WHEELDOWNMOUSE'}:
            self.shikoushuaxing = True
            return {'PASS_THROUGH'}  # 滚轮刷新坐标显示
        elif event.type == 'MIDDLEMOUSE':
            self.snapshuaxing = True
            return {'PASS_THROUGH'}  # 中键刷新视口坐标参数
        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        selection = bpy.context.selected_objects
        js = len(selection)
        self.suzhitiaozheng = []  # 可以进行数值调整的对象
        self.jichuobj = []
        for i in selection:
            if i.type == 'CURVE':
                for i2 in i.modifiers:
                    if i2.type == 'NODES':
                        if 'c_extrude' in i2.node_group.name:
                            self.suzhitiaozheng.append(i2.node_group)
                            self.jichuobj.append(i)
                            # 检测是否有挤出操作
                js -= 1
        if len(self.suzhitiaozheng) != 0:
            self.report({'INFO'}, "提示：指定两点或输入数值")

            if context.scene.cxl_snaptoggle == True :cc_shuaxing_shikou_dingdian()
            context.window.cursor_set('CROSSHAIR')  # 光标设置为十字星
            context.window_manager.modal_handler_add(
                self)  # 这句必须要有  否则无法运行modal
            return {'RUNNING_MODAL'}  # 进入调整数值模式
        elif js == 0:
            for i in selection:
                if i.active_material == None:
                    i.active_material = cxl_tishicaizhi_get()
                temp = i.modifiers.new("cxl_extrude", 'NODES')  # 添加节点修改器
                temp.node_group = c_extrude_node_tree(i)
            return {'CANCELLED'}
        else:
            return {'CANCELLED'}

##################################################################


class cxl_flip(bpy.types.Operator):  # 翻转面
    bl_idname = "view3d.cxl_flipface"  # 名称不能有大写
    bl_label = "flipface"

    def execute(self, context):
        edit_mode = context.mode
        if edit_mode == "OBJECT":
            selection = bpy.context.selected_objects
            for i in selection:
                if i.type == 'MESH':
                    i.data.flip_normals()
                Update3DViewPorts()
        return {'FINISHED'}


class cxl_xyz_uvwmap_modfier (bpy.types.Operator):
    bl_idname = "view3d.cxl_xyz_uvwmap"  # 名称不能有大写
    bl_label = "uvw贴图"

    def execute(self, context):
        selection = [
            i for i in context.selected_objects if i.type in ['CURVE', 'MESH']]
        if len(selection) > 0:
            tikuai = cc_jisuanxuanzheduixiantijikuang()  # 选中对象体块
            daxiao = cxl_jian(tikuai[0], tikuai[1])
            zhongxingdian = cc_jisuanzhongxingdian(tikuai)

            new_uvwmap = c_xyz_uvmap_node_tree()
            for i in selection:
                ipiancha = cxl_jian(zhongxingdian, i.location)
                temp = i.modifiers.new("cxl_xyz_uvwmap", 'NODES')  # 添加节点修改器
                temp.node_group = new_uvwmap
                temp["Socket_1"][0] = daxiao[0]
                temp["Socket_1"][1] = daxiao[1]
                temp["Socket_1"][2] = daxiao[2]
                temp["Socket_2"][0] = ipiancha[0]
                temp["Socket_2"][1] = ipiancha[1]
                temp["Socket_2"][2] = ipiancha[2]
                temp["Socket_5_attribute_name"] = 'c_uv'
                cxl_obj_tex_image_shuxing_tianjia(i)
        return {'FINISHED'}

class cxl_pinmian_modfier (bpy.types.Operator):
    bl_idname = "view3d.cxl_pinmian_modfier"  # 名称不能有大写
    bl_label = "平面"

    def execute(self, context):
        selection = [i for i in context.selected_objects if i.type =='CURVE']
        if len(selection) > 0:
            new_pinmian = c_pingmian_node_tree(selection[0])
            for i in selection:
                if i.active_material == None:
                    i.active_material = cxl_tishicaizhi_get()
                temp = i.modifiers.new("cxl_pingmian", 'NODES')  # 添加节点修改器
                temp.node_group = new_pinmian
                temp["Socket_3_attribute_name"] = 'c_uv'
        return {'FINISHED'}

class cxl_zhuankuai_modfier (bpy.types.Operator):
    bl_idname = "view3d.cxl_zhuankuai_modfier"  # 名称不能有大写
    bl_label = "砖块"

    def execute(self, context):
        selection = [i for i in context.selected_objects if i.type =='CURVE']
        if len(selection) > 0:
            new_zhuankuai = c_zhuankuai_node_tree(selection[0])
            for i in selection:
                if i.active_material == None:
                    i.active_material = cxl_tishicaizhi_get()
                temp = i.modifiers.new("cxl_zhuankuai", 'NODES')  # 添加节点修改器
                temp.node_group = new_zhuankuai
                temp["Socket_8_attribute_name"]= 'c_uv'
        return {'FINISHED'}

class cxl_caizhi_c_uv_tianjia (bpy.types.Operator):
    bl_idname = "view3d.cxl_caizhi_c_uv_tianjia"  # 名称不能有大写
    bl_label = "c_uv 添加"

    def execute(self, context):
        selection = [i for i in context.selected_objects if i.active_material != None ]
        if len(selection) > 0:
            for i in selection:
                cxl_obj_tex_image_shuxing_tianjia(i)
        return {'FINISHED'}

