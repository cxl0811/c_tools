'''
    This part of the script originaly made by MACHIN3, machin3.io, support@machin3.io 

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

'''
#脚本快捷键注册借鉴了quick_groups 插件的方式  并做了修改 



import bpy
from .keys import cxl_keys 

#--------------------------------------------
cxl_keymaps=[]
cxl_keylists = cxl_keys ["MENU"]


def cxl_register_keymaps():
    global cxl_keylists , cxl_keymaps
    cxl_keymaps = []

    keymaps = bpy.context.window_manager.keyconfigs.addon.keymaps
    if 'Object Mode' not in keymaps:
        keymaps.new(name='Object Mode', space_type='EMPTY',region_type='WINDOW')
    if '3D View' not in keymaps :
        keymaps.new(name='3D View', space_type='VIEW_3D',region_type='WINDOW')
    for i in cxl_keylists:
        kongjian = i.get("keymap")
        km = keymaps[kongjian] 
        iidname = i.get("idname")
        itype = i.get("type")
        ivalue = i.get("value")
        ishift = i.get("shift", False)
        ictrl = i.get("ctrl", False)
        ialt = i.get("alt", False)
        kmi = km.keymap_items.new(iidname, type=itype, value=ivalue, shift=ishift, ctrl=ictrl, alt=ialt)
        properties = i.get("properties")
        if properties:
            for name, value in properties:
                setattr(kmi.properties, name, value)
        cxl_keymaps.append((km, kmi))

#------------------------------
def cxl_unregister_keymaps():
    global cxl_keymaps
    for km, kmi in cxl_keymaps:
        km.keymap_items.remove(kmi)
    cxl_keymaps=[]
#------------------------------------------------------------


                        