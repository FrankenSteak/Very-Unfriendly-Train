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

        self.__cAnt_Default     = None

        #   endregion

        #   region  STEP 1.2: TRO Params

        self.__iTRO_Iterations_Primary      = None
        self.__iTRO_Iterations_Secondary    = None
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

        """

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

        """

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

        self.__iTRO_Iterations_Primary      = self.__cf.data["parameters"]["trust region"]["primary iterations"]
        self.__iTRO_Iterations_Secondary    = self.__cf.data["parameters"]["trust region"]["secondary iterations"]
        self.__iTRO_Candidates              = self.__cf.data["parameters"]["trust region"]["candidates"]
        self.__iTRO_Region                  = self.__cf.data["parameters"]["trust region"]["algorithm region"]
        self.__iTRO_Region_SRG              = self.__cf.data["parameters"]["trust region"]["surrogate region"]
        self.__iTRO_Retension_FallOff       = self.__cf.data["parameters"]["trust region"]["retension fall off"]

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
                "start":    round(kwargs["ant"]["frequency"]["start"] + ( self.__cf.data["parameters"]["frequency"]["lower frequency offset"] ), 2),
                "end":      round(kwargs["ant"]["frequency"]["end"] - ( self.__cf.data["parameters"]["frequency"]["upper frequency offset"] ), 2),
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

        #   STEP 13: Return
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
            fTmp_Left   = ( dTmp_Fit["lower"]["total"] ) * 0.5

            #   STEP 11: Get center firness
            fTmp_Mid    = ( dTmp_Fit["desired"]["total"] ) * 0.7

            #   STEP 12: Get right fitness
            fTmp_Right  = ( dTmp_Fit["upper"]["total"] ) * 0.3

            #   STEP 13: Get total area fitness
            fTmp_Area   = fTmp_Area / fOriginal_Area

            #   STEP 14: Get total frequency fitness
            fTmp_Freq_Tot   = fTmp_Left + fTmp_Mid + fTmp_Right
            
            #   STEP 15: Get overall fitness
            fTmp_Fitness    = self.__aActivation.logistic( fTmp_Area * 8.0  - 6.0 ) 
            fTmp_Fitness    = fTmp_Fitness * fTmp_Freq_Tot +  0.375 * fTmp_Freq_Tot  + 0.6 * fTmp_Fitness

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

                    "dir":      kwargs["fitness"][i]["dir"] 
                }

                #   STEP 18: Loop through hard data
                for j in range(0, dTmp_Fit["hard"]["items"] ):
                    #   STEP 19: Add to fitness dictionary
                    dTmp_Results[ "f" + str( j ) ] = dTmp_Fit["hard"][ str( j ) ]["frequency"]
                    dTmp_Results[ "g" + str( j ) ] = dTmp_Fit["hard"][ str( j ) ]["gain"]

                Helga.nop()

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

                    "dir":      kwargs["fitness"][i]["dir"]
                }

            #   STEP 22: Append to output
            lOut.append(dTmp_Results)

        #   STEP 23: Return
        return lOut

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

                + slots = ( bool ) A flag that indicates whether or not slots
                    should be created and removed. If fals then slots will
                    only be changed
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

        #   STEP 8: Check if slots arg passed
        if ("slots" not in kwargs):
            #   STEP 9: Error handling
            raise Exception("An error occured in Natalie.__getCandidates__() -> Step 8: No slots arg passed")

        #
        #   endregion

        #   STEP 10: Update - Local variables
        dCenter     = kwargs["center"]
        dScalars    = self.__cAnt_Default["scalars"]

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
            dTmp_Candidate["ground plane"]["slots"]     = self.__getSlots__(center=dCenter["ground plane"]["slots"],       scalars=dScalars["ground plane"]["slots"],      plane=dTmp_Candidate["ground plane"],       z=0.0,                              region=fRegion, slots=kwargs["slots"])
            dTmp_Candidate["radiating plane"]["slots"]  = self.__getSlots__(center=dCenter["radiating plane"]["slots"],    scalars=dScalars["radiating plane"]["slots"],   plane=dTmp_Candidate["radiating plane"],    z=dTmp_Candidate["substrate"]["h"], region=fRegion, slots=kwargs["slots"])
            
            #   STEP 19: Append new candidate to output list
            lOut.append(dTmp_Candidate)
            
        #   STEP 20: Return
        return lOut

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

                + slots     = ( bool ) A flag that indicates whether or not
                    slots may be created and removed
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
        
        #   STEP 12: Check if slots arg passed
        if ("slots" not in kwargs):
            #   STEP 13: Error handling
            raise Exception("An error occured in Natalie.__getSlots__() -> Step 12: No slots arg passed")

        #
        #   endregion
        
        #   STEP 14: Update - Local variables
        dOut = cp.deepcopy(kwargs["center"])

        #   STEP 15: Check if there are elliptical slots
        if (kwargs["center"]["elliptical"]["items"] > 0):
            #   STEP 16: Setup - Tmp dictionaries
            dTmp_Slots  = dOut["elliptical"]
            dTmp_Scalar = kwargs["scalars"]["ellipse"]["change slot"]

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
            dTmp_Scalar = kwargs["scalars"]["square"]["change slot"]

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
            dTmp_Scalar = kwargs["scalars"]["triangle"]["change slot"]

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
            dTmp_Scalar = kwargs["scalars"]["polygon"]["change point"]

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

        #   STEP 41->115: Check - Slot creation and removal status
        if (kwargs["slots"]):
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

                fTmp_Prob   = kwargs["scalars"]["square"]["probability"]
                fTmp_Rand   = rn.uniform(0.0, 1.0)

                #   STEP 47->49: Check if square slot
                if (( fTmp_Rand < fTmp_Prob ) and ( dTmp_Slot == None )):
                    #   STEP 48: Setup - Scope variables
                    dTmp_Scalar = kwargs["scalars"]["square"]["create slot"]

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
                fTmp_Prob    += kwargs["scalars"]["ellipse"]["probability"]

                #   STEP 51->53: Check if elliptical slot
                if (( fTmp_Rand < fTmp_Prob ) and ( dTmp_Slot == None )):
                    #   STEP 52: Setup - Scope variables
                    dTmp_Scalar = kwargs["scalars"]["ellipse"]["create slot"]

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
                fTmp_Prob    += kwargs["scalars"]["triangle"]["probability"]

                #   STEP 55->60: Check if triangular slot
                if (( fTmp_Rand < fTmp_Prob ) and ( dTmp_Slot == None )):
                    #   STEP 56: Setup - Scope variables
                    dTmp_Scalar = kwargs["scalars"]["triangle"]["create slot"]

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
                fTmp_Prob    += kwargs["scalars"]["polygon"]["probability"]

                #   STEP 62->78: Check if polygonal slot
                if (( fTmp_Rand < fTmp_Prob ) and ( dTmp_Slot == None )):
                    #   STPE 63: Setup - Scope variables
                    dTmp_Scalar = kwargs["scalars"]["polygon"]["create point"]

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
                        if (rn.uniform(0.0, 1.0) < kwargs["scalars"]["ellipse"]["remove slot"]["probability"]):
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

                        return dOut

                    #   STEP 90: Add rectangular items to sum
                    iTmp_Sum    += dOut["rectangular"]["items"]

                    #   STEP 91: Check if rectangular
                    if (iTmp_Index < iTmp_Sum):
                        if (rn.uniform(0.0, 1.0) < kwargs["scalars"]["square"]["remove slot"]["probability"]):
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

                        return dOut

                    #   STEP 99: Add triangular items to sum
                    iTmp_Sum    += dOut["triangular"]["items"]

                    #   STEP 100: Check if triangular
                    if (iTmp_Index < iTmp_Sum):
                        if (rn.uniform(0.0, 1.0) < kwargs["scalars"]["triangle"]["remove slot"]["probability"]):
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

                        return dOut

                    iTmp_Sum += dOut["polygon"]["items"]

                    if (iTmp_Index < iTmp_Sum):
                        if (rn.uniform(0.0, 1.0) < kwargs["scalars"]["polygon"]["remove point"]["probability"]):
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

        #   STEP 116: Return
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
            iIndex  = kwargs["index"]

            if (kwargs["data"][0]["elliptical"]["items"] > 0):
                lTmp    = [[], [], [], []]

                for i in range(0, kwargs["data"][0]["elliptical"]["items"]):
                    for j in range(0, len( kwargs["data"] ) ):
                        lTmp[0].append( kwargs["data"][j]["elliptical"][str(i)]["l"])
                        lTmp[1].append( kwargs["data"][j]["elliptical"][str(i)]["w"])
                        lTmp[2].append( kwargs["data"][j]["elliptical"][str(i)]["x"])
                        lTmp[3].append( kwargs["data"][j]["elliptical"][str(i)]["y"])

                    lOut.extend(lTmp)
                    
                    kwargs["template"]["elliptical"][str(i)]["l"] = "remap-" + str(iIndex + 0)
                    kwargs["template"]["elliptical"][str(i)]["w"] = "remap-" + str(iIndex + 1)
                    kwargs["template"]["elliptical"][str(i)]["x"] = "remap-" + str(iIndex + 2)
                    kwargs["template"]["elliptical"][str(i)]["y"] = "remap-" + str(iIndex + 3)

                    iIndex += 4

            if (kwargs["data"][0]["rectangular"]["items"] > 0):
                lTmp    = [[], [], [], []]

                """
                ToDo:
                for i in range(0, kwargs["data"][0]["rectangular"]["items"]):
                    for j in range(0, len( kwargs["data"] ) ):
                        lTmp[0].append( kwargs["data"][j]["rectangular"][str(i)]["l"])
                        lTmp[1].append( kwargs["data"][j]["rectangular"][str(i)]["w"])
                        lTmp[2].append( kwargs["data"][j]["rectangular"][str(i)]["x"])
                        lTmp[3].append( kwargs["data"][j]["rectangular"][str(i)]["y"])

                    lOut.extend(lTmp)
                    
                    kwargs["template"]["rectangular"][str(i)]["l"] = "remap-" + str(iIndex + 0)
                    kwargs["template"]["rectangular"][str(i)]["w"] = "remap-" + str(iIndex + 1)
                    kwargs["template"]["rectangular"][str(i)]["x"] = "remap-" + str(iIndex + 2)
                    kwargs["template"]["rectangular"][str(i)]["y"] = "remap-" + str(iIndex + 3)

                    iIndex += 4
                """
                
                i = rn.randint(0, kwargs["data"][0]["rectangular"]["items"] - 1)
                for j in range(0, len( kwargs["data"] ) ):
                    lTmp[0].append( kwargs["data"][j]["rectangular"][str(i)]["l"])
                    lTmp[1].append( kwargs["data"][j]["rectangular"][str(i)]["w"])
                    lTmp[2].append( kwargs["data"][j]["rectangular"][str(i)]["x"])
                    lTmp[3].append( kwargs["data"][j]["rectangular"][str(i)]["y"])

                lOut.extend(lTmp)
                
                kwargs["template"]["rectangular"][str(i)]["l"] = "remap-" + str(iIndex + 0)
                kwargs["template"]["rectangular"][str(i)]["w"] = "remap-" + str(iIndex + 1)
                kwargs["template"]["rectangular"][str(i)]["x"] = "remap-" + str(iIndex + 2)
                kwargs["template"]["rectangular"][str(i)]["y"] = "remap-" + str(iIndex + 3)

                iIndex += 4

            if (kwargs["data"][0]["triangular"]["items"] > 0):
                lTmp    = [[], [], [], [], [], []]

                """
                ToDo
                for i in range(0, kwargs["data"][0]["triangular"]["items"]):
                    for j in range(0, len( kwargs["data"] ) ):
                        lTmp[0].append( kwargs["data"][j]["triangular"][str(i)]["0"]["x"])
                        lTmp[1].append( kwargs["data"][j]["triangular"][str(i)]["0"]["y"])
                        lTmp[2].append( kwargs["data"][j]["triangular"][str(i)]["1"]["x"])
                        lTmp[3].append( kwargs["data"][j]["triangular"][str(i)]["1"]["y"])
                        lTmp[4].append( kwargs["data"][j]["triangular"][str(i)]["2"]["x"])
                        lTmp[5].append( kwargs["data"][j]["triangular"][str(i)]["2"]["y"])
                        
                    lOut.extend(lTmp)
                    
                    kwargs["template"]["triangular"][str(i)]["0"]["x"] = "remap-" + str(iIndex + 0)
                    kwargs["template"]["triangular"][str(i)]["0"]["y"] = "remap-" + str(iIndex + 1)
                    kwargs["template"]["triangular"][str(i)]["1"]["x"] = "remap-" + str(iIndex + 0)
                    kwargs["template"]["triangular"][str(i)]["1"]["y"] = "remap-" + str(iIndex + 1)
                    kwargs["template"]["triangular"][str(i)]["2"]["x"] = "remap-" + str(iIndex + 0)
                    kwargs["template"]["triangular"][str(i)]["2"]["y"] = "remap-" + str(iIndex + 1)

                    iIndex += 6
                """
                
                i = rn.randint(0, kwargs["data"][0]["triangular"]["items"] - 1)
                for j in range(0, len( kwargs["data"] ) ):
                    lTmp[0].append( kwargs["data"][j]["triangular"][str(i)]["0"]["x"])
                    lTmp[1].append( kwargs["data"][j]["triangular"][str(i)]["0"]["y"])
                    lTmp[2].append( kwargs["data"][j]["triangular"][str(i)]["1"]["x"])
                    lTmp[3].append( kwargs["data"][j]["triangular"][str(i)]["1"]["y"])
                    lTmp[4].append( kwargs["data"][j]["triangular"][str(i)]["2"]["x"])
                    lTmp[5].append( kwargs["data"][j]["triangular"][str(i)]["2"]["y"])
                    
                lOut.extend(lTmp)
                
                kwargs["template"]["triangular"][str(i)]["0"]["x"] = "remap-" + str(iIndex + 0)
                kwargs["template"]["triangular"][str(i)]["0"]["y"] = "remap-" + str(iIndex + 1)
                kwargs["template"]["triangular"][str(i)]["1"]["x"] = "remap-" + str(iIndex + 0)
                kwargs["template"]["triangular"][str(i)]["1"]["y"] = "remap-" + str(iIndex + 1)
                kwargs["template"]["triangular"][str(i)]["2"]["x"] = "remap-" + str(iIndex + 0)
                kwargs["template"]["triangular"][str(i)]["2"]["y"] = "remap-" + str(iIndex + 1)

                iIndex += 6
                
        except Exception as ex:
            print("Initial error: ", ex)

        #   STEP 38: Return
        return lOut

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

                + candidate = ( list ) A list of the parameters for the antenna
                    geometry
                    ~ Required
        """

        #   STEP 0: Local variables
        lOut                    = []

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
        
        #   STEP 7: Check if candidate is list
        if (type(kwargs["candidate"]) == list):

            for i in range(0, len(kwargs["candidate"])):
                #   STEP 6: Setup - Local variables
                dCandidate_New  = cp.deepcopy(self.__dTemplate)

                #   STEP 7: Outsource
                self.__remapData_Recursion__(template=self.__dTemplate, data=kwargs["candidate"][i], candidate=dCandidate_New)

                #   STEP 8: Remap substrate
                self.__remapData_Substrate__(candidate=dCandidate_New)

                lOut.append(dCandidate_New)

        else:
            #   STEP 6: Setup - Local variables
            dCandidate_New  = cp.deepcopy(self.__dTemplate)

            #   STEP 7: Outsource
            self.__remapData_Recursion__(template=self.__dTemplate, data=kwargs["candidate"], candidate=dCandidate_New)

            #   STEP 8: Remap substrate
            self.__remapData_Substrate__(candidate=dCandidate_New)

            lOut.append(dCandidate_New)

        #   STEP 9: Return
        return lOut

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
                if (type(sTmp_Child) == dict):
                    self.__remapData_Recursion__(template=sTmp_Child, candidate=kwargs["candidate"][str(i)], data=kwargs["data"])

                #   STEP 11: Check if slots
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
        """

        #   STEP 0: Local variables
        dBest_Geo               = None
        dBest_Fit               = None

        sDir                    = None

        iRegion_Alg             = None
        iRegion_Srg             = None

        iIterations             = None

        bCull                   = None
        bSave                   = None
        bSurrogate              = None

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
        sDir            = self.__sDirectory + Helga.ticks() + "_" + kwargs["stage"]
        os.mkdir(sDir)

        iRegion_Alg     = cp.deepcopy(self.__iTRO_Region)
        iRegion_Srg     = cp.deepcopy(self.__iTRO_Region_SRG)

        bCull           = kwargs["cull"]
        bSave           = kwargs["save"]
        bSurrogate      = kwargs["surrogate"]

        #   STEP 13: Check if stage is primary
        if (kwargs["stage"] == "Primary"):
            iIterations = self.__iTRO_Iterations_Primary

            #   STEP 14: Check if new center or if center is None
            if ((kwargs["new"]) or (self.__dAnt_Center == None)):
                #   STEP 15: User output
                if (self.bShowOutput):
                    print("Natalie (tro-" + kwargs["stage"] + ") {" + Helga.time() + "} - Simulating starting antenna geometry")

                #   STEP 16: Outsource
                self.__dAnt_Center  = Matthew.getPatch_Default(name="center", dir=sDir, substrate=self.__dAnt_Substrate, frequency=self.__dAnt_Frequency, mesh=self.__dAnt_Mesh, runt=self.__dAnt_Runt, fitness=self.__dAnt_Fitness)
        
            #   STEP 17: Setup - Local variables
            dBest_Geo       = cp.deepcopy(self.__dAnt_Center)
            dBest_Fit       = {
                "fitness":  dBest_Geo["fitness"],
                "dir":      dBest_Geo["dir"]
            }

            dBest_Fit       = self.__getFitness__( ant=[dBest_Geo], fitness=[dBest_Fit] )[0]

            self.__dAnt_CenterFit = cp.deepcopy(dBest_Fit)

            #   STEP 20: Setup - Final steps
            del dBest_Geo["dir"]
            del dBest_Geo["fitness"]

        else:
            if ("center" not in kwargs):
                raise Exception("An error occured in Natalie.__tro__() -> Step ??: No center arg passed during primary pass")

            dBest_Geo   = kwargs["center"]["result"]
            dBest_Fit   = kwargs["center"]["fitness"]

            iIterations = self.__iTRO_Iterations_Secondary

        #
        #   endregion
        
        #   STEP 21: User output
        if (self.bShowOutput):
            print("Natalie (tro-" + kwargs["stage"] + ") {" + Helga.time() + "} - Begining Trust-Region Optimization.")

        #   STEP 22->116: TRO - Loop through iterations
        for i in range(0, iIterations):
            #   STEP 23: Setup - Scope variables
            lCandidates         = []
            lFitness            = []

            fTmp_Fitness        = np.inf

            iTmp_Candidates     = self.__iTRO_Candidates
            iTmp_Index          = 0
            iTmp_Count          = 0

            iTmp_Region         = 0

            #   STEP 24: Check - Surrogate status
            if (bSurrogate):
                #   STEP 25: Update - Scope variables
                iTmp_Region     = 0.5 * float(iRegion_Srg + iRegion_Alg) / float(self.__iTRO_Region_SRG + self.__iTRO_Region)

            #   STEP 26: No surrogate
            else:
                #   STEP 27: Update - Scope variables
                iTmp_Region     = 0.5 * float(iRegion_Alg) / float(self.__iTRO_Region)

            #   region STEP 28->48: Candidate generations and simulation

            #   STEP 28: Loop till amount of candidates reached
            while (True):
                #   STEP 29: Setup - Temp variables
                lTmp_Candidates = []
                
                #   STEP 30: Check if stage is Primary
                if (kwargs["stage"] == "Primary"):
                    #   STEP 31: Outsoruce - Get candidates
                    lTmp_Candidates = self.__getCandidates__(center=dBest_Geo, region=iTmp_Region, candidates=iTmp_Candidates, slots=True)

                #   STEP 32: Stage is secondary
                else:
                    #   STEP 33: Outsource - Get candidates
                    lTmp_Candidates = self.__getCandidates__(center=dBest_Geo, region=iTmp_Region, candidates=iTmp_Candidates, slots=False)

                #   STEP 34: User output
                if (self.bShowOutput):
                    print("\n\t{" + Helga.time() + "} - Simulating " + str(iTmp_Candidates) + " candidate antennas")

                #   STEP 35: Simulate antennas
                lTmp_Fitness    = Matthew.simulateCandidates_Json(dir=sDir, ant=lTmp_Candidates, frequency=self.__dAnt_Frequency, mesh=self.__dAnt_Mesh, runt=self.__dAnt_Runt, fitness=self.__dAnt_Fitness)

                #   STEP 36: Evaluate overall fitness of all geometries
                lTmp_Fitness    = self.__getFitness__(ant=lTmp_Candidates, fitness=lTmp_Fitness)

                #   STEP 37: Loop through all candidates
                while (iTmp_Count < len( lTmp_Candidates )):
                    #   STEP 38: Check that default fitness library wasn't returned
                    if ( lTmp_Fitness[iTmp_Count]["desired"] == np.inf):
                        #   STEP 39: Pop from list
                        sh.rmtree(os.path.dirname(lTmp_Fitness[iTmp_Count]["dir"]))

                        lTmp_Candidates.pop(iTmp_Count)
                        lTmp_Fitness.pop(iTmp_Count)

                    #   STEP 40: Not default library
                    else:
                        #   STEP 41: Increment counter
                        iTmp_Count  += 1

                #   STEP 42: Append results and fitnesses to lists
                lCandidates.extend(lTmp_Candidates)
                lFitness.extend(lTmp_Fitness)

                #   STEP 43: Check that required number of candidates met
                if (len( lCandidates ) == self.__iTRO_Candidates):
                    #   STEP 44: Exit loop
                    break

                #   STEP 45: Recalculate candidates
                iTmp_Candidates = self.__iTRO_Candidates - len( lCandidates )

            #   STEP 46: Append current best to lists
            lCandidates.append(dBest_Geo)
            lFitness.append(dBest_Fit)

            #
            #   endregion
            
            #   STEP 49->72: Check surrogate status
            if (bSurrogate):
                
                #   region STEP 50->62: Setup - Data container

                #   STEP 50: Setup - Scope variables
                dTmp_Data           = None
                dTmp_DataRange      = None
                dTmp_DataMap        = None

                lTmp_DataMap_In     = []
                lTmp_DataMap_Out    = []
                
                #   STEP 54: Update - Data dictionary
                dTmp_Data       = self.__moldData__(candidates=lCandidates,     fitness=lFitness)

                #   STEP 55: Setup - Final data ranges
                dTmp_DataRange      = {
                    "lower":        -0.99,
                    "center":       0.0,
                    "upper":        0.99
                }

                #   STEP 56: Setup - Data maps
                for j in range(0, len( dTmp_Data["in"] ) ):
                    lTmp_DataMap_In.append(j)

                for j in range(0, len( dTmp_Data["out"] ) ):
                    lTmp_DataMap_Out.append(j)

                dTmp_DataMap    = {
                    "in":   lTmp_DataMap_In,
                    "out":  lTmp_DataMap_Out
                }

                #   STEP 57: Setup - Create new Data container
                vData   = Data()
                vData.setData(data=dTmp_Data, automap=False, transpose=True)

                #   STEP 61: Map data
                vData.mapData(mapRange=dTmp_DataRange, mapSets=dTmp_DataMap, input=True, output=True)

                #
                #   endregion

                #   region STEP 63->72: Surrogate creation, training, mapping, simulation, and fitness evaluation

                #   STEP 63: Setup - Create new surrogate handler
                vGolem = Golem(numSurrogates=8)

                #   STEP 64: Update - surrogate handler parameters
                vGolem.bSRG_Random              = True
                vGolem.bSRG_RandomParameters    = False

                #   STEP 65: Train and map the surrogates
                vGolem.trainAndMap(data=vData, region=float( iRegion_Srg ) / self.__iTRO_Region_SRG, rand=True, remap=True)
                
                #   STEP 66: Remap - Surrogate candidate
                dTmp_SrgResults = self.__remapData__(candidate=vGolem.lMap_Results)

                #   STEP 67: User output
                if (self.bShowOutput):
                    print("\n\t{" + Helga.time() + "} - Simulating surrogate candidate.")

                #   STEP 68: Simulate - Surrogate candidate
                lTmp_SrgFitness = Matthew.simulateCandidates_Json(dir=sDir, ant=dTmp_SrgResults, frequency=self.__dAnt_Frequency, mesh=self.__dAnt_Mesh, runt=self.__dAnt_Runt, fitness=self.__dAnt_Fitness)

                #   STEP 69: Evaluate   - Surrogate candidate fitness
                lTmp_SrgFitness    = self.__getFitness__(ant=dTmp_SrgResults, fitness=lTmp_SrgFitness)
            
                #   STEP 70: Append - Surrogate candidate
                lCandidates.extend(dTmp_SrgResults)
                lFitness.extend(lTmp_SrgFitness)

                #
                #   endregion

            #   region STEP 73->76: Candidate evaluation

            #   STEP 73: Loop through candidates
            for j in range(0, len( lFitness )):
                #   STEP 74: Check if less than current best fitness
                if (lFitness[j]["final"] < fTmp_Fitness):
                    #   STEP 75: Update tmp vars
                    iTmp_Index      = j
                    fTmp_Fitness    = lFitness[j]["final"]

            #   STEP 76: Set new best candidate
            dBest_Geo = lCandidates[iTmp_Index]
            dBest_Fit = lFitness[iTmp_Index]
            
            #
            #   endregion

            #   region STEP 104->110: Continuous save

            #   STEP 104: Check for continuous save
            if (bSave):
                #   STEP 105: Setup - File location
                sTmp_File = sDir + "\\" + str(i) + ".json"

                #   STEP 106: Create file
                vTmp_File   = open(sTmp_File, "a")

                #   STEP 107: Close file
                vTmp_File.close()
                vTmp_File = None

                #   STEP 108: Re-open file
                with open(sTmp_File, "r+") as vTmp_File:
                    #   STEP 109: Create temp dictionary
                    dTmp = {
                        "geometry": dBest_Geo,
                        "fitness":  dBest_Fit,
                        "antenna":  self.__cAnt_Default,
                        "natalie":  self.__cf.data
                    }

                    #   STEP 110: Dump data
                    js.dump(dTmp, vTmp_File, indent=4, separators=(", ", " : "))
                    
                sFile   = os.path.abspath(".") + "\\Data\\DataSets\\Antenna\\920\\" + Helga.ticks()
                for j in range(0, len( lCandidates )):
                    sTmp_File = sFile + "_" + str(j) + ".json"

                    #   STEP 106: Create file
                    vTmp_File   = open(sTmp_File, "a")

                    #   STEP 107: Close file
                    vTmp_File.close()
                    vTmp_File = None

                    #   STEP 108: Re-open file
                    with open(sTmp_File, "r+") as vTmp_File:
                        #   STEP 109: Create temp dictionary
                        dTmp = {
                            "geometry": lCandidates[j],
                            "fitness":  lFitness[j]
                        }

                        #   STEP 110: Dump data
                        js.dump(dTmp, vTmp_File, indent=4, separators=(", ", " : "))

            #
            #   endregion
        
            #   region STEP 111->116: Cull the unworthy :)

            #   STEP 111: Check culling status
            if (bCull):
                #   STEP 112: Loop through candidates
                for j in range(0, self.__iTRO_Candidates + 1 ):
                    #   STEP 113: If not current best and not previous best
                    if ((j != iTmp_Index) and (j != self.__iTRO_Candidates)):
                        #   STEP 114: Get path for directory
                        sTmp_Path = os.path.dirname(lFitness[j]["dir"])

                        #   STEP 115: If not center
                        if ("center" not in sTmp_Path):
                            #   STEP 116: Delete directory
                            sh.rmtree(sTmp_Path)

            #
            #   endregion

            #   region STEP 77->99: Region update

            #   STEP 77->93: Check surrogate status
            if (bSurrogate):
                #   STEP 78: Check if best is surrogate candidates
                if (iTmp_Index > self.__iTRO_Candidates):
                    #   STEP 79: Update region
                    iRegion_Alg         += 1
                    iRegion_Srg         += 1

                    iTmp_Region         = round( float(iRegion_Alg + iRegion_Srg) / float(self.__iTRO_Region + self.__iTRO_Region_SRG), 3)

                    #   STEP 80: User output
                    if (self.bShowOutput):
                        print("\t{" + Helga.time() + "} - Iteration (" + str(i + 1) + "/" + str(iIterations) + ") : Increasing region via surrogate -> " + str(iTmp_Region))

                        dHold = lFitness[self.__iTRO_Candidates]
                        print("\t\t-Initial:",  "area=" + str(round(dHold["area"] * 100.0, 3)), "freq=" + str(round(dHold["freq"] * 100.0, 3)), "final=" + str(round(dHold["final"] * 100.0, 3)), sep="\t")
                        
                        dHold = lFitness[iTmp_Index]
                        print("\t\t-New:\t",    "area=" + str(round(dHold["area"] * 100.0, 3)), "freq=" + str(round(dHold["freq"] * 100.0, 3)), "final=" + str(round(dHold["final"] * 100.0, 3)), sep="\t", end="\n\n")

                #   STEP 81: Check if new best isn't old best
                elif (iTmp_Index != self.__iTRO_Candidates):
                    #   STEP 82: Update region
                    iRegion_Alg     += 1

                    #   STEP 83: Check if surrogate region not too small
                    if (iRegion_Srg > 0):
                        #   STEP 84: Update surrogate region
                        iRegion_Srg     -= 1

                    iTmp_Region         = round( float(iRegion_Alg + iRegion_Srg) / float(self.__iTRO_Region + self.__iTRO_Region_SRG), 3)

                    #   STEP 85: User output
                    if (self.bShowOutput):
                        print("\t{" + Helga.time() + "} - Iteration (" + str(i + 1) + "/" + str(iIterations) + ") : Increasing region -> " + str(iTmp_Region))

                        dHold = lFitness[self.__iTRO_Candidates]
                        print("\t\t-Initial:",  "area=" + str(round(dHold["area"] * 100.0, 3)), "freq=" + str(round(dHold["freq"] * 100.0, 3)), "final=" + str(round(dHold["final"] * 100.0, 3)), sep="\t")
                        
                        dHold = lFitness[iTmp_Index]
                        print("\t\t-New:\t",    "area=" + str(round(dHold["area"] * 100.0, 3)), "freq=" + str(round(dHold["freq"] * 100.0, 3)), "final=" + str(round(dHold["final"] * 100.0, 3)), sep="\t")
                        
                        dHold = lFitness[len(lFitness) - 1]
                        print("\t\t-SRG:\t",    "area=" + str(round(dHold["area"] * 100.0, 3)), "freq=" + str(round(dHold["freq"] * 100.0, 3)), "final=" + str(round(dHold["final"] * 100.0, 3)), sep="\t", end="\n\n")

                #   STEP 86: Bad region
                else:
                    #   STEP 87: Check if alg region not too small
                    if (iRegion_Alg > 0):
                        #   STEP 88: Update region
                        iRegion_Alg     += 1

                        #   STEP 89: Check if surrogate region not too small
                        if (iRegion_Srg > 0):
                            #   STEP 90: Update surrogate region
                            iRegion_Srg     -= 1

                        iTmp_Region         = round( float(iRegion_Alg + iRegion_Srg) / float(self.__iTRO_Region + self.__iTRO_Region_SRG), 3)

                        #   STEP 91: User output
                        if (self.bShowOutput):
                            print("\t{" + Helga.time() + "} - Iteration (" + str(i + 1) + "/" + str(iIterations) + ") : Decreasing region -> " + str(iTmp_Region))

                            dHold = lFitness[self.__iTRO_Candidates]
                            print("\t\t-Initial:",  "area=" + str(round(dHold["area"] * 100.0, 3)), "freq=" + str(round(dHold["freq"] * 100.0, 3)), "final=" + str(round(dHold["final"] * 100.0, 3)), sep="\t")
                            
                            dHold = lFitness[iTmp_Index]
                            print("\t\t-New:\t",    "area=" + str(round(dHold["area"] * 100.0, 3)), "freq=" + str(round(dHold["freq"] * 100.0, 3)), "final=" + str(round(dHold["final"] * 100.0, 3)), sep="\t")
                            
                            dHold = lFitness[len(lTmp_Candidates) - 1]
                            print("\t\t-SRG:\t",    "area=" + str(round(dHold["area"] * 100.0, 3)), "freq=" + str(round(dHold["freq"] * 100.0, 3)), "final=" + str(round(dHold["final"] * 100.0, 3)), sep="\t", end="\n\n")

                    #   STEP 92: Region too small
                    else:
                        #   STEP 93: Exit loop
                        break

            #   STEP 94->103: No surrogate
            else:
                #   STEP 95: Check if new best
                if (iTmp_Index != self.__iTRO_Candidates):
                    #   STEP 96: Update region
                    iRegion_Alg += 1

                    iTmp_Region = round( float(iRegion_Alg) / float(self.__iTRO_Region ), 3)

                    #   STEP 97: User output
                    if (self.bShowOutput):
                        print("\t{" + Helga.time() + "} - Iteration (" + str(i + 1) + "/" + str(iIterations) + ") : Increasing region -> " + str(iTmp_Region))

                        dHold = lFitness[self.__iTRO_Candidates]
                        print("\t\t-Initial:",  "area=" + str(round(dHold["area"] * 100.0, 3)), "freq=" + str(round(dHold["freq"] * 100.0, 3)), "final=" + str(round(dHold["final"] * 100.0, 3)), sep="\t")
                        
                        dHold = lFitness[iTmp_Index]
                        print("\t\t-New:\t",    "area=" + str(round(dHold["area"] * 100.0, 3)), "freq=" + str(round(dHold["freq"] * 100.0, 3)), "final=" + str(round(dHold["final"] * 100.0, 3)), sep="\t", end="\n\n")

                #   STEP 98: Not new best
                else:
                    #   STEP 99: Check if region too small
                    if (iRegion_Alg > 0):
                        #   STEP 100: Update - Decrement region
                        iRegion_Alg     -= 1

                        iTmp_Region = round( float(iRegion_Alg) / float(self.__iTRO_Region ), 3)

                        #   STEP 101: User output
                        if (self.bShowOutput):
                            print("\t{" + Helga.time() + "} - Iteration (" + str(i + 1) + "/" + str(iIterations) + ") : Decreasing region -> " + str(iTmp_Region), end="\n\n")
                    
                    #   STPE 102: Region too small
                    else:
                        #   STEP 103: Exit loop
                        break

            #
            #   endregion

        #   STEP 121: Populate output dictionary
        dOut    = {
            "result":   dBest_Geo,
            "fitness":  dBest_Fit
        }

        #   STEP 122: Return
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
        nat.optimizeAntenna(primary="tro", secondary="tro", surrogate=True)

#
#endregion