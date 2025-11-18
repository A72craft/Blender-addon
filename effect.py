import bpy
import mathutils
from .constants import *

def get_blush_material(mesh_obj):
    """Helper function to get blush material from the active mesh, returns first found or None"""
    if not mesh_obj or mesh_obj.type != 'MESH':
        return None
    # Check materials assigned to the mesh
    for material_slot in mesh_obj.material_slots:
        if material_slot.material is None:
            continue
        mat = material_slot.material
        # Check if material name matches any in the list
        if mat.name in MATERIAL_BLUSH:
            return mat
    return None

def get_blush_factor(mesh_obj):
    """Helper function to get current blush factor value from active mesh, returns None if not found"""
    mat = get_blush_material(mesh_obj)
    if not mat or not mat.node_tree:
        return None
    node_group = bpy.data.node_groups.get("脸红节点")
    if not node_group:
        return None
    for node in mat.node_tree.nodes:
        if node.type == 'GROUP' and node.node_tree == node_group:
            try:
                return node.inputs['脸红系数'].default_value
            except (KeyError, IndexError):
                return None
    return None

class Blush(bpy.types.Operator):
    """设置脸红"""
    bl_idname = "render.blush_setup"
    bl_label = "72craft_脸红"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        if not (context.active_object is not None and 
                context.active_object.type == 'MESH' and 
                context.active_object.select_get()):
            return False
        # Only enable if blush factor is not already 1
        factor = get_blush_factor(context.active_object)
        return factor is None or factor < 0.99
    
    def execute(self, context):
        # Get the selected mesh object
        selected_mesh = context.active_object
        if not selected_mesh or selected_mesh.type != 'MESH':
            self.report({'ERROR'}, "请选择一个网格对象!")
            return {'CANCELLED'}
        
        # Find the material from the selected mesh
        mat = get_blush_material(selected_mesh)
        if mat is None:
            mat_names_str = ", ".join(MATERIAL_BLUSH)
            self.report({'WARNING'}, f"未找到材质 ({mat_names_str})")
            return {'CANCELLED'}
        
        if not mat.use_nodes:
            mat.use_nodes = True
        
        # Check if node group already exists, if so, reuse it
        blush_node_group = bpy.data.node_groups.get("脸红节点")
        
        if blush_node_group is None:
            # Create the node group if it doesn't exist
            blush_node_group = create_blush_node_group()
        
        # Add the node group to the material's node tree
        tree = mat.node_tree
        if tree is None:
            self.report({'ERROR'}, "材质节点树不存在!")
            return {'CANCELLED'}
        
        # Check if the node group is already added
        group_node = None
        for node in tree.nodes:
            if node.type == 'GROUP' and node.node_tree == blush_node_group:
                group_node = node
                break
        
        if group_node is None:
            # Add the node group node to the material
            group_node = tree.nodes.new(type='ShaderNodeGroup')
            group_node.name = "脸红节点"
            group_node.node_tree = blush_node_group
            group_node.location = (0, 0)
        else:
            # If node already exists, set blush factor to 1
            try:
                group_node.inputs['脸红系数'].default_value = 1.0
            except (KeyError, IndexError):
                pass
        
        # Find mmd_base_tex node
        mmd_base_tex = None
        for node in tree.nodes:
            if node.type == 'TEX_IMAGE' and node.name == "mmd_base_tex":
                mmd_base_tex = node
                break
        
        # Connect alpha from mmd_base_tex to blush node group's alpha input
        if mmd_base_tex is not None:
            try:
                tree.links.new(mmd_base_tex.outputs['Alpha'], group_node.inputs['颜赤'])
            except (KeyError, IndexError) as e:
                self.report({'WARNING'}, f"无法连接Alpha到颜赤: {e}")
        else:
            self.report({'WARNING'}, "未找到mmd_base_tex节点，请先添加基础纹理节点")
        
        # Find Material Output node
        material_output = None
        for node in tree.nodes:
            if node.type == 'OUTPUT_MATERIAL':
                material_output = node
                break
        
        # Connect blush node group's Shader output to Material Output
        if material_output is not None:
            try:
                tree.links.new(group_node.outputs['Shader'], material_output.inputs['Surface'])
            except (KeyError, IndexError) as e:
                self.report({'WARNING'}, f"无法连接Shader到Material Output: {e}")
        else:
            self.report({'WARNING'}, "未找到Material Output节点")
        
        mat_name = mat.name if mat else MATERIAL_BLUSH[0]
        self.report({'INFO'}, f"已添加节点组到材质 {mat_name} 并连接节点")
        return {'FINISHED'}

class RemoveBlush(bpy.types.Operator):
    """移除脸红效果"""
    bl_idname = "render.blush_remove"
    bl_label = "72craft_移除脸红"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        if not (context.active_object is not None and 
                context.active_object.type == 'MESH' and 
                context.active_object.select_get()):
            return False
        # Only enable if blush factor is not already 0
        factor = get_blush_factor(context.active_object)
        return factor is None or factor > 0.01
    
    def execute(self, context):
        # Get the selected mesh object
        selected_mesh = context.active_object
        if not selected_mesh or selected_mesh.type != 'MESH':
            self.report({'ERROR'}, "请选择一个网格对象!")
            return {'CANCELLED'}
        
        # Find the material from the selected mesh
        mat = get_blush_material(selected_mesh)
        
        if mat is None:
            mat_names_str = ", ".join(MATERIAL_BLUSH)
            self.report({'WARNING'}, f"未找到材质 ({mat_names_str})")
            return {'CANCELLED'}
        
        tree = mat.node_tree
        if tree is None:
            self.report({'WARNING'}, "材质节点树不存在!")
            return {'CANCELLED'}
        
        # Find the blush node group
        blush_node_group = bpy.data.node_groups.get("脸红节点")
        
        if blush_node_group is None:
            self.report({'WARNING'}, "未找到脸红节点组")
            return {'CANCELLED'}
        
        # Find the blush node group node in the material
        group_node = None
        for node in tree.nodes:
            if node.type == 'GROUP' and node.node_tree == blush_node_group:
                group_node = node
                break
        
        if group_node is None:
            self.report({'WARNING'}, "材质中未找到脸红节点")
            return {'CANCELLED'}
        
        # Set blush factor to 0 instead of removing the node
        try:
            group_node.inputs['脸红系数'].default_value = 0.0
            self.report({'INFO'}, f"已设置材质 {mat.name} 中的脸红系数为 0")
        except (KeyError, IndexError) as e:
            self.report({'WARNING'}, f"无法设置脸红系数: {e}")
            return {'CANCELLED'}
        
        return {'FINISHED'}

def mmdtexuv_001_node_group():
        """Initialize MMDTexUV.001 node group"""
        mmdtexuv_001 = bpy.data.node_groups.new(type='ShaderNodeTree', name="MMDTexUV.001")

        mmdtexuv_001.color_tag = 'NONE'
        mmdtexuv_001.description = ""
        mmdtexuv_001.default_group_node_width = 140
        # mmdtexuv_001 interface

        # Socket Base UV
        base_uv_socket = mmdtexuv_001.interface.new_socket(name="Base UV", in_out='OUTPUT', socket_type='NodeSocketVector')
        base_uv_socket.default_value = (0.0, 0.0, 0.0)
        base_uv_socket.min_value = -10.0
        base_uv_socket.max_value = 10.0
        base_uv_socket.subtype = 'NONE'
        base_uv_socket.attribute_domain = 'POINT'
        base_uv_socket.default_input = 'VALUE'
        base_uv_socket.structure_type = 'AUTO'

        # Socket Toon UV
        toon_uv_socket = mmdtexuv_001.interface.new_socket(name="Toon UV", in_out='OUTPUT', socket_type='NodeSocketVector')
        toon_uv_socket.default_value = (0.0, 0.0, 0.0)
        toon_uv_socket.min_value = -10.0
        toon_uv_socket.max_value = 10.0
        toon_uv_socket.subtype = 'NONE'
        toon_uv_socket.attribute_domain = 'POINT'
        toon_uv_socket.default_input = 'VALUE'
        toon_uv_socket.structure_type = 'AUTO'

        # Socket Sphere UV
        sphere_uv_socket = mmdtexuv_001.interface.new_socket(name="Sphere UV", in_out='OUTPUT', socket_type='NodeSocketVector')
        sphere_uv_socket.default_value = (0.0, 0.0, 0.0)
        sphere_uv_socket.min_value = -10.0
        sphere_uv_socket.max_value = 10.0
        sphere_uv_socket.subtype = 'NONE'
        sphere_uv_socket.attribute_domain = 'POINT'
        sphere_uv_socket.default_input = 'VALUE'
        sphere_uv_socket.structure_type = 'AUTO'

        # Socket SubTex UV
        subtex_uv_socket = mmdtexuv_001.interface.new_socket(name="SubTex UV", in_out='OUTPUT', socket_type='NodeSocketVector')
        subtex_uv_socket.default_value = (0.0, 0.0, 0.0)
        subtex_uv_socket.min_value = -10.0
        subtex_uv_socket.max_value = 10.0
        subtex_uv_socket.subtype = 'NONE'
        subtex_uv_socket.attribute_domain = 'POINT'
        subtex_uv_socket.default_input = 'VALUE'
        subtex_uv_socket.structure_type = 'AUTO'

        # Initialize mmdtexuv_001 nodes

        # Node Group Output
        group_output = mmdtexuv_001.nodes.new("NodeGroupOutput")
        group_output.name = "Group Output"
        group_output.is_active_output = True

        # Node Texture Coordinate
        texture_coordinate = mmdtexuv_001.nodes.new("ShaderNodeTexCoord")
        texture_coordinate.name = "Texture Coordinate"
        texture_coordinate.from_instancer = False

        # Node UV Map
        uv_map = mmdtexuv_001.nodes.new("ShaderNodeUVMap")
        uv_map.name = "UV Map"
        uv_map.from_instancer = False
        uv_map.uv_map = "UV1"

        # Node Vector Transform
        vector_transform = mmdtexuv_001.nodes.new("ShaderNodeVectorTransform")
        vector_transform.name = "Vector Transform"
        vector_transform.convert_from = 'OBJECT'
        vector_transform.convert_to = 'CAMERA'
        vector_transform.vector_type = 'NORMAL'

        # Node Mapping
        mapping = mmdtexuv_001.nodes.new("ShaderNodeMapping")
        mapping.name = "Mapping"
        mapping.vector_type = 'POINT'
        # Location
        mapping.inputs[1].default_value = (0.5, 0.5, 0.0)
        # Rotation
        mapping.inputs[2].default_value = (0.0, 0.0, 0.0)
        # Scale
        mapping.inputs[3].default_value = (0.5, 0.5, 1.0)

        # Set locations
        group_output.location = (1260.0, 0.0)
        texture_coordinate.location = (0.0, 0.0)
        uv_map.location = (840.0, -440.0)
        vector_transform.location = (210.0, -220.0)
        mapping.location = (420.0, -220.0)

        # Set dimensions
        group_output.width, group_output.height = 140.0, 100.0
        texture_coordinate.width, texture_coordinate.height = 140.0, 100.0
        uv_map.width, uv_map.height = 150.0, 100.0
        vector_transform.width, vector_transform.height = 140.0, 100.0
        mapping.width, mapping.height = 140.0, 100.0

        # Initialize mmdtexuv_001 links

        # texture_coordinate.Normal -> vector_transform.Vector
        mmdtexuv_001.links.new(texture_coordinate.outputs[1], vector_transform.inputs[0])
        # vector_transform.Vector -> mapping.Vector
        mmdtexuv_001.links.new(vector_transform.outputs[0], mapping.inputs[0])
        # texture_coordinate.UV -> group_output.Base UV
        mmdtexuv_001.links.new(texture_coordinate.outputs[2], group_output.inputs[0])
        # mapping.Vector -> group_output.Toon UV
        mmdtexuv_001.links.new(mapping.outputs[0], group_output.inputs[1])
        # mapping.Vector -> group_output.Sphere UV
        mmdtexuv_001.links.new(mapping.outputs[0], group_output.inputs[2])
        # uv_map.UV -> group_output.SubTex UV
        mmdtexuv_001.links.new(uv_map.outputs[0], group_output.inputs[3])

        return mmdtexuv_001

def create_blush_node_group():
    """Initialize 脸红节点 node group"""
    ____ = bpy.data.node_groups.new(type='ShaderNodeTree', name="脸红节点")

    ____.color_tag = 'NONE'
    ____.description = ""
    ____.default_group_node_width = 140
    # ____ interface

    # Socket Shader
    shader_socket = ____.interface.new_socket(name="Shader", in_out='OUTPUT', socket_type='NodeSocketShader')
    shader_socket.attribute_domain = 'POINT'
    shader_socket.default_input = 'VALUE'
    shader_socket.structure_type = 'AUTO'

    # Socket 颜赤
    ___socket = ____.interface.new_socket(name="颜赤", in_out='INPUT', socket_type='NodeSocketFloat')
    ___socket.default_value = 0.5
    ___socket.min_value = 0.0
    ___socket.max_value = 1.0
    ___socket.subtype = 'FACTOR'
    ___socket.attribute_domain = 'POINT'
    ___socket.description = "颜赤Alpha贴图的连接点"
    ___socket.default_input = 'VALUE'
    ___socket.structure_type = 'AUTO'

    # Socket 脸红系数
    _____socket = ____.interface.new_socket(name="脸红系数", in_out='INPUT', socket_type='NodeSocketFloat')
    _____socket.default_value = 1.0
    _____socket.min_value = 0.0
    _____socket.max_value = 1.0
    _____socket.subtype = 'FACTOR'
    _____socket.attribute_domain = 'POINT'
    _____socket.default_input = 'VALUE'
    _____socket.structure_type = 'AUTO'

    # Socket 脸红颜色
    _____socket_1 = ____.interface.new_socket(name="脸红颜色", in_out='INPUT', socket_type='NodeSocketColor')
    _____socket_1.default_value = (1.0, 0.004592727404087782, 0.0019137747585773468, 1.0)
    _____socket_1.attribute_domain = 'POINT'
    _____socket_1.description = "脸红使用的颜色"
    _____socket_1.default_input = 'VALUE'
    _____socket_1.structure_type = 'AUTO'

    # Socket 关闭脸黑
    _____socket_2 = ____.interface.new_socket(name="关闭脸黑", in_out='INPUT', socket_type='NodeSocketBool')
    _____socket_2.default_value = True
    _____socket_2.attribute_domain = 'POINT'
    _____socket_2.description = "是否关闭脸黑效果"
    _____socket_2.default_input = 'VALUE'
    _____socket_2.structure_type = 'AUTO'

    # Initialize ____ nodes

    # Node 组输出
    ___ = ____.nodes.new("NodeGroupOutput")
    ___.name = "组输出"
    ___.is_active_output = True

    # Node 组输入
    ____1 = ____.nodes.new("NodeGroupInput")
    ____1.name = "组输入"

    # Node 自发光
    ____2 = ____.nodes.new("ShaderNodeEmission")
    ____2.name = "自发光"

    # Node 透明 BSDF
    ___bsdf = ____.nodes.new("ShaderNodeBsdfTransparent")
    ___bsdf.name = "透明 BSDF"
    # Color
    ___bsdf.inputs[0].default_value = (1.0, 1.0, 1.0, 1.0)

    # Node 混合着色器
    _____ = ____.nodes.new("ShaderNodeMixShader")
    _____.name = "混合着色器"

    # Node 透明 BSDF.001
    ___bsdf_001 = ____.nodes.new("ShaderNodeBsdfTransparent")
    ___bsdf_001.name = "透明 BSDF.001"
    # Color
    ___bsdf_001.inputs[0].default_value = (1.0, 1.0, 1.0, 1.0)

    # Node 混合着色器.001
    ______001 = ____.nodes.new("ShaderNodeMixShader")
    ______001.name = "混合着色器.001"

    # Node 运算
    __ = ____.nodes.new("ShaderNodeMath")
    __.name = "运算"
    __.operation = 'MULTIPLY'
    __.use_clamp = False
    # Value_001
    __.inputs[1].default_value = 6.0

    # Set locations
    ___.location = (401.39227294921875, 0.0)
    ____1.location = (-821.1004028320312, 28.859390258789062)
    ____2.location = (-211.3922882080078, 111.3023681640625)
    ___bsdf.location = (-211.39210510253906, -30.5838623046875)
    _____.location = (27.11943817138672, 39.6968994140625)
    ___bsdf_001.location = (12.645709991455078, -161.8624725341797)
    ______001.location = (211.3922882080078, -18.75439453125)
    __.location = (-520.751220703125, -70.71031951904297)

    # Set dimensions
    ___.width, ___.height = 140.0, 100.0
    ____1.width, ____1.height = 140.0, 100.0
    ____2.width, ____2.height = 140.0, 100.0
    ___bsdf.width, ___bsdf.height = 140.0, 100.0
    _____.width, _____.height = 140.0, 100.0
    ___bsdf_001.width, ___bsdf_001.height = 140.0, 100.0
    ______001.width, ______001.height = 140.0, 100.0
    __.width, __.height = 140.0, 100.0

    # Initialize ____ links

    # ____2.Emission -> _____.Shader
    ____.links.new(____2.outputs[0], _____.inputs[2])
    # ___bsdf_001.BSDF -> ______001.Shader
    ____.links.new(___bsdf_001.outputs[0], ______001.inputs[1])
    # ___bsdf.BSDF -> _____.Shader
    ____.links.new(___bsdf.outputs[0], _____.inputs[1])
    # _____.Shader -> ______001.Shader
    ____.links.new(_____.outputs[0], ______001.inputs[2])
    # ____1.颜赤 -> _____.Fac
    ____.links.new(____1.outputs[0], _____.inputs[0])
    # ______001.Shader -> ___.Shader
    ____.links.new(______001.outputs[0], ___.inputs[0])
    # ____1.脸红系数 -> ______001.Fac
    ____.links.new(____1.outputs[1], ______001.inputs[0])
    # ____1.脸红颜色 -> ____2.Color
    ____.links.new(____1.outputs[2], ____2.inputs[0])
    # __.Value -> ____2.Strength
    ____.links.new(__.outputs[0], ____2.inputs[1])
    # ____1.关闭脸黑 -> __.Value
    ____.links.new(____1.outputs[3], __.inputs[0])

    return ____

