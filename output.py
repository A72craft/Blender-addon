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