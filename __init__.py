bl_info = {
    "name": "72craft的小插件",
    "description" : "Blender MMD小插件",
    "author": "72craft",
    "version": (0, 4, 0),
    "blender": (4, 5, 0),
    "location": "View3D UI",
    "category": "Render",
    "doc_url": "https://github.com/A72craft",
    "tracker_url": "https://github.com/A72craft",
    "license": "GPL"
}

import bpy
import mathutils
import importlib

# Import constants first (no reload needed)
from . import constants
from .constants import POSE_BONES

# Import modules first
from . import compositor
from . import output
from . import effect
from . import presets

# Force reload modules when addon is reloaded (useful during development)
# This ensures changes to compositor.py, output.py, effect.py, and presets.py are picked up
try:
    importlib.reload(compositor)
except:
    pass
try:
    importlib.reload(output)
except:
    pass
try:
    importlib.reload(effect)
except:
    pass
try:
    importlib.reload(presets)
except:
    pass

# Import classes after reload
from .compositor import *
from .output import *
from .effect import *
from .presets import *


class Pose(bpy.types.Operator):
    """归类常用骨骼"""
    bl_idname = "pose.isolate_bones_by_name"
    bl_label = "Isolate Selected Bones by Name"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        # This operator is only active in Pose Mode with an active armature
        return (context.active_object is not None and 
                context.active_object.type == 'ARMATURE')
        
    def execute(self, context):
        target_bones = POSE_BONES
        
        armature_obj = context.active_object
        armature_data = armature_obj.data

        if not armature_data:
            self.report({'WARNING'}, "未选择骨骼!")
            return {'CANCELLED'}

        # --- 1. Filter the selection ---
        # Create a new list containing ONLY the selected bones that are in our target set.
        bones_to_process = [bone for bone in armature_data.bones
                            if bone.name in target_bones]

        if not bones_to_process:
            self.report({'ERROR'},"无任何骨骼名称匹配")
            return {'CANCELLED'}
        
        
        # --- 2. Hide all existing bone collections ---
        for bc in armature_data.collections:
            bc.is_visible = False

        # --- 3. Create ONE collection named "core" ---
        # Define the name for your single collection
        core_collection_name = "核心"
        
        # Get the "core" collection if it exists, otherwise create it
        core_collection = armature_data.collections.get(core_collection_name)
        if not core_collection:
            core_collection = armature_data.collections.new(name=core_collection_name)
        
        # Make sure this single collection is visible
        core_collection.is_visible = True

        # --- 4. Assign ALL matching bones to the "core" collection ---
        for bone in bones_to_process:
            # Get the corresponding pose bone
            pose_bone = armature_obj.pose.bones.get(bone.name)
            if pose_bone:
                # Assign this bone to the single "core" collection
                core_collection.assign(pose_bone)
        
        self.report({'INFO'}, f"{len(bones_to_process)}/52" \
            " 个骨骼被选中并分类")
        return {'FINISHED'}


# ------------------------------------------------------------------
class UI_Effect(bpy.types.Panel):
    bl_category = "72craft"   #侧边栏标签
    bl_label = "特效"     #工具卷展栏标签
    bl_idname = "OBJECT_effect_set"   #工具ID
    bl_space_type = 'VIEW_3D'   #空间类型():3D视图
    bl_region_type = 'UI'       #区域类型:右边侧栏
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        row1 = self.layout.row(align=True)
        row1.scale_y=1
        row1.operator(Blush.bl_idname,text="设置脸红效果",icon="MATERIAL_DATA")
        row1.operator(RemoveBlush.bl_idname,text="",icon="TRASH")
        row2 = self.layout.row(align=True)  
     
class UI_Pose(bpy.types.Panel):
    bl_category = "72craft"   #侧边栏标签
    bl_label = "动作"     #工具卷展栏标签
    bl_idname = "OBJECT_poses_set"   #工具ID
    bl_space_type = 'VIEW_3D'   #空间类型():3D视图
    bl_region_type = 'UI'       #区域类型:右边侧栏
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):  
        row1 = self.layout.row(align=True)
        row1.scale_y=1
        row1.operator(Pose.bl_idname,text="分类骨骼",icon='BONE_DATA')
        
class UI_Output(bpy.types.Panel):
    bl_category = "72craft"   #侧边栏标签
    bl_label = "输出"     #工具卷展栏标签
    bl_idname = "OBJECT_output_set"   #工具ID
    bl_space_type = 'VIEW_3D'   #空间类型():3D视图
    bl_region_type = 'UI'       #区域类型:右边侧栏
    
    def draw(self, context):  
        row_res = self.layout.row(align=True)
        row_res.prop(context.scene.render, "resolution_x", text="X")
        row_res.prop(context.scene.render, "resolution_y", text="Y")
        
        row_preset = self.layout.row(align=True)
        row_preset.scale_y=1
        row_preset.operator(P1080.bl_idname,text="1080p",icon="RENDER_RESULT")
        row_preset.operator(P2K.bl_idname,text="2K",icon="RENDER_RESULT")
        row_preset.operator(P4K.bl_idname,text="4K",icon="RENDER_RESULT")
        
        row1 = self.layout.row(align=True)
        row1.scale_y=1
        row1.operator(Horizontal.bl_idname,text="横屏",icon="ORIENTATION_GIMBAL")
        row1.operator(Vertical.bl_idname,text="竖屏",icon="ORIENTATION_GIMBAL")
        row2 = self.layout.row(align=True)
        row2.scale_y=1
        row2.operator(Hz30.bl_idname,text="30Hz",icon="TIME")
        row2.operator(Hz60.bl_idname,text="60Hz",icon="TIME")
        
class UI_Composit(bpy.types.Panel):
    bl_category = "72craft"   #侧边栏标签
    bl_label = "合成"     #工具卷展栏标签
    bl_idname = "OBJECT_composit_set"   #工具ID
    bl_space_type = 'VIEW_3D'   #空间类型():3D视图
    bl_region_type = 'UI'       #区域类型:右边侧栏
    
    def draw(self, context):
        row1 = self.layout.row(align=True)
        row1.scale_y=1
        row1.operator(AOV.bl_idname,text="1.设置AOV输出",icon="MATERIAL_DATA") 
        row2 = self.layout.row(align=True)
        row2.scale_y=1
        row2.operator(Compositor.bl_idname,text="2.设置合成器",icon="SCENE_DATA")


# ------------------------------------------------------------------

classes = [
    ImportMatPresetsUI,UI_Effect,UI_Pose,UI_Output,UI_Composit,
    Blush,RemoveBlush,
    Compositor,AOV,Pose,
    Horizontal,Vertical,Hz30,Hz60,P1080,P2K,P4K,
    ImportMatPresets
]


# Functions to register and unregister the addon
def register():
    for clss in classes:
        bpy.utils.register_class(clss)

def unregister():
    for clss in classes:
        bpy.utils.unregister_class(clss)

# This allows the script to be run directly in Blender's Text Editor for testing
if __name__ == "__main__":
    register()
