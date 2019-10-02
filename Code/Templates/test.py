#region Imports

from    enum                                import  Enum
from    multiprocessing                     import  Process                 as  pr

import  copy                                as      cp
import  numpy                               as      np
import  os
import  random                              as      rn
import  sys
import  threading                           as      tr
import  time                                as      tm

sys.path.append(os.path.abspath("."))

from    Code.Enums.Enums                    import  Enums                   as  en
from    Code.Enums.GeneticAlgorithms        import  GeneticAlgorithms       as  ga
from    Code.Enums.Swarms                   import  Swarms                  as  sw

from    Code.Handlers.GAHandler             import  SpongeBob
from    Code.Handlers.SwarmHandler          import  Sarah

from    Helpers.Config                      import  Conny
from    Helpers.GeneralHelpers              import  Helga

#endregion

#region Globals

global  eStopTraining
global  eStopMapping

global  elTrainingEvents
global  lTrainingResults

global  elMappingEvents
global  lMappingResults

global  eUiEvent
global  sUiResults

global  eUoEvent
global  sUoEvent

#endregion

#region Class - Hermione

class Hermione:

    #region Init

    """
    """
    
    def __init__(self):

        #region STEP 0: Local variables

        self.__enum             = en.Hermione
        self.__cf               = Conny()
        self.__cf.load(self.__enum.value)

        #endregion

        #region STEP 1: Private variables

        self.__bAllowTesting        = self.__cf.data["parameters"]["allow testing"]

        #endregion

        #region STEP 2: Public variables

        self.bShowOutput            = self.__cf.data["parameters"]["show output"]

        #endregion

        #region STEP 3: Setup - Private variables

        #endregion

        #region STEP 4: Setup - Public variables

        #endregion
        
        return

    #
    #endregion

    #region Front-End

    #   region Front-End: Mapping

    def mapSurrogate(self, **kwargs) -> dict:
        """
            Description:

                Maps the passed surrogate using the passed dataset.

            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:

                + data  = ( vars ) A Data container instance containing the
                    dataset to be used for mapping
                    ~ Required

                + surrogate = ( vars ) A surrogate model to map
                    ~ Required

                + optimizer = ( enum ) The enum of the optimizer to be used
                    during the mapping process
                    ~ Default   = PSO

                + thread    = ( bool ) A flag that indicates if threading 
                    should be used to map the surrogate
                    ~ Default   = False
        """

        #   STEP 0: Local variables
        eOptimizer              = sw.PSO

        #   STEP 1: Setup - Local variables
        
        #   region STEP 2->??: Error checking

        #   STEP 2: Check if data arg passed
        if ("data" not in kwargs):
            #   STEP 3: Error handling
            raise Exception("An error occured in Hermione.mapSurrogate() -> Step 2: No data arg passed")

        #   STEP 4: Check if surrogate arg passed
        if ("surrogate" not in kwargs):
            #   STEP 5: Error handling
            raise Exception("An error occured in Hermion.mapSurrogate() -> Step 4: No surrogate arg passed")

        #
        #   endregion

        #   STEP 6: Check threading status
        if ("threading" in kwargs):
            #   STEP 7: Check if threading
            if (kwargs["threading"] == True):
                #   STEP 8: Check if optimizer specified
                if ("optimizer" in kwargs):
                    #   STEP 11: Outsource threading and return
                    return self.__mapSurrogate__(surrogate=kwargs["surrogate"], data=kwargs["data"], optimizer=kwargs["optimizer"])

                else:
                    #   STEP 12: Outsource do default threading and return
                    return self.__mapSurrogate__(surrogate=kwargs["surrogate"], data=kwargs["data"])

        #   STEP 13: Check if optimizer arg passed
        if ("optimzer" in kwargs):
            #   STEP 14: Update - Local variables
            eOptimizer = kwargs["optimizer"]

        #   STEP 15: Check if optimizer is GA
        if (ga.isEnum(eOptimizer)):
            #   STEP 16: User output
            if (self.bShowOutput):
                print("Hermione (map-srg) {" + Helga.time() + "} - Outsourcing surrogate mapping to SpongeBob")

            #   STEP 17: Create new spongebob
            sb  = SpongeBob()

            #   STEP 18: Outsource and return the Jedi
            return sb.mapSurrogate(surrogate=kwargs["surrogate"], data=kwargs["data"], optimizer=eOptimizer)

        #   STEP 19: Not GA, therefore swarm
        elif (sw.isEnum(eOptimizer)):
            #   STEP 20: User output
            if (self.bShowOutput):
                print("Hermione (map-srg) {" + Helga.time() + "} - Outsourcing surrogate mapping to Sarah")

            #   STEP 21: Create new swarm handler
            sarah = Sarah()

            #   STEP 22: Outsource and return
            return sarah.mapSurrogate(surrogate=kwargs["surrogate"], data=kwargs["data"], optimizer=eOptimizer)
            
        #   STEP ?23: Return
        return None

    #
    #   endregion

    #   region Front-End: Training

    def trainSurrogate(self, **kwargs) -> vars:
        """
            Description:
            
                Trains the passed surrogate using thread techniques if required to
                do so. If an optimizer is specified, only that optimizer will be used.
                However, if no optimizer is specified a random optimizer will be used. 

            |\n
            |\n
            |\n
            |\n
            |\n

            Args:

                + surrogate   = ( vars ) A surrogate class instance
                    ~ Required

                + data        = ( vars ) Data container
                    ~ Required

                + password    = ( int ) Surrogate pass
                    ~ Required

                + optimizer   = ( enum ) The enum of the optimizer to be used
                    ~ Default = { PSO }

                + threading   = ( bool ) Multi-treading flag
                    ~ Default = { False }

            |\n

            Returns:

                surrogate   = ( vars ) The trained surrogate

        """

        #   STEP 0: Local variables
        eOptimizer              = sw.PSO

        #   STEP 1: Setup - Local variables

        #   STEP 2: Check that a surrogate was passed
        if ("surrogate" not in kwargs):
            #   STEP 3: Error handling
            raise Exception("An error occured in Hermione.trainSurrogate() -> Step 2: No surrogate passed")

        #   STEP 4: Check that the data container was passed
        if ("data" not in kwargs):
            #   STEP 5: Error handling
            raise Exception("An error occured in Hermione.trainSurrogate() -> Step 4: Data container not passed")

        #   STEP 6: Check that the surrogate password was passed
        if ("password" not in kwargs):
            #   STEP 7: Error handling
            raise Exception("An error occured in Hermione.trainSurrogate() -> Step 4: Password associated with surrogate not passed")

        #   STEP 8: Check if threading was specified
        if ("threading" in kwargs):
            #   STEP 9: Check if threading enabled
            if (kwargs["threading"] == True):
                #   STEP 10: Check if optimizer specified
                if ("optimizer" in kwargs):
                    #   STEP 11: Outsource threading and return
                    return self.__trainSurrogate__(surrogate=kwargs["surrogate"], data=kwargs["data"], password=kwargs["password"], optimizer=kwargs["optimizer"])

                else:
                    #   STEP 12: Outsource threading and return
                    return self.__trainSurrogate__(surrogate=kwargs["surrogate"], data=kwargs["data"], password=kwargs["password"])

        #   STEP 13: Check if optimizer was specified
        if ("optimizer" in kwargs):
            #   STEP 14: Set optimizer
            eOptimizer = kwargs["optimizer"]

        #   STEP 15: Check if optimizer is GA
        if (ga.isEnum(eOptimizer)):
            #   STEP 16: User Output
            if (self.bShowOutput):
                print("Hermione (train-srg) {" + Helga.time() + "} - Outsourcing surrogate training to SpongeBob")

            #   STEP 17: Outsource training to spongebob
            sb = SpongeBob()
            
            #   STEP 18: Return of the jedi
            return sb.trainSurrogate(surrogate=kwargs["surrogate"], data=kwargs["data"], password=kwargs["password"], optimizer=eOptimizer)

        else:
            #   STEP 19: User Output
            if (self.bShowOutput):
                print("Hermione (train-srg) {" + Helga.time() + "} - Outsourcing surrogate training to Sarah")

            #   STEP 20: Outsource training to Sarah
            sarah = Sarah()

            #   STEP 21: Return of the jedi
            return sarah.trainSurrogate(surrogate=kwargs["surrogate"], data=kwargs["data"], password=kwargs["password"], optimizer=eOptimizer)
            
        #   STEP 22: Return
        return None

    #
    #   endregion

    #
    #endregion

    #region Back-End

    #   region Back-End: Gets

    def __getUI__(self) -> None:
        """
            Description:

                This function is used to get user input while a threading process is being
                executed by this class:

            |\n
            |\n
            |\n
            |\n
            |\n

            Returns:

                +   sInput      = ( str ) The input from the user
                    ~ Pushed to global variable, not returned directly
            
        """

        #   STEP 0: Global variables

        global  eUiEvent
        global  sUiResults

        #   STEP 1: Local variables
        
        #   STEP 4: Check that the ui event is clear
        if (eUiEvent.is_set() == True):
            #   STEP 5: Wait for the event to clear
            eUiEvent.wait()
            
        #   STEP 5: Get user input
        sUiResults = input("")

        #   STEP 7: Check that the event hasn't been reset
        if (eUiEvent != None):
            eUiEvent.set()

        #   STEP 8: Return
        return

    #
    #   endregion

    #   region Back-End: Sets
    
    #
    #   endregion

    #   region Back-End: Resets

    def __resetGlobals__(self) -> None:
        """
            Description:

                Resets the global variables used by this class' threading processes.

            |\n
            |\n
            |\n
            |\n
            |\n

        """

        #   STEP 0: GLobal variables

        global  eStopTraining

        global  elTrainingEvents
        global  lTrainingResults

        global  eUiEvent
        global  sUiResults

        #   STEP 1: Local variables
        #   STEP 2: Setup - Local variables
        #   STEP 3: Setup - Global variables

        #   STEP 4: Reset globals
        eStopTraining = None

        elTrainingEvents    = None
        lTrainingResults    = None

        eUiEvent            = None
        sUiResults          = None

        #   STEP 5: Return
        return

    #
    #   endregion

    #   region Back-End: Mapping

    def __mapSurrogate__(self, **kwargs) -> dict:
        """
            Description:
            
                Maps the passed surrogate using thread techniques. If an
                optimizer is specified, that surrogate will be more likely to
                be used during the threaded training process. However, if no
                optimizer is specified then all optimizers will have the same
                probability of being used. 

            |\n
            |\n
            |\n
            |\n
            |\n

            Args:

                + surrogate   = ( vars ) A surrogate class instance
                    ~ Required

                + data        = ( vars ) Data container
                    ~ Required
                    
                + optimizer   = ( enum ) The enum of the optimizer to be used
                    ~ Default = { Random }

            |\n

            Returns:

                + dOut  = ( dict ) A dictionary containing the optimized 
                    solution along with its fitness
        """

        #   STEP -1: Global variables
        global  eMap_Stop

        global  eMap_
        global  lMappingResults

        global  eUiEvent
        global  sUiResults

        global  eUoEvent
        
        #   STEP 0: Local variables
        tThread0                = None
        tThread1                = None
        tThread2                = None
        tThread3                = None

        lResults                = []

        lMapping                = []

        fFittest                = np.inf
        iFittest                = -1

        iThreadID               = 0
        iNumThreads             = 4

        #   STEP 1: Setup - Local variables

        #   region STEP 2->5: Error checking

        #   STEP 2: Check if data arg passed
        if ("data" not in kwargs):
            #   STEP 3: Error handling
            raise Exception("An error occured in Hermione.__mapSurrogate__() -> Step 2: No data arg passed")

        #   STEP 4: Check if surrogate arg passed
        if ("surrogate" not in kwargs):
            #   STEP 5: Error handling
            raise Exception("An error occured in Hermione.__mapSurrogate__() -> Step 2; No surrogate argpassed")

        #
        #   endregion
        
        #   region STEP 6->10: Setup - Global variables

        #   STEP 6: Setup - Stop mapping event
        eStopMapping    = tr.Event()
        eStopMapping.clear()

        #   STEP 7: Setup - UI variables
        eUiEvent        = tr.Event()
        eUiEvent.clear()

        sUiResults      = ""

        #   STEP 8: Setup - Mapping events
        lTmp    = []
        for _ in range(0, 4):
            lTmp.append(None)

        elMappingEvents = lTmp
        
        #   STEP 9: Setup - Mapping results
        lTmp    = []
        for _ in range(0, 4):
            lTmp.append(None)

        lMappingResults = lTmp

        #   STEP 10: Setup - UO lock
        eUoEvent        = tr.RLock()

        #
        #   endregion

        #   region STEP 11->12: Setup - Local variables

        #   STEP 11: Setup - UI thread
        tTmp_ThreadUI   = tr.Thread(target=self.__getUI__)
        tTmp_ThreadUI.daemon = True

        tTmp_ThreadUI.start()

        #   STEP 12: Setup - Training list
        for _ in range(0, 4):
            lMapping.append(False)

        #
        #   endregion

        #   STEP 13: User output
        if (self.bShowOutput):
            sTmp_Strings = ["Hermione (map-thread) {" + Helga.time() + "} - Starting threaded surrogate mapping\n"]
            self.__threadUO__(strings=sTmp_Strings)

        #   region 14->??: Mapping process
        
        #   STEP 14: Loop bish
        while (True):

            #   region STEP 15->40: Thread creation

            #   STEP 15: Loop through mapping events
            for i in range(0, len(elMappingEvents)):
                #   STEP 16: Check if no event
                if (elMappingEvents[i] == None):
                    #   STEP 17: Create a new event
                    eTmp_Event  = tr.Event()
                    eTmp_Event.clear()

                    #   STEP 18: Push to global
                    elMappingEvents[i]  = eTmp_Event

                    #   STEP 20: Create tmp thread dictionary
                    dTmp_Thread = {
                        "surrogate":    cp.deepcopy(kwargs["surrogate"]),
                        "data":         cp.deepcopy(kwargs["data"]),

                        "id":           iThreadID,
                        "thread":       i
                    }

                    #   STEP 21: Check if optimizer is specified
                    if ("optimizer" in kwargs):
                        #   STEP 22: Add to dictionary
                        dTmp_Thread["optimizer"] = kwargs["optimizer"]

                    #   STEP 23: Create new thread
                    tTmp_Thread = tr.Thread(target=self.__threadMap__, args=(dTmp_Thread, ))
                    tTmp_Thread.daemon = True

                    #   STEP 24: Set thread var
                    if (i == 0):
                        tThread0    = tTmp_Thread
                        tThread0.start()

                    elif (i == 1):
                        tThread1    = tTmp_Thread
                        tThread1.start()

                    elif (i == 2):
                        tThread2    = tTmp_Thread
                        tThread2.start()

                    else:
                        tThread3    = tTmp_Thread
                        tThread3.start()

                    #   STEP 25: Set training flag and increment thread id
                    iThreadID       += 1
                    lMapping[i]     = True

                #   STEP 26: Event not None
                else:
                    #   STEP 27: Check if thread has exited
                    if (elMappingEvents[i].is_set() == True):
                        #   STEP 28: Clear event
                        elMappingEvents[i].clear()

                        #   STEP 29: Clear training flag
                        lMapping[i]         = False

                        #   STEP 30: Append data
                        lResults.append(lMappingResults[i])

                        #   STEP 31: Clear results
                        lMappingResults[i]  = None

                        #   STEP 32: Check if max thread reached
                        if (iThreadID < iNumThreads):
                            #   STEP 33: Create tmp thread dictionary
                            dTmp_Thread = {
                                "surrogate":    cp.deepcopy(kwargs["surrogate"]),
                                "data":         cp.deepcopy(kwargs["data"]),

                                "id":           iThreadID,
                                "thread":       i
                            }

                            #   STEP 34: Check if optimizer is specified
                            if ("optimizer" in kwargs):
                                #   STEP 35: Add to dictionary
                                dTmp_Thread["optimizer"] = kwargs["optimizer"]

                            #   STEP 36: Create new thread
                            tTmp_Thread = tr.Thread(target=self.__threadMap__, args=(dTmp_Thread, ))
                            tTmp_Thread.daemon = True

                            #   STEP 37: Set thread var
                            if (i == 0):
                                tThread0    = tTmp_Thread
                                tThread0.start()

                            elif (i == 1):
                                tThread1    = tTmp_Thread
                                tThread1.start()

                            elif (i == 2):
                                tThread2    = tTmp_Thread
                                tThread2.start()

                            else:
                                tThread3    = tTmp_Thread
                                tThread3.start()

                            #   STEP 38: Set training flag and increment thread id
                            iThreadID       += 1
                            lMapping[i]     = True

            #   STEP 39: Check if max threads reached
            if (len(lResults) == iNumThreads):
                #   STEP 40: Exit loop
                break

            #
            #   endregion

            #   region STEP 41->??: UI supposrt

            #   STEP 41: Check if ui event occured
            if (eUiEvent.is_set() == True):
                #   STEP 42: Clear event
                eUiEvent.clear()

                #   STEP 43: Check if ui results == "exit"
                if (sUiResults == "exit"):
                    #   STEP 44: Set thread joining event
                    eStopMapping.set()

                    #   STEP 45: Loop through mapping threads
                    for i in range(0, len(lMapping)):
                        #   STEP 46: Check if thread is still mapping
                        if (lMapping[i] == True):
                            #   STEP 47: Find thread and join
                            if (i == 0):
                                #   STEP 48: Join
                                tThread0.join()

                            elif (i == 1):
                                #   STEP 49: Join
                                tThread1.join()

                            elif (i == 2):
                                #   STEP 50: Join
                                tThread2.join()

                            else:
                                #   STEP 51: Join
                                tThread3.join()

                            #   STEP 52: Save results
                            lResults.append(lMappingResults[i])

                    #   STEP 53: Clear thread join event
                    eStopMapping.clear()

                    #   STEP 54: Exit loop
                    break
                
                #   STEP 55: UI input not "exit"
                else:
                    #   STEP 56: Create new ui thread
                    lTmp = tr.Thread(target=self.__getUI__)
                    lTmp.daemon = True
            #
            #   endregion

        #
        #   endregion

        #   STEP ??: Return
        return {"result": None, "fitness": rn.random()}

    def __threadMap__(self, kwargs) -> dict:
        """
        """

        #   STEP 0: Local variables
        #   STEP 1: Setup - Local variables
        #   STEP 2: ??
        #   STEP ??: Return
        return {"result": None, "fitness": rn.random()}

    #
    #   endregion

    #   region Back-End: Training

    def __trainSurrogate__(self, **kwargs) -> vars:
        """
            Description:
            
                Trains the passed surrogate using thread techniques. If an optimizer is specified,
                that surrogate will be more likely to be used during the threaded training 
                process. However, if no optimizer is specified then all optimizers will have the 
                same probability of being used. 

            |\n
            |\n
            |\n
            |\n
            |\n

            Args:

                + surrogate   = ( vars ) A surrogate class instance
                    ~ Required
                + data        = ( vars ) Data container
                    ~ Required
                + password    = ( int ) Surrogate password
                    ~ Required
                + optimizer   = ( enum ) The enum of the optimizer to be used
                    ~ Default = { Random }

            |\n

            Returns:

                + surrogate   = ( vars ) The optimized surrogate instance
        """

        #   STEP 0: Global variables
        global  eStopTraining

        global  elTrainingEvents
        global  lTrainingResults

        global  eUiEvent
        global  sUiResults

        global  eUoEvent

        #   STEP 1: Local variables
        tThread0                    = None
        tThread1                    = None
        tThread2                    = None
        tThread3                    = None

        lResults                    = []

        lTraining                   = []

        fFittest                    = np.inf
        iFittest                    = -1

        iThreadID                   = 0
        iNumThreads                 = 16

        #   region STEP 2: Setup - Global variables

        #       STEP 2.1: Init training stop event
        eStopTraining = tr.Event()
        eStopTraining.clear()

        #       STEP 2.2: Init training events
        lTmp = []
        for _ in range(0, 4):
            lTmp.append(None)

        elTrainingEvents = lTmp

        #       STEP 2.3: Init training results
        lTmp = []
        for _ in range(0, 4):
            lTmp.append(None)

        lTrainingResults = lTmp

        #       STEP 2.4: Init ui event
        eUiEvent = tr.Event()
        eUiEvent.clear()

        #       STEP 2.5: Init ui results
        sUiResults = ""

        #       STEP 2.6: Init uo event
        eUoEvent = tr.RLock()

        #       STEP 2.7: Start ui thread
        tTmp_threadUI = tr.Thread(target=self.__getUI__)
        tTmp_threadUI.daemon = True

        tTmp_threadUI.start()

        #   endregion

        #   region STEP 3: Setup - Local variables
        
        for _ in range(0, 4):
            lTraining.append(False)

        #   endregion

        #   STEP !!: User Output
        if (self.bShowOutput):
            strings = ["Hermione (train-thread) {" + Helga.time() + "} - Starting threaded surrogate training.\n"]
            self.__threadUO__(strings=strings)

        #   region STEP 4->40: Training process

        #   STEP 4: Loop
        while (True):

            #   region STEP 5->28: Thread creation

            #   STEP 5: Iterate through training events
            for i in range(0, len(elTrainingEvents)):
                #   STEP 6: Check if event is currently None
                if (elTrainingEvents[i] == None):
                    #   STEP 7: Create a new event
                    eTmpEvent = tr.Event()
                    eTmpEvent.clear()

                    #   STEP 8: Push to global
                    elTrainingEvents[i] = eTmpEvent

                    #   STEP 9 : Create new thread dictionary
                    dTmp = {
                        "surrogate":    cp.deepcopy(kwargs["surrogate"]),
                        "data":         cp.deepcopy(kwargs["data"]),

                        "id":           iThreadID,
                        "password":     kwargs["password"],
                        "thread":       i
                    }

                    #   STEP 10: Check optimizer is specified
                    if ("optimizer" in kwargs):
                        #   STEP 11: Add to dictionary
                        dTmp["optimizer"] = kwargs["optimizer"]

                    #   STEP 12: Create new thread
                    tTmp = tr.Thread(target=self.__threadTrain__, args=(dTmp, ))
                    tTmp.daemon = True
                    
                    #   STEP 13: Set thread variable
                    if (i == 0):
                        tThread0 = tTmp
                        tThread0.start()

                    elif (i == 1):
                        tThread1 = tTmp
                        tThread1.start()

                    elif (i == 2):
                        tThread2 = tTmp
                        tThread2.start()

                    elif (i == 3):
                        tThread3 = tTmp
                        tThread3.start()

                    #   STEP 14: Set training flag and icnrement thread id
                    iThreadID       += 1
                    lTraining[i]    = True

                else:
                    #   STEP 15: Check if thread has exited
                    if (elTrainingEvents[i].is_set() == True):
                        #   STEP 16: Clear event
                        elTrainingEvents[i].clear()

                        #   STEP 17: Clear training flag
                        lTraining[i] = False

                        #   STEP 18: Append data
                        lResults.append(lTrainingResults[i])

                        #   STEP 19: Clear results
                        lTrainingResults[i] = None

                        #   STEP 20: Check if max threads not reached
                        if (iThreadID < iNumThreads):
                            #   STEP 21: Create new thread dictionary
                            dTmp = {
                                "surrogate":    cp.deepcopy(kwargs["surrogate"]),
                                "data":         cp.deepcopy(kwargs["data"]),

                                "id":           iThreadID,
                                "password":     kwargs["password"],
                                "thread":       i
                            }

                            #   STEP 22: Check if optimizer is specified
                            if ("optimizer" in kwargs):
                                #   STEP 23: Add to dictionary
                                dTmp["optimizer"] = kwargs["optimizer"]

                            #   STEP 24: Create a new thread
                            tTmp = tr.Thread(target=self.__threadTrain__, args=(dTmp, ))
                            tTmp.daemon = True

                            #   STEP 25: Set thread variable
                            if (i == 0):
                                tThread0 = tTmp
                                tThread0.start()

                            elif (i == 1):
                                tThread1 = tTmp
                                tThread1.start()

                            elif (i == 2):
                                tThread2 = tTmp
                                tThread2.start()

                            elif (i == 3):
                                tThread3 = tTmp
                                tThread3.start()

                            #   STEP 26: Set training flag and increment thread ID
                            iThreadID       += 1
                            lTraining[i]    = True

            #   STEP 27: Check if 16 threads reached
            if (len(lResults) == iNumThreads):
                #   STEP 28: Exit loop
                break

            #
            #   endregion

            #   region STEP 29->40: Ui support

            #   STEP 29: Check if ui thread is set
            if (eUiEvent.is_set() == True):
                #   STEP 30: Clear event
                eUiEvent.clear()

                #   STEP 31: Check if ui output == "stop"
                if (sUiResults == "stop"):
                    #   STEP 32: Set thread joining event
                    eStopTraining.set()

                    #   STEP 33: Loop through training threads
                    for i in range(0, len(lTraining)):
                        #   STEP 34: Check if thread is still training
                        if (lTraining[i] == True):
                            #   STEP 35: If first thread
                            if (i == 0):
                                tThread0.join()

                                lResults.append(lTrainingResults[i])

                            #   STEP 36: If second thread
                            elif (i == 1):
                                tThread1.join()

                                lResults.append(lTrainingResults[i])

                            #   STEP 37: If third thread
                            elif (i == 2):
                                tThread2.join()

                                lResults.append(lTrainingResults[i])

                            #   STEP 38: If fourth thread
                            elif (i == 3):
                                tThread3.join()

                                lResults.append(lTrainingResults[i])

                    #   STEP 39: Reset thread joining event
                    eStopTraining.clear()

                    #   STEP 40: Exit loop
                    break

                else:
                    #   STEP !!: Create new ui thread
                    tTmp_threadUI = mp.Process(target=self.__getUI__)
                    tTmp_threadUI.daemon = True

                    #   STEP !!: Start new thread
                    tTmp_threadUI.start()

            #
            #   endregion

        #
        #   endregion

        #   STEP 41: Iterate through results
        for i in range(0, len(lResults)):
            #   STEP 42: Check if fitter than current best
            if (lResults[i]["fitness"] < fFittest):
                #   STEP 43: Set new best candidate
                fFittest    = lResults[i]["fitness"]
                iFittest    = i

        #   STEP 44: Reset globals
        self.__resetGlobals__()

        #   STEP 45: Return
        return lResults[iFittest]

    def __threadTrain__(self, kwargs) -> dict:
        """
            Description:
            
                This fucntion outsources the training of the surrogate to the appropriate
                optimization handler after finding the optimizer to use.

            |\n
            |\n
            |\n
            |\n
            |\n

            Args:

                + surrogate = ( vars ) A surrogate class instance
                    ~ Required

                + data  = ( vars ) Data container
                    ~ Required
                    
                + password  = ( int ) Surrogate password
                    ~ Required

                + thread    = ( int ) The number of this thread
                    ~ Required
                
                + id    = ( int ) The ID of this thread
                    ~ Required
                
                + optimizer = ( enum ) The enum of the optimizer to be used

            |\n

            Returns:

                + dict        = ( dict )
                    ~ surrogate   = ( vars ) The trained surrogate
                    ~ fitness     = ( float ) The overall fitness of the trained surrogate
        """

        #   STEP 0: Global variables

        global  elTrainingEvents
        global  lTrainingResults

        #   STEP 1: Local variables
        data                    = None

        dResults                = None

        iThreadID               = tr.get_ident()
        iThreadID_App           = None

        iActiveSwarms           = 0
        iActiveGAs              = 0

        iActiveOptimizers       = 0

        #   STEP 2: Setup - Global variables
        #   STEP 3: Setup - Local variables

        #   region STEP 4->12: Error checking

        #   STEP 4: Check that surrogate was passed
        if ("surrogate" not in kwargs):
            #   STEP 5: Error handling
            raise Exception("An error occured in Hermione.__threadTrain__() -> Step 4: No surrogate passed")

        #   STEP 6: Check that the data container was passed
        if ("data" not in kwargs):
            #   STEP 7: Error handling
            raise Exception("An error occured in Hermione.__threadTrain__() -> Step 6: No data container passed")

        else:
            data = cp.deepcopy(kwargs["data"])

        #   STEP 8: Check that surrogate password passed
        if ("password" not in kwargs):
            #   STEP 9: Error handling
            raise Exception("An error occured in Hermione.__threadTrain__() -> Step 8: No surrogate password passed")

        #   STEP 10: Check that thread number was passed
        if ("thread" not in kwargs):
            #   STEP 11: Erro handling
            raise Exception("An error occured in Hermione.__threadTrain__() -> Step 10: No thread number passed")

        #   STEP 12: Check that thread ID was passed
        if ("id" not in kwargs):
            #   STEP 13: Error handling
            raise Exception("An error occured in Hermione.__threadTrain__() -> Step 12: No application thread ID passed")

        else:
            iThreadID_App = kwargs["id"]

        #
        #   endregion

        #   STEP 14: Check if optimizer specified
        if ("optimizer" in kwargs):
            #   STEP 15: Decide if passed optimizer should be used
            iTmp = rn.random()

            if (iTmp >= 0.5):
                #   STEP 16: Use the provided optimizer - Is ga?
                if (ga.isEnum(kwargs["optimizer"])):
                    #   STEP 17: User Output
                    if (self.bShowOutput):
                        strings = []
                        strings.append("\t- Assigning SpongeBob to training")
                        strings.append("\t- Optimizer: " + str(kwargs["optimizer"]))
                        strings.append("\t- Thread ID: " + str(iThreadID))
                        strings.append("\t- Application Thread ID: " + str(iThreadID_App) + "\n")

                        self.__threadUO__(strings=strings)

                    #   STEP 18: Outsource to spongebob
                    sb = SpongeBob()

                    dResults = sb.trainSurrogate(surrogate=kwargs["surrogate"], data=data, password=kwargs["password"], optimizer=kwargs["optimizer"])

                else:
                    #   STEP 19: User Output
                    if (self.bShowOutput):
                        strings = []
                        strings.append("\t- Assigning Sarah to training")
                        strings.append("\t- Optimizer: " + str(kwargs["optimizer"]))
                        strings.append("\t- Thread ID: " + str(iThreadID))
                        strings.append("\t- Application Thread ID: " + str(iThreadID_App) + "\n")

                        self.__threadUO__(strings=strings)

                    #   STEP 20: Outsource to sarah
                    sarah = Sarah()

                    dResults = sarah.trainSurrogate(surrogate=kwargs["surrogate"], data=data, password=kwargs["password"], optimizer=kwargs["optimizer"])

        #   STEP 19: Check if training hasn't occured
        if (dResults == None):
            #   STEP 20: Get the number of active optimizers
            iActiveSwarms = sw.getNumActiveSwarms()
            iActiveGAs = ga.getNumActiveGAs()

            iActiveOptimizers = iActiveSwarms + iActiveGAs

            #   STEP 21: Random a handler
            iTmp = rn.randint(0, iActiveOptimizers - 1)

            #   STEP 22: if swarm
            if (iTmp < sw.getNumActiveSwarms()):
                #   STEP 23: Get new swarm enum
                eTmpOptimizer = sw.getActiveSwarms()[iTmp]

                #   STEP 24: User Output
                if (self.bShowOutput):
                    strings = []
                    strings.append("\t- Assigning Sarah to training")
                    strings.append("\t- Optimizer: " + str(eTmpOptimizer))
                    strings.append("\t- Thread ID: " + str(iThreadID))
                    strings.append("\t- Application Thread ID: " + str(iThreadID_App) + "\n")

                    self.__threadUO__(strings=strings)

                #   STEP 25: Outsource to Sarah
                sarah = Sarah()

                dResults = sarah.trainSurrogate(surrogate=kwargs["surrogate"], data=data, password=kwargs["password"], optimizer=eTmpOptimizer)

            else:
                #   STEP 26: Get new ga enum
                eTmpOptimizer = ga.getActiveGAs()[iTmp - iActiveSwarms]

                #   STEP 27: User Output
                if (self.bShowOutput):
                    strings = []
                    strings.append("\t- Assigning SpongeBob to training")
                    strings.append("\t- Optimizer: " + str(eTmpOptimizer))
                    strings.append("\t- Thread ID: " + str(iThreadID))
                    strings.append("\t- Application Thread ID: " + str(iThreadID_App) + "\n")

                    self.__threadUO__(strings=strings)

                #   STEP 28: Outsource to SpongeBob
                sb = SpongeBob()

                dResults = sb.trainSurrogate(surrogate=kwargs["surrogate"], data=data, password=kwargs["password"], optimizer=eTmpOptimizer)
                
        #   STEP 29: Get surrogate fitness
        fTmpFitness = dResults["surrogate"].getAFitness(data=kwargs["data"])
        fTmpFitness = fTmpFitness * dResults["inverse accuracy"]
        
        #   STEP 30: User Output
        if (self.bShowOutput):
            strings = []
            strings.append("\t\t\t\t\t- Thread: " + str(iThreadID_App) +  " - <" + str(dResults["accuracy"]) + "  :  " + str(round(fTmpFitness, 2)) + ">\n")

            self.__threadUO__(strings=strings)
        
        #   STEP 31: Populate output dictionary
        dOut = {
            "accuracy":     dResults["accuracy"],
            "algorithm":    dResults["algorithm"],
            "fitness":      fTmpFitness,
            "iterations":   dResults["iterations"],
            "inverse accuracy": dResults["inverse accuracy"],
            "scalar":       dResults["scalar"],
            "surrogate":    dResults["surrogate"]
        }

        #   STEP 32: Set training results
        lTrainingResults[kwargs["thread"]] = dOut

        #   STEP 33: Set training finished result
        elTrainingEvents[kwargs["thread"]].set()

        #   STEP 34: Return
        return

    #
    #   endregion

    #   region Back-End: Other

    def __threadUO__(self, **kwargs) -> None:
        """
            Description:

                Uses a thread for the __userOutput__ function instead of
                waiting for it to finish.

            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:

                + strings   = ( list ) List of strings to print

        """

        #   STEP 0: Local variables
        tTmpThread              = None

        #   STEP 1: Setup - Local variables

        #   STEP 2: Check that strings were passed
        if ("strings" not in kwargs):
            #   STEP 3: Error handling
            raise Exception("An error occured in Hermione.__threadUO__() -> Step 2: No strings passed")

        #   STEP 4: Create thread
        tTmpThread = tr.Thread(target=self.__userOutput__, args=(kwargs["strings"], ))
        tTmpThread.daemon = True

        #   STEP 5: Start thread
        tTmpThread.start()

        #   STEP 6: Return
        return

    def __userOutput__(self, lStrings: list) -> None:
        """
        """

        #   STEP 0: Global varialbes

        global  eUoEvent

        #   STEP 1: Local variables
        #   STEP 2: Setup - Global variables
        #   STEP 3: Setup - Local variables

        #   STEP 4: Check that global isn't None
        if (eUoEvent != None):
            #   STEP 5: Acquired the lock
            eUoEvent.acquire()
                
            #   STEP 6: Iterate throughs strings
            for i in range(0, len(lStrings)):
                print(lStrings[i])            

            #   STEP 7: Release the lock
            eUoEvent.release()

        else:
            #   STEP 8: Iterate through strings
            for i in range(0, len(lStrings)):
                print(lStrings[i])

        #   STEP 9: Return
        return

    #
    #   endregion

    #
    #endregion

#
#endregion

#region Testing