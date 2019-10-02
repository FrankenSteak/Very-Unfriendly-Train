#region Imports

from    enum                            import  Enum

import  copy                            as      cp
import  numpy                           as      np
import  os
import  random                          as      rn
import  sys
import  threading                       as      tr
import  time                            as      t

sys.path.append(os.path.abspath("."))

from    Code.Enums.Enums                import  Enums           as en
from    Code.Enums.Surrogates           import  Surrogates
from    Code.Enums.Swarms               import  Swarms
from    Code.Enums.GeneticAlgorithms    import  GeneticAlgorithms   as  ga

from    Code.Handlers.AntennaMathHandler                        import  Matthew
from    Code.Handlers.OptimizationHandler                       import  Hermione

from    Code.Surrogates.ArtificialNeuralNetwork                 import  Annie

from    Helpers.Config                  import  Conny
from    Helpers.DataContainer 		    import  Data
from    Helpers.GeneralHelpers          import  Helga

#endregion

#region Globals

global  thread_sUI
global  thread_eUI
global  thread_lUI

global  thread_lTR_Results
global  thread_lTR_Lock
global  thread_eTR_Exit
global  thread_eTR_Trained

global  thread_eEX

global  thread_eGlobal

#endregion

#region Class - Golem

class Golem:

    #region Init

    """
        Description:
        
            This class creates and trains multiple surrogate models using the
            provided dataset. It then uses multi-variate optimization
            algorithms to map the surrogate models in order to find the best
            solution for the provided dataset.

        |\n
        |\n
        |\n
        |\n
        |\n

        Arguments:

            + numSurrogates = ( int ) The number of surrogates that the class
                should use during the training and surface mapping process
                ~ Required
    """

    def __init__(self, **kwargs) -> None:
        
        #   region STEP 0: Local Variables

        self.__enum                     = en.Golem
        self.__cf                       = Conny()
        self.__cf.load(self.__enum.value)
        
        #
        #   endregion

        #   region STEP 1: Private Variables

        #   STEP 1.1: Surrogate variables
        self.__iSurrogates              = None

        self.__lSRG                     = []
        self.__lSRG_Parameters          = []
        self.__lSRG_Types               = []

        self.__lSRG_Results             = []
        self.__lSRG_FItness             = []
        self.__lSRG_Accuracy            = []

        #   STEP 1.2: Data variables
        self.__lData_Input              = []
        self.__lData_Output             = []
        
        #   STEP 1.3: Surrogate generation variables
        self.__iSRG_Min                 = self.__cf.data["parameters"]["surrogates"]["min"]
        self.__iSRG_Max                 = self.__cf.data["parameters"]["surrogates"]["max"]
        
        self.__fSRG_AccRequirement      = self.__cf.data["parameters"]["surrogates"]["accuracy requirement"]

        #   STEP 1.4: Other variables
        self.__bAllowTesting            = self.__cf.data["parameters"]["allow testing"]

        #
        #   endregion

        #   region STEP 2: Public Variables

        #   STEP 2.2: Results
        self.vBest                      = None
        self.vFitness                   = None

        self.lMap_Fitness               = None
        self.lMap_Results               = None

        #   STEP 2.3: Bools
        self.bShowOutput                = self.__cf.data["parameters"]["show output"]
        
        self.bSRG_Random                = self.__cf.data["parameters"]["bools"]["rand surrogate"]
        self.bSRG_RandomParameters      = self.__cf.data["parameters"]["bools"]["rand surrogate params"]

        #
        #   endregion

        #   region STEP 3->4: Error checking

        #   STEP 3: Check if numSurrogates arg passed
        if ("numSurrogates" not in kwargs):
            #   STEP 4: Error handling
            raise Exception("An error occured in Golem.__init__() -> Step 3: No numSurrogates arg passed")

        #
        #   endregion

        #   STEP 5: Update - Private variables
        self.__iSurrogates = kwargs["numSurrogates"]

        #   STEP 6: Return
        return
    
    #
    #endregion

    #region Front-End

    #   region Front-End: Import/Export

    def importGolem(self, **kwargs) -> None:
        """
            ToDo:

                + Implement function
        """

        #   STPE 0: Local variables
        #   STEP 1: Setup - Local variables
        #   STEP 2: ??
        #   STEP ??: Return
        return

    def exportGolem(self, **kwargs) -> None:
        """
            ToDo:

                + Implement function
        """

        #   STEP 0: Local variables
        #   STEP 1: Setup - Local variables
        #   STEP 2: ??
        #   STEP ??: Return
        return

    #
    #   endregion

    #   region Front-End: Train and Map (Teenage Mutant Ninja Turtles)

    def trainAndMap(self, **kwargs) -> dict:
        """
            Description:

                Uses multi-threading to train and map multiple surrogate models
                simultaneously.

            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:

                + data  = ( vars ) Data container instance that contains the
                    dataset required for training and mapping

                + region    = ( float ) The region within which random 
                    generation is allowed
                    ~ Required

                + rand  = ( bool ) A flag that specifies whether or not random
                    parameters are allowed for the training and mapping process

                + testing   = ( bool ) Disables Data.setData() for testing
                    purposes

                + remap = ( bool ) A flag to indicate if the results of the
                    mapping should be un-normalized via the dataset

            |\n

            Returns:

                + dOut = ( dict ) A dictionary containing the best surrogate
                    result and the fitness of the results
                    ~ "result"  = ( dict )
                    ~ "fitness" = ( dict )
                    
            |\n

            ToDo:

                + Add start arg
        """

        #   STEP 0: Local variables

        #   STEP 1: Setup - Local variables

        #   region STEP 2->10: Error checking

        #   STEP 2: Check if data arg passed
        if ("data" not in kwargs):
            #   STEP 3: Error handling
            raise Exception("An error occured in Golem.trainAndMap() -> Step 2: No data arg passed")

        #   STEP 4: Check if region arg passed
        if ("region" not in kwargs):
            #   STEP 5: Error handling
            raise Exception("An error occured in Golem.trainAndMap() -> Step 4: No region arg passed")

        #   STEP 6: Check if rand arg passed
        if ("rand" in kwargs):
            #   STEP 7: Update - Class var
            self.bSRG_Random = kwargs["rand"]

        #
        #   endregion

        #   STEP 9: Train surrogates
        self.__train_srgOverseer__(data=kwargs["data"], region=kwargs["region"])

        #   STEP 10: Map surrogates
        self.__map_srgOverseer__(data=kwargs["data"])

        #   STEP 11: Check for remapping
        if ("remap" in kwargs):
            #   STEP 12: Check remapping state
            if (kwargs["remap"]):
                #   STEP 13: Remap
                self.vBest = kwargs["data"].remap( cp.deepcopy( self.vBest ) )

        #   STEP 14: Populate output dict
        dOut = {
            "result":   self.vBest,
            "fitness":  self.vFitness
        }

        #   STEP 15: Return
        return dOut

    #
    #   endregion

    #
    #endregion

    #region Back-End

    #   region Back-End: Inits
    
    def __initSRGParams__(self, **kwargs) -> dict:
        """
            Description:

                Recursively iterates through the antenna surrogate parameters
                and randomizes them

            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:

                + params    = ( dict ) A dictionary containing the parameters
                    for a surrogate model
                    ~ Requried

                + scalars   = ( dict ) A dictionary containing the scalar
                    values for a surrogate model
                    ~ Required

                + region    = ( int ) The region in which random generation is
                    allowed
                    ~ Required
        """

        #   STEP 0: Local variables
        dOut                    = None

        #   STEP 1: Setup - Local variables

        #   region STEP 2->7: Error checking

        #   STEP 2: Check if params arg passed
        if ("params" not in kwargs):
            #   STEP 3: Error handling
            raise Exception("An error occured in Golem.__initSRGParms__() -> Step 2: No params arg passed")

        #   STEP 4: Check if scalars arg passed
        if ("scalars" not in kwargs):
            #   STEP 5: Error handling
            raise Exception("An error occured in Golem.__initSRGParams__() -> Step 4: No scalars arg passed")

        #   STEP 6: Check if region arg passed
        if ("region" not in kwargs):
            #   STEP 7: Error handling
            raise Exception("An error occured in Golem.__initSRGParams__() -> Step 6: No region arg passed")

        #
        #   endregion

        #   STEP 8: Update - Local variables
        dOut    = kwargs["params"]

        #   STEP 9: Check if random parameters allowed
        if (self.bSRG_RandomParameters == False):
            #   STEP 10: Return
            return dOut

        #   STEP 11: Loop through parameters in current dictionary
        for i in range(0, dOut["items"]):
            #   STEP 12: Get child entry name
            sTmp_Child  = dOut[str(i)]

            #   STEP 13: Check if in scalars
            if (sTmp_Child in kwargs["scalars"]):
                #   STEP 14: Be safe
                try:
                    #   STEP 15: Check if field contains child dictionary
                    if ("items" in dOut[sTmp_Child]):
                        #   STEP 16: Outsource
                        self.__initSRGParams__(params=dOut[sTmp_Child], scalars=kwargs["scalars"][sTmp_Child], region=kwargs["region"])

                #   STEP 17: Shortcut
                except:
                    #   STEP 18: Outsoruce
                    dOut[sTmp_Child] = self.__randVal__(param=dOut[sTmp_Child], scalar=kwargs["scalars"][sTmp_Child], region=kwargs["region"])


        #   STEP 20: Return
        return dOut

    def __initGlobals__(self) -> None:
        """
            Description:

                Initializes all the required global variables for this class.
        """

        #   STEP -1: Global variables
        global  thread_sUI
        global  thread_eUI
        global  thread_lUI

        global  thread_lTR_Results
        global  thread_lTR_Lock
        global  thread_eTR_Exit

        global  thread_eEX

        global  thread_eGlobal

        #   STEP 0: Local variables
        lTmp                    = None

        #   STEP 1: Setup - Local variables

        #   STEP 2: Setup - Global UI variables
        thread_sUI      = ""
        thread_eUI      = tr.Event()
        thread_lUI      = tr.Lock()
        
        #   STEP 3: Setup - Training thread variables
        lTmp = []

        #   STEP 4: Loop through required surrogates
        for _ in range(0, self.__iSRG_Max):
            #   STEP 5: Append empty var as holder
            lTmp.append(None)

        #   STEP 6: Set global variable
        thread_lTR_Results  = lTmp
        thread_lTR_Lock     = tr.Lock()

        #   STEP 7: Setup - Training exit event
        thread_eTR_Exit = tr.Event()
        thread_eTR_Exit.clear()

        #   STEP 8: Setup - Global exit event
        thread_eEX      = tr.Event()
        thread_eEX.clear()

        #   STEP 9: Setup - Global event signal
        thread_eGlobal  = tr.Event()
        thread_eGlobal.clear()

        #   STEP 10: Return
        return

    #
    #   endregion

    #   region Back-End: Gets

    def __randVal__(self, **kwargs) -> float:
        """
            Description:

                Gets a random value using the provided arguments.

            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:

                + param = ( float ) The parameters to be randomized
                    ~ Required

                + scalar    = ( dict ) The scalar values to use during the
                    randomization process
                    ~ Required

                + region    = ( float ) The region within which random
                    generation is allowed
                    ~ Required
        """

        #   STEP 0: Local variables
        dOut                = None

        fRand               = rn.random()

        bRegion             = False

        #   STEP 1: Setup - Local variables
        
        #   region STEP 2->7: Error checking

        #   STEP 2: Check if param arg passed
        if ("param" not in kwargs):
            #   STEP 3: Error handling
            raise Exception("An error occured in Golem.__randVal__() -> Step 2: No param arg passed")

        #   STEP 4: Check if scalar arg passed
        if ("scalar" not in kwargs):
            #   STEP 5: Error handling
            raise Exception("An error occured in Golem.__randVal__() -> Step 4: No scalar arg passed")

        #   STEP 6: Check region arg passed
        if ("region" not in kwargs):
            #   STEP 7: Error handling
            raise Exception("An error occured in Golem.__randVal__() -> Step 6: No region arg passed")

        #
        #   endregion
        
        #   STEP 7: Update - Local variables
        dOut        = kwargs["param"]

        #   STEP 8: Check if positive
        if (fRand <= kwargs["scalar"]["region"]):
            #   STEP 9: Set region = True for pos
            bRegion = True

        #   STEP 10: Check if positive region
        if (bRegion):
            #   STEP 11: Get pos offset
            fTmp_Offset_Pos = rn.random() * kwargs["region"] * kwargs["scalar"]["range"]["positive"]

            #   STEP 12: Add offset to output
            dOut += fTmp_Offset_Pos

        #   STEP 13: Then negative
        else:
            #   STEP 14: Get neg offset
            fTmp_Offset_Neg = rn.random() * kwargs["region"] * kwargs["scalar"]["range"]["negative"]

            #   STEP 15: Subtract offset from output
            dOut -= fTmp_Offset_Neg

        #   STEP 16: Check if type defined
        if ("type" in kwargs["scalar"]):
            #   STPE 17: Check if int
            if (kwargs["scalar"]["type"] == "int"):
                #   STEP 18: Cast to int
                dOut = int(dOut)

        #   STEP 19: Return
        return dOut

    def __getSurrogate__(self, **kwargs) -> dict:
        """
            Description:
            
                Initializes a surrogate model using the parameters from the
                config files.

            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:

                + region    = ( float ) The region within which random
                    generation is allowed
                    ~ Required
        """

        #   STEP 0: Local variables
        vSRG_New                = None
        eSRG_Enum               = None

        dSRG_Params             = None
        dSRG_Scalars            = None
        
        iSRG_Index              = None

        lSRG_Active             = Surrogates.getActiveSurrogates()
        lSRG_Parameters         = Surrogates.getActiveParameters()
        lSRG_Scalars            = Surrogates.getActiveScalars()

        #   STEP 1: Setup - Local variables

        #   STEP 2: Check if region arg passed
        if ("region" not in kwargs):
            #   STEP 3: Error handling
            raise Exception("An error occured in Golem.__getSurrogate__() -> Step 2: No region arg passed")

        #   STEP 4: Check if random surrogate selection allowed
        if (self.bSRG_Random):
            #   STEP 5: Get random surrogate enum index
            iSRG_Index  = rn.randint(0, len(lSRG_Active) - 1)

            #   STEP 6: Set new surrogate enum
            eSRG_Enum   = lSRG_Active[iSRG_Index]

        else:
            #   STEP 7: Select default surrogate (i.e: Annie)
            iSRG_Index  = 0
            eSRG_Enum   = lSRG_Active[0]

        #   STEP 8: Get new surrogate parameters and scalars
        dSRG_Params     = cp.deepcopy(lSRG_Parameters[iSRG_Index])
        dSRG_Scalars    = cp.deepcopy(lSRG_Scalars[iSRG_Index])

        #   STEP 9: Adjust surrogate parameters
        dSRG_Params     = self.__initSRGParams__(params=dSRG_Params, scalars=dSRG_Scalars, region=kwargs["region"])

        #   STEP 10: Create new surrogate
        vSRG_New        = Surrogates.getNewSurrogate(surrogate=eSRG_Enum, params=dSRG_Params)

        #   STEP 11: Populate output dictionary
        dTmp_Out        = {
            "surrogate":    vSRG_New,
            "params":       dSRG_Params,
            "enum":         eSRG_Enum
        }

        #   STEP 12: Return
        return dTmp_Out

    #
    #   endregion

    #   region Back-End: Training

    def __train_srgOverseer__(self, **kwargs) -> None:
        """
            Description:

                Trains the initialized surrogates using the provided dataset.

            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:

                + data  = ( vars ) A data container containing the data set for
                    the training process
                    ~ Required

                + region    = ( float ) The region within which random 
                    number generation can cocured
                    ~ Required
        """

        #   STEP -1: Global variables
        global  thread_eUI
        global  thread_sUI

        global  thread_eTR_Exit

        global  thread_eEX

        global  thread_eGlobal

        #   STEP 0: Local variables
        tUI_Thread              = None
        tTR_Thread              = None

        #   STEP 1: Setup - Local variables

        #   region STEP 2->7: Error checking

        #   STEP 2: Check if data arg passed
        if ("data" not in kwargs):
            #   STEP 3: Error handling
            raise Exception("An error occured in Golem.__train_srgOverseer__() -> Step 2: No data arg passed")
        
        #   STEP 4: Check if region arg passed
        if ("region" not in kwargs):
            #   STEP 5: Error handling
            raise Exception("An error occured in Golem.__train_srgOverseer__() -> Step 4: No region arg passed") 
        
        #
        #   endregion

        #   STEP 8: Setup - UI Thread
        tUI_Thread  = tr.Thread(target=self.__threadUI__)
        tUI_Thread.daemon = True

        #   STEP 9: Setup - Training thread
        dTmp_Train = {
            "min":      self.__iSRG_Min,
            "max":      self.__iSRG_Max,
            "acc":      self.__fSRG_AccRequirement,

            "region":   kwargs["region"],

            "data":     kwargs["data"]
        }

        tTR_Thread  = tr.Thread(target=self.__train_srgHandler__, args=(dTmp_Train, ))
        tTR_Thread.daemon = True

        #   STEP 10: Setup - Global variables
        self.__initGlobals__()

        #   STEP 11: Start threads
        print("\t~ Starting surrogate training")
        tUI_Thread.start()
        tTR_Thread.start()

        #   STEP 12: Loop until exit
        while (True):
            #   STEP 13: Wait for global event
            thread_eGlobal.wait()

            #   STEP 14: Clear event
            thread_eGlobal.clear()

            #   STEP 15: Check if ui
            if (thread_eUI.is_set()):
                #   STEP 16: Check if input is "exit"
                if (thread_sUI == "exit"):
                    #   STEP 17: Set exit event
                    thread_eEX.set()

                    #   STEP 18: Wait for training thread to join
                    tTR_Thread.join()

                    #   STEP 19: Exit loop
                    break
                
                #   STEP 20: Output wasn't exit
                else:
                    #   STEP 21: Reset - Global UI variables
                    thread_eUI.clear()
                    thread_sUI = ""

                    #   STEP 22: Reset - UI thread
                    tUI_Thread  = tr.Thread(target=self.__threadUI__)
                    tUI_Thread.daemon = True

                    #   STEP 23: Restart - UI thread
                    tUI_Thread.start()

            #   STEP 24: Check if training completed
            if (thread_eTR_Exit.is_set()):
                #   STEP 25: Transfer thread results
                self.__train_transferResults__()

                #   STEP 26: Exit loop
                break

        #   STEP 27: Return
        del tUI_Thread

        return

    def __train_srgHandler__(self, kwargs: dict) -> None:
        """
            Description:

                Iteratively trains surrogates until it either finds a surrogate
                that meets the minimum accuracy requirements or until it has
                trained the maximum amount of surrogates.

            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:

                + data  = ( vars ) A Data instance containing the dataset for
                    the training process
                    ~ Required

                + region    = ( float ) The region within which random 
                    number generation can cocured
                    ~ Required

                + min   = ( int ) The minimum amount of required trained
                    surrogates
                    ~ Required

                + max   = ( int ) The maximum amount of required trained
                    surrogates
                    ~ Required

                + acc   = ( float ) The minimum accuracy requirement for which
                    the function will terminate early
                    ~ Required
        """

        #   STEP -1: Global variables
        global  thread_lTR_Results
        global  thread_eTR_Exit

        global  thread_eEX

        global  thread_eGlobal

        #   STEP 0: Local variables
        vData                   = None

        fBest_Fitness           = np.inf
        iBest_Index             = 0

        #   STEP 1: Setup - Local variables

        #   region STEP 2->?11: Error checking

        #   STEP 2: Check if data arg passed
        if ("data" not in kwargs):
            #   STEP 3: Error handling
            raise Exception("An error occured in Golem.__train_srgHandler__() -> Step 2: No data arg passed")
        
        #   STEP 4: Check if min arg passed
        if ("min" not in kwargs):
            #   STEP 5: Error handling
            raise Exception("An error occured in Golem.__train_srgHandler__() -> Step 4: No min arg passed")
        
        #   STEP 6: Check if max arg passed
        if ("max" not in kwargs):
            #   STPE 7: Error handling
            raise Exception("An error occured in Golem.__train_srgHandler__() -> Step 6: No max arg passed")

        #   STEP 8: Check if acc arg passed
        if ("acc" not in kwargs):
            #   STPE 9: Error handling
            raise Exception("An error occured in Golem.__train_srgHandler__() -> Step 8: No acc arg passed")

        #   STEP 10: Checkif start arg passed
        if ("region" not in kwargs):
            #   STEP 11: Error handling
            raise Exception("An error occured in Golem.__train_srgHandler__() -> Step 10: No start region passed")

        #
        #   endregion
        
        #   STEP 12: Update - Local variables
        vData   = kwargs["data"]

        #   STEP 13: Iterate through max surrogates
        for i in range(0, kwargs["max"]):
            #   STEP 14: Get new surrogate
            dSRG    = self.__getSurrogate__(region=kwargs["region"])

            vSRG    = dSRG["surrogate"]

            #   STEP 15: Do necessary pre-training
            vSRG.bShowOutput = False

            #   STEP 16: Train surrogate
            vSRG.trainSet(cp.deepcopy(vData), advanced_training=False, compare=False)

            #   STEP 17: Get accuracy and fitness
            fTmp_Fitness    = float ( vSRG.getAFitness(data=vData) / vData.getLen() )
            fTmp_Accuracy   = vSRG.getAccuracy(data=vData, size=vData.getLen(), full_set=True)
            
            #   STEP 18: Create result dictionary
            dTmp_Results    = {
                "surrogate":        vSRG,
                "params":           dSRG["params"],
                "enum":             dSRG["enum"],

                "fitness":          fTmp_Fitness,

                "accuracy":         fTmp_Accuracy["percent accuracy"]
            }

            #   STEP 19: Add to global
            thread_lTR_Results[i] = dTmp_Results

            #   STEP 20: Check if fittest surrogate so far
            if ((fTmp_Fitness < fBest_Fitness) and (fTmp_Accuracy["percent accuracy"] == 1.0)):
                #   STEP 21: Update - Local variables
                fBest_Fitness   = fTmp_Fitness
                iBest_Index     = i

                #   STEP 22: User output - minimal
                print("!", end="")

            else:
                #   STEP 23: Minimal output
                print(".", end="")

            #   STEP 24: Check if fitness below required and min surrogates generated 
            if ((fBest_Fitness < kwargs["acc"]) and (i >= kwargs["min"])):
                #   STEP 25: Exit loop early
                print("")
                break

            #   STEP 26: Check if exit even
            if (thread_eEX.is_set()):
                #   STEP 27: Exit loop early
                print("")
                break

        #   STEP 28: Swap best surrogate to index = 0
        dSwap_0                         = thread_lTR_Results[0]
        thread_lTR_Results[0]           = thread_lTR_Results[iBest_Index]
        thread_lTR_Results[iBest_Index] = dSwap_0

        #   STEP 29: Set exit events
        thread_eTR_Exit.set()
        thread_eGlobal.set()

        #   STEP 30: Return
        return
    
    def __train_transferResults__(self, **kwargs) -> None:
        """
            Description:

                Transfers results from the surrogate handler to this class'
                private variables
        """

        #   STEP -1: Global variables
        global  thread_lTR_Results
        global  thread_lTR_Lock

        #   STEP 0: Local variables
        thread_lTR_Lock.acquire()
        
        #   STEP 1: Setup - Local variables
        
        #   STEP 2: Clear current vars (precautionary)
        self.__lSRG             = []
        self.__lSRG_Parameters  = []
        self.__lSRG_FItness     = []
        self.__lSRG_Types       = []
        self.__lSRG_Accuracy    = []
        
        #   STEP 3: Iterate through globally stored results
        for i in range(0, len(thread_lTR_Results)):
            #   STEP 4: Be safe OwO
            try:
                #   STEP 5: Save data to class variables
                self.__lSRG.append(thread_lTR_Results[i]["surrogate"])
                self.__lSRG_Parameters.append(thread_lTR_Results[i]["params"])
                self.__lSRG_FItness.append(thread_lTR_Results[i]["fitness"])
                self.__lSRG_Types.append(thread_lTR_Results[i]["enum"])
                self.__lSRG_Accuracy.append(thread_lTR_Results[i]["accuracy"])

            except:
                #   STEP 6: End of list reached, exit loop
                break

        #   STEP 7: Return
        thread_lTR_Lock.release()
        return

    #
    #   endregion

    #   region Back-End: Mapping

    def __map_srgOverseer__(self, **kwargs) -> None:
        """
            Description:

                Maps the fittest surrogate as well as all the other surrogates
                whose fitness were within the required range
        """

        #   STEP 0: Local variables
        optimizer               = Hermione()

        self.vBest              = None
        self.vFitness           = np.inf

        #   STEP 1: Setup - Local variables
        self.lMap_Results     = []
        self.lMap_Fitness     = []
        
        #   STEP 2: User output
        print("\t~ Starting surrogate mapping\t\t-> ", end="")

        #   STEP 3: Loop through surrogates
        for i in range(0, len(self.__lSRG)):
            #   STEP 4: If surrogate fitness less than required or i == 0
            if ((i == 0) or (self.__lSRG_Accuracy[i] == 1.0)):
                #   STEP 5: Outsource
                dTmp_MapResults = optimizer.mapSurrogate(threading=False, data=kwargs["data"], surrogate=self.__lSRG[i], optimizer=ga.TRO)

                #   STEP 6: Append to results
                self.lMap_Results.append(dTmp_MapResults["result"])
                self.lMap_Fitness.append(dTmp_MapResults["fitness"])

                #   STEP 7: Check if new fittest
                if (dTmp_MapResults["fitness"] < self.vFitness):
                    #   STEP 8: Set new fittest
                    self.vBest      = dTmp_MapResults["result"]
                    self.vFitness   = dTmp_MapResults["fitness"]

                    print("!", end="")

                else:
                    print(".", end="")

        #   STEP 9: Return
        print("")
        return

    #
    #   endregion

    #   region Back-End: Threading
    
    def __threadUI__(self) -> None:
        """
            ToDo:
            
                + Implement
        """
        
        #   STEP -1: Global variables
        global  thread_sUI
        global  thread_eUI
        global  thread_lUI

        global  thread_eGlobal

        #   STEP 0: Local variables

        #   STEP 1: Setup - Local variables
        
        #   STEP 2: Attempt to acquire lock
        if (thread_eUI.is_set()):
            thread_eUI.wait()

        #   STEP 3: Wait for user input
        thread_sUI = input("\t> ")

        #   STEP 5: Check that parent hasn't reset
        if (thread_eUI != None):
            #   STEP 6: Set events
            thread_eUI.set()
            thread_eGlobal.set()

        #   STEP 8: Return
        return

    def __clearGlobals__(self) -> None:
        """
            Description:

                Clears all the global variables associated with this class.
        """

        #   STEP 0: Local variables
        global  thread_sUI
        global  thread_eUI
        global  thread_lUI

        global  thread_lTR_Results
        global  thread_lTR_Lock
        global  thread_eTR_Exit

        global  thread_eEX

        global  thread_eGlobal

        #   STEP 1: Setup - Local variables
        thread_lTR_Lock.acquire()
        thread_lTR_Lock.release()

        #   STEP 2: Yeet
        thread_sUI          = None
        thread_eUI          = None
        thread_lUI.release()
        thread_lUI          = None

        thread_lTR_Results  = None
        thread_lTR_Lock     = None
        thread_eTR_Exit     = None

        thread_eEX          = None

        thread_eGlobal      = None

        #   STEP 3: Return
        return

    #
    #   endregion

    #
    #endregion

#
#endregion

#region Testing

#
#endregion