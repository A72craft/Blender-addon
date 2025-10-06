import bpy
import mathutils

class Horizontal(bpy.types.Operator):
    """设置横屏"""
    # Unique ID for the operator
    bl_idname = "render.horizontal_setup"
    # Name that appears in the Blender search menu
    bl_label = "72craft_横屏"

    # The execute() function runs when the operator is called
    def execute(self, context):
        scene = context.scene
        render = scene.render
        # Set the render resolution
        if render.resolution_x < render.resolution_y:
        # If it is, swap the x and y values
            render.resolution_x, render.resolution_y = render.resolution_y, render.resolution_x

        # Optional: Report a success message to the user
        self.report({'INFO'},"已设置为横屏")

        # Tell Blender the operator finished successfully
        return {'FINISHED'}
    
class Vertical(bpy.types.Operator):
    """设置竖屏"""
    # Unique ID for the operator
    bl_idname = "render.vertical_setup"
    # Name that appears in the Blender search menu
    bl_label = "72craft_竖屏"

    # The execute() function runs when the operator is called
    def execute(self, context):
        scene = context.scene

        render = scene.render
        # Set the render resolution
        if render.resolution_x > render.resolution_y:
        # If it is, swap the x and y values
            render.resolution_x, render.resolution_y = render.resolution_y, render.resolution_x

        # Optional: Report a success message to the user
        self.report({'INFO'},"已设置为竖屏")

        # Tell Blender the operator finished successfully
        return {'FINISHED'}
    
class Hz30(bpy.types.Operator):
    """设置输出为30Hz"""
    # Unique ID for the operator
    bl_idname = "render.30hz"
    # Name that appears in the Blender search menu
    bl_label = "72craft_30Hz"

    # The execute() function runs when the operator is called
    def execute(self, context):
        # Get the active scene from the context
        scene = context.scene

        original_fps = scene.render.fps

        # Check if the frame rate is not already 30
        if original_fps != 30:
            # If not 30, double the start and end frames
            scene.frame_start //= 2
            scene.frame_end //= 2
            self.report({'INFO'}, f"帧范围减半.已设置为30Hz.")
        else:
            # If already 30, do nothing to the frame range
            self.report({'INFO'}, "已设置为30Hz.")
        
        # 1. Change the output frame rate to 30Hz (fps)
        scene.render.fps = 30
        # 2. Change the Time Remapping (stretch) values
        scene.render.frame_map_old = 30
        scene.render.frame_map_new = 30

        # Tell Blender the operator finished successfully
        return {'FINISHED'}
    
class Hz60(bpy.types.Operator):
    """设置输出为60Hz"""
    # Unique ID for the operator
    bl_idname = "render.60hz"
    # Name that appears in the Blender search menu
    bl_label = "72craft_60Hz"

    # The execute() function runs when the operator is called
    def execute(self, context):
        # Get the active scene from the context
        scene = context.scene

        original_fps = scene.render.fps

        # Check if the frame rate is not already 60
        if original_fps != 60:
            # If not 60, double the start and end frames
            scene.frame_start *= 2
            scene.frame_end *= 2
            self.report({'INFO'}, f"帧范围翻倍.已设置为60Hz.")
        else:
            # If already 60, do nothing to the frame range
            self.report({'INFO'}, "已设置为60Hz.")

        # 1. Change the output frame rate to 60Hz (fps)
        scene.render.fps = 60
        # 2. Change the Time Remapping (stretch) values
        scene.render.frame_map_old = 30
        scene.render.frame_map_new = 60
        # Tell Blender the operator finished successfully
        return {'FINISHED'}