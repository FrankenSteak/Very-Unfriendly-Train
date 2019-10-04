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
        self.__dAnt_Best        = None

        self.__cAnt_Default     = None

        #   endregion

        #   region  STEP 1.2: TRO Params

        self.__iTRO_Iterations  = None
        self.__iTRO_Candidates  = None

        self.__iTRO_Region      = None
        self.__iTRO_Region_SRG  = None

        self.__fTRO_Acc         = None

        #   endregion

        #   region STEP 1.3: TRO Runtime requirements

        self.__dTemplate        = None

        #   endregion

        #endregion

        #   STEP 2: Public variables
        self.bShowOutput        = self.__cf.data["parameters"]["show output"]

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

        bNew                    = True
        bCull                   = True
        bSave                   = True
        bSurrogate              = True

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
        
        #   region STEP 6->13: Update - Local variables

        #   STEP 6: Check if new arg passed
        if ("new" in kwargs):
            #   STEP 7: Update - Local variables
            bNew = kwargs["new"]

        #   STEP 8: Check if cull arg passed
        if ("cull" in kwargs):
            #   STEP 9: Update - Local variables
            bCull   = kwargs["cull"]

        #   STEP 10: Check if save arg passed
        if ("save" in kwargs):
            #   STEP 11: Update - Local variables
            bSave   = kwargs["save"]

        #   STEP 12: Check if surrogate arg passed
        if ("surrogate" in kwargs):
            #   STEP 13: Update - Local variables
            bSurrogate  = kwargs["surrogate"]

        #
        #   endregion
        
        #   region STEP 14->19: Primary optimization

        #   STEP 14: Check if primary is tro
        if (kwargs["primary"] == "tro"):
            #   STEP 15: Outsource
            dPrimary_Results    = self.__tro__(stage="Primary", new=bNew, cull=bCull, save=bSave, surrogate=False)

        #   STEP 16: Check if primary is nm
        elif (kwargs["primary"] == "nm"):
            #   STEP 17: Outsource
            dPrimary_Results    = self.__nm__(stage="Primary", new=bNew, cull=bCull, save=bSave, surrogate=False)

        #   STEP 18: Unrecognized optimizer
        else:
            #   STEP 19: Error handling
            raise Exception("An error occured in Natalie.optimizeAntenna() -> Step 18: Unrecognized optimizer")

        #
        #   endregion

        #   region STEP 20->25: Secondary optimization

        #   STEP 20: Check if secondary is tro
        if (kwargs["secondary"] == "tro"):
            #   STEP 21: Outsource
            self.__tro__(stage="Secondary", center=dPrimary_Results, new=False, cull=bCull, save=bSave, surrogate=bSurrogate)

        #   STEP 22: Check if secondary is nm
        if (kwargs["secondary"] == "nm"):
            #   STEP 23: Outsource
            self.__nm__(stage="Secondary", center=dPrimary_Results, new=False, cull=bCull, save=bSave, surrogate=bSurrogate)

        #   STEP 24: Unrecognized optimizer
        else:
            #   STEP 25: Error handling
            raise Exception("An error occured in Natalie.optimizeAntenna() -> Step 24: Unrecognized optimizer")

        #
        #   endregion

        #   STEP 26: Return
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

        self.__iTRO_Iterations  = self.__cf.data["parameters"]["trust region"]["iterations"]
        self.__iTRO_Candidates  = self.__cf.data["parameters"]["trust region"]["candidates"]
        self.__iTRO_Region      = self.__cf.data["parameters"]["trust region"]["algorithm region"]
        self.__iTRO_Region_SRG  = self.__cf.data["parameters"]["trust region"]["surrogate region"]

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

        #   STEP 0: Local variables
        dFrequency              = None

        #   STEP 1: Setup - Local variables

        #   STEP 2: Check if ant arg passed
        if ("ant" not in kwargs):
            #   STEP 3: Error handling
            raise Exception("An error occured in Natalie.__initAnt__() -> Step 2: No ant arg passed")

        #   STEP 4: Update - class variables
        self.__dAnt_Substrate   = kwargs["ant"]["substrate"]

        self.__dAnt_Fitness     = {
            "desired":
            {
                "start":    kwargs["ant"]["frequency"]["start"],
                "end":      kwargs["ant"]["frequency"]["end"]
            }
        }

        #   STEP 5: check if number of samples > 2
        if (self.__cf.data["parameters"]["frequency"]["samples"] >= 5):
            #   STEP 6: Set frequency parameters accordingly
            self.__dAnt_Frequency   = {
                "center":   round(kwargs["ant"]["frequency"]["start"] + ( kwargs["ant"]["frequency"]["end"] - kwargs["ant"]["frequency"]["start"] ) / 2.0, 2),
                "start":    round(kwargs["ant"]["frequency"]["start"] - self.__cf.data["parameters"]["frequency"]["lower frequency offset"], 2),
                "end":      round(kwargs["ant"]["frequency"]["end"] + self.__cf.data["parameters"]["frequency"]["upper frequency offset"], 2),
                "samples":  self.__cf.data["parameters"]["frequency"]["samples"]
            }

        #   STEP 7: check if number of samples > 1
        elif (self.__cf.data["parameters"]["frequency"]["samples"] > 1):
            #   STEP 7: Set frequency parameters accordingly
            self.__dAnt_Frequency   = {
                "center":   round(kwargs["ant"]["frequency"]["start"] + ( kwargs["ant"]["frequency"]["end"] - kwargs["ant"]["frequency"]["start"] ) / 2.0, 2),
                "start":    round(kwargs["ant"]["frequency"]["start"] + ( self.__cf.data["parameters"]["frequency"]["lower frequency offset"] * 0.375 ), 2),
                "end":      round(kwargs["ant"]["frequency"]["end"] - ( self.__cf.data["parameters"]["frequency"]["upper frequency offset"] * 0.375 ), 2),
                "samples":  self.__cf.data["parameters"]["frequency"]["samples"]
            }

        #   STEP 9: Check that frequency samples not 0
        elif (self.__cf.data["paramters"]["frequency"]["samples"] > 0):
            #   STEP 10: Set frequency parameters accordingly
            self.__dAnt_Frequency   = {
                "center":   round(kwargs["ant"]["frequency"]["start"] + ( kwargs["ant"]["frequency"]["end"] - kwargs["ant"]["frequency"]["start"] ) / 2.0, 2),
                "start":    round(kwargs["ant"]["frequency"]["start"] + ( kwargs["ant"]["frequency"]["end"] - kwargs["ant"]["frequency"]["start"] ) / 2.0, 2),
                "end":      round(kwargs["ant"]["frequency"]["start"] + ( kwargs["ant"]["frequency"]["end"] - kwargs["ant"]["frequency"]["start"] ) / 2.0, 2),
                "samples":  self.__cf.data["parameters"]["frequency"]["samples"]
            }

        else:
            #   STEP 11: Error handling
            raise Exception("An error occured in Natalie.__initAnt__() -> Step 11: Invalid sample number set in config file")

        #   STEP 12: Update - Local variables
        dFrequency = cp.deepcopy(self.__dAnt_Frequency)
        dFrequency["samples"] = self.__cf.data["parameters"]["frequency"]["accuracy check samples"]

        #   STEP 15: Return
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

    def __getCandidates__(self, **kwargs) -> list:
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
        iRegion                 = None

        #   STEP 1: Setup - Local variables
        
        #   region STEP 2->7: Error checking

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

        #   STEP 8: Update - Local variables
        dCenter     = kwargs["center"]
        dScalars    = self.__cAnt_Default["scalars"]

        iCandidates = kwargs["candidates"]
        iRegion     = kwargs["region"]

        #   STEP 9: Loop for required number of candidates
        for _ in range(0, iCandidates):
            #   STEP 10: Create new candidate
            dTmp_Candidate = {
                "items":    3,
                
                "0":        "feed",
                "1":        "ground plane",
                "2":        "radiating plane",
                "3":        "substrate",

                "feed":
                {
                    "items":    2,
                    
                    "0":        "center",
                    "1":        "width",

                    "center":   self.__randVal__(center=dCenter["feed"]["center"], scalars=dScalars["feed"]["center"], region=iRegion),
                    "width":    self.__randVal__(center=dCenter["feed"]["width"], scalars=dScalars["feed"]["width"], region=iRegion)
                },
                "ground plane":
                {
                    "items":    5,

                    "0":        "l",
                    "1":        "w",
                    "2":        "x",
                    "3":        "y",
                    "4":        "slots",

                    "l":        self.__randVal__(center=dCenter["ground plane"]["l"], scalars=dScalars["ground plane"]["l"], region=iRegion),
                    "w":        self.__randVal__(center=dCenter["ground plane"]["w"], scalars=dScalars["ground plane"]["w"], region=iRegion),
                    "x":        self.__randVal__(center=dCenter["ground plane"]["x"], scalars=dScalars["ground plane"]["x"], region=iRegion),
                    "y":        self.__randVal__(center=dCenter["ground plane"]["y"], scalars=dScalars["ground plane"]["y"], region=iRegion),

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
                    
                    "l":        self.__randVal__(center=dCenter["radiating plane"]["l"], scalars=dScalars["radiating plane"]["l"], region=iRegion),
                    "w":        self.__randVal__(center=dCenter["radiating plane"]["w"], scalars=dScalars["radiating plane"]["w"], region=iRegion),
                    "x":        self.__randVal__(center=dCenter["radiating plane"]["x"], scalars=dScalars["radiating plane"]["x"], region=iRegion),
                    "y":        self.__randVal__(center=dCenter["radiating plane"]["y"], scalars=dScalars["radiating plane"]["y"], region=iRegion),

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
                    "h":        self.__randVal__(center=dCenter["substrate"]["h"], scalars=dScalars["substrate"]["h"], region=iRegion),
                    "x":        0.0,
                    "y":        0.0,

                    "permitivitty": dCenter["substrate"]["permitivitty"],
                    "loss":         dCenter["substrate"]["loss"],
                    "name":         dCenter["substrate"]["name"]
                }
            }

            #   STEP 11: Update - Candidate substrate
            self.__remapData_Substrate__(candidate=dTmp_Candidate)

            #   region STEP 12: Get plane slots

            dTmp_Candidate["ground plane"]["slots"] = self.__randSlots__(center=dCenter["ground plane"]["slots"], scalars=dScalars["ground plane"]["slots"], plane=dTmp_Candidate["ground plane"], z=0.0, region=iRegion + 1)
            dTmp_Candidate["radiating plane"]["slots"] = self.__randSlots__(center=dCenter["radiating plane"]["slots"], scalars=dScalars["radiating plane"]["slots"], plane=dTmp_Candidate["radiating plane"], z=dTmp_Candidate["substrate"]["h"], region=iRegion + 1)
            
            #
            #   endregion

            #   STEP 13: Append new candidate to output list
            lOut.append(dTmp_Candidate)
            
        #   STEP 15: Return
        return lOut

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

        fArea_Original          = None

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

        #   STEP 7: Update - Local variables
        fArea_Original = self.__dAnt_Center["substrate"]["l"] * self.__dAnt_Center["substrate"]["w"]

        #   STEP 6: Iterate through antenna
        for i in range(0, len(kwargs["ant"])):
            #   STEP 7: Get current ant and fitness
            dAnt = kwargs["ant"][i]
            dFit = kwargs["fitness"][i]["fitness"]["frequency"]

            #   STEP 8: Calculate area of antenna
            fTmp_Area   = dAnt["substrate"]["l"] * dAnt["substrate"]["w"]

            #   STEP 9: Get left fitness
            fTmp_Left   = ( dFit["lower"]["total"] ) * 0.5

            #   STEP 10: Get center firness
            fTmp_Mid    = ( dFit["desired"]["total"] ) * 0.7

            #   STEP 11: Get right fitness
            fTmp_Right  = ( dFit["upper"]["total"] ) * 0.3

            #   STEP 12: Get total area fitness
            fTmp_Area_Tot   = fTmp_Area / fArea_Original

            #   STEP 13: Get total frequency fitness
            fTmp_Freq_Tot   = fTmp_Left + fTmp_Mid + fTmp_Right

            #   STEP 14: Get overall fitness
            fTmp_Fitness    = self.__aActivation.logistic( fTmp_Area_Tot * 8.0  - 6.0 ) 
            fTmp_Fitness    = fTmp_Fitness * fTmp_Freq_Tot +  0.8 * fTmp_Freq_Tot  + 0.8 * fTmp_Fitness

            #   STEP 15: Populate output dictionary
            dTmp = {
                "items":    2,

                "0":        "freq",
                "1":        "area",

                "lower":    dFit["lower"]["total"],
                "desired":  dFit["desired"]["total"],
                "upper":    dFit["upper"]["total"],

                "area":     fTmp_Area_Tot,
                "freq":     fTmp_Freq_Tot,
                "final":    fTmp_Fitness
            }

            #   STEP 16: Append to output
            lOut.append(dTmp)

        #   STEP 3: Return
        return lOut

    #
    #   endregion

    #   region Back-End: Random functions

    def __randVal__(self, **kwargs) -> float:
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
        fOffset                 = None

        bRegion                 = None

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

        #   region STEP 10->21: Get random region
        
        #   STEP 10: Check if even regions
        if (kwargs["scalars"]["region"] == 0):
            #   STEP 11: Generate random num - If greater than 0.5 go positive
            if (rn.random() > 0.5):
                #   STEP 12: Set bRegion = True for positive
                bRegion = True

            else:
                #   STEP 13: Set bRegion = False for negative
                bRegion = False
            
        #   STEP 14: Check if positive bias
        elif (kwargs["scalars"]["region"] > 0):
            #   STEP 15: Gen random num - if less than region go positive
            if (rn.random() <= kwargs["scalars"]["region"]):
                #   STEp 16: Set bRegion = True for positive
                bRegion = True

            else:
                #   STEP 17: Set bRegion = False for negative
                bRegion = False

        #   STEP 18: Must be negative bias
        else:
            #   STEP 19: Gen random num if less than -1*region go negative
            if (rn.random() <= -1.0 * kwargs["scalars"]["region"]):
                #   STEP 20: Set bRegion = False for negative
                bRegion = False

            else:
                #   STEP 21: Set bRegion = True for pos
                bRegion = True

        #
        #   endregion

        #   STEP 22: Get offset
        fOffset = rn.random() * kwargs["scalars"]["range"] * float( kwargs["region"] / self.__iTRO_Region )

        #   STEP 23: Caluclate output
        if (bRegion):
            #   STEP 24: Add offset to center
            fOut = kwargs["center"] + fOffset

        else:
            #   STEP 25: Subtract offset from center
            fOut = kwargs["center"] - fOffset

        #   STEP 26: Return
        return round(fOut, 3)

    def __randSlots__(self, **kwargs) -> dict:
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

                + z = ( int ) The z value for the plane
                    ~ Required

                + region    = ( int ) The region for randomization
                    ~ Required
        """
        
        #   STEP 0: Local variables
        dOut                    = None

        #   STEP 1: Setup - Local variables
        
        #   region STEP 2->11: Error checking

        #   STEP 2: Check if center arg passed
        if ("center" not in kwargs):
            #   STEP 3: Error handling
            raise Exception("An error occured in Natalie.__randSlots__() -> Step 2: No center arg passed")

        #   STEP 4: check if scalars arg passed
        if ("scalars" not in kwargs):
            #   STEP 5: Error handling
            raise Exception("An error occured in Natalie.__randSLots__() -> Step 4: No scalars arg passed")
        
        #   STEP 6: Check if plane arg passed
        if ("plane" not in kwargs):
            #   STPE 7: Error handling
            raise Exception("An error occured in Natalie.__randSlots__() -> Step 6: No plane arg passed")

        #   STPE 8: Check if region arg passed
        if ("region" not in kwargs):
            #   STEP 9: Error handling
            raise Exception("An error occured in Natalie.__randSlots__() -> Step 8: No region arg passed")
        
        #   STEP 10: Check if z arg passed
        if ("z" not in kwargs):
            #   STEP 11: Error handling
            raise Exception("An error occured in Natalie.__randSlots__() -> Step 10: No z arg passed")

        #
        #   endregion
        
        #   STEP ?? : Update - Local variables
        dOut = cp.deepcopy(kwargs["center"])

        #   region STEP 12->16: Slot creation

        #   STEP 12: Check for slot creation
        if (rn.random() < kwargs["scalars"]["create slot"]["default"]["range"]):
            #   STEP 13: Get temp vars
            fTmp_X =    ( kwargs["plane"]["l"] - kwargs["plane"]["x"] ) * rn.random()
            fTmp_Y =    ( kwargs["plane"]["w"] - kwargs["plane"]["y"] ) * rn.random()

            #   STEP 14: Populate tmp dictionary
            dTmp = {
                "0":
                {
                    "x": self.__randVal__(center=fTmp_X, scalars=kwargs["scalars"]["create slot"]["x"], region=kwargs["region"]),
                    "y": self.__randVal__(center=fTmp_Y, scalars=kwargs["scalars"]["create slot"]["y"], region=kwargs["region"]),
                    "z": kwargs["z"]
                },
                "1":
                {
                    "x": self.__randVal__(center=fTmp_X, scalars=kwargs["scalars"]["create slot"]["x"], region=kwargs["region"]),
                    "y": self.__randVal__(center=fTmp_Y, scalars=kwargs["scalars"]["create slot"]["y"], region=kwargs["region"]),
                    "z": kwargs["z"]
                },
                "2":
                {
                    "x": self.__randVal__(center=fTmp_X, scalars=kwargs["scalars"]["create slot"]["x"], region=kwargs["region"]),
                    "y": self.__randVal__(center=fTmp_Y, scalars=kwargs["scalars"]["create slot"]["y"], region=kwargs["region"]),
                    "z": kwargs["z"]
                },
                "id":   Helga.ticks()
            }

            #   STEP 15: Add slot to output dictionary
            dOut[str(dOut["items"])] = dTmp

            #   STEP 16: Increment slots in dictionary
            dOut["items"] += 1

        #
        #   endregion

        #   region STEP 17->24: Slot removal

        #   STEP 17: Check for slot removal
        if (rn.random() < kwargs["scalars"]["remove slot"]["range"]):
            #   STEP 18: Check that there are slots to remove
            if (dOut["items"] > 0):
                #   STEP 19: Pick a random slot
                iTmp_Index = rn.randint(0, dOut["items"] - 1)

                #   STEP 20: Decrement slot counter
                dOut["items"] -= 1

                #   STEP 21: If slots not zero
                if (dOut["items"] > 0):
                    #   STEP 22: Loop through remaining slots
                    for i in range(iTmp_Index + 1, dOut["items"] + 1):
                        #   STEP 23: Reposition slot
                        dOut[str(i - 1)] = dOut[str(i)]

                #   STEP 24: Delete copy slot in last position
                del dOut[str(dOut["items"])]

        #
        #   endregion

        #   region STEP 25->31: Slot shifting

        #   STEP 25: Check if change
        if (rn.random() < kwargs["scalars"]["change slot"]["probability"]["range"]):
            #   STEP 26: Check if there are any slots to change
            if (dOut["items"] > 0):
                #   STEP 27: Loop through slots
                for _ in range(0, dOut["items"]):
                    #   STEP 28: Pick a random slot
                    iTmp_Index = rn.randint(0, dOut["items"] - 1)

                    #   STEP 29: Get tmp slot
                    dTmp_Slot = dOut[str(iTmp_Index)]

                    #   STEP 30: loop through slot co-ordinates
                    for i in range(0, 3):
                        #   STEP 31: Adjust coordinates
                        dTmp_Slot[str(i)]["x"] = self.__randVal__(center=dTmp_Slot[str(i)]["x"], region=kwargs["region"], scalars=kwargs["scalars"]["change slot"]["x"])
                        dTmp_Slot[str(i)]["y"] = self.__randVal__(center=dTmp_Slot[str(i)]["y"], region=kwargs["region"], scalars=kwargs["scalars"]["change slot"]["y"])

        #
        #   endregion

        #   STEP 32: Return
        return dOut
    
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

        #   STEP 0: Local variables
        dOut                    = None

        dTemplate_Candidate     = None
        dTemplate_Fitness       = None

        lInput                  = []
        lOutput                 = []

        #   STEP 1: Setup - Local variables

        #   region STEP 2->5: Error checking

        #   STEP 2: Check if canddiates arg passed
        if ("candidates" not in kwargs):
            #   STEP 3: Error handling
            raise Exception("An error occured in Natalie.__moldData__() -> Step 2: No candidates arg passed")

        #   STEP 4: Check if fitness arg passed
        if ("fitness" not in kwargs):
            #   STEP 5: Error handling
            raise Exception("An error occured in Natalie.__moldData__() -> Step 4: No fitness arg passed")

        #
        #   endregion
        
        #   STEP 6: Create template for rebuilding
        dTemplate_Candidate = cp.deepcopy(kwargs["candidates"][0])
        dTemplate_Fitness   = cp.deepcopy(kwargs["fitness"][0])

        #   STEP 7: Outsource
        lInput  = self.__dataRecursion__(data=kwargs["candidates"], template=dTemplate_Candidate, index=-0)
        lOutput = self.__dataRecursion__(data=kwargs["fitness"], template=dTemplate_Fitness, index=0)

        #   STEP 8: Set class surrogate template
        self.__dTemplate    = dTemplate_Candidate

        #   STEP 9: Populate output dictionary
        dOut    = {
            "in":   lInput,
            "out":  lOutput
        }

        #   STEP 10: Return
        return dOut

    def __dataRecursion__(self, **kwargs) -> vars:
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

                + template  = ( dict ) A template dictionary that will be
                    used to reconstruct the surrogate optimization results
                    ~ Required

                + index = ( int ) The current starting index of any new fields
                    ~ Required
        """

        #   STEP 0: Local variables
        lOut                    = []
        
        iIndex                  = None

        #   STEP 1: Setup - Local variables
        
        #   region STEP 2->7: Error checking

        #   STEP 2: Check if data arg passed
        if ("data" not in kwargs):
            #   STEP 3: Error handling
            raise Exception("An error occured in Natalie.__dataRecursion__() -> Step 2: No data arg passed")

        #   STEP 4: Check fi template arg passed
        if ("template" not in kwargs):
            #   STEP 5: Error handling
            raise Exception("An error occured in Natalie.__dataRecursion__() -> Step 4: No tepmlate arg passed")
        
        #   STEP 6: Check if index arg passed
        if ("index" not in kwargs):
            #   STEP 7: Error handling
            raise Exception("An error occured in Natalie.__dataRecursion__() -> Step 6: No index arg passed")

        #
        #   endregion
        
        #   STEP 8: Check if "items" entry in template
        if ("items" not in kwargs["template"]):
            #   STEP 9: Return empty
            return None

        #   STEP 10: Update - Local variables
        iIndex  = kwargs["index"]

        #   STEP 11: Iterate through items list
        for i in range(0, kwargs["template"]["items"]):
            #   STEP 12: Setup - Scope variables
            lTmp_Child_In   = []
            lTmp_Child_Out  = None

            sTmp_Child  = kwargs["template"][str(i)]

            #   STEP 13: Loop through candidates
            for j in range(0, len(kwargs["data"])):
                #   STEP 14: Append child dictionary from all candidates to temp list for recursion
                lTmp_Child_In.append(kwargs["data"][j][sTmp_Child])

            #   STEP 15: Be safe OwO - Shortcut
            try:
                #   STEP 16: Check if slots
                if (sTmp_Child == "slots"):
                    #   STEP 17: Outsource
                    lTmp_Child_Out = self.__dataRecursion_Slots__(data=lTmp_Child_In, template=kwargs["template"][sTmp_Child], index= iIndex)

                #   STEP 18: Check if child has children
                elif ("items" in kwargs["template"][sTmp_Child]):
                    #   STEP 19: Outsource
                    lTmp_Child_Out  = self.__dataRecursion__(data=lTmp_Child_In, template=kwargs["template"][sTmp_Child], index=iIndex)

            #   STEP 20: Normal output
            except:
                #   STEP 21: Set output equal to temp input
                lTmp_Child_Out = [lTmp_Child_In]

                #   STEP 22: Update Template dictionary
                kwargs["template"][sTmp_Child] = "remap-" + str(iIndex)
            
            #   STEP 23: Check child output status
            if (lTmp_Child_Out != None):
                #   STEP 24: Update - Output variables
                lOut.extend(lTmp_Child_Out)

                #   STEP 25: Increment index
                iIndex += len(lTmp_Child_Out)

        #   STEP 26: Return
        return lOut

    def __dataRecursion_Slots__(self, **kwargs) -> vars:
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

                + template  = ( dict ) A template dictionary that will be used
                    to reconstruct the surrogate optimized results
                    ~ Required

                + index = ( int ) The current starting index of any new fields
                    ~ Required
        """

        #   STEP 0: Local variables
        lOut                    = []

        lSlots_Template         = []
        lSlots_Unique           = []
        lSlots_Unique_Count     = []
        lSlots_Common           = []

        fZ                      = None

        iStep                   = 0

        #   STEP 1: Setup - Local variables

        #   region STEP 2->7: Error checking

        #   STEP 2: Check if data arg passed
        if ("data" not in kwargs):
            #   STEP 3: Error handling
            raise Exception("An error occured in Natalie.__dataRecursion_Slots__() -> Step 2: No data arg passed")
        
        #   STEP 4: Check fi template arg passed
        if ("template" not in kwargs):
            #   STEP 5: Error handling
            raise Exception("An error occured in Natalie.__dataRecursion_Slots__() -> Step 4: No template arg passed")
        
        #   STEP 6: Check if index arg passed
        if ("index" not in kwargs):
            #   STEP 7: error handling
            raise Exception("An error occured in Natalie.__dataRecursion_Slots__() -> Step 6: No index arg passed")

        #
        #   endregion

        try:
            #   STEP 8: Loop through all candidates
            iStep += 1
            for i in range(0, len(kwargs["data"])):
                #   STEP 9: Get temp candidate dictionary
                dTmp_Candidate = kwargs["data"][i]

                #   STEP 10: Loop through slots in candidate
                for j in range(0, dTmp_Candidate["items"]):
                    #   STEP 11: Check if slot not in unique slots list
                    if (dTmp_Candidate[str(j)]["id"] not in lSlots_Unique):
                        #   STEP 12: Append to list
                        lSlots_Unique.append(dTmp_Candidate[str(j)]["id"])
                        lSlots_Unique_Count.append(1)

                    #   STEP 13: Not unique
                    else:
                        #   STEP 14: Get index in unique list
                        iTmp_Index = lSlots_Unique.index(dTmp_Candidate[str(j)]["id"])

                        #   STEP 15: Increment counter
                        lSlots_Unique_Count[iTmp_Index] += 1

                    #   STEP 16: Check if Z-axis has been set
                    if (fZ == None):
                        #   STEP 17: Update - Local variables
                        fZ = dTmp_Candidate[str(j)]["0"]["z"]

            iStep += 1
            if (len(lSlots_Unique_Count) == 0):
                return

            #   STEP 18: Loop through unique slots
            iStep += 1
            for i in range(0, len(lSlots_Unique_Count)):
                #   STEP 19: Check if not unique
                if (lSlots_Unique_Count[i] > 1):
                    #   STEP 20: Append to common list
                    lSlots_Common.append(lSlots_Unique_Count[i])
                    
            #   STEP 21: Iterate through unique slots
            iStep += 1
            for _ in range(0, len( lSlots_Common ) + 1 ):
                #   STEP 22: Add 6 fields for each unique slot to output
                for _ in range(0, 6):
                    #   STEP 23: Append field to output
                    lOut.append([])

                #   STEP 24: Append field to template
                lSlots_Template.append([])
                
            #   STEP 25: Loop through all candidates
            iStep += 1
            for i in range(0, len(kwargs["data"])):
                #   STEP 26: Setup - Temp vars
                dTmp_Candidate  = kwargs["data"][i]

                lTmp_Slots_Data = cp.deepcopy(lSlots_Template)

                #   STEP 27: Loop through slots in this candidate
                for j in range(0, dTmp_Candidate["items"]):
                    iStep += 1
                    #   STEP 28: Check if common
                    if (dTmp_Candidate[str(j)]["id"] in lSlots_Common):
                        #   STEP 29: Get index
                        iTmp_Index  = lSlots_Common.index(dTmp_Candidate[str(j)]["id"])

                    #   STEP 32: Unique slot
                    else:
                        #   STEP 33: Set index to end of list
                        iTmp_Index  = len(lSlots_Template) - 1

                    #   STEP 34: Populate candidate slot dictionary
                    lTmp = []
                    lTmp.append(dTmp_Candidate[str(j)]["0"]["x"])
                    lTmp.append(dTmp_Candidate[str(j)]["0"]["y"])
                    lTmp.append(dTmp_Candidate[str(j)]["1"]["x"])
                    lTmp.append(dTmp_Candidate[str(j)]["1"]["y"])
                    lTmp.append(dTmp_Candidate[str(j)]["2"]["x"])
                    lTmp.append(dTmp_Candidate[str(j)]["2"]["y"])

                    #   STEP 35: Append to output
                    lTmp_Slots_Data[iTmp_Index] = lTmp

                #   STEP 36: Loop through candidate
                for j in range(0, len(lTmp_Slots_Data)):
                    #   STEP 37: Check if empty
                    if (len(lTmp_Slots_Data[j]) <= i):
                        #   STEP 38: Append empty
                        lTmp_Slots_Data[j] = [None, None, None, None, None, None]

                #   STEP 39: Translate candidate data to output data
                for j in range(0, len(lTmp_Slots_Data)):
                    #   STEP 40:  Append data to output list
                    lOut[ j * 6 + 0 ].append(lTmp_Slots_Data[j][0])
                    lOut[ j * 6 + 1 ].append(lTmp_Slots_Data[j][1])
                    lOut[ j * 6 + 2 ].append(lTmp_Slots_Data[j][2])
                    lOut[ j * 6 + 3 ].append(lTmp_Slots_Data[j][3])
                    lOut[ j * 6 + 4 ].append(lTmp_Slots_Data[j][4])
                    lOut[ j * 6 + 5 ].append(lTmp_Slots_Data[j][5])

            iStep += 1
            #   STEP 31: Loop through template slots
            for i in range(0, kwargs["template"]["items"]):
                #   STEP 34: Update - Template
                kwargs["template"][str(i)]["0"]["x"] = "remap-" + str(kwargs["index"] + i * 6 + 0)
                kwargs["template"][str(i)]["0"]["y"] = "remap-" + str(kwargs["index"] + i * 6 + 1)
                kwargs["template"][str(i)]["1"]["x"] = "remap-" + str(kwargs["index"] + i * 6 + 2)
                kwargs["template"][str(i)]["1"]["y"] = "remap-" + str(kwargs["index"] + i * 6 + 3)
                kwargs["template"][str(i)]["2"]["x"] = "remap-" + str(kwargs["index"] + i * 6 + 4)
                kwargs["template"][str(i)]["2"]["y"] = "remap-" + str(kwargs["index"] + i * 6 + 5)

            iStep += 1
            while (kwargs["template"]["items"] < len(lTmp_Slots_Data)):
                #   STEP 36: Create temp dict
                dTmp = {
                    "0":
                    {
                        "x": "remap-" + str(kwargs["index"] + kwargs["template"]["items"] * 6 + 0),
                        "y": "remap-" + str(kwargs["index"] + kwargs["template"]["items"] * 6 + 1),
                        "z": fZ
                    },
                    "1":
                    {
                        "x": "remap-" + str(kwargs["index"] + kwargs["template"]["items"] * 6 + 2),
                        "y": "remap-" + str(kwargs["index"] + kwargs["template"]["items"] * 6 + 3),
                        "z": fZ
                    },
                    "2":
                    {
                        "x": "remap-" + str(kwargs["index"] + kwargs["template"]["items"] * 6 + 4),
                        "y": "remap-" + str(kwargs["index"] + kwargs["template"]["items"] * 6 + 5),
                        "z": fZ
                    },
                    "id": Helga.ticks()
                }

                #   STEP 37: Add to template dictionary
                kwargs["template"][str(kwargs["template"]["items"])] = dTmp
                kwargs["template"]["items"] += 1

        except Exception as ex:
            print("Initial error: ", ex)
            Helga.nop()
            Helga.nop()
            Helga.nop()

        #   STEP 38: Return
        return lOut

    #
    #       endregion

    #       region Back-End-(Data Management): Remapping

    def __remapData__(self, **kwargs) -> dict:
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

                + candidate = ( list ) A list of the parameters for the antenna
                    geometry
                    ~ Required
        """

        #   STEP 0: Local variables
        dCandidate_New          = None

        #   STEP 1: Setup - Local variables

        #   region STEP 2->5: Error checking

        #   STEP 2: Check if candidate arg passed
        if ("candidate" not in kwargs):
            #   STEP 3: Error handling
            raise Exception("An error occured in Natalie.__remapData__() -> Step 2: No candidate arg passed")

        #   STEP 4: Check if template exists
        if (self.__dTemplate == None):
            #   STEP 5: Error handling
            raise Exception("An error occured in Natalie.__remapData__() -> Step 4: No template exists for remapping")
        
        #
        #   endregion
        
        #   STEP 6: Setup - Local variables
        dCandidate_New  = cp.deepcopy(self.__dTemplate)

        #   STEP 7: Outsource
        self.__remapData_Recursion__(template=self.__dTemplate, data=kwargs["candidate"], candidate=dCandidate_New)

        #   STEP 8: Remap substrate
        self.__remapData_Substrate__(candidate=dCandidate_New)

        #   STEP 9: Return
        return dCandidate_New

    def __remapData_Recursion__(self, **kwargs) -> None:
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

                + candidate = ( dict ) The new antenna geometry
                    ~ Required
        """

        #   STEP 0: Local variables

        #   STEP 1: Setup - Local variables

        #   region STEP 2->7: Error checking

        #   STEP 2: Check if template arg passed
        if ("template" not in kwargs):
            #   STEP 3: Error handling
            raise Exception("An error occured in Natalie.__remapData_Recursion__() -> Step 2: No template arg passed")

        #   STEP 4: Check if data arg passed
        if ("data" not in kwargs):
            #   STEP 5: Error handling
            raise Exception("An error occured in Natalie.__remapData_Recursion__() -> Step 4: No data arg passed")

        #   STEP 6: Check if candidate arg passed
        if ("candidate" not in kwargs):
            #   STEP 7: Error handling
            raise Exception("An error occured in Natalie.__remapData_Recursion__() -> Step 6: No candidate arg passed")

        #
        #   endregion

        #   STEP 8: Loop through items list
        for i in range(0, kwargs["template"]["items"]):
            #   STEP 9: Setup - Scope variables
            sTmp_Child  = kwargs["template"][str(i)]

            #   STEP 10: Be safe OwO
            try:
                #   STEP 11: Check if slots
                if (sTmp_Child  == "slots"):
                    #   STEP 12: Outsource
                    self.__remapData_Slots__(template=kwargs["template"][sTmp_Child], candidate=kwargs["candidate"][sTmp_Child], data=kwargs["data"])

                #   STEP 13: Not slot
                elif ("items" in kwargs["template"][sTmp_Child]):
                    #   STEP 14: Recurse this bitch
                    self.__remapData_Recursion__(template=kwargs["template"][sTmp_Child], candidate=kwargs["candidate"][sTmp_Child], data=kwargs["data"])

                #   STEP 15: Not child field
                else:
                    #   STEP 16: Get index
                    sTmp_Index  = kwargs["template"][sTmp_Child].strip("remap-")
                    iTmp_Index  = int(sTmp_Index)

                    #   STEP 17: Remap field
                    kwargs["candidate"][sTmp_Child] = kwargs["data"][iTmp_Index]
            
            #   STEP 18: Shortcut to nowhere
            except:
                #   STEP 19: Welcome to nowhere
                Helga.nop()

        #   STEP 18: Return
        return

    def __remapData_Slots__(self, **kwargs) -> None:
        """
            Description:

                Remaps the slots of the template antenna geometry using the
                provided arguments.

            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:

                + candidate = ( dict ) The new antenna geometry to which the
                    input data should be mapped
                    ~ Required

                + template  = ( dict ) The antenna geometry template to use
                    during the remapping process
                    ~ Required

                + data  = ( list ) The new parameters for the antenna geometry
                    to be used during the remapping process
                    ~ Required
        """

        #   STEP 0: Local variables

        #   STEP 1: Setup - Local variables

        #   region STEP 2->7: Error checking

        #   STEP 2: Check if candidate arg passed
        if ("candidate" not in kwargs):
            #   STPE 3: Error handling
            raise Exception("An error occured in Natalie.__remapData_Slots__() -> Step 2: No candidate arg passed")

        #   STEP 4: Check if template arg passed
        if ("template" not in kwargs):
            #   STEP 5: Error handling
            raise Exception("An error occured in Natalie.__remapData_Slots__() -> Step 4: No template arg passed")

        #   STEP 6: Check if data arg passed
        if ("data" not in kwargs):
            #   STEP 7: Error handling
            raise Exception("An error occured in Natalie.__remapData_Slots__() -> Step 6: No data arg passed")

        #
        #   endregion

        #   STEP 8: Iterate through items in template
        for i in range(0, kwargs["template"]["items"]):
            #   STEP 9: 0-x
            sTmp_Index  = kwargs["template"][str(i)]["0"]["x"].strip("remap-")
            iTmp_Index  = int(sTmp_Index)

            kwargs["candidate"][str(i)]["0"]["x"]   = kwargs["data"][iTmp_Index]

            #   STEP 10: 0-y
            sTmp_Index  = kwargs["template"][str(i)]["0"]["y"].strip("remap-")
            iTmp_Index  = int(sTmp_Index)

            kwargs["candidate"][str(i)]["0"]["y"]   = kwargs["data"][iTmp_Index]

            #   STEP 11: 1-x
            sTmp_Index  = kwargs["template"][str(i)]["1"]["x"].strip("remap-")
            iTmp_Index  = int(sTmp_Index)

            kwargs["candidate"][str(i)]["1"]["x"]   = kwargs["data"][iTmp_Index]

            #   STEP 12: 1-y
            sTmp_Index  = kwargs["template"][str(i)]["1"]["y"].strip("remap-")
            iTmp_Index  = int(sTmp_Index)

            kwargs["candidate"][str(i)]["1"]["y"]   = kwargs["data"][iTmp_Index]

            #   STEP 13: 2-x
            sTmp_Index  = kwargs["template"][str(i)]["2"]["x"].strip("remap-")
            iTmp_Index  = int(sTmp_Index)

            kwargs["candidate"][str(i)]["2"]["x"]   = kwargs["data"][iTmp_Index]

            #   STEP 13: 2-y
            sTmp_Index  = kwargs["template"][str(i)]["2"]["y"].strip("remap-")
            iTmp_Index  = int(sTmp_Index)

            kwargs["candidate"][str(i)]["2"]["y"]   = kwargs["data"][iTmp_Index]
            
        #   STEP 14: Return
        return

    def __remapData_Substrate__(self, **kwargs) -> None:
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
        return
    
    #
    #       endregion

    #
    #   endregion

    #   region Back-End: Optimization

    def __tro__(self, **kwargs) -> dict:
        """
            Description:

                Performs trust-region optimization of the candidate solution.

            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:

                + stage = ( str ) The current stage of the optimization process
                    ~ Required

                    ~ Options:
                        - "Primary"
                        - "Secondary"

                + center    = ( dict ) The candidate solution to be optimized
                    ~ Required if <stage="Secondary">

                + new   = ( bool ) Whether or not a new center microstrip patch
                    antenna should be simulated at the start of the project
                    ~ Required

                + cull  = ( bool ) A flag that specifies whether of not
                    unworthy antenna candidate simulations should be deleted
                    from the local drive
                    ~ Required

                + save  = ( bool ) A flag that specifies whether or not
                    continuous saving of the best candidate in an algorithm
                    should be done
                    ~ Required

                + surrogate = ( bool ) A flag that specifies whether or not a
                    surrogate model should be used during the optimization 
                    process
                    ~ Required

                + retension = ( bool ) A flag that specifies whether or not
                    some data from previous iterations should be saved instead
                    of discarded
                    ~ Default = True
        """

        #   STEP 0: Local variables
        dBest_Geo               = None
        dBest_Fit               = None

        sDir                    = None

        iRegion_Alg             = None
        iRegion_Srg             = None

        bCull                   = None
        bSave                   = None
        bSurrogate              = None
        bRetension              = True

        #   STEP 1: Setup - Local variables

        #   region STEP 2->11: Error checking

        #   STEP 2: Check if stage arg passed
        if ("stage" not in kwargs):
            #   STEP 3: Error handling
            raise Exception("An error occured in Natalie.__tro__() -> Step 2: No stage arg passed")

        #   STEP 4: Check if new arg passed
        if ("new" not in kwargs):
            #   STEP 5: Error handling
            raise Exception("An error occured in Natalie.__tro__() -> Step 4: No new arg passed")

        #   STEP 6: Check if cull arg passed
        if ("cull" not in kwargs):
            #   STEP 7: Error handling
            raise Exception("An error occured in Natalie.__tro__() -> Step 6: No cull arg passed")

        #   STEP 8: Check if save arg passed
        if ("save" not in kwargs):
            #   STEP 9: Error handling
            raise Exception("An error occured in Natalie.__tro__() -> Step 8: No save arg passed")

        #   STEP 10: Check if surrogate arg passed
        if ("surrogate" not in kwargs):
            #   STEP 11: Error handling
            raise Exception("An error occured in Natalie.__tro__() -> Step 10: No surrogate arg passed")

        #
        #   endregion

        #   region STEP 12->20: Setup - Local variables

        #   STEP 12: Setup - Local variables
        sDir            = self.__sDirectory + "\\" + Helga.ticks() + "_" + kwargs["stage"]

        iRegion_Alg     = cp.deepcopy(self.__iTRO_Region)
        iRegion_SRG     = cp.deepcopy(self.__iTRO_Region_SRG)

        bCull           = kwargs["cull"]
        bSave           = kwargs["save"]
        bSurrogate      = kwargs["surrogate"]

        #   STEP 13: Check if stage is primary
        if (kwargs["stage"] == "Primary"):
            #   STEP 14: Check if new center or if center is None
            if ((kwargs["new"]) or (self.__dAnt_Center == None)):
                #   STEP 15: User output
                if (self.bShowOutput):
                    print("Natalie (tro-" + kwargs["stage"] + ") {" + Helga.time() + "} - Simulating starting antenna geometry")

                #   STEP 16: Outsource
                self.__dAnt_Center  = Matthew.getPatch_Default(name="center", dir=self.__sDirectory, substrate=self.__dAnt_Substrate, frequency=self.__dAnt_Frequency, mesh=self.__dAnt_Mesh, runt=self.__dAnt_Runt, fitness=self.__dAnt_Fitness)
        
        #   STEP 17: Setup - Local variables
        dBest_Geo       = cp.deepcopy(self.__dAnt_Center)
        dBest_Fit       = {
            "fitness":  dBest_Geo["fitness"],
            "dir":      dBest_Geo["dir"]
        }

        dBest_Fit       = self.__getFitness__( ant=[dBest_Geo], fitness=[dBest_Fit] )[0]

        #   STEP 18: Check if retension arg passed
        if ("retension" in kwargs):
            #   STEP 19: Update - Local variables
            bRetension  = kwargs["retension"]

        #   STEP 20: Setup - Final steps
        del dBest_Geo["dir"]
        del dBest_Geo["fitness"]

        os.mkdir(sDir)

        #
        #   endregion
        
        #   STEP 21: User output
        if (self.bShowOutput):
            print("Natalie (tro-" + kwargs["stage"] + ") {" + Helga.time() + "} - Begining Trust-Region Optimization.")

        #   STEP 22->??: TRO - Loop through iterations
        for i in range(0, self.__iTRO_Iterations):
            #   STEP 23: Setup - Scope variables
            lCandidates         = []
            lFitness            = []

            fTmp_Fitness        = np.inf

            iTmp_Candidates     = self.__iTRO_Candidates
            iTmp_Index          = 0
            iTmp_Count          = 0

            bTmp_Region         = False

            #   region STEP 24->42: Candidate generations and simulation

            #   STEP 24: Loop till amount of candidates reached
            while (True):
                #   STEP 25: Setup - Temp variables
                lTmp_Candidates = []
                
                #   STEP 26: Check if stage is Primary
                if (kwargs["stage"] == "Primary"):
                    #   STEP 27: Outsoruce - Get candidates
                    lTmp_Candidates = self.__getCandidates__(center=dBest_Geo, region=iRegion_Srg, candidates=iTmp_Candidates, slots=True)

                #   STEP 28: Stage is secondary
                else:
                    #   STEP 29: Outsource - Get candidates
                    lTmp_Candidates = self.__getCandidates__(center=dBest_Geo, region=iRegion_Srg, candidates=iTmp_Candidates, slots=False)

                #   STEP 30: User output
                if (self.bShowOutput):
                    print("\n\t{" + Helga.time() + "} - Simulating " + str(iTmp_Candidates) + " candidate antennas.\n")

                #   STEP 31: Simulate antennas
                lTmp_Fitness    = Matthew.simulateCandidates_Json(dir=sDir, ant=lTmp_Candidates, frequency=self.__dAnt_Frequency, mesh=self.__dAnt_Mesh, runt=self.__dAnt_Runt, fitness=self.__dAnt_Fitness)

                #   STEP 32: Evaluate overall fitness of all geometries
                lTmp_Fitness    = self.__getFitness__(ant=lTmp_Candidates, fitness=lTmp_Fitness)

                #   STEP 33: Loop through all candidates
                while (iTmp_Count < len( lTmp_Candidates )):
                    #   STEP 34: Check that default fitness library wasn't returned
                    if ( lTmp_Fitness[iTmp_Count]["desired"] == np.inf):
                        #   STEP 35: Pop from list
                        lTmp_Candidates.pop(iTmp_Count)
                        lTmp_Fitness.pop(iTmp_Count)

                    #   STEP 36: Not default library
                    else:
                        #   STEP 37: Increment counter
                        iTmp_Count  += 1

                #   STEP 38: Append results and fitnesses to lists
                lCandidates.extend(lTmp_Candidates)
                lFitness.extend(lTmp_Fitness)

                #   STEP 39: Check that required number of candidates met
                if (len( lCandidates ) == self.__iTRO_Candidates):
                    #   STEP 40: Exit loop
                    break

                #   STEP 41: Recalculate candidates
                iTmp_Candidates = self.__iTRO_Candidates - len( lCandidates )

            #   STEP 42: Append current best to lists
            lCandidates.append(dBest_Geo)
            lFitness.append(dBest_Fit)

            #
            #   endregion
            
            #   region STEP 43->58: Surrogate stuff

            #   STEP 43: Check surrogate status
            if (bSurrogate):
                
                #   region STEP 44->52: Setup - Data container

                #   STEP 44: Setup - Scope variables
                dTmp_Data           = self.__moldData__(candidates=lTmp_Candidates, fitness=lFitness)
                dTmp_DataRange      = None
                dTmp_DataMap        = None
                dTmp_DataMin        = None

                lTmp_DataMap_In     = []
                lTmp_DataMap_Out    = []

                #   STEP 45: Setup - Final data ranges
                dTmp_DataRange      = {
                    "lower":        -1.0,
                    "center":       0.0,
                    "upper":        1.0
                }

                #   STEP 46: Setup - Data maps
                for j in range(0, len( dTmp_Data["in"] ) ):
                    lTmp_DataMap_In.append(i)

                for j in range(0, len( dTmp_Data["out"] ) ):
                    lTmp_DataMap_Out.append(i)

                #   STEP 47: Setup - Create new Data container
                vData   = Data()
                vData.setData(data=dTmp_Data, automap=False, transpose=True)

                #   STEP 48: Get data minimums
                fTmp_OutMin_0   = vData.getOutputMin(0)
                fTmp_OutMin_1   = vData.getOutputMin(1)

                #   STEP 49: Setup - Data minimum dict
                dTmp_DataMin    = {
                    "output":
                    {
                        "0":    [fTmp_OutMin_0 - 0.075],
                        "1":    [fTmp_OutMin_1 - 0.075]
                    },
                    "input":
                    {

                    }
                }

                #   STEP 50: User output
                if (self.bShowOutput):
                    print("\t\t- Data Distance (pre-mapping) : ", vData.getInputDistance(0), end="\n\n")

                #   STEP 51: Map data
                vData.mapData(mapRange=dTmp_DataRange, mapSets=dTmp_DataMap, input=True, output=True, min=dTmp_DataMin)

                #   STEP 52: User output
                if (self.bShowOutput):
                    print("\t\t- Data Distance (post-mapping) : ", vData.getInputDistance(0), end="\n\n")

                #
                #   endregion

                #   region STEP 53->58: Surrogate creation, training, mapping, simulation, and fitness evaluation

                #   STEP 53: Setup - Create new surrogate handler
                vGolem = Golem(numSurrogates=8)

                #   STEP 54: Update - surrogate handler parameters
                vGolem.bSRG_Random              = True
                vGolem.bSRG_RandomParameters    = False

                #   STEP 55: Train and map the surrogates
                lTmp_SrgResults = vGolem.trainAndMap(data=vData, region=float( iRegion_Srg ) / self.__iTRO_Region_SRG, rand=True, remap=True)
                
                #   STEP 54: Remap - Surrogate candidate
                dTmp_SrgResults = self.__remapData__(candidate=lTmp_SrgResults["result"])

                #   STEP 55: User output
                if (self.bShowOutput):
                    print("\n\t{" + Helga.time() + "} - Simulating surrogate candidate.")

                #   STEP 56: Simulate - Surrogate candidate
                lTmp_SrgFitness = Matthew.simulateCandidates_Json(dir=sDir, ant=[dTmp_SrgResults], frequency=self.__dAnt_Frequency, mesh=self.__dAnt_Mesh, runt=self.__dAnt_Runt, fitness=self.__dAnt_Fitness)

                #   STEP 57: Evaluate   - Surrogate candidate fitness
                lTmp_SrgFitness    = self.__getFitness__(ant=[dTmp_SrgResults], fitness=lTmp_SrgFitness)
            
                #   STEP 58: Append - Surrogate candidate
                lCandidates.append(dTmp_SrgResults)
                lFitness.append(lTmp_SrgFitness[0])

                #
                #   endregion

            #
            #   endregion

            #   region STEP 59->62: Candidate evaluation

            #   STEP 59: Loop through candidates
            for i in range(0, len( lFitness )):
                #   STEP 60: Check if less than current best fitness
                if (lFitness[i]["final"] < fTmp_Fitness):
                    #   STEP 61: Update tmp vars
                    iTmp_Index      = i
                    fTmp_Fitness    = lFitness[i]["final"]

            #   STEP 62: Set new best candidate
            dBest_Geo = lCandidates[iTmp_Index]
            dBest_Fit = lFitness[iTmp_Index]
            
            #
            #   endregion

            #   region STEP 63->89: Region update

            #   STEP 63: Check surrogate status
            if (bSurrogate):
                #   STEP 64: Check if best is surrogate candidates
                if (iTmp_Index == len(lTmp_Candidates) - 1):
                    #   STEP 65: Update region
                    iRegion_Alg         += 1
                    iRegion_SRG         += 1

                    #   STEP 66: User output
                    if (self.bShowOutput):
                        print("\n\t{" + Helga.time() + "} - Iteration (" + str(j) + ") : Increasing region via surrogate -> " + str(iRegion_Alg))

                        dHold = lFitness[self.__iTRO_Candidates]
                        print("\t\t-Initial:",  "area=" + str(round(dHold["area"] * 100.0, 3)), "freq=" + str(round(dHold["freq"] * 100.0, 3)), "final=" + str(round(dHold["final"] * 10.0, 3)), sep="\t")
                        
                        dHold = lFitness[iTmp_Index]
                        print("\t\t-New:\t",    "area=" + str(round(dHold["area"] * 100.0, 3)), "freq=" + str(round(dHold["freq"] * 100.0, 3)), "final=" + str(round(dHold["final"] * 100.0, 3)), sep="\t")
                        print("")

                #   STEP 67: Check if new best isn't old best
                elif (iTmp_Index != self.__iTRO_Candidates):
                    #   STEP 68: Update region
                    iRegion_Alg     += 1

                    #   STEP 69: Check if surrogate region not too small
                    if (iRegion_SRG > 0):
                        #   STEP 70: Update surrogate region
                        iRegion_SRG     -= 1

                    #   STEP 71: User output
                    if (self.bShowOutput):
                        print("\n\t{" + Helga.time() + "} - Iteration (" + str(j) + ") : Increasing region -> " + str(iRegion_Alg))

                        dHold = lFitness[self.__iTRO_Candidates]
                        print("\t\t-Initial:",  "area=" + str(round(dHold["area"] * 100.0, 3)), "freq=" + str(round(dHold["freq"] * 100.0, 3)), "final=" + str(round(dHold["final"] * 10.0, 3)), sep="\t")
                        
                        dHold = lFitness[iTmp_Index]
                        print("\t\t-New:\t",    "area=" + str(round(dHold["area"] * 100.0, 3)), "freq=" + str(round(dHold["freq"] * 100.0, 3)), "final=" + str(round(dHold["final"] * 100.0, 3)), sep="\t")
                        
                        dHold = lFitness[len(lTmp_Candidates) - 1]
                        print("\t\t-SRG:\t",    "area=" + str(round(dHold["area"] * 100.0, 3)), "freq=" + str(round(dHold["freq"] * 100.0, 3)), "final=" + str(round(dHold["final"] * 100.0, 3)), sep="\t")
                        print("")

                #   STEP 72: Bad region
                else:
                    #   STEP 73: Check if alg region not too small
                    if (iRegion_Alg > 0):
                        #   STEP 74: Update region
                        iRegion_Alg     += 1

                        #   STEP 75: Check if surrogate region not too small
                        if (iRegion_SRG > 0):
                            #   STEP 76: Update surrogate region
                            iRegion_SRG     -= 1

                        #   STEP 77: User output
                        if (self.bShowOutput):
                            print("\n\t{" + Helga.time() + "} - Iteration (" + str(j) + ") : Decreasing region -> " + str(iRegion_Alg))

                            dHold = lFitness[self.__iTRO_Candidates]
                            print("\t\t-Initial:",  "area=" + str(round(dHold["area"] * 100.0, 3)), "freq=" + str(round(dHold["freq"] * 100.0, 3)), "final=" + str(round(dHold["final"] * 10.0, 3)), sep="\t")
                            
                            dHold = lFitness[iTmp_Index]
                            print("\t\t-New:\t",    "area=" + str(round(dHold["area"] * 100.0, 3)), "freq=" + str(round(dHold["freq"] * 100.0, 3)), "final=" + str(round(dHold["final"] * 100.0, 3)), sep="\t")
                            
                            dHold = lFitness[len(lTmp_Candidates) - 1]
                            print("\t\t-SRG:\t",    "area=" + str(round(dHold["area"] * 100.0, 3)), "freq=" + str(round(dHold["freq"] * 100.0, 3)), "final=" + str(round(dHold["final"] * 100.0, 3)), sep="\t")
                            print("")

                    #   STEP 78: Region too small
                    else:
                        #   STEP 79: Exit loop
                        break

            #   STEP 80: No surrogate
            else:
                #   STEP 81: Check if new best
                if (iTmp_Index != self.__iTRO_Candidates):
                    #   STEP 82: Update region
                    iRegion_Alg += 1

                    #   STEP 83: User output
                    if (self.bShowOutput):
                        print("\n\t{" + Helga.time() + "} - Iteration (" + str(j) + ") : Increasing region -> " + str(iRegion_Alg))

                        dHold = lFitness[self.__iTRO_Candidates]
                        print("\t\t-Initial:",  "area=" + str(round(dHold["area"] * 100.0, 3)), "freq=" + str(round(dHold["freq"] * 100.0, 3)), "final=" + str(round(dHold["final"] * 100.0, 3)), sep="\t")
                        
                        dHold = lFitness[iTmp_Index]
                        print("\t\t-New:\t",    "area=" + str(round(dHold["area"] * 100.0, 3)), "freq=" + str(round(dHold["freq"] * 100.0, 3)), "final=" + str(round(dHold["final"] * 100.0, 3)), sep="\t", end="\n\n")

                #   STEP 84: Not new best
                else:
                    #   STEP 85: Check if region too small
                    if (iRegion_Alg > 0):
                        #   STEP 86: Update - Decrement region
                        iRegion_Alg     -= 1

                        #   STEP 87: User output
                        if (self.bShowOutput):
                            print("\n\t{" + Helga.time() + "} - Iteration (" + str(j) + ") : Decreasing region -> " + str(iRegion_Alg), end="\n\n")
                    
                    #   STPE 88: Region too small
                    else:
                        #   STEP 89: Exit loop
                        break

            #
            #   endregion

            #   region STEP 90->96: Continuous save

            #   STEP 90: Check for continuous save
            if (bSave):
                #   STEP 91: Setup - File location
                sTmp_File = sDir + "\\" + str(j) + ".json"

                #   STEP 92: Create file
                vTmp_File   = open(sTmp_File, "a")

                #   STEP 93: Close file
                vTmp_File.close()
                vTmp_File = None

                #   STEP 94: Re-open file
                with open(sTmp_File, "r+") as vTmp_File:
                    #   STEP 95: Create temp dictionary
                    dTmp = {
                        "geometry": dBest_Geo,
                        "fitness":  dBest_Fit,
                        "antenna":  self.__cAnt_Default,
                        "natalie":  self.__cf.data
                    }

                    #   STEP 96: Dump data
                    js.dump(dTmp, vTmp_File, indent=4, separators=(", ", " : "))

            #
            #   endregion
        
            #   region STEP 97->102: Cull the unworthy :)

            #   STEP 97: Check culling status
            if (bCull):
                #   STEP 98: Loop through candidates
                for i in range(0, len( lFitness ) ):
                    #   STEP 99: If not current best and not previous best
                    if ((i != iTmp_Index) and (i != self.__iTRO_Candidates)):
                        #   STEP 100: Get path for directory
                        sTmp_Path = os.path.dirname(lTmp_Fitness[i]["dir"])

                        #   STEP 101: If not center
                        if ("center" not in sTmp_Path):
                            #   STEP 102: Delete directory
                            sh.rmtree(sTmp_Path)

            #
            #   endregion

        #   STEP 103: Return
        return dBest_Geo

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
        nat.optimizeAntenna(primary="nm", secondary="tro", surrogate=True)

#
#endregion