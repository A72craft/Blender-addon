import bpy
import mathutils

def generate_compositor_scene():

	# Generate unique scene name
	base_name = "72craft的合成器场景"
	end_name = base_name
	if bpy.data.scenes.get(end_name) is not None:
		i = 1
		end_name = base_name + f".{i:03d}"
		while bpy.data.scenes.get(end_name) is not None:
			end_name = base_name + f".{i:03d}"
			i += 1

	scene = bpy.context.window.scene.copy()

	scene.name = end_name
	scene.use_fake_user = True
	bpy.context.window.scene = scene


	def compos_node_group():
		"""Initialize 眼透&辉光&刘海阴影 node group"""
		compos = bpy.data.node_groups.new(type = 'CompositorNodeTree', name = "眼透&辉光&刘海阴影")

		compos.color_tag = 'NONE'
		compos.description = "用于合成器中的节点"
		compos.default_group_node_width = 140
		# compos interface

		# Socket Result
		result_socket = compos.interface.new_socket(name="Result", in_out='OUTPUT', socket_type='NodeSocketColor')
		result_socket.default_value = (0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0)
		result_socket.attribute_domain = 'POINT'
		result_socket.default_input = 'VALUE'
		result_socket.structure_type = 'AUTO'

		# Socket 渲染结果
		_____socket = compos.interface.new_socket(name="渲染结果", in_out='INPUT', socket_type='NodeSocketColor')
		_____socket.default_value = (1.0, 1.0, 1.0, 1.0)
		_____socket.attribute_domain = 'POINT'
		_____socket.default_input = 'VALUE'
		_____socket.structure_type = 'AUTO'

		# Socket 深度
		___socket = compos.interface.new_socket(name="深度", in_out='INPUT', socket_type='NodeSocketFloat')
		___socket.default_value = 0.0
		___socket.min_value = -3.4028234663852886e+38
		___socket.max_value = 3.4028234663852886e+38
		___socket.subtype = 'NONE'
		___socket.attribute_domain = 'POINT'
		___socket.default_input = 'VALUE'
		___socket.structure_type = 'AUTO'

		# Socket transp
		transp_socket = compos.interface.new_socket(name="transp", in_out='INPUT', socket_type='NodeSocketColor')
		transp_socket.default_value = (0.0, 0.0, 0.0, 1.0)
		transp_socket.attribute_domain = 'POINT'
		transp_socket.default_input = 'VALUE'
		transp_socket.structure_type = 'AUTO'

		# Socket face(AOV)
		face_aov__socket = compos.interface.new_socket(name="face(AOV)", in_out='INPUT', socket_type='NodeSocketFloat')
		face_aov__socket.default_value = 0.0
		face_aov__socket.min_value = -3.4028234663852886e+38
		face_aov__socket.max_value = 3.4028234663852886e+38
		face_aov__socket.subtype = 'NONE'
		face_aov__socket.attribute_domain = 'POINT'
		face_aov__socket.default_input = 'VALUE'
		face_aov__socket.structure_type = 'AUTO'

		# Socket eye_val(AOV)
		eye_val_aov__socket = compos.interface.new_socket(name="eye_val(AOV)", in_out='INPUT', socket_type='NodeSocketFloat')
		eye_val_aov__socket.default_value = 0.0
		eye_val_aov__socket.min_value = -3.4028234663852886e+38
		eye_val_aov__socket.max_value = 3.4028234663852886e+38
		eye_val_aov__socket.subtype = 'NONE'
		eye_val_aov__socket.attribute_domain = 'POINT'
		eye_val_aov__socket.default_input = 'VALUE'
		eye_val_aov__socket.structure_type = 'AUTO'

		# Socket eye_mat(AOV)
		eye_mat_aov__socket = compos.interface.new_socket(name="eye_mat(AOV)", in_out='INPUT', socket_type='NodeSocketColor')
		eye_mat_aov__socket.default_value = (0.0, 0.0, 0.0, 1.0)
		eye_mat_aov__socket.attribute_domain = 'POINT'
		eye_mat_aov__socket.default_input = 'VALUE'
		eye_mat_aov__socket.structure_type = 'AUTO'

		# Socket 辉光颜色
		_____socket_1 = compos.interface.new_socket(name="辉光颜色", in_out='INPUT', socket_type='NodeSocketColor')
		_____socket_1.default_value = (0.5028828978538513, 0.5028868913650513, 0.5028865933418274, 1.0)
		_____socket_1.attribute_domain = 'POINT'
		_____socket_1.default_input = 'VALUE'
		_____socket_1.structure_type = 'AUTO'

		# Socket 阴影颜色
		_____socket_2 = compos.interface.new_socket(name="阴影颜色", in_out='INPUT', socket_type='NodeSocketColor')
		_____socket_2.default_value = (0.0, 0.0, 0.0, 1.0)
		_____socket_2.attribute_domain = 'POINT'
		_____socket_2.default_input = 'VALUE'
		_____socket_2.structure_type = 'AUTO'

		# Socket 眼透系数
		_____socket_3 = compos.interface.new_socket(name="眼透系数", in_out='INPUT', socket_type='NodeSocketFloat')
		_____socket_3.default_value = 0.30000001192092896
		_____socket_3.min_value = 0.0
		_____socket_3.max_value = 0.699999988079071
		_____socket_3.subtype = 'NONE'
		_____socket_3.attribute_domain = 'POINT'
		_____socket_3.default_input = 'VALUE'
		_____socket_3.structure_type = 'AUTO'

		# Socket 刘海阴影法向
		_______socket = compos.interface.new_socket(name="刘海阴影法向", in_out='INPUT', socket_type='NodeSocketVector')
		_______socket.dimensions = 2
		# Get the socket again, as its default value could have been updated
		_______socket = compos.interface.items_tree[_______socket.index]
		_______socket.default_value = (0.10000000149011612, -0.10000000149011612)
		_______socket.min_value = -9.999999790214768e+33
		_______socket.max_value = 3.402820018375656e+38
		_______socket.subtype = 'NONE'
		_______socket.attribute_domain = 'POINT'
		_______socket.default_input = 'VALUE'
		_______socket.structure_type = 'AUTO'

		# Initialize compos nodes

		# Node 组输出
		___ = compos.nodes.new("NodeGroupOutput")
		___.name = "组输出"
		___.is_active_output = True

		# Node 组输入
		____1 = compos.nodes.new("NodeGroupInput")
		____1.name = "组输入"

		# Node 眩光
		__ = compos.nodes.new("CompositorNodeGlare")
		__.name = "眩光"
		__.glare_type = 'BLOOM'
		__.quality = 'HIGH'
		# Highlights Threshold
		__.inputs[1].default_value = 0.6800000071525574
		# Highlights Smoothness
		__.inputs[2].default_value = 1.0
		# Clamp Highlights
		__.inputs[3].default_value = False
		# Maximum Highlights
		__.inputs[4].default_value = 10.0
		# Strength
		__.inputs[5].default_value = 0.800000011920929
		# Saturation
		__.inputs[6].default_value = 1.0
		# Tint
		__.inputs[7].default_value = (1.0, 1.0, 1.0, 1.0)
		# Size
		__.inputs[8].default_value = 8.0

		# Node 混合
		___1 = compos.nodes.new("ShaderNodeMix")
		___1.name = "混合"
		___1.blend_type = 'MULTIPLY'
		___1.clamp_factor = True
		___1.clamp_result = False
		___1.data_type = 'RGBA'
		___1.factor_mode = 'UNIFORM'
		# Factor_Float
		___1.inputs[0].default_value = 1.0

		# Node 混合.001
		___001 = compos.nodes.new("ShaderNodeMix")
		___001.name = "混合.001"
		___001.blend_type = 'LIGHTEN'
		___001.clamp_factor = True
		___001.clamp_result = False
		___001.data_type = 'RGBA'
		___001.factor_mode = 'UNIFORM'
		# Factor_Float
		___001.inputs[0].default_value = 1.0

		# Node 置换
		___2 = compos.nodes.new("CompositorNodeDisplace")
		___2.name = "置换"
		# Image
		___2.inputs[0].default_value = (1.0, 1.0, 1.0, 1.0)
		# Vector
		___2.inputs[1].default_value = (1.0, 1.0)
		# X Scale
		___2.inputs[2].default_value = -60.0
		# Y Scale
		___2.inputs[3].default_value = -60.0

		# Node 运算
		___3 = compos.nodes.new("ShaderNodeMath")
		___3.name = "运算"
		___3.operation = 'SUBTRACT'
		___3.use_clamp = False
		# Value_001
		___3.inputs[1].default_value = 0.5

		# Node 运算.001
		___001_1 = compos.nodes.new("ShaderNodeMath")
		___001_1.name = "运算.001"
		___001_1.operation = 'MULTIPLY'
		___001_1.use_clamp = False
		# Value_001
		___001_1.inputs[1].default_value = 0.5

		# Node 帧
		_ = compos.nodes.new("NodeFrame")
		_.label = "辉光"
		_.name = "帧"
		_.label_size = 20
		_.shrink = True

		# Node 帧.001
		__001 = compos.nodes.new("NodeFrame")
		__001.label = "刘海阴影"
		__001.name = "帧.001"
		__001.label_size = 20
		__001.shrink = True

		# Node 混合.003
		___003 = compos.nodes.new("ShaderNodeMix")
		___003.name = "混合.003"
		___003.blend_type = 'MULTIPLY'
		___003.clamp_factor = True
		___003.clamp_result = False
		___003.data_type = 'RGBA'
		___003.factor_mode = 'UNIFORM'

		# Node 运算.002
		___002 = compos.nodes.new("ShaderNodeMath")
		___002.name = "运算.002"
		___002.operation = 'MULTIPLY'
		___002.use_clamp = False

		# Node 预览器
		____2 = compos.nodes.new("CompositorNodeViewer")
		____2.name = "预览器"
		____2.ui_shortcut = 0

		# Node 帧.002
		__002 = compos.nodes.new("NodeFrame")
		__002.label = "眼透"
		__002.name = "帧.002"
		__002.label_size = 20
		__002.shrink = True

		# Node 分离颜色
		____ = compos.nodes.new("CompositorNodeSeparateColor")
		____.name = "分离颜色"
		____.mode = 'RGB'
		____.ycc_mode = 'ITUBT709'

		# Node 运算.003
		___003_1 = compos.nodes.new("ShaderNodeMath")
		___003_1.name = "运算.003"
		___003_1.operation = 'DIVIDE'
		___003_1.use_clamp = False

		# Node 运算.004
		___004 = compos.nodes.new("ShaderNodeMath")
		___004.name = "运算.004"
		___004.operation = 'DIVIDE'
		___004.use_clamp = False

		# Node 置换.001
		___001_2 = compos.nodes.new("CompositorNodeDisplace")
		___001_2.name = "置换.001"
		# X Scale
		___001_2.inputs[2].default_value = 5.0
		# Y Scale
		___001_2.inputs[3].default_value = 5.0

		# Node 运算.005
		___005 = compos.nodes.new("ShaderNodeMath")
		___005.name = "运算.005"
		___005.operation = 'SUBTRACT'
		___005.use_clamp = False

		# Node 运算.006
		___006 = compos.nodes.new("ShaderNodeMath")
		___006.name = "运算.006"
		___006.operation = 'MULTIPLY'
		___006.use_clamp = False

		# Node 运算.007
		___007 = compos.nodes.new("ShaderNodeMath")
		___007.name = "运算.007"
		___007.operation = 'MULTIPLY'
		___007.use_clamp = False
		# Value_001
		___007.inputs[1].default_value = 0.5

		# Node 混合.004
		___004_1 = compos.nodes.new("ShaderNodeMix")
		___004_1.name = "混合.004"
		___004_1.blend_type = 'MULTIPLY'
		___004_1.clamp_factor = True
		___004_1.clamp_result = False
		___004_1.data_type = 'RGBA'
		___004_1.factor_mode = 'UNIFORM'

		# Node 帧.003
		__003 = compos.nodes.new("NodeFrame")
		__003.label = "刘海阴影"
		__003.name = "帧.003"
		__003.label_size = 20
		__003.shrink = True

		# Node 分离 XYZ
		___xyz = compos.nodes.new("ShaderNodeSeparateXYZ")
		___xyz.name = "分离 XYZ"

		# Node 合并 XYZ
		___xyz_1 = compos.nodes.new("ShaderNodeCombineXYZ")
		___xyz_1.name = "合并 XYZ"
		# Z
		___xyz_1.inputs[2].default_value = 0.0

		# Set parents
		__.parent = _
		___1.parent = _
		___001.parent = _
		___2.parent = __001
		___3.parent = __001
		___001_1.parent = __001
		___003.parent = __002
		___002.parent = __002
		____.parent = __003
		___003_1.parent = __003
		___004.parent = __003
		___001_2.parent = __003
		___005.parent = __003
		___006.parent = __003
		___007.parent = __003
		___xyz.parent = __003
		___xyz_1.parent = __003

		# Set locations
		___.location = (2388.418212890625, -38.40216064453125)
		____1.location = (-457.8623962402344, 47.464439392089844)
		__.location = (30.7186279296875, -62.11048889160156)
		___1.location = (232.576171875, -36.242584228515625)
		___001.location = (235.0374755859375, -277.3536071777344)
		___2.location = (30.6812744140625, -66.46588134765625)
		___3.location = (259.4117431640625, -84.04562377929688)
		___001_1.location = (473.13336181640625, -36.19720458984375)
		_.location = (1798.1817626953125, 301.1999816894531)
		__001.location = (-1296.727294921875, -306.0727233886719)
		___003.location = (215.15594482421875, -36.24436950683594)
		___002.location = (30.6416015625, -55.50408935546875)
		____2.location = (2298.051025390625, 86.12122344970703)
		__002.location = (613.0908813476562, 251.74545288085938)
		____.location = (208.4605712890625, -376.12689208984375)
		___003_1.location = (246.62130737304688, -207.3846893310547)
		___004.location = (248.66275024414062, -48.325592041015625)
		___001_2.location = (611.6818237304688, -95.08177185058594)
		___005.location = (868.5042724609375, -93.46733093261719)
		___006.location = (1059.5589599609375, -59.36399841308594)
		___007.location = (1219.1243896484375, -36.135345458984375)
		___004_1.location = (1431.2532958984375, 42.34690475463867)
		__003.location = (-153.09091186523438, -200.98182678222656)
		___xyz.location = (30.57501983642578, -154.04515075683594)
		___xyz_1.location = (418.73419189453125, -100.52192687988281)

		# Set dimensions
		___.width, ___.height = 140.0, 100.0
		____1.width, ____1.height = 140.0, 100.0
		__.width, __.height = 140.0, 100.0
		___1.width, ___1.height = 140.0, 100.0
		___001.width, ___001.height = 140.0, 100.0
		___2.width, ___2.height = 140.0, 100.0
		___3.width, ___3.height = 140.0, 100.0
		___001_1.width, ___001_1.height = 140.0, 100.0
		_.width, _.height = 405.4547119140625, 532.8363647460938
		__001.width, __001.height = 643.6364135742188, 282.2909240722656
		___003.width, ___003.height = 140.0, 100.0
		___002.width, ___002.height = 140.0, 100.0
		____2.width, ____2.height = 140.0, 100.0
		__002.width, __002.height = 385.8182373046875, 292.83636474609375
		____.width, ____.height = 140.0, 100.0
		___003_1.width, ___003_1.height = 140.0, 100.0
		___004.width, ___004.height = 140.0, 100.0
		___001_2.width, ___001_2.height = 140.0, 100.0
		___005.width, ___005.height = 140.0, 100.0
		___006.width, ___006.height = 140.0, 100.0
		___007.width, ___007.height = 140.0, 100.0
		___004_1.width, ___004_1.height = 140.0, 100.0
		__003.width, __003.height = 1389.8182373046875, 575.0181884765625
		___xyz.width, ___xyz.height = 140.0, 100.0
		___xyz_1.width, ___xyz_1.height = 140.0, 100.0

		# Initialize compos links

		# ___3.Value -> ___001_1.Value
		compos.links.new(___3.outputs[0], ___001_1.inputs[0])
		# ___1.Result -> ___001.A
		compos.links.new(___1.outputs[2], ___001.inputs[6])
		# __.Image -> ___1.A
		compos.links.new(__.outputs[0], ___1.inputs[6])
		# ___2.Image -> ___3.Value
		compos.links.new(___2.outputs[0], ___3.inputs[0])
		# ____1.eye_val(AOV) -> ___002.Value
		compos.links.new(____1.outputs[4], ___002.inputs[0])
		# ___002.Value -> ___003.Factor
		compos.links.new(___002.outputs[0], ___003.inputs[0])
		# ____1.渲染结果 -> ___003.A
		compos.links.new(____1.outputs[0], ___003.inputs[6])
		# ___001.Result -> ___.Result
		compos.links.new(___001.outputs[2], ___.inputs[0])
		# ____1.eye_mat(AOV) -> ___003.B
		compos.links.new(____1.outputs[5], ___003.inputs[7])
		# ____1.眼透系数 -> ___002.Value
		compos.links.new(____1.outputs[8], ___002.inputs[1])
		# ___001.Result -> ____2.Image
		compos.links.new(___001.outputs[2], ____2.inputs[0])
		# ____1.transp -> ____.Image
		compos.links.new(____1.outputs[2], ____.inputs[0])
		# ____1.深度 -> ___004.Value
		compos.links.new(____1.outputs[1], ___004.inputs[1])
		# ____1.深度 -> ___003_1.Value
		compos.links.new(____1.outputs[1], ___003_1.inputs[1])
		# ____.Alpha -> ___001_2.Image
		compos.links.new(____.outputs[3], ___001_2.inputs[0])
		# ___001_2.Image -> ___005.Value
		compos.links.new(___001_2.outputs[0], ___005.inputs[0])
		# ____.Alpha -> ___005.Value
		compos.links.new(____.outputs[3], ___005.inputs[1])
		# ___005.Value -> ___006.Value
		compos.links.new(___005.outputs[0], ___006.inputs[0])
		# ____1.face(AOV) -> ___006.Value
		compos.links.new(____1.outputs[3], ___006.inputs[1])
		# ___006.Value -> ___007.Value
		compos.links.new(___006.outputs[0], ___007.inputs[0])
		# ___003.Result -> ___004_1.A
		compos.links.new(___003.outputs[2], ___004_1.inputs[6])
		# ____1.阴影颜色 -> ___004_1.B
		compos.links.new(____1.outputs[7], ___004_1.inputs[7])
		# ___007.Value -> ___004_1.Factor
		compos.links.new(___007.outputs[0], ___004_1.inputs[0])
		# ___004_1.Result -> __.Image
		compos.links.new(___004_1.outputs[2], __.inputs[0])
		# ___004_1.Result -> ___001.B
		compos.links.new(___004_1.outputs[2], ___001.inputs[7])
		# ____1.辉光颜色 -> ___1.B
		compos.links.new(____1.outputs[6], ___1.inputs[7])
		# ___xyz.X -> ___004.Value
		compos.links.new(___xyz.outputs[0], ___004.inputs[0])
		# ___xyz.Y -> ___003_1.Value
		compos.links.new(___xyz.outputs[1], ___003_1.inputs[0])
		# ___xyz_1.Vector -> ___001_2.Vector
		compos.links.new(___xyz_1.outputs[0], ___001_2.inputs[1])
		# ___003_1.Value -> ___xyz_1.Y
		compos.links.new(___003_1.outputs[0], ___xyz_1.inputs[1])
		# ___004.Value -> ___xyz_1.X
		compos.links.new(___004.outputs[0], ___xyz_1.inputs[0])
		# ____1.刘海阴影法向 -> ___xyz.Vector
		compos.links.new(____1.outputs[9], ___xyz.inputs[0])

		return compos


	compos = compos_node_group()

	def scene_1_node_group():
		"""Initialize Scene node group"""
		scene_1 = scene.node_tree

		# Start with a clean node tree
		for node in scene_1.nodes:
			scene_1.nodes.remove(node)
		scene_1.color_tag = 'NONE'
		scene_1.description = ""
		scene_1.default_group_node_width = 140
		# scene_1 interface

		# Initialize scene_1 nodes

		# Node 合成
		___4 = scene_1.nodes.new("CompositorNodeComposite")
		___4.name = "合成"

		# Node 渲染层
		____3 = scene_1.nodes.new("CompositorNodeRLayers")
		____3.name = "渲染层"
		____3.layer = 'ViewLayer'

		# Node 转接点
		____4 = scene_1.nodes.new("NodeReroute")
		____4.name = "转接点"
		____4.socket_idname = "NodeSocketColor"
		# Node 预览器
		____5 = scene_1.nodes.new("CompositorNodeViewer")
		____5.name = "预览器"
		____5.ui_shortcut = 0

		# Node 群组
		___5 = scene_1.nodes.new("CompositorNodeGroup")
		___5.name = "群组"
		___5.node_tree = compos
		# Socket_6
		___5.inputs[6].default_value = (0.5028828978538513, 0.5028868913650513, 0.5028865933418274, 1.0)
		# Socket_8
		___5.inputs[7].default_value = (0.88525390625, 0.1956787109375, 0.2149658203125, 1.0)
		# Socket_7
		___5.inputs[8].default_value = 0.41999998688697815

		# Node 法向
		___6 = scene_1.nodes.new("CompositorNodeNormal")
		___6.name = "法向"
		# Normal
		___6.inputs[0].default_value = (0.0, 0.0, 1.0)

		___6.outputs[0].default_value = (0.48024317622184753, -0.3069908916950226, 0.8216587901115417)
		# Set locations
		___4.location = (200.0, 0.0)
		____3.location = (-545.0386962890625, -13.882312774658203)
		____4.location = (100.0, -35.0)
		____5.location = (200.0, -60.0)
		___5.location = (-125.62604522705078, -16.40192985534668)
		___6.location = (-444.6949157714844, -276.26934814453125)

		# Set dimensions
		___4.width, ___4.height = 140.0, 100.0
		____3.width, ____3.height = 240.0, 100.0
		____4.width, ____4.height = 28.0, 100.0
		____5.width, ____5.height = 140.0, 100.0
		___5.width, ___5.height = 140.0, 100.0
		___6.width, ___6.height = 140.0, 100.0

		# Initialize scene_1 links

		# ____4.Output -> ___4.Image
		scene_1.links.new(____4.outputs[0], ___4.inputs[0])
		# ____4.Output -> ____5.Image
		scene_1.links.new(____4.outputs[0], ____5.inputs[0])
		# ___5.Result -> ____4.Input
		scene_1.links.new(___5.outputs[0], ____4.inputs[0])
		# ____3.Image -> ___5.渲染结果
		scene_1.links.new(____3.outputs[0], ___5.inputs[0])
		# ____3.Depth -> ___5.深度
		scene_1.links.new(____3.outputs[2], ___5.inputs[1])
		# ____3.Transp -> ___5.transp
		scene_1.links.new(____3.outputs[3], ___5.inputs[2])
		# ____3.face -> ___5.face(AOV)
		scene_1.links.new(____3.outputs[4], ___5.inputs[3])
		# ____3.eye_mat -> ___5.eye_mat(AOV)
		scene_1.links.new(____3.outputs[6], ___5.inputs[5])
		# ____3.eye_val -> ___5.eye_val(AOV)
		scene_1.links.new(____3.outputs[5], ___5.inputs[4])
		# ___6.Normal -> ___5.刘海阴影法向
		scene_1.links.new(___6.outputs[0], ___5.inputs[9])

		return scene_1


	scene_1 = scene_1_node_group()

	return scene_1