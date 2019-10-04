#region Imports

from    enum                            import Enum

import  copy                            as cp
import  numpy                           as np
import  os
import  random                          as rn
import  sys
import  time                            as tm

sys.path.append(os.path.abspath("."))

from    Code.Enums.Enums                import Enums        as en

from    Code.Handlers.LuaHandler        import Lana

from    Helpers.ActivationFunctions     import Antonio
from    Helpers.Config                  import Conny
from    Helpers.GeneralHelpers          import Helga

#endregion

#region Class - Mathew

class Matthew:

    #region Init

    """
    """

    def __init__(self):

        #   region STEP 0: Local variables

        self.__enum                 = en.Mathew
        self.__cf                   = Conny()
        self.__cf.load(self.__enum.value)
        
        #   endregion

        #   region STEP 1: Private variables

        #   endregion

        #   region STEP 2: Public variables

        #   endregion

        #   region STEP 3: Setup - Private variables

        #   endregion

        #   region STEP 4: Setup - Public variables

        #   endregion

        return
    
    #
    #endregion

    #region Front-End
    
    #   region Front-End: Gets

    #       region Front-End-(Gets): Antenna

    @classmethod
    def getPatch_Default(self, **kwargs) -> dict:
        """
            Description:

                Creates a default rectangular patch antenna using the passed
                arguments.
            
            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:

                + name  = ( str ) The name of the new patch antenna
                    ~ Required

                + dir   = ( str ) The directory for the new patch antenna
                    project
                    ~ Required

                + substrate = ( dict ) Dictionary containing information that
                    will be used for the substrate
                    ~ Required

                    ~ "name"            = ( str )
                    ~ "height"          = ( float )
                    ~ "permitivitty"    = ( float )
                    ~ "loss tangent"    = ( float )

                + frequency = ( dict ) Dictionary containing the data for the 
                    frequency operation of the patch as well as the simulation
                    frequency parameters
                    ~ Required

                    ~ "center"  = ( float )
                    ~ "start"   = ( float )
                    ~ "end"     = ( float )
                    ~ "samples" = ( int )

                + mesh  = ( dict ) Dictionary containing the data for the
                    meshing of the patch antenna
                    ~ Required

                    ~ "wire radius" = ( float )
                    ~ "size"        = ( str )
                        - "Coarse"
                        - "Standard"
                        - "Fine"

                + runt  = ( dict ) Dictionary containing the runtime data for 
                    the patch antenna project
                    ~ Required

                    ~ "parallel"    = ( bool )
                    ~ "run"         = ( bool )
                    ~ "interactive" = ( bool )

                + fitness   = ( dict ) Dictionary containing the requried
                    parameters for frequency fitness evaluation
                    ~ "desired" : { "start" = ( float ), "end" = ( float ) }
        """

        #   STEP 0: Local variables
        dGeometry               = None
        dOut                    = None

        sName                   = Helga.ticks()

        #   STEP 1: Setup - Local variables

        #   region STEP 2->13: Error checking

        #   STEP 2: Check if name arg passed
        if ("name" not in kwargs):
            #   STEP 3: Error handling
            raise Exception("An error occured in Matthew.getPatch_Default() -> Step 2: No name arg passed")

        #   STEP 4: Cehck if dir arg passed
        if ("dir" not in kwargs):
            #   STEP 5: Error handling
            raise Exception("An error occured in Matthew.getPatch_Default()-> Step 4: No dir arg passed")

        #   STEP 6: Check if substrate arg passed
        if ("substrate" not in kwargs):
            #   STEP 7: Error handling
            raise Exception("An error occured in Matthew.getPatch_Default() -> Step 6: No substrate arg passed")

        #   STEP 8: Check if frequency arg passed
        if ("frequency" not in kwargs):
            #   STEP 9: Error handling
            raise Exception("An error occured in Matthew.getPatch_Default() -> Step 8: No frequency arg passed")

        #   STEP 10: Check if mesh arg passed
        if ("mesh" not in kwargs):
            #   STEP 11: Error handling
            raise Exception("An error occured in Matthew.getPatch_Default() -> Step 10: No mesh arg passed")

        #   STEP 12: Check if runt arg passed
        if ("runt" not in kwargs):
            #   STEP 13: Error handling
            raise Exception("An error occured in Matthew.getPatch_Default() -> Step 12: No runt arg passed")             
        
        #
        #   endregion

        #   STEP 14: Get patch geometry
        dGeometry = self.getPatch_Geometry(substrate=kwargs["substrate"], frequency=kwargs["frequency"])

        #   STEP 15: Create the antenna project
        lAntenna = Lana(name=sName, dir=kwargs["dir"], units="Millimetres")
        lAntenna.newAntenna(name=kwargs["name"])

        #   region STEP 16: Create ground plane
        
        dTmp_Corner = {
            "x": 0.0,
            "y": 0.0,
            "z": 0.0
        }

        dTmp_Dim    = {
            "l": dGeometry["ground plane"]["length"],
            "w": dGeometry["ground plane"]["width"]
        }

        sTmp_GroundPlane = lAntenna.newASurface(surface="Rectangle", corner=dTmp_Corner, dimensions=dTmp_Dim, label="GroundPlane")

        #
        #   endregion

        #   region STEP 17: Create radiating plane

        dTmp_Corner = {
            "x": round((dGeometry["ground plane"]["length"] - dGeometry["radiating plane"]["length"]) / 2.0, 6),
            "y": round((dGeometry["ground plane"]["width"] - dGeometry["radiating plane"]["width"]) / 2.0, 6),
            "z": kwargs["substrate"]["height"]
        }

        dTmp_Dim    = {
            "l": round(dGeometry["radiating plane"]["length"], 6),
            "w": round(dGeometry["radiating plane"]["width"], 6)
        }

        sTmp_RadiatingPlane = lAntenna.newASurface(surface="Rectangle", corner=dTmp_Corner, dimensions=dTmp_Dim, label="RadiatingPlane")

        #
        #   endregion

        #   region STEP 18: Create top feed strip

        fTmp_L  = round(dTmp_Dim["l"] + dTmp_Corner["x"], 6)
        fTmp_W  = round(dGeometry["ground plane"]["width"] / 2.0, 6)

        dTmp_Corner ={
            "items": 4,

            "0": {
                "x": fTmp_L,
                "y": fTmp_W - kwargs["substrate"]["height"] / 2.0,
                "z": kwargs["substrate"]["height"]
            },
            "1": {
                "x": fTmp_L,
                "y": fTmp_W + kwargs["substrate"]["height"] / 2.0,
                "z": kwargs["substrate"]["height"]
            },
            "2": {
                "x": dGeometry["ground plane"]["length"] + kwargs["substrate"]["height"],
                "y": fTmp_W + kwargs["substrate"]["height"] / 2.0,
                "z": kwargs["substrate"]["height"]
            },
            "3": {
                "x": dGeometry["ground plane"]["length"] + kwargs["substrate"]["height"],
                "y": fTmp_W - kwargs["substrate"]["height"] / 2.0,
                "z": kwargs["substrate"]["height"]
            }
        }
        
        sTmp_FeedStrip_Top = lAntenna.newASurface(surface="Polygon", corner=dTmp_Corner, label="TopFeedStrip")

        #
        #   endregion

        #   region STEP 19: Create top feed connection
        
        dTmp_Corner ={
            "items": 4,

            "0": {
                "x": dGeometry["ground plane"]["length"] + kwargs["substrate"]["height"],
                "y": fTmp_W + kwargs["substrate"]["height"] / 2.0,
                "z": kwargs["substrate"]["height"]
            },
            "1": {
                "x": dGeometry["ground plane"]["length"] + kwargs["substrate"]["height"],
                "y": fTmp_W - kwargs["substrate"]["height"] / 2.0,
                "z": kwargs["substrate"]["height"]
            },
            "2": {
                "x": dGeometry["ground plane"]["length"] + kwargs["substrate"]["height"],
                "y": fTmp_W - kwargs["substrate"]["height"] / 2.0,
                "z": kwargs["substrate"]["height"] / 2.0
            },
            "3": {
                "x": dGeometry["ground plane"]["length"] + kwargs["substrate"]["height"],
                "y": fTmp_W + kwargs["substrate"]["height"] / 2.0,
                "z": kwargs["substrate"]["height"] / 2.0                
            }
        }

        sTmp_FeedConnect_Top = lAntenna.newASurface(surface="Polygon", corner=dTmp_Corner, label="TopFeedConnect")

        #
        #   endregion

        #   region STEP 20: Create bot feed connection

        dTmp_Corner ={
            "items": 4,

            "0": {
                "x": dGeometry["ground plane"]["length"] + kwargs["substrate"]["height"],
                "y": fTmp_W + kwargs["substrate"]["height"] / 2.0,
                "z": 0.0
            },
            "1": {
                "x": dGeometry["ground plane"]["length"] + kwargs["substrate"]["height"],
                "y": fTmp_W - kwargs["substrate"]["height"] / 2.0,
                "z": 0.0
            },
            "2": {
                "x": dGeometry["ground plane"]["length"] + kwargs["substrate"]["height"],
                "y": fTmp_W - kwargs["substrate"]["height"] / 2.0,
                "z": kwargs["substrate"]["height"] / 2.0
            },
            "3": {
                "x": dGeometry["ground plane"]["length"] + kwargs["substrate"]["height"],
                "y": fTmp_W + kwargs["substrate"]["height"] / 2.0,
                "z": kwargs["substrate"]["height"] / 2.0                
            }
        }

        sTmp_FeedConnect_Bot = lAntenna.newASurface(surface="Polygon", corner=dTmp_Corner, label="BotFeedConnect")

        #
        #   endregion

        #   region STEP 21: create bot feed strip

        dTmp_Corner ={
            "items": 4,

            "0": {
                "x": dGeometry["ground plane"]["length"] + kwargs["substrate"]["height"],
                "y": fTmp_W + kwargs["substrate"]["height"] / 2.0,
                "z": 0.0
            },
            "1": {
                "x": dGeometry["ground plane"]["length"] + kwargs["substrate"]["height"],
                "y": fTmp_W - kwargs["substrate"]["height"] / 2.0,
                "z": 0.0
            },
            "2": {
                "x": dGeometry["ground plane"]["length"],
                "y": fTmp_W - kwargs["substrate"]["height"] / 2.0,
                "z": 0.0
            },
            "3": {
                "x": dGeometry["ground plane"]["length"],
                "y": fTmp_W + kwargs["substrate"]["height"] / 2.0,
                "z": 0.0                
            }
        }

        sTmp_FeedStrip_Bot = lAntenna.newASurface(surface="Polygon", corner=dTmp_Corner, label="BotFeedStrip")

        #
        #   endregion

        #   region STEP 22: Create substrate

        lAntenna.newAMedium(label=kwargs["substrate"]["name"], permitivitty=kwargs["substrate"]["permitivitty"], loss=kwargs["substrate"]["loss"])

        dTmp_Corner = {
            "x": 0.0,
            "y": 0.0,
            "z": 0.0
        }

        dTmp_Dim = {
            "l": dGeometry["ground plane"]["length"],
            "w": dGeometry["ground plane"]["width"],
            "h": kwargs["substrate"]["height"]
        }

        sTmp_Substrate = lAntenna.newASolid(solid="Cuboid", corner=dTmp_Corner, dimensions=dTmp_Dim, label="Substrate")

        lAntenna.setASolidMedium(medium=kwargs["substrate"]["name"], solid=sTmp_Substrate)

        #
        #   endregion

        #   region STEP 23: Create union

        dTmp_Parts = {
            "items": 7,

            "0": sTmp_GroundPlane,
            "1": sTmp_RadiatingPlane,
            "2": sTmp_FeedStrip_Top,
            "3": sTmp_FeedConnect_Top,
            "4": sTmp_FeedConnect_Bot,
            "5": sTmp_FeedStrip_Bot,
            "6": sTmp_Substrate
        }

        sTmp_Union = lAntenna.newAModification(mod="Union", parts=dTmp_Parts, label="Union")

        #
        #   endregion

        #   region STEP 24: Reset face media

        lAntenna.setAFaceMedium(medium="Perfect electric conductor", face="Face13", union=sTmp_Union)
        lAntenna.setAFaceMedium(medium="Perfect electric conductor", face="Face14", union=sTmp_Union)
        lAntenna.setAFaceMedium(medium="Perfect electric conductor", face="Face15", union=sTmp_Union)
        
        #
        #   endregion

        #   region STEP 25: Create new port

        dTmp_Pos = {
            "items": 1,
            "0": "Face4"
        }

        dTmp_Neg = {
            "items": 1,
            "0": "Face5"
        }

        sTmp_Port = lAntenna.newAPort(port="Edge", union=sTmp_Union, label="EdgePort", pos=dTmp_Pos, neg=dTmp_Neg)

        #
        #   endregion

        #   region STEP 26: Create new voltage source
        
        lAntenna.newASource(source="Voltage", port=sTmp_Port, label="VSource")
        
        #
        #   endregion

        #   region STEP 27: Set frequency and mesh

        lAntenna.setAFrequency(start=kwargs["frequency"]["start"], end=kwargs["frequency"]["end"], range_type="Linear", samples=kwargs["frequency"]["samples"])
        lAntenna.setAMesh(wire_radius=kwargs["mesh"]["wire radius"], size=kwargs["mesh"]["size"])

        #
        #   endregion

        #   region STEP 28: Save and run

        lAntenna.saveAntenna(dir=kwargs["name"])
        lAntenna.simulateAntenna(parallel=kwargs["runt"]["parallel"])
        lAntenna.closeAntenna()
        lAntenna.exportLua(replace=True, run=kwargs["runt"]["run"], interactive=kwargs["runt"]["interactive"])

        #
        #   endregion

        #   STEP 29: Populate output
        dOut = {
            "items":    4,

            "0":        "feed",
            "1":        "ground plane",
            "2":        "radiating plane",
            "3":        "substrate",

            "feed":
            {
                "items":    2,

                "0":        "center",
                "1":        "width",

                "center":   fTmp_W,
                "width":    kwargs["substrate"]["height"]
            },
            "ground plane":
            {
                "items":    5,

                "0":        "l",
                "1":        "w",
                "2":        "x",
                "3":        "y",
                "4":        "slots",

                "l":        dGeometry["ground plane"]["length"],
                "w":        dGeometry["ground plane"]["width"],
                "x":        0.0,
                "y":        0.0,

                "slots":
                {
                    "items": 0
                }
            },
            "radiating plane":
            {
                "items":    5,

                "0":        "l",
                "1":        "w",
                "2":        "x",
                "3":        "y",
                "4":        "slots",

                "l":        dGeometry["radiating plane"]["length"],
                "w":        dGeometry["radiating plane"]["width"],
                "x":        round((dGeometry["ground plane"]["length"] - dGeometry["radiating plane"]["length"] ) / 2.0, 6),
                "y":        round((dGeometry["ground plane"]["width"] - dGeometry["radiating plane"]["width"] ) / 2.0, 6),

                "slots":
                {
                    "items": 0
                }
            },
            "substrate":
            {
                "items":    4,
                "0":    "l",
                "1":    "w",
                "2":    "x",
                "3":    "y",
                
                "x": 0.0,
                "y": 0.0,
                "l": dGeometry["ground plane"]["length"],
                "w": dGeometry["ground plane"]["width"],
                "h": kwargs["substrate"]["height"],

                "permitivitty": kwargs["substrate"]["permitivitty"],
                "loss":         kwargs["substrate"]["loss"],
                "name":         kwargs["substrate"]["name"]
            },
            "dir": kwargs["dir"] + "\\" + sName + "_" + kwargs["name"] + "\\" + kwargs["name"] + ".out"
        }

        #   STEP 30: Check if fitness should be evaluated
        if ("fitness" in kwargs):
            #   STEP 31: Get config file
            vConny = Conny()
            vConny.load(en.Mathew.value)

            #   STEP 32: Get fitness evaluation
            dOut["fitness"] = self.getFitness(dir=dOut["dir"], frequency=kwargs["fitness"], params=vConny.data["parameters"])

        #   STEP 33: Return
        return dOut

    @classmethod
    def getPatch_Geometry(self, **kwargs) -> dict:
        """
            Description:

                Gets the geometry parameters for a default rectangular patch
                antenna.

            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:

                
                + substrate = ( dict ) Dictionary containing information that
                    will be used for the substrate
                    ~ Required

                    ~ "height"          = ( float )
                    ~ "permitivitty"    = ( float )

                + frequency = ( dict ) Dictionary containing the data for the 
                    frequency operation of the patch as well as the simulation
                    frequency parameters
                    ~ Required

                    ~ "center"  = ( float )
        """

        #   STEP 0: Local variables
        dOut                    = None

        fFreq_Center            = None

        fSub_Permitivitty       = None
        fSub_Height             = None

        fRadiating_Width        = None
        fRadiating_Length       = None
        fRadiating_DLength      = None
        fRadiating_ELength      = None

        fGround_Width           = None
        fGround_Length          = None

        fPermitivitty_Eff       = None

        fC                      = 2.99792458e8

        #   STEP 1: Setup - Local variables
        
        #   region STEP 2->5: Error checking

        #   STEP 2: Check if substrate arg passed
        if ("substrate" not in kwargs):
            #   STEP 3: Error handling
            raise Exception("An error occured in Matthew.getPatch_Geometry() -> Step 2: No substrate arg passed")

        #   STEP 4: Check if frequency arg passed
        if ("frequency" not in kwargs):
            #   STEP 5: Error handling
            raise Exception("An error occured in Matthew.getPatch_Geometry() -> Step 4: No frequency arg passed")
        
        #
        #   endregion

        #   region STEP 6: Update - Local variables

        #   STEP 6: Update - Local variables
        fFreq_Center = kwargs["frequency"]["center"]

        fSub_Permitivitty = kwargs["substrate"]["permitivitty"]
        fSub_Height = kwargs["substrate"]["height"] / 1000.0

        #
        #   endregion

        #   region STEP 7: Calculate radiating width

        #   STEP 7: Calculate radiatgin width
        fTmp_Width0 = fC / ( 2.0 * fFreq_Center )
        fTmp_Width1 = np.sqrt( 2.0 / ( fSub_Permitivitty + 1.0 ) )

        fRadiating_Width = round(fTmp_Width0 * fTmp_Width1, 8)

        #
        #   endregion

        #   region  STEP 8: Cacluate the effective permitivitty

        #   STEP 8: Calculate the effective permitivitty
        fTmp_PEff0  = ( fSub_Permitivitty - 1.0 ) / 2.0

        fTmp_PEff1  = 12.0 * ( fSub_Height / fRadiating_Width ) + 1.0
        fTmp_PEff1  = np.power(fTmp_PEff1, -0.5)
        
        fTmp_PEff3  = fTmp_PEff0 * fTmp_PEff1
        
        fTmp_PEff4  = ( fSub_Permitivitty + 1.0 ) / 2.0

        fPermitivitty_Eff = round(fTmp_PEff3 + fTmp_PEff4, 5)

        #
        #   endregion

        #   region STEP 9->11: Calculate radiating length

        #   STEP 9: Calculate ^l
        fTmp_DL0    = 0.412 * fSub_Height * ( fPermitivitty_Eff + 0.3 ) * ( fRadiating_Width / fSub_Height + 0.264 )
        fTmp_DL1    = ( fPermitivitty_Eff - 0.258 ) *  ( fRadiating_Width / fSub_Height + 0.8 )

        fRadiating_DLength = round(fTmp_DL0 / fTmp_DL1, 8)

        #   STEP 10: Calculate lEff
        fTmp_EL0    = 2.0 * fFreq_Center * np.sqrt(fPermitivitty_Eff)

        fRadiating_ELength  = round(fC / fTmp_EL0, 8)

        #   STEP 11: Cacluate radiating length
        fRadiating_Length   = round(fRadiating_ELength - 2.0 * fRadiating_DLength, 8)

        #
        #   endregion

        #   region STEP 12: Ground plane

        #   STEP 12: Calculate ground width and height
        fGround_Width   = round(6.0 * fSub_Height + fRadiating_Width, 8)
        fGround_Length  = round(6.0 * fSub_Height + fRadiating_Length, 8)

        #
        #   endregion

        #   STEP 13: Populate output dictionary
        dOut = {
            "radiating plane": {
                "length":   fRadiating_Length * 1e3,
                "width":    fRadiating_Width * 1e3
            },
            "ground plane":
            {
                "length":   fGround_Length * 1e3,
                "width":    fGround_Width * 1e3
            }
        }

        #   STEP 14: Return
        return dOut

    #
    #       endregion

    #       region Front-End-(Gets): Fitness

    @classmethod
    def getFitness(self, **kwargs) -> dict:
        """
            Description:

                Gets the fitness of the specified antenna simulation using the
                provided arguments.

            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:

                + dir   = ( str ) The path of the antenna simulationto use
                    for the fitness evaluation
                    ~ Required

                + frequency = ( dict ) A dictionary that contains the relevant
                    information for the fitness evaluation
                    ~ "desired" : { "start" = ( float ), "end" = ( float ) }

                + params    = ( dict ) A dictionary containing the parameters
                    the frequency fitness evaluation
        """

        #   STEP 0: Local variables
        dOut                    = {}

        #   STEP 1: Setup - Local variables

        #   STEP 2: Check if dir argument passed
        if ("dir" not in kwargs):
            #   STEP 3: Error handling
            raise Exception("An error occured in Matthew.getFitness() -> Step 2: No dir arg passed")

        #   STEP 4: Check if frequency fitness evaluations needs to be performed
        if ("frequency" in kwargs):
            #   STEP 5: Check if params arg passed
            if ("params" not in kwargs):
                #   STEP 6: Error handling
                raise Exception("An error occured in Matthew.getFitness() -> Step 5: No params arg passed")

            #   STEP 7: Append to output
            dOut["frequency"] = self.__getFitness_Frequency__(dir=kwargs["dir"], frequency=kwargs["frequency"], params=kwargs["params"])

        #   STEP 8: Return
        return dOut

    #
    #       endregion

    #
    #   endregion

    #   region Front-End: Other

    @classmethod
    def simulateCandidates_Json(self, **kwargs) -> list:
        """
            Description:

                Simulates the list of antennas provided and returns their
                fitness functions

            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:

                + dir   = ( str ) The directory for the new antenna projects
                    ~ Required

                + ant   = ( list ) A list of dictionaries containing patch
                    antenna geometries
                    ~ Required

                    ~ "feed":
                        {
                            "center":   ( float ),
                            "width":    ( float )
                        }
                    
                    ~ "ground plane":
                        {
                            "l":    ( float ),
                            "w":    ( float ),
                            "x":    ( float ),
                            "y":    ( float ),
                            "slots":
                            {
                                "items":    1,
                                "0":
                                {
                                    "0":    ( float ),
                                    "1":    ( float ),
                                    "2":    ( float )
                                }
                            }
                        }

                    ~ "radiating plane":
                        {
                            "l":    ( float ),
                            "w":    ( float ),
                            "x":    ( float ),
                            "y":    ( float ),
                            "slots":
                            {
                                "items":    1,
                                "0":
                                {
                                    "0":    ( float ),
                                    "1":    ( float ),
                                    "2":    ( float )
                                }
                            }
                        }

                    ~ "substrate":
                        {
                            "l":    ( float ),
                            "w":    ( float ),
                            "h":    ( float ),
                            "x":    ( float ),
                            "y":    ( float ),
                            "permitivitty": ( float ),
                            "loss": ( float ),
                            "name": ( str )
                        }

                + frequency = ( dict ) A dictionary containing the data for
                    the frequency simulations
                    ~ Required

                    ~ "center"  = ( float )
                    ~ "start"   = ( float )
                    ~ "end"     = ( float )
                    ~ "samples" = ( int )

                + mesh  = ( dict ) Dictionary containing the data for the
                    meshing of the patch antenna
                    ~ Required

                    ~ "wire radius" = ( float )
                    ~ "size"        = ( str )
                        - "Coarse"
                        - "Standard"
                        - "Fine"

                + runt  = ( dict ) Dictionary containing the runtime data for 
                    the patch antenna project
                    ~ Required

                    ~ "parallel"    = ( bool )
                    ~ "run"         = ( bool )
                    ~ "interactive" = ( bool )

                + fitness   = ( dict ) A dcitionary containing the data for
                    the frequency fitness evaluations
                    ~ "desired" : { "start" = ( float ), "end" = ( float ) }

            |\n

            Returns:

                + lOut  = ( list ) A list containing the fitness information
                    for the passed list of antenna
                    ~ dir   = ( str ) Path of the .out
                    ~ fitness    = ( fitness ) Information from the fitness
                        evaluations
        """

        #   STEP 0: Local variables
        lurkhei                 = None

        vConny                  = Conny()

        lOut                    = []

        sName                   = Helga.ticks()

        #   STEP 1: Setup - Local variables
        vConny.load(en.Mathew.value)
        
        #   region STEP 2->13: Error checking

        #   STEP 2: Check if dir arg passed
        if ("dir" not in kwargs):
            #   STEP 3: Error handling
            raise Exception("An error occured in Matthew.getPatch_Json() -> Step 2: No dir arg passed")

        #   STEP 4: Check if ant arg passed
        if ("ant" not in kwargs):
            #   STEP 5: Error handling
            raise Exception("An error occured in Matthew.getPatch_Json() -> Step 4: No ant arg passed")

        #   STEP 6: check if ant arg valid
        if (type(kwargs["ant"]) != list):
            #   STEP 7: Error handling
            raise Exception("An error occured in Matthew.getPatch_Json() -> Step 6: Invali ant arg passed")

        #   STEP 8: Check if mesh arg passed
        if ("mesh" not in kwargs):
            #   STEP 9: Error handling
            raise Exception("An error occured in Matthew.getPatch_Json() -> Step 8: No mesh arg passed")

        #   STEP 10: Check if runt arg passed
        if ("runt" not in kwargs):
            #   STEP 11: error handling
            raise Exception("An error occured in Matthew.getPatch_Json() -> Step 10: No runt arg passed")
        
        #   STEP 12: Check if frequency arg passed
        if ("frequency" not in kwargs):
            #   STEP 13: Error handling
            raise Exception("An error occured in Matthew.getPatch_Json() -> Step 12: No frequency arg passed")
        
        #
        #   endregion

        #   STEP 14: Setup - local variables
        lurkhei = Lana(name=sName, dir=kwargs["dir"], units="Millimetres")

        #   STEP 15: Loop through antenna
        for i in range(0, len(kwargs["ant"])):
            #   STEP 16: Get temp antenna
            dTmp_Ant    = kwargs["ant"][i]

            iTmp_Faces  = 0

            #   STEP 17: Create a new antenna project
            lurkhei.newAntenna(name=str(i))

            #   region STEP 18->26: Create feed

            #   STEP 18: Setup - Temp variables
            fTmp_X  = dTmp_Ant["radiating plane"]["x"]  + dTmp_Ant["radiating plane"]["l"]
            fTmp_Y  = dTmp_Ant["feed"]["center"]        - dTmp_Ant["feed"]["width"] / 2.0

            #   STEP 19: Setup - Surface corners
            dTmp_Corner = {
                "items": 4,
                "0":
                {
                    "x": fTmp_X,
                    "y": fTmp_Y,
                    "z": dTmp_Ant["substrate"]["h"]
                },
                "1":
                {
                    "x": fTmp_X,
                    "y": dTmp_Ant                   + dTmp_Ant["feed"]["width"],
                    "z": dTmp_Ant["substrate"]["h"]
                },
                "2":
                {
                    "x": dTmp_Ant["substrate"]["l"] + dTmp_Ant["substrate"]["x"] + dTmp_Ant["substrate"]["h"],
                    "y": fTmp_Y                     + dTmp_Ant["feed"]["width"],
                    "z": dTmp_Ant["substrate"]["h"]
                },
                "3":
                {
                    "x": dTmp_Ant["substrate"]["l"] + dTmp_Ant["substrate"]["x"] + dTmp_Ant["substrate"]["h"],
                    "y": fTmp_Y,
                    "z": dTmp_Ant["substrate"]["h"]
                }
            }

            #   STEP 20: Setup - Create surface and update faces
            sFeed_Top = lurkhei.newASurface(surface="Polygon", corner=dTmp_Corner, label="Feed_Top")

            iTmp_Faces += 1

            #   STEP 21: Setup - Create positive feed face corners
            dTmp_Corner = {
                "items": 4,
                "0":
                {
                    "x": dTmp_Ant["substrate"]["l"] + dTmp_Ant["substrate"]["x"] + dTmp_Ant["substrate"]["h"],
                    "y": fTmp_Y + dTmp_Ant["feed"]["width"],
                    "z": dTmp_Ant["substrate"]["h"]
                },
                "1":
                {
                    "x": dTmp_Ant["substrate"]["l"] + dTmp_Ant["substrate"]["x"] + dTmp_Ant["substrate"]["h"],
                    "y": fTmp_Y + dTmp_Ant["feed"]["width"],
                    "z": dTmp_Ant["substrate"]["h"] / 2.0
                },
                "2":
                {
                    "x": dTmp_Ant["substrate"]["l"] + dTmp_Ant["substrate"]["x"] + dTmp_Ant["substrate"]["h"],
                    "y": fTmp_Y,
                    "z": dTmp_Ant["substrate"]["h"] / 2.0
                },
                "3":
                {
                    "x": dTmp_Ant["substrate"]["l"] + dTmp_Ant["substrate"]["x"] + dTmp_Ant["substrate"]["h"],
                    "y": fTmp_Y,
                    "z": dTmp_Ant["substrate"]["h"]
                }
            }

            #   STEP 22: Setup - Create surface and update faces
            sFeed_Pos   = lurkhei.newASurface(surface="Polygon", corner=dTmp_Corner, label="Feed_Pos")
            
            iTmp_Faces  += 1

            #   STEP 23: Setup - Create negative feed face corners
            dTmp_Corner = {
                "items": 4,
                "0":
                {
                    "x": dTmp_Ant["substrate"]["l"] + dTmp_Ant["substrate"]["x"] + dTmp_Ant["substrate"]["h"],
                    "y": fTmp_Y + dTmp_Ant["feed"]["width"],
                    "z": 0.0
                },
                "1":
                {
                    "x": dTmp_Ant["substrate"]["l"] + dTmp_Ant["substrate"]["x"] + dTmp_Ant["substrate"]["h"],
                    "y": fTmp_Y + dTmp_Ant["feed"]["width"],
                    "z": dTmp_Ant["substrate"]["h"] / 2.0
                },
                "2":
                {
                    "x": dTmp_Ant["substrate"]["l"] + dTmp_Ant["substrate"]["x"] + dTmp_Ant["substrate"]["h"],
                    "y": fTmp_Y,
                    "z": dTmp_Ant["substrate"]["h"] / 2.0
                },
                "3":
                {
                    "x": dTmp_Ant["substrate"]["l"] + dTmp_Ant["substrate"]["x"] + dTmp_Ant["substrate"]["h"],
                    "y": fTmp_Y,
                    "z": 0.0
                }
            }

            #   STEP 24: Setup - Create surface and update faces
            sFeed_Neg   = lurkhei.newASurface(surface="Polygon", corner=dTmp_Corner, label="Feed_Neg")
            
            iTmp_Faces  += 1

            #   STEP 25: Setup - Create bot feed strip corners
            dTmp_Corner = {
                "items": 4,
                "0":
                {
                    "x": dTmp_Ant["substrate"]["l"] + dTmp_Ant["substrate"]["x"] + dTmp_Ant["substrate"]["h"],
                    "y": fTmp_Y,
                    "z": 0.0
                },
                "1":
                {
                    "x": dTmp_Ant["substrate"]["l"] + dTmp_Ant["substrate"]["x"] + dTmp_Ant["substrate"]["h"],
                    "y": fTmp_Y + dTmp_Ant["feed"]["width"],
                    "z": 0.0
                },
                "2":
                {
                    "x": dTmp_Ant["ground plane"]["l"] + dTmp_Ant["ground plane"]["x"],
                    "y": fTmp_Y + dTmp_Ant["feed"]["width"],
                    "z": 0.0
                },
                "3":
                {
                    "x": dTmp_Ant["ground plane"]["l"] + dTmp_Ant["ground plane"]["x"],
                    "y": fTmp_Y,
                    "z": 0.0
                }
            }

            #   STEP 26: Setup - Create surface and update faces
            sFeed_Bot   = lurkhei.newASurface(surface="Polygon", corner=dTmp_Corner, label="Feed_Bot")
            
            iTmp_Faces  += 1

            #
            #   endregion

            #   region STEP 27: Create ground plane

            dTmp_Corner = {
                "x":    dTmp_Ant["ground plane"]["x"],
                "y":    dTmp_Ant["ground plane"]["y"],
                "z":    0.0
            }

            dTmp_Dim    = {
                "l":    dTmp_Ant["ground plane"]["l"],
                "w":    dTmp_Ant["ground plane"]["w"]
            }

            sGPlane     = lurkhei.newASurface(surface="Rectangle", corner=dTmp_Corner, dimensions=dTmp_Dim, label="GP")
            
            iTmp_Faces  += 1

            #
            #   endregion
            
            #   region STEP 28->46: Add slots to ground plane

            #   STEP 28: Check if there are slots
            if (dTmp_Ant["ground plane"]["slots"]["items"] > 0):
                #   STEP 29: Setup - Scope variables
                dTmp_Slots  = dTmp_Ant["ground plane"]["slots"]

                dSubs   = {
                    "items": dTmp_Slots["items"]
                }

                #   STEP 30: Loop through slots
                for j in range(0, dTmp_Slots["items"]):
                    #   STEP 31: Get curr slot
                    dTmp_CurrSlot   = dTmp_Slots[str(j)]

                    #   STEP 32: Check if square
                    if (dTmp_CurrSlot["type"]   == "square"):
                        #   STEP 33: Setup - Square slot top-left corner
                        dTmp_Corner = {
                            "x":    dTmp_CurrSlot["x"],
                            "y":    dTmp_CurrSlot["y"],
                            "z":    0.0
                        }

                        #   STEP 34: Setup - Square slot dimenions
                        dTmp_Dim    = {
                            "l":    dTmp_CurrSlot["l"],
                            "w":    dTmp_CurrSlot["w"]
                        }

                        #   STEP 35: Setup - Create square/rect surface
                        sTmp_GPSlot     = lurkhei.newASurface(surface="Rectangle", corner=dTmp_Corner, dimensions=dTmp_Dim, label="GPSlot_" + str(j))

                        dSubs[str(j)]   = sTmp_GPSlot

                        #   STEP 36: Update - Faces
                        iTmp_Faces      += 1

                    #   STEP 37: Check if circle/ellipse
                    elif (dTmp_CurrSlot["type"] == "ellipse"):
                        #   STEP 38: Setup - Elliptical slot center
                        dTmp_Corner = {
                            "x":    dTmp_CurrSlot["x"],
                            "y":    dTmp_CurrSlot["y"],
                            "z":    0.0
                        }

                        #   STEP 39: Setup - Elliptical slot dimensions
                        dTmp_Dim    = {
                            "l":    dTmp_CurrSlot["l"],
                            "w":    dTmp_CurrSlot["w"]
                        }

                        #   STEP 40: Setup - Create elliptical surface
                        sTmp_GPSlot     = lurkhei.newASurface(surface="Ellipse", corner=dTmp_Corner, dimensions=dTmp_Dim, label="GPSlot_" + str(j))

                        dSubs[str(j)]   = sTmp_GPSlot

                        #   STEP 41: Update - Faces
                        iTmp_Faces      += 1

                    #   STEP 42: Check if triangle or polygon
                    elif ((dTmp_CurrSlot["type"] == "triangle") or (dTmp_CurrSlot["type"] == "polygon")):
                        #   STEP 43: Check that there are at least three points in polygon
                        if (dTmp_CurrSlot["items"] < 3):
                            #   STEP 44: Error handling
                            raise Exception("An error occured in Matthew.simulateCandidates_Json() -> Step 43: Polygon has less than three corners")

                        #   STEP 45: Setup - Create polygonal surface
                        sTmp_GPSlot     = lurkhei.newASurface(surface="Polygon", corner=cp.deepcopy(dTmp_CurrSlot))

                        dSubs[str(j)]   = sTmp_GPSlot

                        #   STEP 42: Update - Faces
                        iTmp_Faces      += 1

                    #   STEP 43: Unrecognized surface type
                    else:   
                        #   STEP 44: Error handling
                        raise Exception("An error occured in Matthew.simulateCandidates_Json() -> Step 44: Unrecognized surface type")
                    
                #   STEP 45: Create parts dictionary
                dTmp_Parts = {
                    "target":   sGPlane,
                    "subs":     dSubs
                }

                #   STEP 46: Perform subtraction
                sGPlane = lurkhei.newAModification(mod="Subtract", parts=dTmp_Parts, label="GP_Slotted")

            #
            #   endregion

            #   region STEP 47->50: Create substrate

            #   STEP 47: Setup - Create new medium
            lurkhei.newAMedium(label=dTmp_Ant["substrate"]["name"], permitivitty=dTmp_Ant["substrate"]["permitivitty"], loss=dTmp_Ant["substrate"]["loss"])
            
            #   STEP 48: Setup - Substrate args
            dTmp_Corner = {
                "x": dTmp_Ant["substrate"]["x"],
                "y": dTmp_Ant["substrate"]["y"],
                "z": 0.0
            }

            dTmp_Dim    = {
                "l": dTmp_Ant["substrate"]["l"],
                "w": dTmp_Ant["substrate"]["w"],
                "h": dTmp_Ant["substrate"]["h"]
            }

            #   STEP 49: Setup - Create substrate
            sSubstrate  = lurkhei.newASolid(solid="Cuboid", corner=dTmp_Corner, dimensions=dTmp_Dim, label="Substrate")

            lurkhei.setASolidMedium(medium=dTmp_Ant["substrate"]["name"], solid=sSubstrate)

            #   STPE 50: Update - Faces
            iTmp_Faces  += 6

            #
            #   endregion

            #   region STEP 51->53: Create radiating plane

            #   STEP 51: Create RPlane atgs
            dTmp_Corner = {
                "x":    dTmp_Ant["radiating plane"]["x"],
                "y":    dTmp_Ant["radiating plane"]["y"],
                "z":    dTmp_Ant["substrate"]["h"]
            }

            dTmp_Dim    = {
                "l":    dTmp_Ant["radiating plane"]["l"],
                "w":    dTmp_Ant["radiating plane"]["w"]
            }

            #   STEP 52: Create RPlane
            sRPlane = lurkhei.newASurface(surface="Rectangle", corner=dTmp_Corner, dimensions=dTmp_Dim, label="RP")

            #   STEP 53: Update - Faces
            iFaces += 1

            #
            #   endregion

            #   region STEP 54->76: Create slotted RPlane

            #   STEP 54: Check if there are slots in RPlane
            if (dTmp_Ant["radiating plane"]["slots"]["items"] > 0):
                #   STEP 55: Setup - Scope variables
                dTmp_Slots  = dTmp_Ant["radiating plane"]["slots"]

                dSubs   = {
                    "items":    dTmp_Slots["items"]
                }

                #   STEP 56: Loop through slots
                for j in range(0, dTmp_Slots["items"]):
                    #   STEP 57: Get curr slot
                    dTmp_CurrSlot = dTmp_Slots[str(j)]

                    #   STEP 58: Check if square
                    if (dTmp_CurrSlot["type"] == "square"):
                        #   STEP 59: Setup - Square slot top-left corner
                        dTmp_Corner = {
                            "x":    dTmp_CurrSlot["x"],
                            "y":    dTmp_CurrSlot["y"],
                            "z":    dTmp_Ant["substrate"]["h"]
                        }

                        #   STEP 60: Setup - Square slot dimensions
                        dTmp_Dim    = {
                            "l":    dTmp_CurrSlot["l"],
                            "w":    dTmp_CurrSlot["w"]
                        }

                        #   STPE 61: Setup - Create square/rect surface
                        sTmp_RPSlot     = lurkhei.newASurface(surface="Rectangle", corner=dTmp_Corner, dimensions=dTmp_Dim, label="RPSlot_" + str(j))

                        dSubs[str(j)]   = sTmp_RPSlot

                        #   STEP 62: Update - Faces
                        iTmp_Faces      += 1

                    #   STEP 63: Check if ellipse
                    elif (dTmp_CurrSlot["type"] == "ellipse"):
                        #   STEP 64: Setup - Elliptical slot center
                        dTmp_Corner = {
                            "x":    dTmp_CurrSlot["x"],
                            "y":    dTmp_CurrSlot["y"],
                            "z":    dTmp_Ant["substrate"]["h"]
                        }

                        #   STEP 65: Setup - Elliptical slot dimensions
                        dTmp_Dim    = {
                            "l":    dTmp_CurrSlot["l"],
                            "w":    dTmp_CurrSlot["w"]
                        }

                        #   STEP 66: Setup - Create elliptical surface
                        sTmp_RPSlot     = lurkhei.newASurface(surface="Ellipse", corner=dTmp_Corner, dimensions=dTmp_Dim, label="RPSlot_" + str(j))

                        dSubs[str(j)]   = sTmp_RPSlot

                        #   STEP 67: Update - Faces
                        iTmp_Faces      += 1

                    #   STEP 68: Check if triangle or polygon
                    elif ((dTmp_CurrSlot["type"] == "triangle") or (dTmp_CurrSlot["type"] == "polygon")):
                        #   STEP 69: Check that there are at least three points in polygon
                        if (dTmp_CurrSlot["items"] < 3):
                            #   STEP 70: Error handling
                            raise Exception("An error occured in Matthew.simulateCandidates_Json() -> Stpe 69: Polygon has less than three corners")

                        #   STEP 71: Setup - Create polygonal surface
                        sTmp_RPSlot     = lurkhei.newASurface(surface="Polygon", corner=cp.deepcopy(dTmp_CurrSlot))

                        dSubs[str(j)]   = sTmp_RPSlot

                        #   STEP 72: Update - Faces
                        iTmp_Faces      += 1

                    #   STEP 73: Unrecognized surface type
                    else:
                        #   STEP 74: Error handling
                        raise Exception("An error occured in Matthew.simulateCandidates_Json() -> Step 73: Unrecognized surface")

                #   STEP 75: Create parts dictionary
                dTmp_Parts  = {
                    "target":   sRPlane,
                    "subs":     dSubs
                }

                #   STEP 76: Perform subtraction
                sRPlane     = lurkhei.newAModification(mod="Subtract", parts=dParts, label="RP_Slotted")

            #
            #   endregion

            #   region STEP 77: Create union

            dParts = {
                "items": 7,
                "0": sGPlane,
                "1": sRPlane,
                "2": sSubstrate,
                "3": sFeed_Top,
                "4": sFeed_Pos,
                "5": sFeed_Neg,
                "6": sFeed_Bot
            }

            sUnion = lurkhei.newAModification(mod="Union", parts=dParts, label="Onion")

            #
            #   endregion

            #   region STEP 78: Reset face media

            lurkhei.setAFaceMedium(medium="Perfect electric conductor", face="Face" + str(iFaces + 1), union=sUnion)
            lurkhei.setAFaceMedium(medium="Perfect electric conductor", face="Face" + str(iFaces + 2), union=sUnion)
            lurkhei.setAFaceMedium(medium="Perfect electric conductor", face="Face" + str(iFaces + 3), union=sUnion)

            #
            #   endregion

            #   region STEP 79: Create new port

            dTmp_Pos = {
                "items": 1,
                "0": "Face2"
            }

            dTmp_Neg = {
                "items":1,
                "0": "Face3"
            }

            sPort = lurkhei.newAPort(port="Edge", union=sUnion, label="SourcePort", pos=dTmp_Pos, neg=dTmp_Neg)

            #
            #   endregion

            #   region STEP 80: Create voltage source

            lurkhei.newASource(source="Voltage", port=sPort, label="VoltageSource")

            #
            #   endregion

            #   region STEP 81->83: Set frequency and mesh

            #   STEP 81: Check if frequency arg passed
            if ("frequency" in kwargs):
                #   STEP 82: Set frequency
                lurkhei.setAFrequency(start=kwargs["frequency"]["start"], end=kwargs["frequency"]["end"], range_type="Linear", samples=kwargs["frequency"]["samples"])

            #   STEP 83: Set mesh
            lurkhei.setAMesh(wire_radius=kwargs["mesh"]["wire radius"], size=kwargs["mesh"]["size"])

            #
            #   endregion

            #   region STEP 84->86: Save and close project

            #   STEP 84: Save antenna project
            lurkhei.saveAntenna(dir=str(i))

            #   STEP 85: Set project to simulate
            lurkhei.simulateAntenna(parallel=kwargs["runt"]["parallel"])

            #   STEP 86: Close project
            lurkhei.closeAntenna()

            #
            #   endregion

        #   STEP 87: Run script
        lurkhei.exportLua(replace=True, run=kwargs["runt"]["run"], interactive=kwargs["runt"]["interactive"])

        #   STEP 88: Loop through antenna
        for i in range(0, len(kwargs["ant"])):
            #   STEP 89: Get path for this sim
            #sPath = kwargs["dir"] + "\\" + sName + "_" + str(i) + "\\" + str(i) + ".out"
            sPath = kwargs["dir"] + sName + "_" + str(i) + "\\" + str(i) + ".out"

            #   STEP 90: Create temp dictionary
            dTmp = {
                "dir": sPath,
                "fitness": Matthew.getFitness(dir=sPath, frequency=kwargs["fitness"], params=vConny.data["parameters"])
            }

            #   STEP 91: Append to output list
            lOut.append(dTmp)

        #   STEP 92: Return
        return lOut

    #
    #   endregion
    
    #
    #endregion

    #region Back-End

    #   region Back-End: Gets

    @classmethod
    def __getFitness_Frequency__(self, **kwargs) -> dict:
        """
            Description:

                Bitch I got the mac or the .40, turn a bitch to some macaroni.

            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:

                + dir   = ( str ) The path of the .out file to use for the
                    fitness evaluation
                    ~ Required

                + frequency = ( dict ) A dictionary that contains the relevant
                    information for the fitness evaluation
                    ~ Required

                    ~ "desired" : { "start" = ( float ), "end" = ( float ) }

                + params    = ( dict ) A dictionary containing the parameters
                    for the fitness evaluation
                    ~ "offset"  = ( float )
                    ~ "divisor" = ( float )

            |\n

            Returns:

                + dFitness  = ( dict ) A dictionary containing the results of
                    the fitness evaluation
                    ~ "in range":   ( float ) Total fitness of samples inside
                        desired range
                    
                    ~ "left range": ( float ) Total fitnees of samples to the
                        left of the desired range

                    ~ "right range":    ( float ) Total fitness of samples to
                        the right of the desired range

                    ~ "in samples": ( int ) Number of samples inside the
                        desired range

                    ~ "left samples":   ( int ) Number of samples to the left
                        of the desired range

                    ~ "right samples":  ( int ) Number of samples to the right
                        of the desired range

                    ~ "full range": ( bool ) Flag that states if the entirety
                        of the desired range was sampled

                + offset    = ( float ) The offset for the data in the
                    activation function

            |\n

            ToDo:

                + Recount steps
        """

        #   STEP 0: Local variables
        vFile                   = None
        lData                   = None

        dOut                    = None

        fDesired_Lower          = None
        fDesired_Upper          = None

        fResonant_Frequency     = None
        fResonant_Fitness       = None

        fLower_Sum              = 0.0
        fLower_Samples          = 0

        fDesired_Sum            = 0.0
        fDesired_Samples        = 0
        
        fUpper_Sum              = 0.0
        fUpper_Samples          = 0

        vActivations            = Antonio()

        #   STEP 1: Setup - Local variables
        
        #   region STEP 2->9: Error checking

        #   STEP 2: Check if dir arg passed
        if ("dir" not in kwargs):
            #   STEP 3: Error handling
            raise Exception("An error occured in Matthew.__getFitness_Frequency__() -> Step 2: No dir arg passed")

        #   STEP 4: Check if file exists
        if (os.path.exists(kwargs["dir"]) == False):
            print("\n\n\tAn error occured in Matthew.__getFitness_Frequency__() -> Step 4: Specified .out file does not exist")
            
            dOut ={
                "lower":
                {
                    "sum":      np.inf,
                    "samples":  np.inf,
                    "total":    np.inf
                },
                "desired":
                {
                    "sum":      np.inf,
                    "samples":  np.inf,
                    "total":    np.inf
                },
                "upper":
                {
                    "sum":      np.inf,
                    "samples":  np.inf,
                    "total":    np.inf
                },
                "resonant frequency": 0
            }

            return dOut

        #   STEP 6: check if frequency arg passed
        if ("frequency" not in kwargs):
            #   STEP 7: Error handling
            raise Exception("An error occured in Matthew.__getFitness_Frequency__() -> Step 6: No frequency arg passed")
        
        #   STEP 8: Check if params arg passed
        if ("params" not in kwargs):
            #   STEP 9: Error handling
            raise Exception("An error occured in Matthew.__getFitness_Frequency__() -> Step 8: No params arg passed")

        #
        #   endregion

        #   STEP 10: Update - Local variables
        fDesired_Lower = kwargs["frequency"]["desired"]["start"]
        fDesired_Upper = kwargs["frequency"]["desired"]["end"]
            
        #   STEP 11: Be safe OwO
        try:
            #   region STEP 12->23: Data acquisition

            #   STEP 12: Open file
            with open(kwargs["dir"], "r+") as vFile:
                #   STEP 13: Read data from file
                lData = vFile.readlines()

            #   STEP 14: Tmp vars
            lData_Actual    = []
            lData_F         = None
            lData_S         = None

            #   STEP 15: Loop through data
            for i in range(0, len(lData)):
                #   STEP 16: Check if this line contains frequency
                if (" Frequency in Hz:               FREQ =    " in lData[i]):
                    #   STEP 17: Set tmp Frequency var
                    lData_F = lData[i].strip(" Frequency in Hz:               FREQ =    ")
                    lData_F = self.__cleanString__(lData_F)

                #   STEP 18: Check if line contains s11 param
                elif ("         Sum |S|^2 of these S-parameters:    " in lData[i]):
                    #   STEP 19: Save to tmp S11 var
                    lData_S = lData[i].strip("         Sum |S|^2 of these S-parameters:    ")
                    lData_S = self.__cleanString__(lData_S)

                    iData_S = lData_S.find("  ")

                    lData_S = lData_S[iData_S:]

                    #   STEP 20: Get fitness safely
                    try:
                        fTmp_Fitness = float(lData_S)
                    
                    except:
                        fTmp_Fitness = 0.0

                    #   STEP 21: Save to temp dictionary
                    dTmp_Data = {
                        "frequency":    float(lData_F),
                        "fitness":      fTmp_Fitness
                    }

                    #   STEP 22: Append to actual data list
                    lData_Actual.append(dTmp_Data)

                    #   STEP 23: Clear tmp variables
                    lData_F = None
                    lData_S = None

            #
            #   endregion

            #   region STEP 24->34: Data modification

            #   STEP 24: Update - Local variables
            fResonant_Fitness   = np.inf

            #   STEP 25: Loop through actual data
            for i in range(0, len(lData_Actual)):
                #   STEP 26: Get tmp var
                dTmp            = lData_Actual[i]
                fTmp_Fitness    = vActivations.logistic( ( dTmp["fitness"] + kwargs["params"]["offset"] ) / kwargs["params"]["divisor"] )

                #   STEP 27: Check if frequency in lower
                if (dTmp["frequency"] < fDesired_Lower):
                    #   STEP 28: Update - Local variables
                    fLower_Sum      += fTmp_Fitness
                    fLower_Samples  += 1

                #   STEP 29: Check if in desired range
                elif (dTmp["frequency"] < fDesired_Upper):
                    #   STEP 30: Update - Local variables
                    fDesired_Sum        += fTmp_Fitness
                    fDesired_Samples    += 1

                #   STEP 31: Then has to be upper range
                else:
                    #   STEP 32: Update - Local variables
                    fUpper_Sum      += fTmp_Fitness
                    fUpper_Samples  += 1

                #   STEP 33: Check if Fr
                if (dTmp["fitness"] < fResonant_Fitness):
                    #   STEP 34: Set new Fr
                    fResonant_Frequency = dTmp["frequency"]
                    fResonant_Fitness   = dTmp["fitness"]
            
            #
            #   endregion

            #   region STEP 35->38: Update lower Sum and Product

            #   STEP 35: Check that there were samples
            if (fLower_Samples > 0):
                #   STEP 36: Update sum
                fLower_Sum      = fLower_Sum / float( fLower_Samples )

            else:
                #   STEP 38: Set default values
                fLower_Sum      = 0.0

            #
            #   endregion

            #   region STEP 39->42: Update desired Sum and Product

            #   STEP 39: Check that there were samples
            if (fDesired_Samples > 0):
                #   STEP 40: Update sum
                fDesired_Sum        = fDesired_Sum / float( fDesired_Samples )

            else:
                #   STPE 42: Set defaults
                fDesired_Sum        = 0.0

            #
            #   endregion

            #   region STEP 43->46: Update upper Sum & Product

            #   STEP 43: Check that there were samples
            if (fUpper_Samples > 0):
                #   STEP 44: Update sum
                fUpper_Sum      = fUpper_Sum / float( fUpper_Samples )

            else:
                #   STEP 46: Set defaults
                fUpper_Sum      = 0.0

            #
            #   endregion

        except Exception as ex:
            #   STEP 41: Error handling
            print("Initial error: ", ex)
            raise Exception("An error occured in Matthew.__getFitness_Frequency__()")

        finally:
            #   STEP 42: Check if file closed
            if (vFile != None):
                #   STEP 43: Close file
                vFile.close()
                vFile = None

        #   STEP 44: Populate output var
        Helga.nop()
        dOut ={
            "lower":
            {
                "sum":      fLower_Sum,
                "samples":  fLower_Samples,
                "total":    fLower_Sum
            },
            "desired":
            {
                "sum":      fDesired_Sum,
                "samples":  fDesired_Samples,
                "total":    fDesired_Sum
            },
            "upper":
            {
                "sum":      fUpper_Sum,
                "samples":  fUpper_Samples,
                "total":    fUpper_Sum
            },
            "resonant frequency": fResonant_Frequency
        }

        #   STEP 45: Return
        return dOut

    #
    #   endregion

    #   region Back-End: String handling

    @classmethod
    def __cleanString__(self, _s: str) -> str:
        """
            Description:

                Removes " ", "\t", and "\n" from the passed string.

            |\n
            |\n
            |\n
            |\n
            |\n

            Parameters:

                + _s    = ( str ) The string to clean

            |\n

            Returns:

                + sOut  = ( str ) The cleaned string
        """

        #   STEP 0: Local variables
        sOut                    = cp.deepcopy(_s)

        #   STEP 1: Setup - Local variables

        #   STEP 2: Clean string
        sOut = sOut.strip(" ")
        sOut = sOut.strip("\t")
        sOut = sOut.strip("\n")
        sOut = sOut.strip("   ")

        #   STEP 3: Return
        return sOut

    
    #
    #   endregion

    #
    #endregion

#
#endregion

#region Testing

if (__name__ == "__main__"):
    os.system("cls")

    sDir    = "C:\\Users\\project\\0. My Work\\1. Repositories\\0. Unfriendly Train\\Code\\Templates\\Tests\\Lua"

    dSubstrate = {
        "name":         "FR4",
        "height":       1.6,
        "permitivitty": 4.4,
        "loss tangent": 0.02
    }

    dFrequency = {
        "center":       0.92e9,
        "start":        0.88e9,
        "end":          0.96e9,
        "samples":      19
    }

    dMesh = {
        "wire radius":  0.001,
        "size":         "Fine"
    }

    dRunt = {
        "parallel":     True,
        "run":          True,
        "interactive":  True
    }

    dFitness = {
        "desired":
        {
            "start":    0.9e9,
            "end":      0.94e9
        }
    }

    lAnt = []

    dTmp = {
        "feed":
        {
            "center": 54.37823,
            "width": 1.6
        },
        "ground plane":
        {
            "l": 87.08759,
            "w": 108.75646,
            "x": 0.0,
            "y": 0.0,
            "slots":
            {
                "items": 0
            }
        },
        "radiating plane":
        {
            "l": 77.48759,
            "w": 99.15646,
            "x": 4.8,
            "y": 4.8,
            "slots":
            {
                "items": 0
            }
        },
        "substrate":
        {
            "h": 1.6,
            "l": 87.08759,
            "w": 108.75646,
            "x": 0.0,
            "y": 0.0,
            "permitivitty": 4.4,
            "loss": 0.02,
            "name": "FR4"
        }
    }

    lAnt.append(dTmp)

    dTmp = {
        "feed":
        {
            "center": 54.37823,
            "width": 1.6
        },
        "ground plane":
        {
            "l": 87.08759,
            "w": 108.75646,
            "x": 0.0,
            "y": 0.0,
            "slots":
            {
                "items": 1,
                "0":
                {
                    "items": 3,
                    "0":
                    {
                        "x": 2.0,
                        "y": 2.0,
                        "z": 0.0
                    },
                    "1":
                    {
                        "x": 4.0,
                        "y": 4.0,
                        "z": 0.0
                    },
                    "2":
                    {
                        "x": 2.0,
                        "y": 4.0,
                        "z": 0.0
                    }
                }
            }
        },
        "radiating plane":
        {
            "l": 77.48759,
            "w": 99.15646,
            "x": 4.8,
            "y": 4.8,
            "slots":
            {
                "items": 0
            }
        },
        "substrate":
        {
            "h": 1.6,
            "l": 87.08759,
            "w": 108.75646,
            "x": 0.0,
            "y": 0.0,
            "permitivitty": 4.4,
            "loss": 0.02,
            "name": "FR4"
        }
    }

    lAnt.append(dTmp)

    dTmp = {
        "feed":
        {
            "center": 54.37823,
            "width": 1.6
        },
        "ground plane":
        {
            "l": 87.08759,
            "w": 108.75646,
            "x": 0.0,
            "y": 0.0,
            "slots":
            {
                "items": 2,
                "0":
                {
                    "items": 3,
                    "0":
                    {
                        "x": 2.0,
                        "y": 2.0,
                        "z": 0.0
                    },
                    "1":
                    {
                        "x": 4.0,
                        "y": 4.0,
                        "z": 0.0
                    },
                    "2":
                    {
                        "x": 2.0,
                        "y": 4.0,
                        "z": 0.0
                    }
                },
                "1":
                {
                    "items": 3,
                    "0":
                    {
                        "x": 12.0,
                        "y": 12.0,
                        "z": 0.0
                    },
                    "1":
                    {
                        "x": 14.0,
                        "y": 14.0,
                        "z": 0.0
                    },
                    "2":
                    {
                        "x": 12.0,
                        "y": 14.0,
                        "z": 0.0
                    }
                }
            }
        },
        "radiating plane":
        {
            "l": 77.48759,
            "w": 99.15646,
            "x": 4.8,
            "y": 4.8,
            "slots":
            {
                "items": 0
            }
        },
        "substrate":
        {
            "h": 1.6,
            "l": 87.08759,
            "w": 108.75646,
            "x": 0.0,
            "y": 0.0,
            "permitivitty": 4.4,
            "loss": 0.02,
            "name": "FR4"
        }
    }

    lAnt.append(dTmp)

    dTmp = {
        "feed":
        {
            "center": 54.37823,
            "width": 1.6
        },
        "ground plane":
        {
            "l": 87.08759,
            "w": 108.75646,
            "x": 0.0,
            "y": 0.0,
            "slots":
            {
                "items": 3,
                "0":
                {
                    "items": 3,
                    "0":
                    {
                        "x": 2.0,
                        "y": 2.0,
                        "z": 0.0
                    },
                    "1":
                    {
                        "x": 4.0,
                        "y": 4.0,
                        "z": 0.0
                    },
                    "2":
                    {
                        "x": 2.0,
                        "y": 4.0,
                        "z": 0.0
                    }
                },
                "1":
                {
                    "items": 3,
                    "0":
                    {
                        "x": 12.0,
                        "y": 12.0,
                        "z": 0.0
                    },
                    "1":
                    {
                        "x": 14.0,
                        "y": 14.0,
                        "z": 0.0
                    },
                    "2":
                    {
                        "x": 12.0,
                        "y": 14.0,
                        "z": 0.0
                    }
                },
                "2":
                {
                    "items": 3,
                    "0":
                    {
                        "x": 22.0,
                        "y": 22.0,
                        "z": 0.0
                    },
                    "1":
                    {
                        "x": 24.0,
                        "y": 24.0,
                        "z": 0.0
                    },
                    "2":
                    {
                        "x": 22.0,
                        "y": 24.0,
                        "z": 0.0
                    }
                }
            }
        },
        "radiating plane":
        {
            "l": 77.48759,
            "w": 99.15646,
            "x": 4.8,
            "y": 4.8,
            "slots":
            {
                "items": 0
            }
        },
        "substrate":
        {
            "h": 1.6,
            "l": 87.08759,
            "w": 108.75646,
            "x": 0.0,
            "y": 0.0,
            "permitivitty": 4.4,
            "loss": 0.02,
            "name": "FR4"
        }
    }

    lAnt.append(dTmp)

    dTmp = {
        "feed":
        {
            "center": 54.37823,
            "width": 1.6
        },
        "ground plane":
        {
            "l": 87.08759,
            "w": 108.75646,
            "x": 0.0,
            "y": 0.0,
            "slots":
            {
                "items": 3,
                "0":
                {
                    "items": 3,
                    "0":
                    {
                        "x": 2.0,
                        "y": 2.0,
                        "z": 0.0
                    },
                    "1":
                    {
                        "x": 4.0,
                        "y": 4.0,
                        "z": 0.0
                    },
                    "2":
                    {
                        "x": 2.0,
                        "y": 4.0,
                        "z": 0.0
                    }
                },
                "1":
                {
                    "items": 3,
                    "0":
                    {
                        "x": 12.0,
                        "y": 12.0,
                        "z": 0.0
                    },
                    "1":
                    {
                        "x": 14.0,
                        "y": 14.0,
                        "z": 0.0
                    },
                    "2":
                    {
                        "x": 12.0,
                        "y": 14.0,
                        "z": 0.0
                    }
                },
                "2":
                {
                    "items": 3,
                    "0":
                    {
                        "x": 22.0,
                        "y": 22.0,
                        "z": 0.0
                    },
                    "1":
                    {
                        "x": 24.0,
                        "y": 24.0,
                        "z": 0.0
                    },
                    "2":
                    {
                        "x": 22.0,
                        "y": 24.0,
                        "z": 0.0
                    }
                }
            }
        },
        "radiating plane":
        {
            "l": 77.48759,
            "w": 99.15646,
            "x": 4.8,
            "y": 4.8,
            "slots":
            {
                "items": 1,
                "0":
                {
                    "items": 3,
                    "0":
                    {
                        "x": 32.0,
                        "y": 32.0,
                        "z": 1.6
                    },
                    "1":
                    {
                        "x": 34.0,
                        "y": 34.0,
                        "z": 1.6
                    },
                    "2":
                    {
                        "x": 32.0,
                        "y": 34.0,
                        "z": 1.6
                    }
                },
            }
        },
        "substrate":
        {
            "h": 1.6,
            "l": 87.08759,
            "w": 108.75646,
            "x": 0.0,
            "y": 0.0,
            "permitivitty": 4.4,
            "loss": 0.02,
            "name": "FR4"
        }
    }

    lAnt.append(dTmp)

    lOut =Matthew.simulateCandidates_Json(dir=sDir, ant=lAnt, frequency=dFrequency, mesh=dMesh, runt=dRunt, fitness=dFitness)

    Helga.nop()

#
#endregion