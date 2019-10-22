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
   VTmp_Points[1] = cf.Point(76.769, 46.512, 1.6)
   VTmp_Points[2] = cf.Point(76.769, 48.466, 1.6)
   VTmp_Points[3] = cf.Point(78.419, 48.466, 1.6)
   VTmp_Points[4] = cf.Point(78.419, 46.512, 1.6)
   VAnt_Polygon_Feed_Top = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_Feed_Top.Label = "Feed_Top"
--

-- STEP 4: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(78.419, 48.466, 1.6)
   VTmp_Points[2] = cf.Point(78.419, 48.466, 0.8)
   VTmp_Points[3] = cf.Point(78.419, 46.512, 0.8)
   VTmp_Points[4] = cf.Point(78.419, 46.512, 1.6)
   VAnt_Polygon_Feed_Pos = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_Feed_Pos.Label = "Feed_Pos"
--

-- STEP 5: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(78.419, 48.466, 0.0)
   VTmp_Points[2] = cf.Point(78.419, 48.466, 0.8)
   VTmp_Points[3] = cf.Point(78.419, 46.512, 0.8)
   VTmp_Points[4] = cf.Point(78.419, 46.512, 0.0)
   VAnt_Polygon_Feed_Neg = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_Feed_Neg.Label = "Feed_Neg"
--

-- STEP 6: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(78.419, 46.512, 0.0)
   VTmp_Points[2] = cf.Point(78.419, 48.466, 0.0)
   VTmp_Points[3] = cf.Point(76.819, 48.466, 0.0)
   VTmp_Points[4] = cf.Point(76.819, 46.512, 0.0)
   VAnt_Polygon_Feed_Bot = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_Feed_Bot.Label = "Feed_Bot"
--

-- STEP 7: Create new rectangular surface
   VTmp_Corner = cf.Point(-0.434, 0.452, 0.0)
   VAnt_Rectangle_GP = VAnt_Geometry:AddRectangle(VTmp_Corner, 77.253, 97.544)
   VAnt_Rectangle_GP.Label = "GP"
--

-- STEP 8: Create new rectangular surface
   VTmp_Corner = cf.Point(38.934, 14.01, 0.0)
   VAnt_Rectangle_GPSlot_0 = VAnt_Geometry:AddRectangle(VTmp_Corner, 11.265, 13.953)
   VAnt_Rectangle_GPSlot_0.Label = "GPSlot_0"
--

-- STEP 9: Create new rectangular surface
   VTmp_Corner = cf.Point(46.274, 19.885, 0.0)
   VAnt_Rectangle_GPSlot_1 = VAnt_Geometry:AddRectangle(VTmp_Corner, 3.438, 4.211)
   VAnt_Rectangle_GPSlot_1.Label = "GPSlot_1"
--

-- STEP 10: Create new rectangular surface
   VTmp_Corner = cf.Point(61.75, 23.375, 0.0)
   VAnt_Rectangle_GPSlot_2 = VAnt_Geometry:AddRectangle(VTmp_Corner, 25.193, 2.694)
   VAnt_Rectangle_GPSlot_2.Label = "GPSlot_2"
--

-- STEP 11: Create new rectangular surface
   VTmp_Corner = cf.Point(33.054, 82.923, 0.0)
   VAnt_Rectangle_GPSlot_3 = VAnt_Geometry:AddRectangle(VTmp_Corner, 15.932, 18.885)
   VAnt_Rectangle_GPSlot_3.Label = "GPSlot_3"
--

-- STEP 12: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(29.023, 6.208, 0.0)
   VTmp_Points[2] = cf.Point(33.496, 22.286, 0.0)
   VTmp_Points[3] = cf.Point(24.033, -8.445, 0.0)
   VAnt_Polygon_GPSlot_4 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_4.Label = "GPSlot_4"
--

-- STEP 13: Create new subtraction
   VTmp_Subs = {}
   VTmp_Subs[1] = VAnt_Rectangle_GPSlot_0
   VTmp_Subs[2] = VAnt_Rectangle_GPSlot_1
   VTmp_Subs[3] = VAnt_Rectangle_GPSlot_2
   VTmp_Subs[4] = VAnt_Rectangle_GPSlot_3
   VTmp_Subs[5] = VAnt_Polygon_GPSlot_4
   VAnt_Subtraction_GP_Slotted = VAnt_Geometry:Subtract(VAnt_Rectangle_GP, VTmp_Subs)
   VAnt_Subtraction_GP_Slotted.Label = "GP_Slotted"
--

-- STEP 14: Creating medium
   VAnt_Medium_FR4 = VAnt_Project.Media:AddDielectric()
   VAnt_Medium_FR4.Label = "FR4"
   VAnt_Medium_FR4.DielectricModelling.RelativePermittivity = 4.4
   VAnt_Medium_FR4.DielectricModelling.LossTangent = 0.02
--

-- STEP 15: Create new solid.cuboid
   VTmp_Corner = cf.Point(-0.434, 0.452, 0.0)
   VAnt_Cuboid_Substrate = VAnt_Geometry:AddCuboid(VTmp_Corner, 77.253, 100.94, 1.6)
   VAnt_Cuboid_Substrate.Label = "Substrate"
--

-- STEP 16: Set solid medium
   VAnt_Cuboid_Substrate.Regions:Item(1).Medium = VAnt_Project.Media:Item("FR4")
--

-- STEP 17: Create new rectangular surface
   VTmp_Corner = cf.Point(6.227, 4.568, 1.6)
   VAnt_Rectangle_RP = VAnt_Geometry:AddRectangle(VTmp_Corner, 70.542, 96.774)
   VAnt_Rectangle_RP.Label = "RP"
--

-- STEP 18: Create new rectangular surface
   VTmp_Corner = cf.Point(45.26, 78.042, 1.6)
   VAnt_Rectangle_GPSlot_0 = VAnt_Geometry:AddRectangle(VTmp_Corner, 1.696, 1.722)
   VAnt_Rectangle_GPSlot_0.Label = "GPSlot_0"
--

-- STEP 19: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(58.205, 23.768, 1.6)
   VTmp_Points[2] = cf.Point(59.579, 24.168, 1.6)
   VTmp_Points[3] = cf.Point(59.672, 19.036, 1.6)
   VAnt_Polygon_GPSlot_1 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_1.Label = "GPSlot_1"
--

-- STEP 20: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(59.28, 6.564, 1.6)
   VTmp_Points[2] = cf.Point(61.802, 8.516, 1.6)
   VTmp_Points[3] = cf.Point(61.528, 8.042, 1.6)
   VAnt_Polygon_GPSlot_2 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_2.Label = "GPSlot_2"
--

-- STEP 21: Create new subtraction
   VTmp_Subs = {}
   VTmp_Subs[1] = VAnt_Rectangle_GPSlot_0
   VTmp_Subs[2] = VAnt_Polygon_GPSlot_1
   VTmp_Subs[3] = VAnt_Polygon_GPSlot_2
   VAnt_Subtraction_RP_Slotted = VAnt_Geometry:Subtract(VAnt_Rectangle_RP, VTmp_Subs)
   VAnt_Subtraction_RP_Slotted.Label = "RP_Slotted"
--

-- STEP 22: Create new union
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

-- STEP 23: Changing face medium
   VAnt_Union_Onion.Faces:Item("Face21").Medium = VAnt_Project.Media:Item("Perfect electric conductor")
--

-- STEP 24: Changing face medium
   VAnt_Union_Onion.Faces:Item("Face22").Medium = VAnt_Project.Media:Item("Perfect electric conductor")
--

-- STEP 25: Changing face medium
   VAnt_Union_Onion.Faces:Item("Face23").Medium = VAnt_Project.Media:Item("Perfect electric conductor")
--

-- STEP 26: Create new edge port
   VTmp_Pos = {}
   VTmp_Neg = {}
   VTmp_Pos[1] = VAnt_Union_Onion.Faces:Item("Face2")
   VTmp_Neg[1] = VAnt_Union_Onion.Faces:Item("Face3")
   VAnt_EPort_SourcePort = VAnt_Project.Ports:AddEdgePort(VTmp_Pos, VTmp_Neg)
   VAnt_EPort_SourcePort.Label = "SourcePort"
--

-- STEP 27: Get config file
   VAnt_Config = VAnt_Project.SolutionConfigurations[1]
--

-- STEP 28: Create new voltage source
   VAnt_VSource_VoltageSource = VAnt_Config.Sources:AddVoltageSource(VAnt_EPort_SourcePort)
   VAnt_VSource_VoltageSource.Impedance = 50.0
   VAnt_VSource_VoltageSource.Magnitude = 1.0
   VAnt_VSource_VoltageSource.Phase = 0.0
   VAnt_VSource_VoltageSource.Label = "VoltageSource"
--

-- STEP 29: Create new Far-Field request
   VAnt_Config.FarFields:Add(0.0, 0.0, 180.0, 360.0, 5.0, 5.0)
--
-- STEP 30: Set frequency range
   VAnt_tmp = VAnt_Config.Frequency:GetProperties()
   VAnt_tmp.Start  = 906500000.0
   VAnt_tmp.End    = 933500000.0
   VAnt_tmp.RangeType  = cf.Enums.FrequencyRangeTypeEnum.LinearSpacedDiscrete
   VAnt_tmp.NumberOfDiscreteValues = 2
   VAnt_Config.Frequency:SetProperties(VAnt_tmp)
--

-- STEP 31: Mesh the project
   VAnt_Project.Mesher.Settings.WireRadius = 0.001
   VAnt_Project.Mesher.Settings.MeshSizeOption = cf.Enums.MeshSizeOptionEnum.Coarse
   VAnt_Project.Mesher:Mesh()
--

-- STEP 32: Save project
   VSes_Application:SaveAs("C:/Users/project/0. My Work/1. Repositories/1. Very Unfriendly Train/Data/Simulations/637072110041561472_Primary/637072123817201280_0/0.cfx")
--

-- STEP 33: Run simulation
   VAnt_Project.Launcher.Settings.FEKO.Parallel.Enabled = true
   VAnt_Project.Launcher:RunFEKO()
--

-- STEP 34: Close project
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
   VTmp_Points[1] = cf.Point(75.43799999999999, 47.807500000000005, 1.6)
   VTmp_Points[2] = cf.Point(75.43799999999999, 49.7385, 1.6)
   VTmp_Points[3] = cf.Point(81.02999999999999, 49.7385, 1.6)
   VTmp_Points[4] = cf.Point(81.02999999999999, 47.807500000000005, 1.6)
   VAnt_Polygon_Feed_Top = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_Feed_Top.Label = "Feed_Top"
--

-- STEP 4: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(81.02999999999999, 49.7385, 1.6)
   VTmp_Points[2] = cf.Point(81.02999999999999, 49.7385, 0.8)
   VTmp_Points[3] = cf.Point(81.02999999999999, 47.807500000000005, 0.8)
   VTmp_Points[4] = cf.Point(81.02999999999999, 47.807500000000005, 1.6)
   VAnt_Polygon_Feed_Pos = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_Feed_Pos.Label = "Feed_Pos"
--

-- STEP 5: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(81.02999999999999, 49.7385, 0.0)
   VTmp_Points[2] = cf.Point(81.02999999999999, 49.7385, 0.8)
   VTmp_Points[3] = cf.Point(81.02999999999999, 47.807500000000005, 0.8)
   VTmp_Points[4] = cf.Point(81.02999999999999, 47.807500000000005, 0.0)
   VAnt_Polygon_Feed_Neg = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_Feed_Neg.Label = "Feed_Neg"
--

-- STEP 6: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(81.02999999999999, 47.807500000000005, 0.0)
   VTmp_Points[2] = cf.Point(81.02999999999999, 49.7385, 0.0)
   VTmp_Points[3] = cf.Point(79.42999999999999, 49.7385, 0.0)
   VTmp_Points[4] = cf.Point(79.42999999999999, 47.807500000000005, 0.0)
   VAnt_Polygon_Feed_Bot = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_Feed_Bot.Label = "Feed_Bot"
--

-- STEP 7: Create new rectangular surface
   VTmp_Corner = cf.Point(-0.171, 0.141, 0.0)
   VAnt_Rectangle_GP = VAnt_Geometry:AddRectangle(VTmp_Corner, 79.601, 104.928)
   VAnt_Rectangle_GP.Label = "GP"
--

-- STEP 8: Create new rectangular surface
   VTmp_Corner = cf.Point(31.681, 11.617, 0.0)
   VAnt_Rectangle_GPSlot_0 = VAnt_Geometry:AddRectangle(VTmp_Corner, 17.224, 16.139)
   VAnt_Rectangle_GPSlot_0.Label = "GPSlot_0"
--

-- STEP 9: Create new rectangular surface
   VTmp_Corner = cf.Point(61.166, 23.874, 0.0)
   VAnt_Rectangle_GPSlot_1 = VAnt_Geometry:AddRectangle(VTmp_Corner, 30.726, 0.83)
   VAnt_Rectangle_GPSlot_1.Label = "GPSlot_1"
--

-- STEP 10: Create new rectangular surface
   VTmp_Corner = cf.Point(23.388, 71.717, 0.0)
   VAnt_Rectangle_GPSlot_2 = VAnt_Geometry:AddRectangle(VTmp_Corner, 25.838, 16.983)
   VAnt_Rectangle_GPSlot_2.Label = "GPSlot_2"
--

-- STEP 11: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(24.125, 2.858, 0.0)
   VTmp_Points[2] = cf.Point(37.158, 14.168, 0.0)
   VTmp_Points[3] = cf.Point(22.389, -4.753, 0.0)
   VAnt_Polygon_GPSlot_3 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_3.Label = "GPSlot_3"
--

-- STEP 12: Create new subtraction
   VTmp_Subs = {}
   VTmp_Subs[1] = VAnt_Rectangle_GPSlot_0
   VTmp_Subs[2] = VAnt_Rectangle_GPSlot_1
   VTmp_Subs[3] = VAnt_Rectangle_GPSlot_2
   VTmp_Subs[4] = VAnt_Polygon_GPSlot_3
   VAnt_Subtraction_GP_Slotted = VAnt_Geometry:Subtract(VAnt_Rectangle_GP, VTmp_Subs)
   VAnt_Subtraction_GP_Slotted.Label = "GP_Slotted"
--

-- STEP 13: Creating medium
   VAnt_Medium_FR4 = VAnt_Project.Media:AddDielectric()
   VAnt_Medium_FR4.Label = "FR4"
   VAnt_Medium_FR4.DielectricModelling.RelativePermittivity = 4.4
   VAnt_Medium_FR4.DielectricModelling.LossTangent = 0.02
--

-- STEP 14: Create new solid.cuboid
   VTmp_Corner = cf.Point(-0.171, 0.141, 0.0)
   VAnt_Cuboid_Substrate = VAnt_Geometry:AddCuboid(VTmp_Corner, 79.601, 104.928, 1.6)
   VAnt_Cuboid_Substrate.Label = "Substrate"
--

-- STEP 15: Set solid medium
   VAnt_Cuboid_Substrate.Regions:Item(1).Medium = VAnt_Project.Media:Item("FR4")
--

-- STEP 16: Create new rectangular surface
   VTmp_Corner = cf.Point(5.335, 5.193, 1.6)
   VAnt_Rectangle_RP = VAnt_Geometry:AddRectangle(VTmp_Corner, 70.103, 94.498)
   VAnt_Rectangle_RP.Label = "RP"
--

-- STEP 17: Create new rectangular surface
   VTmp_Corner = cf.Point(43.043, 78.941, 1.6)
   VAnt_Rectangle_GPSlot_0 = VAnt_Geometry:AddRectangle(VTmp_Corner, 4.024, 3.174)
   VAnt_Rectangle_GPSlot_0.Label = "GPSlot_0"
--

-- STEP 18: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(51.285, 9.042, 1.6)
   VTmp_Points[2] = cf.Point(46.745, 12.556, 1.6)
   VTmp_Points[3] = cf.Point(43.822, 14.862, 1.6)
   VAnt_Polygon_GPSlot_1 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_1.Label = "GPSlot_1"
--

-- STEP 19: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(58.343, 10.473, 1.6)
   VTmp_Points[2] = cf.Point(60.712, 7.22, 1.6)
   VTmp_Points[3] = cf.Point(62.025, 5.564, 1.6)
   VAnt_Polygon_GPSlot_2 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_2.Label = "GPSlot_2"
--

-- STEP 20: Create new subtraction
   VTmp_Subs = {}
   VTmp_Subs[1] = VAnt_Rectangle_GPSlot_0
   VTmp_Subs[2] = VAnt_Polygon_GPSlot_1
   VTmp_Subs[3] = VAnt_Polygon_GPSlot_2
   VAnt_Subtraction_RP_Slotted = VAnt_Geometry:Subtract(VAnt_Rectangle_RP, VTmp_Subs)
   VAnt_Subtraction_RP_Slotted.Label = "RP_Slotted"
--

-- STEP 21: Create new union
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

-- STEP 22: Changing face medium
   VAnt_Union_Onion.Faces:Item("Face20").Medium = VAnt_Project.Media:Item("Perfect electric conductor")
--

-- STEP 23: Changing face medium
   VAnt_Union_Onion.Faces:Item("Face21").Medium = VAnt_Project.Media:Item("Perfect electric conductor")
--

-- STEP 24: Changing face medium
   VAnt_Union_Onion.Faces:Item("Face22").Medium = VAnt_Project.Media:Item("Perfect electric conductor")
--

-- STEP 25: Create new edge port
   VTmp_Pos = {}
   VTmp_Neg = {}
   VTmp_Pos[1] = VAnt_Union_Onion.Faces:Item("Face2")
   VTmp_Neg[1] = VAnt_Union_Onion.Faces:Item("Face3")
   VAnt_EPort_SourcePort = VAnt_Project.Ports:AddEdgePort(VTmp_Pos, VTmp_Neg)
   VAnt_EPort_SourcePort.Label = "SourcePort"
--

-- STEP 26: Get config file
   VAnt_Config = VAnt_Project.SolutionConfigurations[1]
--

-- STEP 27: Create new voltage source
   VAnt_VSource_VoltageSource = VAnt_Config.Sources:AddVoltageSource(VAnt_EPort_SourcePort)
   VAnt_VSource_VoltageSource.Impedance = 50.0
   VAnt_VSource_VoltageSource.Magnitude = 1.0
   VAnt_VSource_VoltageSource.Phase = 0.0
   VAnt_VSource_VoltageSource.Label = "VoltageSource"
--

-- STEP 28: Create new Far-Field request
   VAnt_Config.FarFields:Add(0.0, 0.0, 180.0, 360.0, 5.0, 5.0)
--
-- STEP 29: Set frequency range
   VAnt_tmp = VAnt_Config.Frequency:GetProperties()
   VAnt_tmp.Start  = 906500000.0
   VAnt_tmp.End    = 933500000.0
   VAnt_tmp.RangeType  = cf.Enums.FrequencyRangeTypeEnum.LinearSpacedDiscrete
   VAnt_tmp.NumberOfDiscreteValues = 2
   VAnt_Config.Frequency:SetProperties(VAnt_tmp)
--

-- STEP 30: Mesh the project
   VAnt_Project.Mesher.Settings.WireRadius = 0.001
   VAnt_Project.Mesher.Settings.MeshSizeOption = cf.Enums.MeshSizeOptionEnum.Coarse
   VAnt_Project.Mesher:Mesh()
--

-- STEP 31: Save project
   VSes_Application:SaveAs("C:/Users/project/0. My Work/1. Repositories/1. Very Unfriendly Train/Data/Simulations/637072110041561472_Primary/637072123817201280_1/1.cfx")
--

-- STEP 32: Run simulation
   VAnt_Project.Launcher.Settings.FEKO.Parallel.Enabled = true
   VAnt_Project.Launcher:RunFEKO()
--

-- STEP 33: Close project
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
   VTmp_Points[1] = cf.Point(77.353, 47.620999999999995, 1.6)
   VTmp_Points[2] = cf.Point(77.353, 49.63099999999999, 1.6)
   VTmp_Points[3] = cf.Point(79.00299999999999, 49.63099999999999, 1.6)
   VTmp_Points[4] = cf.Point(79.00299999999999, 47.620999999999995, 1.6)
   VAnt_Polygon_Feed_Top = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_Feed_Top.Label = "Feed_Top"
--

-- STEP 4: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(79.00299999999999, 49.63099999999999, 1.6)
   VTmp_Points[2] = cf.Point(79.00299999999999, 49.63099999999999, 0.8)
   VTmp_Points[3] = cf.Point(79.00299999999999, 47.620999999999995, 0.8)
   VTmp_Points[4] = cf.Point(79.00299999999999, 47.620999999999995, 1.6)
   VAnt_Polygon_Feed_Pos = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_Feed_Pos.Label = "Feed_Pos"
--

-- STEP 5: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(79.00299999999999, 49.63099999999999, 0.0)
   VTmp_Points[2] = cf.Point(79.00299999999999, 49.63099999999999, 0.8)
   VTmp_Points[3] = cf.Point(79.00299999999999, 47.620999999999995, 0.8)
   VTmp_Points[4] = cf.Point(79.00299999999999, 47.620999999999995, 0.0)
   VAnt_Polygon_Feed_Neg = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_Feed_Neg.Label = "Feed_Neg"
--

-- STEP 6: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(79.00299999999999, 47.620999999999995, 0.0)
   VTmp_Points[2] = cf.Point(79.00299999999999, 49.63099999999999, 0.0)
   VTmp_Points[3] = cf.Point(77.40299999999999, 49.63099999999999, 0.0)
   VTmp_Points[4] = cf.Point(77.40299999999999, 47.620999999999995, 0.0)
   VAnt_Polygon_Feed_Bot = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_Feed_Bot.Label = "Feed_Bot"
--

-- STEP 7: Create new rectangular surface
   VTmp_Corner = cf.Point(-0.373, 1.014, 0.0)
   VAnt_Rectangle_GP = VAnt_Geometry:AddRectangle(VTmp_Corner, 77.776, 96.486)
   VAnt_Rectangle_GP.Label = "GP"
--

-- STEP 8: Create new rectangular surface
   VTmp_Corner = cf.Point(38.139, 6.0, 0.0)
   VAnt_Rectangle_GPSlot_0 = VAnt_Geometry:AddRectangle(VTmp_Corner, 10.158, 16.903)
   VAnt_Rectangle_GPSlot_0.Label = "GPSlot_0"
--

-- STEP 9: Create new rectangular surface
   VTmp_Corner = cf.Point(45.301, 11.341, 0.0)
   VAnt_Rectangle_GPSlot_1 = VAnt_Geometry:AddRectangle(VTmp_Corner, 2.089, 10.888)
   VAnt_Rectangle_GPSlot_1.Label = "GPSlot_1"
--

-- STEP 10: Create new rectangular surface
   VTmp_Corner = cf.Point(58.078, 19.91, 0.0)
   VAnt_Rectangle_GPSlot_2 = VAnt_Geometry:AddRectangle(VTmp_Corner, 16.765, 0.581)
   VAnt_Rectangle_GPSlot_2.Label = "GPSlot_2"
--

-- STEP 11: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(29.936, 4.669, 0.0)
   VTmp_Points[2] = cf.Point(39.319, 15.796, 0.0)
   VTmp_Points[3] = cf.Point(18.788, 0.237, 0.0)
   VAnt_Polygon_GPSlot_3 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_3.Label = "GPSlot_3"
--

-- STEP 12: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(77.594, 63.606, 0.0)
   VTmp_Points[2] = cf.Point(82.826, 32.375, 0.0)
   VTmp_Points[3] = cf.Point(57.471, 47.403, 0.0)
   VAnt_Polygon_GPSlot_4 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_4.Label = "GPSlot_4"
--

-- STEP 13: Create new subtraction
   VTmp_Subs = {}
   VTmp_Subs[1] = VAnt_Rectangle_GPSlot_0
   VTmp_Subs[2] = VAnt_Rectangle_GPSlot_1
   VTmp_Subs[3] = VAnt_Rectangle_GPSlot_2
   VTmp_Subs[4] = VAnt_Polygon_GPSlot_3
   VTmp_Subs[5] = VAnt_Polygon_GPSlot_4
   VAnt_Subtraction_GP_Slotted = VAnt_Geometry:Subtract(VAnt_Rectangle_GP, VTmp_Subs)
   VAnt_Subtraction_GP_Slotted.Label = "GP_Slotted"
--

-- STEP 14: Creating medium
   VAnt_Medium_FR4 = VAnt_Project.Media:AddDielectric()
   VAnt_Medium_FR4.Label = "FR4"
   VAnt_Medium_FR4.DielectricModelling.RelativePermittivity = 4.4
   VAnt_Medium_FR4.DielectricModelling.LossTangent = 0.02
--

-- STEP 15: Create new solid.cuboid
   VTmp_Corner = cf.Point(-0.373, 1.014, 0.0)
   VAnt_Cuboid_Substrate = VAnt_Geometry:AddCuboid(VTmp_Corner, 77.776, 98.81, 1.6)
   VAnt_Cuboid_Substrate.Label = "Substrate"
--

-- STEP 16: Set solid medium
   VAnt_Cuboid_Substrate.Regions:Item(1).Medium = VAnt_Project.Media:Item("FR4")
--

-- STEP 17: Create new rectangular surface
   VTmp_Corner = cf.Point(5.056, 4.191, 1.6)
   VAnt_Rectangle_RP = VAnt_Geometry:AddRectangle(VTmp_Corner, 72.297, 95.583)
   VAnt_Rectangle_RP.Label = "RP"
--

-- STEP 18: Create new rectangular surface
   VTmp_Corner = cf.Point(43.946, 75.889, 1.6)
   VAnt_Rectangle_GPSlot_0 = VAnt_Geometry:AddRectangle(VTmp_Corner, 4.047, 1.503)
   VAnt_Rectangle_GPSlot_0.Label = "GPSlot_0"
--

-- STEP 19: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(61.923, 21.435, 1.6)
   VTmp_Points[2] = cf.Point(57.388, 22.622, 1.6)
   VTmp_Points[3] = cf.Point(59.608, 16.094, 1.6)
   VAnt_Polygon_GPSlot_1 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_1.Label = "GPSlot_1"
--

-- STEP 20: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(59.764, 7.699, 1.6)
   VTmp_Points[2] = cf.Point(63.029, 8.347, 1.6)
   VTmp_Points[3] = cf.Point(63.311, 6.8, 1.6)
   VAnt_Polygon_GPSlot_2 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_2.Label = "GPSlot_2"
--

-- STEP 21: Create new subtraction
   VTmp_Subs = {}
   VTmp_Subs[1] = VAnt_Rectangle_GPSlot_0
   VTmp_Subs[2] = VAnt_Polygon_GPSlot_1
   VTmp_Subs[3] = VAnt_Polygon_GPSlot_2
   VAnt_Subtraction_RP_Slotted = VAnt_Geometry:Subtract(VAnt_Rectangle_RP, VTmp_Subs)
   VAnt_Subtraction_RP_Slotted.Label = "RP_Slotted"
--

-- STEP 22: Create new union
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

-- STEP 23: Changing face medium
   VAnt_Union_Onion.Faces:Item("Face21").Medium = VAnt_Project.Media:Item("Perfect electric conductor")
--

-- STEP 24: Changing face medium
   VAnt_Union_Onion.Faces:Item("Face22").Medium = VAnt_Project.Media:Item("Perfect electric conductor")
--

-- STEP 25: Changing face medium
   VAnt_Union_Onion.Faces:Item("Face23").Medium = VAnt_Project.Media:Item("Perfect electric conductor")
--

-- STEP 26: Create new edge port
   VTmp_Pos = {}
   VTmp_Neg = {}
   VTmp_Pos[1] = VAnt_Union_Onion.Faces:Item("Face2")
   VTmp_Neg[1] = VAnt_Union_Onion.Faces:Item("Face3")
   VAnt_EPort_SourcePort = VAnt_Project.Ports:AddEdgePort(VTmp_Pos, VTmp_Neg)
   VAnt_EPort_SourcePort.Label = "SourcePort"
--

-- STEP 27: Get config file
   VAnt_Config = VAnt_Project.SolutionConfigurations[1]
--

-- STEP 28: Create new voltage source
   VAnt_VSource_VoltageSource = VAnt_Config.Sources:AddVoltageSource(VAnt_EPort_SourcePort)
   VAnt_VSource_VoltageSource.Impedance = 50.0
   VAnt_VSource_VoltageSource.Magnitude = 1.0
   VAnt_VSource_VoltageSource.Phase = 0.0
   VAnt_VSource_VoltageSource.Label = "VoltageSource"
--

-- STEP 29: Create new Far-Field request
   VAnt_Config.FarFields:Add(0.0, 0.0, 180.0, 360.0, 5.0, 5.0)
--
-- STEP 30: Set frequency range
   VAnt_tmp = VAnt_Config.Frequency:GetProperties()
   VAnt_tmp.Start  = 906500000.0
   VAnt_tmp.End    = 933500000.0
   VAnt_tmp.RangeType  = cf.Enums.FrequencyRangeTypeEnum.LinearSpacedDiscrete
   VAnt_tmp.NumberOfDiscreteValues = 2
   VAnt_Config.Frequency:SetProperties(VAnt_tmp)
--

-- STEP 31: Mesh the project
   VAnt_Project.Mesher.Settings.WireRadius = 0.001
   VAnt_Project.Mesher.Settings.MeshSizeOption = cf.Enums.MeshSizeOptionEnum.Coarse
   VAnt_Project.Mesher:Mesh()
--

-- STEP 32: Save project
   VSes_Application:SaveAs("C:/Users/project/0. My Work/1. Repositories/1. Very Unfriendly Train/Data/Simulations/637072110041561472_Primary/637072123817201280_2/2.cfx")
--

-- STEP 33: Run simulation
   VAnt_Project.Launcher.Settings.FEKO.Parallel.Enabled = true
   VAnt_Project.Launcher:RunFEKO()
--

-- STEP 34: Close project
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
   VTmp_Points[1] = cf.Point(75.021, 46.849000000000004, 1.6)
   VTmp_Points[2] = cf.Point(75.021, 48.831, 1.6)
   VTmp_Points[3] = cf.Point(76.67099999999999, 48.831, 1.6)
   VTmp_Points[4] = cf.Point(76.67099999999999, 46.849000000000004, 1.6)
   VAnt_Polygon_Feed_Top = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_Feed_Top.Label = "Feed_Top"
--

-- STEP 4: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(76.67099999999999, 48.831, 1.6)
   VTmp_Points[2] = cf.Point(76.67099999999999, 48.831, 0.8)
   VTmp_Points[3] = cf.Point(76.67099999999999, 46.849000000000004, 0.8)
   VTmp_Points[4] = cf.Point(76.67099999999999, 46.849000000000004, 1.6)
   VAnt_Polygon_Feed_Pos = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_Feed_Pos.Label = "Feed_Pos"
--

-- STEP 5: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(76.67099999999999, 48.831, 0.0)
   VTmp_Points[2] = cf.Point(76.67099999999999, 48.831, 0.8)
   VTmp_Points[3] = cf.Point(76.67099999999999, 46.849000000000004, 0.8)
   VTmp_Points[4] = cf.Point(76.67099999999999, 46.849000000000004, 0.0)
   VAnt_Polygon_Feed_Neg = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_Feed_Neg.Label = "Feed_Neg"
--

-- STEP 6: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(76.67099999999999, 46.849000000000004, 0.0)
   VTmp_Points[2] = cf.Point(76.67099999999999, 48.831, 0.0)
   VTmp_Points[3] = cf.Point(75.071, 48.831, 0.0)
   VTmp_Points[4] = cf.Point(75.071, 46.849000000000004, 0.0)
   VAnt_Polygon_Feed_Bot = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_Feed_Bot.Label = "Feed_Bot"
--

-- STEP 7: Create new rectangular surface
   VTmp_Corner = cf.Point(-0.243, 0.401, 0.0)
   VAnt_Rectangle_GP = VAnt_Geometry:AddRectangle(VTmp_Corner, 75.314, 102.213)
   VAnt_Rectangle_GP.Label = "GP"
--

-- STEP 8: Create new rectangular surface
   VTmp_Corner = cf.Point(46.609, 8.023, 0.0)
   VAnt_Rectangle_GPSlot_0 = VAnt_Geometry:AddRectangle(VTmp_Corner, 18.974, 11.639)
   VAnt_Rectangle_GPSlot_0.Label = "GPSlot_0"
--

-- STEP 9: Create new rectangular surface
   VTmp_Corner = cf.Point(43.789, 17.774, 0.0)
   VAnt_Rectangle_GPSlot_1 = VAnt_Geometry:AddRectangle(VTmp_Corner, 3.939, 7.683)
   VAnt_Rectangle_GPSlot_1.Label = "GPSlot_1"
--

-- STEP 10: Create new rectangular surface
   VTmp_Corner = cf.Point(55.965, 20.579, 0.0)
   VAnt_Rectangle_GPSlot_2 = VAnt_Geometry:AddRectangle(VTmp_Corner, 26.044, 0.966)
   VAnt_Rectangle_GPSlot_2.Label = "GPSlot_2"
--

-- STEP 11: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(22.857, -3.45, 0.0)
   VTmp_Points[2] = cf.Point(37.309, 20.214, 0.0)
   VTmp_Points[3] = cf.Point(28.547, 1.394, 0.0)
   VAnt_Polygon_GPSlot_3 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_3.Label = "GPSlot_3"
--

-- STEP 12: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(35.931, 8.827, 0.0)
   VTmp_Points[2] = cf.Point(54.257, 39.5, 0.0)
   VTmp_Points[3] = cf.Point(56.717, 27.084, 0.0)
   VAnt_Polygon_GPSlot_4 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_4.Label = "GPSlot_4"
--

-- STEP 13: Create new subtraction
   VTmp_Subs = {}
   VTmp_Subs[1] = VAnt_Rectangle_GPSlot_0
   VTmp_Subs[2] = VAnt_Rectangle_GPSlot_1
   VTmp_Subs[3] = VAnt_Rectangle_GPSlot_2
   VTmp_Subs[4] = VAnt_Polygon_GPSlot_3
   VTmp_Subs[5] = VAnt_Polygon_GPSlot_4
   VAnt_Subtraction_GP_Slotted = VAnt_Geometry:Subtract(VAnt_Rectangle_GP, VTmp_Subs)
   VAnt_Subtraction_GP_Slotted.Label = "GP_Slotted"
--

-- STEP 14: Creating medium
   VAnt_Medium_FR4 = VAnt_Project.Media:AddDielectric()
   VAnt_Medium_FR4.Label = "FR4"
   VAnt_Medium_FR4.DielectricModelling.RelativePermittivity = 4.4
   VAnt_Medium_FR4.DielectricModelling.LossTangent = 0.02
--

-- STEP 15: Create new solid.cuboid
   VTmp_Corner = cf.Point(-0.243, 0.401, 0.0)
   VAnt_Cuboid_Substrate = VAnt_Geometry:AddCuboid(VTmp_Corner, 75.314, 102.213, 1.6)
   VAnt_Cuboid_Substrate.Label = "Substrate"
--

-- STEP 16: Set solid medium
   VAnt_Cuboid_Substrate.Regions:Item(1).Medium = VAnt_Project.Media:Item("FR4")
--

-- STEP 17: Create new rectangular surface
   VTmp_Corner = cf.Point(4.916, 3.743, 1.6)
   VAnt_Rectangle_RP = VAnt_Geometry:AddRectangle(VTmp_Corner, 70.105, 95.608)
   VAnt_Rectangle_RP.Label = "RP"
--

-- STEP 18: Create new rectangular surface
   VTmp_Corner = cf.Point(45.345, 77.497, 1.6)
   VAnt_Rectangle_GPSlot_0 = VAnt_Geometry:AddRectangle(VTmp_Corner, 3.49, 2.547)
   VAnt_Rectangle_GPSlot_0.Label = "GPSlot_0"
--

-- STEP 19: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(48.634, 10.851, 1.6)
   VTmp_Points[2] = cf.Point(46.954, 10.179, 1.6)
   VTmp_Points[3] = cf.Point(48.554, 14.679, 1.6)
   VAnt_Polygon_GPSlot_1 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_1.Label = "GPSlot_1"
--

-- STEP 20: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(60.361, 8.322, 1.6)
   VTmp_Points[2] = cf.Point(61.262, 6.313, 1.6)
   VTmp_Points[3] = cf.Point(62.71, 7.224, 1.6)
   VAnt_Polygon_GPSlot_2 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_2.Label = "GPSlot_2"
--

-- STEP 21: Create new subtraction
   VTmp_Subs = {}
   VTmp_Subs[1] = VAnt_Rectangle_GPSlot_0
   VTmp_Subs[2] = VAnt_Polygon_GPSlot_1
   VTmp_Subs[3] = VAnt_Polygon_GPSlot_2
   VAnt_Subtraction_RP_Slotted = VAnt_Geometry:Subtract(VAnt_Rectangle_RP, VTmp_Subs)
   VAnt_Subtraction_RP_Slotted.Label = "RP_Slotted"
--

-- STEP 22: Create new union
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

-- STEP 23: Changing face medium
   VAnt_Union_Onion.Faces:Item("Face21").Medium = VAnt_Project.Media:Item("Perfect electric conductor")
--

-- STEP 24: Changing face medium
   VAnt_Union_Onion.Faces:Item("Face22").Medium = VAnt_Project.Media:Item("Perfect electric conductor")
--

-- STEP 25: Changing face medium
   VAnt_Union_Onion.Faces:Item("Face23").Medium = VAnt_Project.Media:Item("Perfect electric conductor")
--

-- STEP 26: Create new edge port
   VTmp_Pos = {}
   VTmp_Neg = {}
   VTmp_Pos[1] = VAnt_Union_Onion.Faces:Item("Face2")
   VTmp_Neg[1] = VAnt_Union_Onion.Faces:Item("Face3")
   VAnt_EPort_SourcePort = VAnt_Project.Ports:AddEdgePort(VTmp_Pos, VTmp_Neg)
   VAnt_EPort_SourcePort.Label = "SourcePort"
--

-- STEP 27: Get config file
   VAnt_Config = VAnt_Project.SolutionConfigurations[1]
--

-- STEP 28: Create new voltage source
   VAnt_VSource_VoltageSource = VAnt_Config.Sources:AddVoltageSource(VAnt_EPort_SourcePort)
   VAnt_VSource_VoltageSource.Impedance = 50.0
   VAnt_VSource_VoltageSource.Magnitude = 1.0
   VAnt_VSource_VoltageSource.Phase = 0.0
   VAnt_VSource_VoltageSource.Label = "VoltageSource"
--

-- STEP 29: Create new Far-Field request
   VAnt_Config.FarFields:Add(0.0, 0.0, 180.0, 360.0, 5.0, 5.0)
--
-- STEP 30: Set frequency range
   VAnt_tmp = VAnt_Config.Frequency:GetProperties()
   VAnt_tmp.Start  = 906500000.0
   VAnt_tmp.End    = 933500000.0
   VAnt_tmp.RangeType  = cf.Enums.FrequencyRangeTypeEnum.LinearSpacedDiscrete
   VAnt_tmp.NumberOfDiscreteValues = 2
   VAnt_Config.Frequency:SetProperties(VAnt_tmp)
--

-- STEP 31: Mesh the project
   VAnt_Project.Mesher.Settings.WireRadius = 0.001
   VAnt_Project.Mesher.Settings.MeshSizeOption = cf.Enums.MeshSizeOptionEnum.Coarse
   VAnt_Project.Mesher:Mesh()
--

-- STEP 32: Save project
   VSes_Application:SaveAs("C:/Users/project/0. My Work/1. Repositories/1. Very Unfriendly Train/Data/Simulations/637072110041561472_Primary/637072123817201280_3/3.cfx")
--

-- STEP 33: Run simulation
   VAnt_Project.Launcher.Settings.FEKO.Parallel.Enabled = true
   VAnt_Project.Launcher:RunFEKO()
--

-- STEP 34: Close project
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
   VTmp_Points[1] = cf.Point(74.892, 47.0745, 1.6)
   VTmp_Points[2] = cf.Point(74.892, 49.0955, 1.6)
   VTmp_Points[3] = cf.Point(76.72999999999999, 49.0955, 1.6)
   VTmp_Points[4] = cf.Point(76.72999999999999, 47.0745, 1.6)
   VAnt_Polygon_Feed_Top = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_Feed_Top.Label = "Feed_Top"
--

-- STEP 4: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(76.72999999999999, 49.0955, 1.6)
   VTmp_Points[2] = cf.Point(76.72999999999999, 49.0955, 0.8)
   VTmp_Points[3] = cf.Point(76.72999999999999, 47.0745, 0.8)
   VTmp_Points[4] = cf.Point(76.72999999999999, 47.0745, 1.6)
   VAnt_Polygon_Feed_Pos = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_Feed_Pos.Label = "Feed_Pos"
--

-- STEP 5: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(76.72999999999999, 49.0955, 0.0)
   VTmp_Points[2] = cf.Point(76.72999999999999, 49.0955, 0.8)
   VTmp_Points[3] = cf.Point(76.72999999999999, 47.0745, 0.8)
   VTmp_Points[4] = cf.Point(76.72999999999999, 47.0745, 0.0)
   VAnt_Polygon_Feed_Neg = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_Feed_Neg.Label = "Feed_Neg"
--

-- STEP 6: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(76.72999999999999, 47.0745, 0.0)
   VTmp_Points[2] = cf.Point(76.72999999999999, 49.0955, 0.0)
   VTmp_Points[3] = cf.Point(75.13, 49.0955, 0.0)
   VTmp_Points[4] = cf.Point(75.13, 47.0745, 0.0)
   VAnt_Polygon_Feed_Bot = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_Feed_Bot.Label = "Feed_Bot"
--

-- STEP 7: Create new rectangular surface
   VTmp_Corner = cf.Point(0.064, -0.008, 0.0)
   VAnt_Rectangle_GP = VAnt_Geometry:AddRectangle(VTmp_Corner, 75.066, 102.363)
   VAnt_Rectangle_GP.Label = "GP"
--

-- STEP 8: Create new rectangular surface
   VTmp_Corner = cf.Point(40.607, 7.68, 0.0)
   VAnt_Rectangle_GPSlot_0 = VAnt_Geometry:AddRectangle(VTmp_Corner, 13.844, 23.923)
   VAnt_Rectangle_GPSlot_0.Label = "GPSlot_0"
--

-- STEP 9: Create new rectangular surface
   VTmp_Corner = cf.Point(53.673, 10.67, 0.0)
   VAnt_Rectangle_GPSlot_1 = VAnt_Geometry:AddRectangle(VTmp_Corner, 5.599, 3.417)
   VAnt_Rectangle_GPSlot_1.Label = "GPSlot_1"
--

-- STEP 10: Create new rectangular surface
   VTmp_Corner = cf.Point(57.093, 32.027, 0.0)
   VAnt_Rectangle_GPSlot_2 = VAnt_Geometry:AddRectangle(VTmp_Corner, 25.518, 1.889)
   VAnt_Rectangle_GPSlot_2.Label = "GPSlot_2"
--

-- STEP 11: Create new rectangular surface
   VTmp_Corner = cf.Point(22.0, 34.372, 0.0)
   VAnt_Rectangle_GPSlot_3 = VAnt_Geometry:AddRectangle(VTmp_Corner, 9.305, 2.804)
   VAnt_Rectangle_GPSlot_3.Label = "GPSlot_3"
--

-- STEP 12: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(28.202, 3.505, 0.0)
   VTmp_Points[2] = cf.Point(37.358, 10.677, 0.0)
   VTmp_Points[3] = cf.Point(19.591, -2.061, 0.0)
   VAnt_Polygon_GPSlot_4 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_4.Label = "GPSlot_4"
--

-- STEP 13: Create new subtraction
   VTmp_Subs = {}
   VTmp_Subs[1] = VAnt_Rectangle_GPSlot_0
   VTmp_Subs[2] = VAnt_Rectangle_GPSlot_1
   VTmp_Subs[3] = VAnt_Rectangle_GPSlot_2
   VTmp_Subs[4] = VAnt_Rectangle_GPSlot_3
   VTmp_Subs[5] = VAnt_Polygon_GPSlot_4
   VAnt_Subtraction_GP_Slotted = VAnt_Geometry:Subtract(VAnt_Rectangle_GP, VTmp_Subs)
   VAnt_Subtraction_GP_Slotted.Label = "GP_Slotted"
--

-- STEP 14: Creating medium
   VAnt_Medium_FR4 = VAnt_Project.Media:AddDielectric()
   VAnt_Medium_FR4.Label = "FR4"
   VAnt_Medium_FR4.DielectricModelling.RelativePermittivity = 4.4
   VAnt_Medium_FR4.DielectricModelling.LossTangent = 0.02
--

-- STEP 15: Create new solid.cuboid
   VTmp_Corner = cf.Point(0.064, -0.008, 0.0)
   VAnt_Cuboid_Substrate = VAnt_Geometry:AddCuboid(VTmp_Corner, 75.066, 102.363, 1.6)
   VAnt_Cuboid_Substrate.Label = "Substrate"
--

-- STEP 16: Set solid medium
   VAnt_Cuboid_Substrate.Regions:Item(1).Medium = VAnt_Project.Media:Item("FR4")
--

-- STEP 17: Create new rectangular surface
   VTmp_Corner = cf.Point(5.43, 4.924, 1.6)
   VAnt_Rectangle_RP = VAnt_Geometry:AddRectangle(VTmp_Corner, 69.462, 94.922)
   VAnt_Rectangle_RP.Label = "RP"
--

-- STEP 18: Create new rectangular surface
   VTmp_Corner = cf.Point(43.526, 78.218, 1.6)
   VAnt_Rectangle_GPSlot_0 = VAnt_Geometry:AddRectangle(VTmp_Corner, 3.212, 2.632)
   VAnt_Rectangle_GPSlot_0.Label = "GPSlot_0"
--

-- STEP 19: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(61.872, 21.118, 1.6)
   VTmp_Points[2] = cf.Point(58.711, 24.073, 1.6)
   VTmp_Points[3] = cf.Point(60.35, 19.077, 1.6)
   VAnt_Polygon_GPSlot_1 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_1.Label = "GPSlot_1"
--

-- STEP 20: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(49.53, 10.954, 1.6)
   VTmp_Points[2] = cf.Point(47.103, 12.09, 1.6)
   VTmp_Points[3] = cf.Point(46.778, 14.482, 1.6)
   VAnt_Polygon_GPSlot_2 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_2.Label = "GPSlot_2"
--

-- STEP 21: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(59.098, 4.826, 1.6)
   VTmp_Points[2] = cf.Point(61.158, 8.384, 1.6)
   VTmp_Points[3] = cf.Point(62.806, 7.347, 1.6)
   VAnt_Polygon_GPSlot_3 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_3.Label = "GPSlot_3"
--

-- STEP 22: Create new subtraction
   VTmp_Subs = {}
   VTmp_Subs[1] = VAnt_Rectangle_GPSlot_0
   VTmp_Subs[2] = VAnt_Polygon_GPSlot_1
   VTmp_Subs[3] = VAnt_Polygon_GPSlot_2
   VTmp_Subs[4] = VAnt_Polygon_GPSlot_3
   VAnt_Subtraction_RP_Slotted = VAnt_Geometry:Subtract(VAnt_Rectangle_RP, VTmp_Subs)
   VAnt_Subtraction_RP_Slotted.Label = "RP_Slotted"
--

-- STEP 23: Create new union
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

-- STEP 24: Changing face medium
   VAnt_Union_Onion.Faces:Item("Face22").Medium = VAnt_Project.Media:Item("Perfect electric conductor")
--

-- STEP 25: Changing face medium
   VAnt_Union_Onion.Faces:Item("Face23").Medium = VAnt_Project.Media:Item("Perfect electric conductor")
--

-- STEP 26: Changing face medium
   VAnt_Union_Onion.Faces:Item("Face24").Medium = VAnt_Project.Media:Item("Perfect electric conductor")
--

-- STEP 27: Create new edge port
   VTmp_Pos = {}
   VTmp_Neg = {}
   VTmp_Pos[1] = VAnt_Union_Onion.Faces:Item("Face2")
   VTmp_Neg[1] = VAnt_Union_Onion.Faces:Item("Face3")
   VAnt_EPort_SourcePort = VAnt_Project.Ports:AddEdgePort(VTmp_Pos, VTmp_Neg)
   VAnt_EPort_SourcePort.Label = "SourcePort"
--

-- STEP 28: Get config file
   VAnt_Config = VAnt_Project.SolutionConfigurations[1]
--

-- STEP 29: Create new voltage source
   VAnt_VSource_VoltageSource = VAnt_Config.Sources:AddVoltageSource(VAnt_EPort_SourcePort)
   VAnt_VSource_VoltageSource.Impedance = 50.0
   VAnt_VSource_VoltageSource.Magnitude = 1.0
   VAnt_VSource_VoltageSource.Phase = 0.0
   VAnt_VSource_VoltageSource.Label = "VoltageSource"
--

-- STEP 30: Create new Far-Field request
   VAnt_Config.FarFields:Add(0.0, 0.0, 180.0, 360.0, 5.0, 5.0)
--
-- STEP 31: Set frequency range
   VAnt_tmp = VAnt_Config.Frequency:GetProperties()
   VAnt_tmp.Start  = 906500000.0
   VAnt_tmp.End    = 933500000.0
   VAnt_tmp.RangeType  = cf.Enums.FrequencyRangeTypeEnum.LinearSpacedDiscrete
   VAnt_tmp.NumberOfDiscreteValues = 2
   VAnt_Config.Frequency:SetProperties(VAnt_tmp)
--

-- STEP 32: Mesh the project
   VAnt_Project.Mesher.Settings.WireRadius = 0.001
   VAnt_Project.Mesher.Settings.MeshSizeOption = cf.Enums.MeshSizeOptionEnum.Coarse
   VAnt_Project.Mesher:Mesh()
--

-- STEP 33: Save project
   VSes_Application:SaveAs("C:/Users/project/0. My Work/1. Repositories/1. Very Unfriendly Train/Data/Simulations/637072110041561472_Primary/637072123817201280_4/4.cfx")
--

-- STEP 34: Run simulation
   VAnt_Project.Launcher.Settings.FEKO.Parallel.Enabled = true
   VAnt_Project.Launcher:RunFEKO()
--

-- STEP 35: Close project
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
   VTmp_Points[1] = cf.Point(77.765, 47.444500000000005, 1.6)
   VTmp_Points[2] = cf.Point(77.765, 49.34550000000001, 1.6)
   VTmp_Points[3] = cf.Point(79.41499999999999, 49.34550000000001, 1.6)
   VTmp_Points[4] = cf.Point(79.41499999999999, 47.444500000000005, 1.6)
   VAnt_Polygon_Feed_Top = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_Feed_Top.Label = "Feed_Top"
--

-- STEP 4: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(79.41499999999999, 49.34550000000001, 1.6)
   VTmp_Points[2] = cf.Point(79.41499999999999, 49.34550000000001, 0.8)
   VTmp_Points[3] = cf.Point(79.41499999999999, 47.444500000000005, 0.8)
   VTmp_Points[4] = cf.Point(79.41499999999999, 47.444500000000005, 1.6)
   VAnt_Polygon_Feed_Pos = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_Feed_Pos.Label = "Feed_Pos"
--

-- STEP 5: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(79.41499999999999, 49.34550000000001, 0.0)
   VTmp_Points[2] = cf.Point(79.41499999999999, 49.34550000000001, 0.8)
   VTmp_Points[3] = cf.Point(79.41499999999999, 47.444500000000005, 0.8)
   VTmp_Points[4] = cf.Point(79.41499999999999, 47.444500000000005, 0.0)
   VAnt_Polygon_Feed_Neg = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_Feed_Neg.Label = "Feed_Neg"
--

-- STEP 6: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(79.41499999999999, 47.444500000000005, 0.0)
   VTmp_Points[2] = cf.Point(79.41499999999999, 49.34550000000001, 0.0)
   VTmp_Points[3] = cf.Point(77.815, 49.34550000000001, 0.0)
   VTmp_Points[4] = cf.Point(77.815, 47.444500000000005, 0.0)
   VAnt_Polygon_Feed_Bot = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_Feed_Bot.Label = "Feed_Bot"
--

-- STEP 7: Create new rectangular surface
   VTmp_Corner = cf.Point(-0.835, 0.548, 0.0)
   VAnt_Rectangle_GP = VAnt_Geometry:AddRectangle(VTmp_Corner, 78.64999999999999, 95.946)
   VAnt_Rectangle_GP.Label = "GP"
--

-- STEP 8: Create new rectangular surface
   VTmp_Corner = cf.Point(41.269, 2.475, 0.0)
   VAnt_Rectangle_GPSlot_0 = VAnt_Geometry:AddRectangle(VTmp_Corner, 17.56, 14.756)
   VAnt_Rectangle_GPSlot_0.Label = "GPSlot_0"
--

-- STEP 9: Create new rectangular surface
   VTmp_Corner = cf.Point(48.699, 13.97, 0.0)
   VAnt_Rectangle_GPSlot_1 = VAnt_Geometry:AddRectangle(VTmp_Corner, 0.858, 2.914)
   VAnt_Rectangle_GPSlot_1.Label = "GPSlot_1"
--

-- STEP 10: Create new rectangular surface
   VTmp_Corner = cf.Point(62.688, 25.339, 0.0)
   VAnt_Rectangle_GPSlot_2 = VAnt_Geometry:AddRectangle(VTmp_Corner, 28.201, 3.094)
   VAnt_Rectangle_GPSlot_2.Label = "GPSlot_2"
--

-- STEP 11: Create new rectangular surface
   VTmp_Corner = cf.Point(75.574, -4.515, 0.0)
   VAnt_Rectangle_GPSlot_3 = VAnt_Geometry:AddRectangle(VTmp_Corner, 2.517, 2.251)
   VAnt_Rectangle_GPSlot_3.Label = "GPSlot_3"
--

-- STEP 12: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(24.874, 4.864, 0.0)
   VTmp_Points[2] = cf.Point(29.967, 11.655, 0.0)
   VTmp_Points[3] = cf.Point(19.55, -1.62, 0.0)
   VAnt_Polygon_GPSlot_4 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_4.Label = "GPSlot_4"
--

-- STEP 13: Create new subtraction
   VTmp_Subs = {}
   VTmp_Subs[1] = VAnt_Rectangle_GPSlot_0
   VTmp_Subs[2] = VAnt_Rectangle_GPSlot_1
   VTmp_Subs[3] = VAnt_Rectangle_GPSlot_2
   VTmp_Subs[4] = VAnt_Rectangle_GPSlot_3
   VTmp_Subs[5] = VAnt_Polygon_GPSlot_4
   VAnt_Subtraction_GP_Slotted = VAnt_Geometry:Subtract(VAnt_Rectangle_GP, VTmp_Subs)
   VAnt_Subtraction_GP_Slotted.Label = "GP_Slotted"
--

-- STEP 14: Creating medium
   VAnt_Medium_FR4 = VAnt_Project.Media:AddDielectric()
   VAnt_Medium_FR4.Label = "FR4"
   VAnt_Medium_FR4.DielectricModelling.RelativePermittivity = 4.4
   VAnt_Medium_FR4.DielectricModelling.LossTangent = 0.02
--

-- STEP 15: Create new solid.cuboid
   VTmp_Corner = cf.Point(-0.835, 0.548, 0.0)
   VAnt_Cuboid_Substrate = VAnt_Geometry:AddCuboid(VTmp_Corner, 78.64999999999999, 99.062, 1.6)
   VAnt_Cuboid_Substrate.Label = "Substrate"
--

-- STEP 16: Set solid medium
   VAnt_Cuboid_Substrate.Regions:Item(1).Medium = VAnt_Project.Media:Item("FR4")
--

-- STEP 17: Create new rectangular surface
   VTmp_Corner = cf.Point(6.307, 5.016, 1.6)
   VAnt_Rectangle_RP = VAnt_Geometry:AddRectangle(VTmp_Corner, 71.458, 94.544)
   VAnt_Rectangle_RP.Label = "RP"
--

-- STEP 18: Create new rectangular surface
   VTmp_Corner = cf.Point(45.066, 78.237, 1.6)
   VAnt_Rectangle_GPSlot_0 = VAnt_Geometry:AddRectangle(VTmp_Corner, 2.496, 0.988)
   VAnt_Rectangle_GPSlot_0.Label = "GPSlot_0"
--

-- STEP 19: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(61.548, 20.934, 1.6)
   VTmp_Points[2] = cf.Point(57.957, 25.241, 1.6)
   VTmp_Points[3] = cf.Point(61.618, 18.936, 1.6)
   VAnt_Polygon_GPSlot_1 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_1.Label = "GPSlot_1"
--

-- STEP 20: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(46.209, 10.559, 1.6)
   VTmp_Points[2] = cf.Point(45.857, 14.933, 1.6)
   VTmp_Points[3] = cf.Point(47.549, 12.374, 1.6)
   VAnt_Polygon_GPSlot_2 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_2.Label = "GPSlot_2"
--

-- STEP 21: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(59.424, 8.868, 1.6)
   VTmp_Points[2] = cf.Point(60.873, 6.769, 1.6)
   VTmp_Points[3] = cf.Point(61.622, 5.597, 1.6)
   VAnt_Polygon_GPSlot_3 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_3.Label = "GPSlot_3"
--

-- STEP 22: Create new subtraction
   VTmp_Subs = {}
   VTmp_Subs[1] = VAnt_Rectangle_GPSlot_0
   VTmp_Subs[2] = VAnt_Polygon_GPSlot_1
   VTmp_Subs[3] = VAnt_Polygon_GPSlot_2
   VTmp_Subs[4] = VAnt_Polygon_GPSlot_3
   VAnt_Subtraction_RP_Slotted = VAnt_Geometry:Subtract(VAnt_Rectangle_RP, VTmp_Subs)
   VAnt_Subtraction_RP_Slotted.Label = "RP_Slotted"
--

-- STEP 23: Create new union
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

-- STEP 24: Changing face medium
   VAnt_Union_Onion.Faces:Item("Face22").Medium = VAnt_Project.Media:Item("Perfect electric conductor")
--

-- STEP 25: Changing face medium
   VAnt_Union_Onion.Faces:Item("Face23").Medium = VAnt_Project.Media:Item("Perfect electric conductor")
--

-- STEP 26: Changing face medium
   VAnt_Union_Onion.Faces:Item("Face24").Medium = VAnt_Project.Media:Item("Perfect electric conductor")
--

-- STEP 27: Create new edge port
   VTmp_Pos = {}
   VTmp_Neg = {}
   VTmp_Pos[1] = VAnt_Union_Onion.Faces:Item("Face2")
   VTmp_Neg[1] = VAnt_Union_Onion.Faces:Item("Face3")
   VAnt_EPort_SourcePort = VAnt_Project.Ports:AddEdgePort(VTmp_Pos, VTmp_Neg)
   VAnt_EPort_SourcePort.Label = "SourcePort"
--

-- STEP 28: Get config file
   VAnt_Config = VAnt_Project.SolutionConfigurations[1]
--

-- STEP 29: Create new voltage source
   VAnt_VSource_VoltageSource = VAnt_Config.Sources:AddVoltageSource(VAnt_EPort_SourcePort)
   VAnt_VSource_VoltageSource.Impedance = 50.0
   VAnt_VSource_VoltageSource.Magnitude = 1.0
   VAnt_VSource_VoltageSource.Phase = 0.0
   VAnt_VSource_VoltageSource.Label = "VoltageSource"
--

-- STEP 30: Create new Far-Field request
   VAnt_Config.FarFields:Add(0.0, 0.0, 180.0, 360.0, 5.0, 5.0)
--
-- STEP 31: Set frequency range
   VAnt_tmp = VAnt_Config.Frequency:GetProperties()
   VAnt_tmp.Start  = 906500000.0
   VAnt_tmp.End    = 933500000.0
   VAnt_tmp.RangeType  = cf.Enums.FrequencyRangeTypeEnum.LinearSpacedDiscrete
   VAnt_tmp.NumberOfDiscreteValues = 2
   VAnt_Config.Frequency:SetProperties(VAnt_tmp)
--

-- STEP 32: Mesh the project
   VAnt_Project.Mesher.Settings.WireRadius = 0.001
   VAnt_Project.Mesher.Settings.MeshSizeOption = cf.Enums.MeshSizeOptionEnum.Coarse
   VAnt_Project.Mesher:Mesh()
--

-- STEP 33: Save project
   VSes_Application:SaveAs("C:/Users/project/0. My Work/1. Repositories/1. Very Unfriendly Train/Data/Simulations/637072110041561472_Primary/637072123817201280_5/5.cfx")
--

-- STEP 34: Run simulation
   VAnt_Project.Launcher.Settings.FEKO.Parallel.Enabled = true
   VAnt_Project.Launcher:RunFEKO()
--

-- STEP 35: Close project
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
   VTmp_Points[1] = cf.Point(75.055, 47.995999999999995, 1.6)
   VTmp_Points[2] = cf.Point(75.055, 49.952, 1.6)
   VTmp_Points[3] = cf.Point(78.238, 49.952, 1.6)
   VTmp_Points[4] = cf.Point(78.238, 47.995999999999995, 1.6)
   VAnt_Polygon_Feed_Top = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_Feed_Top.Label = "Feed_Top"
--

-- STEP 4: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(78.238, 49.952, 1.6)
   VTmp_Points[2] = cf.Point(78.238, 49.952, 0.8)
   VTmp_Points[3] = cf.Point(78.238, 47.995999999999995, 0.8)
   VTmp_Points[4] = cf.Point(78.238, 47.995999999999995, 1.6)
   VAnt_Polygon_Feed_Pos = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_Feed_Pos.Label = "Feed_Pos"
--

-- STEP 5: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(78.238, 49.952, 0.0)
   VTmp_Points[2] = cf.Point(78.238, 49.952, 0.8)
   VTmp_Points[3] = cf.Point(78.238, 47.995999999999995, 0.8)
   VTmp_Points[4] = cf.Point(78.238, 47.995999999999995, 0.0)
   VAnt_Polygon_Feed_Neg = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_Feed_Neg.Label = "Feed_Neg"
--

-- STEP 6: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(78.238, 47.995999999999995, 0.0)
   VTmp_Points[2] = cf.Point(78.238, 49.952, 0.0)
   VTmp_Points[3] = cf.Point(76.638, 49.952, 0.0)
   VTmp_Points[4] = cf.Point(76.638, 47.995999999999995, 0.0)
   VAnt_Polygon_Feed_Bot = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_Feed_Bot.Label = "Feed_Bot"
--

-- STEP 7: Create new rectangular surface
   VTmp_Corner = cf.Point(0.066, 0.819, 0.0)
   VAnt_Rectangle_GP = VAnt_Geometry:AddRectangle(VTmp_Corner, 76.572, 98.246)
   VAnt_Rectangle_GP.Label = "GP"
--

-- STEP 8: Create new rectangular surface
   VTmp_Corner = cf.Point(41.42, 7.817, 0.0)
   VAnt_Rectangle_GPSlot_0 = VAnt_Geometry:AddRectangle(VTmp_Corner, 16.909, 18.641)
   VAnt_Rectangle_GPSlot_0.Label = "GPSlot_0"
--

-- STEP 9: Create new rectangular surface
   VTmp_Corner = cf.Point(46.12, 17.491, 0.0)
   VAnt_Rectangle_GPSlot_1 = VAnt_Geometry:AddRectangle(VTmp_Corner, 0.775, 3.517)
   VAnt_Rectangle_GPSlot_1.Label = "GPSlot_1"
--

-- STEP 10: Create new rectangular surface
   VTmp_Corner = cf.Point(61.602, 20.412, 0.0)
   VAnt_Rectangle_GPSlot_2 = VAnt_Geometry:AddRectangle(VTmp_Corner, 26.169, 0.457)
   VAnt_Rectangle_GPSlot_2.Label = "GPSlot_2"
--

-- STEP 11: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(20.688, 5.289, 0.0)
   VTmp_Points[2] = cf.Point(35.313, 17.024, 0.0)
   VTmp_Points[3] = cf.Point(16.551, -3.123, 0.0)
   VAnt_Polygon_GPSlot_3 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_3.Label = "GPSlot_3"
--

-- STEP 12: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(73.485, 40.642, 0.0)
   VTmp_Points[2] = cf.Point(54.911, 71.575, 0.0)
   VTmp_Points[3] = cf.Point(89.612, 70.224, 0.0)
   VAnt_Polygon_GPSlot_4 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_4.Label = "GPSlot_4"
--

-- STEP 13: Create new subtraction
   VTmp_Subs = {}
   VTmp_Subs[1] = VAnt_Rectangle_GPSlot_0
   VTmp_Subs[2] = VAnt_Rectangle_GPSlot_1
   VTmp_Subs[3] = VAnt_Rectangle_GPSlot_2
   VTmp_Subs[4] = VAnt_Polygon_GPSlot_3
   VTmp_Subs[5] = VAnt_Polygon_GPSlot_4
   VAnt_Subtraction_GP_Slotted = VAnt_Geometry:Subtract(VAnt_Rectangle_GP, VTmp_Subs)
   VAnt_Subtraction_GP_Slotted.Label = "GP_Slotted"
--

-- STEP 14: Creating medium
   VAnt_Medium_FR4 = VAnt_Project.Media:AddDielectric()
   VAnt_Medium_FR4.Label = "FR4"
   VAnt_Medium_FR4.DielectricModelling.RelativePermittivity = 4.4
   VAnt_Medium_FR4.DielectricModelling.LossTangent = 0.02
--

-- STEP 15: Create new solid.cuboid
   VTmp_Corner = cf.Point(0.066, 0.819, 0.0)
   VAnt_Cuboid_Substrate = VAnt_Geometry:AddCuboid(VTmp_Corner, 76.572, 98.246, 1.6)
   VAnt_Cuboid_Substrate.Label = "Substrate"
--

-- STEP 16: Set solid medium
   VAnt_Cuboid_Substrate.Regions:Item(1).Medium = VAnt_Project.Media:Item("FR4")
--

-- STEP 17: Create new rectangular surface
   VTmp_Corner = cf.Point(5.503, 4.835, 1.6)
   VAnt_Rectangle_RP = VAnt_Geometry:AddRectangle(VTmp_Corner, 69.552, 93.32)
   VAnt_Rectangle_RP.Label = "RP"
--

-- STEP 18: Create new rectangular surface
   VTmp_Corner = cf.Point(45.167, 78.343, 1.6)
   VAnt_Rectangle_GPSlot_0 = VAnt_Geometry:AddRectangle(VTmp_Corner, 1.501, 1.985)
   VAnt_Rectangle_GPSlot_0.Label = "GPSlot_0"
--

-- STEP 19: Create new rectangular surface
   VTmp_Corner = cf.Point(23.108, 2.278, 1.6)
   VAnt_Rectangle_GPSlot_1 = VAnt_Geometry:AddRectangle(VTmp_Corner, 0.998, 2.664)
   VAnt_Rectangle_GPSlot_1.Label = "GPSlot_1"
--

-- STEP 20: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(60.389, 21.44, 1.6)
   VTmp_Points[2] = cf.Point(58.68, 27.196, 1.6)
   VTmp_Points[3] = cf.Point(62.106, 18.493, 1.6)
   VAnt_Polygon_GPSlot_2 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_2.Label = "GPSlot_2"
--

-- STEP 21: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(48.654, 11.264, 1.6)
   VTmp_Points[2] = cf.Point(44.86, 12.619, 1.6)
   VTmp_Points[3] = cf.Point(47.762, 12.678, 1.6)
   VAnt_Polygon_GPSlot_3 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_3.Label = "GPSlot_3"
--

-- STEP 22: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(59.586, 9.506, 1.6)
   VTmp_Points[2] = cf.Point(60.394, 5.539, 1.6)
   VTmp_Points[3] = cf.Point(62.719, 6.854, 1.6)
   VAnt_Polygon_GPSlot_4 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_4.Label = "GPSlot_4"
--

-- STEP 23: Create new subtraction
   VTmp_Subs = {}
   VTmp_Subs[1] = VAnt_Rectangle_GPSlot_0
   VTmp_Subs[2] = VAnt_Rectangle_GPSlot_1
   VTmp_Subs[3] = VAnt_Polygon_GPSlot_2
   VTmp_Subs[4] = VAnt_Polygon_GPSlot_3
   VTmp_Subs[5] = VAnt_Polygon_GPSlot_4
   VAnt_Subtraction_RP_Slotted = VAnt_Geometry:Subtract(VAnt_Rectangle_RP, VTmp_Subs)
   VAnt_Subtraction_RP_Slotted.Label = "RP_Slotted"
--

-- STEP 24: Create new union
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

-- STEP 25: Changing face medium
   VAnt_Union_Onion.Faces:Item("Face23").Medium = VAnt_Project.Media:Item("Perfect electric conductor")
--

-- STEP 26: Changing face medium
   VAnt_Union_Onion.Faces:Item("Face24").Medium = VAnt_Project.Media:Item("Perfect electric conductor")
--

-- STEP 27: Changing face medium
   VAnt_Union_Onion.Faces:Item("Face25").Medium = VAnt_Project.Media:Item("Perfect electric conductor")
--

-- STEP 28: Create new edge port
   VTmp_Pos = {}
   VTmp_Neg = {}
   VTmp_Pos[1] = VAnt_Union_Onion.Faces:Item("Face2")
   VTmp_Neg[1] = VAnt_Union_Onion.Faces:Item("Face3")
   VAnt_EPort_SourcePort = VAnt_Project.Ports:AddEdgePort(VTmp_Pos, VTmp_Neg)
   VAnt_EPort_SourcePort.Label = "SourcePort"
--

-- STEP 29: Get config file
   VAnt_Config = VAnt_Project.SolutionConfigurations[1]
--

-- STEP 30: Create new voltage source
   VAnt_VSource_VoltageSource = VAnt_Config.Sources:AddVoltageSource(VAnt_EPort_SourcePort)
   VAnt_VSource_VoltageSource.Impedance = 50.0
   VAnt_VSource_VoltageSource.Magnitude = 1.0
   VAnt_VSource_VoltageSource.Phase = 0.0
   VAnt_VSource_VoltageSource.Label = "VoltageSource"
--

-- STEP 31: Create new Far-Field request
   VAnt_Config.FarFields:Add(0.0, 0.0, 180.0, 360.0, 5.0, 5.0)
--
-- STEP 32: Set frequency range
   VAnt_tmp = VAnt_Config.Frequency:GetProperties()
   VAnt_tmp.Start  = 906500000.0
   VAnt_tmp.End    = 933500000.0
   VAnt_tmp.RangeType  = cf.Enums.FrequencyRangeTypeEnum.LinearSpacedDiscrete
   VAnt_tmp.NumberOfDiscreteValues = 2
   VAnt_Config.Frequency:SetProperties(VAnt_tmp)
--

-- STEP 33: Mesh the project
   VAnt_Project.Mesher.Settings.WireRadius = 0.001
   VAnt_Project.Mesher.Settings.MeshSizeOption = cf.Enums.MeshSizeOptionEnum.Coarse
   VAnt_Project.Mesher:Mesh()
--

-- STEP 34: Save project
   VSes_Application:SaveAs("C:/Users/project/0. My Work/1. Repositories/1. Very Unfriendly Train/Data/Simulations/637072110041561472_Primary/637072123817201280_6/6.cfx")
--

-- STEP 35: Run simulation
   VAnt_Project.Launcher.Settings.FEKO.Parallel.Enabled = true
   VAnt_Project.Launcher:RunFEKO()
--

-- STEP 36: Close project
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
   VTmp_Points[1] = cf.Point(75.078, 46.311, 1.6)
   VTmp_Points[2] = cf.Point(75.078, 48.277, 1.6)
   VTmp_Points[3] = cf.Point(78.663, 48.277, 1.6)
   VTmp_Points[4] = cf.Point(78.663, 46.311, 1.6)
   VAnt_Polygon_Feed_Top = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_Feed_Top.Label = "Feed_Top"
--

-- STEP 4: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(78.663, 48.277, 1.6)
   VTmp_Points[2] = cf.Point(78.663, 48.277, 0.8)
   VTmp_Points[3] = cf.Point(78.663, 46.311, 0.8)
   VTmp_Points[4] = cf.Point(78.663, 46.311, 1.6)
   VAnt_Polygon_Feed_Pos = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_Feed_Pos.Label = "Feed_Pos"
--

-- STEP 5: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(78.663, 48.277, 0.0)
   VTmp_Points[2] = cf.Point(78.663, 48.277, 0.8)
   VTmp_Points[3] = cf.Point(78.663, 46.311, 0.8)
   VTmp_Points[4] = cf.Point(78.663, 46.311, 0.0)
   VAnt_Polygon_Feed_Neg = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_Feed_Neg.Label = "Feed_Neg"
--

-- STEP 6: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(78.663, 46.311, 0.0)
   VTmp_Points[2] = cf.Point(78.663, 48.277, 0.0)
   VTmp_Points[3] = cf.Point(77.063, 48.277, 0.0)
   VTmp_Points[4] = cf.Point(77.063, 46.311, 0.0)
   VAnt_Polygon_Feed_Bot = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_Feed_Bot.Label = "Feed_Bot"
--

-- STEP 7: Create new rectangular surface
   VTmp_Corner = cf.Point(-0.297, 0.54, 0.0)
   VAnt_Rectangle_GP = VAnt_Geometry:AddRectangle(VTmp_Corner, 77.36, 96.657)
   VAnt_Rectangle_GP.Label = "GP"
--

-- STEP 8: Create new rectangular surface
   VTmp_Corner = cf.Point(37.173, 2.606, 0.0)
   VAnt_Rectangle_GPSlot_0 = VAnt_Geometry:AddRectangle(VTmp_Corner, 16.547, 14.401)
   VAnt_Rectangle_GPSlot_0.Label = "GPSlot_0"
--

-- STEP 9: Create new rectangular surface
   VTmp_Corner = cf.Point(50.731, 17.318, 0.0)
   VAnt_Rectangle_GPSlot_1 = VAnt_Geometry:AddRectangle(VTmp_Corner, 5.197, 3.154)
   VAnt_Rectangle_GPSlot_1.Label = "GPSlot_1"
--

-- STEP 10: Create new rectangular surface
   VTmp_Corner = cf.Point(61.405, 21.988, 0.0)
   VAnt_Rectangle_GPSlot_2 = VAnt_Geometry:AddRectangle(VTmp_Corner, 24.44, 4.767)
   VAnt_Rectangle_GPSlot_2.Label = "GPSlot_2"
--

-- STEP 11: Create new rectangular surface
   VTmp_Corner = cf.Point(58.208, 1.432, 0.0)
   VAnt_Rectangle_GPSlot_3 = VAnt_Geometry:AddRectangle(VTmp_Corner, 5.732, 0.378)
   VAnt_Rectangle_GPSlot_3.Label = "GPSlot_3"
--

-- STEP 12: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(26.759, 2.429, 0.0)
   VTmp_Points[2] = cf.Point(36.543, 13.389, 0.0)
   VTmp_Points[3] = cf.Point(22.992, -0.771, 0.0)
   VAnt_Polygon_GPSlot_4 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_4.Label = "GPSlot_4"
--

-- STEP 13: Create new subtraction
   VTmp_Subs = {}
   VTmp_Subs[1] = VAnt_Rectangle_GPSlot_0
   VTmp_Subs[2] = VAnt_Rectangle_GPSlot_1
   VTmp_Subs[3] = VAnt_Rectangle_GPSlot_2
   VTmp_Subs[4] = VAnt_Rectangle_GPSlot_3
   VTmp_Subs[5] = VAnt_Polygon_GPSlot_4
   VAnt_Subtraction_GP_Slotted = VAnt_Geometry:Subtract(VAnt_Rectangle_GP, VTmp_Subs)
   VAnt_Subtraction_GP_Slotted.Label = "GP_Slotted"
--

-- STEP 14: Creating medium
   VAnt_Medium_FR4 = VAnt_Project.Media:AddDielectric()
   VAnt_Medium_FR4.Label = "FR4"
   VAnt_Medium_FR4.DielectricModelling.RelativePermittivity = 4.4
   VAnt_Medium_FR4.DielectricModelling.LossTangent = 0.02
--

-- STEP 15: Create new solid.cuboid
   VTmp_Corner = cf.Point(-0.297, 0.54, 0.0)
   VAnt_Cuboid_Substrate = VAnt_Geometry:AddCuboid(VTmp_Corner, 77.36, 98.68799999999999, 1.6)
   VAnt_Cuboid_Substrate.Label = "Substrate"
--

-- STEP 16: Set solid medium
   VAnt_Cuboid_Substrate.Regions:Item(1).Medium = VAnt_Project.Media:Item("FR4")
--

-- STEP 17: Create new rectangular surface
   VTmp_Corner = cf.Point(5.051, 4.696, 1.6)
   VAnt_Rectangle_RP = VAnt_Geometry:AddRectangle(VTmp_Corner, 70.027, 94.482)
   VAnt_Rectangle_RP.Label = "RP"
--

-- STEP 18: Create new rectangular surface
   VTmp_Corner = cf.Point(42.855, 77.764, 1.6)
   VAnt_Rectangle_GPSlot_0 = VAnt_Geometry:AddRectangle(VTmp_Corner, 2.987, 2.524)
   VAnt_Rectangle_GPSlot_0.Label = "GPSlot_0"
--

-- STEP 19: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(60.887, 21.949, 1.6)
   VTmp_Points[2] = cf.Point(58.3, 25.748, 1.6)
   VTmp_Points[3] = cf.Point(62.71, 18.42, 1.6)
   VAnt_Polygon_GPSlot_1 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_1.Label = "GPSlot_1"
--

-- STEP 20: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(47.283, 13.158, 1.6)
   VTmp_Points[2] = cf.Point(45.503, 11.684, 1.6)
   VTmp_Points[3] = cf.Point(44.185, 14.309, 1.6)
   VAnt_Polygon_GPSlot_2 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_2.Label = "GPSlot_2"
--

-- STEP 21: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(59.813, 8.406, 1.6)
   VTmp_Points[2] = cf.Point(60.91, 6.073, 1.6)
   VTmp_Points[3] = cf.Point(64.246, 7.734, 1.6)
   VAnt_Polygon_GPSlot_3 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_3.Label = "GPSlot_3"
--

-- STEP 22: Create new subtraction
   VTmp_Subs = {}
   VTmp_Subs[1] = VAnt_Rectangle_GPSlot_0
   VTmp_Subs[2] = VAnt_Polygon_GPSlot_1
   VTmp_Subs[3] = VAnt_Polygon_GPSlot_2
   VTmp_Subs[4] = VAnt_Polygon_GPSlot_3
   VAnt_Subtraction_RP_Slotted = VAnt_Geometry:Subtract(VAnt_Rectangle_RP, VTmp_Subs)
   VAnt_Subtraction_RP_Slotted.Label = "RP_Slotted"
--

-- STEP 23: Create new union
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

-- STEP 24: Changing face medium
   VAnt_Union_Onion.Faces:Item("Face22").Medium = VAnt_Project.Media:Item("Perfect electric conductor")
--

-- STEP 25: Changing face medium
   VAnt_Union_Onion.Faces:Item("Face23").Medium = VAnt_Project.Media:Item("Perfect electric conductor")
--

-- STEP 26: Changing face medium
   VAnt_Union_Onion.Faces:Item("Face24").Medium = VAnt_Project.Media:Item("Perfect electric conductor")
--

-- STEP 27: Create new edge port
   VTmp_Pos = {}
   VTmp_Neg = {}
   VTmp_Pos[1] = VAnt_Union_Onion.Faces:Item("Face2")
   VTmp_Neg[1] = VAnt_Union_Onion.Faces:Item("Face3")
   VAnt_EPort_SourcePort = VAnt_Project.Ports:AddEdgePort(VTmp_Pos, VTmp_Neg)
   VAnt_EPort_SourcePort.Label = "SourcePort"
--

-- STEP 28: Get config file
   VAnt_Config = VAnt_Project.SolutionConfigurations[1]
--

-- STEP 29: Create new voltage source
   VAnt_VSource_VoltageSource = VAnt_Config.Sources:AddVoltageSource(VAnt_EPort_SourcePort)
   VAnt_VSource_VoltageSource.Impedance = 50.0
   VAnt_VSource_VoltageSource.Magnitude = 1.0
   VAnt_VSource_VoltageSource.Phase = 0.0
   VAnt_VSource_VoltageSource.Label = "VoltageSource"
--

-- STEP 30: Create new Far-Field request
   VAnt_Config.FarFields:Add(0.0, 0.0, 180.0, 360.0, 5.0, 5.0)
--
-- STEP 31: Set frequency range
   VAnt_tmp = VAnt_Config.Frequency:GetProperties()
   VAnt_tmp.Start  = 906500000.0
   VAnt_tmp.End    = 933500000.0
   VAnt_tmp.RangeType  = cf.Enums.FrequencyRangeTypeEnum.LinearSpacedDiscrete
   VAnt_tmp.NumberOfDiscreteValues = 2
   VAnt_Config.Frequency:SetProperties(VAnt_tmp)
--

-- STEP 32: Mesh the project
   VAnt_Project.Mesher.Settings.WireRadius = 0.001
   VAnt_Project.Mesher.Settings.MeshSizeOption = cf.Enums.MeshSizeOptionEnum.Coarse
   VAnt_Project.Mesher:Mesh()
--

-- STEP 33: Save project
   VSes_Application:SaveAs("C:/Users/project/0. My Work/1. Repositories/1. Very Unfriendly Train/Data/Simulations/637072110041561472_Primary/637072123817201280_7/7.cfx")
--

-- STEP 34: Run simulation
   VAnt_Project.Launcher.Settings.FEKO.Parallel.Enabled = true
   VAnt_Project.Launcher:RunFEKO()
--

-- STEP 35: Close project
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
   VTmp_Points[1] = cf.Point(77.0, 46.680499999999995, 1.6)
   VTmp_Points[2] = cf.Point(77.0, 48.66349999999999, 1.6)
   VTmp_Points[3] = cf.Point(78.64999999999999, 48.66349999999999, 1.6)
   VTmp_Points[4] = cf.Point(78.64999999999999, 46.680499999999995, 1.6)
   VAnt_Polygon_Feed_Top = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_Feed_Top.Label = "Feed_Top"
--

-- STEP 4: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(78.64999999999999, 48.66349999999999, 1.6)
   VTmp_Points[2] = cf.Point(78.64999999999999, 48.66349999999999, 0.8)
   VTmp_Points[3] = cf.Point(78.64999999999999, 46.680499999999995, 0.8)
   VTmp_Points[4] = cf.Point(78.64999999999999, 46.680499999999995, 1.6)
   VAnt_Polygon_Feed_Pos = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_Feed_Pos.Label = "Feed_Pos"
--

-- STEP 5: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(78.64999999999999, 48.66349999999999, 0.0)
   VTmp_Points[2] = cf.Point(78.64999999999999, 48.66349999999999, 0.8)
   VTmp_Points[3] = cf.Point(78.64999999999999, 46.680499999999995, 0.8)
   VTmp_Points[4] = cf.Point(78.64999999999999, 46.680499999999995, 0.0)
   VAnt_Polygon_Feed_Neg = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_Feed_Neg.Label = "Feed_Neg"
--

-- STEP 6: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(78.64999999999999, 46.680499999999995, 0.0)
   VTmp_Points[2] = cf.Point(78.64999999999999, 48.66349999999999, 0.0)
   VTmp_Points[3] = cf.Point(77.05, 48.66349999999999, 0.0)
   VTmp_Points[4] = cf.Point(77.05, 46.680499999999995, 0.0)
   VAnt_Polygon_Feed_Bot = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_Feed_Bot.Label = "Feed_Bot"
--

-- STEP 7: Create new rectangular surface
   VTmp_Corner = cf.Point(0.139, 0.384, 0.0)
   VAnt_Rectangle_GP = VAnt_Geometry:AddRectangle(VTmp_Corner, 76.911, 97.9)
   VAnt_Rectangle_GP.Label = "GP"
--

-- STEP 8: Create new rectangular surface
   VTmp_Corner = cf.Point(39.695, 5.486, 0.0)
   VAnt_Rectangle_GPSlot_0 = VAnt_Geometry:AddRectangle(VTmp_Corner, 21.523, 9.583)
   VAnt_Rectangle_GPSlot_0.Label = "GPSlot_0"
--

-- STEP 9: Create new rectangular surface
   VTmp_Corner = cf.Point(42.77, 15.374, 0.0)
   VAnt_Rectangle_GPSlot_1 = VAnt_Geometry:AddRectangle(VTmp_Corner, 1.766, 1.993)
   VAnt_Rectangle_GPSlot_1.Label = "GPSlot_1"
--

-- STEP 10: Create new rectangular surface
   VTmp_Corner = cf.Point(56.785, 26.227, 0.0)
   VAnt_Rectangle_GPSlot_2 = VAnt_Geometry:AddRectangle(VTmp_Corner, 28.936, 7.074)
   VAnt_Rectangle_GPSlot_2.Label = "GPSlot_2"
--

-- STEP 11: Create new rectangular surface
   VTmp_Corner = cf.Point(3.862, 32.161, 0.0)
   VAnt_Rectangle_GPSlot_3 = VAnt_Geometry:AddRectangle(VTmp_Corner, 9.782, 37.414)
   VAnt_Rectangle_GPSlot_3.Label = "GPSlot_3"
--

-- STEP 12: Create new subtraction
   VTmp_Subs = {}
   VTmp_Subs[1] = VAnt_Rectangle_GPSlot_0
   VTmp_Subs[2] = VAnt_Rectangle_GPSlot_1
   VTmp_Subs[3] = VAnt_Rectangle_GPSlot_2
   VTmp_Subs[4] = VAnt_Rectangle_GPSlot_3
   VAnt_Subtraction_GP_Slotted = VAnt_Geometry:Subtract(VAnt_Rectangle_GP, VTmp_Subs)
   VAnt_Subtraction_GP_Slotted.Label = "GP_Slotted"
--

-- STEP 13: Creating medium
   VAnt_Medium_FR4 = VAnt_Project.Media:AddDielectric()
   VAnt_Medium_FR4.Label = "FR4"
   VAnt_Medium_FR4.DielectricModelling.RelativePermittivity = 4.4
   VAnt_Medium_FR4.DielectricModelling.LossTangent = 0.02
--

-- STEP 14: Create new solid.cuboid
   VTmp_Corner = cf.Point(0.139, 0.384, 0.0)
   VAnt_Cuboid_Substrate = VAnt_Geometry:AddCuboid(VTmp_Corner, 76.911, 99.81700000000001, 1.6)
   VAnt_Cuboid_Substrate.Label = "Substrate"
--

-- STEP 15: Set solid medium
   VAnt_Cuboid_Substrate.Regions:Item(1).Medium = VAnt_Project.Media:Item("FR4")
--

-- STEP 16: Create new rectangular surface
   VTmp_Corner = cf.Point(5.575, 3.989, 1.6)
   VAnt_Rectangle_RP = VAnt_Geometry:AddRectangle(VTmp_Corner, 71.425, 96.162)
   VAnt_Rectangle_RP.Label = "RP"
--

-- STEP 17: Create new rectangular surface
   VTmp_Corner = cf.Point(45.635, 76.855, 1.6)
   VAnt_Rectangle_GPSlot_0 = VAnt_Geometry:AddRectangle(VTmp_Corner, 5.274, 2.177)
   VAnt_Rectangle_GPSlot_0.Label = "GPSlot_0"
--

-- STEP 18: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(59.305, 22.192, 1.6)
   VTmp_Points[2] = cf.Point(57.997, 25.044, 1.6)
   VTmp_Points[3] = cf.Point(59.587, 17.94, 1.6)
   VAnt_Polygon_GPSlot_1 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_1.Label = "GPSlot_1"
--

-- STEP 19: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(47.686, 8.284, 1.6)
   VTmp_Points[2] = cf.Point(45.205, 10.146, 1.6)
   VTmp_Points[3] = cf.Point(47.037, 14.76, 1.6)
   VAnt_Polygon_GPSlot_2 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_2.Label = "GPSlot_2"
--

-- STEP 20: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(61.905, 10.24, 1.6)
   VTmp_Points[2] = cf.Point(60.312, 6.409, 1.6)
   VTmp_Points[3] = cf.Point(62.072, 7.23, 1.6)
   VAnt_Polygon_GPSlot_3 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_3.Label = "GPSlot_3"
--

-- STEP 21: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(58.031, 32.562, 1.6)
   VTmp_Points[2] = cf.Point(57.678, 32.882, 1.6)
   VTmp_Points[3] = cf.Point(58.887, 31.604, 1.6)
   VAnt_Polygon_GPSlot_4 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_4.Label = "GPSlot_4"
--

-- STEP 22: Create new subtraction
   VTmp_Subs = {}
   VTmp_Subs[1] = VAnt_Rectangle_GPSlot_0
   VTmp_Subs[2] = VAnt_Polygon_GPSlot_1
   VTmp_Subs[3] = VAnt_Polygon_GPSlot_2
   VTmp_Subs[4] = VAnt_Polygon_GPSlot_3
   VTmp_Subs[5] = VAnt_Polygon_GPSlot_4
   VAnt_Subtraction_RP_Slotted = VAnt_Geometry:Subtract(VAnt_Rectangle_RP, VTmp_Subs)
   VAnt_Subtraction_RP_Slotted.Label = "RP_Slotted"
--

-- STEP 23: Create new union
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

-- STEP 24: Changing face medium
   VAnt_Union_Onion.Faces:Item("Face22").Medium = VAnt_Project.Media:Item("Perfect electric conductor")
--

-- STEP 25: Changing face medium
   VAnt_Union_Onion.Faces:Item("Face23").Medium = VAnt_Project.Media:Item("Perfect electric conductor")
--

-- STEP 26: Changing face medium
   VAnt_Union_Onion.Faces:Item("Face24").Medium = VAnt_Project.Media:Item("Perfect electric conductor")
--

-- STEP 27: Create new edge port
   VTmp_Pos = {}
   VTmp_Neg = {}
   VTmp_Pos[1] = VAnt_Union_Onion.Faces:Item("Face2")
   VTmp_Neg[1] = VAnt_Union_Onion.Faces:Item("Face3")
   VAnt_EPort_SourcePort = VAnt_Project.Ports:AddEdgePort(VTmp_Pos, VTmp_Neg)
   VAnt_EPort_SourcePort.Label = "SourcePort"
--

-- STEP 28: Get config file
   VAnt_Config = VAnt_Project.SolutionConfigurations[1]
--

-- STEP 29: Create new voltage source
   VAnt_VSource_VoltageSource = VAnt_Config.Sources:AddVoltageSource(VAnt_EPort_SourcePort)
   VAnt_VSource_VoltageSource.Impedance = 50.0
   VAnt_VSource_VoltageSource.Magnitude = 1.0
   VAnt_VSource_VoltageSource.Phase = 0.0
   VAnt_VSource_VoltageSource.Label = "VoltageSource"
--

-- STEP 30: Create new Far-Field request
   VAnt_Config.FarFields:Add(0.0, 0.0, 180.0, 360.0, 5.0, 5.0)
--
-- STEP 31: Set frequency range
   VAnt_tmp = VAnt_Config.Frequency:GetProperties()
   VAnt_tmp.Start  = 906500000.0
   VAnt_tmp.End    = 933500000.0
   VAnt_tmp.RangeType  = cf.Enums.FrequencyRangeTypeEnum.LinearSpacedDiscrete
   VAnt_tmp.NumberOfDiscreteValues = 2
   VAnt_Config.Frequency:SetProperties(VAnt_tmp)
--

-- STEP 32: Mesh the project
   VAnt_Project.Mesher.Settings.WireRadius = 0.001
   VAnt_Project.Mesher.Settings.MeshSizeOption = cf.Enums.MeshSizeOptionEnum.Coarse
   VAnt_Project.Mesher:Mesh()
--

-- STEP 33: Save project
   VSes_Application:SaveAs("C:/Users/project/0. My Work/1. Repositories/1. Very Unfriendly Train/Data/Simulations/637072110041561472_Primary/637072123817201280_8/8.cfx")
--

-- STEP 34: Run simulation
   VAnt_Project.Launcher.Settings.FEKO.Parallel.Enabled = true
   VAnt_Project.Launcher:RunFEKO()
--

-- STEP 35: Close project
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
   VTmp_Points[1] = cf.Point(75.035, 47.3495, 1.6)
   VTmp_Points[2] = cf.Point(75.035, 49.320499999999996, 1.6)
   VTmp_Points[3] = cf.Point(76.68499999999999, 49.320499999999996, 1.6)
   VTmp_Points[4] = cf.Point(76.68499999999999, 47.3495, 1.6)
   VAnt_Polygon_Feed_Top = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_Feed_Top.Label = "Feed_Top"
--

-- STEP 4: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(76.68499999999999, 49.320499999999996, 1.6)
   VTmp_Points[2] = cf.Point(76.68499999999999, 49.320499999999996, 0.8)
   VTmp_Points[3] = cf.Point(76.68499999999999, 47.3495, 0.8)
   VTmp_Points[4] = cf.Point(76.68499999999999, 47.3495, 1.6)
   VAnt_Polygon_Feed_Pos = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_Feed_Pos.Label = "Feed_Pos"
--

-- STEP 5: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(76.68499999999999, 49.320499999999996, 0.0)
   VTmp_Points[2] = cf.Point(76.68499999999999, 49.320499999999996, 0.8)
   VTmp_Points[3] = cf.Point(76.68499999999999, 47.3495, 0.8)
   VTmp_Points[4] = cf.Point(76.68499999999999, 47.3495, 0.0)
   VAnt_Polygon_Feed_Neg = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_Feed_Neg.Label = "Feed_Neg"
--

-- STEP 6: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(76.68499999999999, 47.3495, 0.0)
   VTmp_Points[2] = cf.Point(76.68499999999999, 49.320499999999996, 0.0)
   VTmp_Points[3] = cf.Point(75.085, 49.320499999999996, 0.0)
   VTmp_Points[4] = cf.Point(75.085, 47.3495, 0.0)
   VAnt_Polygon_Feed_Bot = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_Feed_Bot.Label = "Feed_Bot"
--

-- STEP 7: Create new rectangular surface
   VTmp_Corner = cf.Point(-0.27, 0.02, 0.0)
   VAnt_Rectangle_GP = VAnt_Geometry:AddRectangle(VTmp_Corner, 75.35499999999999, 99.375)
   VAnt_Rectangle_GP.Label = "GP"
--

-- STEP 8: Create new rectangular surface
   VTmp_Corner = cf.Point(44.95, 17.626, 0.0)
   VAnt_Rectangle_GPSlot_0 = VAnt_Geometry:AddRectangle(VTmp_Corner, 2.314, 1.486)
   VAnt_Rectangle_GPSlot_0.Label = "GPSlot_0"
--

-- STEP 9: Create new rectangular surface
   VTmp_Corner = cf.Point(55.551, 23.805, 0.0)
   VAnt_Rectangle_GPSlot_1 = VAnt_Geometry:AddRectangle(VTmp_Corner, 26.645, 0.89)
   VAnt_Rectangle_GPSlot_1.Label = "GPSlot_1"
--

-- STEP 10: Create new rectangular surface
   VTmp_Corner = cf.Point(28.03, 37.023, 0.0)
   VAnt_Rectangle_GPSlot_2 = VAnt_Geometry:AddRectangle(VTmp_Corner, 15.203, 19.197)
   VAnt_Rectangle_GPSlot_2.Label = "GPSlot_2"
--

-- STEP 11: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(28.405, 1.37, 0.0)
   VTmp_Points[2] = cf.Point(36.266, 15.476, 0.0)
   VTmp_Points[3] = cf.Point(23.999, -4.599, 0.0)
   VAnt_Polygon_GPSlot_3 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_3.Label = "GPSlot_3"
--

-- STEP 12: Create new subtraction
   VTmp_Subs = {}
   VTmp_Subs[1] = VAnt_Rectangle_GPSlot_0
   VTmp_Subs[2] = VAnt_Rectangle_GPSlot_1
   VTmp_Subs[3] = VAnt_Rectangle_GPSlot_2
   VTmp_Subs[4] = VAnt_Polygon_GPSlot_3
   VAnt_Subtraction_GP_Slotted = VAnt_Geometry:Subtract(VAnt_Rectangle_GP, VTmp_Subs)
   VAnt_Subtraction_GP_Slotted.Label = "GP_Slotted"
--

-- STEP 13: Creating medium
   VAnt_Medium_FR4 = VAnt_Project.Media:AddDielectric()
   VAnt_Medium_FR4.Label = "FR4"
   VAnt_Medium_FR4.DielectricModelling.RelativePermittivity = 4.4
   VAnt_Medium_FR4.DielectricModelling.LossTangent = 0.02
--

-- STEP 14: Create new solid.cuboid
   VTmp_Corner = cf.Point(-0.27, 0.02, 0.0)
   VAnt_Cuboid_Substrate = VAnt_Geometry:AddCuboid(VTmp_Corner, 75.35499999999999, 101.159, 1.6)
   VAnt_Cuboid_Substrate.Label = "Substrate"
--

-- STEP 15: Set solid medium
   VAnt_Cuboid_Substrate.Regions:Item(1).Medium = VAnt_Project.Media:Item("FR4")
--

-- STEP 16: Create new rectangular surface
   VTmp_Corner = cf.Point(6.139, 4.292, 1.6)
   VAnt_Rectangle_RP = VAnt_Geometry:AddRectangle(VTmp_Corner, 68.896, 96.837)
   VAnt_Rectangle_RP.Label = "RP"
--

-- STEP 17: Create new rectangular surface
   VTmp_Corner = cf.Point(44.772, 77.56, 1.6)
   VAnt_Rectangle_GPSlot_0 = VAnt_Geometry:AddRectangle(VTmp_Corner, 5.658, 1.037)
   VAnt_Rectangle_GPSlot_0.Label = "GPSlot_0"
--

-- STEP 18: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(60.949, 21.442, 1.6)
   VTmp_Points[2] = cf.Point(59.114, 26.562, 1.6)
   VTmp_Points[3] = cf.Point(61.364, 17.27, 1.6)
   VAnt_Polygon_GPSlot_1 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_1.Label = "GPSlot_1"
--

-- STEP 19: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(48.131, 13.136, 1.6)
   VTmp_Points[2] = cf.Point(48.192, 12.94, 1.6)
   VTmp_Points[3] = cf.Point(45.661, 12.792, 1.6)
   VAnt_Polygon_GPSlot_2 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_2.Label = "GPSlot_2"
--

-- STEP 20: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(60.314, 8.92, 1.6)
   VTmp_Points[2] = cf.Point(61.155, 7.331, 1.6)
   VTmp_Points[3] = cf.Point(61.527, 7.66, 1.6)
   VAnt_Polygon_GPSlot_3 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_3.Label = "GPSlot_3"
--

-- STEP 21: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(40.02, 50.874, 1.6)
   VTmp_Points[2] = cf.Point(40.749, 51.289, 1.6)
   VTmp_Points[3] = cf.Point(40.829, 50.695, 1.6)
   VAnt_Polygon_GPSlot_4 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_4.Label = "GPSlot_4"
--

-- STEP 22: Create new subtraction
   VTmp_Subs = {}
   VTmp_Subs[1] = VAnt_Rectangle_GPSlot_0
   VTmp_Subs[2] = VAnt_Polygon_GPSlot_1
   VTmp_Subs[3] = VAnt_Polygon_GPSlot_2
   VTmp_Subs[4] = VAnt_Polygon_GPSlot_3
   VTmp_Subs[5] = VAnt_Polygon_GPSlot_4
   VAnt_Subtraction_RP_Slotted = VAnt_Geometry:Subtract(VAnt_Rectangle_RP, VTmp_Subs)
   VAnt_Subtraction_RP_Slotted.Label = "RP_Slotted"
--

-- STEP 23: Create new union
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

-- STEP 24: Changing face medium
   VAnt_Union_Onion.Faces:Item("Face22").Medium = VAnt_Project.Media:Item("Perfect electric conductor")
--

-- STEP 25: Changing face medium
   VAnt_Union_Onion.Faces:Item("Face23").Medium = VAnt_Project.Media:Item("Perfect electric conductor")
--

-- STEP 26: Changing face medium
   VAnt_Union_Onion.Faces:Item("Face24").Medium = VAnt_Project.Media:Item("Perfect electric conductor")
--

-- STEP 27: Create new edge port
   VTmp_Pos = {}
   VTmp_Neg = {}
   VTmp_Pos[1] = VAnt_Union_Onion.Faces:Item("Face2")
   VTmp_Neg[1] = VAnt_Union_Onion.Faces:Item("Face3")
   VAnt_EPort_SourcePort = VAnt_Project.Ports:AddEdgePort(VTmp_Pos, VTmp_Neg)
   VAnt_EPort_SourcePort.Label = "SourcePort"
--

-- STEP 28: Get config file
   VAnt_Config = VAnt_Project.SolutionConfigurations[1]
--

-- STEP 29: Create new voltage source
   VAnt_VSource_VoltageSource = VAnt_Config.Sources:AddVoltageSource(VAnt_EPort_SourcePort)
   VAnt_VSource_VoltageSource.Impedance = 50.0
   VAnt_VSource_VoltageSource.Magnitude = 1.0
   VAnt_VSource_VoltageSource.Phase = 0.0
   VAnt_VSource_VoltageSource.Label = "VoltageSource"
--

-- STEP 30: Create new Far-Field request
   VAnt_Config.FarFields:Add(0.0, 0.0, 180.0, 360.0, 5.0, 5.0)
--
-- STEP 31: Set frequency range
   VAnt_tmp = VAnt_Config.Frequency:GetProperties()
   VAnt_tmp.Start  = 906500000.0
   VAnt_tmp.End    = 933500000.0
   VAnt_tmp.RangeType  = cf.Enums.FrequencyRangeTypeEnum.LinearSpacedDiscrete
   VAnt_tmp.NumberOfDiscreteValues = 2
   VAnt_Config.Frequency:SetProperties(VAnt_tmp)
--

-- STEP 32: Mesh the project
   VAnt_Project.Mesher.Settings.WireRadius = 0.001
   VAnt_Project.Mesher.Settings.MeshSizeOption = cf.Enums.MeshSizeOptionEnum.Coarse
   VAnt_Project.Mesher:Mesh()
--

-- STEP 33: Save project
   VSes_Application:SaveAs("C:/Users/project/0. My Work/1. Repositories/1. Very Unfriendly Train/Data/Simulations/637072110041561472_Primary/637072123817201280_9/9.cfx")
--

-- STEP 34: Run simulation
   VAnt_Project.Launcher.Settings.FEKO.Parallel.Enabled = true
   VAnt_Project.Launcher:RunFEKO()
--

-- STEP 35: Close project
   VSes_Application:CloseAllWindows()
--

-- STEP ??: Close file
   VSes_Application:CloseAllWindows()
   VSes_Application:Close()
--
