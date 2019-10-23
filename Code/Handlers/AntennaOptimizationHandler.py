#region Imports

from    enum                            import Enum

import  copy                            as cp
import  json                            as js
import  numpy                           as np
import  os
import  random                          as rn
import  shutil                          as sh
import  sys

sys.path.append(os.path.abspath("."))

from    Code.Enums.Enums                import Enums            as en

from    Code.Handlers.AntennaMathHandler                        import Matthew
from    Code.Handlers.SurrogateHandler  import Golem

from    Code.Interface.MenuInterface    import Rae

from    Helpers.ActivationFunctions     import Antonio
from    Helpers.Config                  import Conny
from    Helpers.DataContainer           import Data
from    Helpers.GeneralHelpers          import Helga

#endregion

#region Class - Natalie

class Natalie:

    #region Init

    """
        Description:

            This class handles the optimization of the specified patch antenna.

        |\n
        |\n
        |\n
        |\n
        |\n

        Arguments:

            + ant   = ( dict ) A dictionary containing the parameters for the
                desired patch antenna
                ~ Required

                ~ "substrate":
                    {
                        "permitivitty": ( float ),
                        "loss": ( float ),
                        "name": ( str ),
                        "height":   ( float )
                    }

                ~ "frequency":
                    {
                        "desired":
                        {
                            "start": ( float ),
                            "end": ( float )
                        }
                    }

            + params    = ( dict ) A dictionary containing all the parameters
                for the initialization of this class. If this is passed this
                will be used for initialization instead of the default config
                file

            + overwrite = ( bool ) A flag that specifies if the default config
                file should be overwritten using <params>
                ~ Required only if <params!=None>
    """

    def __init__(self, **kwargs) -> None:

        #region STEP 0: Local variables

        self.__enum             = en.Natalie
        self.__cf               = Conny()
        self.__cf.load(self.__enum.value)

        self.__aActivation      = Antonio()

        #endregion

        #region STEP 1: Private variables

        #   region  STEP 1.1: Antenna Params

        self.__sDirectory       = None

        self.__dAnt_Substrate   = None
        self.__dAnt_Frequency   = None
        self.__dAnt_Mesh        = None
        self.__dAnt_Runt        = None
        self.__dAnt_Fitness     = None

        self.__dAnt_Center      = None
        self.__dAnt_CenterFit   = None
        self.__dAnt_Best        = None
        self.__dAnt_Template    = None

        self.__cAnt_Default     = None

        #   endregion

        #   region  STEP 1.2: TRO Params

        self.__iTRO_Iterations_Primary      = None
        self.__iTRO_Iterations_Secondary    = None
        self.__iTRO_Iterations_Grace        = None

        self.__iTRO_Candidates              = None
        self.__iTRO_Candidates_Secondary    = None

        self.__iTRO_Region                  = None
        self.__iTRO_Region_SRG              = None
        
        self.__fTRO_RegionScalar_Primary    = None
        self.__fTRO_RegionScalar_Secondary  = None
        
        self.__fTRO_EarlyExit_Area          = None
        self.__fTRO_EarlyExit_Fitness       = None

        #   endregion

        #   region STEP 1.3: TRO Runtime requirements


        #   endregion

        #endregion

        #   STEP 2: Public variables
        self.bShowOutput        = self.__cf.data["parameters"]["show output"]
        self.bEarlyExit         = False

        #region STEP 3->7: Error checking

        #   STEP 3: Check if ant arg was passed
        if ("ant" not in kwargs):
            #   STEP 4: Error handling
            raise Exception("An error occured in Natalie.__init__() -> Step 4: No ant arg passed")
        
        #   STEP 5: Check if params arg passed
        if ("params" in kwargs):
            #   STEP 6: Check if overwrite arg passed
            if ("overwrite" not in kwargs):
                #   STEP 7: Error handling
                raise Exception("An error occured in Natalie.__init__() -> Step 5: No overwrite arg passed")
        
        #
        #   endregion

        #region STEP 8->11: Init class

        #   STEP 8: Check if default init
        if ("params" in kwargs):
            #   STEP 9: Outsource init
            self.__initClass__(params=kwargs["params"], overwrite=kwargs["overwrite"])
            
        #   STEP 10: Outsource default init
        else:
            self.__initClass__()

        #   STEP 11: Init antenna params
        self.__initAnt__(ant=kwargs["ant"])
        
        #
        #endregion

        #   STEP 12: Return
        return

    #
    #endregion

    #region Front-End

    def optimizeAntenna(self, **kwargs) -> None:
        """
            Description:

                Uses multi-variate optimization to optimize a microstrip
                patch antenna for the specified frequencies.

            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:

                + primary   = ( str ) The primary optimizer for the process.
                    ~ Required

                    ~ Optionse:
                        - "tro"
                        - "nm"

                + secondary = ( str ) The secondary optimizer for the process.
                    ~ Required

                    ~ Options:
                        - "tro"
                        - "nm"

                + new   = ( bool ) Whether or not a new center microstrip patch
                    antenna should be simulated at the start of the project
                    ~ Default   = True

                + cull  = ( bool ) A flag that specifies whether of not
                    unworthy antenna candidate simulations should be deleted
                    from the local drive
                    ~ Default   = True
                    ~ Note: If this is set to false the simulations could take
                        up a lot of storage space

                + save  = ( bool ) A flag that specifies whether or not
                    continuous saving of the best candidate in an algorithm
                    should be done
                    ~ Default   = True

                + surrogate = ( bool ) A flag that specifies whether or not a
                    surrogate model should be used during the optimization 
                    process
        """

        #   STEP 0: Local variables
        dPrimary_Results        = None

        bCull                   = True
        bSave                   = True

        #   STEP 1: Setup - Local variables

        #   region STEP 2->5: Error checking

        #   STEP 2: Check if primary arg passed
        if ("primary" not in kwargs):
            #   STEP 3: Error handling
            raise Exception("An error occured in Natalie.optimizeAntenna() -> Step 2: No primary arg passed")

        #   STEP 4: Check if secondary arg passed
        if ("secondary" not in kwargs):
            #   STEP 5: Error handling
            raise Exception("An error occured in Natalie.optimizeAntenna() -> Step 4: No secondary arg passed")
        
        #
        #   endregion
        
        #   region STEP 6->9: Update - Local variables

        #   STEP 6: Check if cull arg passed
        if ("cull" in kwargs):
            #   STEP 7: Update - Local variables
            bCull   = kwargs["cull"]

        #   STEP 8: Check if save arg passed
        if ("save" in kwargs):
            #   STEP 9: Update - Local variables
            bSave   = kwargs["save"]

        #
        #   endregion
        
        #   region STEP 10->15: Primary optimization

        #   STEP 10: Check if primary is tro
        if (kwargs["primary"] == "tro"):
            #   STEP 11: Outsource
            dPrimary_Results    = self.__tro_Primary__(cull=bCull, save=bSave)

        #   STEP 12: Check if primary is nm
        elif (kwargs["primary"] == "nm"):
            #   STEP 13: Outsource
            dPrimary_Results    = self.__nm__(cull=bCull, save=bSave)

        #   STEP 14: No optimizer specified
        else:
            #   STEP 15: Return
            return

        #
        #   endregion

        #   region STEP 16->19: Secondary optimization

        #   STEP 16: Check if secondary is tro
        if (kwargs["secondary"] == "tro"):
            #   STEP 17: Outsource
            self.__tro_Secondary__(center=dPrimary_Results, cull=bCull, save=bSave)

        #   STEP 18: Check if secondary is nm
        if (kwargs["secondary"] == "nm"):
            #   STEP 19: Outsource
            self.__nm__(stage="Secondary", center=dPrimary_Results, new=False, cull=bCull, save=bSave)

        #
        #   endregion

        #   STEP 20: Return
        return
        
    #
    #endregion

    #region Back-End

    #   region Back-End: Init

    def __initClass__(self, **kwargs) -> None:
        """
            Description:

                Initializes this instance from either the default config file
                or from the provided dictionary.

            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:

                + params    = ( dict ) A dictionary containing all the parameters
                    for the initialization of this class. If this is passed this
                    will be used for initialization instead of the default config
                    file

                + overwrite = ( bool ) A flag that specifies if the default config
                    file should be overwritten using <params>
                    ~ Required only if <params!=None>
        """

        #   STEP 0: Local variables
        vConny                  = Conny()
        
        #   STEP 1: Setup - Local variables
        vConny.getDirectory()
        self.__sDirectory = os.path.abspath(".") + vConny.data["natalie"]
        
        #   STEP 2: Check if params passed
        if ("params" in kwargs):
            #   STEP 3: Validate params arg
            if (self.__validateParams__(params=kwargs["params"]) == False):
                #   STEP 4: Error handling
                raise Exception("An error occured in Natalie.__initClass__() -> Step 3: Invalid params arg passed")

            #   STEP 5: Update class config file
            self.__cf.data = kwargs["params"]

            #   STEP 6: Check if the config file should be updated
            if (kwargs["overwrite"] == True):
                #   STEP 7: Update config file
                self.__cf.update()

        #   STEP 8: Init - Class variables
        self.__dAnt_Mesh = {
            "wire radius":      self.__cf.data["parameters"]["mesh"]["wire radius"],
            "size":             self.__cf.data["parameters"]["mesh"]["size"]
        }

        self.__dAnt_Runt = {
            "parallel":         self.__cf.data["parameters"]["runt"]["parallel"],
            "run":              self.__cf.data["parameters"]["runt"]["run"],
            "interactive":      self.__cf.data["parameters"]["runt"]["interactive"]
        }

        self.__iTRO_Iterations_Primary      = self.__cf.data["parameters"]["trust region"]["primary iterations"]
        self.__iTRO_Iterations_Secondary    = self.__cf.data["parameters"]["trust region"]["secondary iterations"]
        self.__iTRO_Iterations_Grace        = self.__cf.data["parameters"]["trust region"]["grace iterations"]

        self.__iTRO_Candidates              = self.__cf.data["parameters"]["trust region"]["candidates"]
        self.__iTRO_Candidates_Secondary    = self.__cf.data["parameters"]["trust region"]["secondary candidates"]

        self.__iTRO_Region                  = self.__cf.data["parameters"]["trust region"]["algorithm region"]
        self.__iTRO_Region_SRG              = self.__cf.data["parameters"]["trust region"]["surrogate region"]
        
        self.__fTRO_RegionScalar_Primary    = self.__cf.data["parameters"]["trust region"]["primary region scalar"]
        self.__fTRO_RegionScalar_Secondary  = self.__cf.data["parameters"]["trust region"]["secondary region scalar"]

        self.__fTRO_EarlyExit_Area          = self.__cf.data["parameters"]["trust region"]["early exit conditions"]["area"]
        self.__fTRO_EarlyExit_Fitness       = self.__cf.data["parameters"]["trust region"]["early exit conditions"]["fitness"]

        #   region STEP 9->11: Retrieve default ant config

        #   STEP 9: Create tmp config holder
        cTmp = Conny()

        #   STEP 10: Load default ant config
        cTmp.load("antenna.json")

        #   STEP 11: Set class var
        self.__cAnt_Default = cTmp.data

        #
        #   endregion

        #   STEP 12: Return
        return
    
    def __initAnt__(self, **kwargs) -> None:
        """
            Description:

                Initializes the antenna parameters for this instance.

            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:

                + ant   = ( dict ) Dictionary containing parameters relevant
                    to createing the default patch
                    ~ Required

                    ~ "substrate":
                        {
                            "permitivitty": ( float ),
                            "loss":         ( float ),
                            "height":       ( float ),
                            "name":         ( str )
                        }

                    ~ "frequency":
                        {
                            "start":    ( float ),
                            "end":      ( float )
                        }
        """

        #   region STEP 0->1: Error checking

        #   STEP 0: Check if ant arg passed
        if ("ant" not in kwargs):
            #   STEP 1: Error handling
            raise Exception("An error occured in Natalie.__initAnt__() -> Step 0: No ant arg passed")

        #
        #   endregion

        #   STEP 1: Local variables
        dFrequency              = kwargs["ant"]["frequency"]
        dSubstrate              = kwargs["ant"]["substrate"]

        #   STEP 2: Update - class variables
        self.__dAnt_Substrate   = dSubstrate

        self.__dAnt_Fitness     = {
            "desired":
            {
                "start":    dFrequency["start"],
                "end":      dFrequency["end"]
            }
        }

        #   STEP 3: check if number of samples > 2
        if (self.__cf.data["parameters"]["frequency"]["samples"] >= 4):
            #   STEP 4: Get offset
            fTmp_Inner_L    = dFrequency["start"]   + self.__cf.data["parameters"]["frequency"]["lower frequency offset"]
            fTmp_Inner_H    = dFrequency["end"]     - self.__cf.data["parameters"]["frequency"]["upper frequency offset"]

            fTmp_Range      = ( fTmp_Inner_H - fTmp_Inner_L ) / 3.0

            fTmp_Samples    = np.floor( ( self.__cf.data["parameters"]["frequency"]["samples"] - 3 ) / 2 )

            fTmp_Range      = fTmp_Samples * fTmp_Range

            #   STEP 5: Set frequency parameters accordingly
            self.__dAnt_Frequency   = {
                "center":   round(dFrequency["start"]   + ( dFrequency["end"] - dFrequency["start"] ) / 2.0, 2),
                "start":    round(fTmp_Inner_L  - fTmp_Range, 2),
                "end":      round(fTmp_Inner_H  + fTmp_Range, 2),
                "samples":  self.__cf.data["parameters"]["frequency"]["samples"]
            }

        #   STEP 6: check if number of samples > 1
        elif (self.__cf.data["parameters"]["frequency"]["samples"] > 1):
            #   STEP 7: Set frequency parameters accordingly
            self.__dAnt_Frequency   = {
                "center":   round(dFrequency["start"]   + ( dFrequency["end"] - dFrequency["start"] ) / 2.0, 2),
                "start":    round(dFrequency["start"]   + ( self.__cf.data["parameters"]["frequency"]["lower frequency offset"] ), 2),
                "end":      round(dFrequency["end"]     - ( self.__cf.data["parameters"]["frequency"]["upper frequency offset"] ), 2),
                "samples":  self.__cf.data["parameters"]["frequency"]["samples"]
            }

        #   STEP 8: Check that frequency samples not 0
        elif (self.__cf.data["paramters"]["frequency"]["samples"] > 0):
            #   STEP 9: Set frequency parameters accordingly
            self.__dAnt_Frequency   = {
                "center":   round(dFrequency["start"] + ( dFrequency["end"] - dFrequency["start"] ) / 2.0, 2),
                "start":    round(dFrequency["start"] + ( dFrequency["end"] - dFrequency["start"] ) / 2.0, 2),
                "end":      round(dFrequency["start"] + ( dFrequency["end"] - dFrequency["start"] ) / 2.0, 2),
                "samples":  self.__cf.data["parameters"]["frequency"]["samples"]
            }

        else:
            #   STEP 10: Error handling
            raise Exception("An error occured in Natalie.__initAnt__() -> Step 11: Invalid sample number set in config file")

        #   STEP 11: Update - Local variables
        dFrequency = cp.deepcopy(self.__dAnt_Frequency)
        dFrequency["samples"] = self.__cf.data["parameters"]["frequency"]["accuracy check samples"]

        #   STEP 12: Return
        return

    #
    #   endregion

    #   region Back-End: Is type statements
    
    def __validateParams__(self, **kwargs) -> bool:
        """
            Description:

                Checks if all the required fields are in the passed dictioanry
                in order for it to act as a config file.

            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:

                + params    = ( dict ) Dictionary containing initialization
                    parameters for this class

            |\n

            Returns:

                + bOut  = ( bool )
        """

        #   STEP 0: Local variables
        dTmp                    = None

        #   STEP 1: Setup - Local variables
        
        #   STEP 2: Check if params arg passed
        if ("params" not in kwargs):
            #   STEP 3: Error handling
            raise Exception("An error occured in Natalie.__validateParams__() -> Step 2: No params arg passed")

        #   STEP 4: Update - Local variables
        dTmp = kwargs["params"]

        #   STEP 5: Check if scalars in dictionary
        if ("scalars" not in dTmp):
            #   STEP 6: Return
            return False

        #   STEP 7: check if menus in dict
        if ("menus" not in dTmp):
            #   STEP 8: Return
            return False

        #   STEP 9: Check if help in dict
        if ("help" not in dTmp):
            #   STEP 10: Return
            return False

        #   STEP 11: check if parameters in dict
        if ("parameters" not in dTmp):
            #   STEP 12: Return
            return False

        #   STPE 13: Update - Local var
        dTmp = dTmp["parameters"]

        #   STEP 14: Check if working dir in dict
        if ("working directory" not in dTmp):
            #   STEP 15: Return
            return False

        #   STPE 16: Check if frequency in dict
        if ("frequency" not in dTmp):
            #STEP 17: Return
            return False

        #   STEP 18: Check if mesh in dict
        if ("mesh" not in dTmp):
            #   STEP 19: Return
            return False

        #   STEP 20: Check if runt in dict
        if ("runt" not in dTmp):
            #   STEP 21: Return
            return False

        #   STEP 22: Check if trust region in dict
        if ("trust region" not in dTmp):
            #   STEP 23: Return
            return False

        #   STEP 24 Return
        return True

    #
    #   endregion
    
    #   region Back-End: Gets

    def __getFitness__(self, **kwargs) -> list:
        """
            Description:

                Using the provided arguments this function evaluates the
                overall fitness for all the antenna geometries passed.

            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:

                + ant   = ( list ) A list containing antenna geometries that
                    have already been simulated
                    ~ Required

                + fitness   = ( list ) A list containing the frequency fitness
                    evaluation of the above mentioned antenna geometries
                    ~ Required

                    ~ ( int )   = ( dict )
                        {
                            "fitness":
                            {
                                "frequency":
                                {
                                    "full range":   ( bool ),
                                    "in range":     ( float ),
                                    "in samples":   ( int ),
                                    "left range":   ( float ),
                                    "left samples": ( int ),
                                    "right range":  ( float ),
                                    "right samples":    ( int ) 
                                }
                            }
                        }
        """

        #   STEP 0: Local variables
        lOut                    = []

        #   STEP 1: Setup - Local variables
        
        #   region STEP 2->5: Error checking

        #   STEP 2: Check if ant arg passed
        if ("ant" not in kwargs):
            #   STEP 3: Error handling
            raise Exception("An error occured in Natalie.__evalFitness__() -> Step 2: No ant arg passed")

        #   STEP 4: Check if fitness arg passed
        if ("fitness" not in kwargs):
            #   STEP 5: Error handling
            raise Exception("An error occured in Natalie.__evalFitness__() -> Step 4: No fitness arg passed")
        
        #
        #   endregion

        #   STEP 6: Update - Local variables
        fOriginal_Area  = self.__dAnt_Center["substrate"]["l"] * self.__dAnt_Center["substrate"]["w"]

        #   STEP 7: Iterate through antenna
        for i in range(0, len(kwargs["ant"])):
            #   STEP 8: Setup - Tmp Variables
            dTmp_Ant        = kwargs["ant"][i]
            dTmp_Fit        = kwargs["fitness"][i]["fitness"]["frequency"]

            dTmp_Results    = {}

            #   STEP 9: Calculate area of antenna
            fTmp_Area   = dTmp_Ant["substrate"]["l"] * dTmp_Ant["substrate"]["w"]

            #   STEP 10: Get left fitness
            fTmp_Left   = ( dTmp_Fit["lower"]["total"] ) * 0.085

            #   STEP 11: Get center firness
            fTmp_Mid    = ( dTmp_Fit["desired"]["total"] ) * 0.7

            #   STEP 12: Get right fitness
            fTmp_Right  = ( dTmp_Fit["upper"]["total"] ) * 0.05

            #   STEP 13: Get total area fitness
            fTmp_Area   = fTmp_Area / fOriginal_Area

            #   STEP 14: Get total frequency fitness
            fTmp_Freq_Tot   = fTmp_Left + fTmp_Mid + fTmp_Right
            
            #   STEP 15: Get overall fitness
            fTmp_Fitness    = self.__aActivation.logistic( fTmp_Area * 8.0  - 6.0 ) 
            fTmp_Fitness    = fTmp_Fitness * fTmp_Freq_Tot +  0.3 * fTmp_Freq_Tot  + 0.65 * fTmp_Fitness

            #   STEP 16: Check if hard data provided
            if ("hard" in dTmp_Fit):
                #   STEP 17: Populate fitness dictionary
                dTmp_Results    = {
                    "items":    1,

                    "0":        "final",
                    "1":        "freq",

                    "lower":    dTmp_Fit["lower"]["total"],
                    "desired":  dTmp_Fit["desired"]["total"],
                    "upper":    dTmp_Fit["upper"]["total"],

                    "area":     fTmp_Area,
                    "freq":     fTmp_Freq_Tot,
                    "final":    fTmp_Fitness,

                    "resonant": dTmp_Fit["resonant frequency"],
                    "dir":      kwargs["fitness"][i]["dir"] 
                }

                #   STEP 18: Loop through hard data
                for j in range(0, dTmp_Fit["hard"]["items"] ):
                    #   STEP 19: Add to fitness dictionary
                    dTmp = {
                        "f":    dTmp_Fit["hard"][ str( j ) ]["fitness"],
                        "g":    dTmp_Fit["hard"][ str( j ) ]["gain"]
                    }

                    dTmp_Results[ dTmp_Fit["hard"][ str( j ) ]["frequency"] ] = dTmp

            #   STEP 20: No hard data provided
            else:
                #   STEP 21: Populate output dictionary
                dTmp_Results = {
                    "items":    1,

                    "0":        "final",
                    "1":        "desired",
                    "2":        "area",
                    #"3":        "freq",
                    #"4":        "lower",
                    #"5":        "upper",

                    "lower":    dTmp_Fit["lower"]["total"],
                    "desired":  dTmp_Fit["desired"]["total"],
                    "upper":    dTmp_Fit["upper"]["total"],

                    "area":     fTmp_Area,
                    "freq":     fTmp_Freq_Tot,
                    "final":    fTmp_Fitness,

                    "resonant": dTmp_Fit["resonant frequency"],
                    "dir":      kwargs["fitness"][i]["dir"]
                }

            #   STEP 22: Append to output
            lOut.append(dTmp_Results)

        #   STEP 23: Return
        return lOut

    def __getCandidates_Primary__(self, **kwargs) -> list:
        """
            Description:
            
                Generates the specified amount of candidates withing the trust
                Region as specified in the provided arguments.

            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:

                + center    = ( dict ) Dictionary containing a patch geometry
                    ~ Required

                + region    = ( int ) The region for random value generation
                    ~ Required

                + candidates    = ( int ) The number of candidates required
                    ~ Required
        """

        #   STEP 0: Local variables
        dCenter                 = None
        dScalars                = None

        lOut                    = []

        iCandidates             = None
        fRegion                 = None

        #   STEP 1: Setup - Local variables
        
        #   region STEP 2->9: Error checking

        #   STEP 2: Check if center arg passed
        if ("center" not in kwargs):
            #   STEP 3: Error handling
            raise Exception("An error occured in Natalie.__getCandidates__() -> Step 2: No center arg passed")

        #   STEP 4: Check if region arg passed
        if ("region" not in kwargs):
            #   STEP 5: Error handling
            raise Exception("An error occured in Natalie.__getCandidates__() -> Step 4: No region arg passed")

        #   STEP 6: Check if candidates arg passed
        if ("candidates" not in kwargs):
            #   STEP 7: Error handling
            raise Exception("An error occured in Natalie.__getCandidates__() -> Stpe 6: No candidates arg passed")

        #
        #   endregion

        #   STEP 10: Update - Local variables
        dCenter     = kwargs["center"]

        cTmp = Conny()
        cTmp.load("antenna.json")
        
        dScalars = cTmp.data["scalars"]

        iCandidates = kwargs["candidates"]

        #   STEP 11: Check region not 0
        if (kwargs["region"] == 0.0):
            #   STEP 12: Update - Local variables
            fRegion     = 0.01
        
        #   STEP 13: Region not 0
        else:
            #   STEP 14: Update - Local variables
            fRegion     = kwargs["region"]
        

        #   STEP 15: Loop for required number of candidates
        for _ in range(0, iCandidates):
            #   STEP 16: Create new candidate
            dTmp_Candidate = {
                "items":    3,
                
                "0":        "feed",
                "1":        "ground plane",
                "2":        "radiating plane",

                "feed":
                {
                    "items":    2,
                    
                    "0":        "center",
                    "1":        "width",

                    "center":   self.__getRandVal__(center=dCenter["feed"]["center"],  scalars=dScalars["feed"]["center"],     region=fRegion),
                    "width":    self.__getRandVal__(center=dCenter["feed"]["width"],   scalars=dScalars["feed"]["width"],      region=fRegion)
                },
                "ground plane":
                {
                    "items":    5,

                    "0":        "l",
                    "1":        "w",
                    "2":        "x",
                    "3":        "y",
                    "4":        "slots",

                    "l":        self.__getRandVal__(center=dCenter["ground plane"]["l"], scalars=dScalars["ground plane"]["l"], region=fRegion),
                    "w":        self.__getRandVal__(center=dCenter["ground plane"]["w"], scalars=dScalars["ground plane"]["w"], region=fRegion),
                    "x":        self.__getRandVal__(center=dCenter["ground plane"]["x"], scalars=dScalars["ground plane"]["x"], region=fRegion),
                    "y":        self.__getRandVal__(center=dCenter["ground plane"]["y"], scalars=dScalars["ground plane"]["y"], region=fRegion),

                    "slots":    None
                },
                "radiating plane":
                {
                    "items":    5,

                    "0":        "l",
                    "1":        "w",
                    "2":        "x",
                    "3":        "y",
                    "4":        "slots",
                    
                    "l":        self.__getRandVal__(center=dCenter["radiating plane"]["l"], scalars=dScalars["radiating plane"]["l"], region=fRegion),
                    "w":        self.__getRandVal__(center=dCenter["radiating plane"]["w"], scalars=dScalars["radiating plane"]["w"], region=fRegion),
                    "x":        self.__getRandVal__(center=dCenter["radiating plane"]["x"], scalars=dScalars["radiating plane"]["x"], region=fRegion),
                    "y":        self.__getRandVal__(center=dCenter["radiating plane"]["y"], scalars=dScalars["radiating plane"]["y"], region=fRegion),

                    "slots":    None
                },
                "substrate":
                {
                    "items":    4,

                    "0":        "l",
                    "1":        "w",
                    "2":        "x",
                    "3":        "h",
                    
                    "l":        0.0,
                    "w":        0.0,
                    "h":        dCenter["substrate"]["h"],
                    "x":        0.0,
                    "y":        0.0,

                    "permitivitty": dCenter["substrate"]["permitivitty"],
                    "loss":         dCenter["substrate"]["loss"],
                    "name":         dCenter["substrate"]["name"]
                }
            }

            #   STEP 17: Update - Candidate substrate
            self.__remapData_Substrate__(candidate=dTmp_Candidate)

            #   STEP 18: Get plane slots
            dTmp_Candidate["ground plane"]["slots"]     = self.__getSlots__(center=dCenter["ground plane"]["slots"],       scalars=dScalars["ground plane"]["slots"],      plane=dTmp_Candidate["ground plane"],       z=0.0,                              region=fRegion)
            dTmp_Candidate["radiating plane"]["slots"]  = self.__getSlots__(center=dCenter["radiating plane"]["slots"],    scalars=dScalars["radiating plane"]["slots"],   plane=dTmp_Candidate["radiating plane"],    z=dTmp_Candidate["substrate"]["h"], region=fRegion)
            
            #   STEP 19: Append new candidate to output list
            lOut.append(dTmp_Candidate)
            
        #   STEP 20: Return
        return lOut

    def __getCandidates_Secondary__(self, **kwargs) -> list:
        """
            Description:

                Generates the specified number of candidates with-in the Trust-
                Region.

            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:

                + center    = ( dict ) The current center antenna patch
                    geometry
                    ~ Requried
                
                + region    = ( dict ) Dictionary containgin the scaled and
                    unscaled regions for the current iterations
                    ~ Required

                + parameters    = ( dict ) Dictionary containing the parameters
                    to be adjusted during this iteration
                    ~ Required

                + candidates    = ( int ) The number of candidates to generate
                    ~ Default = self.__iTRO_Candidates
        """

        #   region STEP 0->5: Error checking

        #   STEP 0: check if center arg passed
        if ("center" not in kwargs):
            #   STEP 1: Error handling
            raise Exception("An error occured in Natalie.__getCandidates_Secondary__() -> Step 0: No center arg passed")

        #   STEP 2: Check if region arg passed
        if ("region" not in kwargs):
            #   STEP 3: Error handling
            raise Exception("An error occured in Natalie.__getCandidates_Secondary__() -> Step 2: No region arg passed")
        
        #   STEP 4: Check if parameters arg passed
        if ("parameters" not in kwargs):
            #   STEP 5: Error handling
            raise Exception("An error occured in Natalie.__getCandidates_Secondary__() -> Step 4: No parameters arg passed")

        #
        #   endregion

        #   STEP 6: Check - Number of candidates
        if (kwargs["candidates"] <= 0):
            #   STEP 7: Return
            return []

        #   STEP 8: Local variables
        lOut                    = []
        
        dCenter                 = kwargs["center"]
        dScalars                = self.__cAnt_Default["scalars"]

        iCandidates             = self.__iTRO_Candidates

        #   STEP 9: Check if candidates passed
        if ("candidates" in kwargs):
            #   STEP 10: Update - Local variables
            iCandidates = kwargs["candidates"]

        #   STEP 11: Loop through candidates
        for _ in range(0, iCandidates):
            #   STEP 12: Create new candidate
            lOut.append( cp.deepcopy( dCenter ) )

        #   STEP 13: Outsource - Recursively
        lOut = self.__getCandidates_SecRecurse__(scalars=dScalars, candidates=lOut, parameters=kwargs["parameters"], region=kwargs["region"], template=self.__dAnt_Template)
        
        #   STEP 14: Loop through candidates
        for i in range(0, len( lOut )):
            #   STEP 15: Remap - substrate
            lOut[i] = self.__remapData_Substrate__(candidate=lOut[i])
            
        #   STEP 16: Return
        return lOut

    def __getCandidates_SecRecurse__(self, **kwargs) -> list:
        """
            Description:

                Recursively generates the candidate parameters for the provided
                candidates using the provided arguments.

            |\n
            |\n
            |\n
            |\n
            |\n
            
            Arguments:

                + scalars   = ( dict ) Dictionary containing all the scalars necessarry for
                    the randomization of parameters.
                    ~ Required

                + candidates    = ( list ) List of candidates
                    ~ Required

                + parameters    = ( dict ) Dictionary containing the parameters
                    that should be adjusted
                    ~ Required

                + region    = ( idk ) Dictionary containing the region 
                    parameters
                    ~ Required

                + template  = ( dict ) The template for which parameters are
                    linked to which integers
                    ~ Required
  
        """

        #   region STEP 0->9: Error checking

        #   STEP 0: Check if scalars arg passed
        if ("scalars" not in kwargs):
            #   STEP 1: Error handling
            raise Exception("An error occured in Natalie.__getCandidates_SecRecurse__() -> Step 0: No scalars arg passed")

        #   STEP 2: Check if candidates arg passed
        if ("candidates" not in kwargs):
            #   STEP 3: Error handling
            raise Exception("An error occured in Natalie.__getCandidates_SecRecurse__() -> Step 2: NO candidates arg passed")
        
        #   STEP 4: Check if parameters arg passed
        if ("parameters" not in kwargs):
            #   STEP 5: Error handling
            raise Exception("An error occured in Natalie.__getCandidates_SecRecurse__() -> Step 4: No parameters arg passed")

        #   STEP 6: Check if region arg passed
        if ("region" not in kwargs):
            #   STEP 7: Error handling
            raise Exception("An error occured in Natalie.__getCandidates_SecRecurse__() -> Step 6: No region arg passed")

        #   STEP 8: Check if tmplate arg passed
        if ("template" not in kwargs):
            #   STEP 9: Error handling
            raise Exception("An error occured in Natalie.__getCandidates_SecRecurse__() -> Step 8: No template arg passed")

        #
        #   endregion

        #   STEP 10: Check that there are items in this dictionary
        if ("items" not in kwargs["template"]):
            #   STEP 11: Don't do this
            return kwargs["candidates"]

        #   STEP 12: Local variables
        dParams                 = kwargs["parameters"]
        dRegion                 = kwargs["region"]
        dScalars                = kwargs["scalars"]
        dTemplate               = kwargs["template"]

        lCandidates             = kwargs["candidates"]

        #   STEP 13: Loop through items in template
        for i in range(0, dTemplate["items"]):
            #   STEP 14: Setup - Tmp variable
            sTmp_Child      = dTemplate[str(i)]
            lTmp_Candidates = []

            #   STEP 15: Check if scalars
            try:
                #   STEP 16: Loop through candidates
                for j in range(0, len( lCandidates )):
                    #   STEP 17: Append candidates to list
                    lTmp_Candidates.append( lCandidates[j][ sTmp_Child ])
                
                #   STEP 18: If child is in scalars
                if (sTmp_Child in dScalars):
                    #   STEP 19: Check if dictionary
                    if ( type(dTemplate[sTmp_Child]) == dict ):
                        #   STEP 20: Outsource
                        lTmp_Candidates = self.__getCandidates_SecRecurse__(scalars=dScalars[sTmp_Child], candidates=lTmp_Candidates, parameters=dParams, region=dRegion, template=dTemplate[sTmp_Child])

                        #   STEP 20: Loop through candidates
                        for j in range(0, len( lCandidates )):
                            #   STEP 21: Update - Candidate params
                            lCandidates[j][sTmp_Child] = lTmp_Candidates[j]

                    #   STEP 22: Then normal param
                    else:
                        #   STEP 23: Be safe OwO
                        try:
                            #   STEP 24: Get param number
                            iTmp_Parameter  = int( dTemplate[sTmp_Child].strip("remap-") )

                            #   STEP 25: Check if this param is being used
                            if (iTmp_Parameter in dParams["current"]):
                                #   STEP 26: Get center val
                                fTmp_Center = cp.deepcopy( lTmp_Candidates[0] )

                                #   STEP 27: Loop through candidates
                                for j in range(0, len( lCandidates )):
                                    #   STEP 28: Update - Candidate val
                                    lCandidates[j][sTmp_Child] = self.__getRandVal__(center=fTmp_Center, scalars=dScalars[sTmp_Child], region=dRegion["scaled"])
                                
                        except Exception as ex:
                            #   STEP 29: Error handling
                            print("Initial error: ", ex)
                            raise Exception("An error occured in Natalie.__getCandidates_SecRecurse__() -> Step 29")

                #   STEP 30: Not in scalars
                else:
                    #   STEP 31: Totaly not a shortcut
                    raise Exception("yeet")

            except Exception as ex:
                #   STEP 32: Check if items in temp
                if ("items" in sTmp_Child):
                    #   STEP 33: Loop through items in child
                    for j in range(0, sTmp_Child["items"]):
                        #   STEP 34: Setup - Tmp variables
                        sTmp_GChild = sTmp_Child[str(j)]

                        #   STEP 35: Check if GChild is dict
                        if (type(sTmp_GChild) == dict):
                            #   STEP 36: Setup - Tmp variables
                            lTmp_Candidates = []

                            #   STEP 37: Loop through candidates
                            for k in range(0, len( lCandidates )):
                                #   STEP 38: Append candidate param
                                lTmp_Candidates.append( lCandidates[k][str(i)][str(j)] )

                            #   STEP 39: Outsource - Recurse
                            lTmp_Candidates = self.__getCandidates_SecRecurse__(scalars=dScalars["change slot"], candidates=lTmp_Candidates, parameters=dParams, region=dRegion, template=sTmp_GChild)

                            #   STEP 40: Loop through candidates
                            for k in range(0, len( lCandidates )):
                                #   STEP 41: Update - Candidate vals
                                lCandidates[k][str(i)][str(j)] = lTmp_Candidates[k]

                        else:
                            #   STEP 42: Get param number
                            iTmp_Parameter  = int( sTmp_Child[sTmp_GChild].strip("remap-") )
                            
                            #   STEP 43: Check if this param is being used
                            if (iTmp_Parameter in dParams["current"]):
                                #   STEP 44: Get center val
                                fTmp_Center = cp.deepcopy( lCandidates[0][str(i)][sTmp_GChild] )

                                #   STEP 45: Loop through candidates
                                for k in range(0, len( lCandidates )):
                                    #   STEP 46: Update - Candidate val
                                    lCandidates[k][str(i)][sTmp_GChild] = self.__getRandVal__(center=fTmp_Center, scalars=dScalars["change slot"][sTmp_GChild], region=dRegion["scaled"])
                
                else:
                    #   STEP 47: Error handling
                    print("Initial error: ", ex)
                    raise Exception("An error occured in Natalie.__getCandidates_SecSlots__() -> Step 47")

        #   STEP 48: Return
        return lCandidates

    def __getRandVal__(self, **kwargs) -> float:
        """
            Description:

                Generates a random float value around the center within the
                specified region.

            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:

                + center    = ( float ) The center float value
                    ~ Required

                + region    = ( int ) The region in which values can be 
                    generated
                    ~ Required

                + scalars   = ( dict ) Dictionary containing the random value
                    generation parameters
                    ~ Required

                    ~ "region"  = ( float )
                    ~ "range"   = ( float )
        """

        #   STPE 0: Local variables
        fOut                    = None

        #   STEP 1: Setup - Local variables
        
        #   region STEP 2->7: Error checking

        #   STEP 2: Check if center arg passed
        if ("center" not in kwargs):
            #   STEP 3: Error handling
            raise Exception("An error occured in Natalie.__randVal__() -> Step 2: No center arg passed")
        
        #   STEP 4: Check if region arg passed
        if ("region" not in kwargs):
            #   STEP 5: Error handling
            raise Exception("An error occured in Natalie.__randVal__() -> Step 4: No region arg passed")

        #   STEP 6: Check if scalars arg passed
        if ("scalars" not in kwargs):
            #   STEP 7: Error handling
            raise Exception("An error occured in Natalie.__randVal__() -> Step 6: No scalars arg passed")
        
        #
        #   endregion
        
        #   STEP 8: Check that rand generation actually required
        if (kwargs["scalars"]["range"] == 0.0):
            #   STEP 9: Return
            return kwargs["center"]

        #   STEP 22: Get offset
        fOffset = kwargs["center"] + kwargs["scalars"]["range"] * ( kwargs["scalars"]["region"] - 0.5 ) * 2.0

        fOut    = rn.gauss(fOffset, kwargs["scalars"]["range"] * kwargs["region"])

        #   STEP 26: Check if lw arg passed
        if ("lw" in kwargs):
            return abs( round( fOut, 3 ) )
        
        return round( fOut, 3 )

    def __getSlots__(self, **kwargs) -> dict:
        """
            Description:

                Returns the slots for some plane dependent on the provided
                arguments.

            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:

                + center    = ( dict ) The current slots for the plane
                    ~ Required

                    ~ "items"   = ( int )

                    ~ "( int )  = ( dict )
                        {
                            "0":
                            {
                                "x" = ( float ),
                                "y" = ( float ),
                                "z" = ( float )
                            },
                            "1":
                            {
                                "x" = ( float ),
                                "y" = ( float ),
                                "z" = ( float )
                            },
                            "2":
                            {
                                "x" = ( float ),
                                "y" = ( float ),
                                "z" = ( float )
                            }
                        }

                + scalars   = ( dict ) The scalar values for slot randomization
                    ~ Required

                + plane     = ( dict ) Dictionary containing the parameters for
                    the relevant plane
                    ~ Required

                    ~ "l"   = ( float )
                    ~ "w"   = ( float )
                    ~ "x"   = ( float )
                    ~ "y"   = ( float )

                + z         = ( int ) The z value for the plane
                    ~ Required

                + region    = ( int ) The region for randomization
                    ~ Required

                + force     = ( int ) Force creates slots until the specified
                    number of slots is met
                    ~ only viable if <slots=True>
        """
        
        #   STEP 0: Local variables
        dOut                    = None

        #   STEP 1: Setup - Local variables
        
        #   region STEP 2->13: Error checking

        #   STEP 2: Check if center arg passed
        if ("center" not in kwargs):
            #   STEP 3: Error handling
            raise Exception("An error occured in Natalie.__getSlots__() -> Step 2: No center arg passed")

        #   STEP 4: check if scalars arg passed
        if ("scalars" not in kwargs):
            #   STEP 5: Error handling
            raise Exception("An error occured in Natalie.__getSlots__() -> Step 4: No scalars arg passed")
        
        #   STEP 6: Check if plane arg passed
        if ("plane" not in kwargs):
            #   STPE 7: Error handling
            raise Exception("An error occured in Natalie.__getSlots__() -> Step 6: No plane arg passed")

        #   STPE 8: Check if region arg passed
        if ("region" not in kwargs):
            #   STEP 9: Error handling
            raise Exception("An error occured in Natalie.__getSlots__() -> Step 8: No region arg passed")
        
        #   STEP 10: Check if z arg passed
        if ("z" not in kwargs):
            #   STEP 11: Error handling
            raise Exception("An error occured in Natalie.__getSlots__() -> Step 10: No z arg passed")

        #
        #   endregion
        
        #   STEP 14: Update - Local variables
        dOut = cp.deepcopy(kwargs["center"])

        #   STEP 15: Check if there are elliptical slots
        if (kwargs["center"]["elliptical"]["items"] > 0):
            #   STEP 16: Setup - Tmp dictionaries
            dTmp_Slots  = dOut["elliptical"]
            dTmp_Scalar = kwargs["scalars"]["elliptical"]["change slot"]

            #   STEP 17: Loop through slots
            for i in range(0, dTmp_Slots["items"]):
                #   STEP 18: Check - Change probability
                if (rn.uniform(0.0, 1.0) < dTmp_Scalar["probability"]):
                    #   STEP 19: Setup - Tmp slot
                    dTmp_CurrSlot   = dTmp_Slots[ str(i) ]

                    #   STEP 20: Outsource - SLot parameter randomization
                    dTmp_CurrSlot["x"]  = self.__getRandVal__(center=dTmp_CurrSlot["x"], region=kwargs["region"], scalars=dTmp_Scalar["x"])
                    dTmp_CurrSlot["y"]  = self.__getRandVal__(center=dTmp_CurrSlot["y"], region=kwargs["region"], scalars=dTmp_Scalar["y"])
                    dTmp_CurrSlot["l"]  = self.__getRandVal__(center=dTmp_CurrSlot["l"], region=kwargs["region"], scalars=dTmp_Scalar["l"], lw=True)
                    dTmp_CurrSlot["w"]  = self.__getRandVal__(center=dTmp_CurrSlot["w"], region=kwargs["region"], scalars=dTmp_Scalar["w"], lw=True)
        
        #   STEP 21: Check if there are rectangular slots
        if (kwargs["center"]["rectangular"]["items"] > 0):
            #   STEP 22: Setup - Tmp dictionaries
            dTmp_Slots  = dOut["rectangular"]
            dTmp_Scalar = kwargs["scalars"]["rectangular"]["change slot"]

            #   STEP 23: Loop through slots
            for i in range(0, dTmp_Slots["items"]):
                #   STEP 24: Check - Change probability
                if (rn.uniform(0.0, 1.0) < dTmp_Scalar["probability"]):
                    #   STEP 25: Setup - Tmp slot
                    dTmp_CurrSlot   = dTmp_Slots[ str(i) ]

                    #   STEP 26: Outsource - SLot parameter randomization
                    dTmp_CurrSlot["x"]  = self.__getRandVal__(center=dTmp_CurrSlot["x"], region=kwargs["region"], scalars=dTmp_Scalar["x"])
                    dTmp_CurrSlot["y"]  = self.__getRandVal__(center=dTmp_CurrSlot["y"], region=kwargs["region"], scalars=dTmp_Scalar["y"])
                    dTmp_CurrSlot["l"]  = self.__getRandVal__(center=dTmp_CurrSlot["l"], region=kwargs["region"], scalars=dTmp_Scalar["l"], lw=True)
                    dTmp_CurrSlot["w"]  = self.__getRandVal__(center=dTmp_CurrSlot["w"], region=kwargs["region"], scalars=dTmp_Scalar["w"], lw=True)
        
        #   STEP 27: Check if there are triangular sltos
        if (kwargs["center"]["triangular"]["items"] > 0):
            #   STEP 28: Setup - Tmp dictionaries
            dTmp_Slots  = dOut["triangular"]
            dTmp_Scalar = kwargs["scalars"]["triangular"]["change slot"]

            #   STPE 29: Loop through slots
            for i in range(0, dTmp_Slots["items"]):
                #   STPE 30: Check - Change probability
                if (rn.uniform(0.0, 1.0) < dTmp_Scalar["probability"]):
                    #   STEP 31: Setup - Tmp slot
                    dTmp_CurrSlot   = dTmp_Slots[ str(i) ]

                    #   STEP 32: Loop through points in slot
                    for j in range(0, dTmp_CurrSlot["items"]):
                        #   STEP 33: Outsource slot parameter randomization
                        dTmp_CurrSlot[str(j)]["x"]  = self.__getRandVal__(center=dTmp_CurrSlot[str(j)]["x"], region=kwargs["region"], scalars=dTmp_Scalar["x"])
                        dTmp_CurrSlot[str(j)]["y"]  = self.__getRandVal__(center=dTmp_CurrSlot[str(j)]["y"], region=kwargs["region"], scalars=dTmp_Scalar["y"])

        #   STEP 34: Check if there are any polygonal slots
        if (kwargs["center"]["polygonal"]["items"] > 0):
            #   STEP 35: Setup - Tmp dictionaries
            dTmp_Slots  = dOut["polygonal"]
            dTmp_Scalar = kwargs["scalars"]["polygonal"]["change point"]

            #   STEP 36: Loop through slots
            for i in range(0, dTmp_Slots["items"]):
                #   STEP 37: Check - Change probability
                if (rn.uniform(0.0, 1.0) < dTmp_Scalar["probability"]):
                    #   STEP 38: Setup - Tmp slot
                    dTmp_CurrSlot   = dTmp_Slots[ str(i) ]
                    
                    #   STEP 39: Loop through points in slot
                    for j in range(0, dTmp_CurrSlot["items"]):
                        #   STEP 40: Outsource slot parameter randomization
                        dTmp_CurrSlot[str(j)]["x"]  = self.__getRandVal__(center=dTmp_CurrSlot[str(j)]["x"], region=kwargs["region"], scalars=dTmp_Scalar["x"])
                        dTmp_CurrSlot[str(j)]["y"]  = self.__getRandVal__(center=dTmp_CurrSlot[str(j)]["y"], region=kwargs["region"], scalars=dTmp_Scalar["y"])

        while (True):
            #   STEP 71->115: Check if force not in kwargs
            if ("force" not in kwargs):
                #   STEP 72: Get number of slots
                iTmp_Slots  =   dOut["elliptical"]["items"]
                iTmp_Slots  +=  dOut["rectangular"]["items"]
                iTmp_Slots  +=  dOut["triangular"]["items"]
                iTmp_Slots  +=  dOut["polygonal"]["items"]

                #   STEP 73: If there are slots
                if (iTmp_Slots > 0):
                    #   STEP 81: Get a random slot
                    iTmp_Index  = rn.randint(0, iTmp_Slots - 1)
                    iTmp_Sum    = dOut["elliptical"]["items"]

                    #   STEP 82: Check if elliptical
                    if (iTmp_Index < iTmp_Sum):
                        if (rn.uniform(0.0, 1.0) < kwargs["scalars"]["elliptical"]["remove slot"]["probability"]):
                            #   STEP 83: Get local slot
                            iTmp_Index  = rn.randint(0, dOut["elliptical"]["items"] - 1)

                            #   STEP 84: Decrement slots
                            dOut["elliptical"]["items"] -= 1

                            #   STEP 85: If slots not zero
                            if (dOut["elliptical"]["items"] > 0):
                                #   STEP 86: Loop through remaining slots
                                for i in range(iTmp_Index + 1, dOut["elliptical"]["items"] + 1):
                                    #   STEP 87: Shift slot
                                    dOut["elliptical"][ str(i - 1) ] = dOut[ str(i) ]

                            #   STEP 88: Remove slot at end of list
                            del dOut["elliptical"][ str( dOut["elliptical"]["items"] ) ]

                        break

                    #   STEP 90: Add rectangular items to sum
                    iTmp_Sum    += dOut["rectangular"]["items"]

                    #   STEP 91: Check if rectangular
                    if (iTmp_Index < iTmp_Sum):
                        if (rn.uniform(0.0, 1.0) < kwargs["scalars"]["rectangular"]["remove slot"]["probability"]):
                            #   STEP 92: Get local slot index
                            iTmp_Index  = rn.randint(0, dOut["rectangular"]["items"] - 1)

                            #   STEP 93: Decrement slots
                            dOut["rectangular"]["items"] -= 1

                            #   STEP 94: If slots not zero
                            if ( dOut["rectangular"]["items"] > 0):
                                #   STEP 95: Loop through remaining slots
                                for i in range(iTmp_Index + 1, dOut["rectangular"]["items"] + 1):
                                    #   STEP 96: Shift slot
                                    dOut["rectangular"][ str(i - 1) ] = dOut["rectangular"][ str(i) ]

                            #   STEP 97: Remove slot at end of list
                            del dOut["rectangular"][ str( dOut["rectangular"]["items"] ) ]

                        break

                    #   STEP 99: Add triangular items to sum
                    iTmp_Sum    += dOut["triangular"]["items"]

                    #   STEP 100: Check if triangular
                    if (iTmp_Index < iTmp_Sum):
                        if (rn.uniform(0.0, 1.0) < kwargs["scalars"]["triangular"]["remove slot"]["probability"]):
                            #   STEP 101: Get local slot index
                            iTmp_Index  = rn.randint(0, dOut["triangular"]["items"] - 1)

                            #   STEP 102: Decrement slots
                            dOut["triangular"]["items"] -= 1

                            #   STEP 103: If slots not zero
                            if ( dOut["triangular"]["items"] > 0 ):
                                #   STEP 103: Loop through remaining slots
                                for i in range(iTmp_Index, dOut["triangular"]["items"] + 1):
                                    #   STEP 104: Shift slot
                                    dOut["triangular"][ str(i - 1) ] = dOut["triangular"][ str(i) ]

                            #   STEP 105: Remove slot at end of list
                            del dOut["triangular"][ str( dOut["triangular"]["items"] ) ]

                        break

                    iTmp_Sum += dOut["polygonal"]["items"]

                    if (iTmp_Index < iTmp_Sum):
                        if (rn.uniform(0.0, 1.0) < kwargs["scalars"]["polygonal"]["remove point"]["probability"]):
                            #   STEP 107: Get local slot index
                            iTmp_Index  = rn.randint(0, dOut["polygonal"]["items"] - 1)

                            #   STEP 108: Decrement slots
                            dOut["polygonal"]["items"] -= 1

                            #   STEP 109: If slots not zero
                            if ( dOut["polygonal"]["items"] > 0):
                                #   STEP 110: Loop through remaining slots
                                for i in range(iTmp_Index, dOut["polygonal"]["items"] + 1):
                                    #   STEP 111: Shift slot
                                    dOut["polygonal"][ str(i - 1) ] = dOut["polygonal"][ str(i) ]

                            #   STEP 112: Remove slot at end of list
                            del dOut["polygonal"][ str( dOut["polygonal"]["items"] ) ]
            
            break

        #   STEP 42: Setup - Temp Variables
        iTmp_CreationIterations = 1

        #   STEP 43: Check if force arg passed
        if ("force" in kwargs):
            #   STEP 44: Update - Tmp variables
            iTmp_CreationIterations = kwargs["force"]

        #   STEP 45->70: Force create slots
        for i in range(0, iTmp_CreationIterations):
            #   STEP 46: Setup - Tmp variable
            dTmp_Slot   = None

            fTmp_X      = ( kwargs["plane"]["l"] - kwargs["plane"]["x"] ) * rn.uniform(0.0, 1.0)
            fTmp_Y      = ( kwargs["plane"]["w"] - kwargs["plane"]["y"] ) * rn.uniform(0.0, 1.0)

            fTmp_Prob   = kwargs["scalars"]["rectangular"]["probability"]
            fTmp_Rand   = rn.uniform(0.0, 1.0)

            #   STEP 47->49: Check if square slot
            if (( fTmp_Rand < fTmp_Prob ) and ( dTmp_Slot == None )):
                #   STEP 48: Setup - Scope variables
                dTmp_Scalar = kwargs["scalars"]["rectangular"]["create slot"]

                #   STEP 49: Create slot
                dTmp_Slot   = {
                    "items":    4,

                    "0":        "x",
                    "1":        "y",
                    "2":        "l",
                    "3":        "w",

                    "x":    self.__getRandVal__(center=fTmp_X,  scalars=dTmp_Scalar["x"], region=kwargs["region"]),
                    "y":    self.__getRandVal__(center=fTmp_Y,  scalars=dTmp_Scalar["y"], region=kwargs["region"]),
                    "z":    kwargs["z"],
                    "l":    self.__getRandVal__(center=1.0,     scalars=dTmp_Scalar["l"], region=kwargs["region"], lw=True),
                    "w":    self.__getRandVal__(center=1.0,     scalars=dTmp_Scalar["w"], region=kwargs["region"], lw=True),

                    "type": "rectangular",
                    "id":   Helga.ticks()
                }
            
            #   STEP 50: Update - Local variables
            fTmp_Prob    += kwargs["scalars"]["elliptical"]["probability"]

            #   STEP 51->53: Check if elliptical slot
            if (( fTmp_Rand < fTmp_Prob ) and ( dTmp_Slot == None )):
                #   STEP 52: Setup - Scope variables
                dTmp_Scalar = kwargs["scalars"]["elliptical"]["create slot"]

                #   STEP 53: Creat slot
                dTmp_Slot   = {
                    "items":    4,

                    "0":        "x",
                    "1":        "y",
                    "2":        "l",
                    "3":        "w",

                    "x":    self.__getRandVal__(center=fTmp_X,  scalars=dTmp_Scalar["x"], region=kwargs["region"]),
                    "y":    self.__getRandVal__(center=fTmp_Y,  scalars=dTmp_Scalar["y"], region=kwargs["region"]),
                    "z":    kwargs["z"],
                    "l":    self.__getRandVal__(center=1.0,     scalars=dTmp_Scalar["l"], region=kwargs["region"], lw=True),
                    "w":    self.__getRandVal__(center=1.0,     scalars=dTmp_Scalar["w"], region=kwargs["region"], lw=True),

                    "type": "elliptical",
                    "id":   Helga.ticks()
                }

            #   STEP 54: Update - Local variables
            fTmp_Prob    += kwargs["scalars"]["triangular"]["probability"]

            #   STEP 55->60: Check if triangular slot
            if (( fTmp_Rand < fTmp_Prob ) and ( dTmp_Slot == None )):
                #   STEP 56: Setup - Scope variables
                dTmp_Scalar = kwargs["scalars"]["triangular"]["create slot"]

                #   STEP 57: Create slot
                dTmp_Slot   = {
                    "items":    3,

                    "0":        "0",
                    "1":        "1",
                    "2":        "2",

                    "type":     "triangular",
                    "id":       Helga.ticks()
                }

                #   STEP 58: Loop through required corners
                for j in range(0, 3):
                    #   STEP 59: Create corner
                    dTmp_Corner = {
                        "items":    2,

                        "0":        "x",
                        "1":        "y",

                        "x":    self.__getRandVal__(center=fTmp_X,  scalars=dTmp_Scalar["x"], region=kwargs["region"]),
                        "y":    self.__getRandVal__(center=fTmp_Y,  scalars=dTmp_Scalar["y"], region=kwargs["region"]),
                        "z":    kwargs["z"]
                    }

                    #   STEP 60: Add to triangle
                    dTmp_Slot[str(j)] = dTmp_Corner
                
            #   STEP 61: Update - local variables
            fTmp_Prob    += kwargs["scalars"]["polygonal"]["probability"]

            #   STEP 62->78: Check if polygonal slot
            if (( fTmp_Rand < fTmp_Prob ) and ( dTmp_Slot == None )):
                #   STPE 63: Setup - Scope variables
                dTmp_Scalar = kwargs["scalars"]["polygonal"]["create point"]

                #   STEP 64: Create slot
                dTmp_Slot   = {
                    "items":    4,

                    "type":     "polygonal",
                    "id":   Helga.ticks()
                }

                #   STEP 65: Loop through requried corners
                for j in range(0, dTmp_Slot["items"]):
                    #   STEP 66: Create corner
                    dTmp_Corner = {
                        "items":    2,

                        "0":        "x",
                        "1":        "y",
                        
                        "x":    self.__getRandVal__(center=fTmp_X,  scalars=dTmp_Scalar["x"], region=kwargs["region"]),
                        "y":    self.__getRandVal__(center=fTmp_Y,  scalars=dTmp_Scalar["y"], region=kwargs["region"]),
                        "z":    kwargs["z"]
                    }

                    #   STEP 67: Add to polygon
                    dTmp_Slot[str(j)]   = dTmp_Corner

            #   STEP 68->70: Check if slot created
            if (dTmp_Slot != None):
                #   STEP 69: Get type of slot
                sTmp    = dTmp_Slot["type"]

                #   STEP 70: Add to candidate
                dOut[sTmp][ str( dOut[sTmp]["items"] ) ]    = dTmp_Slot
                dOut[sTmp]["items"] += 1

        #   STEP 116: Return
        return dOut
    
    def __getCandidate_Best__(self, _lFitness) -> int:
        """
        """

        #   STEP 0: Local variables
        fBest                   = np.inf
        
        iBest                   = 0
        
        #   STEP 1: Loop through the fitness list
        for i in range(0, len( _lFitness ) ):
            #   STEP 2: Check if less than current best fitness
            if ( _lFitness[i]["final"] < fBest ):
                #   STEP 3: Update - Best variables
                iBest = i
                fBest = _lFitness[i]["final"]

        #   STEP 4: Return
        return iBest

    def __getSurrogate_Results__(self, **kwargs) -> list:
        """
            Description:

                Builds the dataset for the surrogate model. After building the
                data set the surrogate is trained and mapped.

            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:

                + center    = ( dict ) Dictionary containing the current center
                    antenna geometry
                    ~ Required

                + inputs    = ( list ) List of inputs
                    ~ Required

                + outputs   = ( list ) List of outputs
                    ~ Required

                + region    = ( dict ) Dictionary containing the scaled and
                    unscaled regions
                    ~ Required

                + parameters    = ( dict ) Dictionary containing the parameters
                    to be used in the new data set
                    ~ Required
        """

        #   region STEP 0->9: Error checking

        #   STEP 0: Check if inputs arg passed
        if ("inputs" not in kwargs):
            #   STEP 1: Error handling
            raise Exception("An error occured in Natalie.__getSurrogate_Results__() -> Step 0: No inputs arg passed")

        #   STEP 2: Check if outputs arg passed
        if ("outputs" not in kwargs):
            #   STEP 3: Error handling
            raise Exception("An error occured in Natalie.__getSurrogate_Results__() -> Step 2: No outputs arg passed")

        #   STEP 4: Check if region arg passed
        if ("region" not in kwargs):
            #   STEP 5: Error handling
            raise Exception("An error occured in Natalie.__getSurrogate_Results__() -> Step 4: No region arg passed")

        #   STEP 6: Check if parameters arg passed
        if ("parameters" not in kwargs):
            #   STEP 7: Error handling
            raise Exception("An error occured in Natalie.__getSurrogate_Results__() -> Step 6: No parameters arg passed")
        
        #   STEP 8: Check if center arg passed
        if ("center" not in kwargs):
            #   STEP 9: Error handling
            raise Exception("An error occured in Natalie.__getSurrogate_Results__() -> Step 8: No center arg passed")

        #
        #   endregion

        #   STEP 10: Local variables
        vData                   = None

        dData_Range             = None
        dData_Map               = None

        lData_In                = []
        lData_Out               = kwargs["outputs"]

        lParams_Current         = kwargs["parameters"]["current"]

        #   region STEP 11->16: Setup - Local variables

        #   STEP 11: Loop through inputs
        for i in range(0, len(kwargs["inputs"])):
            #   STEP 12: Setup - Tmp variables
            lTmp_Input  = []

            #   STEP 13: Loop through current parameters
            for j in range(0, len( lParams_Current )):
                #   STEP 14: Append input val
                lTmp_Input.append( kwargs["inputs"][i][ lParams_Current[j] ])

            #   STEP 15: Append to input list
            lData_In.append(lTmp_Input)

        #   STEP 16: User output
        if (self.bShowOutput):
            print("")


        #
        #   endregion

        #   region STEP 16->25: Setup - Data container

        #   STEP 16: Create temp data dictionary
        dTmp_Data   = {
            "in":   lData_In,
            "out":  lData_Out
        }

        #   STEP 17: Create data container
        vData   = Data()
        vData.setData(data=dTmp_Data)

        #   STEP 18: Check if last iteration was successful
        if (vData.getLen() > self.__iTRO_Candidates_Secondary + 1):
            #   STEP 19: Setup - Tmp variables
            lInputDistances = vData.getInputDistance( vData.getLen() - 1)
            fTmp_MaxRegion  = float( kwargs["region"]["unscaled-srg"] + 1 ) * ( kwargs["region"]["scaled"] / self.__fTRO_RegionScalar_Secondary )
            iTmp_Count      = 0
            
            #   STEP 20: Loop through input distances
            while (iTmp_Count < len(lInputDistances) - 1):
                #   STEP 21: Check if outside region
                if (( lInputDistances[iTmp_Count] > fTmp_MaxRegion ) or ( lInputDistances[iTmp_Count] == 0.0 )):
                    #   STEP 22: Pop from data set
                    vData.pop(used=False, index=iTmp_Count)
                    iTmp_Distance = lInputDistances.pop(iTmp_Count)

                    #   STEP 23: User output
                    if (self.bShowOutput):
                        print("\t{" + Helga.time() + "} - Removing input-output pair <" + str( round(iTmp_Distance, 2) ) + ":" + str( round(fTmp_MaxRegion, 2)) + ">")

                #   STPE 24: Not outside region
                else:
                    #   STEP 25: Increment counter
                    iTmp_Count += 1
        
        #   STPE ??: Check if there is data left
        if (len(lInputDistances) < 5):
            #   STEP ??: ERror handling
            raise Exception("An error occured in Natalie.__getSurrogate_Results__() -> Step ??: Too little data for surrogate training")
        
        #
        #   endregion

        #   region STEP 26->38: Data mapping

        #   STEP 26: Setup - Tmp variables
        dData_Range = {
            "lower":    -0.9,
            #"center":   0.0,
            "center":   -0.05,
            "upper":    1.0
        }

        lTmp_DataMap_Out    = []
        lTmp_DataMap_In     = []

        #   STEP 27: Loop through output parameters
        for i in range(0, len(lData_Out[0])):
            #   STEP 28: Append to mapp
            lTmp_DataMap_Out.append(i)

        #   STEP 29: Loop throughinput parameters
        for i in range(0, len(lData_In[0])):
            #   STEP 30: Append to map
            lTmp_DataMap_In.append(i)

        #   STEP 31: Setup - Data map
        dData_Map   = {
            "out":  lTmp_DataMap_Out,
            "in":   lTmp_DataMap_In
        }

        #   STEP 32: Check if normalizaing or standardizing
        if (rn.uniform(0.0, 1.0) < 0.5):
            #   STEP 33: User output
            if (self.bShowOutput):
                print("\t{" + Helga.time() + "} - Standardizing data")

            #   STEP 34: Standardize data
            vData.normalize(mapRange=dData_Range, mapSets=dData_Map, input=False, output=True)
            vData.standardize(input=True)

        else:
            #   STEP 35: User output
            if (self.bShowOutput):
                print("\t{" + Helga.time() + "} - Normalizing data")

            #   STEP 36: Normalize outputs
            vData.normalize(mapRange=dData_Range, mapSets=dData_Map, input=False, output=True)

            #   STEP 37: Setup - Input range
            dData_Range = {
                "lower":    -1.0,
                "center":   0.0,
                "upper":    1.0
            }

            #   STEP 38: Normalize inputs
            vData.normalize(mapRange=dData_Range, mapSets=dData_Map, input=True, output=False)

        #
        #   endregion

        #   region STEP 39->41: Surrogate Modelling

        #   STEP 39: Setup - Golem
        vGolem  = Golem(numSurrogates=8)
        vGolem.bSRG_Random              = True
        vGolem.bSRG_RandomParameters    = False

        #   STEP 40: Train and map
        vGolem.trainAndMap(data=vData, region=float(kwargs["region"]["unscaled-srg"])/self.__iTRO_Region_SRG, rand=True, remap=True)

        #   STEP 41: Remap results
        lCandidates = self.__remapData__(candidates=vGolem.lMap_Results, parameters=kwargs["parameters"], center=kwargs["center"])
        
        #
        #   endregion

        #   STEP 41: Return
        return lCandidates

    #
    #   endregion

    #   region Back-End: Data management

    #       region Back-End-(Data Management): Data molding

    def __moldData__(self, **kwargs) -> dict:
        """
            Description:

                Recursively iterates through the candidate data and fitness
                data to build a dataset to be used during surrogate modelling.
                
            |\n 
            |\n 
            |\n 
            |\n 
            |\n

            Arguments:

                + candidates    = ( list ) A list of antenna geometries
                    ~ Required

                + fitness       = ( list ) A list of fitness parameters
                    for each candidate antenna geometry

            |\n
            
            Returns:

                + dOut  = ( dict ) An dictionary containing the input and
                    output lists for a dataset
        """

        #   region STEP 0->3: Error checking

        #   STEP 0: Check if canddiates arg passed
        if ("candidates" not in kwargs):
            #   STEP 1: Error handling
            raise Exception("An error occured in Natalie.__moldData__() -> Step 0: No candidates arg passed")

        #   STEP 2: Check if fitness arg passed
        if ("fitness" not in kwargs):
            #   STEP 3: Error handling
            raise Exception("An error occured in Natalie.__moldData__() -> Step 2: No fitness arg passed")

        #
        #   endregion

        #   STEP 4: Local variables
        dOut                    = None

        lInput                  = []
        lOutput                 = []

        #   STEP 5: Outsource
        lInput  = self.__moldData_Recurse__(data=kwargs["candidates"])
        lOutput = self.__moldData_Recurse__(data=kwargs["fitness"])

        #   STEP 6: Populate output dictionary
        dOut    = {
            "in":   lInput,
            "out":  lOutput
        }

        #   STEP 7: Return
        return dOut

    def __moldData_Recurse__(self, **kwargs) -> vars:
        """
            Description:

                Iteates through the provided template in order to map the
                antenna geometries to usable dataset.

            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:

                + data  = ( list ) A list of candidate antenna geometries
                    ~ Required
        """

        #   region STEP 0->1: Error checking

        #   STEP 0: Check if data arg passed
        if ("data" not in kwargs):
            #   STEP 1: Error handling
            raise Exception("An error occured in Natalie.__moldData_Recurse__() -> Step 0: No data arg passed")
        
        #
        #   endregion

        #   STEP 2: Local variables
        dTemplate               = kwargs["data"][0]

        lOut                    = []
        
        #   STEP 3: Check if "items" entry in template
        if ("items" not in dTemplate):
            #   STEP 4: Return empty
            return None

        #   STEP 5: Iterate through items list
        for i in range(0, dTemplate["items"]):
            #   STEP 6: Setup - Scope variables
            lTmp_Child_In   = []
            lTmp_Child_Out  = None

            sTmp_Child      = dTemplate[str(i)]

            #   STEP 7: Loop through candidates
            for j in range(0, len(kwargs["data"])):
                #   STEP 8: Append child dictionary from all candidates to temp list for recursion
                lTmp_Child_In.append(kwargs["data"][j][sTmp_Child])

            #   STEP 9: Be safe OwO - Shortcut
            try:
                #   STEP 10: Check if slots
                if (sTmp_Child == "slots"):
                    #   STEP 11: Outsource
                    lTmp_Child_Out = self.__moldData_Slots__(data=lTmp_Child_In)

                #   STEP 12: Check if child has children
                elif ("items" in dTemplate[sTmp_Child]):
                    #   STEP 13: Outsource
                    lTmp_Child_Out  = self.__moldData_Recurse__(data=lTmp_Child_In)

            #   STEP 14: Normal output
            except:
                #   STEP 15: Set output equal to temp input
                lTmp_Child_Out = [lTmp_Child_In]
            
            #   STEP 16: Check child output status
            if (lTmp_Child_Out != None):
                #   STEP 17: Update - Output variables
                lOut.extend(lTmp_Child_Out)

        #   STEP 18: Return
        return lOut

    def __moldData_Slots__(self, **kwargs) -> vars:
        """
            Description:

                Iterates through the provided data in order to map the antenna
                slots to a usable dataset
            
            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:

                + data  = ( list ) A list of candidate antenna geometries
                    ~ Required
        """

        #   region STEP 0->1: Error checking

        #   STEP 0: Check if data arg passed
        if ("data" not in kwargs):
            #   STEP 1: Error handling
            raise Exception("An error occured in Natalie.__dataRecursion_Slots__() -> Step 0: No data arg passed")

        #
        #   endregion

        #   STEP 2: Local variables
        lOut                    = []

        #   STEP 3: Be safe OwO
        try:
            #   STEP 4: Check if there are any elliptical slots
            if (kwargs["data"][0]["elliptical"]["items"] > 0):
                #   STEP 5: Loop through elliptical slots
                for i in range(0, kwargs["data"][0]["elliptical"]["items"]):
                    #   STEP 6: Setup - Tmp variables
                    lTmp    = [[], [], [], []]

                    #   STEP 7: Loop through candidates
                    for j in range(0, len( kwargs["data"] ) ):
                        #   STEP 8: Append data to tmp var
                        lTmp[0].append( kwargs["data"][j]["elliptical"][str(i)]["l"])
                        lTmp[1].append( kwargs["data"][j]["elliptical"][str(i)]["w"])
                        lTmp[2].append( kwargs["data"][j]["elliptical"][str(i)]["x"])
                        lTmp[3].append( kwargs["data"][j]["elliptical"][str(i)]["y"])
                    
                    #   STEP 9: Append data to output
                    lOut.extend(lTmp)

            #   STEP 10: Check if there are any rectangular slots
            if (kwargs["data"][0]["rectangular"]["items"] > 0):
                #   STEP 11: Loop through rectangular slots
                for i in range(0, kwargs["data"][0]["rectangular"]["items"]):
                    #   STEP 12: Setup - Tmp Variables
                    lTmp    = [[], [], [], []]

                    #   STEP 13: Loop through candidates
                    for j in range(0, len( kwargs["data"] ) ):
                        #   STEP 14: Append data to tmp var
                        lTmp[0].append( kwargs["data"][j]["rectangular"][str(i)]["l"])
                        lTmp[1].append( kwargs["data"][j]["rectangular"][str(i)]["w"])
                        lTmp[2].append( kwargs["data"][j]["rectangular"][str(i)]["x"])
                        lTmp[3].append( kwargs["data"][j]["rectangular"][str(i)]["y"])

                    #   STEP 15: Append data to output
                    lOut.extend(lTmp)

            #   STEP 16: Check if there are any triangular sltos
            if (kwargs["data"][0]["triangular"]["items"] > 0):
                #   STEP 17: Loop through triangular slots
                for i in range(0, kwargs["data"][0]["triangular"]["items"]):
                    #   STEP 18: Setup - Tmp variables
                    lTmp    = [[], [], [], [], [], []]
                    
                    #   STEP 19: Loop through candidates
                    for j in range(0, len( kwargs["data"] ) ):
                        #   STEP 20: Append data to tmp 
                        lTmp[0].append( kwargs["data"][j]["triangular"][str(i)]["0"]["x"])
                        lTmp[1].append( kwargs["data"][j]["triangular"][str(i)]["0"]["y"])
                        lTmp[2].append( kwargs["data"][j]["triangular"][str(i)]["1"]["x"])
                        lTmp[3].append( kwargs["data"][j]["triangular"][str(i)]["1"]["y"])
                        lTmp[4].append( kwargs["data"][j]["triangular"][str(i)]["2"]["x"])
                        lTmp[5].append( kwargs["data"][j]["triangular"][str(i)]["2"]["y"])

                    #   STEP 21: Append data to output
                    lOut.extend(lTmp)
                
        except Exception as ex:
            #   STEP 22: Error handling
            print("Initial error: ", ex)
            raise Exception("An error occured in Natalie.__moldData_Slots__() -> Step 22")

        #   STEP 23: Return
        return lOut

    def __getParameters_Secondary__(self, **kwargs) -> dict:
        """
            Description:

                Creates a template for the candidate creation and remapping as
                well as creating the parameters dictionary to be used during
                candidate creation.

            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:

                + center    = ( dict ) The current center antenna patch
                    geometry
                    ~ Requried

                + region    = ( int ) The current region for the surrogate
                    model
                    ~ Required
        """

        #   region STEP 0->1: Error checking

        #   STEP 0: Check if center arg passed
        if ("center" not in kwargs):
            #   STEP 1: Error handling
            raise Exception("An error occured in Natalie.__getParameters_Secondary__() -> Step 0: No center arg passed")
        
        #   STEP 2: Check if region arg passed
        if ("region" not in kwargs):
            #   STEP 3: Error handling
            raise Exception("An error occured in Natalie.__getParameters_Secondary__() -> Step 2: No region arg passed")

        #
        #   endregion

        #   STEP 4: Local variables
        dOut                    = None

        dTemplate               = cp.deepcopy( kwargs["center"] )

        lCurrent                = []
        lUsed                   = []
        lUnused                 = []

        iParameters             = self.__createTemplate_Recurse__(template=dTemplate, parameters=0)

        #   STEP 5: Update - Class template
        self.__dAnt_Template    = dTemplate

        #   STEP 6: Loop through parameters
        for i in range(0, iParameters):
            #   STEP 7: Append to unused list
            lUnused.append(i)

        #   STEP 8: Loop through surrogate region
        for i in range(0, kwargs["region"]):
            iTmp_Index = int( rn.uniform( 0.0, float( len(lUnused) - 1 ) ) )

            #   STEP 9: Transfer parameter from unused to current
            lCurrent.append( lUnused.pop( iTmp_Index ) )

        #   STEP 10: Sort parameters
        lCurrent.sort()

        #   STEP 11: Populate output dictionary
        dOut    = {
            "count":    iParameters,
            "current":  lCurrent,
            "used":     lUsed,
            "unused":   lUnused

        }
        
        #   STEP 12: Return
        return dOut

    def __updateParameters_Secondary__(self, **kwargs) -> vars:
        """
            Description:

                Performs the required action's update on the parameters. idk
                how to english

            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:

                + region    = ( int ) The surrogate region
                    ~ Required

                + grace     = ( int ) The grace region
                    ~ Required

                + parameters    = ( dict ) Dictionary containing the current
                    parameters being used
                    ~ Required

                + action    = ( str ) The action to be performed
                    ~ Required

                    ~ Possibilities:
                        - "increase"
                        - "decrease"
        """

        #   region STEP 0->??: Error checking

        #   STEP 0: Check if region arg passed
        if ("region" not in kwargs):
            #   STEP 1: Error handlign
            raise Exception("An error occured in Natalie.__updateParameters_Secondary__() -> Step 0: No region arg passed")

        #   STEP 2: Check if grace arg passed
        if ("grace" not in kwargs):
            #   STEP 3: Error handling
            raise Exception("An error occured in Natalie.__updateParameters_Secondary__() -> Step 2: No grace arg passed")

        #   STEP 4: Check if parameters arg passed
        if ("parameters" not in kwargs):
            #   STEP 5: Error handling
            raise Exception("An error occured in Natalie.__updateParameters_Secondary__() -> Step 4: No parameters arg passed")

        #   STEP 8: Check if action arg passed
        if ("action" not in kwargs):
            #   STEP 9: Error handling
            raise Exception("An error occured in Natalie.__updateParameters_Secondary__() -> Step 8: No action arg passed")

        #
        #   endregion

        #   STEP 10: Check if increase
        if (kwargs["action"] == "increase"):
            #   STEP 11: Check if there are unused parameters
            if ( len( kwargs["parameters"]["unused"] ) > 0 ):
                #   STEP 12: Get index
                iTmp_Index = rn.randint(0, len( kwargs["parameters"]["unused"] ) - 1 )

                #   STEP 13: Get param
                iTmp_Param  = kwargs["parameters"]["unused"].pop(iTmp_Index)

                #   STEP 14: Add to used and current
                kwargs["parameters"]["used"].append(iTmp_Param)
                kwargs["parameters"]["current"].append(iTmp_Param)

                #   STEP 15: Sort current
                kwargs["parameters"]["current"].sort()

        #   STEP 16: Check if decrease
        elif (kwargs["action"] == "decrease"):
            #   STEP 17: Check if region is dead
            if (kwargs["region"] == 0):
                #   STEP 18: Check if grace is dead
                if (kwargs["grace"] == 0):
                    #   STEP 19: Return
                    return None

                #   STEP 20: Decrement grace and reset region
                kwargs["grace"]     -= 1
                kwargs["region"]    = self.__iTRO_Region_SRG

            #   STEP 22: Reset parameters
            kwargs["parameters"]["used"]    = []
            kwargs["parameters"]["unused"]  = []
            kwargs["parameters"]["current"] = []

            #   STEP 23: Loop through parameters
            for i in range(0, kwargs["parameters"]["count"]):
                #   STEP 24: Append to unused
                kwargs["parameters"]["unused"].append(i)

            #   STEP 25: Loop through region
            for i in range(0, kwargs["region"]):
                #   STEP 26: Get random index
                iTmp_Index  = rn.randint(0, len(kwargs["parameters"]["unused"]) - 1)

                #   STEP 27: Move from unused to current
                kwargs["parameters"]["current"].append( kwargs["parameters"]["unused"].pop(iTmp_Index) )

                #   STEP 28: Sort unused and current
                kwargs["parameters"]["current"].sort()
                
        #   STEP 29: Return

        return kwargs["parameters"]

    def __createTemplate_Recurse__(self, **kwargs) -> int:
        """
            Description:

                Recursively traverses the provided antenna geometry to count
                the parameters and create the template

            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:

                + template      = ( dict ) The current center antenna patch
                    geometry
                    ~ Requried
                
                + parameters    = ( int ) The current amount of parameters
                    ~ Required
        """

        #   region STEP 0->3: Error checking

        #   STEP 0: Check if template arg passed
        if ("template" not in kwargs):
            #   STEP 1: Error handling
            raise Exception("An error occured in Natalie.__createTemplate_Recurse__() -> Step 0: No template arg passed")

        #   STEP 2: Check if parameters arg passed
        if ("parameters" not in kwargs):
            #   STEP 3: Error handling
            raise Exception("An error occured in Natalie.__createTemplate_Recurse__() -> Step 2: No parameters arg passed")

        #
        #   endregion

        #   STEP 4: Loop through items
        for i in range(0, kwargs["template"]["items"]):
            #   STEP 5: Setup - Tmp variables
            sTmp_Child      = kwargs["template"][str(i)]

            #   STEP 6: Check if slots
            if (sTmp_Child == "slots"):
                #   STEP 7: Outsource - Create Slots Template
                kwargs["parameters"] = self.__createTemplate_Slots__(template=kwargs["template"][sTmp_Child], parameters=kwargs["parameters"])

            #   STEP 8: Check if child is float
            elif ( ( type(kwargs["template"][sTmp_Child]) == float ) or ( type(kwargs["template"][sTmp_Child]) == np.float64 ) ):
                #   STEP 9: Set to remap
                kwargs["template"][sTmp_Child] = "remap-" + str(kwargs["parameters"])

                #   STEP 10: Increment parameters
                kwargs["parameters"] += 1

            #   STEP 11: Not float or slots -> Outsource
            else:
                #   STEP 12: Outsource
                kwargs["parameters"] = self.__createTemplate_Recurse__(template=kwargs["template"][sTmp_Child], parameters=kwargs["parameters"])

        #   STEP 13: Return
        return kwargs["parameters"]

    def __createTemplate_Slots__(self, **kwargs) -> int:
        """
            Description:

                Traverses the provided antenna geometry to count the parameters
                and create the template.

            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:

                + template      = ( dict ) The current center antenna patch
                    geometry
                    ~ Requried
                
                + parameters    = ( int ) The current amount of parameters
                    ~ Required
        """

        #   region STEP 0->3: Error checking

        #   STEP 0: Check if template arg passed
        if ("template" not in kwargs):
            #   STEP 1: Error handling
            raise Exception("An error occured in Natalie.__createTemplate_Slots__() -> Step 0: No template arg passed")

        #   STEP 2: Check if parameters arg passed
        if ("parameters" not in kwargs):
            #   STEP 3: Error handling
            raise Exception("An error occured in Natalie.__createTemplate_Slots__() -> Step 2: No parameters arg passed")

        #
        #   endregion

        #   STEP 4: Be safe OwO
        try:
            #   STEP 5: Check if there are any elliptical slots
            if (kwargs["template"]["elliptical"]["items"] > 0):
                #   STEP 6: Loop through elliptical slots
                for i in range(0, kwargs["template"]["elliptical"]["items"]):
                    #   STEP 7: Set to remaps
                    kwargs["template"]["elliptical"][str(i)]["l"] = "remap-" + str(kwargs["parameters"] + 0)
                    kwargs["template"]["elliptical"][str(i)]["w"] = "remap-" + str(kwargs["parameters"] + 1)
                    kwargs["template"]["elliptical"][str(i)]["x"] = "remap-" + str(kwargs["parameters"] + 2)
                    kwargs["template"]["elliptical"][str(i)]["y"] = "remap-" + str(kwargs["parameters"] + 3)

                    #   STEP 8: Increment counter
                    kwargs["parameters"] += 4

            #   STEP 9: Check if there are any rectangular slots
            if (kwargs["template"]["rectangular"]["items"] > 0):
                #   STEP 10: Loop through elliptical slots
                for i in range(0, kwargs["template"]["rectangular"]["items"]):
                    #   STEP 11: Set to remaps
                    kwargs["template"]["rectangular"][str(i)]["l"] = "remap-" + str(kwargs["parameters"] + 0)
                    kwargs["template"]["rectangular"][str(i)]["w"] = "remap-" + str(kwargs["parameters"] + 1)
                    kwargs["template"]["rectangular"][str(i)]["x"] = "remap-" + str(kwargs["parameters"] + 2)
                    kwargs["template"]["rectangular"][str(i)]["y"] = "remap-" + str(kwargs["parameters"] + 3)

                    #   STEP 12: Increment counter
                    kwargs["parameters"] += 4
                    
            #   STEP 13: Check if there are any rectangular slots
            if (kwargs["template"]["triangular"]["items"] > 0):
                #   STEP 14: Loop through elliptical slots
                for i in range(0, kwargs["template"]["triangular"]["items"]):
                    #   STEP 15: Set to remaps
                    kwargs["template"]["triangular"][str(i)]["0"]["x"] = "remap-" + str(kwargs["parameters"] + 0)
                    kwargs["template"]["triangular"][str(i)]["0"]["y"] = "remap-" + str(kwargs["parameters"] + 1)
                    kwargs["template"]["triangular"][str(i)]["1"]["x"] = "remap-" + str(kwargs["parameters"] + 2)
                    kwargs["template"]["triangular"][str(i)]["1"]["y"] = "remap-" + str(kwargs["parameters"] + 3)
                    kwargs["template"]["triangular"][str(i)]["2"]["x"] = "remap-" + str(kwargs["parameters"] + 4)
                    kwargs["template"]["triangular"][str(i)]["2"]["y"] = "remap-" + str(kwargs["parameters"] + 5)

                    #   STEP 16: Increment counter
                    kwargs["parameters"] += 6

        except Exception as ex:
            #   STEP 17: Error handling
            print("Initial Error: ", ex)
            raise Exception("An error occured in Natali.__createTemplate_Slots__() -> Step 17")

        #   STEP 18: Return
        return kwargs["parameters"]
        
    #
    #       endregion

    #       region Back-End-(Data Management): Remapping

    def __remapData__(self, **kwargs) -> list:
        """
            Description:

                Remaps a passed candidate using the template saved during the
                __moldData__ function.

            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:

                + candidates = ( list ) A list of the parameters for the antenna
                    geometry
                    ~ Required

                + center    = ( dict ) Dictionary containing the current center
                    antenna geometry
                    ~ Required

                + parameters    = ( dict ) Dictionary containing the parameters
                    to be used in the new data set
                    ~ Required
        """

        #   region STEP 0->5: Error checking

        #   STEP 0: Check if candidate arg passed
        if ("candidates" not in kwargs):
            #   STEP 1: Error handling
            raise Exception("An error occured in Natalie.__remapData__() -> Step 0: No candidates arg passed")

        #   STEP 2: Check if center arg passed
        if ("center" not in kwargs):
            #   STEP 3: Error handling
            raise Exception("An error occured in Natalie.__remapData__() -> Step 2: No center arg passed")

        #   STEP 4: Check if parameters arg passed
        if ("parameters" not in kwargs):
            #   STEP 5: Error handling
            raise Exception("An error occured in Natalie.__remapData__() -> Step 4: No parameters arg passed")

        #
        #   endregion

        #   STEP 6: Local variables
        lOut                    = []

        #   STPE 7: Create new candidates
        for _ in range(0, len(kwargs["candidates"])):
            #   STEP 8: Create new candidate
            lOut.append( cp.deepcopy(kwargs["center"]) )
        
        #   STEP 9: Oursource - Recursively
        lOut = self.__remapData_Recursion__(data=kwargs["candidates"], candidates=lOut, template=self.__dAnt_Template, parameters=kwargs["parameters"])

        #   STEP 10: Loop through candidates
        for i in range(0, len(lOut)):
            #   STEP 11: Outsource - Substrate remapping
            lOut[i] = self.__remapData_Substrate__(candidate=lOut[i])

        #   STEP 12: Return
        return lOut

    def __remapData_Recursion__(self, **kwargs) -> list:
        """
            Description:

                Remaps a passed candidate recursively using the provided
                template.

            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:

                + template  = ( dict ) A dictionary containing the parameters
                    of an antenna geometry
                    ~ Required

                + data  = ( list ) The list of data to be remapped
                    ~ Required

                + candidates = ( dict ) The new antenna geometry
                    ~ Required

                + parameters    = ( dict ) Dictionary containing the parameters
                    to be used in the new data set
                    ~ Required
        """

        #   region STEP 0->7: Error checking

        #   STEP 0: Check if template arg passed
        if ("template" not in kwargs):
            #   STEP 1: Error handling
            raise Exception("An error occured in Natalie.__remapData_Recursion__() -> Step 0: No template arg passed")

        #   STEP 2: Check if data arg passed
        if ("data" not in kwargs):
            #   STEP 3: Error handling
            raise Exception("An error occured in Natalie.__remapData_Recursion__() -> Step 2: No data arg passed")

        #   STEP 4: Check if candidates arg passed
        if ("candidates" not in kwargs):
            #   STEP 5: Error handling
            raise Exception("An error occured in Natalie.__remapData_Recursion__() -> Step 4: No candidates arg passed")

        #   STEP 6: Check if parameters arg passed
        if ("parameters" not in kwargs):
            #   STEP 7: Error handling
            raise Exception("An error occured in Natalie.__remapData_Recursion__() -> Step 6: No parameters arg passed")

        #
        #   endregion

        #   STEP 8: Check that there are items in this dictionary
        if ("items" not in kwargs["template"]):
            #   STEP 9: Return
            return kwargs["candidates"]

        #   STEP 10: Local variables
        dParams                 = kwargs["parameters"]
        dTemplate               = kwargs["template"]

        lCandidates             = kwargs["candidates"]

        #   STEP 11: Loop through items in template
        for i in range(0, dTemplate["items"]):
            #   STEP 12: Setup - Tmp variables
            sTmp_Child          = dTemplate[str(i)]
            lTmp_Candidates     = []

            #   STEP 13: Check if dictionary
            try: 
                if ( type(dTemplate[sTmp_Child]) == dict):
                    #   STEP 14: Loop through candidates
                    for j in range(0, len(lCandidates)):
                        #   STEP 15: Populate candidates
                        lTmp_Candidates.append( lCandidates[j][sTmp_Child] )

                    #   STEP 16: Outsource
                    lTmp_Candidates = self.__remapData_Recursion__(template=dTemplate[sTmp_Child], data=kwargs["data"], candidates=lTmp_Candidates, parameters=dParams)
            
                    #   STEP 17: Loop through candidates
                    for j in range(0, len(lCandidates)):
                        #   STEP 18: Update - Candidate params
                        lCandidates[j][sTmp_Child] = lTmp_Candidates[j]
                        
                #   STEP 19: Not a dictionary
                elif ( type(dTemplate[sTmp_Child]) == str):
                    #   STEP 20: Be safe OwO
                    try:
                        #   STEP 21: Get parameter
                        iTmp_Parameter  = int( dTemplate[sTmp_Child].strip("remap-") )

                        #   STEP 22: Check if parameter being used
                        if (iTmp_Parameter in dParams["current"]):
                            #   STEP 23: Get index
                            iTmp_Index = dParams["current"].index(iTmp_Parameter)

                            #   STEP 24: Loop through candidates
                            for j in range(0, len(lCandidates)):
                                #   STEP 25: Update - Candidate params
                                lCandidates[j][sTmp_Child] = kwargs["data"][j][iTmp_Index]

                            Helga.nop()

                    except Exception as ex:
                        print("Initial error: ", ex)
            
            except Exception as ex:
                #   STEP ??: Check if items in child
                if ("items" in sTmp_Child):
                    #   STEP ??: Loop through items in child
                    for j in range(0, sTmp_Child["items"]):
                        #   STEP ??: Setup - Tmp variables
                        sTmp_GChild = sTmp_Child[str(j)]

                        #   STEP ??: Check if GChild is dict
                        if ( type(sTmp_GChild) == dict ):
                            lTmp_Candidates = []

                            #   STEP ??: Loop through candidates
                            for k in range(0, len( lCandidates )):
                                #   STEP ??: Populate candidate list
                                lTmp_Candidates.append( lCandidates[k][str(i)][str(j)])

                            #   STEP ??: Outsource - Recursively
                            lTmp_Candidates = self.__remapData_Recursion__(template=sTmp_GChild, data=kwargs["data"], candidates=lTmp_Candidates, parameters=dParams)

                            #   STEP ??: Loop through candidates
                            for k in range(0, len(lCandidates)):
                                #   STEP ??: Update - candidate vals
                                lCandidates[k][str(i)][str(j)] = lTmp_Candidates[k]

                        #   STEP ??: Not dictionary
                        else:
                            #   STEP ??: Get param num
                            iTmp_Parameter  = int( sTmp_Child[sTmp_GChild].strip("remap-") )

                            #   STEP ??: Check if parameter being used
                            if (iTmp_Parameter in dParams["current"]):
                                #   STEP ??: Get parameter index
                                iTmp_Index = dParams["current"].index(iTmp_Parameter)

                                #   STEP 24: Loop through candidates
                                for k in range(0, len(lCandidates)):
                                    #   STEP 25: Update - Candidate params
                                    lCandidates[k][str(i)][sTmp_GChild] = kwargs["data"][k][iTmp_Index]

                else:
                    #   STEP ??: Error handling
                    print("Initial error: ", ex)
                    raise Exception("An error occured in Natalie.__remapData_Recursion__() -> Step ??")
        
        #   STEP 18: Return
        return lCandidates

    def __remapData_Substrate__(self, **kwargs) -> dict:
        """
            Description:

                Updates the substrate for this antenna candidate.

            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:

                + candidate = ( dict ) A dictionary containing the antenna
                    candidate
                    ~ Required
        """

        #   STEP 0: Local variables
        dCandidate              = None

        #   STEP 1: Setup - Local variables
        
        #   STEP 2: Check if candidate arg passed
        if ("candidate" not in kwargs):
            #   STEP 3: Error handling
            raise Exception("An error occured in Natalie.__remapData_Substrate__() -> Step 2: No candidate arg passed")
        
        #   STEP 4: Setup - Local variables
        dCandidate  = kwargs["candidate"]

        #   region STEP 5->7: Setup - Substrate x

        #   STEP 5 if ground plane x less than radiating plane
        if (dCandidate["ground plane"]["x"] < dCandidate["radiating plane"]['x']):
            #   STEP 6: Set x = gp[x]
            dCandidate["substrate"]["x"] = dCandidate["ground plane"]["x"]

        else:
            #   STEP 7: Set x = rp[x]
            dCandidate["substrate"]["x"] = dCandidate["radiating plane"]["x"]

        #
        #   endregion

        #   region STEP 8->10: Get substrate y co-ordinate

        #   STEP 8: If gp y less than rp
        if (dCandidate["ground plane"]["y"] < dCandidate["radiating plane"]["y"]):
            #   STEP 9: Set y = gp[y]
            dCandidate["substrate"]["y"] = dCandidate["ground plane"]["y"]

        else:
            #   STEP 10: Set y = rp[yu]
            dCandidate["substrate"]["y"] = dCandidate["radiating plane"]["y"]
            
        #
        #   endregion

        #   region STEP 11->14: Get substrate length

        #   STEP 11: Get furthest on l axis
        fTmp_GP = dCandidate["ground plane"]["x"] + dCandidate["ground plane"]["l"]
        fTmp_RP = dCandidate["radiating plane"]["x"] + dCandidate["radiating plane"]["l"]

        #   STEP 12: If gp l less than rp
        if (fTmp_GP > fTmp_RP):
            #   STEP 13: Set l = gp
            dCandidate["substrate"]["l"] = fTmp_GP - dCandidate["substrate"]["x"]

        else:
            #   STEP 14: Set l = rp
            dCandidate["substrate"]["l"] = fTmp_RP - dCandidate["substrate"]["x"] + 0.05
            dCandidate["ground plane"]["l"] = fTmp_RP - dCandidate["ground plane"]["x"] + 0.05

        #
        #   endregion

        #   region STEP 15->18: Get substrate width

        #   STEP 15: Get furthest on W axis
        fTmp_GP = dCandidate["ground plane"]["y"] + dCandidate["ground plane"]["w"]
        fTmp_RP = dCandidate["radiating plane"]["y"] + dCandidate["radiating plane"]["w"]

        #   STEP 16: If gp W less than rp
        if (fTmp_GP > fTmp_RP):
            #   STEP 17: Set W = gp
            dCandidate["substrate"]["w"] = fTmp_GP - dCandidate["substrate"]["y"]

        else:
            #   STEP 18: Set W = rp
            dCandidate["substrate"]["w"] = fTmp_RP - dCandidate["substrate"]["y"] + 0.05

        #
        #   endregion

        #   STEP 19: Return
        return dCandidate
    
    #
    #       endregion

    #       region Back-End-(Data Management): Creation and desctruction

    def __saveData__(self, **kwargs) -> None:
        """
            Description:
            
                Saves the provided data to the appropriate location.

            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:

                + dir       = ( str ) The direcotry to save the data to
                    ~ Required

                + bestGeo   = ( dict ) Dictionary containing the geometry of
                    the current best antenna simulation

                + bestFit   = ( dict ) Dictionary containing the fitness data
                    for the current best antenna simulation

                + candidates    = ( list ) List of current antenna candidates
                    to be written to file for data base createion

                + fitness   = ( list ) List of current antenna candidate
                    fitness evaluations to be written to file for data base
                    creation
        """

        #   region STEP 0->7: Error checking

        #   STEP 0: Check if bestGeo arg passed
        if ("bestGeo" in kwargs):
            #   STEP 1: Check if bestFit arg passed
            if ("bestFit" not in kwargs):
                #   STEP 2: Error handling
                raise Exception("An error occured in Natalie.__saveData__() -> Step 1: No bestFit arg passed")
        
        #   STEP 3: Check if candidates arg passed
        if ("candidates" in kwargs):
            #   STEP 4: Check if fitness arg passed
            if ("fitness" not in kwargs):
                #   STEP 5: Error handling
                raise Exception("An error occured in Natalie.__saveData__() -> Step 4: No fitness arg passed")

        #   STEP 6: Check if dir arg passed
        if ("dir" not in kwargs):
            #   STEP 7: Error handling
            raise Exception("An error occured in Natalie.__saveData__() -> Step 6: No dir arg passed")

        #
        #   endregion

        #   region STEP 8->13: Dump best candidate

        #   STEP 8: Check if bestGeo arg passed
        if ("bestGeo" in kwargs):
            #   STEP 9: Setup - File location
            sTmp_File   = kwargs["dir"] + "\\" + Helga.ticks() + "_best.json"

            #   STEP 10: Create file
            vTmp_File   = open(sTmp_File, "a")
            vTmp_File.close()
            vTmp_File   = None

            #   STEP 11: Re-Open file
            with open(sTmp_File, "r+") as vTmp_File:
                #   STEP 12: Setup - Tmp dictionary
                dTmp = {
                    "geometry": kwargs["bestGeo"],
                    "fitness":  kwargs["bestFit"]
                }

                #   STEP 13: Dump data
                js.dump(dTmp, vTmp_File, indent=4, separators=(", ", " :\t"))
        
        #
        #   endregion

        #   region STEP 14->??: Dump all sims

        #   STEP 14: Check if candidates arg passed
        if ("candidates" in kwargs):
            #   STEP 15: Setup - File Directory
            sFile   = os.path.abspath(".") + "\\Data\\DataSets\\Antenna\\920\\" + Helga.ticks()

            #   STEP 16: Loop through candidates
            for i in range(0, len( kwargs["candidates"] ) ):
                #   STEP 17: Setup - File location
                sTmp_File   = sFile + "_" + str(i) + ".json"

                #   STEP 18: Create file
                vTmp_File   = open(sTmp_File, "a")
                vTmp_File.close()
                vTmp_File   = None

                #   STEP 19: Re-Open file
                with open(sTmp_File, "r+") as vTmp_File:
                    #   STEP 20: Create temp dictionary
                    dTmp    = {
                        "geometry": kwargs["candidates"][i],
                        "fitness":  kwargs["fitness"][i]
                    }

                    #   STEP 21: Dump data
                    js.dump(dTmp, vTmp_File, indent=4, separators=(", ", " :\t"))

        #
        #   endregion

        #   STEP 22: Return
        return

    def __cullData__(self, **kwargs) -> None:
        """
            Description:

                Culls the simulations in the list.

            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:

                + data  = ( list ) List of candidates dictionaries containing
                    "dir" entry
                    ~ Required

                + spare = ( int ) The index of a candidate to spare
                    ~ Default   = -1
        """

        #   region STEP 0->1: Error checking

        #   STEP 0: Check if data arg passed
        if ("data" not in kwargs):
            #   STEP 1: Error handling
            raise Exception("An error occured in Natalie.__cullData__() -> Step 0: No data arg passed")

        #
        #   endregion

        #   STEP 2: Local variables
        iSpare                  = -1

        #   STEP 3: Check if spare arg passed
        if ("spare" in kwargs):
            #   STEP 4: Update - Spare
            iSpare = kwargs["spare"]

            #   STEP 5: Loop through candidates
            for i in range(0, self.__iTRO_Candidates + 1 ):
                #   STEP 6: If not spare and not previous best
                if ((i != iSpare) and (i != self.__iTRO_Candidates)):
                    #   STEP 7: Get path for directory
                    sTmp_Path = os.path.dirname(kwargs["data"][i]["dir"])

                    #   STEP 8: If not center
                    if ("center" not in sTmp_Path):
                        #   STEP 9: Delete directory
                        sh.rmtree(sTmp_Path)

        #   STEP 10: Return
        return

    #
    #       endregion

    #
    #   endregion

    #   region Back-End: Optimization

    def __tro_Primary__(self, **kwargs) -> dict:
        """
            Description:

                Performs trust-region optimization of the candidate solution.

            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:

                + cull  = ( bool ) A flag that specifies whether of not
                    unworthy antenna candidate simulations should be deleted
                    from the local drive
                    ~ Required

                + save  = ( bool ) A flag that specifies whether or not
                    continuous saving of the best candidate in an algorithm
                    should be done
                    ~ Required
        """

        #   region STEP 0->3: Error checking

        #   STEP 0: Check if cull arg passed
        if ("cull" not in kwargs):
            #   STEP 1: Error handling
            raise Exception("An error occured in Natalie.__tro_Primary__() -> Step 0: No cull arg passed")

        #   STEP 2: Check if save arg passed
        if ("save" not in kwargs):
            #   STEP 3: Error handling
            raise Exception("An error occured in Natalie.__tro_Primary__() -> Step 2: No save arg passed")

        #
        #   endregion

        #   STEP 4: Local varialbes
        dBest_Geo               = None
        dBest_Fit               = None

        sDir                    = None

        iRegion                 = cp.deepcopy( self.__iTRO_Region )
        iIterations             = cp.deepcopy( self.__iTRO_Iterations_Primary )

        bCull                   = kwargs["cull"]
        bSave                   = kwargs["save"]

        #   region STEP 5->10: Setup - Local variables

        #   STEP 5: Make optimization project directory
        sDir    = self.__sDirectory + Helga.ticks() + "_Primary"
        os.mkdir(sDir)

        #   STEP 6: User output
        if (self.bShowOutput):
            print("Natalie (tro-Primary) {" + Helga.time() + "} - Simulating starting antenna geometry")

        #   STEP 7: Outsource - Simulate center
        self.__dAnt_Center  = Matthew.getPatch_Default(name="center", dir=sDir, substrate=self.__dAnt_Substrate, frequency=self.__dAnt_Frequency, mesh=self.__dAnt_Mesh, runt=self.__dAnt_Runt, fitness=self.__dAnt_Fitness)
        
        #   STEP 8: Setup - Center geometry
        dBest_Geo           = cp.deepcopy(self.__dAnt_Center)
        dBest_Fit           = {
            "fitness":  dBest_Geo["fitness"],
            "dir":      dBest_Geo["dir"]
        }

        del dBest_Geo["fitness"]
        del dBest_Geo["dir"]

        #   STEP 9: Setup - Center fitness
        dBest_Fit               = self.__getFitness__(ant=[dBest_Geo], fitness=[dBest_Fit])[0]
        self.__dAnt_CenterFit   = cp.deepcopy(dBest_Fit)
        
        #
        #   endregion

        #   STEP 11: User output
        if (self.bShowOutput):
            print("Natalie (tro-Primary) {" + Helga.time() + "} - Begining Trust-Region Optimization.")

        #   region STEP 12->46: TRO - Primary

        #   STEP 12: Loop
        for i in range(0, iIterations):
            #   STEP 13: Setup - Scope variables
            lCandidates         = []
            lFitness            = []

            iTmp_Candidates     = self.__iTRO_Candidates
            iTmp_Region         = self.__fTRO_RegionScalar_Primary * float( iRegion ) / float( self.__iTRO_Region )

            iTmp_BestIndex      = 0
            iTmp_Count          = 0

            #   region STEP 14->27: Candidate generation and simulation
            
            #   STEP 14: Loop
            while (True):
                #   STEP 15: Setup - Get candidate list
                lTmp_Candidates = self.__getCandidates_Primary__(center=dBest_Geo, region=iTmp_Region, candidates=iTmp_Candidates)

                #   STEP 16: User output
                if (self.bShowOutput):
                    print("\n\t{" + Helga.time() + "} - Simulating " + str(iTmp_Candidates) + " candidate antennas")

                #   STEP 17: Simulate antennas
                lTmp_Fitness    = Matthew.simulateCandidates_Json(dir=sDir, ant=lTmp_Candidates, frequency=self.__dAnt_Frequency, mesh=self.__dAnt_Mesh, runt=self.__dAnt_Runt, fitness=self.__dAnt_Fitness)

                #   STEP 18: Evaluate overall fitness of all geometries
                lTmp_Fitness    = self.__getFitness__(ant=lTmp_Candidates, fitness=lTmp_Fitness)

                #   STEP 19: Loop through all candidates
                while (iTmp_Count < len( lTmp_Candidates )):
                    #   STEP 20: Check that default fitness library wasn't returned
                    if ( lTmp_Fitness[iTmp_Count]["desired"] == np.inf):
                        #   STEP 21: Pop from list and remove directory
                        sh.rmtree(os.path.dirname(lTmp_Fitness[iTmp_Count]["dir"]))

                        lTmp_Candidates.pop(iTmp_Count)
                        lTmp_Fitness.pop(iTmp_Count)

                    #   STEP 22: Not default library
                    else:
                        #   STEP 23: Increment counter
                        iTmp_Count  += 1

                #   STEP 24: Append results and fitnesses to lists
                lCandidates.extend(lTmp_Candidates)
                lFitness.extend(lTmp_Fitness)

                #   STEP 25: Check that required number of candidates met
                if (len( lCandidates ) == self.__iTRO_Candidates):
                    #   STEP 26: Exit loop
                    break

                #   STEP 27: Recalculate candidates
                iTmp_Candidates = self.__iTRO_Candidates - len( lCandidates )

            #
            #   endregion

            #   STEP 28: Append current center to lists
            lCandidates.append(dBest_Geo)
            lFitness.append(dBest_Fit)

            #   STEP 29: Outsource - Candidate evaluation
            iTmp_BestIndex  = self.__getCandidate_Best__(lFitness)

            #   STEP 30: Set new best candidate
            dBest_Geo   = lCandidates[iTmp_BestIndex]
            dBest_Fit   = lFitness[iTmp_BestIndex]

            #   STEP 31: Check - Save status
            if (bSave):
                #   STEP 32: Outsource - Continuous save
                self.__saveData__(dir=sDir, bestGeo=dBest_Geo, bestFit=dBest_Fit, candidates=lCandidates, fitness=lFitness)

            #   STEP 33: Check - Culling status
            if (bCull):
                #   STEP 34: Outsource - Cull the weak :)
                self.__cullData__(data=lFitness, spare=iTmp_BestIndex)

            #   region STEP 35->43: Region Update

            #   STEP 35: Check if new best
            if (iTmp_BestIndex != self.__iTRO_Candidates):
                #   STEP 36: Update region
                iRegion += 1
                iTmp_Region = round( float(iRegion) / float(self.__iTRO_Region ), 3)

                #   STEP 37: User output
                if (self.bShowOutput):
                    print("\t{" + Helga.time() + "} - Iteration (" + str(i + 1) + "/" + str(iIterations) + ") : Increasing region -> " + str(iTmp_Region))

                    dHold = lFitness[self.__iTRO_Candidates]
                    print("\t\t-Initial:",  "area=" + str(round(dHold["area"] * 100.0, 3)), "freq=" + str(round(dHold["freq"] * 100.0, 3)), "final=" + str(round(dHold["final"] * 100.0, 3)), sep="\t")
                    
                    dHold = lFitness[iTmp_BestIndex]
                    print("\t\t-New:\t",    "area=" + str(round(dHold["area"] * 100.0, 3)), "freq=" + str(round(dHold["freq"] * 100.0, 3)), "final=" + str(round(dHold["final"] * 100.0, 3)), sep="\t", end="\n\n")

            #   STEP 38: Not new best
            else:
                #   STEP 39: Check if region too small
                if (iRegion > 0):
                    #   STEP 40: Update - Decrement region
                    iRegion     -= 1
                    iTmp_Region = round( float(iRegion) / float(self.__iTRO_Region ), 3)

                    #   STEP 41: User output
                    if (self.bShowOutput):
                        print("\t{" + Helga.time() + "} - Iteration (" + str(i + 1) + "/" + str(iIterations) + ") : Decreasing region -> " + str(iTmp_Region), end="\n\n")
                
                #   STPE 42: Region too small
                else:
                    #   STEP 43: Exit loop
                    break

            #
            #   endregion

            #   region STEP 44->50: Early Exit

            #   STEP 44: Check - Early Exit status
            if (self.bEarlyExit):
                #   STEP 45: Check area
                if (dBest_Fit["area"] <= self.__fTRO_EarlyExit_Area):
                    #   STEP 46: User output
                    if (self.bShowOutput):
                        print("\t{" + Helga.time() + "} - Miniaturization goal met; exiting Primary Optimization early")

                    #   STEP 47: Exit loop
                    break

                #   STEP 48: Check fitness
                if (dBest_Fit["final"] <= self.__fTRO_EarlyExit_Fitness):
                    #   STEP 49: User output
                    if (self.bShowOutput):
                        print("\t{" + Helga.time() + "} - Fitness goal met; exiting Primary Optimization early")

                    #   STEP 50: User output
                    break
            
            #
            #   endregion

        #
        #   endregion

        #   STEP 51: Populate output dictionary
        dOut    = {
            "result":   dBest_Geo,
            "fitness":  dBest_Fit
        }
        
        #   STEP 52: Return
        return dOut

    def __tro_Secondary__(self, **kwargs) -> dict:
        """
            Description:

                Performs trust-region optimization of the candidate solution.

            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:

                + center    = ( dict ) The candidate solution to be optimized
                    ~ Required

                + cull  = ( bool ) A flag that specifies whether of not
                    unworthy antenna candidate simulations should be deleted
                    from the local drive
                    ~ Required

                + save  = ( bool ) A flag that specifies whether or not
                    continuous saving of the best candidate in an algorithm
                    should be done
                    ~ Required
        """

        #   region STEP 0->5: Error checking

        #   STEP 0: Check if center passed
        if ("center" not in kwargs):
            #   STEP 1: Error handling
            raise Exception("An error occured in Natalie.__tro_Secondary__() -> Step 0: No center arg passed")

        #   STEP 2: Check if cull arg passed
        if ("cull" not in kwargs):
            #   STEP 3: Error handling
            raise Exception("An error occured in Natalie.__tro_Secondary__() -> Step 2: No cull arg passed")

        #   STEP 4: Check if save arg passed
        if ("save" not in kwargs):
            #   STEP 5: Error handling
            raise Exception("An error occured in Natalie.__tro_Secondary__() -> Step 4: No save arg passed")

        #
        #   endregion

        #   STEP 6: Local variables
        dBest_Geo               = kwargs["center"]["result"]
        dBest_Fit               = kwargs["center"]["fitness"]

        dParameters             = None

        lInputs                 = []
        lOutputs                = []

        sDir                    = None

        iIterations_Main        = cp.deepcopy( self.__iTRO_Iterations_Secondary )
        iIterations_Grace       = cp.deepcopy( self.__iTRO_Iterations_Grace )

        iRegion_Alg             = cp.deepcopy( self.__iTRO_Region )
        iRegion_Srg             = cp.deepcopy( self.__iTRO_Region_SRG )

        bCull                   = kwargs["cull"]
        bSave                   = kwargs["save"]

        #   STEP 7: Setup - Project Folder
        sDir            = self.__sDirectory + Helga.ticks() + "_Secondary"
        os.mkdir(sDir)

        #   STEP 8: User output
        if (self.bShowOutput):
            print("Natalie (tro-Secondary) {" + Helga.time() + "} - Begining Trust-Region Optimization.")

        #   region STEP 9->56: TRO - Secondary

        #   STEP 9: Loop - Main
        for _ in range(0, iIterations_Main):
            #   STEP 10: Setup - Scope variables
            lInputs     = []
            lOutputs    = []

            iRegion_Srg = cp.deepcopy(self.__iTRO_Region_SRG)

            dParameters = self.__getParameters_Secondary__(center=dBest_Geo, region=iRegion_Srg)

            #   STEP 11: Loop - Grace
            for j in range(0, iIterations_Grace):
                #   STEP 12: Setup - Scope variables
                lCandidates         = []
                lFitness            = []

                iTmp_Candidates     = self.__iTRO_Candidates_Secondary
                iTmp_Region         = self.__fTRO_RegionScalar_Secondary * float(iRegion_Srg + iRegion_Alg) / float(self.__iTRO_Region_SRG + self.__iTRO_Region)

                iTmp_BestIndex      = 0
                iTmp_Count          = 0

                dTmp_Region         = {
                    "unscaled-srg": iRegion_Srg,
                    "unscaled-alg": iRegion_Alg,
                    "scaled":       iTmp_Region
                }

                #   region STEP 11->26: Candidate generation and simulation

                #   STEP 13: Loop
                while (True):
                    #   STEP 14: Setup - Temp variables
                    lTmp_Candidates = self.__getCandidates_Secondary__(center=dBest_Geo, region=dTmp_Region, candidates=iTmp_Candidates, parameters=dParameters)

                    #   STEP 15: User output
                    if (self.bShowOutput):
                        print("\n\t{" + Helga.time() + "} - Simulating " + str(iTmp_Candidates) + " candidate antennas")

                    #   STEP 16: Simulate antennas
                    lTmp_Fitness    = Matthew.simulateCandidates_Json(dir=sDir, ant=lTmp_Candidates, frequency=self.__dAnt_Frequency, mesh=self.__dAnt_Mesh, runt=self.__dAnt_Runt, fitness=self.__dAnt_Fitness)

                    #   STEP 17: Evaluate overall fitness of all geometries
                    lTmp_Fitness    = self.__getFitness__(ant=lTmp_Candidates, fitness=lTmp_Fitness)

                    #   STEP 18: Loop through all candidates
                    while (iTmp_Count < len( lTmp_Candidates )):
                        #   STEP 19: Check that default fitness library wasn't returned
                        if ( lTmp_Fitness[iTmp_Count]["desired"] == np.inf):
                            #   STEP 20: Pop from list
                            sh.rmtree(os.path.dirname(lTmp_Fitness[iTmp_Count]["dir"]))

                            lTmp_Candidates.pop(iTmp_Count)
                            lTmp_Fitness.pop(iTmp_Count)

                        #   STEP 21: Not default library
                        else:
                            #   STEP 22: Increment counter
                            iTmp_Count  += 1

                    #   STEP 23: Append results and fitnesses to lists
                    lCandidates.extend(lTmp_Candidates)
                    lFitness.extend(lTmp_Fitness)

                    #   STEP 24: Check that required number of candidates met
                    if (len( lCandidates ) == self.__iTRO_Candidates_Secondary):
                        #   STEP 25: Exit loop
                        break

                    #   STEP 26: Recalculate candidates
                    iTmp_Candidates =  iTmp_Candidates - len( lCandidates )

                #
                #   endregion

                #   STEP 27: Append current best to lists
                lCandidates.append(dBest_Geo)
                lFitness.append(dBest_Fit)

                #   STEP 28: Mold current data set
                dTmp_MoldedData     = self.__moldData__(candidates=lCandidates, fitness=lFitness)

                #   STEP 29: Add new data to data list
                lInputs.extend( Helga.transpose( dTmp_MoldedData["in"]) )
                lOutputs.extend( Helga.transpose( dTmp_MoldedData["out"]) )

                #   region STEP 30->39: Surrogate stuffs

                #   STEP 30: Be safe OwO
                try:
                    #   STEP 31: Get surrogate results
                    lTmp_SrgCandidates  = self.__getSurrogate_Results__(center=dBest_Geo, inputs=cp.deepcopy(lInputs), outputs=cp.deepcopy(lOutputs), parameters=dParameters, region=dTmp_Region)
                    
                    #   STEP 32: User output
                    if (self.bShowOutput):
                        print("\n\n\t{" + Helga.time() + "} - Simulating " + str(len(lTmp_SrgCandidates)) + " surrogate candidate antennas")

                    #   STEP 33: Simulate antennas
                    lTmp_SrgFitness     = Matthew.simulateCandidates_Json(dir=sDir, ant=lTmp_SrgCandidates, frequency=self.__dAnt_Frequency, mesh=self.__dAnt_Mesh, runt=self.__dAnt_Runt, fitness=self.__dAnt_Fitness)
                    lTmp_SrgFitness    = self.__getFitness__(ant=lTmp_SrgCandidates, fitness=lTmp_SrgFitness)

                    #   STEP 34: Append to candidate and fitness lists
                    lCandidates.extend( lTmp_SrgCandidates )
                    lFitness.extend( lTmp_SrgFitness )

                    #   STEP 35: Mold surrogate data list
                    dTmp_MoldedData     = self.__moldData__(candidates=lTmp_SrgCandidates, fitness=lTmp_SrgFitness)

                    #   STEP 36: Add new data to data list
                    lInputs.extend( Helga.transpose( dTmp_MoldedData["in"]) )
                    lOutputs.extend( Helga.transpose( dTmp_MoldedData["out"]) )
                
                except Exception as ex:
                    #   STEP 37: Error handling
                    print("\t{" + Helga.time() + "} - An error occured during surrogate tnm")
                    print("\t\t-Error:", ex, sep="\t")

                    #   STEP 38: Check surrogate region
                    if (iRegion_Srg > 0):
                        #   STEP 39: Decrement surrogate region
                        iRegion_Srg -= 1

                #
                #   endregion

                #   region STEP 40->45: Candidate evaluation

                finally:
                    #   STEP 40: Outsource - Candidate evaluation
                    iTmp_BestIndex  = self.__getCandidate_Best__(lFitness)

                    #   STEP 41: Set new best candidate
                    dBest_Geo   = lCandidates[iTmp_BestIndex]
                    dBest_Fit   = lFitness[iTmp_BestIndex]
                    
                    #   STEP 42: Check - Save status
                    if (bSave):
                        #   STEP 43: Outsource - Continuous save
                        self.__saveData__(dir=sDir, bestGeo=dBest_Geo, bestFit=dBest_Fit, candidates=lCandidates, fitness=lFitness)

                    #   STEP 44: Check - Culling status
                    if (bCull):
                        #   STEP 45: Outsource - Cull the weak :)
                        self.__cullData__(data=lFitness, spare=iTmp_BestIndex)

                #
                #   endregion

                #   region STEP 46->67: Region Update
                    
                #   STEP 46: Check if best is surrogate candidates
                if (iTmp_BestIndex > self.__iTRO_Candidates_Secondary):
                    #   STEP 47: Update - Region
                    iRegion_Alg         += 1
                    iRegion_Srg         += 1
                    
                    #   STEP 48: User output
                    if (self.bShowOutput):
                        #   STEP 49: Get current region
                        iTmp_Region         = round( float(iRegion_Alg + iRegion_Srg) / float(self.__iTRO_Region + self.__iTRO_Region_SRG), 3)

                        #   STEP 50: Print output
                        print("\t{" + Helga.time() + "} - Iteration (" + str(j + 1) + "/" + str(iIterations_Grace) + ") : Increasing region via surrogate -> " + str(iTmp_Region))

                        dHold = lFitness[self.__iTRO_Candidates_Secondary]
                        print("\t\t-Initial:",  "area=" + str(round(dHold["area"] * 100.0, 3)), "freq=" + str(round(dHold["freq"] * 100.0, 3)), "final=" + str(round(dHold["final"] * 100.0, 3)), sep="\t")
                        
                        dHold = lFitness[iTmp_BestIndex]
                        print("\t\t-SRG:\t",    "area=" + str(round(dHold["area"] * 100.0, 3)), "freq=" + str(round(dHold["freq"] * 100.0, 3)), "final=" + str(round(dHold["final"] * 100.0, 3)), sep="\t", end="\n\n")

                #   STEP 51: Check if new best isn't old best
                elif (iTmp_BestIndex != self.__iTRO_Candidates_Secondary):
                    #   STEP 52: Update region
                    iRegion_Alg     += 1

                    #   STEP 53: Check if surrogate region not too small
                    if (iRegion_Srg > 0):
                        #   STEP 54: Update surrogate region
                        iRegion_Srg     -= 1

                    #   STEP 55: User output
                    if (self.bShowOutput):
                        #   STEP 56: Get new region
                        iTmp_Region         = round( float(iRegion_Alg + iRegion_Srg) / float(self.__iTRO_Region + self.__iTRO_Region_SRG), 3)
                        
                        #   STEP 57: Print output
                        print("\t{" + Helga.time() + "} - Iteration (" + str(j + 1) + "/" + str(iIterations_Grace) + ") : Increasing region -> " + str(iTmp_Region))

                        dHold = lFitness[self.__iTRO_Candidates_Secondary]
                        print("\t\t-Initial:",  "area=" + str(round(dHold["area"] * 100.0, 3)), "freq=" + str(round(dHold["freq"] * 100.0, 3)), "final=" + str(round(dHold["final"] * 100.0, 3)), sep="\t")
                        
                        dHold = lFitness[iTmp_BestIndex]
                        print("\t\t-New:\t",    "area=" + str(round(dHold["area"] * 100.0, 3)), "freq=" + str(round(dHold["freq"] * 100.0, 3)), "final=" + str(round(dHold["final"] * 100.0, 3)), sep="\t")
                        
                        dHold = lFitness[len(lFitness) - 1]
                        print("\t\t-SRG:\t",    "area=" + str(round(dHold["area"] * 100.0, 3)), "freq=" + str(round(dHold["freq"] * 100.0, 3)), "final=" + str(round(dHold["final"] * 100.0, 3)), sep="\t", end="\n\n")

                #   STEP 58: Bad region
                else:
                    #   STEP 59: Check if alg region not too small
                    if (iRegion_Alg > 0):
                        #   STEP 60: Update region
                        iRegion_Alg     -= 1

                        #   STEP 61: Check if surrogate region not too small
                        if (iRegion_Srg > 0):
                            #   STEP 62: Update surrogate region
                            iRegion_Srg     -= 1

                        #   STEP 63: User output
                        if (self.bShowOutput):
                            #   STEP 64: Get new region
                            iTmp_Region = round( float(iRegion_Alg + iRegion_Srg) / float(self.__iTRO_Region + self.__iTRO_Region_SRG), 3)
                            
                            #   STEP 65: Print output
                            print("\t{" + Helga.time() + "} - Iteration (" + str(j + 1) + "/" + str(iIterations_Grace) + ") : Decreasing region -> " + str(iTmp_Region))

                            dHold = lFitness[self.__iTRO_Candidates]
                            print("\t\t-Initial:",  "area=" + str(round(dHold["area"] * 100.0, 3)), "freq=" + str(round(dHold["freq"] * 100.0, 3)), "final=" + str(round(dHold["final"] * 100.0, 3)), sep="\t")
                            
                            dHold = lFitness[ iTmp_BestIndex ]
                            print("\t\t-SRG:\t",    "area=" + str(round(dHold["area"] * 100.0, 3)), "freq=" + str(round(dHold["freq"] * 100.0, 3)), "final=" + str(round(dHold["final"] * 100.0, 3)), sep="\t", end="\n\n")

                    #   STEP 66: Region too small
                    else:
                        #   STEP 67: Exit loop
                        break

                #
                #   endregion

            #   STEP 68: Check if region too small
            if (iRegion_Alg <= 0):
                #   STEP 69: Exit loop
                break

        #
        #   endregion

        #   STEP 81: Populate output dictionary
        dOut    = {
            "result":   dBest_Geo,
            "fitness":  dBest_Fit
        }

        #   STEP 82: Return
        return dOut

    def __nm__(self, **kwargs) -> dict:
        """
        """

        #   STEP 0: Local variables
        #   STEP 1: Setup - Local variables
        #   STEP 2: ??
        #   STEP ??: Return
        return {}

    #
    #   endregion

    #
    #endregion

#
#endregion

#region Testing

if (__name__ == "__main__"):
    
    dAnt = {
        "substrate":
        {
            "permitivitty": 4.4,
            "loss":         0.02,
            "name":         "FR4",
            "height":       1.6
        },
        "frequency":
        {
            "start":        0.9e9,
            "end":          0.94e9
        }
    }

    while (True):
        os.system("cls")

        nat = Natalie(ant=dAnt)
        nat.bEarlyExit  = True

        nat.optimizeAntenna(primary="tro", secondary="tro", surrogate=True)

#
#endregion
