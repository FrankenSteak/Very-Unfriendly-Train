--   STEP 0: Get application
   VSes_Application = cf.GetApplication()
--

-- STEP 1: Make a new project
   VAnt_Project    = VSes_Application:NewProject()
   VAnt_Geometry   = VAnt_Project.Geometry
--

-- STEP 2: Set project unit of measurement
   VAnt_Project.ModelUnit  = cf.Enums.ModelUnitEnum.Millimetres
--

-- STEP 3: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(56.92, 34.166999999999994, 1.6)
   VTmp_Points[2] = cf.Point(56.92, 36.30499999999999, 1.6)
   VTmp_Points[3] = cf.Point(58.57, 36.30499999999999, 1.6)
   VTmp_Points[4] = cf.Point(58.57, 34.166999999999994, 1.6)
   VAnt_Polygon_Feed_Top = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_Feed_Top.Label = "Feed_Top"
--

-- STEP 4: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(58.57, 36.30499999999999, 1.6)
   VTmp_Points[2] = cf.Point(58.57, 36.30499999999999, 0.8)
   VTmp_Points[3] = cf.Point(58.57, 34.166999999999994, 0.8)
   VTmp_Points[4] = cf.Point(58.57, 34.166999999999994, 1.6)
   VAnt_Polygon_Feed_Pos = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_Feed_Pos.Label = "Feed_Pos"
--

-- STEP 5: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(58.57, 36.30499999999999, 0.0)
   VTmp_Points[2] = cf.Point(58.57, 36.30499999999999, 0.8)
   VTmp_Points[3] = cf.Point(58.57, 34.166999999999994, 0.8)
   VTmp_Points[4] = cf.Point(58.57, 34.166999999999994, 0.0)
   VAnt_Polygon_Feed_Neg = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_Feed_Neg.Label = "Feed_Neg"
--

-- STEP 6: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(58.57, 34.166999999999994, 0.0)
   VTmp_Points[2] = cf.Point(58.57, 36.30499999999999, 0.0)
   VTmp_Points[3] = cf.Point(56.97, 36.30499999999999, 0.0)
   VTmp_Points[4] = cf.Point(56.97, 34.166999999999994, 0.0)
   VAnt_Polygon_Feed_Bot = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_Feed_Bot.Label = "Feed_Bot"
--

-- STEP 7: Create new rectangular surface
   VTmp_Corner = cf.Point(-3.971, -1.803, 0.0)
   VAnt_Rectangle_GP = VAnt_Geometry:AddRectangle(VTmp_Corner, 60.941, 78.021)
   VAnt_Rectangle_GP.Label = "GP"
--

-- STEP 8: Create new rectangular surface
   VTmp_Corner = cf.Point(-4.556, 98.647, 0.0)
   VAnt_Rectangle_GPSlot_0 = VAnt_Geometry:AddRectangle(VTmp_Corner, 9.652, 11.434)
   VAnt_Rectangle_GPSlot_0.Label = "GPSlot_0"
--

-- STEP 9: Create new rectangular surface
   VTmp_Corner = cf.Point(14.432, 21.161, 0.0)
   VAnt_Rectangle_GPSlot_1 = VAnt_Geometry:AddRectangle(VTmp_Corner, 2.402, 21.335)
   VAnt_Rectangle_GPSlot_1.Label = "GPSlot_1"
--

-- STEP 10: Create new rectangular surface
   VTmp_Corner = cf.Point(18.339, 51.944, 0.0)
   VAnt_Rectangle_GPSlot_2 = VAnt_Geometry:AddRectangle(VTmp_Corner, 9.557, 20.921)
   VAnt_Rectangle_GPSlot_2.Label = "GPSlot_2"
--

-- STEP 11: Create new rectangular surface
   VTmp_Corner = cf.Point(41.133, 56.298, 0.0)
   VAnt_Rectangle_GPSlot_3 = VAnt_Geometry:AddRectangle(VTmp_Corner, 4.33, 10.307)
   VAnt_Rectangle_GPSlot_3.Label = "GPSlot_3"
--

-- STEP 12: Create new rectangular surface
   VTmp_Corner = cf.Point(50.679, 84.069, 0.0)
   VAnt_Rectangle_GPSlot_4 = VAnt_Geometry:AddRectangle(VTmp_Corner, 9.416, 3.747)
   VAnt_Rectangle_GPSlot_4.Label = "GPSlot_4"
--

-- STEP 13: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(84.391, 134.071, 0.0)
   VTmp_Points[2] = cf.Point(72.255, 107.507, 0.0)
   VTmp_Points[3] = cf.Point(75.533, 106.022, 0.0)
   VAnt_Polygon_GPSlot_5 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_5.Label = "GPSlot_5"
--

-- STEP 14: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(26.367, 92.212, 0.0)
   VTmp_Points[2] = cf.Point(5.453, 130.963, 0.0)
   VTmp_Points[3] = cf.Point(19.591, 88.854, 0.0)
   VAnt_Polygon_GPSlot_6 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_6.Label = "GPSlot_6"
--

-- STEP 15: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(46.487, 21.262, 0.0)
   VTmp_Points[2] = cf.Point(58.355, -15.318, 0.0)
   VTmp_Points[3] = cf.Point(73.872, 2.891, 0.0)
   VAnt_Polygon_GPSlot_7 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_7.Label = "GPSlot_7"
--

-- STEP 16: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(24.418, 107.74, 0.0)
   VTmp_Points[2] = cf.Point(49.636, 78.474, 0.0)
   VTmp_Points[3] = cf.Point(52.895, 64.758, 0.0)
   VAnt_Polygon_GPSlot_8 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_8.Label = "GPSlot_8"
--

-- STEP 17: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(44.011, 35.71, 0.0)
   VTmp_Points[2] = cf.Point(56.989, -3.912, 0.0)
   VTmp_Points[3] = cf.Point(14.786, 10.991, 0.0)
   VAnt_Polygon_GPSlot_9 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_9.Label = "GPSlot_9"
--

-- STEP 18: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(-0.308, 14.869, 0.0)
   VTmp_Points[2] = cf.Point(42.472, 6.955, 0.0)
   VTmp_Points[3] = cf.Point(49.255, 17.58, 0.0)
   VAnt_Polygon_GPSlot_10 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_10.Label = "GPSlot_10"
--

-- STEP 19: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(19.501, 56.532, 0.0)
   VTmp_Points[2] = cf.Point(36.517, 78.495, 0.0)
   VTmp_Points[3] = cf.Point(21.515, 75.645, 0.0)
   VAnt_Polygon_GPSlot_11 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_11.Label = "GPSlot_11"
--

-- STEP 20: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(66.759, 20.086, 0.0)
   VTmp_Points[2] = cf.Point(68.142, 27.474, 0.0)
   VTmp_Points[3] = cf.Point(63.904, 19.892, 0.0)
   VAnt_Polygon_GPSlot_12 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_12.Label = "GPSlot_12"
--

-- STEP 21: Create new subtraction
   VTmp_Subs = {}
   VTmp_Subs[1] = VAnt_Rectangle_GPSlot_0
   VTmp_Subs[2] = VAnt_Rectangle_GPSlot_1
   VTmp_Subs[3] = VAnt_Rectangle_GPSlot_2
   VTmp_Subs[4] = VAnt_Rectangle_GPSlot_3
   VTmp_Subs[5] = VAnt_Rectangle_GPSlot_4
   VTmp_Subs[6] = VAnt_Polygon_GPSlot_5
   VTmp_Subs[7] = VAnt_Polygon_GPSlot_6
   VTmp_Subs[8] = VAnt_Polygon_GPSlot_7
   VTmp_Subs[9] = VAnt_Polygon_GPSlot_8
   VTmp_Subs[10] = VAnt_Polygon_GPSlot_9
   VTmp_Subs[11] = VAnt_Polygon_GPSlot_10
   VTmp_Subs[12] = VAnt_Polygon_GPSlot_11
   VTmp_Subs[13] = VAnt_Polygon_GPSlot_12
   VAnt_Subtraction_GP_Slotted = VAnt_Geometry:Subtract(VAnt_Rectangle_GP, VTmp_Subs)
   VAnt_Subtraction_GP_Slotted.Label = "GP_Slotted"
--

-- STEP 22: Creating medium
   VAnt_Medium_FR4 = VAnt_Project.Media:AddDielectric()
   VAnt_Medium_FR4.Label = "FR4"
   VAnt_Medium_FR4.DielectricModelling.RelativePermittivity = 4.4
   VAnt_Medium_FR4.DielectricModelling.LossTangent = 0.02
--

-- STEP 23: Create new solid.cuboid
   VTmp_Corner = cf.Point(-3.971, -2.901, 0.0)
   VAnt_Cuboid_Substrate = VAnt_Geometry:AddCuboid(VTmp_Corner, 60.941, 79.332, 1.6)
   VAnt_Cuboid_Substrate.Label = "Substrate"
--

-- STEP 24: Set solid medium
   VAnt_Cuboid_Substrate.Regions:Item(1).Medium = VAnt_Project.Media:Item("FR4")
--

-- STEP 25: Create new rectangular surface
   VTmp_Corner = cf.Point(-2.299, -2.901, 1.6)
   VAnt_Rectangle_RP = VAnt_Geometry:AddRectangle(VTmp_Corner, 59.219, 79.282)
   VAnt_Rectangle_RP.Label = "RP"
--

-- STEP 26: Create new rectangular surface
   VTmp_Corner = cf.Point(31.914, 31.275, 1.6)
   VAnt_Rectangle_GPSlot_0 = VAnt_Geometry:AddRectangle(VTmp_Corner, 9.327, 3.526)
   VAnt_Rectangle_GPSlot_0.Label = "GPSlot_0"
--

-- STEP 27: Create new rectangular surface
   VTmp_Corner = cf.Point(37.296, 54.767, 1.6)
   VAnt_Rectangle_GPSlot_1 = VAnt_Geometry:AddRectangle(VTmp_Corner, 1.671, 5.906)
   VAnt_Rectangle_GPSlot_1.Label = "GPSlot_1"
--

-- STEP 28: Create new rectangular surface
   VTmp_Corner = cf.Point(39.471, 80.69, 1.6)
   VAnt_Rectangle_GPSlot_2 = VAnt_Geometry:AddRectangle(VTmp_Corner, 2.572, 7.892)
   VAnt_Rectangle_GPSlot_2.Label = "GPSlot_2"
--

-- STEP 29: Create new rectangular surface
   VTmp_Corner = cf.Point(55.281, 53.646, 1.6)
   VAnt_Rectangle_GPSlot_3 = VAnt_Geometry:AddRectangle(VTmp_Corner, 1.7, 0.121)
   VAnt_Rectangle_GPSlot_3.Label = "GPSlot_3"
--

-- STEP 30: Create new rectangular surface
   VTmp_Corner = cf.Point(14.462, 34.801, 1.6)
   VAnt_Rectangle_GPSlot_4 = VAnt_Geometry:AddRectangle(VTmp_Corner, 1.23, 2.29)
   VAnt_Rectangle_GPSlot_4.Label = "GPSlot_4"
--

-- STEP 31: Create new rectangular surface
   VTmp_Corner = cf.Point(57.258, 76.972, 1.6)
   VAnt_Rectangle_GPSlot_5 = VAnt_Geometry:AddRectangle(VTmp_Corner, 2.505, 4.305)
   VAnt_Rectangle_GPSlot_5.Label = "GPSlot_5"
--

-- STEP 32: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(12.733, 74.837, 1.6)
   VTmp_Points[2] = cf.Point(10.912, 83.866, 1.6)
   VTmp_Points[3] = cf.Point(12.661, 79.173, 1.6)
   VAnt_Polygon_GPSlot_6 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_6.Label = "GPSlot_6"
--

-- STEP 33: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(46.209, -9.718, 1.6)
   VTmp_Points[2] = cf.Point(50.631, -0.071, 1.6)
   VTmp_Points[3] = cf.Point(49.993, 3.046, 1.6)
   VAnt_Polygon_GPSlot_7 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_7.Label = "GPSlot_7"
--

-- STEP 34: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(24.733, 42.442, 1.6)
   VTmp_Points[2] = cf.Point(22.337, 40.672, 1.6)
   VTmp_Points[3] = cf.Point(21.643, 40.692, 1.6)
   VAnt_Polygon_GPSlot_8 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_8.Label = "GPSlot_8"
--

-- STEP 35: Create new subtraction
   VTmp_Subs = {}
   VTmp_Subs[1] = VAnt_Rectangle_GPSlot_0
   VTmp_Subs[2] = VAnt_Rectangle_GPSlot_1
   VTmp_Subs[3] = VAnt_Rectangle_GPSlot_2
   VTmp_Subs[4] = VAnt_Rectangle_GPSlot_3
   VTmp_Subs[5] = VAnt_Rectangle_GPSlot_4
   VTmp_Subs[6] = VAnt_Rectangle_GPSlot_5
   VTmp_Subs[7] = VAnt_Polygon_GPSlot_6
   VTmp_Subs[8] = VAnt_Polygon_GPSlot_7
   VTmp_Subs[9] = VAnt_Polygon_GPSlot_8
   VAnt_Subtraction_RP_Slotted = VAnt_Geometry:Subtract(VAnt_Rectangle_RP, VTmp_Subs)
   VAnt_Subtraction_RP_Slotted.Label = "RP_Slotted"
--

-- STEP 36: Create new union
   VTmp_Parts = {}
   VTmp_Parts[1] = VAnt_Subtraction_GP_Slotted
   VTmp_Parts[2] = VAnt_Subtraction_RP_Slotted
   VTmp_Parts[3] = VAnt_Cuboid_Substrate
   VTmp_Parts[4] = VAnt_Polygon_Feed_Top
   VTmp_Parts[5] = VAnt_Polygon_Feed_Pos
   VTmp_Parts[6] = VAnt_Polygon_Feed_Neg
   VTmp_Parts[7] = VAnt_Polygon_Feed_Bot
   VAnt_Union_Onion = VAnt_Geometry:Union(VTmp_Parts)
   VAnt_Union_Onion.Label = "Onion"
--

-- STEP 37: Changing face medium
   VAnt_Union_Onion.Faces:Item("Face35").Medium = VAnt_Project.Media:Item("Perfect electric conductor")
--

-- STEP 38: Changing face medium
   VAnt_Union_Onion.Faces:Item("Face36").Medium = VAnt_Project.Media:Item("Perfect electric conductor")
--

-- STEP 39: Changing face medium
   VAnt_Union_Onion.Faces:Item("Face37").Medium = VAnt_Project.Media:Item("Perfect electric conductor")
--

-- STEP 40: Create new edge port
   VTmp_Pos = {}
   VTmp_Neg = {}
   VTmp_Pos[1] = VAnt_Union_Onion.Faces:Item("Face2")
   VTmp_Neg[1] = VAnt_Union_Onion.Faces:Item("Face3")
   VAnt_EPort_SourcePort = VAnt_Project.Ports:AddEdgePort(VTmp_Pos, VTmp_Neg)
   VAnt_EPort_SourcePort.Label = "SourcePort"
--

-- STEP 41: Get config file
   VAnt_Config = VAnt_Project.SolutionConfigurations[1]
--

-- STEP 42: Create new voltage source
   VAnt_VSource_VoltageSource = VAnt_Config.Sources:AddVoltageSource(VAnt_EPort_SourcePort)
   VAnt_VSource_VoltageSource.Impedance = 50.0
   VAnt_VSource_VoltageSource.Magnitude = 1.0
   VAnt_VSource_VoltageSource.Phase = 0.0
   VAnt_VSource_VoltageSource.Label = "VoltageSource"
--

-- STEP 43: Create new Far-Field request
   VAnt_Config.FarFields:Add(0.0, 0.0, 180.0, 360.0, 5.0, 5.0)
--
-- STEP 44: Set frequency range
   VAnt_tmp = VAnt_Config.Frequency:GetProperties()
   VAnt_tmp.Start  = 906500000.0
   VAnt_tmp.End    = 933500000.0
   VAnt_tmp.RangeType  = cf.Enums.FrequencyRangeTypeEnum.LinearSpacedDiscrete
   VAnt_tmp.NumberOfDiscreteValues = 2
   VAnt_Config.Frequency:SetProperties(VAnt_tmp)
--

-- STEP 45: Mesh the project
   VAnt_Project.Mesher.Settings.WireRadius = 0.001
   VAnt_Project.Mesher.Settings.MeshSizeOption = cf.Enums.MeshSizeOptionEnum.Coarse
   VAnt_Project.Mesher:Mesh()
--

-- STEP 46: Save project
   VSes_Application:SaveAs("C:/Users/project/0. My Work/1. Repositories/1. Very Unfriendly Train/Data/Simulations/637072128687662976_Primary/637072223066233344_0/0.cfx")
--

-- STEP 47: Run simulation
   VAnt_Project.Launcher.Settings.FEKO.Parallel.Enabled = true
   VAnt_Project.Launcher:RunFEKO()
--

-- STEP 48: Close project
   VSes_Application:CloseAllWindows()
--

-- STEP 1: Make a new project
   VAnt_Project    = VSes_Application:NewProject()
   VAnt_Geometry   = VAnt_Project.Geometry
--

-- STEP 2: Set project unit of measurement
   VAnt_Project.ModelUnit  = cf.Enums.ModelUnitEnum.Millimetres
--

-- STEP 3: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(57.563, 33.723, 1.6)
   VTmp_Points[2] = cf.Point(57.563, 35.894999999999996, 1.6)
   VTmp_Points[3] = cf.Point(60.222, 35.894999999999996, 1.6)
   VTmp_Points[4] = cf.Point(60.222, 33.723, 1.6)
   VAnt_Polygon_Feed_Top = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_Feed_Top.Label = "Feed_Top"
--

-- STEP 4: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(60.222, 35.894999999999996, 1.6)
   VTmp_Points[2] = cf.Point(60.222, 35.894999999999996, 0.8)
   VTmp_Points[3] = cf.Point(60.222, 33.723, 0.8)
   VTmp_Points[4] = cf.Point(60.222, 33.723, 1.6)
   VAnt_Polygon_Feed_Pos = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_Feed_Pos.Label = "Feed_Pos"
--

-- STEP 5: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(60.222, 35.894999999999996, 0.0)
   VTmp_Points[2] = cf.Point(60.222, 35.894999999999996, 0.8)
   VTmp_Points[3] = cf.Point(60.222, 33.723, 0.8)
   VTmp_Points[4] = cf.Point(60.222, 33.723, 0.0)
   VAnt_Polygon_Feed_Neg = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_Feed_Neg.Label = "Feed_Neg"
--

-- STEP 6: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(60.222, 33.723, 0.0)
   VTmp_Points[2] = cf.Point(60.222, 35.894999999999996, 0.0)
   VTmp_Points[3] = cf.Point(58.622, 35.894999999999996, 0.0)
   VTmp_Points[4] = cf.Point(58.622, 33.723, 0.0)
   VAnt_Polygon_Feed_Bot = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_Feed_Bot.Label = "Feed_Bot"
--

-- STEP 7: Create new rectangular surface
   VTmp_Corner = cf.Point(-3.961, -1.649, 0.0)
   VAnt_Rectangle_GP = VAnt_Geometry:AddRectangle(VTmp_Corner, 62.583, 73.539)
   VAnt_Rectangle_GP.Label = "GP"
--

-- STEP 8: Create new rectangular surface
   VTmp_Corner = cf.Point(-3.18, 98.762, 0.0)
   VAnt_Rectangle_GPSlot_0 = VAnt_Geometry:AddRectangle(VTmp_Corner, 8.957, 9.375)
   VAnt_Rectangle_GPSlot_0.Label = "GPSlot_0"
--

-- STEP 9: Create new rectangular surface
   VTmp_Corner = cf.Point(13.96, 23.249, 0.0)
   VAnt_Rectangle_GPSlot_1 = VAnt_Geometry:AddRectangle(VTmp_Corner, 0.435, 24.059)
   VAnt_Rectangle_GPSlot_1.Label = "GPSlot_1"
--

-- STEP 10: Create new rectangular surface
   VTmp_Corner = cf.Point(20.457, 59.482, 0.0)
   VAnt_Rectangle_GPSlot_2 = VAnt_Geometry:AddRectangle(VTmp_Corner, 9.244, 18.263)
   VAnt_Rectangle_GPSlot_2.Label = "GPSlot_2"
--

-- STEP 11: Create new rectangular surface
   VTmp_Corner = cf.Point(40.108, 54.156, 0.0)
   VAnt_Rectangle_GPSlot_3 = VAnt_Geometry:AddRectangle(VTmp_Corner, 4.63, 12.112)
   VAnt_Rectangle_GPSlot_3.Label = "GPSlot_3"
--

-- STEP 12: Create new rectangular surface
   VTmp_Corner = cf.Point(50.409, 84.22, 0.0)
   VAnt_Rectangle_GPSlot_4 = VAnt_Geometry:AddRectangle(VTmp_Corner, 10.062, 3.41)
   VAnt_Rectangle_GPSlot_4.Label = "GPSlot_4"
--

-- STEP 13: Create new rectangular surface
   VTmp_Corner = cf.Point(37.281, 57.674, 0.0)
   VAnt_Rectangle_GPSlot_5 = VAnt_Geometry:AddRectangle(VTmp_Corner, 18.455, 5.993)
   VAnt_Rectangle_GPSlot_5.Label = "GPSlot_5"
--

-- STEP 14: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(87.178, 131.438, 0.0)
   VTmp_Points[2] = cf.Point(74.974, 109.409, 0.0)
   VTmp_Points[3] = cf.Point(78.677, 107.107, 0.0)
   VAnt_Polygon_GPSlot_6 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_6.Label = "GPSlot_6"
--

-- STEP 15: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(22.664, 91.848, 0.0)
   VTmp_Points[2] = cf.Point(2.769, 130.708, 0.0)
   VTmp_Points[3] = cf.Point(21.076, 92.438, 0.0)
   VAnt_Polygon_GPSlot_7 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_7.Label = "GPSlot_7"
--

-- STEP 16: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(46.386, 21.9, 0.0)
   VTmp_Points[2] = cf.Point(58.015, -16.165, 0.0)
   VTmp_Points[3] = cf.Point(74.493, 0.41, 0.0)
   VAnt_Polygon_GPSlot_8 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_8.Label = "GPSlot_8"
--

-- STEP 17: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(22.195, 107.647, 0.0)
   VTmp_Points[2] = cf.Point(51.003, 79.362, 0.0)
   VTmp_Points[3] = cf.Point(54.778, 67.216, 0.0)
   VAnt_Polygon_GPSlot_9 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_9.Label = "GPSlot_9"
--

-- STEP 18: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(44.549, 35.502, 0.0)
   VTmp_Points[2] = cf.Point(57.052, -2.563, 0.0)
   VTmp_Points[3] = cf.Point(14.73, 8.988, 0.0)
   VAnt_Polygon_GPSlot_10 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_10.Label = "GPSlot_10"
--

-- STEP 19: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(4.276, 12.675, 0.0)
   VTmp_Points[2] = cf.Point(40.101, 4.093, 0.0)
   VTmp_Points[3] = cf.Point(46.4, 18.951, 0.0)
   VAnt_Polygon_GPSlot_11 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_11.Label = "GPSlot_11"
--

-- STEP 20: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(20.02, 56.863, 0.0)
   VTmp_Points[2] = cf.Point(36.899, 78.11, 0.0)
   VTmp_Points[3] = cf.Point(21.615, 73.695, 0.0)
   VAnt_Polygon_GPSlot_12 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_12.Label = "GPSlot_12"
--

-- STEP 21: Create new subtraction
   VTmp_Subs = {}
   VTmp_Subs[1] = VAnt_Rectangle_GPSlot_0
   VTmp_Subs[2] = VAnt_Rectangle_GPSlot_1
   VTmp_Subs[3] = VAnt_Rectangle_GPSlot_2
   VTmp_Subs[4] = VAnt_Rectangle_GPSlot_3
   VTmp_Subs[5] = VAnt_Rectangle_GPSlot_4
   VTmp_Subs[6] = VAnt_Rectangle_GPSlot_5
   VTmp_Subs[7] = VAnt_Polygon_GPSlot_6
   VTmp_Subs[8] = VAnt_Polygon_GPSlot_7
   VTmp_Subs[9] = VAnt_Polygon_GPSlot_8
   VTmp_Subs[10] = VAnt_Polygon_GPSlot_9
   VTmp_Subs[11] = VAnt_Polygon_GPSlot_10
   VTmp_Subs[12] = VAnt_Polygon_GPSlot_11
   VTmp_Subs[13] = VAnt_Polygon_GPSlot_12
   VAnt_Subtraction_GP_Slotted = VAnt_Geometry:Subtract(VAnt_Rectangle_GP, VTmp_Subs)
   VAnt_Subtraction_GP_Slotted.Label = "GP_Slotted"
--

-- STEP 22: Creating medium
   VAnt_Medium_FR4 = VAnt_Project.Media:AddDielectric()
   VAnt_Medium_FR4.Label = "FR4"
   VAnt_Medium_FR4.DielectricModelling.RelativePermittivity = 4.4
   VAnt_Medium_FR4.DielectricModelling.LossTangent = 0.02
--

-- STEP 23: Create new solid.cuboid
   VTmp_Corner = cf.Point(-3.961, -3.074, 0.0)
   VAnt_Cuboid_Substrate = VAnt_Geometry:AddCuboid(VTmp_Corner, 62.583, 80.002, 1.6)
   VAnt_Cuboid_Substrate.Label = "Substrate"
--

-- STEP 24: Set solid medium
   VAnt_Cuboid_Substrate.Regions:Item(1).Medium = VAnt_Project.Media:Item("FR4")
--

-- STEP 25: Create new rectangular surface
   VTmp_Corner = cf.Point(-2.635, -3.074, 1.6)
   VAnt_Rectangle_RP = VAnt_Geometry:AddRectangle(VTmp_Corner, 60.198, 79.952)
   VAnt_Rectangle_RP.Label = "RP"
--

-- STEP 26: Create new rectangular surface
   VTmp_Corner = cf.Point(31.682, 31.154, 1.6)
   VAnt_Rectangle_GPSlot_0 = VAnt_Geometry:AddRectangle(VTmp_Corner, 7.934, 3.858)
   VAnt_Rectangle_GPSlot_0.Label = "GPSlot_0"
--

-- STEP 27: Create new rectangular surface
   VTmp_Corner = cf.Point(37.679, 56.361, 1.6)
   VAnt_Rectangle_GPSlot_1 = VAnt_Geometry:AddRectangle(VTmp_Corner, 1.545, 4.731)
   VAnt_Rectangle_GPSlot_1.Label = "GPSlot_1"
--

-- STEP 28: Create new rectangular surface
   VTmp_Corner = cf.Point(39.158, 82.355, 1.6)
   VAnt_Rectangle_GPSlot_2 = VAnt_Geometry:AddRectangle(VTmp_Corner, 3.809, 9.434)
   VAnt_Rectangle_GPSlot_2.Label = "GPSlot_2"
--

-- STEP 29: Create new rectangular surface
   VTmp_Corner = cf.Point(56.939, 52.865, 1.6)
   VAnt_Rectangle_GPSlot_3 = VAnt_Geometry:AddRectangle(VTmp_Corner, 2.483, 0.785)
   VAnt_Rectangle_GPSlot_3.Label = "GPSlot_3"
--

-- STEP 30: Create new rectangular surface
   VTmp_Corner = cf.Point(15.889, 34.842, 1.6)
   VAnt_Rectangle_GPSlot_4 = VAnt_Geometry:AddRectangle(VTmp_Corner, 1.226, 3.138)
   VAnt_Rectangle_GPSlot_4.Label = "GPSlot_4"
--

-- STEP 31: Create new rectangular surface
   VTmp_Corner = cf.Point(58.428, 77.311, 1.6)
   VAnt_Rectangle_GPSlot_5 = VAnt_Geometry:AddRectangle(VTmp_Corner, 3.401, 5.193)
   VAnt_Rectangle_GPSlot_5.Label = "GPSlot_5"
--

-- STEP 32: Create new rectangular surface
   VTmp_Corner = cf.Point(28.475, 45.825, 1.6)
   VAnt_Rectangle_GPSlot_6 = VAnt_Geometry:AddRectangle(VTmp_Corner, 2.593, 3.522)
   VAnt_Rectangle_GPSlot_6.Label = "GPSlot_6"
--

-- STEP 33: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(14.013, 74.956, 1.6)
   VTmp_Points[2] = cf.Point(11.2, 84.251, 1.6)
   VTmp_Points[3] = cf.Point(12.969, 77.18, 1.6)
   VAnt_Polygon_GPSlot_7 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_7.Label = "GPSlot_7"
--

-- STEP 34: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(46.38, -10.419, 1.6)
   VTmp_Points[2] = cf.Point(50.361, -0.503, 1.6)
   VTmp_Points[3] = cf.Point(51.138, 4.532, 1.6)
   VAnt_Polygon_GPSlot_8 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_8.Label = "GPSlot_8"
--

-- STEP 35: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(22.976, 41.624, 1.6)
   VTmp_Points[2] = cf.Point(23.211, 39.209, 1.6)
   VTmp_Points[3] = cf.Point(20.755, 40.843, 1.6)
   VAnt_Polygon_GPSlot_9 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_9.Label = "GPSlot_9"
--

-- STEP 36: Create new subtraction
   VTmp_Subs = {}
   VTmp_Subs[1] = VAnt_Rectangle_GPSlot_0
   VTmp_Subs[2] = VAnt_Rectangle_GPSlot_1
   VTmp_Subs[3] = VAnt_Rectangle_GPSlot_2
   VTmp_Subs[4] = VAnt_Rectangle_GPSlot_3
   VTmp_Subs[5] = VAnt_Rectangle_GPSlot_4
   VTmp_Subs[6] = VAnt_Rectangle_GPSlot_5
   VTmp_Subs[7] = VAnt_Rectangle_GPSlot_6
   VTmp_Subs[8] = VAnt_Polygon_GPSlot_7
   VTmp_Subs[9] = VAnt_Polygon_GPSlot_8
   VTmp_Subs[10] = VAnt_Polygon_GPSlot_9
   VAnt_Subtraction_RP_Slotted = VAnt_Geometry:Subtract(VAnt_Rectangle_RP, VTmp_Subs)
   VAnt_Subtraction_RP_Slotted.Label = "RP_Slotted"
--

-- STEP 37: Create new union
   VTmp_Parts = {}
   VTmp_Parts[1] = VAnt_Subtraction_GP_Slotted
   VTmp_Parts[2] = VAnt_Subtraction_RP_Slotted
   VTmp_Parts[3] = VAnt_Cuboid_Substrate
   VTmp_Parts[4] = VAnt_Polygon_Feed_Top
   VTmp_Parts[5] = VAnt_Polygon_Feed_Pos
   VTmp_Parts[6] = VAnt_Polygon_Feed_Neg
   VTmp_Parts[7] = VAnt_Polygon_Feed_Bot
   VAnt_Union_Onion = VAnt_Geometry:Union(VTmp_Parts)
   VAnt_Union_Onion.Label = "Onion"
--

-- STEP 38: Changing face medium
   VAnt_Union_Onion.Faces:Item("Face36").Medium = VAnt_Project.Media:Item("Perfect electric conductor")
--

-- STEP 39: Changing face medium
   VAnt_Union_Onion.Faces:Item("Face37").Medium = VAnt_Project.Media:Item("Perfect electric conductor")
--

-- STEP 40: Changing face medium
   VAnt_Union_Onion.Faces:Item("Face38").Medium = VAnt_Project.Media:Item("Perfect electric conductor")
--

-- STEP 41: Create new edge port
   VTmp_Pos = {}
   VTmp_Neg = {}
   VTmp_Pos[1] = VAnt_Union_Onion.Faces:Item("Face2")
   VTmp_Neg[1] = VAnt_Union_Onion.Faces:Item("Face3")
   VAnt_EPort_SourcePort = VAnt_Project.Ports:AddEdgePort(VTmp_Pos, VTmp_Neg)
   VAnt_EPort_SourcePort.Label = "SourcePort"
--

-- STEP 42: Get config file
   VAnt_Config = VAnt_Project.SolutionConfigurations[1]
--

-- STEP 43: Create new voltage source
   VAnt_VSource_VoltageSource = VAnt_Config.Sources:AddVoltageSource(VAnt_EPort_SourcePort)
   VAnt_VSource_VoltageSource.Impedance = 50.0
   VAnt_VSource_VoltageSource.Magnitude = 1.0
   VAnt_VSource_VoltageSource.Phase = 0.0
   VAnt_VSource_VoltageSource.Label = "VoltageSource"
--

-- STEP 44: Create new Far-Field request
   VAnt_Config.FarFields:Add(0.0, 0.0, 180.0, 360.0, 5.0, 5.0)
--
-- STEP 45: Set frequency range
   VAnt_tmp = VAnt_Config.Frequency:GetProperties()
   VAnt_tmp.Start  = 906500000.0
   VAnt_tmp.End    = 933500000.0
   VAnt_tmp.RangeType  = cf.Enums.FrequencyRangeTypeEnum.LinearSpacedDiscrete
   VAnt_tmp.NumberOfDiscreteValues = 2
   VAnt_Config.Frequency:SetProperties(VAnt_tmp)
--

-- STEP 46: Mesh the project
   VAnt_Project.Mesher.Settings.WireRadius = 0.001
   VAnt_Project.Mesher.Settings.MeshSizeOption = cf.Enums.MeshSizeOptionEnum.Coarse
   VAnt_Project.Mesher:Mesh()
--

-- STEP 47: Save project
   VSes_Application:SaveAs("C:/Users/project/0. My Work/1. Repositories/1. Very Unfriendly Train/Data/Simulations/637072128687662976_Primary/637072223066233344_1/1.cfx")
--

-- STEP 48: Run simulation
   VAnt_Project.Launcher.Settings.FEKO.Parallel.Enabled = true
   VAnt_Project.Launcher:RunFEKO()
--

-- STEP 49: Close project
   VSes_Application:CloseAllWindows()
--

-- STEP 1: Make a new project
   VAnt_Project    = VSes_Application:NewProject()
   VAnt_Geometry   = VAnt_Project.Geometry
--

-- STEP 2: Set project unit of measurement
   VAnt_Project.ModelUnit  = cf.Enums.ModelUnitEnum.Millimetres
--

-- STEP 3: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(57.867999999999995, 33.7, 1.6)
   VTmp_Points[2] = cf.Point(57.867999999999995, 35.84, 1.6)
   VTmp_Points[3] = cf.Point(59.517999999999994, 35.84, 1.6)
   VTmp_Points[4] = cf.Point(59.517999999999994, 33.7, 1.6)
   VAnt_Polygon_Feed_Top = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_Feed_Top.Label = "Feed_Top"
--

-- STEP 4: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(59.517999999999994, 35.84, 1.6)
   VTmp_Points[2] = cf.Point(59.517999999999994, 35.84, 0.8)
   VTmp_Points[3] = cf.Point(59.517999999999994, 33.7, 0.8)
   VTmp_Points[4] = cf.Point(59.517999999999994, 33.7, 1.6)
   VAnt_Polygon_Feed_Pos = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_Feed_Pos.Label = "Feed_Pos"
--

-- STEP 5: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(59.517999999999994, 35.84, 0.0)
   VTmp_Points[2] = cf.Point(59.517999999999994, 35.84, 0.8)
   VTmp_Points[3] = cf.Point(59.517999999999994, 33.7, 0.8)
   VTmp_Points[4] = cf.Point(59.517999999999994, 33.7, 0.0)
   VAnt_Polygon_Feed_Neg = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_Feed_Neg.Label = "Feed_Neg"
--

-- STEP 6: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(59.517999999999994, 33.7, 0.0)
   VTmp_Points[2] = cf.Point(59.517999999999994, 35.84, 0.0)
   VTmp_Points[3] = cf.Point(57.91799999999999, 35.84, 0.0)
   VTmp_Points[4] = cf.Point(57.91799999999999, 33.7, 0.0)
   VAnt_Polygon_Feed_Bot = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_Feed_Bot.Label = "Feed_Bot"
--

-- STEP 7: Create new rectangular surface
   VTmp_Corner = cf.Point(-4.068, -1.878, 0.0)
   VAnt_Rectangle_GP = VAnt_Geometry:AddRectangle(VTmp_Corner, 61.98599999999999, 75.256)
   VAnt_Rectangle_GP.Label = "GP"
--

-- STEP 8: Create new rectangular surface
   VTmp_Corner = cf.Point(-6.062, 96.527, 0.0)
   VAnt_Rectangle_GPSlot_0 = VAnt_Geometry:AddRectangle(VTmp_Corner, 9.237, 9.813)
   VAnt_Rectangle_GPSlot_0.Label = "GPSlot_0"
--

-- STEP 9: Create new rectangular surface
   VTmp_Corner = cf.Point(9.468, 20.689, 0.0)
   VAnt_Rectangle_GPSlot_1 = VAnt_Geometry:AddRectangle(VTmp_Corner, 0.223, 24.347)
   VAnt_Rectangle_GPSlot_1.Label = "GPSlot_1"
--

-- STEP 10: Create new rectangular surface
   VTmp_Corner = cf.Point(20.371, 55.898, 0.0)
   VAnt_Rectangle_GPSlot_2 = VAnt_Geometry:AddRectangle(VTmp_Corner, 9.769, 21.372)
   VAnt_Rectangle_GPSlot_2.Label = "GPSlot_2"
--

-- STEP 11: Create new rectangular surface
   VTmp_Corner = cf.Point(41.213, 56.215, 0.0)
   VAnt_Rectangle_GPSlot_3 = VAnt_Geometry:AddRectangle(VTmp_Corner, 4.775, 12.949)
   VAnt_Rectangle_GPSlot_3.Label = "GPSlot_3"
--

-- STEP 12: Create new rectangular surface
   VTmp_Corner = cf.Point(48.084, 81.75, 0.0)
   VAnt_Rectangle_GPSlot_4 = VAnt_Geometry:AddRectangle(VTmp_Corner, 9.623, 2.608)
   VAnt_Rectangle_GPSlot_4.Label = "GPSlot_4"
--

-- STEP 13: Create new rectangular surface
   VTmp_Corner = cf.Point(39.164, 13.85, 0.0)
   VAnt_Rectangle_GPSlot_5 = VAnt_Geometry:AddRectangle(VTmp_Corner, 11.146, 22.682)
   VAnt_Rectangle_GPSlot_5.Label = "GPSlot_5"
--

-- STEP 14: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(86.685, 138.206, 0.0)
   VTmp_Points[2] = cf.Point(73.575, 109.951, 0.0)
   VTmp_Points[3] = cf.Point(76.731, 106.019, 0.0)
   VAnt_Polygon_GPSlot_6 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_6.Label = "GPSlot_6"
--

-- STEP 15: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(21.712, 88.344, 0.0)
   VTmp_Points[2] = cf.Point(3.995, 128.258, 0.0)
   VTmp_Points[3] = cf.Point(18.942, 93.009, 0.0)
   VAnt_Polygon_GPSlot_7 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_7.Label = "GPSlot_7"
--

-- STEP 16: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(46.681, 19.147, 0.0)
   VTmp_Points[2] = cf.Point(61.351, -18.602, 0.0)
   VTmp_Points[3] = cf.Point(73.523, -0.549, 0.0)
   VAnt_Polygon_GPSlot_8 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_8.Label = "GPSlot_8"
--

-- STEP 17: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(24.237, 110.542, 0.0)
   VTmp_Points[2] = cf.Point(49.065, 79.345, 0.0)
   VTmp_Points[3] = cf.Point(57.145, 67.831, 0.0)
   VAnt_Polygon_GPSlot_9 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_9.Label = "GPSlot_9"
--

-- STEP 18: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(43.226, 36.514, 0.0)
   VTmp_Points[2] = cf.Point(58.473, -3.235, 0.0)
   VTmp_Points[3] = cf.Point(14.316, 11.792, 0.0)
   VAnt_Polygon_GPSlot_10 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_10.Label = "GPSlot_10"
--

-- STEP 19: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(1.959, 12.423, 0.0)
   VTmp_Points[2] = cf.Point(43.045, 6.638, 0.0)
   VTmp_Points[3] = cf.Point(46.971, 21.96, 0.0)
   VAnt_Polygon_GPSlot_11 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_11.Label = "GPSlot_11"
--

-- STEP 20: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(16.818, 54.431, 0.0)
   VTmp_Points[2] = cf.Point(39.874, 79.983, 0.0)
   VTmp_Points[3] = cf.Point(24.514, 74.273, 0.0)
   VAnt_Polygon_GPSlot_12 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_12.Label = "GPSlot_12"
--

-- STEP 21: Create new subtraction
   VTmp_Subs = {}
   VTmp_Subs[1] = VAnt_Rectangle_GPSlot_0
   VTmp_Subs[2] = VAnt_Rectangle_GPSlot_1
   VTmp_Subs[3] = VAnt_Rectangle_GPSlot_2
   VTmp_Subs[4] = VAnt_Rectangle_GPSlot_3
   VTmp_Subs[5] = VAnt_Rectangle_GPSlot_4
   VTmp_Subs[6] = VAnt_Rectangle_GPSlot_5
   VTmp_Subs[7] = VAnt_Polygon_GPSlot_6
   VTmp_Subs[8] = VAnt_Polygon_GPSlot_7
   VTmp_Subs[9] = VAnt_Polygon_GPSlot_8
   VTmp_Subs[10] = VAnt_Polygon_GPSlot_9
   VTmp_Subs[11] = VAnt_Polygon_GPSlot_10
   VTmp_Subs[12] = VAnt_Polygon_GPSlot_11
   VTmp_Subs[13] = VAnt_Polygon_GPSlot_12
   VAnt_Subtraction_GP_Slotted = VAnt_Geometry:Subtract(VAnt_Rectangle_GP, VTmp_Subs)
   VAnt_Subtraction_GP_Slotted.Label = "GP_Slotted"
--

-- STEP 22: Creating medium
   VAnt_Medium_FR4 = VAnt_Project.Media:AddDielectric()
   VAnt_Medium_FR4.Label = "FR4"
   VAnt_Medium_FR4.DielectricModelling.RelativePermittivity = 4.4
   VAnt_Medium_FR4.DielectricModelling.LossTangent = 0.02
--

-- STEP 23: Create new solid.cuboid
   VTmp_Corner = cf.Point(-4.068, -2.793, 0.0)
   VAnt_Cuboid_Substrate = VAnt_Geometry:AddCuboid(VTmp_Corner, 61.98599999999999, 79.179, 1.6)
   VAnt_Cuboid_Substrate.Label = "Substrate"
--

-- STEP 24: Set solid medium
   VAnt_Cuboid_Substrate.Regions:Item(1).Medium = VAnt_Project.Media:Item("FR4")
--

-- STEP 25: Create new rectangular surface
   VTmp_Corner = cf.Point(-2.508, -2.793, 1.6)
   VAnt_Rectangle_RP = VAnt_Geometry:AddRectangle(VTmp_Corner, 60.376, 79.129)
   VAnt_Rectangle_RP.Label = "RP"
--

-- STEP 26: Create new rectangular surface
   VTmp_Corner = cf.Point(31.786, 30.08, 1.6)
   VAnt_Rectangle_GPSlot_0 = VAnt_Geometry:AddRectangle(VTmp_Corner, 9.896, 3.015)
   VAnt_Rectangle_GPSlot_0.Label = "GPSlot_0"
--

-- STEP 27: Create new rectangular surface
   VTmp_Corner = cf.Point(37.175, 56.343, 1.6)
   VAnt_Rectangle_GPSlot_1 = VAnt_Geometry:AddRectangle(VTmp_Corner, 2.729, 4.179)
   VAnt_Rectangle_GPSlot_1.Label = "GPSlot_1"
--

-- STEP 28: Create new rectangular surface
   VTmp_Corner = cf.Point(38.61, 81.571, 1.6)
   VAnt_Rectangle_GPSlot_2 = VAnt_Geometry:AddRectangle(VTmp_Corner, 4.111, 9.09)
   VAnt_Rectangle_GPSlot_2.Label = "GPSlot_2"
--

-- STEP 29: Create new rectangular surface
   VTmp_Corner = cf.Point(56.121, 53.518, 1.6)
   VAnt_Rectangle_GPSlot_3 = VAnt_Geometry:AddRectangle(VTmp_Corner, 2.891, 0.546)
   VAnt_Rectangle_GPSlot_3.Label = "GPSlot_3"
--

-- STEP 30: Create new rectangular surface
   VTmp_Corner = cf.Point(16.307, 34.673, 1.6)
   VAnt_Rectangle_GPSlot_4 = VAnt_Geometry:AddRectangle(VTmp_Corner, 1.301, 2.325)
   VAnt_Rectangle_GPSlot_4.Label = "GPSlot_4"
--

-- STEP 31: Create new rectangular surface
   VTmp_Corner = cf.Point(58.044, 76.948, 1.6)
   VAnt_Rectangle_GPSlot_5 = VAnt_Geometry:AddRectangle(VTmp_Corner, 3.924, 4.397)
   VAnt_Rectangle_GPSlot_5.Label = "GPSlot_5"
--

-- STEP 32: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(14.435, 74.87, 1.6)
   VTmp_Points[2] = cf.Point(11.716, 83.368, 1.6)
   VTmp_Points[3] = cf.Point(11.874, 79.55, 1.6)
   VAnt_Polygon_GPSlot_6 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_6.Label = "GPSlot_6"
--

-- STEP 33: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(47.262, -9.787, 1.6)
   VTmp_Points[2] = cf.Point(50.883, -0.067, 1.6)
   VTmp_Points[3] = cf.Point(50.176, 4.258, 1.6)
   VAnt_Polygon_GPSlot_7 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_7.Label = "GPSlot_7"
--

-- STEP 34: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(24.526, 41.046, 1.6)
   VTmp_Points[2] = cf.Point(22.684, 39.647, 1.6)
   VTmp_Points[3] = cf.Point(20.861, 42.68, 1.6)
   VAnt_Polygon_GPSlot_8 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_8.Label = "GPSlot_8"
--

-- STEP 35: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(43.784, 20.663, 1.6)
   VTmp_Points[2] = cf.Point(43.897, 20.892, 1.6)
   VTmp_Points[3] = cf.Point(44.088, 21.929, 1.6)
   VAnt_Polygon_GPSlot_9 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_9.Label = "GPSlot_9"
--

-- STEP 36: Create new subtraction
   VTmp_Subs = {}
   VTmp_Subs[1] = VAnt_Rectangle_GPSlot_0
   VTmp_Subs[2] = VAnt_Rectangle_GPSlot_1
   VTmp_Subs[3] = VAnt_Rectangle_GPSlot_2
   VTmp_Subs[4] = VAnt_Rectangle_GPSlot_3
   VTmp_Subs[5] = VAnt_Rectangle_GPSlot_4
   VTmp_Subs[6] = VAnt_Rectangle_GPSlot_5
   VTmp_Subs[7] = VAnt_Polygon_GPSlot_6
   VTmp_Subs[8] = VAnt_Polygon_GPSlot_7
   VTmp_Subs[9] = VAnt_Polygon_GPSlot_8
   VTmp_Subs[10] = VAnt_Polygon_GPSlot_9
   VAnt_Subtraction_RP_Slotted = VAnt_Geometry:Subtract(VAnt_Rectangle_RP, VTmp_Subs)
   VAnt_Subtraction_RP_Slotted.Label = "RP_Slotted"
--

-- STEP 37: Create new union
   VTmp_Parts = {}
   VTmp_Parts[1] = VAnt_Subtraction_GP_Slotted
   VTmp_Parts[2] = VAnt_Subtraction_RP_Slotted
   VTmp_Parts[3] = VAnt_Cuboid_Substrate
   VTmp_Parts[4] = VAnt_Polygon_Feed_Top
   VTmp_Parts[5] = VAnt_Polygon_Feed_Pos
   VTmp_Parts[6] = VAnt_Polygon_Feed_Neg
   VTmp_Parts[7] = VAnt_Polygon_Feed_Bot
   VAnt_Union_Onion = VAnt_Geometry:Union(VTmp_Parts)
   VAnt_Union_Onion.Label = "Onion"
--

-- STEP 38: Changing face medium
   VAnt_Union_Onion.Faces:Item("Face36").Medium = VAnt_Project.Media:Item("Perfect electric conductor")
--

-- STEP 39: Changing face medium
   VAnt_Union_Onion.Faces:Item("Face37").Medium = VAnt_Project.Media:Item("Perfect electric conductor")
--

-- STEP 40: Changing face medium
   VAnt_Union_Onion.Faces:Item("Face38").Medium = VAnt_Project.Media:Item("Perfect electric conductor")
--

-- STEP 41: Create new edge port
   VTmp_Pos = {}
   VTmp_Neg = {}
   VTmp_Pos[1] = VAnt_Union_Onion.Faces:Item("Face2")
   VTmp_Neg[1] = VAnt_Union_Onion.Faces:Item("Face3")
   VAnt_EPort_SourcePort = VAnt_Project.Ports:AddEdgePort(VTmp_Pos, VTmp_Neg)
   VAnt_EPort_SourcePort.Label = "SourcePort"
--

-- STEP 42: Get config file
   VAnt_Config = VAnt_Project.SolutionConfigurations[1]
--

-- STEP 43: Create new voltage source
   VAnt_VSource_VoltageSource = VAnt_Config.Sources:AddVoltageSource(VAnt_EPort_SourcePort)
   VAnt_VSource_VoltageSource.Impedance = 50.0
   VAnt_VSource_VoltageSource.Magnitude = 1.0
   VAnt_VSource_VoltageSource.Phase = 0.0
   VAnt_VSource_VoltageSource.Label = "VoltageSource"
--

-- STEP 44: Create new Far-Field request
   VAnt_Config.FarFields:Add(0.0, 0.0, 180.0, 360.0, 5.0, 5.0)
--
-- STEP 45: Set frequency range
   VAnt_tmp = VAnt_Config.Frequency:GetProperties()
   VAnt_tmp.Start  = 906500000.0
   VAnt_tmp.End    = 933500000.0
   VAnt_tmp.RangeType  = cf.Enums.FrequencyRangeTypeEnum.LinearSpacedDiscrete
   VAnt_tmp.NumberOfDiscreteValues = 2
   VAnt_Config.Frequency:SetProperties(VAnt_tmp)
--

-- STEP 46: Mesh the project
   VAnt_Project.Mesher.Settings.WireRadius = 0.001
   VAnt_Project.Mesher.Settings.MeshSizeOption = cf.Enums.MeshSizeOptionEnum.Coarse
   VAnt_Project.Mesher:Mesh()
--

-- STEP 47: Save project
   VSes_Application:SaveAs("C:/Users/project/0. My Work/1. Repositories/1. Very Unfriendly Train/Data/Simulations/637072128687662976_Primary/637072223066233344_2/2.cfx")
--

-- STEP 48: Run simulation
   VAnt_Project.Launcher.Settings.FEKO.Parallel.Enabled = true
   VAnt_Project.Launcher:RunFEKO()
--

-- STEP 49: Close project
   VSes_Application:CloseAllWindows()
--

-- STEP 1: Make a new project
   VAnt_Project    = VSes_Application:NewProject()
   VAnt_Geometry   = VAnt_Project.Geometry
--

-- STEP 2: Set project unit of measurement
   VAnt_Project.ModelUnit  = cf.Enums.ModelUnitEnum.Millimetres
--

-- STEP 3: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(56.919000000000004, 33.272499999999994, 1.6)
   VTmp_Points[2] = cf.Point(56.919000000000004, 35.43149999999999, 1.6)
   VTmp_Points[3] = cf.Point(58.569, 35.43149999999999, 1.6)
   VTmp_Points[4] = cf.Point(58.569, 33.272499999999994, 1.6)
   VAnt_Polygon_Feed_Top = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_Feed_Top.Label = "Feed_Top"
--

-- STEP 4: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(58.569, 35.43149999999999, 1.6)
   VTmp_Points[2] = cf.Point(58.569, 35.43149999999999, 0.8)
   VTmp_Points[3] = cf.Point(58.569, 33.272499999999994, 0.8)
   VTmp_Points[4] = cf.Point(58.569, 33.272499999999994, 1.6)
   VAnt_Polygon_Feed_Pos = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_Feed_Pos.Label = "Feed_Pos"
--

-- STEP 5: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(58.569, 35.43149999999999, 0.0)
   VTmp_Points[2] = cf.Point(58.569, 35.43149999999999, 0.8)
   VTmp_Points[3] = cf.Point(58.569, 33.272499999999994, 0.8)
   VTmp_Points[4] = cf.Point(58.569, 33.272499999999994, 0.0)
   VAnt_Polygon_Feed_Neg = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_Feed_Neg.Label = "Feed_Neg"
--

-- STEP 6: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(58.569, 33.272499999999994, 0.0)
   VTmp_Points[2] = cf.Point(58.569, 35.43149999999999, 0.0)
   VTmp_Points[3] = cf.Point(56.969, 35.43149999999999, 0.0)
   VTmp_Points[4] = cf.Point(56.969, 33.272499999999994, 0.0)
   VAnt_Polygon_Feed_Bot = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_Feed_Bot.Label = "Feed_Bot"
--

-- STEP 7: Create new rectangular surface
   VTmp_Corner = cf.Point(-3.883, -1.274, 0.0)
   VAnt_Rectangle_GP = VAnt_Geometry:AddRectangle(VTmp_Corner, 60.852000000000004, 75.499)
   VAnt_Rectangle_GP.Label = "GP"
--

-- STEP 8: Create new rectangular surface
   VTmp_Corner = cf.Point(-4.328, 100.845, 0.0)
   VAnt_Rectangle_GPSlot_0 = VAnt_Geometry:AddRectangle(VTmp_Corner, 10.332, 11.102)
   VAnt_Rectangle_GPSlot_0.Label = "GPSlot_0"
--

-- STEP 9: Create new rectangular surface
   VTmp_Corner = cf.Point(9.913, 23.114, 0.0)
   VAnt_Rectangle_GPSlot_1 = VAnt_Geometry:AddRectangle(VTmp_Corner, 1.651, 23.455)
   VAnt_Rectangle_GPSlot_1.Label = "GPSlot_1"
--

-- STEP 10: Create new rectangular surface
   VTmp_Corner = cf.Point(18.651, 54.17, 0.0)
   VAnt_Rectangle_GPSlot_2 = VAnt_Geometry:AddRectangle(VTmp_Corner, 11.858, 22.119)
   VAnt_Rectangle_GPSlot_2.Label = "GPSlot_2"
--

-- STEP 11: Create new rectangular surface
   VTmp_Corner = cf.Point(41.517, 60.078, 0.0)
   VAnt_Rectangle_GPSlot_3 = VAnt_Geometry:AddRectangle(VTmp_Corner, 2.994, 9.913)
   VAnt_Rectangle_GPSlot_3.Label = "GPSlot_3"
--

-- STEP 12: Create new rectangular surface
   VTmp_Corner = cf.Point(44.971, 84.445, 0.0)
   VAnt_Rectangle_GPSlot_4 = VAnt_Geometry:AddRectangle(VTmp_Corner, 10.109, 0.311)
   VAnt_Rectangle_GPSlot_4.Label = "GPSlot_4"
--

-- STEP 13: Create new rectangular surface
   VTmp_Corner = cf.Point(28.527, 49.484, 0.0)
   VAnt_Rectangle_GPSlot_5 = VAnt_Geometry:AddRectangle(VTmp_Corner, 14.563, 12.974)
   VAnt_Rectangle_GPSlot_5.Label = "GPSlot_5"
--

-- STEP 14: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(85.619, 133.409, 0.0)
   VTmp_Points[2] = cf.Point(75.327, 111.94, 0.0)
   VTmp_Points[3] = cf.Point(75.53, 106.781, 0.0)
   VAnt_Polygon_GPSlot_6 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_6.Label = "GPSlot_6"
--

-- STEP 15: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(24.057, 91.27, 0.0)
   VTmp_Points[2] = cf.Point(4.124, 130.416, 0.0)
   VTmp_Points[3] = cf.Point(14.783, 93.635, 0.0)
   VAnt_Polygon_GPSlot_7 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_7.Label = "GPSlot_7"
--

-- STEP 16: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(50.405, 19.689, 0.0)
   VTmp_Points[2] = cf.Point(60.821, -16.868, 0.0)
   VTmp_Points[3] = cf.Point(73.319, 0.457, 0.0)
   VAnt_Polygon_GPSlot_8 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_8.Label = "GPSlot_8"
--

-- STEP 17: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(22.925, 108.886, 0.0)
   VTmp_Points[2] = cf.Point(46.826, 81.342, 0.0)
   VTmp_Points[3] = cf.Point(55.613, 64.996, 0.0)
   VAnt_Polygon_GPSlot_9 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_9.Label = "GPSlot_9"
--

-- STEP 18: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(42.581, 34.826, 0.0)
   VTmp_Points[2] = cf.Point(54.714, -6.776, 0.0)
   VTmp_Points[3] = cf.Point(15.323, 12.092, 0.0)
   VAnt_Polygon_GPSlot_10 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_10.Label = "GPSlot_10"
--

-- STEP 19: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(-0.376, 14.979, 0.0)
   VTmp_Points[2] = cf.Point(39.768, 9.179, 0.0)
   VTmp_Points[3] = cf.Point(48.418, 21.089, 0.0)
   VAnt_Polygon_GPSlot_11 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_11.Label = "GPSlot_11"
--

-- STEP 20: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(18.581, 54.468, 0.0)
   VTmp_Points[2] = cf.Point(38.128, 79.784, 0.0)
   VTmp_Points[3] = cf.Point(20.67, 74.673, 0.0)
   VAnt_Polygon_GPSlot_12 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_12.Label = "GPSlot_12"
--

-- STEP 21: Create new subtraction
   VTmp_Subs = {}
   VTmp_Subs[1] = VAnt_Rectangle_GPSlot_0
   VTmp_Subs[2] = VAnt_Rectangle_GPSlot_1
   VTmp_Subs[3] = VAnt_Rectangle_GPSlot_2
   VTmp_Subs[4] = VAnt_Rectangle_GPSlot_3
   VTmp_Subs[5] = VAnt_Rectangle_GPSlot_4
   VTmp_Subs[6] = VAnt_Rectangle_GPSlot_5
   VTmp_Subs[7] = VAnt_Polygon_GPSlot_6
   VTmp_Subs[8] = VAnt_Polygon_GPSlot_7
   VTmp_Subs[9] = VAnt_Polygon_GPSlot_8
   VTmp_Subs[10] = VAnt_Polygon_GPSlot_9
   VTmp_Subs[11] = VAnt_Polygon_GPSlot_10
   VTmp_Subs[12] = VAnt_Polygon_GPSlot_11
   VTmp_Subs[13] = VAnt_Polygon_GPSlot_12
   VAnt_Subtraction_GP_Slotted = VAnt_Geometry:Subtract(VAnt_Rectangle_GP, VTmp_Subs)
   VAnt_Subtraction_GP_Slotted.Label = "GP_Slotted"
--

-- STEP 22: Creating medium
   VAnt_Medium_FR4 = VAnt_Project.Media:AddDielectric()
   VAnt_Medium_FR4.Label = "FR4"
   VAnt_Medium_FR4.DielectricModelling.RelativePermittivity = 4.4
   VAnt_Medium_FR4.DielectricModelling.LossTangent = 0.02
--

-- STEP 23: Create new solid.cuboid
   VTmp_Corner = cf.Point(-3.883, -3.002, 0.0)
   VAnt_Cuboid_Substrate = VAnt_Geometry:AddCuboid(VTmp_Corner, 60.852000000000004, 80.008, 1.6)
   VAnt_Cuboid_Substrate.Label = "Substrate"
--

-- STEP 24: Set solid medium
   VAnt_Cuboid_Substrate.Regions:Item(1).Medium = VAnt_Project.Media:Item("FR4")
--

-- STEP 25: Create new rectangular surface
   VTmp_Corner = cf.Point(-2.928, -3.002, 1.6)
   VAnt_Rectangle_RP = VAnt_Geometry:AddRectangle(VTmp_Corner, 59.847, 79.958)
   VAnt_Rectangle_RP.Label = "RP"
--

-- STEP 26: Create new rectangular surface
   VTmp_Corner = cf.Point(31.652, 31.789, 1.6)
   VAnt_Rectangle_GPSlot_0 = VAnt_Geometry:AddRectangle(VTmp_Corner, 10.232, 2.732)
   VAnt_Rectangle_GPSlot_0.Label = "GPSlot_0"
--

-- STEP 27: Create new rectangular surface
   VTmp_Corner = cf.Point(37.42, 55.922, 1.6)
   VAnt_Rectangle_GPSlot_1 = VAnt_Geometry:AddRectangle(VTmp_Corner, 2.783, 5.52)
   VAnt_Rectangle_GPSlot_1.Label = "GPSlot_1"
--

-- STEP 28: Create new rectangular surface
   VTmp_Corner = cf.Point(40.278, 82.14, 1.6)
   VAnt_Rectangle_GPSlot_2 = VAnt_Geometry:AddRectangle(VTmp_Corner, 4.305, 8.828)
   VAnt_Rectangle_GPSlot_2.Label = "GPSlot_2"
--

-- STEP 29: Create new rectangular surface
   VTmp_Corner = cf.Point(55.587, 53.957, 1.6)
   VAnt_Rectangle_GPSlot_3 = VAnt_Geometry:AddRectangle(VTmp_Corner, 2.748, 0.467)
   VAnt_Rectangle_GPSlot_3.Label = "GPSlot_3"
--

-- STEP 30: Create new rectangular surface
   VTmp_Corner = cf.Point(15.889, 34.842, 1.6)
   VAnt_Rectangle_GPSlot_4 = VAnt_Geometry:AddRectangle(VTmp_Corner, 1.226, 3.138)
   VAnt_Rectangle_GPSlot_4.Label = "GPSlot_4"
--

-- STEP 31: Create new rectangular surface
   VTmp_Corner = cf.Point(57.695, 77.268, 1.6)
   VAnt_Rectangle_GPSlot_5 = VAnt_Geometry:AddRectangle(VTmp_Corner, 3.136, 4.322)
   VAnt_Rectangle_GPSlot_5.Label = "GPSlot_5"
--

-- STEP 32: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(13.529, 75.764, 1.6)
   VTmp_Points[2] = cf.Point(10.251, 85.082, 1.6)
   VTmp_Points[3] = cf.Point(13.475, 77.467, 1.6)
   VAnt_Polygon_GPSlot_6 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_6.Label = "GPSlot_6"
--

-- STEP 33: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(46.102, -10.679, 1.6)
   VTmp_Points[2] = cf.Point(50.568, 0.775, 1.6)
   VTmp_Points[3] = cf.Point(50.104, 3.22, 1.6)
   VAnt_Polygon_GPSlot_7 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_7.Label = "GPSlot_7"
--

-- STEP 34: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(24.795, 43.257, 1.6)
   VTmp_Points[2] = cf.Point(22.474, 39.75, 1.6)
   VTmp_Points[3] = cf.Point(20.929, 41.483, 1.6)
   VAnt_Polygon_GPSlot_8 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_8.Label = "GPSlot_8"
--

-- STEP 35: Create new subtraction
   VTmp_Subs = {}
   VTmp_Subs[1] = VAnt_Rectangle_GPSlot_0
   VTmp_Subs[2] = VAnt_Rectangle_GPSlot_1
   VTmp_Subs[3] = VAnt_Rectangle_GPSlot_2
   VTmp_Subs[4] = VAnt_Rectangle_GPSlot_3
   VTmp_Subs[5] = VAnt_Rectangle_GPSlot_4
   VTmp_Subs[6] = VAnt_Rectangle_GPSlot_5
   VTmp_Subs[7] = VAnt_Polygon_GPSlot_6
   VTmp_Subs[8] = VAnt_Polygon_GPSlot_7
   VTmp_Subs[9] = VAnt_Polygon_GPSlot_8
   VAnt_Subtraction_RP_Slotted = VAnt_Geometry:Subtract(VAnt_Rectangle_RP, VTmp_Subs)
   VAnt_Subtraction_RP_Slotted.Label = "RP_Slotted"
--

-- STEP 36: Create new union
   VTmp_Parts = {}
   VTmp_Parts[1] = VAnt_Subtraction_GP_Slotted
   VTmp_Parts[2] = VAnt_Subtraction_RP_Slotted
   VTmp_Parts[3] = VAnt_Cuboid_Substrate
   VTmp_Parts[4] = VAnt_Polygon_Feed_Top
   VTmp_Parts[5] = VAnt_Polygon_Feed_Pos
   VTmp_Parts[6] = VAnt_Polygon_Feed_Neg
   VTmp_Parts[7] = VAnt_Polygon_Feed_Bot
   VAnt_Union_Onion = VAnt_Geometry:Union(VTmp_Parts)
   VAnt_Union_Onion.Label = "Onion"
--

-- STEP 37: Changing face medium
   VAnt_Union_Onion.Faces:Item("Face35").Medium = VAnt_Project.Media:Item("Perfect electric conductor")
--

-- STEP 38: Changing face medium
   VAnt_Union_Onion.Faces:Item("Face36").Medium = VAnt_Project.Media:Item("Perfect electric conductor")
--

-- STEP 39: Changing face medium
   VAnt_Union_Onion.Faces:Item("Face37").Medium = VAnt_Project.Media:Item("Perfect electric conductor")
--

-- STEP 40: Create new edge port
   VTmp_Pos = {}
   VTmp_Neg = {}
   VTmp_Pos[1] = VAnt_Union_Onion.Faces:Item("Face2")
   VTmp_Neg[1] = VAnt_Union_Onion.Faces:Item("Face3")
   VAnt_EPort_SourcePort = VAnt_Project.Ports:AddEdgePort(VTmp_Pos, VTmp_Neg)
   VAnt_EPort_SourcePort.Label = "SourcePort"
--

-- STEP 41: Get config file
   VAnt_Config = VAnt_Project.SolutionConfigurations[1]
--

-- STEP 42: Create new voltage source
   VAnt_VSource_VoltageSource = VAnt_Config.Sources:AddVoltageSource(VAnt_EPort_SourcePort)
   VAnt_VSource_VoltageSource.Impedance = 50.0
   VAnt_VSource_VoltageSource.Magnitude = 1.0
   VAnt_VSource_VoltageSource.Phase = 0.0
   VAnt_VSource_VoltageSource.Label = "VoltageSource"
--

-- STEP 43: Create new Far-Field request
   VAnt_Config.FarFields:Add(0.0, 0.0, 180.0, 360.0, 5.0, 5.0)
--
-- STEP 44: Set frequency range
   VAnt_tmp = VAnt_Config.Frequency:GetProperties()
   VAnt_tmp.Start  = 906500000.0
   VAnt_tmp.End    = 933500000.0
   VAnt_tmp.RangeType  = cf.Enums.FrequencyRangeTypeEnum.LinearSpacedDiscrete
   VAnt_tmp.NumberOfDiscreteValues = 2
   VAnt_Config.Frequency:SetProperties(VAnt_tmp)
--

-- STEP 45: Mesh the project
   VAnt_Project.Mesher.Settings.WireRadius = 0.001
   VAnt_Project.Mesher.Settings.MeshSizeOption = cf.Enums.MeshSizeOptionEnum.Coarse
   VAnt_Project.Mesher:Mesh()
--

-- STEP 46: Save project
   VSes_Application:SaveAs("C:/Users/project/0. My Work/1. Repositories/1. Very Unfriendly Train/Data/Simulations/637072128687662976_Primary/637072223066233344_3/3.cfx")
--

-- STEP 47: Run simulation
   VAnt_Project.Launcher.Settings.FEKO.Parallel.Enabled = true
   VAnt_Project.Launcher:RunFEKO()
--

-- STEP 48: Close project
   VSes_Application:CloseAllWindows()
--

-- STEP 1: Make a new project
   VAnt_Project    = VSes_Application:NewProject()
   VAnt_Geometry   = VAnt_Project.Geometry
--

-- STEP 2: Set project unit of measurement
   VAnt_Project.ModelUnit  = cf.Enums.ModelUnitEnum.Millimetres
--

-- STEP 3: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(56.684000000000005, 33.5295, 1.6)
   VTmp_Points[2] = cf.Point(56.684000000000005, 35.692499999999995, 1.6)
   VTmp_Points[3] = cf.Point(58.334, 35.692499999999995, 1.6)
   VTmp_Points[4] = cf.Point(58.334, 33.5295, 1.6)
   VAnt_Polygon_Feed_Top = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_Feed_Top.Label = "Feed_Top"
--

-- STEP 4: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(58.334, 35.692499999999995, 1.6)
   VTmp_Points[2] = cf.Point(58.334, 35.692499999999995, 0.8)
   VTmp_Points[3] = cf.Point(58.334, 33.5295, 0.8)
   VTmp_Points[4] = cf.Point(58.334, 33.5295, 1.6)
   VAnt_Polygon_Feed_Pos = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_Feed_Pos.Label = "Feed_Pos"
--

-- STEP 5: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(58.334, 35.692499999999995, 0.0)
   VTmp_Points[2] = cf.Point(58.334, 35.692499999999995, 0.8)
   VTmp_Points[3] = cf.Point(58.334, 33.5295, 0.8)
   VTmp_Points[4] = cf.Point(58.334, 33.5295, 0.0)
   VAnt_Polygon_Feed_Neg = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_Feed_Neg.Label = "Feed_Neg"
--

-- STEP 6: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(58.334, 33.5295, 0.0)
   VTmp_Points[2] = cf.Point(58.334, 35.692499999999995, 0.0)
   VTmp_Points[3] = cf.Point(56.734, 35.692499999999995, 0.0)
   VTmp_Points[4] = cf.Point(56.734, 33.5295, 0.0)
   VAnt_Polygon_Feed_Bot = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_Feed_Bot.Label = "Feed_Bot"
--

-- STEP 7: Create new rectangular surface
   VTmp_Corner = cf.Point(-3.796, -1.675, 0.0)
   VAnt_Rectangle_GP = VAnt_Geometry:AddRectangle(VTmp_Corner, 60.53, 73.558)
   VAnt_Rectangle_GP.Label = "GP"
--

-- STEP 8: Create new rectangular surface
   VTmp_Corner = cf.Point(-4.548, 98.572, 0.0)
   VAnt_Rectangle_GPSlot_0 = VAnt_Geometry:AddRectangle(VTmp_Corner, 9.035, 9.461)
   VAnt_Rectangle_GPSlot_0.Label = "GPSlot_0"
--

-- STEP 9: Create new rectangular surface
   VTmp_Corner = cf.Point(11.628, 19.669, 0.0)
   VAnt_Rectangle_GPSlot_1 = VAnt_Geometry:AddRectangle(VTmp_Corner, 0.466, 21.447)
   VAnt_Rectangle_GPSlot_1.Label = "GPSlot_1"
--

-- STEP 10: Create new rectangular surface
   VTmp_Corner = cf.Point(17.675, 58.73, 0.0)
   VAnt_Rectangle_GPSlot_2 = VAnt_Geometry:AddRectangle(VTmp_Corner, 12.573, 21.319)
   VAnt_Rectangle_GPSlot_2.Label = "GPSlot_2"
--

-- STEP 11: Create new rectangular surface
   VTmp_Corner = cf.Point(40.979, 53.128, 0.0)
   VAnt_Rectangle_GPSlot_3 = VAnt_Geometry:AddRectangle(VTmp_Corner, 4.611, 10.413)
   VAnt_Rectangle_GPSlot_3.Label = "GPSlot_3"
--

-- STEP 12: Create new rectangular surface
   VTmp_Corner = cf.Point(49.296, 85.024, 0.0)
   VAnt_Rectangle_GPSlot_4 = VAnt_Geometry:AddRectangle(VTmp_Corner, 8.228, 0.412)
   VAnt_Rectangle_GPSlot_4.Label = "GPSlot_4"
--

-- STEP 13: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(86.881, 133.647, 0.0)
   VTmp_Points[2] = cf.Point(74.157, 109.118, 0.0)
   VTmp_Points[3] = cf.Point(77.207, 105.332, 0.0)
   VAnt_Polygon_GPSlot_5 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_5.Label = "GPSlot_5"
--

-- STEP 14: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(24.678, 87.654, 0.0)
   VTmp_Points[2] = cf.Point(2.867, 127.524, 0.0)
   VTmp_Points[3] = cf.Point(20.947, 91.098, 0.0)
   VAnt_Polygon_GPSlot_6 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_6.Label = "GPSlot_6"
--

-- STEP 15: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(46.174, 21.731, 0.0)
   VTmp_Points[2] = cf.Point(57.424, -17.139, 0.0)
   VTmp_Points[3] = cf.Point(75.009, -2.528, 0.0)
   VAnt_Polygon_GPSlot_7 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_7.Label = "GPSlot_7"
--

-- STEP 16: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(20.775, 105.939, 0.0)
   VTmp_Points[2] = cf.Point(50.17, 77.635, 0.0)
   VTmp_Points[3] = cf.Point(56.362, 71.252, 0.0)
   VAnt_Polygon_GPSlot_8 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_8.Label = "GPSlot_8"
--

-- STEP 17: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(40.586, 34.701, 0.0)
   VTmp_Points[2] = cf.Point(55.855, -3.077, 0.0)
   VTmp_Points[3] = cf.Point(16.493, 11.929, 0.0)
   VAnt_Polygon_GPSlot_9 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_9.Label = "GPSlot_9"
--

-- STEP 18: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(3.055, 11.163, 0.0)
   VTmp_Points[2] = cf.Point(42.84, 8.566, 0.0)
   VTmp_Points[3] = cf.Point(49.599, 19.191, 0.0)
   VAnt_Polygon_GPSlot_10 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_10.Label = "GPSlot_10"
--

-- STEP 19: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(17.758, 55.441, 0.0)
   VTmp_Points[2] = cf.Point(36.184, 77.669, 0.0)
   VTmp_Points[3] = cf.Point(23.315, 70.715, 0.0)
   VAnt_Polygon_GPSlot_11 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_11.Label = "GPSlot_11"
--

-- STEP 20: Create new subtraction
   VTmp_Subs = {}
   VTmp_Subs[1] = VAnt_Rectangle_GPSlot_0
   VTmp_Subs[2] = VAnt_Rectangle_GPSlot_1
   VTmp_Subs[3] = VAnt_Rectangle_GPSlot_2
   VTmp_Subs[4] = VAnt_Rectangle_GPSlot_3
   VTmp_Subs[5] = VAnt_Rectangle_GPSlot_4
   VTmp_Subs[6] = VAnt_Polygon_GPSlot_5
   VTmp_Subs[7] = VAnt_Polygon_GPSlot_6
   VTmp_Subs[8] = VAnt_Polygon_GPSlot_7
   VTmp_Subs[9] = VAnt_Polygon_GPSlot_8
   VTmp_Subs[10] = VAnt_Polygon_GPSlot_9
   VTmp_Subs[11] = VAnt_Polygon_GPSlot_10
   VTmp_Subs[12] = VAnt_Polygon_GPSlot_11
   VAnt_Subtraction_GP_Slotted = VAnt_Geometry:Subtract(VAnt_Rectangle_GP, VTmp_Subs)
   VAnt_Subtraction_GP_Slotted.Label = "GP_Slotted"
--

-- STEP 21: Creating medium
   VAnt_Medium_FR4 = VAnt_Project.Media:AddDielectric()
   VAnt_Medium_FR4.Label = "FR4"
   VAnt_Medium_FR4.DielectricModelling.RelativePermittivity = 4.4
   VAnt_Medium_FR4.DielectricModelling.LossTangent = 0.02
--

-- STEP 22: Create new solid.cuboid
   VTmp_Corner = cf.Point(-3.796, -2.741, 0.0)
   VAnt_Cuboid_Substrate = VAnt_Geometry:AddCuboid(VTmp_Corner, 60.53, 80.709, 1.6)
   VAnt_Cuboid_Substrate.Label = "Substrate"
--

-- STEP 23: Set solid medium
   VAnt_Cuboid_Substrate.Regions:Item(1).Medium = VAnt_Project.Media:Item("FR4")
--

-- STEP 24: Create new rectangular surface
   VTmp_Corner = cf.Point(-2.342, -2.741, 1.6)
   VAnt_Rectangle_RP = VAnt_Geometry:AddRectangle(VTmp_Corner, 59.026, 80.659)
   VAnt_Rectangle_RP.Label = "RP"
--

-- STEP 25: Create new rectangular surface
   VTmp_Corner = cf.Point(31.885, 30.59, 1.6)
   VAnt_Rectangle_GPSlot_0 = VAnt_Geometry:AddRectangle(VTmp_Corner, 9.604, 3.386)
   VAnt_Rectangle_GPSlot_0.Label = "GPSlot_0"
--

-- STEP 26: Create new rectangular surface
   VTmp_Corner = cf.Point(38.099, 82.101, 1.6)
   VAnt_Rectangle_GPSlot_1 = VAnt_Geometry:AddRectangle(VTmp_Corner, 3.174, 8.152)
   VAnt_Rectangle_GPSlot_1.Label = "GPSlot_1"
--

-- STEP 27: Create new rectangular surface
   VTmp_Corner = cf.Point(55.144, 54.274, 1.6)
   VAnt_Rectangle_GPSlot_2 = VAnt_Geometry:AddRectangle(VTmp_Corner, 1.304, 1.663)
   VAnt_Rectangle_GPSlot_2.Label = "GPSlot_2"
--

-- STEP 28: Create new rectangular surface
   VTmp_Corner = cf.Point(16.681, 35.34, 1.6)
   VAnt_Rectangle_GPSlot_3 = VAnt_Geometry:AddRectangle(VTmp_Corner, 0.925, 3.821)
   VAnt_Rectangle_GPSlot_3.Label = "GPSlot_3"
--

-- STEP 29: Create new rectangular surface
   VTmp_Corner = cf.Point(58.028, 77.535, 1.6)
   VAnt_Rectangle_GPSlot_4 = VAnt_Geometry:AddRectangle(VTmp_Corner, 3.613, 4.347)
   VAnt_Rectangle_GPSlot_4.Label = "GPSlot_4"
--

-- STEP 30: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(14.464, 76.326, 1.6)
   VTmp_Points[2] = cf.Point(11.342, 82.555, 1.6)
   VTmp_Points[3] = cf.Point(10.935, 78.653, 1.6)
   VAnt_Polygon_GPSlot_5 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_5.Label = "GPSlot_5"
--

-- STEP 31: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(47.699, -10.39, 1.6)
   VTmp_Points[2] = cf.Point(50.678, 0.718, 1.6)
   VTmp_Points[3] = cf.Point(50.388, 4.765, 1.6)
   VAnt_Polygon_GPSlot_6 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_6.Label = "GPSlot_6"
--

-- STEP 32: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(24.807, 40.743, 1.6)
   VTmp_Points[2] = cf.Point(22.718, 39.82, 1.6)
   VTmp_Points[3] = cf.Point(20.719, 42.59, 1.6)
   VAnt_Polygon_GPSlot_7 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_7.Label = "GPSlot_7"
--

-- STEP 33: Create new subtraction
   VTmp_Subs = {}
   VTmp_Subs[1] = VAnt_Rectangle_GPSlot_0
   VTmp_Subs[2] = VAnt_Rectangle_GPSlot_1
   VTmp_Subs[3] = VAnt_Rectangle_GPSlot_2
   VTmp_Subs[4] = VAnt_Rectangle_GPSlot_3
   VTmp_Subs[5] = VAnt_Rectangle_GPSlot_4
   VTmp_Subs[6] = VAnt_Polygon_GPSlot_5
   VTmp_Subs[7] = VAnt_Polygon_GPSlot_6
   VTmp_Subs[8] = VAnt_Polygon_GPSlot_7
   VAnt_Subtraction_RP_Slotted = VAnt_Geometry:Subtract(VAnt_Rectangle_RP, VTmp_Subs)
   VAnt_Subtraction_RP_Slotted.Label = "RP_Slotted"
--

-- STEP 34: Create new union
   VTmp_Parts = {}
   VTmp_Parts[1] = VAnt_Subtraction_GP_Slotted
   VTmp_Parts[2] = VAnt_Subtraction_RP_Slotted
   VTmp_Parts[3] = VAnt_Cuboid_Substrate
   VTmp_Parts[4] = VAnt_Polygon_Feed_Top
   VTmp_Parts[5] = VAnt_Polygon_Feed_Pos
   VTmp_Parts[6] = VAnt_Polygon_Feed_Neg
   VTmp_Parts[7] = VAnt_Polygon_Feed_Bot
   VAnt_Union_Onion = VAnt_Geometry:Union(VTmp_Parts)
   VAnt_Union_Onion.Label = "Onion"
--

-- STEP 35: Changing face medium
   VAnt_Union_Onion.Faces:Item("Face33").Medium = VAnt_Project.Media:Item("Perfect electric conductor")
--

-- STEP 36: Changing face medium
   VAnt_Union_Onion.Faces:Item("Face34").Medium = VAnt_Project.Media:Item("Perfect electric conductor")
--

-- STEP 37: Changing face medium
   VAnt_Union_Onion.Faces:Item("Face35").Medium = VAnt_Project.Media:Item("Perfect electric conductor")
--

-- STEP 38: Create new edge port
   VTmp_Pos = {}
   VTmp_Neg = {}
   VTmp_Pos[1] = VAnt_Union_Onion.Faces:Item("Face2")
   VTmp_Neg[1] = VAnt_Union_Onion.Faces:Item("Face3")
   VAnt_EPort_SourcePort = VAnt_Project.Ports:AddEdgePort(VTmp_Pos, VTmp_Neg)
   VAnt_EPort_SourcePort.Label = "SourcePort"
--

-- STEP 39: Get config file
   VAnt_Config = VAnt_Project.SolutionConfigurations[1]
--

-- STEP 40: Create new voltage source
   VAnt_VSource_VoltageSource = VAnt_Config.Sources:AddVoltageSource(VAnt_EPort_SourcePort)
   VAnt_VSource_VoltageSource.Impedance = 50.0
   VAnt_VSource_VoltageSource.Magnitude = 1.0
   VAnt_VSource_VoltageSource.Phase = 0.0
   VAnt_VSource_VoltageSource.Label = "VoltageSource"
--

-- STEP 41: Create new Far-Field request
   VAnt_Config.FarFields:Add(0.0, 0.0, 180.0, 360.0, 5.0, 5.0)
--
-- STEP 42: Set frequency range
   VAnt_tmp = VAnt_Config.Frequency:GetProperties()
   VAnt_tmp.Start  = 906500000.0
   VAnt_tmp.End    = 933500000.0
   VAnt_tmp.RangeType  = cf.Enums.FrequencyRangeTypeEnum.LinearSpacedDiscrete
   VAnt_tmp.NumberOfDiscreteValues = 2
   VAnt_Config.Frequency:SetProperties(VAnt_tmp)
--

-- STEP 43: Mesh the project
   VAnt_Project.Mesher.Settings.WireRadius = 0.001
   VAnt_Project.Mesher.Settings.MeshSizeOption = cf.Enums.MeshSizeOptionEnum.Coarse
   VAnt_Project.Mesher:Mesh()
--

-- STEP 44: Save project
   VSes_Application:SaveAs("C:/Users/project/0. My Work/1. Repositories/1. Very Unfriendly Train/Data/Simulations/637072128687662976_Primary/637072223066233344_4/4.cfx")
--

-- STEP 45: Run simulation
   VAnt_Project.Launcher.Settings.FEKO.Parallel.Enabled = true
   VAnt_Project.Launcher:RunFEKO()
--

-- STEP 46: Close project
   VSes_Application:CloseAllWindows()
--

-- STEP 1: Make a new project
   VAnt_Project    = VSes_Application:NewProject()
   VAnt_Geometry   = VAnt_Project.Geometry
--

-- STEP 2: Set project unit of measurement
   VAnt_Project.ModelUnit  = cf.Enums.ModelUnitEnum.Millimetres
--

-- STEP 3: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(57.239000000000004, 33.675, 1.6)
   VTmp_Points[2] = cf.Point(57.239000000000004, 35.806999999999995, 1.6)
   VTmp_Points[3] = cf.Point(58.889, 35.806999999999995, 1.6)
   VTmp_Points[4] = cf.Point(58.889, 33.675, 1.6)
   VAnt_Polygon_Feed_Top = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_Feed_Top.Label = "Feed_Top"
--

-- STEP 4: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(58.889, 35.806999999999995, 1.6)
   VTmp_Points[2] = cf.Point(58.889, 35.806999999999995, 0.8)
   VTmp_Points[3] = cf.Point(58.889, 33.675, 0.8)
   VTmp_Points[4] = cf.Point(58.889, 33.675, 1.6)
   VAnt_Polygon_Feed_Pos = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_Feed_Pos.Label = "Feed_Pos"
--

-- STEP 5: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(58.889, 35.806999999999995, 0.0)
   VTmp_Points[2] = cf.Point(58.889, 35.806999999999995, 0.8)
   VTmp_Points[3] = cf.Point(58.889, 33.675, 0.8)
   VTmp_Points[4] = cf.Point(58.889, 33.675, 0.0)
   VAnt_Polygon_Feed_Neg = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_Feed_Neg.Label = "Feed_Neg"
--

-- STEP 6: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(58.889, 33.675, 0.0)
   VTmp_Points[2] = cf.Point(58.889, 35.806999999999995, 0.0)
   VTmp_Points[3] = cf.Point(57.289, 35.806999999999995, 0.0)
   VTmp_Points[4] = cf.Point(57.289, 33.675, 0.0)
   VAnt_Polygon_Feed_Bot = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_Feed_Bot.Label = "Feed_Bot"
--

-- STEP 7: Create new rectangular surface
   VTmp_Corner = cf.Point(-3.852, -1.449, 0.0)
   VAnt_Rectangle_GP = VAnt_Geometry:AddRectangle(VTmp_Corner, 61.141, 74.979)
   VAnt_Rectangle_GP.Label = "GP"
--

-- STEP 8: Create new rectangular surface
   VTmp_Corner = cf.Point(-3.7, 95.749, 0.0)
   VAnt_Rectangle_GPSlot_0 = VAnt_Geometry:AddRectangle(VTmp_Corner, 11.453, 11.369)
   VAnt_Rectangle_GPSlot_0.Label = "GPSlot_0"
--

-- STEP 9: Create new rectangular surface
   VTmp_Corner = cf.Point(13.328, 21.874, 0.0)
   VAnt_Rectangle_GPSlot_1 = VAnt_Geometry:AddRectangle(VTmp_Corner, 3.191, 28.265)
   VAnt_Rectangle_GPSlot_1.Label = "GPSlot_1"
--

-- STEP 10: Create new rectangular surface
   VTmp_Corner = cf.Point(18.342, 60.057, 0.0)
   VAnt_Rectangle_GPSlot_2 = VAnt_Geometry:AddRectangle(VTmp_Corner, 8.797, 18.259)
   VAnt_Rectangle_GPSlot_2.Label = "GPSlot_2"
--

-- STEP 11: Create new rectangular surface
   VTmp_Corner = cf.Point(40.869, 56.56, 0.0)
   VAnt_Rectangle_GPSlot_3 = VAnt_Geometry:AddRectangle(VTmp_Corner, 5.271, 11.485)
   VAnt_Rectangle_GPSlot_3.Label = "GPSlot_3"
--

-- STEP 12: Create new rectangular surface
   VTmp_Corner = cf.Point(49.204, 83.826, 0.0)
   VAnt_Rectangle_GPSlot_4 = VAnt_Geometry:AddRectangle(VTmp_Corner, 10.476, 2.697)
   VAnt_Rectangle_GPSlot_4.Label = "GPSlot_4"
--

-- STEP 13: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(86.513, 136.723, 0.0)
   VTmp_Points[2] = cf.Point(72.357, 113.743, 0.0)
   VTmp_Points[3] = cf.Point(78.69, 106.561, 0.0)
   VAnt_Polygon_GPSlot_5 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_5.Label = "GPSlot_5"
--

-- STEP 14: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(21.506, 89.19, 0.0)
   VTmp_Points[2] = cf.Point(3.884, 131.327, 0.0)
   VTmp_Points[3] = cf.Point(18.599, 90.248, 0.0)
   VAnt_Polygon_GPSlot_6 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_6.Label = "GPSlot_6"
--

-- STEP 15: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(48.633, 22.807, 0.0)
   VTmp_Points[2] = cf.Point(62.553, -17.325, 0.0)
   VTmp_Points[3] = cf.Point(73.777, -2.919, 0.0)
   VAnt_Polygon_GPSlot_7 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_7.Label = "GPSlot_7"
--

-- STEP 16: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(23.863, 107.406, 0.0)
   VTmp_Points[2] = cf.Point(52.767, 80.788, 0.0)
   VTmp_Points[3] = cf.Point(54.109, 66.074, 0.0)
   VAnt_Polygon_GPSlot_8 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_8.Label = "GPSlot_8"
--

-- STEP 17: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(47.28, 36.342, 0.0)
   VTmp_Points[2] = cf.Point(57.521, -3.497, 0.0)
   VTmp_Points[3] = cf.Point(13.875, 11.458, 0.0)
   VAnt_Polygon_GPSlot_9 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_9.Label = "GPSlot_9"
--

-- STEP 18: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(3.946, 14.209, 0.0)
   VTmp_Points[2] = cf.Point(40.537, 5.047, 0.0)
   VTmp_Points[3] = cf.Point(48.265, 21.575, 0.0)
   VAnt_Polygon_GPSlot_10 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_10.Label = "GPSlot_10"
--

-- STEP 19: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(19.236, 55.217, 0.0)
   VTmp_Points[2] = cf.Point(36.055, 83.437, 0.0)
   VTmp_Points[3] = cf.Point(21.881, 76.086, 0.0)
   VAnt_Polygon_GPSlot_11 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_11.Label = "GPSlot_11"
--

-- STEP 20: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(56.471, 30.872, 0.0)
   VTmp_Points[2] = cf.Point(62.006, 32.933, 0.0)
   VTmp_Points[3] = cf.Point(61.274, 28.579, 0.0)
   VAnt_Polygon_GPSlot_12 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_12.Label = "GPSlot_12"
--

-- STEP 21: Create new subtraction
   VTmp_Subs = {}
   VTmp_Subs[1] = VAnt_Rectangle_GPSlot_0
   VTmp_Subs[2] = VAnt_Rectangle_GPSlot_1
   VTmp_Subs[3] = VAnt_Rectangle_GPSlot_2
   VTmp_Subs[4] = VAnt_Rectangle_GPSlot_3
   VTmp_Subs[5] = VAnt_Rectangle_GPSlot_4
   VTmp_Subs[6] = VAnt_Polygon_GPSlot_5
   VTmp_Subs[7] = VAnt_Polygon_GPSlot_6
   VTmp_Subs[8] = VAnt_Polygon_GPSlot_7
   VTmp_Subs[9] = VAnt_Polygon_GPSlot_8
   VTmp_Subs[10] = VAnt_Polygon_GPSlot_9
   VTmp_Subs[11] = VAnt_Polygon_GPSlot_10
   VTmp_Subs[12] = VAnt_Polygon_GPSlot_11
   VTmp_Subs[13] = VAnt_Polygon_GPSlot_12
   VAnt_Subtraction_GP_Slotted = VAnt_Geometry:Subtract(VAnt_Rectangle_GP, VTmp_Subs)
   VAnt_Subtraction_GP_Slotted.Label = "GP_Slotted"
--

-- STEP 22: Creating medium
   VAnt_Medium_FR4 = VAnt_Project.Media:AddDielectric()
   VAnt_Medium_FR4.Label = "FR4"
   VAnt_Medium_FR4.DielectricModelling.RelativePermittivity = 4.4
   VAnt_Medium_FR4.DielectricModelling.LossTangent = 0.02
--

-- STEP 23: Create new solid.cuboid
   VTmp_Corner = cf.Point(-3.852, -2.302, 0.0)
   VAnt_Cuboid_Substrate = VAnt_Geometry:AddCuboid(VTmp_Corner, 61.141, 79.035, 1.6)
   VAnt_Cuboid_Substrate.Label = "Substrate"
--

-- STEP 24: Set solid medium
   VAnt_Cuboid_Substrate.Regions:Item(1).Medium = VAnt_Project.Media:Item("FR4")
--

-- STEP 25: Create new rectangular surface
   VTmp_Corner = cf.Point(-2.556, -2.302, 1.6)
   VAnt_Rectangle_RP = VAnt_Geometry:AddRectangle(VTmp_Corner, 59.795, 78.985)
   VAnt_Rectangle_RP.Label = "RP"
--

-- STEP 26: Create new rectangular surface
   VTmp_Corner = cf.Point(31.087, 30.909, 1.6)
   VAnt_Rectangle_GPSlot_0 = VAnt_Geometry:AddRectangle(VTmp_Corner, 9.156, 3.538)
   VAnt_Rectangle_GPSlot_0.Label = "GPSlot_0"
--

-- STEP 27: Create new rectangular surface
   VTmp_Corner = cf.Point(37.917, 55.227, 1.6)
   VAnt_Rectangle_GPSlot_1 = VAnt_Geometry:AddRectangle(VTmp_Corner, 2.531, 5.459)
   VAnt_Rectangle_GPSlot_1.Label = "GPSlot_1"
--

-- STEP 28: Create new rectangular surface
   VTmp_Corner = cf.Point(38.631, 82.092, 1.6)
   VAnt_Rectangle_GPSlot_2 = VAnt_Geometry:AddRectangle(VTmp_Corner, 3.684, 8.522)
   VAnt_Rectangle_GPSlot_2.Label = "GPSlot_2"
--

-- STEP 29: Create new rectangular surface
   VTmp_Corner = cf.Point(56.496, 54.199, 1.6)
   VAnt_Rectangle_GPSlot_3 = VAnt_Geometry:AddRectangle(VTmp_Corner, 2.264, 0.034)
   VAnt_Rectangle_GPSlot_3.Label = "GPSlot_3"
--

-- STEP 30: Create new rectangular surface
   VTmp_Corner = cf.Point(16.281, 34.413, 1.6)
   VAnt_Rectangle_GPSlot_4 = VAnt_Geometry:AddRectangle(VTmp_Corner, 1.064, 3.588)
   VAnt_Rectangle_GPSlot_4.Label = "GPSlot_4"
--

-- STEP 31: Create new rectangular surface
   VTmp_Corner = cf.Point(57.136, 77.618, 1.6)
   VAnt_Rectangle_GPSlot_5 = VAnt_Geometry:AddRectangle(VTmp_Corner, 3.642, 4.245)
   VAnt_Rectangle_GPSlot_5.Label = "GPSlot_5"
--

-- STEP 32: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(15.06, 75.444, 1.6)
   VTmp_Points[2] = cf.Point(10.302, 82.854, 1.6)
   VTmp_Points[3] = cf.Point(11.084, 78.381, 1.6)
   VAnt_Polygon_GPSlot_6 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_6.Label = "GPSlot_6"
--

-- STEP 33: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(45.715, -10.142, 1.6)
   VTmp_Points[2] = cf.Point(51.861, -0.185, 1.6)
   VTmp_Points[3] = cf.Point(50.046, 4.094, 1.6)
   VAnt_Polygon_GPSlot_7 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_7.Label = "GPSlot_7"
--

-- STEP 34: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(24.641, 40.627, 1.6)
   VTmp_Points[2] = cf.Point(21.331, 39.321, 1.6)
   VTmp_Points[3] = cf.Point(20.969, 41.915, 1.6)
   VAnt_Polygon_GPSlot_8 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_8.Label = "GPSlot_8"
--

-- STEP 35: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(56.541, 15.28, 1.6)
   VTmp_Points[2] = cf.Point(55.874, 15.352, 1.6)
   VTmp_Points[3] = cf.Point(55.086, 15.843, 1.6)
   VAnt_Polygon_GPSlot_9 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_9.Label = "GPSlot_9"
--

-- STEP 36: Create new subtraction
   VTmp_Subs = {}
   VTmp_Subs[1] = VAnt_Rectangle_GPSlot_0
   VTmp_Subs[2] = VAnt_Rectangle_GPSlot_1
   VTmp_Subs[3] = VAnt_Rectangle_GPSlot_2
   VTmp_Subs[4] = VAnt_Rectangle_GPSlot_3
   VTmp_Subs[5] = VAnt_Rectangle_GPSlot_4
   VTmp_Subs[6] = VAnt_Rectangle_GPSlot_5
   VTmp_Subs[7] = VAnt_Polygon_GPSlot_6
   VTmp_Subs[8] = VAnt_Polygon_GPSlot_7
   VTmp_Subs[9] = VAnt_Polygon_GPSlot_8
   VTmp_Subs[10] = VAnt_Polygon_GPSlot_9
   VAnt_Subtraction_RP_Slotted = VAnt_Geometry:Subtract(VAnt_Rectangle_RP, VTmp_Subs)
   VAnt_Subtraction_RP_Slotted.Label = "RP_Slotted"
--

-- STEP 37: Create new union
   VTmp_Parts = {}
   VTmp_Parts[1] = VAnt_Subtraction_GP_Slotted
   VTmp_Parts[2] = VAnt_Subtraction_RP_Slotted
   VTmp_Parts[3] = VAnt_Cuboid_Substrate
   VTmp_Parts[4] = VAnt_Polygon_Feed_Top
   VTmp_Parts[5] = VAnt_Polygon_Feed_Pos
   VTmp_Parts[6] = VAnt_Polygon_Feed_Neg
   VTmp_Parts[7] = VAnt_Polygon_Feed_Bot
   VAnt_Union_Onion = VAnt_Geometry:Union(VTmp_Parts)
   VAnt_Union_Onion.Label = "Onion"
--

-- STEP 38: Changing face medium
   VAnt_Union_Onion.Faces:Item("Face36").Medium = VAnt_Project.Media:Item("Perfect electric conductor")
--

-- STEP 39: Changing face medium
   VAnt_Union_Onion.Faces:Item("Face37").Medium = VAnt_Project.Media:Item("Perfect electric conductor")
--

-- STEP 40: Changing face medium
   VAnt_Union_Onion.Faces:Item("Face38").Medium = VAnt_Project.Media:Item("Perfect electric conductor")
--

-- STEP 41: Create new edge port
   VTmp_Pos = {}
   VTmp_Neg = {}
   VTmp_Pos[1] = VAnt_Union_Onion.Faces:Item("Face2")
   VTmp_Neg[1] = VAnt_Union_Onion.Faces:Item("Face3")
   VAnt_EPort_SourcePort = VAnt_Project.Ports:AddEdgePort(VTmp_Pos, VTmp_Neg)
   VAnt_EPort_SourcePort.Label = "SourcePort"
--

-- STEP 42: Get config file
   VAnt_Config = VAnt_Project.SolutionConfigurations[1]
--

-- STEP 43: Create new voltage source
   VAnt_VSource_VoltageSource = VAnt_Config.Sources:AddVoltageSource(VAnt_EPort_SourcePort)
   VAnt_VSource_VoltageSource.Impedance = 50.0
   VAnt_VSource_VoltageSource.Magnitude = 1.0
   VAnt_VSource_VoltageSource.Phase = 0.0
   VAnt_VSource_VoltageSource.Label = "VoltageSource"
--

-- STEP 44: Create new Far-Field request
   VAnt_Config.FarFields:Add(0.0, 0.0, 180.0, 360.0, 5.0, 5.0)
--
-- STEP 45: Set frequency range
   VAnt_tmp = VAnt_Config.Frequency:GetProperties()
   VAnt_tmp.Start  = 906500000.0
   VAnt_tmp.End    = 933500000.0
   VAnt_tmp.RangeType  = cf.Enums.FrequencyRangeTypeEnum.LinearSpacedDiscrete
   VAnt_tmp.NumberOfDiscreteValues = 2
   VAnt_Config.Frequency:SetProperties(VAnt_tmp)
--

-- STEP 46: Mesh the project
   VAnt_Project.Mesher.Settings.WireRadius = 0.001
   VAnt_Project.Mesher.Settings.MeshSizeOption = cf.Enums.MeshSizeOptionEnum.Coarse
   VAnt_Project.Mesher:Mesh()
--

-- STEP 47: Save project
   VSes_Application:SaveAs("C:/Users/project/0. My Work/1. Repositories/1. Very Unfriendly Train/Data/Simulations/637072128687662976_Primary/637072223066233344_5/5.cfx")
--

-- STEP 48: Run simulation
   VAnt_Project.Launcher.Settings.FEKO.Parallel.Enabled = true
   VAnt_Project.Launcher:RunFEKO()
--

-- STEP 49: Close project
   VSes_Application:CloseAllWindows()
--

-- STEP 1: Make a new project
   VAnt_Project    = VSes_Application:NewProject()
   VAnt_Geometry   = VAnt_Project.Geometry
--

-- STEP 2: Set project unit of measurement
   VAnt_Project.ModelUnit  = cf.Enums.ModelUnitEnum.Millimetres
--

-- STEP 3: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(57.811, 34.072500000000005, 1.6)
   VTmp_Points[2] = cf.Point(57.811, 36.21750000000001, 1.6)
   VTmp_Points[3] = cf.Point(60.405, 36.21750000000001, 1.6)
   VTmp_Points[4] = cf.Point(60.405, 34.072500000000005, 1.6)
   VAnt_Polygon_Feed_Top = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_Feed_Top.Label = "Feed_Top"
--

-- STEP 4: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(60.405, 36.21750000000001, 1.6)
   VTmp_Points[2] = cf.Point(60.405, 36.21750000000001, 0.8)
   VTmp_Points[3] = cf.Point(60.405, 34.072500000000005, 0.8)
   VTmp_Points[4] = cf.Point(60.405, 34.072500000000005, 1.6)
   VAnt_Polygon_Feed_Pos = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_Feed_Pos.Label = "Feed_Pos"
--

-- STEP 5: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(60.405, 36.21750000000001, 0.0)
   VTmp_Points[2] = cf.Point(60.405, 36.21750000000001, 0.8)
   VTmp_Points[3] = cf.Point(60.405, 34.072500000000005, 0.8)
   VTmp_Points[4] = cf.Point(60.405, 34.072500000000005, 0.0)
   VAnt_Polygon_Feed_Neg = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_Feed_Neg.Label = "Feed_Neg"
--

-- STEP 6: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(60.405, 34.072500000000005, 0.0)
   VTmp_Points[2] = cf.Point(60.405, 36.21750000000001, 0.0)
   VTmp_Points[3] = cf.Point(58.805, 36.21750000000001, 0.0)
   VTmp_Points[4] = cf.Point(58.805, 34.072500000000005, 0.0)
   VAnt_Polygon_Feed_Bot = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_Feed_Bot.Label = "Feed_Bot"
--

-- STEP 7: Create new rectangular surface
   VTmp_Corner = cf.Point(-3.995, -1.753, 0.0)
   VAnt_Rectangle_GP = VAnt_Geometry:AddRectangle(VTmp_Corner, 62.8, 73.787)
   VAnt_Rectangle_GP.Label = "GP"
--

-- STEP 8: Create new rectangular surface
   VTmp_Corner = cf.Point(-4.333, 98.409, 0.0)
   VAnt_Rectangle_GPSlot_0 = VAnt_Geometry:AddRectangle(VTmp_Corner, 11.756, 7.478)
   VAnt_Rectangle_GPSlot_0.Label = "GPSlot_0"
--

-- STEP 9: Create new rectangular surface
   VTmp_Corner = cf.Point(10.384, 23.486, 0.0)
   VAnt_Rectangle_GPSlot_1 = VAnt_Geometry:AddRectangle(VTmp_Corner, 3.389, 27.118)
   VAnt_Rectangle_GPSlot_1.Label = "GPSlot_1"
--

-- STEP 10: Create new rectangular surface
   VTmp_Corner = cf.Point(20.147, 55.365, 0.0)
   VAnt_Rectangle_GPSlot_2 = VAnt_Geometry:AddRectangle(VTmp_Corner, 11.601, 15.29)
   VAnt_Rectangle_GPSlot_2.Label = "GPSlot_2"
--

-- STEP 11: Create new rectangular surface
   VTmp_Corner = cf.Point(42.263, 56.663, 0.0)
   VAnt_Rectangle_GPSlot_3 = VAnt_Geometry:AddRectangle(VTmp_Corner, 4.539, 12.029)
   VAnt_Rectangle_GPSlot_3.Label = "GPSlot_3"
--

-- STEP 12: Create new rectangular surface
   VTmp_Corner = cf.Point(48.272, 84.139, 0.0)
   VAnt_Rectangle_GPSlot_4 = VAnt_Geometry:AddRectangle(VTmp_Corner, 8.933, 4.821)
   VAnt_Rectangle_GPSlot_4.Label = "GPSlot_4"
--

-- STEP 13: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(87.368, 135.906, 0.0)
   VTmp_Points[2] = cf.Point(75.527, 106.868, 0.0)
   VTmp_Points[3] = cf.Point(76.104, 103.634, 0.0)
   VAnt_Polygon_GPSlot_5 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_5.Label = "GPSlot_5"
--

-- STEP 14: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(22.643, 90.653, 0.0)
   VTmp_Points[2] = cf.Point(3.029, 130.996, 0.0)
   VTmp_Points[3] = cf.Point(20.098, 92.991, 0.0)
   VAnt_Polygon_GPSlot_6 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_6.Label = "GPSlot_6"
--

-- STEP 15: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(47.863, 20.817, 0.0)
   VTmp_Points[2] = cf.Point(61.255, -16.93, 0.0)
   VTmp_Points[3] = cf.Point(75.933, -0.039, 0.0)
   VAnt_Polygon_GPSlot_7 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_7.Label = "GPSlot_7"
--

-- STEP 16: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(22.195, 107.647, 0.0)
   VTmp_Points[2] = cf.Point(51.003, 79.362, 0.0)
   VTmp_Points[3] = cf.Point(54.778, 67.216, 0.0)
   VAnt_Polygon_GPSlot_8 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_8.Label = "GPSlot_8"
--

-- STEP 17: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(41.881, 37.349, 0.0)
   VTmp_Points[2] = cf.Point(62.196, -5.716, 0.0)
   VTmp_Points[3] = cf.Point(16.118, 12.907, 0.0)
   VAnt_Polygon_GPSlot_9 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_9.Label = "GPSlot_9"
--

-- STEP 18: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(2.978, 14.76, 0.0)
   VTmp_Points[2] = cf.Point(42.82, 8.022, 0.0)
   VTmp_Points[3] = cf.Point(51.086, 19.891, 0.0)
   VAnt_Polygon_GPSlot_10 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_10.Label = "GPSlot_10"
--

-- STEP 19: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(21.599, 58.401, 0.0)
   VTmp_Points[2] = cf.Point(39.518, 80.355, 0.0)
   VTmp_Points[3] = cf.Point(23.502, 77.342, 0.0)
   VAnt_Polygon_GPSlot_11 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_11.Label = "GPSlot_11"
--

-- STEP 20: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(67.965, 10.783, 0.0)
   VTmp_Points[2] = cf.Point(69.678, 7.024, 0.0)
   VTmp_Points[3] = cf.Point(68.504, 6.204, 0.0)
   VAnt_Polygon_GPSlot_12 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_12.Label = "GPSlot_12"
--

-- STEP 21: Create new subtraction
   VTmp_Subs = {}
   VTmp_Subs[1] = VAnt_Rectangle_GPSlot_0
   VTmp_Subs[2] = VAnt_Rectangle_GPSlot_1
   VTmp_Subs[3] = VAnt_Rectangle_GPSlot_2
   VTmp_Subs[4] = VAnt_Rectangle_GPSlot_3
   VTmp_Subs[5] = VAnt_Rectangle_GPSlot_4
   VTmp_Subs[6] = VAnt_Polygon_GPSlot_5
   VTmp_Subs[7] = VAnt_Polygon_GPSlot_6
   VTmp_Subs[8] = VAnt_Polygon_GPSlot_7
   VTmp_Subs[9] = VAnt_Polygon_GPSlot_8
   VTmp_Subs[10] = VAnt_Polygon_GPSlot_9
   VTmp_Subs[11] = VAnt_Polygon_GPSlot_10
   VTmp_Subs[12] = VAnt_Polygon_GPSlot_11
   VTmp_Subs[13] = VAnt_Polygon_GPSlot_12
   VAnt_Subtraction_GP_Slotted = VAnt_Geometry:Subtract(VAnt_Rectangle_GP, VTmp_Subs)
   VAnt_Subtraction_GP_Slotted.Label = "GP_Slotted"
--

-- STEP 22: Creating medium
   VAnt_Medium_FR4 = VAnt_Project.Media:AddDielectric()
   VAnt_Medium_FR4.Label = "FR4"
   VAnt_Medium_FR4.DielectricModelling.RelativePermittivity = 4.4
   VAnt_Medium_FR4.DielectricModelling.LossTangent = 0.02
--

-- STEP 23: Create new solid.cuboid
   VTmp_Corner = cf.Point(-3.995, -2.901, 0.0)
   VAnt_Cuboid_Substrate = VAnt_Geometry:AddCuboid(VTmp_Corner, 62.8, 79.618, 1.6)
   VAnt_Cuboid_Substrate.Label = "Substrate"
--

-- STEP 24: Set solid medium
   VAnt_Cuboid_Substrate.Regions:Item(1).Medium = VAnt_Project.Media:Item("FR4")
--

-- STEP 25: Create new rectangular surface
   VTmp_Corner = cf.Point(-2.606, -2.901, 1.6)
   VAnt_Rectangle_RP = VAnt_Geometry:AddRectangle(VTmp_Corner, 60.417, 79.568)
   VAnt_Rectangle_RP.Label = "RP"
--

-- STEP 26: Create new rectangular surface
   VTmp_Corner = cf.Point(30.788, 31.026, 1.6)
   VAnt_Rectangle_GPSlot_0 = VAnt_Geometry:AddRectangle(VTmp_Corner, 8.961, 3.208)
   VAnt_Rectangle_GPSlot_0.Label = "GPSlot_0"
--

-- STEP 27: Create new rectangular surface
   VTmp_Corner = cf.Point(36.772, 55.59, 1.6)
   VAnt_Rectangle_GPSlot_1 = VAnt_Geometry:AddRectangle(VTmp_Corner, 2.645, 5.616)
   VAnt_Rectangle_GPSlot_1.Label = "GPSlot_1"
--

-- STEP 28: Create new rectangular surface
   VTmp_Corner = cf.Point(38.242, 81.95, 1.6)
   VAnt_Rectangle_GPSlot_2 = VAnt_Geometry:AddRectangle(VTmp_Corner, 2.625, 8.477)
   VAnt_Rectangle_GPSlot_2.Label = "GPSlot_2"
--

-- STEP 29: Create new rectangular surface
   VTmp_Corner = cf.Point(55.826, 53.396, 1.6)
   VAnt_Rectangle_GPSlot_3 = VAnt_Geometry:AddRectangle(VTmp_Corner, 3.049, 1.366)
   VAnt_Rectangle_GPSlot_3.Label = "GPSlot_3"
--

-- STEP 30: Create new rectangular surface
   VTmp_Corner = cf.Point(14.827, 36.414, 1.6)
   VAnt_Rectangle_GPSlot_4 = VAnt_Geometry:AddRectangle(VTmp_Corner, 1.087, 3.15)
   VAnt_Rectangle_GPSlot_4.Label = "GPSlot_4"
--

-- STEP 31: Create new rectangular surface
   VTmp_Corner = cf.Point(57.941, 76.369, 1.6)
   VAnt_Rectangle_GPSlot_5 = VAnt_Geometry:AddRectangle(VTmp_Corner, 3.965, 4.289)
   VAnt_Rectangle_GPSlot_5.Label = "GPSlot_5"
--

-- STEP 32: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(14.222, 75.912, 1.6)
   VTmp_Points[2] = cf.Point(10.551, 82.767, 1.6)
   VTmp_Points[3] = cf.Point(12.183, 78.677, 1.6)
   VAnt_Polygon_GPSlot_6 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_6.Label = "GPSlot_6"
--

-- STEP 33: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(47.16, -9.758, 1.6)
   VTmp_Points[2] = cf.Point(49.657, 0.87, 1.6)
   VTmp_Points[3] = cf.Point(50.861, 3.379, 1.6)
   VAnt_Polygon_GPSlot_7 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_7.Label = "GPSlot_7"
--

-- STEP 34: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(24.674, 40.613, 1.6)
   VTmp_Points[2] = cf.Point(22.289, 39.811, 1.6)
   VTmp_Points[3] = cf.Point(20.866, 42.332, 1.6)
   VAnt_Polygon_GPSlot_8 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_8.Label = "GPSlot_8"
--

-- STEP 35: Create new subtraction
   VTmp_Subs = {}
   VTmp_Subs[1] = VAnt_Rectangle_GPSlot_0
   VTmp_Subs[2] = VAnt_Rectangle_GPSlot_1
   VTmp_Subs[3] = VAnt_Rectangle_GPSlot_2
   VTmp_Subs[4] = VAnt_Rectangle_GPSlot_3
   VTmp_Subs[5] = VAnt_Rectangle_GPSlot_4
   VTmp_Subs[6] = VAnt_Rectangle_GPSlot_5
   VTmp_Subs[7] = VAnt_Polygon_GPSlot_6
   VTmp_Subs[8] = VAnt_Polygon_GPSlot_7
   VTmp_Subs[9] = VAnt_Polygon_GPSlot_8
   VAnt_Subtraction_RP_Slotted = VAnt_Geometry:Subtract(VAnt_Rectangle_RP, VTmp_Subs)
   VAnt_Subtraction_RP_Slotted.Label = "RP_Slotted"
--

-- STEP 36: Create new union
   VTmp_Parts = {}
   VTmp_Parts[1] = VAnt_Subtraction_GP_Slotted
   VTmp_Parts[2] = VAnt_Subtraction_RP_Slotted
   VTmp_Parts[3] = VAnt_Cuboid_Substrate
   VTmp_Parts[4] = VAnt_Polygon_Feed_Top
   VTmp_Parts[5] = VAnt_Polygon_Feed_Pos
   VTmp_Parts[6] = VAnt_Polygon_Feed_Neg
   VTmp_Parts[7] = VAnt_Polygon_Feed_Bot
   VAnt_Union_Onion = VAnt_Geometry:Union(VTmp_Parts)
   VAnt_Union_Onion.Label = "Onion"
--

-- STEP 37: Changing face medium
   VAnt_Union_Onion.Faces:Item("Face35").Medium = VAnt_Project.Media:Item("Perfect electric conductor")
--

-- STEP 38: Changing face medium
   VAnt_Union_Onion.Faces:Item("Face36").Medium = VAnt_Project.Media:Item("Perfect electric conductor")
--

-- STEP 39: Changing face medium
   VAnt_Union_Onion.Faces:Item("Face37").Medium = VAnt_Project.Media:Item("Perfect electric conductor")
--

-- STEP 40: Create new edge port
   VTmp_Pos = {}
   VTmp_Neg = {}
   VTmp_Pos[1] = VAnt_Union_Onion.Faces:Item("Face2")
   VTmp_Neg[1] = VAnt_Union_Onion.Faces:Item("Face3")
   VAnt_EPort_SourcePort = VAnt_Project.Ports:AddEdgePort(VTmp_Pos, VTmp_Neg)
   VAnt_EPort_SourcePort.Label = "SourcePort"
--

-- STEP 41: Get config file
   VAnt_Config = VAnt_Project.SolutionConfigurations[1]
--

-- STEP 42: Create new voltage source
   VAnt_VSource_VoltageSource = VAnt_Config.Sources:AddVoltageSource(VAnt_EPort_SourcePort)
   VAnt_VSource_VoltageSource.Impedance = 50.0
   VAnt_VSource_VoltageSource.Magnitude = 1.0
   VAnt_VSource_VoltageSource.Phase = 0.0
   VAnt_VSource_VoltageSource.Label = "VoltageSource"
--

-- STEP 43: Create new Far-Field request
   VAnt_Config.FarFields:Add(0.0, 0.0, 180.0, 360.0, 5.0, 5.0)
--
-- STEP 44: Set frequency range
   VAnt_tmp = VAnt_Config.Frequency:GetProperties()
   VAnt_tmp.Start  = 906500000.0
   VAnt_tmp.End    = 933500000.0
   VAnt_tmp.RangeType  = cf.Enums.FrequencyRangeTypeEnum.LinearSpacedDiscrete
   VAnt_tmp.NumberOfDiscreteValues = 2
   VAnt_Config.Frequency:SetProperties(VAnt_tmp)
--

-- STEP 45: Mesh the project
   VAnt_Project.Mesher.Settings.WireRadius = 0.001
   VAnt_Project.Mesher.Settings.MeshSizeOption = cf.Enums.MeshSizeOptionEnum.Coarse
   VAnt_Project.Mesher:Mesh()
--

-- STEP 46: Save project
   VSes_Application:SaveAs("C:/Users/project/0. My Work/1. Repositories/1. Very Unfriendly Train/Data/Simulations/637072128687662976_Primary/637072223066233344_6/6.cfx")
--

-- STEP 47: Run simulation
   VAnt_Project.Launcher.Settings.FEKO.Parallel.Enabled = true
   VAnt_Project.Launcher:RunFEKO()
--

-- STEP 48: Close project
   VSes_Application:CloseAllWindows()
--

-- STEP 1: Make a new project
   VAnt_Project    = VSes_Application:NewProject()
   VAnt_Geometry   = VAnt_Project.Geometry
--

-- STEP 2: Set project unit of measurement
   VAnt_Project.ModelUnit  = cf.Enums.ModelUnitEnum.Millimetres
--

-- STEP 3: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(55.882, 34.275, 1.6)
   VTmp_Points[2] = cf.Point(55.882, 36.435, 1.6)
   VTmp_Points[3] = cf.Point(57.532, 36.435, 1.6)
   VTmp_Points[4] = cf.Point(57.532, 34.275, 1.6)
   VAnt_Polygon_Feed_Top = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_Feed_Top.Label = "Feed_Top"
--

-- STEP 4: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(57.532, 36.435, 1.6)
   VTmp_Points[2] = cf.Point(57.532, 36.435, 0.8)
   VTmp_Points[3] = cf.Point(57.532, 34.275, 0.8)
   VTmp_Points[4] = cf.Point(57.532, 34.275, 1.6)
   VAnt_Polygon_Feed_Pos = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_Feed_Pos.Label = "Feed_Pos"
--

-- STEP 5: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(57.532, 36.435, 0.0)
   VTmp_Points[2] = cf.Point(57.532, 36.435, 0.8)
   VTmp_Points[3] = cf.Point(57.532, 34.275, 0.8)
   VTmp_Points[4] = cf.Point(57.532, 34.275, 0.0)
   VAnt_Polygon_Feed_Neg = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_Feed_Neg.Label = "Feed_Neg"
--

-- STEP 6: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(57.532, 34.275, 0.0)
   VTmp_Points[2] = cf.Point(57.532, 36.435, 0.0)
   VTmp_Points[3] = cf.Point(55.931999999999995, 36.435, 0.0)
   VTmp_Points[4] = cf.Point(55.931999999999995, 34.275, 0.0)
   VAnt_Polygon_Feed_Bot = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_Feed_Bot.Label = "Feed_Bot"
--

-- STEP 7: Create new rectangular surface
   VTmp_Corner = cf.Point(-4.025, -1.934, 0.0)
   VAnt_Rectangle_GP = VAnt_Geometry:AddRectangle(VTmp_Corner, 59.956999999999994, 75.203)
   VAnt_Rectangle_GP.Label = "GP"
--

-- STEP 8: Create new rectangular surface
   VTmp_Corner = cf.Point(-5.504, 100.848, 0.0)
   VAnt_Rectangle_GPSlot_0 = VAnt_Geometry:AddRectangle(VTmp_Corner, 7.009, 9.907)
   VAnt_Rectangle_GPSlot_0.Label = "GPSlot_0"
--

-- STEP 9: Create new rectangular surface
   VTmp_Corner = cf.Point(12.551, 22.009, 0.0)
   VAnt_Rectangle_GPSlot_1 = VAnt_Geometry:AddRectangle(VTmp_Corner, 6.081, 24.114)
   VAnt_Rectangle_GPSlot_1.Label = "GPSlot_1"
--

-- STEP 10: Create new rectangular surface
   VTmp_Corner = cf.Point(19.314, 57.389, 0.0)
   VAnt_Rectangle_GPSlot_2 = VAnt_Geometry:AddRectangle(VTmp_Corner, 12.034, 20.764)
   VAnt_Rectangle_GPSlot_2.Label = "GPSlot_2"
--

-- STEP 11: Create new rectangular surface
   VTmp_Corner = cf.Point(42.394, 55.43, 0.0)
   VAnt_Rectangle_GPSlot_3 = VAnt_Geometry:AddRectangle(VTmp_Corner, 4.173, 11.248)
   VAnt_Rectangle_GPSlot_3.Label = "GPSlot_3"
--

-- STEP 12: Create new rectangular surface
   VTmp_Corner = cf.Point(48.684, 82.764, 0.0)
   VAnt_Rectangle_GPSlot_4 = VAnt_Geometry:AddRectangle(VTmp_Corner, 11.835, 2.059)
   VAnt_Rectangle_GPSlot_4.Label = "GPSlot_4"
--

-- STEP 13: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(87.69, 131.496, 0.0)
   VTmp_Points[2] = cf.Point(71.955, 111.552, 0.0)
   VTmp_Points[3] = cf.Point(76.007, 104.749, 0.0)
   VAnt_Polygon_GPSlot_5 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_5.Label = "GPSlot_5"
--

-- STEP 14: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(25.226, 87.42, 0.0)
   VTmp_Points[2] = cf.Point(2.604, 132.211, 0.0)
   VTmp_Points[3] = cf.Point(19.751, 93.848, 0.0)
   VAnt_Polygon_GPSlot_6 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_6.Label = "GPSlot_6"
--

-- STEP 15: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(46.124, 17.61, 0.0)
   VTmp_Points[2] = cf.Point(59.359, -16.651, 0.0)
   VTmp_Points[3] = cf.Point(73.935, -0.664, 0.0)
   VAnt_Polygon_GPSlot_7 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_7.Label = "GPSlot_7"
--

-- STEP 16: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(22.601, 111.906, 0.0)
   VTmp_Points[2] = cf.Point(52.53, 80.678, 0.0)
   VTmp_Points[3] = cf.Point(55.786, 65.603, 0.0)
   VAnt_Polygon_GPSlot_8 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_8.Label = "GPSlot_8"
--

-- STEP 17: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(43.659, 36.104, 0.0)
   VTmp_Points[2] = cf.Point(56.802, -1.669, 0.0)
   VTmp_Points[3] = cf.Point(16.065, 14.861, 0.0)
   VAnt_Polygon_GPSlot_9 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_9.Label = "GPSlot_9"
--

-- STEP 18: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(4.465, 12.138, 0.0)
   VTmp_Points[2] = cf.Point(43.496, 4.563, 0.0)
   VTmp_Points[3] = cf.Point(47.785, 22.43, 0.0)
   VAnt_Polygon_GPSlot_10 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_10.Label = "GPSlot_10"
--

-- STEP 19: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(19.069, 55.69, 0.0)
   VTmp_Points[2] = cf.Point(38.164, 79.437, 0.0)
   VTmp_Points[3] = cf.Point(21.573, 73.082, 0.0)
   VAnt_Polygon_GPSlot_11 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_11.Label = "GPSlot_11"
--

-- STEP 20: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(27.593, 29.232, 0.0)
   VTmp_Points[2] = cf.Point(25.636, 17.443, 0.0)
   VTmp_Points[3] = cf.Point(19.267, 17.771, 0.0)
   VAnt_Polygon_GPSlot_12 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_12.Label = "GPSlot_12"
--

-- STEP 21: Create new subtraction
   VTmp_Subs = {}
   VTmp_Subs[1] = VAnt_Rectangle_GPSlot_0
   VTmp_Subs[2] = VAnt_Rectangle_GPSlot_1
   VTmp_Subs[3] = VAnt_Rectangle_GPSlot_2
   VTmp_Subs[4] = VAnt_Rectangle_GPSlot_3
   VTmp_Subs[5] = VAnt_Rectangle_GPSlot_4
   VTmp_Subs[6] = VAnt_Polygon_GPSlot_5
   VTmp_Subs[7] = VAnt_Polygon_GPSlot_6
   VTmp_Subs[8] = VAnt_Polygon_GPSlot_7
   VTmp_Subs[9] = VAnt_Polygon_GPSlot_8
   VTmp_Subs[10] = VAnt_Polygon_GPSlot_9
   VTmp_Subs[11] = VAnt_Polygon_GPSlot_10
   VTmp_Subs[12] = VAnt_Polygon_GPSlot_11
   VTmp_Subs[13] = VAnt_Polygon_GPSlot_12
   VAnt_Subtraction_GP_Slotted = VAnt_Geometry:Subtract(VAnt_Rectangle_GP, VTmp_Subs)
   VAnt_Subtraction_GP_Slotted.Label = "GP_Slotted"
--

-- STEP 22: Creating medium
   VAnt_Medium_FR4 = VAnt_Project.Media:AddDielectric()
   VAnt_Medium_FR4.Label = "FR4"
   VAnt_Medium_FR4.DielectricModelling.RelativePermittivity = 4.4
   VAnt_Medium_FR4.DielectricModelling.LossTangent = 0.02
--

-- STEP 23: Create new solid.cuboid
   VTmp_Corner = cf.Point(-4.025, -3.145, 0.0)
   VAnt_Cuboid_Substrate = VAnt_Geometry:AddCuboid(VTmp_Corner, 59.956999999999994, 79.8, 1.6)
   VAnt_Cuboid_Substrate.Label = "Substrate"
--

-- STEP 24: Set solid medium
   VAnt_Cuboid_Substrate.Regions:Item(1).Medium = VAnt_Project.Media:Item("FR4")
--

-- STEP 25: Create new rectangular surface
   VTmp_Corner = cf.Point(-2.525, -3.145, 1.6)
   VAnt_Rectangle_RP = VAnt_Geometry:AddRectangle(VTmp_Corner, 58.407, 79.75)
   VAnt_Rectangle_RP.Label = "RP"
--

-- STEP 26: Create new rectangular surface
   VTmp_Corner = cf.Point(31.601, 31.349, 1.6)
   VAnt_Rectangle_GPSlot_0 = VAnt_Geometry:AddRectangle(VTmp_Corner, 9.35, 3.867)
   VAnt_Rectangle_GPSlot_0.Label = "GPSlot_0"
--

-- STEP 27: Create new rectangular surface
   VTmp_Corner = cf.Point(37.447, 56.122, 1.6)
   VAnt_Rectangle_GPSlot_1 = VAnt_Geometry:AddRectangle(VTmp_Corner, 2.393, 5.98)
   VAnt_Rectangle_GPSlot_1.Label = "GPSlot_1"
--

-- STEP 28: Create new rectangular surface
   VTmp_Corner = cf.Point(38.117, 81.329, 1.6)
   VAnt_Rectangle_GPSlot_2 = VAnt_Geometry:AddRectangle(VTmp_Corner, 2.557, 9.088)
   VAnt_Rectangle_GPSlot_2.Label = "GPSlot_2"
--

-- STEP 29: Create new rectangular surface
   VTmp_Corner = cf.Point(55.44, 54.105, 1.6)
   VAnt_Rectangle_GPSlot_3 = VAnt_Geometry:AddRectangle(VTmp_Corner, 1.796, 0.843)
   VAnt_Rectangle_GPSlot_3.Label = "GPSlot_3"
--

-- STEP 30: Create new rectangular surface
   VTmp_Corner = cf.Point(16.61, 35.217, 1.6)
   VAnt_Rectangle_GPSlot_4 = VAnt_Geometry:AddRectangle(VTmp_Corner, 0.47, 3.81)
   VAnt_Rectangle_GPSlot_4.Label = "GPSlot_4"
--

-- STEP 31: Create new rectangular surface
   VTmp_Corner = cf.Point(58.521, 76.669, 1.6)
   VAnt_Rectangle_GPSlot_5 = VAnt_Geometry:AddRectangle(VTmp_Corner, 3.585, 5.202)
   VAnt_Rectangle_GPSlot_5.Label = "GPSlot_5"
--

-- STEP 32: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(12.99, 74.569, 1.6)
   VTmp_Points[2] = cf.Point(10.769, 84.289, 1.6)
   VTmp_Points[3] = cf.Point(12.185, 79.231, 1.6)
   VAnt_Polygon_GPSlot_6 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_6.Label = "GPSlot_6"
--

-- STEP 33: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(46.128, -9.373, 1.6)
   VTmp_Points[2] = cf.Point(49.777, 0.733, 1.6)
   VTmp_Points[3] = cf.Point(52.015, 4.302, 1.6)
   VAnt_Polygon_GPSlot_7 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_7.Label = "GPSlot_7"
--

-- STEP 34: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(24.531, 40.369, 1.6)
   VTmp_Points[2] = cf.Point(22.841, 40.221, 1.6)
   VTmp_Points[3] = cf.Point(21.254, 41.681, 1.6)
   VAnt_Polygon_GPSlot_8 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_8.Label = "GPSlot_8"
--

-- STEP 35: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(55.133, 40.946, 1.6)
   VTmp_Points[2] = cf.Point(54.482, 40.815, 1.6)
   VTmp_Points[3] = cf.Point(54.14, 41.167, 1.6)
   VAnt_Polygon_GPSlot_9 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_9.Label = "GPSlot_9"
--

-- STEP 36: Create new subtraction
   VTmp_Subs = {}
   VTmp_Subs[1] = VAnt_Rectangle_GPSlot_0
   VTmp_Subs[2] = VAnt_Rectangle_GPSlot_1
   VTmp_Subs[3] = VAnt_Rectangle_GPSlot_2
   VTmp_Subs[4] = VAnt_Rectangle_GPSlot_3
   VTmp_Subs[5] = VAnt_Rectangle_GPSlot_4
   VTmp_Subs[6] = VAnt_Rectangle_GPSlot_5
   VTmp_Subs[7] = VAnt_Polygon_GPSlot_6
   VTmp_Subs[8] = VAnt_Polygon_GPSlot_7
   VTmp_Subs[9] = VAnt_Polygon_GPSlot_8
   VTmp_Subs[10] = VAnt_Polygon_GPSlot_9
   VAnt_Subtraction_RP_Slotted = VAnt_Geometry:Subtract(VAnt_Rectangle_RP, VTmp_Subs)
   VAnt_Subtraction_RP_Slotted.Label = "RP_Slotted"
--

-- STEP 37: Create new union
   VTmp_Parts = {}
   VTmp_Parts[1] = VAnt_Subtraction_GP_Slotted
   VTmp_Parts[2] = VAnt_Subtraction_RP_Slotted
   VTmp_Parts[3] = VAnt_Cuboid_Substrate
   VTmp_Parts[4] = VAnt_Polygon_Feed_Top
   VTmp_Parts[5] = VAnt_Polygon_Feed_Pos
   VTmp_Parts[6] = VAnt_Polygon_Feed_Neg
   VTmp_Parts[7] = VAnt_Polygon_Feed_Bot
   VAnt_Union_Onion = VAnt_Geometry:Union(VTmp_Parts)
   VAnt_Union_Onion.Label = "Onion"
--

-- STEP 38: Changing face medium
   VAnt_Union_Onion.Faces:Item("Face36").Medium = VAnt_Project.Media:Item("Perfect electric conductor")
--

-- STEP 39: Changing face medium
   VAnt_Union_Onion.Faces:Item("Face37").Medium = VAnt_Project.Media:Item("Perfect electric conductor")
--

-- STEP 40: Changing face medium
   VAnt_Union_Onion.Faces:Item("Face38").Medium = VAnt_Project.Media:Item("Perfect electric conductor")
--

-- STEP 41: Create new edge port
   VTmp_Pos = {}
   VTmp_Neg = {}
   VTmp_Pos[1] = VAnt_Union_Onion.Faces:Item("Face2")
   VTmp_Neg[1] = VAnt_Union_Onion.Faces:Item("Face3")
   VAnt_EPort_SourcePort = VAnt_Project.Ports:AddEdgePort(VTmp_Pos, VTmp_Neg)
   VAnt_EPort_SourcePort.Label = "SourcePort"
--

-- STEP 42: Get config file
   VAnt_Config = VAnt_Project.SolutionConfigurations[1]
--

-- STEP 43: Create new voltage source
   VAnt_VSource_VoltageSource = VAnt_Config.Sources:AddVoltageSource(VAnt_EPort_SourcePort)
   VAnt_VSource_VoltageSource.Impedance = 50.0
   VAnt_VSource_VoltageSource.Magnitude = 1.0
   VAnt_VSource_VoltageSource.Phase = 0.0
   VAnt_VSource_VoltageSource.Label = "VoltageSource"
--

-- STEP 44: Create new Far-Field request
   VAnt_Config.FarFields:Add(0.0, 0.0, 180.0, 360.0, 5.0, 5.0)
--
-- STEP 45: Set frequency range
   VAnt_tmp = VAnt_Config.Frequency:GetProperties()
   VAnt_tmp.Start  = 906500000.0
   VAnt_tmp.End    = 933500000.0
   VAnt_tmp.RangeType  = cf.Enums.FrequencyRangeTypeEnum.LinearSpacedDiscrete
   VAnt_tmp.NumberOfDiscreteValues = 2
   VAnt_Config.Frequency:SetProperties(VAnt_tmp)
--

-- STEP 46: Mesh the project
   VAnt_Project.Mesher.Settings.WireRadius = 0.001
   VAnt_Project.Mesher.Settings.MeshSizeOption = cf.Enums.MeshSizeOptionEnum.Coarse
   VAnt_Project.Mesher:Mesh()
--

-- STEP 47: Save project
   VSes_Application:SaveAs("C:/Users/project/0. My Work/1. Repositories/1. Very Unfriendly Train/Data/Simulations/637072128687662976_Primary/637072223066233344_7/7.cfx")
--

-- STEP 48: Run simulation
   VAnt_Project.Launcher.Settings.FEKO.Parallel.Enabled = true
   VAnt_Project.Launcher:RunFEKO()
--

-- STEP 49: Close project
   VSes_Application:CloseAllWindows()
--

-- STEP 1: Make a new project
   VAnt_Project    = VSes_Application:NewProject()
   VAnt_Geometry   = VAnt_Project.Geometry
--

-- STEP 2: Set project unit of measurement
   VAnt_Project.ModelUnit  = cf.Enums.ModelUnitEnum.Millimetres
--

-- STEP 3: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(57.292, 33.3965, 1.6)
   VTmp_Points[2] = cf.Point(57.292, 35.541500000000006, 1.6)
   VTmp_Points[3] = cf.Point(58.942, 35.541500000000006, 1.6)
   VTmp_Points[4] = cf.Point(58.942, 33.3965, 1.6)
   VAnt_Polygon_Feed_Top = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_Feed_Top.Label = "Feed_Top"
--

-- STEP 4: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(58.942, 35.541500000000006, 1.6)
   VTmp_Points[2] = cf.Point(58.942, 35.541500000000006, 0.8)
   VTmp_Points[3] = cf.Point(58.942, 33.3965, 0.8)
   VTmp_Points[4] = cf.Point(58.942, 33.3965, 1.6)
   VAnt_Polygon_Feed_Pos = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_Feed_Pos.Label = "Feed_Pos"
--

-- STEP 5: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(58.942, 35.541500000000006, 0.0)
   VTmp_Points[2] = cf.Point(58.942, 35.541500000000006, 0.8)
   VTmp_Points[3] = cf.Point(58.942, 33.3965, 0.8)
   VTmp_Points[4] = cf.Point(58.942, 33.3965, 0.0)
   VAnt_Polygon_Feed_Neg = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_Feed_Neg.Label = "Feed_Neg"
--

-- STEP 6: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(58.942, 33.3965, 0.0)
   VTmp_Points[2] = cf.Point(58.942, 35.541500000000006, 0.0)
   VTmp_Points[3] = cf.Point(57.342, 35.541500000000006, 0.0)
   VTmp_Points[4] = cf.Point(57.342, 33.3965, 0.0)
   VAnt_Polygon_Feed_Bot = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_Feed_Bot.Label = "Feed_Bot"
--

-- STEP 7: Create new rectangular surface
   VTmp_Corner = cf.Point(-4.17, -1.571, 0.0)
   VAnt_Rectangle_GP = VAnt_Geometry:AddRectangle(VTmp_Corner, 61.512, 77.579)
   VAnt_Rectangle_GP.Label = "GP"
--

-- STEP 8: Create new rectangular surface
   VTmp_Corner = cf.Point(-3.024, 99.974, 0.0)
   VAnt_Rectangle_GPSlot_0 = VAnt_Geometry:AddRectangle(VTmp_Corner, 6.51, 7.959)
   VAnt_Rectangle_GPSlot_0.Label = "GPSlot_0"
--

-- STEP 9: Create new rectangular surface
   VTmp_Corner = cf.Point(11.288, 21.662, 0.0)
   VAnt_Rectangle_GPSlot_1 = VAnt_Geometry:AddRectangle(VTmp_Corner, 1.912, 23.117)
   VAnt_Rectangle_GPSlot_1.Label = "GPSlot_1"
--

-- STEP 10: Create new rectangular surface
   VTmp_Corner = cf.Point(18.337, 57.004, 0.0)
   VAnt_Rectangle_GPSlot_2 = VAnt_Geometry:AddRectangle(VTmp_Corner, 11.696, 19.475)
   VAnt_Rectangle_GPSlot_2.Label = "GPSlot_2"
--

-- STEP 11: Create new rectangular surface
   VTmp_Corner = cf.Point(38.409, 56.03, 0.0)
   VAnt_Rectangle_GPSlot_3 = VAnt_Geometry:AddRectangle(VTmp_Corner, 2.938, 11.967)
   VAnt_Rectangle_GPSlot_3.Label = "GPSlot_3"
--

-- STEP 12: Create new rectangular surface
   VTmp_Corner = cf.Point(47.859, 85.009, 0.0)
   VAnt_Rectangle_GPSlot_4 = VAnt_Geometry:AddRectangle(VTmp_Corner, 11.344, 2.042)
   VAnt_Rectangle_GPSlot_4.Label = "GPSlot_4"
--

-- STEP 13: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(84.379, 132.65, 0.0)
   VTmp_Points[2] = cf.Point(75.12, 107.65, 0.0)
   VTmp_Points[3] = cf.Point(79.538, 106.374, 0.0)
   VAnt_Polygon_GPSlot_5 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_5.Label = "GPSlot_5"
--

-- STEP 14: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(23.013, 89.47, 0.0)
   VTmp_Points[2] = cf.Point(1.463, 132.853, 0.0)
   VTmp_Points[3] = cf.Point(21.384, 92.599, 0.0)
   VAnt_Polygon_GPSlot_6 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_6.Label = "GPSlot_6"
--

-- STEP 15: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(50.011, 23.774, 0.0)
   VTmp_Points[2] = cf.Point(62.793, -18.333, 0.0)
   VTmp_Points[3] = cf.Point(73.254, 0.993, 0.0)
   VAnt_Polygon_GPSlot_7 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_7.Label = "GPSlot_7"
--

-- STEP 16: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(20.333, 107.987, 0.0)
   VTmp_Points[2] = cf.Point(52.537, 76.808, 0.0)
   VTmp_Points[3] = cf.Point(53.633, 67.717, 0.0)
   VAnt_Polygon_GPSlot_8 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_8.Label = "GPSlot_8"
--

-- STEP 17: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(44.112, 36.468, 0.0)
   VTmp_Points[2] = cf.Point(56.192, -3.744, 0.0)
   VTmp_Points[3] = cf.Point(12.363, 11.867, 0.0)
   VAnt_Polygon_GPSlot_9 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_9.Label = "GPSlot_9"
--

-- STEP 18: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(5.323, 11.159, 0.0)
   VTmp_Points[2] = cf.Point(43.782, 6.901, 0.0)
   VTmp_Points[3] = cf.Point(50.347, 18.208, 0.0)
   VAnt_Polygon_GPSlot_10 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_10.Label = "GPSlot_10"
--

-- STEP 19: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(18.805, 56.567, 0.0)
   VTmp_Points[2] = cf.Point(33.042, 79.227, 0.0)
   VTmp_Points[3] = cf.Point(25.012, 77.869, 0.0)
   VAnt_Polygon_GPSlot_11 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_11.Label = "GPSlot_11"
--

-- STEP 20: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(11.012, 73.9, 0.0)
   VTmp_Points[2] = cf.Point(15.019, 59.681, 0.0)
   VTmp_Points[3] = cf.Point(6.426, 70.796, 0.0)
   VAnt_Polygon_GPSlot_12 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_12.Label = "GPSlot_12"
--

-- STEP 21: Create new subtraction
   VTmp_Subs = {}
   VTmp_Subs[1] = VAnt_Rectangle_GPSlot_0
   VTmp_Subs[2] = VAnt_Rectangle_GPSlot_1
   VTmp_Subs[3] = VAnt_Rectangle_GPSlot_2
   VTmp_Subs[4] = VAnt_Rectangle_GPSlot_3
   VTmp_Subs[5] = VAnt_Rectangle_GPSlot_4
   VTmp_Subs[6] = VAnt_Polygon_GPSlot_5
   VTmp_Subs[7] = VAnt_Polygon_GPSlot_6
   VTmp_Subs[8] = VAnt_Polygon_GPSlot_7
   VTmp_Subs[9] = VAnt_Polygon_GPSlot_8
   VTmp_Subs[10] = VAnt_Polygon_GPSlot_9
   VTmp_Subs[11] = VAnt_Polygon_GPSlot_10
   VTmp_Subs[12] = VAnt_Polygon_GPSlot_11
   VTmp_Subs[13] = VAnt_Polygon_GPSlot_12
   VAnt_Subtraction_GP_Slotted = VAnt_Geometry:Subtract(VAnt_Rectangle_GP, VTmp_Subs)
   VAnt_Subtraction_GP_Slotted.Label = "GP_Slotted"
--

-- STEP 22: Creating medium
   VAnt_Medium_FR4 = VAnt_Project.Media:AddDielectric()
   VAnt_Medium_FR4.Label = "FR4"
   VAnt_Medium_FR4.DielectricModelling.RelativePermittivity = 4.4
   VAnt_Medium_FR4.DielectricModelling.LossTangent = 0.02
--

-- STEP 23: Create new solid.cuboid
   VTmp_Corner = cf.Point(-4.17, -3.065, 0.0)
   VAnt_Cuboid_Substrate = VAnt_Geometry:AddCuboid(VTmp_Corner, 61.512, 79.704, 1.6)
   VAnt_Cuboid_Substrate.Label = "Substrate"
--

-- STEP 24: Set solid medium
   VAnt_Cuboid_Substrate.Regions:Item(1).Medium = VAnt_Project.Media:Item("FR4")
--

-- STEP 25: Create new rectangular surface
   VTmp_Corner = cf.Point(-2.341, -3.065, 1.6)
   VAnt_Rectangle_RP = VAnt_Geometry:AddRectangle(VTmp_Corner, 59.633, 79.654)
   VAnt_Rectangle_RP.Label = "RP"
--

-- STEP 26: Create new rectangular surface
   VTmp_Corner = cf.Point(31.202, 31.406, 1.6)
   VAnt_Rectangle_GPSlot_0 = VAnt_Geometry:AddRectangle(VTmp_Corner, 10.102, 3.283)
   VAnt_Rectangle_GPSlot_0.Label = "GPSlot_0"
--

-- STEP 27: Create new rectangular surface
   VTmp_Corner = cf.Point(37.618, 55.842, 1.6)
   VAnt_Rectangle_GPSlot_1 = VAnt_Geometry:AddRectangle(VTmp_Corner, 2.355, 5.364)
   VAnt_Rectangle_GPSlot_1.Label = "GPSlot_1"
--

-- STEP 28: Create new rectangular surface
   VTmp_Corner = cf.Point(39.65, 82.148, 1.6)
   VAnt_Rectangle_GPSlot_2 = VAnt_Geometry:AddRectangle(VTmp_Corner, 3.065, 7.845)
   VAnt_Rectangle_GPSlot_2.Label = "GPSlot_2"
--

-- STEP 29: Create new rectangular surface
   VTmp_Corner = cf.Point(56.019, 53.584, 1.6)
   VAnt_Rectangle_GPSlot_3 = VAnt_Geometry:AddRectangle(VTmp_Corner, 2.49, 0.535)
   VAnt_Rectangle_GPSlot_3.Label = "GPSlot_3"
--

-- STEP 30: Create new rectangular surface
   VTmp_Corner = cf.Point(15.363, 35.624, 1.6)
   VAnt_Rectangle_GPSlot_4 = VAnt_Geometry:AddRectangle(VTmp_Corner, 0.609, 3.653)
   VAnt_Rectangle_GPSlot_4.Label = "GPSlot_4"
--

-- STEP 31: Create new rectangular surface
   VTmp_Corner = cf.Point(57.946, 76.937, 1.6)
   VAnt_Rectangle_GPSlot_5 = VAnt_Geometry:AddRectangle(VTmp_Corner, 3.491, 4.789)
   VAnt_Rectangle_GPSlot_5.Label = "GPSlot_5"
--

-- STEP 32: Create new rectangular surface
   VTmp_Corner = cf.Point(43.568, 27.942, 1.6)
   VAnt_Rectangle_GPSlot_6 = VAnt_Geometry:AddRectangle(VTmp_Corner, 2.677, 1.82)
   VAnt_Rectangle_GPSlot_6.Label = "GPSlot_6"
--

-- STEP 33: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(14.562, 76.327, 1.6)
   VTmp_Points[2] = cf.Point(11.343, 83.25, 1.6)
   VTmp_Points[3] = cf.Point(13.867, 79.345, 1.6)
   VAnt_Polygon_GPSlot_7 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_7.Label = "GPSlot_7"
--

-- STEP 34: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(46.102, -10.312, 1.6)
   VTmp_Points[2] = cf.Point(50.27, 0.823, 1.6)
   VTmp_Points[3] = cf.Point(50.402, 4.303, 1.6)
   VAnt_Polygon_GPSlot_8 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_8.Label = "GPSlot_8"
--

-- STEP 35: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(24.404, 41.309, 1.6)
   VTmp_Points[2] = cf.Point(22.521, 39.416, 1.6)
   VTmp_Points[3] = cf.Point(21.567, 41.739, 1.6)
   VAnt_Polygon_GPSlot_9 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_9.Label = "GPSlot_9"
--

-- STEP 36: Create new subtraction
   VTmp_Subs = {}
   VTmp_Subs[1] = VAnt_Rectangle_GPSlot_0
   VTmp_Subs[2] = VAnt_Rectangle_GPSlot_1
   VTmp_Subs[3] = VAnt_Rectangle_GPSlot_2
   VTmp_Subs[4] = VAnt_Rectangle_GPSlot_3
   VTmp_Subs[5] = VAnt_Rectangle_GPSlot_4
   VTmp_Subs[6] = VAnt_Rectangle_GPSlot_5
   VTmp_Subs[7] = VAnt_Rectangle_GPSlot_6
   VTmp_Subs[8] = VAnt_Polygon_GPSlot_7
   VTmp_Subs[9] = VAnt_Polygon_GPSlot_8
   VTmp_Subs[10] = VAnt_Polygon_GPSlot_9
   VAnt_Subtraction_RP_Slotted = VAnt_Geometry:Subtract(VAnt_Rectangle_RP, VTmp_Subs)
   VAnt_Subtraction_RP_Slotted.Label = "RP_Slotted"
--

-- STEP 37: Create new union
   VTmp_Parts = {}
   VTmp_Parts[1] = VAnt_Subtraction_GP_Slotted
   VTmp_Parts[2] = VAnt_Subtraction_RP_Slotted
   VTmp_Parts[3] = VAnt_Cuboid_Substrate
   VTmp_Parts[4] = VAnt_Polygon_Feed_Top
   VTmp_Parts[5] = VAnt_Polygon_Feed_Pos
   VTmp_Parts[6] = VAnt_Polygon_Feed_Neg
   VTmp_Parts[7] = VAnt_Polygon_Feed_Bot
   VAnt_Union_Onion = VAnt_Geometry:Union(VTmp_Parts)
   VAnt_Union_Onion.Label = "Onion"
--

-- STEP 38: Changing face medium
   VAnt_Union_Onion.Faces:Item("Face36").Medium = VAnt_Project.Media:Item("Perfect electric conductor")
--

-- STEP 39: Changing face medium
   VAnt_Union_Onion.Faces:Item("Face37").Medium = VAnt_Project.Media:Item("Perfect electric conductor")
--

-- STEP 40: Changing face medium
   VAnt_Union_Onion.Faces:Item("Face38").Medium = VAnt_Project.Media:Item("Perfect electric conductor")
--

-- STEP 41: Create new edge port
   VTmp_Pos = {}
   VTmp_Neg = {}
   VTmp_Pos[1] = VAnt_Union_Onion.Faces:Item("Face2")
   VTmp_Neg[1] = VAnt_Union_Onion.Faces:Item("Face3")
   VAnt_EPort_SourcePort = VAnt_Project.Ports:AddEdgePort(VTmp_Pos, VTmp_Neg)
   VAnt_EPort_SourcePort.Label = "SourcePort"
--

-- STEP 42: Get config file
   VAnt_Config = VAnt_Project.SolutionConfigurations[1]
--

-- STEP 43: Create new voltage source
   VAnt_VSource_VoltageSource = VAnt_Config.Sources:AddVoltageSource(VAnt_EPort_SourcePort)
   VAnt_VSource_VoltageSource.Impedance = 50.0
   VAnt_VSource_VoltageSource.Magnitude = 1.0
   VAnt_VSource_VoltageSource.Phase = 0.0
   VAnt_VSource_VoltageSource.Label = "VoltageSource"
--

-- STEP 44: Create new Far-Field request
   VAnt_Config.FarFields:Add(0.0, 0.0, 180.0, 360.0, 5.0, 5.0)
--
-- STEP 45: Set frequency range
   VAnt_tmp = VAnt_Config.Frequency:GetProperties()
   VAnt_tmp.Start  = 906500000.0
   VAnt_tmp.End    = 933500000.0
   VAnt_tmp.RangeType  = cf.Enums.FrequencyRangeTypeEnum.LinearSpacedDiscrete
   VAnt_tmp.NumberOfDiscreteValues = 2
   VAnt_Config.Frequency:SetProperties(VAnt_tmp)
--

-- STEP 46: Mesh the project
   VAnt_Project.Mesher.Settings.WireRadius = 0.001
   VAnt_Project.Mesher.Settings.MeshSizeOption = cf.Enums.MeshSizeOptionEnum.Coarse
   VAnt_Project.Mesher:Mesh()
--

-- STEP 47: Save project
   VSes_Application:SaveAs("C:/Users/project/0. My Work/1. Repositories/1. Very Unfriendly Train/Data/Simulations/637072128687662976_Primary/637072223066233344_8/8.cfx")
--

-- STEP 48: Run simulation
   VAnt_Project.Launcher.Settings.FEKO.Parallel.Enabled = true
   VAnt_Project.Launcher:RunFEKO()
--

-- STEP 49: Close project
   VSes_Application:CloseAllWindows()
--

-- STEP 1: Make a new project
   VAnt_Project    = VSes_Application:NewProject()
   VAnt_Geometry   = VAnt_Project.Geometry
--

-- STEP 2: Set project unit of measurement
   VAnt_Project.ModelUnit  = cf.Enums.ModelUnitEnum.Millimetres
--

-- STEP 3: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(58.787000000000006, 33.191500000000005, 1.6)
   VTmp_Points[2] = cf.Point(58.787000000000006, 35.31250000000001, 1.6)
   VTmp_Points[3] = cf.Point(60.437000000000005, 35.31250000000001, 1.6)
   VTmp_Points[4] = cf.Point(60.437000000000005, 33.191500000000005, 1.6)
   VAnt_Polygon_Feed_Top = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_Feed_Top.Label = "Feed_Top"
--

-- STEP 4: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(60.437000000000005, 35.31250000000001, 1.6)
   VTmp_Points[2] = cf.Point(60.437000000000005, 35.31250000000001, 0.8)
   VTmp_Points[3] = cf.Point(60.437000000000005, 33.191500000000005, 0.8)
   VTmp_Points[4] = cf.Point(60.437000000000005, 33.191500000000005, 1.6)
   VAnt_Polygon_Feed_Pos = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_Feed_Pos.Label = "Feed_Pos"
--

-- STEP 5: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(60.437000000000005, 35.31250000000001, 0.0)
   VTmp_Points[2] = cf.Point(60.437000000000005, 35.31250000000001, 0.8)
   VTmp_Points[3] = cf.Point(60.437000000000005, 33.191500000000005, 0.8)
   VTmp_Points[4] = cf.Point(60.437000000000005, 33.191500000000005, 0.0)
   VAnt_Polygon_Feed_Neg = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_Feed_Neg.Label = "Feed_Neg"
--

-- STEP 6: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(60.437000000000005, 33.191500000000005, 0.0)
   VTmp_Points[2] = cf.Point(60.437000000000005, 35.31250000000001, 0.0)
   VTmp_Points[3] = cf.Point(58.837, 35.31250000000001, 0.0)
   VTmp_Points[4] = cf.Point(58.837, 33.191500000000005, 0.0)
   VAnt_Polygon_Feed_Bot = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_Feed_Bot.Label = "Feed_Bot"
--

-- STEP 7: Create new rectangular surface
   VTmp_Corner = cf.Point(-4.191, -1.446, 0.0)
   VAnt_Rectangle_GP = VAnt_Geometry:AddRectangle(VTmp_Corner, 63.028000000000006, 77.101)
   VAnt_Rectangle_GP.Label = "GP"
--

-- STEP 8: Create new rectangular surface
   VTmp_Corner = cf.Point(-2.829, 100.645, 0.0)
   VAnt_Rectangle_GPSlot_0 = VAnt_Geometry:AddRectangle(VTmp_Corner, 9.968, 9.783)
   VAnt_Rectangle_GPSlot_0.Label = "GPSlot_0"
--

-- STEP 9: Create new rectangular surface
   VTmp_Corner = cf.Point(12.957, 21.94, 0.0)
   VAnt_Rectangle_GPSlot_1 = VAnt_Geometry:AddRectangle(VTmp_Corner, 2.017, 24.98)
   VAnt_Rectangle_GPSlot_1.Label = "GPSlot_1"
--

-- STEP 10: Create new rectangular surface
   VTmp_Corner = cf.Point(18.641, 55.791, 0.0)
   VAnt_Rectangle_GPSlot_2 = VAnt_Geometry:AddRectangle(VTmp_Corner, 10.366, 15.955)
   VAnt_Rectangle_GPSlot_2.Label = "GPSlot_2"
--

-- STEP 11: Create new rectangular surface
   VTmp_Corner = cf.Point(41.46, 53.629, 0.0)
   VAnt_Rectangle_GPSlot_3 = VAnt_Geometry:AddRectangle(VTmp_Corner, 5.693, 9.566)
   VAnt_Rectangle_GPSlot_3.Label = "GPSlot_3"
--

-- STEP 12: Create new rectangular surface
   VTmp_Corner = cf.Point(48.196, 84.88, 0.0)
   VAnt_Rectangle_GPSlot_4 = VAnt_Geometry:AddRectangle(VTmp_Corner, 11.444, 4.324)
   VAnt_Rectangle_GPSlot_4.Label = "GPSlot_4"
--

-- STEP 13: Create new rectangular surface
   VTmp_Corner = cf.Point(52.462, 56.77, 0.0)
   VAnt_Rectangle_GPSlot_5 = VAnt_Geometry:AddRectangle(VTmp_Corner, 3.03, 4.496)
   VAnt_Rectangle_GPSlot_5.Label = "GPSlot_5"
--

-- STEP 14: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(86.881, 133.647, 0.0)
   VTmp_Points[2] = cf.Point(74.157, 109.118, 0.0)
   VTmp_Points[3] = cf.Point(77.207, 105.332, 0.0)
   VAnt_Polygon_GPSlot_6 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_6.Label = "GPSlot_6"
--

-- STEP 15: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(22.194, 89.899, 0.0)
   VTmp_Points[2] = cf.Point(3.989, 136.608, 0.0)
   VTmp_Points[3] = cf.Point(18.932, 89.129, 0.0)
   VAnt_Polygon_GPSlot_7 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_7.Label = "GPSlot_7"
--

-- STEP 16: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(46.065, 21.752, 0.0)
   VTmp_Points[2] = cf.Point(58.279, -18.976, 0.0)
   VTmp_Points[3] = cf.Point(74.282, 2.588, 0.0)
   VAnt_Polygon_GPSlot_8 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_8.Label = "GPSlot_8"
--

-- STEP 17: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(22.281, 106.962, 0.0)
   VTmp_Points[2] = cf.Point(52.798, 77.204, 0.0)
   VTmp_Points[3] = cf.Point(56.527, 67.468, 0.0)
   VAnt_Polygon_GPSlot_9 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_9.Label = "GPSlot_9"
--

-- STEP 18: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(41.951, 38.261, 0.0)
   VTmp_Points[2] = cf.Point(61.417, -2.669, 0.0)
   VTmp_Points[3] = cf.Point(14.529, 8.214, 0.0)
   VAnt_Polygon_GPSlot_10 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_10.Label = "GPSlot_10"
--

-- STEP 19: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(3.714, 10.75, 0.0)
   VTmp_Points[2] = cf.Point(41.681, 6.891, 0.0)
   VTmp_Points[3] = cf.Point(49.239, 22.629, 0.0)
   VAnt_Polygon_GPSlot_11 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_11.Label = "GPSlot_11"
--

-- STEP 20: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(21.539, 56.168, 0.0)
   VTmp_Points[2] = cf.Point(35.465, 76.866, 0.0)
   VTmp_Points[3] = cf.Point(21.151, 76.119, 0.0)
   VAnt_Polygon_GPSlot_12 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_12.Label = "GPSlot_12"
--

-- STEP 21: Create new subtraction
   VTmp_Subs = {}
   VTmp_Subs[1] = VAnt_Rectangle_GPSlot_0
   VTmp_Subs[2] = VAnt_Rectangle_GPSlot_1
   VTmp_Subs[3] = VAnt_Rectangle_GPSlot_2
   VTmp_Subs[4] = VAnt_Rectangle_GPSlot_3
   VTmp_Subs[5] = VAnt_Rectangle_GPSlot_4
   VTmp_Subs[6] = VAnt_Rectangle_GPSlot_5
   VTmp_Subs[7] = VAnt_Polygon_GPSlot_6
   VTmp_Subs[8] = VAnt_Polygon_GPSlot_7
   VTmp_Subs[9] = VAnt_Polygon_GPSlot_8
   VTmp_Subs[10] = VAnt_Polygon_GPSlot_9
   VTmp_Subs[11] = VAnt_Polygon_GPSlot_10
   VTmp_Subs[12] = VAnt_Polygon_GPSlot_11
   VTmp_Subs[13] = VAnt_Polygon_GPSlot_12
   VAnt_Subtraction_GP_Slotted = VAnt_Geometry:Subtract(VAnt_Rectangle_GP, VTmp_Subs)
   VAnt_Subtraction_GP_Slotted.Label = "GP_Slotted"
--

-- STEP 22: Creating medium
   VAnt_Medium_FR4 = VAnt_Project.Media:AddDielectric()
   VAnt_Medium_FR4.Label = "FR4"
   VAnt_Medium_FR4.DielectricModelling.RelativePermittivity = 4.4
   VAnt_Medium_FR4.DielectricModelling.LossTangent = 0.02
--

-- STEP 23: Create new solid.cuboid
   VTmp_Corner = cf.Point(-4.191, -3.105, 0.0)
   VAnt_Cuboid_Substrate = VAnt_Geometry:AddCuboid(VTmp_Corner, 63.028000000000006, 79.713, 1.6)
   VAnt_Cuboid_Substrate.Label = "Substrate"
--

-- STEP 24: Set solid medium
   VAnt_Cuboid_Substrate.Regions:Item(1).Medium = VAnt_Project.Media:Item("FR4")
--

-- STEP 25: Create new rectangular surface
   VTmp_Corner = cf.Point(-2.346, -3.105, 1.6)
   VAnt_Rectangle_RP = VAnt_Geometry:AddRectangle(VTmp_Corner, 61.133, 79.663)
   VAnt_Rectangle_RP.Label = "RP"
--

-- STEP 26: Create new rectangular surface
   VTmp_Corner = cf.Point(31.491, 31.365, 1.6)
   VAnt_Rectangle_GPSlot_0 = VAnt_Geometry:AddRectangle(VTmp_Corner, 9.124, 3.686)
   VAnt_Rectangle_GPSlot_0.Label = "GPSlot_0"
--

-- STEP 27: Create new rectangular surface
   VTmp_Corner = cf.Point(37.385, 55.034, 1.6)
   VAnt_Rectangle_GPSlot_1 = VAnt_Geometry:AddRectangle(VTmp_Corner, 2.402, 5.682)
   VAnt_Rectangle_GPSlot_1.Label = "GPSlot_1"
--

-- STEP 28: Create new rectangular surface
   VTmp_Corner = cf.Point(38.296, 81.712, 1.6)
   VAnt_Rectangle_GPSlot_2 = VAnt_Geometry:AddRectangle(VTmp_Corner, 3.733, 7.425)
   VAnt_Rectangle_GPSlot_2.Label = "GPSlot_2"
--

-- STEP 29: Create new rectangular surface
   VTmp_Corner = cf.Point(57.03, 53.933, 1.6)
   VAnt_Rectangle_GPSlot_3 = VAnt_Geometry:AddRectangle(VTmp_Corner, 2.07, 0.49)
   VAnt_Rectangle_GPSlot_3.Label = "GPSlot_3"
--

-- STEP 30: Create new rectangular surface
   VTmp_Corner = cf.Point(15.767, 34.23, 1.6)
   VAnt_Rectangle_GPSlot_4 = VAnt_Geometry:AddRectangle(VTmp_Corner, 1.449, 2.305)
   VAnt_Rectangle_GPSlot_4.Label = "GPSlot_4"
--

-- STEP 31: Create new rectangular surface
   VTmp_Corner = cf.Point(58.614, 77.815, 1.6)
   VAnt_Rectangle_GPSlot_5 = VAnt_Geometry:AddRectangle(VTmp_Corner, 4.906, 5.316)
   VAnt_Rectangle_GPSlot_5.Label = "GPSlot_5"
--

-- STEP 32: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(13.9, 75.127, 1.6)
   VTmp_Points[2] = cf.Point(10.98, 83.936, 1.6)
   VTmp_Points[3] = cf.Point(13.321, 77.752, 1.6)
   VAnt_Polygon_GPSlot_6 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_6.Label = "GPSlot_6"
--

-- STEP 33: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(47.005, -9.273, 1.6)
   VTmp_Points[2] = cf.Point(50.95, 0.419, 1.6)
   VTmp_Points[3] = cf.Point(49.342, 3.749, 1.6)
   VAnt_Polygon_GPSlot_7 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_7.Label = "GPSlot_7"
--

-- STEP 34: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(24.738, 41.789, 1.6)
   VTmp_Points[2] = cf.Point(21.098, 39.664, 1.6)
   VTmp_Points[3] = cf.Point(22.114, 42.593, 1.6)
   VAnt_Polygon_GPSlot_8 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_8.Label = "GPSlot_8"
--

-- STEP 35: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(10.664, 41.223, 1.6)
   VTmp_Points[2] = cf.Point(10.545, 40.297, 1.6)
   VTmp_Points[3] = cf.Point(10.391, 40.861, 1.6)
   VAnt_Polygon_GPSlot_9 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_9.Label = "GPSlot_9"
--

-- STEP 36: Create new subtraction
   VTmp_Subs = {}
   VTmp_Subs[1] = VAnt_Rectangle_GPSlot_0
   VTmp_Subs[2] = VAnt_Rectangle_GPSlot_1
   VTmp_Subs[3] = VAnt_Rectangle_GPSlot_2
   VTmp_Subs[4] = VAnt_Rectangle_GPSlot_3
   VTmp_Subs[5] = VAnt_Rectangle_GPSlot_4
   VTmp_Subs[6] = VAnt_Rectangle_GPSlot_5
   VTmp_Subs[7] = VAnt_Polygon_GPSlot_6
   VTmp_Subs[8] = VAnt_Polygon_GPSlot_7
   VTmp_Subs[9] = VAnt_Polygon_GPSlot_8
   VTmp_Subs[10] = VAnt_Polygon_GPSlot_9
   VAnt_Subtraction_RP_Slotted = VAnt_Geometry:Subtract(VAnt_Rectangle_RP, VTmp_Subs)
   VAnt_Subtraction_RP_Slotted.Label = "RP_Slotted"
--

-- STEP 37: Create new union
   VTmp_Parts = {}
   VTmp_Parts[1] = VAnt_Subtraction_GP_Slotted
   VTmp_Parts[2] = VAnt_Subtraction_RP_Slotted
   VTmp_Parts[3] = VAnt_Cuboid_Substrate
   VTmp_Parts[4] = VAnt_Polygon_Feed_Top
   VTmp_Parts[5] = VAnt_Polygon_Feed_Pos
   VTmp_Parts[6] = VAnt_Polygon_Feed_Neg
   VTmp_Parts[7] = VAnt_Polygon_Feed_Bot
   VAnt_Union_Onion = VAnt_Geometry:Union(VTmp_Parts)
   VAnt_Union_Onion.Label = "Onion"
--

-- STEP 38: Changing face medium
   VAnt_Union_Onion.Faces:Item("Face36").Medium = VAnt_Project.Media:Item("Perfect electric conductor")
--

-- STEP 39: Changing face medium
   VAnt_Union_Onion.Faces:Item("Face37").Medium = VAnt_Project.Media:Item("Perfect electric conductor")
--

-- STEP 40: Changing face medium
   VAnt_Union_Onion.Faces:Item("Face38").Medium = VAnt_Project.Media:Item("Perfect electric conductor")
--

-- STEP 41: Create new edge port
   VTmp_Pos = {}
   VTmp_Neg = {}
   VTmp_Pos[1] = VAnt_Union_Onion.Faces:Item("Face2")
   VTmp_Neg[1] = VAnt_Union_Onion.Faces:Item("Face3")
   VAnt_EPort_SourcePort = VAnt_Project.Ports:AddEdgePort(VTmp_Pos, VTmp_Neg)
   VAnt_EPort_SourcePort.Label = "SourcePort"
--

-- STEP 42: Get config file
   VAnt_Config = VAnt_Project.SolutionConfigurations[1]
--

-- STEP 43: Create new voltage source
   VAnt_VSource_VoltageSource = VAnt_Config.Sources:AddVoltageSource(VAnt_EPort_SourcePort)
   VAnt_VSource_VoltageSource.Impedance = 50.0
   VAnt_VSource_VoltageSource.Magnitude = 1.0
   VAnt_VSource_VoltageSource.Phase = 0.0
   VAnt_VSource_VoltageSource.Label = "VoltageSource"
--

-- STEP 44: Create new Far-Field request
   VAnt_Config.FarFields:Add(0.0, 0.0, 180.0, 360.0, 5.0, 5.0)
--
-- STEP 45: Set frequency range
   VAnt_tmp = VAnt_Config.Frequency:GetProperties()
   VAnt_tmp.Start  = 906500000.0
   VAnt_tmp.End    = 933500000.0
   VAnt_tmp.RangeType  = cf.Enums.FrequencyRangeTypeEnum.LinearSpacedDiscrete
   VAnt_tmp.NumberOfDiscreteValues = 2
   VAnt_Config.Frequency:SetProperties(VAnt_tmp)
--

-- STEP 46: Mesh the project
   VAnt_Project.Mesher.Settings.WireRadius = 0.001
   VAnt_Project.Mesher.Settings.MeshSizeOption = cf.Enums.MeshSizeOptionEnum.Coarse
   VAnt_Project.Mesher:Mesh()
--

-- STEP 47: Save project
   VSes_Application:SaveAs("C:/Users/project/0. My Work/1. Repositories/1. Very Unfriendly Train/Data/Simulations/637072128687662976_Primary/637072223066233344_9/9.cfx")
--

-- STEP 48: Run simulation
   VAnt_Project.Launcher.Settings.FEKO.Parallel.Enabled = true
   VAnt_Project.Launcher:RunFEKO()
--

-- STEP 49: Close project
   VSes_Application:CloseAllWindows()
--

-- STEP ??: Close file
   VSes_Application:CloseAllWindows()
   VSes_Application:Close()
--
