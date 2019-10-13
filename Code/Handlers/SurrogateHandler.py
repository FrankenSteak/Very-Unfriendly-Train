#region Imports

from    enum                            import  Enum

import  copy                            as      cp
import  multiprocessing                 as      mp
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
        self.__lSRG_FItness             = []
        self.__lSRG_Accuracy            = []
        
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
                self.vBest = kwargs["data"].remap( candidate=cp.deepcopy( self.vBest ) )

                #   STEP 14: Loop through best candidates
                for i in range(0, len( self.lMap_Results )):
                    #   STEP 15: Outsource - Remapping
                    self.lMap_Results[i] = kwargs["data"].remap( candidate=cp.deepcopy( self.lMap_Results[i] ))

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

        #   STEP 0: Local variables
        eGlobal                 = None
        eGlobal_Exit            = None

        eUI_Event               = None
        qUI_Queue               = None
        tUI_Thread              = None

        eTR_Event               = None
        qTR_Queue               = None
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

        #   STEP 8: Setup - Global events
        eGlobal         = mp.Event()
        eGlobal.clear()

        eGlobal_Exit    = mp.Event()
        eGlobal_Exit.clear()

        #   STEP 9: Setup - UI variables
        eUI_Event       = mp.Event()
        eUI_Event.clear()

        qUI_Queue       = mp.Queue()

        tUI_Thread          = tr.Thread(target=self.__threadUI__, args=(eGlobal_Exit, eGlobal, eUI_Event, qUI_Queue, ))
        tUI_Thread.daemon   = True
        #tUI_Thread.start()
        
        #   STEP 9: Setup - Training thread
        eTR_Event           = mp.Event()
        eTR_Event.clear()

        dTmp_Train = {
            "min":      self.__iSRG_Min,
            "max":      self.__iSRG_Max,
            "acc":      self.__fSRG_AccRequirement,

            "region":   kwargs["region"],

            "data":     kwargs["data"]
        }

        qTR_Queue           = mp.Queue()
        qTR_Queue.put([dTmp_Train])

        tTR_Thread          = tr.Thread(target=self.__train_srgHandler__, args=(eGlobal_Exit, eGlobal, eTR_Event, qTR_Queue, ))
        tTR_Thread.daemon   = True
        tTR_Thread.start()

        #   STEP 11: Loop until exit
        while (True):
            #   STEP 12: Wait for global event
            eGlobal.wait()

            #   STEP 13: Clear event
            eGlobal.clear()

            #   STEP 15: Check if ui
            if (eUI_Event.is_set()):
                #   STEP 16: Check if input is "exit"
                if (qUI_Queue.get()[0] == "exit"):
                    #   STEP 17: Set global exit event
                    eGlobal_Exit.set()

                    #   STEP 18: Wait for threads
                    #tUI_Thread.join()
                    tTR_Thread.join()

                    #   STEP 19: Exit loop
                    break
                
            #   STEP 20: Check if training completed
            if (eTR_Event.is_set()):
                #   STEP 21: Set global exit event
                eGlobal_Exit.set()
                #tUI_Thread.join()

                #   STEP 22: Exit loop
                break

        #   STEP 23: Get results from training
        dTmp_SrgResults = qTR_Queue.get()[0]

        #   STEP 24: Update - Class variables
        self.__lSRG_Accuracy    = dTmp_SrgResults["accuracy"]
        self.__lSRG_FItness     = dTmp_SrgResults["fitness"]
        self.__lSRG             = dTmp_SrgResults["results"]

        #   STEP 25: Return
        return

    def __train_srgHandler__(self, _eExit, _eGlobal, _eTR, _qTR) -> None:
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

                + _eExit    = ( mp.Event() ) Global exit event

                + _eGlobal  = ( mp.Event() ) Global thread result event

                + _eTR      = ( mp.Event() ) Surrogate training result event

                + _qTR      = ( mp.Queue() ) Surrogate training result queue
        """

        #   STEP 0: Local variables
        dArgs                   = _qTR.get()[0]

        vData                   = dArgs["data"]

        lAccuracy               = []
        lFitness                = []
        lResults                = []

        fBest_Fitness           = np.inf
        iBest_Index             = 0

        print("\t{" + Helga.time() + "} - Starting surrogate training\t\t-> ", end="")

        #   STEP 1: Iterate through max surrogates
        for i in range(0, dArgs["max"]):
            #   STEP 2: Get new surrogate
            dSRG    = self.__getSurrogate__(region=dArgs["region"])

            vSRG    = dSRG["surrogate"]

            #   STEP 3 Do necessary pre-training
            vSRG.bShowOutput            = True
            vSRG.bUse_NoiseInjection    = True

            #   STEP 4: Train surrogate
            fTmp_Fitness    = vSRG.trainSet(cp.deepcopy(vData), advanced_training=False, compare=False)
            fTmp_Fitness    = fTmp_Fitness["fitness"]

            #   STEP 5: Get accuracy and fitness
            fTmp_Accuracy   = vSRG.getAccuracy(data=vData, size=vData.getLen(), full_set=True)

            fTmp_Fitness    = fTmp_Fitness * (1.1 - fTmp_Accuracy["percent accuracy"])

            #   STEP 6: Append to output lists
            lAccuracy.append( fTmp_Accuracy["percent accuracy"] )
            lFitness.append( fTmp_Fitness )
            lResults.append( vSRG )

            #   STEP 7: Check if fittest surrogate so far
            if ((fTmp_Fitness < fBest_Fitness) and (fTmp_Accuracy["percent accuracy"] == 1.0)):
                #   STEP 8: Update - Local variables
                fBest_Fitness   = fTmp_Fitness
                iBest_Index     = i

                #   STEP 9: User output - minimal
                print("!", end="")

            #   STEP 10: Check if 100p accuracy
            elif (fTmp_Accuracy["percent accuracy"] == 1.0):
                #   STEP 11: Minimal output
                print(":", end="")

            #   STEP 12: Not 100p but best fitness
            elif (fTmp_Fitness < fBest_Fitness):
                #   STEP 13: Update - Local variables
                fBest_Fitness   = fTmp_Fitness
                iBest_Index     = i

                #   STEP 14: User output - minimal
                print("#", end="")

            #   STEP 15: Bad surrogate
            else:
                #   STEP 16: User outptu - minimal
                print(".", end="")

            #   STEP 17: Check if fitness below required and min surrogates generated 
            if ((fBest_Fitness < dArgs["acc"]) and (i >= dArgs["min"])):
                #   STEP 18: Exit loop early
                break

            #   STEP 19: Check if exit even
            if (_eExit.is_set()):
                #   STEP 20: Exit loop early
                break

        print("")
        
        #   STEP 21: Swap best surrogate to index = 0
        vTmp_Swap               = lAccuracy[0]
        lAccuracy[0]            = lAccuracy[iBest_Index]
        lAccuracy[iBest_Index]  = vTmp_Swap
        
        vTmp_Swap               = lFitness[0]
        lFitness[0]             = lFitness[iBest_Index]
        lFitness[iBest_Index]   = vTmp_Swap

        vTmp_Swap               = lResults[0]
        lResults[0]             = lResults[iBest_Index]
        lResults[iBest_Index]   = vTmp_Swap

        #   STEP 22: Populate output dictionary
        dOut    = {
            "accuracy": lAccuracy,
            "fitness":  lFitness,
            "results":  lResults
        }

        #   STEP 23: Put output in queue
        _qTR.put([dOut])

        #   STEP 24: Set events
        _eTR.set()
        _eGlobal.set()

        #   STEP 25: Return
        return

    #
    #   endregion

    #   region Back-End: Mapping

    def __map_srgOverseer__(self, **kwargs) -> None:
        """
            Description:

                Maps the fittest surrogate as well as all the other surrogates
                whose fitness were within the required range
            
            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:

                + data  = ( vars ) A Data container containing the dataset to
                    be used during the mapping process
                    ~ Required
        """

        #   STEP 0: Local variables
        optimizer               = Hermione()

        self.vBest              = None
        self.vFitness           = np.inf

        fTmp_Fitness            = np.inf

        #   STEP 1: Setup - Local variables
        self.lMap_Results     = []
        self.lMap_Fitness     = []
        
        #   STEP 2: Check if data arg passed
        if ("data" not in kwargs):
            #   STEP 3: Error handling
            raise Exception("An error occured in Golem.__map_srgOverseer__() -> Step 2: No data arg passed")

        #   STEP 5: If optimizer output
        if (optimizer.bShowOutput):
            print("")

        else:
            print("\t{" + Helga.time() + "} - Starting surrogate mapping\t\t\t-> ", end="")

        try:

            #   STEP 6: Loop through surrogates
            for i in range(0, len(self.__lSRG)):
                #   STEP 7: Setup - Scope varibales
                dTmp_MapResults     = None

                #   STEP 8: Best candidate
                if (i == 0):
                    #   STEP 9: Outsource threaded mapping
                    dTmp_MapResults = optimizer.mapSurrogate(threading=False, data=kwargs["data"], surrogate=self.__lSRG[i])#, optimizer=ga.TRO)

                #   STEP 10: Else if accuracy = 100%
                elif (self.__lSRG_Accuracy[i] == 1.0):
                    #   STEP 11: Outsource mapping
                    dTmp_MapResults = optimizer.mapSurrogate(threading=False, data=kwargs["data"], surrogate=self.__lSRG[i])

                #   STPE 12: CHeck if there are results
                if (dTmp_MapResults != None):
                    #   STEP 13: Append to results
                    self.lMap_Results.append(dTmp_MapResults["result"])
                    self.lMap_Fitness.append(dTmp_MapResults["fitness"])

                    #   STEP 14: Check - Optimizer output status
                    if (optimizer.bShowOutput == False):
                        #   STEP 15: Check if new results are best
                        if (dTmp_MapResults["fitness"] < fTmp_Fitness):
                            #   STEP 16: Update - Local variables
                            fTmp_Fitness    = dTmp_MapResults["fitness"]

                            #   STEP 17: User output
                            print("!", end="")

                        #   STEP 18: Not new best
                        else:
                            #   STEP 19: User output
                            print(".", end="")

            #   STEP 14: Setup - Best results
            self.vBest      = self.lMap_Results[0]
            self.vFitness   = self.lMap_Fitness[0]

        except Exception as ex:
            print("Initial error: ", ex)
            print("An error occured in Golem.__map_srgOverseer__()")

        #   STEP 15: Return
        print("")
        return

    #
    #   endregion

    #   region Back-End: Threading
    
    def __threadUI__(self, _eGlobal_Exit, _eGlobal, _eUI, _qReturn) -> None:
        """
            Description:

                Run as Thread(). Gets input without blocking and returns via
                the passed mp.Queue()

            |\n
            |\n
            |\n
            |\n
            |\n

            Parameters:

                + _eGlobal_Exit  = ( mp.Event() ) Event signalling global exit
                    for threads and processes

                + _eGlobal  = ( mp.Event() ) Event signalling global action

                + eUI       = ( mp.Event() ) Event signalling input pushed to
                    the output mp.Queue

                + _qReturn  = ( mp.Queue() ) The queue onto which user input
                    should be returned
        """

        #   STEP 0: Local variables
        tBlocking           = None

        qBlocking           = mp.Queue()
        eBlocking           = mp.Event()

        #   STEP 1: Setup - Local variables
        eBlocking.clear()

        #   STEP 2: Setup - Threaded blocking ui
        tBlocking           = tr.Thread(target=self.__threadUI_Blocking__, args=(eBlocking, qBlocking, ) )
        tBlocking.daemon    = True
        tBlocking.start()

        #   STEP 3: Loop to infinity and beyond
        while (True):
            #   STEP 4: Check for global exit event
            if (_eGlobal_Exit.is_set()):
                #   STEP 5: Exit
                break

            #   STEP 6: Check for input from blocking thread
            if (eBlocking.is_set()):
                #   STEP 7:Clear event and pass input along
                eBlocking.clear()

                _qReturn.put( qBlocking.get() )

                #   STEP 8: Set UI event and global event
                _eUI.set()
                _eGlobal.set()

            #   STEP 9: Sleep
            t.sleep(0.1)

        #   STEP 20: Return
        return

    def __threadUI_Blocking__(self, _eUI, _qReturn) -> None:
        """
            Description:

                Run as Thread(). Gets blocking input and returns via the passed
                mp.Queue()

            |\n
            |\n
            |\n
            |\n
            |\n

            Parameters:

                + _eUI       = ( mp.Event() ) Event signalling input pushed to
                    the output mp.Queue

                + _qReturn  = ( mp.Queue() ) The queue onto which user input
                    should be returned
        """

        #   STEP 0: Local variables

        #   STEP 1: Setup - Local varibales

        #   STEP 2: Loop to infinity
        while (True):
            #   STEP 3: Check - _eUI status
            if (_eUI.is_set()):
                #   STEP 4: Wait for it to finish
                _eUI.wait()

            #   STEP 5: Get input
            sTmp_Input  = input()

            #   STEP 6: Push input to queue
            _qReturn.put([sTmp_Input])

            #   STEP 7: Set event
            _eUI.set()

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