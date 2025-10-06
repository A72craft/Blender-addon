bl_info = {
    "name": "72craft的小插件",
    "description" : "添加眼透&刘海阴影&辉光的小插件",
    "author": "72craft",
    "version": (1, 0, 2),
    "blender": (4, 3, 0),
    "location": "View3D UI",
    "category": "Render",
    "doc_url": "https://github.com/A72craft",
    "tracker_url": "https://github.com/A72craft",
    "license": "GPL"
}

import bpy
import mathutils

from .compositor import *
from .output import *

class Compositor(bpy.types.Operator):
    """设置合成器相关设置和节点"""
    # Unique ID for the operator
    bl_idname = "render.compositor_setup"
    # Name that appears in the Blender search menu
    bl_label = "72craft_设置合成器"

    # The execute() function runs when the operator is called
    def execute(self, context):
        # The main action: print the message
        context.view_layer.use_pass_z = True
        bpy.context.view_layer.eevee.use_pass_transparent = True
        
        bpy.context.scene.use_nodes = True
        
        new_scene = generate_compositor_scene()
        
        if new_scene:
            # --- 3. Report Success to the User ---
            self.report({'INFO'}, f"已设置合成器相关设置！")
            return {'FINISHED'}
        else:
            # --- 4. Report Failure if something went wrong ---
            self.report({'ERROR'}, "未能设置合成器")
            return {'CANCELLED'}

class AOV(bpy.types.Operator):
    """设置AOV输出,并在相应材质中添加AOV节点"""
    bl_idname = "render.aov_setup"
    
    bl_label = "72craft_设置AOV"
    
    def execute(self, context):
        view_layer = context.view_layer
        warning_flag = False
        # --- Define the list of AOV names we want to add ---
        aovs = {
            "face": 'COLOR',
            "eye_val": 'VALUE',
            "eye_mat": 'COLOR'
        }
        
        for name,aov_type in aovs.items():
            # Check if the AOV already exists to avoid duplicates
            if name not in view_layer.aovs:
                # If it doesn't exist, create it.
                new_aov = view_layer.aovs.add()
                new_aov.name = name
                new_aov.type = aov_type
            else:
                pass
        
        eye_mat = ["眉睫","白目","目","目光","眉毛","眼白","眼睛"]
        face_mat = ["顏","脸","颜","脸"]
        hair_mat = ["头发","髪"]
        eye_cnt = len(eye_mat)
        
        
        found_face = False
        for material in bpy.data.materials:
            # Check if the material's name is in our target list
            if material.name in face_mat:
                found_face = True
                tree = material.node_tree
                aov_output_node = tree.nodes.new(type='ShaderNodeOutputAOV')
                aov_output_node.aov_name = "face"
                aov_output_node.inputs['Color'].default_value = (1.0, 1.0, 1.0, 1.0)
            if material.name in eye_mat:
                eye_cnt-=1
                tree = material.node_tree
                aov_mat = tree.nodes.new(type='ShaderNodeOutputAOV')
                aov_mat.aov_name = "eye_mat"
                aov_val = tree.nodes.new(type='ShaderNodeOutputAOV')
                aov_val.aov_name = "eye_val"
                aov_val.inputs['Value'].default_value = 1.0
                for node in tree.nodes:
                        if node.type == 'TEX_IMAGE':
                            image_texture_node = node #there should be only one
                tree.links.new(image_texture_node.outputs[0],aov_mat.inputs[0])
                aov_mat.location.y += 750
                aov_val.location.y += 600
            if material.name in hair_mat:
                material.blend_method = 'BLEND'
                material.show_transparent_back = False

                
        
        if not found_face:
            warning_flag = True
            print("未找到面部材质!")
            
        if eye_cnt != 0:
            print("眼部透视部分材质缺失!")
        
        
        if warning_flag:
            self.report({'WARNING'}, "出现错误,请查看日志!")
        else:
            self.report({'INFO'}, "已成功设置AOV!")
        
        return {'FINISHED'}

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

        target_bones = {
            #center
            "両目","頭","首","上半身2","上半身","下半身","腰","グルーブ",
            # Left Bones (.L)
            "左肩","左腕","左腕捩","左ひじ","左手捩","左手首","左親指０",
            "左親指１","左親指２","左小指１","左薬指１","左中指１","左人指１",
            "左小指２","左薬指２","左中指２","左人指２",
            "左小指３","左薬指３","左中指３","左人指３",
            "肩.L", "腕.L", "腕捩.L", "ひじ.L", "手捩.L", "手首.L", "親指０.L",
            "親指１.L", "親指２.L", "人指１.L", "人指２.L", "人指３.L", "中指１.L",
            "中指２.L", "中指３.L", "薬指１.L", "薬指２.L", "薬指３.L", "小指１.L",
            "小指２.L", "小指３.L", "足ＩＫ.L",
            # Right Bones (.R)
            "右肩","右腕","右腕捩","右ひじ","右手捩","右手首","右親指０",
            "右親指１","右親指２","右小指１","右薬指１","右中指１","右人指１",
            "右小指２","右薬指２","右中指２","右人指２",
            "右小指３","右薬指３","右中指３","右人指３",
            "右足ＩＫ","左足ＩＫ",
            "肩.R", "腕.R", "腕捩.R", "ひじ.R", "手捩.R", "手首.R", "親指０.R",
            "親指１.R", "親指２.R", "人指１.R", "人指２.R", "人指３.R", "中指１.R",
            "中指２.R", "中指３.R", "薬指１.R", "薬指２.R", "薬指３.R", "小指１.R",
            "小指２.R", "小指３.R", "足ＩＫ.R"
        }
        
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
class UI_Material(bpy.types.Panel):
    bl_category = "72craft"   #侧边栏标签
    bl_label = "眼透&刘海阴影&辉光"     #工具卷展栏标签
    bl_idname = "OBJECT_material_set"   #工具ID
    bl_space_type = 'VIEW_3D'   #空间类型():3D视图
    bl_region_type = 'UI'       #区域类型:右边侧栏
    
    def draw(self, context):  
        row1 = self.layout.row(align=True)
        row1.scale_y=1
        row1.operator(AOV.bl_idname,text="1.设置AOV输出",icon="MATERIAL_DATA") 
        row2 = self.layout.row(align=True)
        row2.scale_y=1
        row2.operator(Compositor.bl_idname,text="2.设置合成器",icon="SCENE_DATA")
        
class UI_Pose(bpy.types.Panel):
    bl_category = "72craft"   #侧边栏标签
    bl_label = "动作"     #工具卷展栏标签
    bl_idname = "OBJECT_poses_set"   #工具ID
    bl_space_type = 'VIEW_3D'   #空间类型():3D视图
    bl_region_type = 'UI'       #区域类型:右边侧栏
    
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
        row1 = self.layout.row(align=True)
        row1.scale_y=1
        row1.operator(Horizontal.bl_idname,text="横屏")
        row1.operator(Vertical.bl_idname,text="竖屏")
        row2 = self.layout.row(align=True)
        row2.scale_y=1
        row2.operator(Hz30.bl_idname,text="30Hz")
        row2.operator(Hz60.bl_idname,text="60Hz")
# ------------------------------------------------------------------

classes = [
    UI_Material,UI_Pose,UI_Output,
    Compositor,AOV,Pose,
    Horizontal,Vertical,Hz30,Hz60
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
