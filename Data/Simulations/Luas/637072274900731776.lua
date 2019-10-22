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
   VTmp_Points[1] = cf.Point(81.71900000000001, 52.3705, 1.6)
   VTmp_Points[2] = cf.Point(81.71900000000001, 54.0575, 1.6)
   VTmp_Points[3] = cf.Point(87.50599999999999, 54.0575, 1.6)
   VTmp_Points[4] = cf.Point(87.50599999999999, 52.3705, 1.6)
   VAnt_Polygon_Feed_Top = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_Feed_Top.Label = "Feed_Top"
--

-- STEP 4: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(87.50599999999999, 54.0575, 1.6)
   VTmp_Points[2] = cf.Point(87.50599999999999, 54.0575, 0.8)
   VTmp_Points[3] = cf.Point(87.50599999999999, 52.3705, 0.8)
   VTmp_Points[4] = cf.Point(87.50599999999999, 52.3705, 1.6)
   VAnt_Polygon_Feed_Pos = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_Feed_Pos.Label = "Feed_Pos"
--

-- STEP 5: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(87.50599999999999, 54.0575, 0.0)
   VTmp_Points[2] = cf.Point(87.50599999999999, 54.0575, 0.8)
   VTmp_Points[3] = cf.Point(87.50599999999999, 52.3705, 0.8)
   VTmp_Points[4] = cf.Point(87.50599999999999, 52.3705, 0.0)
   VAnt_Polygon_Feed_Neg = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_Feed_Neg.Label = "Feed_Neg"
--

-- STEP 6: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(87.50599999999999, 52.3705, 0.0)
   VTmp_Points[2] = cf.Point(87.50599999999999, 54.0575, 0.0)
   VTmp_Points[3] = cf.Point(85.90599999999999, 54.0575, 0.0)
   VTmp_Points[4] = cf.Point(85.90599999999999, 52.3705, 0.0)
   VAnt_Polygon_Feed_Bot = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_Feed_Bot.Label = "Feed_Bot"
--

-- STEP 7: Create new rectangular surface
   VTmp_Corner = cf.Point(-0.334, -0.238, 0.0)
   VAnt_Rectangle_GP = VAnt_Geometry:AddRectangle(VTmp_Corner, 86.24, 107.591)
   VAnt_Rectangle_GP.Label = "GP"
--

-- STEP 8: Create new rectangular surface
   VTmp_Corner = cf.Point(50.727, 42.226, 0.0)
   VAnt_Rectangle_GPSlot_0 = VAnt_Geometry:AddRectangle(VTmp_Corner, 13.301, 10.032)
   VAnt_Rectangle_GPSlot_0.Label = "GPSlot_0"
--

-- STEP 9: Create new subtraction
   VTmp_Subs = {}
   VTmp_Subs[1] = VAnt_Rectangle_GPSlot_0
   VAnt_Subtraction_GP_Slotted = VAnt_Geometry:Subtract(VAnt_Rectangle_GP, VTmp_Subs)
   VAnt_Subtraction_GP_Slotted.Label = "GP_Slotted"
--

-- STEP 10: Creating medium
   VAnt_Medium_FR4 = VAnt_Project.Media:AddDielectric()
   VAnt_Medium_FR4.Label = "FR4"
   VAnt_Medium_FR4.DielectricModelling.RelativePermittivity = 4.4
   VAnt_Medium_FR4.DielectricModelling.LossTangent = 0.02
--

-- STEP 11: Create new solid.cuboid
   VTmp_Corner = cf.Point(-0.334, -0.238, 0.0)
   VAnt_Cuboid_Substrate = VAnt_Geometry:AddCuboid(VTmp_Corner, 86.24, 107.591, 1.6)
   VAnt_Cuboid_Substrate.Label = "Substrate"
--

-- STEP 12: Set solid medium
   VAnt_Cuboid_Substrate.Regions:Item(1).Medium = VAnt_Project.Media:Item("FR4")
--

-- STEP 13: Create new rectangular surface
   VTmp_Corner = cf.Point(4.754, 4.898, 1.6)
   VAnt_Rectangle_RP = VAnt_Geometry:AddRectangle(VTmp_Corner, 76.965, 99.194)
   VAnt_Rectangle_RP.Label = "RP"
--

-- STEP 14: Create new union
   VTmp_Parts = {}
   VTmp_Parts[1] = VAnt_Subtraction_GP_Slotted
   VTmp_Parts[2] = VAnt_Rectangle_RP
   VTmp_Parts[3] = VAnt_Cuboid_Substrate
   VTmp_Parts[4] = VAnt_Polygon_Feed_Top
   VTmp_Parts[5] = VAnt_Polygon_Feed_Pos
   VTmp_Parts[6] = VAnt_Polygon_Feed_Neg
   VTmp_Parts[7] = VAnt_Polygon_Feed_Bot
   VAnt_Union_Onion = VAnt_Geometry:Union(VTmp_Parts)
   VAnt_Union_Onion.Label = "Onion"
--

-- STEP 15: Changing face medium
   VAnt_Union_Onion.Faces:Item("Face14").Medium = VAnt_Project.Media:Item("Perfect electric conductor")
--

-- STEP 16: Changing face medium
   VAnt_Union_Onion.Faces:Item("Face15").Medium = VAnt_Project.Media:Item("Perfect electric conductor")
--

-- STEP 17: Changing face medium
   VAnt_Union_Onion.Faces:Item("Face16").Medium = VAnt_Project.Media:Item("Perfect electric conductor")
--

-- STEP 18: Create new edge port
   VTmp_Pos = {}
   VTmp_Neg = {}
   VTmp_Pos[1] = VAnt_Union_Onion.Faces:Item("Face2")
   VTmp_Neg[1] = VAnt_Union_Onion.Faces:Item("Face3")
   VAnt_EPort_SourcePort = VAnt_Project.Ports:AddEdgePort(VTmp_Pos, VTmp_Neg)
   VAnt_EPort_SourcePort.Label = "SourcePort"
--

-- STEP 19: Get config file
   VAnt_Config = VAnt_Project.SolutionConfigurations[1]
--

-- STEP 20: Create new voltage source
   VAnt_VSource_VoltageSource = VAnt_Config.Sources:AddVoltageSource(VAnt_EPort_SourcePort)
   VAnt_VSource_VoltageSource.Impedance = 50.0
   VAnt_VSource_VoltageSource.Magnitude = 1.0
   VAnt_VSource_VoltageSource.Phase = 0.0
   VAnt_VSource_VoltageSource.Label = "VoltageSource"
--

-- STEP 21: Create new Far-Field request
   VAnt_Config.FarFields:Add(0.0, 0.0, 180.0, 360.0, 5.0, 5.0)
--
-- STEP 22: Set frequency range
   VAnt_tmp = VAnt_Config.Frequency:GetProperties()
   VAnt_tmp.Start  = 906500000.0
   VAnt_tmp.End    = 933500000.0
   VAnt_tmp.RangeType  = cf.Enums.FrequencyRangeTypeEnum.LinearSpacedDiscrete
   VAnt_tmp.NumberOfDiscreteValues = 2
   VAnt_Config.Frequency:SetProperties(VAnt_tmp)
--

-- STEP 23: Mesh the project
   VAnt_Project.Mesher.Settings.WireRadius = 0.001
   VAnt_Project.Mesher.Settings.MeshSizeOption = cf.Enums.MeshSizeOptionEnum.Coarse
   VAnt_Project.Mesher:Mesh()
--

-- STEP 24: Save project
   VSes_Application:SaveAs("C:/Users/project/0. My Work/1. Repositories/1. Very Unfriendly Train/Data/Simulations/637072274664755200_Primary/637072274900731776_0/0.cfx")
--

-- STEP 25: Run simulation
   VAnt_Project.Launcher.Settings.FEKO.Parallel.Enabled = true
   VAnt_Project.Launcher:RunFEKO()
--

-- STEP 26: Close project
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
   VTmp_Points[1] = cf.Point(83.16, 52.278, 1.6)
   VTmp_Points[2] = cf.Point(83.16, 53.897999999999996, 1.6)
   VTmp_Points[3] = cf.Point(89.31400000000001, 53.897999999999996, 1.6)
   VTmp_Points[4] = cf.Point(89.31400000000001, 52.278, 1.6)
   VAnt_Polygon_Feed_Top = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_Feed_Top.Label = "Feed_Top"
--

-- STEP 4: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(89.31400000000001, 53.897999999999996, 1.6)
   VTmp_Points[2] = cf.Point(89.31400000000001, 53.897999999999996, 0.8)
   VTmp_Points[3] = cf.Point(89.31400000000001, 52.278, 0.8)
   VTmp_Points[4] = cf.Point(89.31400000000001, 52.278, 1.6)
   VAnt_Polygon_Feed_Pos = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_Feed_Pos.Label = "Feed_Pos"
--

-- STEP 5: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(89.31400000000001, 53.897999999999996, 0.0)
   VTmp_Points[2] = cf.Point(89.31400000000001, 53.897999999999996, 0.8)
   VTmp_Points[3] = cf.Point(89.31400000000001, 52.278, 0.8)
   VTmp_Points[4] = cf.Point(89.31400000000001, 52.278, 0.0)
   VAnt_Polygon_Feed_Neg = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_Feed_Neg.Label = "Feed_Neg"
--

-- STEP 6: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(89.31400000000001, 52.278, 0.0)
   VTmp_Points[2] = cf.Point(89.31400000000001, 53.897999999999996, 0.0)
   VTmp_Points[3] = cf.Point(87.71400000000001, 53.897999999999996, 0.0)
   VTmp_Points[4] = cf.Point(87.71400000000001, 52.278, 0.0)
   VAnt_Polygon_Feed_Bot = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_Feed_Bot.Label = "Feed_Bot"
--

-- STEP 7: Create new rectangular surface
   VTmp_Corner = cf.Point(-0.189, 0.027, 0.0)
   VAnt_Rectangle_GP = VAnt_Geometry:AddRectangle(VTmp_Corner, 87.903, 107.505)
   VAnt_Rectangle_GP.Label = "GP"
--

-- STEP 8: Creating medium
   VAnt_Medium_FR4 = VAnt_Project.Media:AddDielectric()
   VAnt_Medium_FR4.Label = "FR4"
   VAnt_Medium_FR4.DielectricModelling.RelativePermittivity = 4.4
   VAnt_Medium_FR4.DielectricModelling.LossTangent = 0.02
--

-- STEP 9: Create new solid.cuboid
   VTmp_Corner = cf.Point(-0.189, 0.027, 0.0)
   VAnt_Cuboid_Substrate = VAnt_Geometry:AddCuboid(VTmp_Corner, 87.903, 107.505, 1.6)
   VAnt_Cuboid_Substrate.Label = "Substrate"
--

-- STEP 10: Set solid medium
   VAnt_Cuboid_Substrate.Regions:Item(1).Medium = VAnt_Project.Media:Item("FR4")
--

-- STEP 11: Create new rectangular surface
   VTmp_Corner = cf.Point(4.883, 4.446, 1.6)
   VAnt_Rectangle_RP = VAnt_Geometry:AddRectangle(VTmp_Corner, 78.277, 97.779)
   VAnt_Rectangle_RP.Label = "RP"
--

-- STEP 12: Create new union
   VTmp_Parts = {}
   VTmp_Parts[1] = VAnt_Rectangle_GP
   VTmp_Parts[2] = VAnt_Rectangle_RP
   VTmp_Parts[3] = VAnt_Cuboid_Substrate
   VTmp_Parts[4] = VAnt_Polygon_Feed_Top
   VTmp_Parts[5] = VAnt_Polygon_Feed_Pos
   VTmp_Parts[6] = VAnt_Polygon_Feed_Neg
   VTmp_Parts[7] = VAnt_Polygon_Feed_Bot
   VAnt_Union_Onion = VAnt_Geometry:Union(VTmp_Parts)
   VAnt_Union_Onion.Label = "Onion"
--

-- STEP 13: Changing face medium
   VAnt_Union_Onion.Faces:Item("Face13").Medium = VAnt_Project.Media:Item("Perfect electric conductor")
--

-- STEP 14: Changing face medium
   VAnt_Union_Onion.Faces:Item("Face14").Medium = VAnt_Project.Media:Item("Perfect electric conductor")
--

-- STEP 15: Changing face medium
   VAnt_Union_Onion.Faces:Item("Face15").Medium = VAnt_Project.Media:Item("Perfect electric conductor")
--

-- STEP 16: Create new edge port
   VTmp_Pos = {}
   VTmp_Neg = {}
   VTmp_Pos[1] = VAnt_Union_Onion.Faces:Item("Face2")
   VTmp_Neg[1] = VAnt_Union_Onion.Faces:Item("Face3")
   VAnt_EPort_SourcePort = VAnt_Project.Ports:AddEdgePort(VTmp_Pos, VTmp_Neg)
   VAnt_EPort_SourcePort.Label = "SourcePort"
--

-- STEP 17: Get config file
   VAnt_Config = VAnt_Project.SolutionConfigurations[1]
--

-- STEP 18: Create new voltage source
   VAnt_VSource_VoltageSource = VAnt_Config.Sources:AddVoltageSource(VAnt_EPort_SourcePort)
   VAnt_VSource_VoltageSource.Impedance = 50.0
   VAnt_VSource_VoltageSource.Magnitude = 1.0
   VAnt_VSource_VoltageSource.Phase = 0.0
   VAnt_VSource_VoltageSource.Label = "VoltageSource"
--

-- STEP 19: Create new Far-Field request
   VAnt_Config.FarFields:Add(0.0, 0.0, 180.0, 360.0, 5.0, 5.0)
--
-- STEP 20: Set frequency range
   VAnt_tmp = VAnt_Config.Frequency:GetProperties()
   VAnt_tmp.Start  = 906500000.0
   VAnt_tmp.End    = 933500000.0
   VAnt_tmp.RangeType  = cf.Enums.FrequencyRangeTypeEnum.LinearSpacedDiscrete
   VAnt_tmp.NumberOfDiscreteValues = 2
   VAnt_Config.Frequency:SetProperties(VAnt_tmp)
--

-- STEP 21: Mesh the project
   VAnt_Project.Mesher.Settings.WireRadius = 0.001
   VAnt_Project.Mesher.Settings.MeshSizeOption = cf.Enums.MeshSizeOptionEnum.Coarse
   VAnt_Project.Mesher:Mesh()
--

-- STEP 22: Save project
   VSes_Application:SaveAs("C:/Users/project/0. My Work/1. Repositories/1. Very Unfriendly Train/Data/Simulations/637072274664755200_Primary/637072274900731776_1/1.cfx")
--

-- STEP 23: Run simulation
   VAnt_Project.Launcher.Settings.FEKO.Parallel.Enabled = true
   VAnt_Project.Launcher:RunFEKO()
--

-- STEP 24: Close project
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
   VTmp_Points[1] = cf.Point(79.981, 52.784499999999994, 1.6)
   VTmp_Points[2] = cf.Point(79.981, 54.41949999999999, 1.6)
   VTmp_Points[3] = cf.Point(90.966, 54.41949999999999, 1.6)
   VTmp_Points[4] = cf.Point(90.966, 52.784499999999994, 1.6)
   VAnt_Polygon_Feed_Top = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_Feed_Top.Label = "Feed_Top"
--

-- STEP 4: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(90.966, 54.41949999999999, 1.6)
   VTmp_Points[2] = cf.Point(90.966, 54.41949999999999, 0.8)
   VTmp_Points[3] = cf.Point(90.966, 52.784499999999994, 0.8)
   VTmp_Points[4] = cf.Point(90.966, 52.784499999999994, 1.6)
   VAnt_Polygon_Feed_Pos = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_Feed_Pos.Label = "Feed_Pos"
--

-- STEP 5: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(90.966, 54.41949999999999, 0.0)
   VTmp_Points[2] = cf.Point(90.966, 54.41949999999999, 0.8)
   VTmp_Points[3] = cf.Point(90.966, 52.784499999999994, 0.8)
   VTmp_Points[4] = cf.Point(90.966, 52.784499999999994, 0.0)
   VAnt_Polygon_Feed_Neg = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_Feed_Neg.Label = "Feed_Neg"
--

-- STEP 6: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(90.966, 52.784499999999994, 0.0)
   VTmp_Points[2] = cf.Point(90.966, 54.41949999999999, 0.0)
   VTmp_Points[3] = cf.Point(89.366, 54.41949999999999, 0.0)
   VTmp_Points[4] = cf.Point(89.366, 52.784499999999994, 0.0)
   VAnt_Polygon_Feed_Bot = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_Feed_Bot.Label = "Feed_Bot"
--

-- STEP 7: Create new rectangular surface
   VTmp_Corner = cf.Point(-0.308, -0.051, 0.0)
   VAnt_Rectangle_GP = VAnt_Geometry:AddRectangle(VTmp_Corner, 89.674, 106.753)
   VAnt_Rectangle_GP.Label = "GP"
--

-- STEP 8: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(47.771, 25.462, 0.0)
   VTmp_Points[2] = cf.Point(29.733, 13.197, 0.0)
   VTmp_Points[3] = cf.Point(44.103, 22.943, 0.0)
   VAnt_Polygon_GPSlot_0 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_0.Label = "GPSlot_0"
--

-- STEP 9: Create new subtraction
   VTmp_Subs = {}
   VTmp_Subs[1] = VAnt_Polygon_GPSlot_0
   VAnt_Subtraction_GP_Slotted = VAnt_Geometry:Subtract(VAnt_Rectangle_GP, VTmp_Subs)
   VAnt_Subtraction_GP_Slotted.Label = "GP_Slotted"
--

-- STEP 10: Creating medium
   VAnt_Medium_FR4 = VAnt_Project.Media:AddDielectric()
   VAnt_Medium_FR4.Label = "FR4"
   VAnt_Medium_FR4.DielectricModelling.RelativePermittivity = 4.4
   VAnt_Medium_FR4.DielectricModelling.LossTangent = 0.02
--

-- STEP 11: Create new solid.cuboid
   VTmp_Corner = cf.Point(-0.308, -0.051, 0.0)
   VAnt_Cuboid_Substrate = VAnt_Geometry:AddCuboid(VTmp_Corner, 89.674, 106.753, 1.6)
   VAnt_Cuboid_Substrate.Label = "Substrate"
--

-- STEP 12: Set solid medium
   VAnt_Cuboid_Substrate.Regions:Item(1).Medium = VAnt_Project.Media:Item("FR4")
--

-- STEP 13: Create new rectangular surface
   VTmp_Corner = cf.Point(4.905, 4.221, 1.6)
   VAnt_Rectangle_RP = VAnt_Geometry:AddRectangle(VTmp_Corner, 75.076, 98.915)
   VAnt_Rectangle_RP.Label = "RP"
--

-- STEP 14: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(33.558, 68.321, 1.6)
   VTmp_Points[2] = cf.Point(32.512, 67.91, 1.6)
   VTmp_Points[3] = cf.Point(31.243, 65.278, 1.6)
   VAnt_Polygon_GPSlot_0 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_0.Label = "GPSlot_0"
--

-- STEP 15: Create new subtraction
   VTmp_Subs = {}
   VTmp_Subs[1] = VAnt_Polygon_GPSlot_0
   VAnt_Subtraction_RP_Slotted = VAnt_Geometry:Subtract(VAnt_Rectangle_RP, VTmp_Subs)
   VAnt_Subtraction_RP_Slotted.Label = "RP_Slotted"
--

-- STEP 16: Create new union
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

-- STEP 17: Changing face medium
   VAnt_Union_Onion.Faces:Item("Face15").Medium = VAnt_Project.Media:Item("Perfect electric conductor")
--

-- STEP 18: Changing face medium
   VAnt_Union_Onion.Faces:Item("Face16").Medium = VAnt_Project.Media:Item("Perfect electric conductor")
--

-- STEP 19: Changing face medium
   VAnt_Union_Onion.Faces:Item("Face17").Medium = VAnt_Project.Media:Item("Perfect electric conductor")
--

-- STEP 20: Create new edge port
   VTmp_Pos = {}
   VTmp_Neg = {}
   VTmp_Pos[1] = VAnt_Union_Onion.Faces:Item("Face2")
   VTmp_Neg[1] = VAnt_Union_Onion.Faces:Item("Face3")
   VAnt_EPort_SourcePort = VAnt_Project.Ports:AddEdgePort(VTmp_Pos, VTmp_Neg)
   VAnt_EPort_SourcePort.Label = "SourcePort"
--

-- STEP 21: Get config file
   VAnt_Config = VAnt_Project.SolutionConfigurations[1]
--

-- STEP 22: Create new voltage source
   VAnt_VSource_VoltageSource = VAnt_Config.Sources:AddVoltageSource(VAnt_EPort_SourcePort)
   VAnt_VSource_VoltageSource.Impedance = 50.0
   VAnt_VSource_VoltageSource.Magnitude = 1.0
   VAnt_VSource_VoltageSource.Phase = 0.0
   VAnt_VSource_VoltageSource.Label = "VoltageSource"
--

-- STEP 23: Create new Far-Field request
   VAnt_Config.FarFields:Add(0.0, 0.0, 180.0, 360.0, 5.0, 5.0)
--
-- STEP 24: Set frequency range
   VAnt_tmp = VAnt_Config.Frequency:GetProperties()
   VAnt_tmp.Start  = 906500000.0
   VAnt_tmp.End    = 933500000.0
   VAnt_tmp.RangeType  = cf.Enums.FrequencyRangeTypeEnum.LinearSpacedDiscrete
   VAnt_tmp.NumberOfDiscreteValues = 2
   VAnt_Config.Frequency:SetProperties(VAnt_tmp)
--

-- STEP 25: Mesh the project
   VAnt_Project.Mesher.Settings.WireRadius = 0.001
   VAnt_Project.Mesher.Settings.MeshSizeOption = cf.Enums.MeshSizeOptionEnum.Coarse
   VAnt_Project.Mesher:Mesh()
--

-- STEP 26: Save project
   VSes_Application:SaveAs("C:/Users/project/0. My Work/1. Repositories/1. Very Unfriendly Train/Data/Simulations/637072274664755200_Primary/637072274900731776_2/2.cfx")
--

-- STEP 27: Run simulation
   VAnt_Project.Launcher.Settings.FEKO.Parallel.Enabled = true
   VAnt_Project.Launcher:RunFEKO()
--

-- STEP 28: Close project
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
   VTmp_Points[1] = cf.Point(81.46900000000001, 52.548, 1.6)
   VTmp_Points[2] = cf.Point(81.46900000000001, 54.196000000000005, 1.6)
   VTmp_Points[3] = cf.Point(85.416, 54.196000000000005, 1.6)
   VTmp_Points[4] = cf.Point(85.416, 52.548, 1.6)
   VAnt_Polygon_Feed_Top = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_Feed_Top.Label = "Feed_Top"
--

-- STEP 4: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(85.416, 54.196000000000005, 1.6)
   VTmp_Points[2] = cf.Point(85.416, 54.196000000000005, 0.8)
   VTmp_Points[3] = cf.Point(85.416, 52.548, 0.8)
   VTmp_Points[4] = cf.Point(85.416, 52.548, 1.6)
   VAnt_Polygon_Feed_Pos = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_Feed_Pos.Label = "Feed_Pos"
--

-- STEP 5: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(85.416, 54.196000000000005, 0.0)
   VTmp_Points[2] = cf.Point(85.416, 54.196000000000005, 0.8)
   VTmp_Points[3] = cf.Point(85.416, 52.548, 0.8)
   VTmp_Points[4] = cf.Point(85.416, 52.548, 0.0)
   VAnt_Polygon_Feed_Neg = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_Feed_Neg.Label = "Feed_Neg"
--

-- STEP 6: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(85.416, 52.548, 0.0)
   VTmp_Points[2] = cf.Point(85.416, 54.196000000000005, 0.0)
   VTmp_Points[3] = cf.Point(83.816, 54.196000000000005, 0.0)
   VTmp_Points[4] = cf.Point(83.816, 52.548, 0.0)
   VAnt_Polygon_Feed_Bot = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_Feed_Bot.Label = "Feed_Bot"
--

-- STEP 7: Create new rectangular surface
   VTmp_Corner = cf.Point(-0.349, -0.478, 0.0)
   VAnt_Rectangle_GP = VAnt_Geometry:AddRectangle(VTmp_Corner, 84.165, 106.887)
   VAnt_Rectangle_GP.Label = "GP"
--

-- STEP 8: Creating medium
   VAnt_Medium_FR4 = VAnt_Project.Media:AddDielectric()
   VAnt_Medium_FR4.Label = "FR4"
   VAnt_Medium_FR4.DielectricModelling.RelativePermittivity = 4.4
   VAnt_Medium_FR4.DielectricModelling.LossTangent = 0.02
--

-- STEP 9: Create new solid.cuboid
   VTmp_Corner = cf.Point(-0.349, -0.478, 0.0)
   VAnt_Cuboid_Substrate = VAnt_Geometry:AddCuboid(VTmp_Corner, 84.165, 106.887, 1.6)
   VAnt_Cuboid_Substrate.Label = "Substrate"
--

-- STEP 10: Set solid medium
   VAnt_Cuboid_Substrate.Regions:Item(1).Medium = VAnt_Project.Media:Item("FR4")
--

-- STEP 11: Create new rectangular surface
   VTmp_Corner = cf.Point(4.662, 4.836, 1.6)
   VAnt_Rectangle_RP = VAnt_Geometry:AddRectangle(VTmp_Corner, 76.807, 97.957)
   VAnt_Rectangle_RP.Label = "RP"
--

-- STEP 12: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(64.833, 82.391, 1.6)
   VTmp_Points[2] = cf.Point(65.695, 84.19, 1.6)
   VTmp_Points[3] = cf.Point(66.335, 84.448, 1.6)
   VAnt_Polygon_GPSlot_0 = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_GPSlot_0.Label = "GPSlot_0"
--

-- STEP 13: Create new subtraction
   VTmp_Subs = {}
   VTmp_Subs[1] = VAnt_Polygon_GPSlot_0
   VAnt_Subtraction_RP_Slotted = VAnt_Geometry:Subtract(VAnt_Rectangle_RP, VTmp_Subs)
   VAnt_Subtraction_RP_Slotted.Label = "RP_Slotted"
--

-- STEP 14: Create new union
   VTmp_Parts = {}
   VTmp_Parts[1] = VAnt_Rectangle_GP
   VTmp_Parts[2] = VAnt_Subtraction_RP_Slotted
   VTmp_Parts[3] = VAnt_Cuboid_Substrate
   VTmp_Parts[4] = VAnt_Polygon_Feed_Top
   VTmp_Parts[5] = VAnt_Polygon_Feed_Pos
   VTmp_Parts[6] = VAnt_Polygon_Feed_Neg
   VTmp_Parts[7] = VAnt_Polygon_Feed_Bot
   VAnt_Union_Onion = VAnt_Geometry:Union(VTmp_Parts)
   VAnt_Union_Onion.Label = "Onion"
--

-- STEP 15: Changing face medium
   VAnt_Union_Onion.Faces:Item("Face14").Medium = VAnt_Project.Media:Item("Perfect electric conductor")
--

-- STEP 16: Changing face medium
   VAnt_Union_Onion.Faces:Item("Face15").Medium = VAnt_Project.Media:Item("Perfect electric conductor")
--

-- STEP 17: Changing face medium
   VAnt_Union_Onion.Faces:Item("Face16").Medium = VAnt_Project.Media:Item("Perfect electric conductor")
--

-- STEP 18: Create new edge port
   VTmp_Pos = {}
   VTmp_Neg = {}
   VTmp_Pos[1] = VAnt_Union_Onion.Faces:Item("Face2")
   VTmp_Neg[1] = VAnt_Union_Onion.Faces:Item("Face3")
   VAnt_EPort_SourcePort = VAnt_Project.Ports:AddEdgePort(VTmp_Pos, VTmp_Neg)
   VAnt_EPort_SourcePort.Label = "SourcePort"
--

-- STEP 19: Get config file
   VAnt_Config = VAnt_Project.SolutionConfigurations[1]
--

-- STEP 20: Create new voltage source
   VAnt_VSource_VoltageSource = VAnt_Config.Sources:AddVoltageSource(VAnt_EPort_SourcePort)
   VAnt_VSource_VoltageSource.Impedance = 50.0
   VAnt_VSource_VoltageSource.Magnitude = 1.0
   VAnt_VSource_VoltageSource.Phase = 0.0
   VAnt_VSource_VoltageSource.Label = "VoltageSource"
--

-- STEP 21: Create new Far-Field request
   VAnt_Config.FarFields:Add(0.0, 0.0, 180.0, 360.0, 5.0, 5.0)
--
-- STEP 22: Set frequency range
   VAnt_tmp = VAnt_Config.Frequency:GetProperties()
   VAnt_tmp.Start  = 906500000.0
   VAnt_tmp.End    = 933500000.0
   VAnt_tmp.RangeType  = cf.Enums.FrequencyRangeTypeEnum.LinearSpacedDiscrete
   VAnt_tmp.NumberOfDiscreteValues = 2
   VAnt_Config.Frequency:SetProperties(VAnt_tmp)
--

-- STEP 23: Mesh the project
   VAnt_Project.Mesher.Settings.WireRadius = 0.001
   VAnt_Project.Mesher.Settings.MeshSizeOption = cf.Enums.MeshSizeOptionEnum.Coarse
   VAnt_Project.Mesher:Mesh()
--

-- STEP 24: Save project
   VSes_Application:SaveAs("C:/Users/project/0. My Work/1. Repositories/1. Very Unfriendly Train/Data/Simulations/637072274664755200_Primary/637072274900731776_3/3.cfx")
--

-- STEP 25: Run simulation
   VAnt_Project.Launcher.Settings.FEKO.Parallel.Enabled = true
   VAnt_Project.Launcher:RunFEKO()
--

-- STEP 26: Close project
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
   VTmp_Points[1] = cf.Point(80.983, 52.832499999999996, 1.6)
   VTmp_Points[2] = cf.Point(80.983, 54.503499999999995, 1.6)
   VTmp_Points[3] = cf.Point(86.562, 54.503499999999995, 1.6)
   VTmp_Points[4] = cf.Point(86.562, 52.832499999999996, 1.6)
   VAnt_Polygon_Feed_Top = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_Feed_Top.Label = "Feed_Top"
--

-- STEP 4: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(86.562, 54.503499999999995, 1.6)
   VTmp_Points[2] = cf.Point(86.562, 54.503499999999995, 0.8)
   VTmp_Points[3] = cf.Point(86.562, 52.832499999999996, 0.8)
   VTmp_Points[4] = cf.Point(86.562, 52.832499999999996, 1.6)
   VAnt_Polygon_Feed_Pos = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_Feed_Pos.Label = "Feed_Pos"
--

-- STEP 5: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(86.562, 54.503499999999995, 0.0)
   VTmp_Points[2] = cf.Point(86.562, 54.503499999999995, 0.8)
   VTmp_Points[3] = cf.Point(86.562, 52.832499999999996, 0.8)
   VTmp_Points[4] = cf.Point(86.562, 52.832499999999996, 0.0)
   VAnt_Polygon_Feed_Neg = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_Feed_Neg.Label = "Feed_Neg"
--

-- STEP 6: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(86.562, 52.832499999999996, 0.0)
   VTmp_Points[2] = cf.Point(86.562, 54.503499999999995, 0.0)
   VTmp_Points[3] = cf.Point(84.962, 54.503499999999995, 0.0)
   VTmp_Points[4] = cf.Point(84.962, 52.832499999999996, 0.0)
   VAnt_Polygon_Feed_Bot = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_Feed_Bot.Label = "Feed_Bot"
--

-- STEP 7: Create new rectangular surface
   VTmp_Corner = cf.Point(-0.128, -0.046, 0.0)
   VAnt_Rectangle_GP = VAnt_Geometry:AddRectangle(VTmp_Corner, 85.09, 108.428)
   VAnt_Rectangle_GP.Label = "GP"
--

-- STEP 8: Creating medium
   VAnt_Medium_FR4 = VAnt_Project.Media:AddDielectric()
   VAnt_Medium_FR4.Label = "FR4"
   VAnt_Medium_FR4.DielectricModelling.RelativePermittivity = 4.4
   VAnt_Medium_FR4.DielectricModelling.LossTangent = 0.02
--

-- STEP 9: Create new solid.cuboid
   VTmp_Corner = cf.Point(-0.128, -0.046, 0.0)
   VAnt_Cuboid_Substrate = VAnt_Geometry:AddCuboid(VTmp_Corner, 85.09, 108.428, 1.6)
   VAnt_Cuboid_Substrate.Label = "Substrate"
--

-- STEP 10: Set solid medium
   VAnt_Cuboid_Substrate.Regions:Item(1).Medium = VAnt_Project.Media:Item("FR4")
--

-- STEP 11: Create new rectangular surface
   VTmp_Corner = cf.Point(4.509, 4.504, 1.6)
   VAnt_Rectangle_RP = VAnt_Geometry:AddRectangle(VTmp_Corner, 76.474, 98.286)
   VAnt_Rectangle_RP.Label = "RP"
--

-- STEP 12: Create new union
   VTmp_Parts = {}
   VTmp_Parts[1] = VAnt_Rectangle_GP
   VTmp_Parts[2] = VAnt_Rectangle_RP
   VTmp_Parts[3] = VAnt_Cuboid_Substrate
   VTmp_Parts[4] = VAnt_Polygon_Feed_Top
   VTmp_Parts[5] = VAnt_Polygon_Feed_Pos
   VTmp_Parts[6] = VAnt_Polygon_Feed_Neg
   VTmp_Parts[7] = VAnt_Polygon_Feed_Bot
   VAnt_Union_Onion = VAnt_Geometry:Union(VTmp_Parts)
   VAnt_Union_Onion.Label = "Onion"
--

-- STEP 13: Changing face medium
   VAnt_Union_Onion.Faces:Item("Face13").Medium = VAnt_Project.Media:Item("Perfect electric conductor")
--

-- STEP 14: Changing face medium
   VAnt_Union_Onion.Faces:Item("Face14").Medium = VAnt_Project.Media:Item("Perfect electric conductor")
--

-- STEP 15: Changing face medium
   VAnt_Union_Onion.Faces:Item("Face15").Medium = VAnt_Project.Media:Item("Perfect electric conductor")
--

-- STEP 16: Create new edge port
   VTmp_Pos = {}
   VTmp_Neg = {}
   VTmp_Pos[1] = VAnt_Union_Onion.Faces:Item("Face2")
   VTmp_Neg[1] = VAnt_Union_Onion.Faces:Item("Face3")
   VAnt_EPort_SourcePort = VAnt_Project.Ports:AddEdgePort(VTmp_Pos, VTmp_Neg)
   VAnt_EPort_SourcePort.Label = "SourcePort"
--

-- STEP 17: Get config file
   VAnt_Config = VAnt_Project.SolutionConfigurations[1]
--

-- STEP 18: Create new voltage source
   VAnt_VSource_VoltageSource = VAnt_Config.Sources:AddVoltageSource(VAnt_EPort_SourcePort)
   VAnt_VSource_VoltageSource.Impedance = 50.0
   VAnt_VSource_VoltageSource.Magnitude = 1.0
   VAnt_VSource_VoltageSource.Phase = 0.0
   VAnt_VSource_VoltageSource.Label = "VoltageSource"
--

-- STEP 19: Create new Far-Field request
   VAnt_Config.FarFields:Add(0.0, 0.0, 180.0, 360.0, 5.0, 5.0)
--
-- STEP 20: Set frequency range
   VAnt_tmp = VAnt_Config.Frequency:GetProperties()
   VAnt_tmp.Start  = 906500000.0
   VAnt_tmp.End    = 933500000.0
   VAnt_tmp.RangeType  = cf.Enums.FrequencyRangeTypeEnum.LinearSpacedDiscrete
   VAnt_tmp.NumberOfDiscreteValues = 2
   VAnt_Config.Frequency:SetProperties(VAnt_tmp)
--

-- STEP 21: Mesh the project
   VAnt_Project.Mesher.Settings.WireRadius = 0.001
   VAnt_Project.Mesher.Settings.MeshSizeOption = cf.Enums.MeshSizeOptionEnum.Coarse
   VAnt_Project.Mesher:Mesh()
--

-- STEP 22: Save project
   VSes_Application:SaveAs("C:/Users/project/0. My Work/1. Repositories/1. Very Unfriendly Train/Data/Simulations/637072274664755200_Primary/637072274900731776_4/4.cfx")
--

-- STEP 23: Run simulation
   VAnt_Project.Launcher.Settings.FEKO.Parallel.Enabled = true
   VAnt_Project.Launcher:RunFEKO()
--

-- STEP 24: Close project
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
   VTmp_Points[1] = cf.Point(81.381, 52.941, 1.6)
   VTmp_Points[2] = cf.Point(81.381, 54.583000000000006, 1.6)
   VTmp_Points[3] = cf.Point(85.64599999999999, 54.583000000000006, 1.6)
   VTmp_Points[4] = cf.Point(85.64599999999999, 52.941, 1.6)
   VAnt_Polygon_Feed_Top = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_Feed_Top.Label = "Feed_Top"
--

-- STEP 4: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(85.64599999999999, 54.583000000000006, 1.6)
   VTmp_Points[2] = cf.Point(85.64599999999999, 54.583000000000006, 0.8)
   VTmp_Points[3] = cf.Point(85.64599999999999, 52.941, 0.8)
   VTmp_Points[4] = cf.Point(85.64599999999999, 52.941, 1.6)
   VAnt_Polygon_Feed_Pos = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_Feed_Pos.Label = "Feed_Pos"
--

-- STEP 5: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(85.64599999999999, 54.583000000000006, 0.0)
   VTmp_Points[2] = cf.Point(85.64599999999999, 54.583000000000006, 0.8)
   VTmp_Points[3] = cf.Point(85.64599999999999, 52.941, 0.8)
   VTmp_Points[4] = cf.Point(85.64599999999999, 52.941, 0.0)
   VAnt_Polygon_Feed_Neg = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_Feed_Neg.Label = "Feed_Neg"
--

-- STEP 6: Create new polygonal surface
   VTmp_Points = {}
   VTmp_Points[1] = cf.Point(85.64599999999999, 52.941, 0.0)
   VTmp_Points[2] = cf.Point(85.64599999999999, 54.583000000000006, 0.0)
   VTmp_Points[3] = cf.Point(84.04599999999999, 54.583000000000006, 0.0)
   VTmp_Points[4] = cf.Point(84.04599999999999, 52.941, 0.0)
   VAnt_Polygon_Feed_Bot = VAnt_Geometry:AddPolygon(VTmp_Points)
   VAnt_Polygon_Feed_Bot.Label = "Feed_Bot"
--

-- STEP 7: Create new rectangular surface
   VTmp_Corner = cf.Point(-0.191, -0.013, 0.0)
   VAnt_Rectangle_GP = VAnt_Geometry:AddRectangle(VTmp_Corner, 84.237, 107.944)
   VAnt_Rectangle_GP.Label = "GP"
--

-- STEP 8: Creating medium
   VAnt_Medium_FR4 = VAnt_Project.Media:AddDielectric()
   VAnt_Medium_FR4.Label = "FR4"
   VAnt_Medium_FR4.DielectricModelling.RelativePermittivity = 4.4
   VAnt_Medium_FR4.DielectricModelling.LossTangent = 0.02
--

-- STEP 9: Create new solid.cuboid
   VTmp_Corner = cf.Point(-0.191, -0.013, 0.0)
   VAnt_Cuboid_Substrate = VAnt_Geometry:AddCuboid(VTmp_Corner, 84.237, 107.944, 1.6)
   VAnt_Cuboid_Substrate.Label = "Substrate"
--

-- STEP 10: Set solid medium
   VAnt_Cuboid_Substrate.Regions:Item(1).Medium = VAnt_Project.Media:Item("FR4")
--

-- STEP 11: Create new rectangular surface
   VTmp_Corner = cf.Point(4.58, 4.922, 1.6)
   VAnt_Rectangle_RP = VAnt_Geometry:AddRectangle(VTmp_Corner, 76.801, 98.642)
   VAnt_Rectangle_RP.Label = "RP"
--

-- STEP 12: Create new rectangular surface
   VTmp_Corner = cf.Point(44.328, 50.437, 1.6)
   VAnt_Rectangle_GPSlot_0 = VAnt_Geometry:AddRectangle(VTmp_Corner, 1.084, 3.887)
   VAnt_Rectangle_GPSlot_0.Label = "GPSlot_0"
--

-- STEP 13: Create new subtraction
   VTmp_Subs = {}
   VTmp_Subs[1] = VAnt_Rectangle_GPSlot_0
   VAnt_Subtraction_RP_Slotted = VAnt_Geometry:Subtract(VAnt_Rectangle_RP, VTmp_Subs)
   VAnt_Subtraction_RP_Slotted.Label = "RP_Slotted"
--

-- STEP 14: Create new union
   VTmp_Parts = {}
   VTmp_Parts[1] = VAnt_Rectangle_GP
   VTmp_Parts[2] = VAnt_Subtraction_RP_Slotted
   VTmp_Parts[3] = VAnt_Cuboid_Substrate
   VTmp_Parts[4] = VAnt_Polygon_Feed_Top
   VTmp_Parts[5] = VAnt_Polygon_Feed_Pos
   VTmp_Parts[6] = VAnt_Polygon_Feed_Neg
   VTmp_Parts[7] = VAnt_Polygon_Feed_Bot
   VAnt_Union_Onion = VAnt_Geometry:Union(VTmp_Parts)
   VAnt_Union_Onion.Label = "Onion"
--

-- STEP 15: Changing face medium
   VAnt_Union_Onion.Faces:Item("Face14").Medium = VAnt_Project.Media:Item("Perfect electric conductor")
--

-- STEP 16: Changing face medium
   VAnt_Union_Onion.Faces:Item("Face15").Medium = VAnt_Project.Media:Item("Perfect electric conductor")
--

-- STEP 17: Changing face medium
   VAnt_Union_Onion.Faces:Item("Face16").Medium = VAnt_Project.Media:Item("Perfect electric conductor")
--

-- STEP 18: Create new edge port
   VTmp_Pos = {}
   VTmp_Neg = {}
   VTmp_Pos[1] = VAnt_Union_Onion.Faces:Item("Face2")
   VTmp_Neg[1] = VAnt_Union_Onion.Faces:Item("Face3")
   VAnt_EPort_SourcePort = VAnt_Project.Ports:AddEdgePort(VTmp_Pos, VTmp_Neg)
   VAnt_EPort_SourcePort.Label = "SourcePort"
--

-- STEP 19: Get config file
   VAnt_Config = VAnt_Project.SolutionConfigurations[1]
--

-- STEP 20: Create new voltage source
   VAnt_VSource_VoltageSource = VAnt_Config.Sources:AddVoltageSource(VAnt_EPort_SourcePort)
   VAnt_VSource_VoltageSource.Impedance = 50.0
   VAnt_VSource_VoltageSource.Magnitude = 1.0
   VAnt_VSource_VoltageSource.Phase = 0.0
   VAnt_VSource_VoltageSource.Label = "VoltageSource"
--

-- STEP 21: Create new Far-Field request
   VAnt_Config.FarFields:Add(0.0, 0.0, 180.0, 360.0, 5.0, 5.0)
--
-- STEP 22: Set frequency range
   VAnt_tmp = VAnt_Config.Frequency:GetProperties()
   VAnt_tmp.Start  = 906500000.0
   VAnt_tmp.End    = 933500000.0
   VAnt_tmp.RangeType  = cf.Enums.FrequencyRangeTypeEnum.LinearSpacedDiscrete
   VAnt_tmp.NumberOfDiscreteValues = 2
   VAnt_Config.Frequency:SetProperties(VAnt_tmp)
--

-- STEP 23: Mesh the project
   VAnt_Project.Mesher.Settings.WireRadius = 0.001
   VAnt_Project.Mesher.Settings.MeshSizeOption = cf.Enums.MeshSizeOptionEnum.Coarse
   VAnt_Project.Mesher:Mesh()
--

-- STEP 24: Save project
   VSes_Application:SaveAs("C:/Users/project/0. My Work/1. Repositories/1. Very Unfriendly Train/Data/Simulations/637072274664755200_Primary/637072274900731776_5/5.cfx")
--

-- STEP 25: Run simulation
   VAnt_Project.Launcher.Settings.FEKO.Parallel.Enabled = true
   VAnt_Project.Launcher:RunFEKO()
--

-- STEP 26: Close project
   VSes_Application:CloseAllWindows()
--

-- STEP ??: Close file
   VSes_Application:CloseAllWindows()
   VSes_Application:Close()
--
