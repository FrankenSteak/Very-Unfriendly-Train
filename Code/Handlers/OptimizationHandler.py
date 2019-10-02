#region Imports

from    enum                                import  Enum

import  copy                                as      cp
import  multiprocessing                     as      mp
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
global  elTrainingEvents
global  lTrainingResults

global  eMap_event_stopMapping
global  elMap_eventList_threadExit
global  lMap_list_results

global  eUI_event_exit
global  sUI_str_results

global  rlUO_rlock
global  slUO_strList_inputStrings

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
        bThreading              = False

        #   STEP 1: Setup - Local variables
        
        #   region STEP 2->5: Error checking

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

        #   region STEP 6->11: Setup - Local variables

        #   STEP 6: Check if threading arg passed
        if ("threading" in kwargs):
            #   STEP 7: Check threading status
            if (kwargs["threading"] == True):
                #   STEP 8: Update - Local variables
                bThreading  = True

        #   STEP 10: Check if optimizer arg passed
        if ("optimizer" in kwargs):
            #   STEP 11: Update - Local variables
            eOptimizer = kwargs["optimizer"]

        #
        #   endregion

        #   STEP 12: Check if optimizer is GA
        if (ga.isEnum(eOptimizer)):
            #   STEP 13: Check threading status
            if (bThreading):
                #   STEP 14: User output
                if (self.bShowOutput):
                    print("Hermione (map-srg) {" + Helga.time() + "} - Starting threaded surrogate mapping")

                #   STEP 15: Outsource and return
                return self.__mapSurrogate__(surrogate=kwargs["surrogate"], data=kwargs["data"], optimizer=eOptimizer)
            
            #   STEP 16: Not threaded
            else:
                #   STEP 17: User output
                if (self.bShowOutput):
                    print("Hermione (map-srg) {" + Helga.time() + "} - Starting surrogate mapping")

                #   STEP 18: Create new mapper
                spongebob   = SpongeBob()

                #   STEP 19: Outsource and return
                return spongebob.mapSurrogate(surrogate=kwargs["surrogate"], data=kwargs["data"], optimizer=eOptimizer)

        #   STEP 20: Check if optimizer is swarm
        elif (sw.isEnum(eOptimizer)):
            #   STPE 21: Check threading status
            if (bThreading):
                #   STEP 22: User output
                if (self.bShowOutput):
                    print("Hermione (map-srg) {" + Helga.time() + "} - Starting threaded surrogate mapping")
                
                #   STEP 23: Outsource and return
                return self.__mapSurrogate__(surrogate=kwargs["surrogate"], data=kwargs["data"], optimizer=eOptimizer)

            #   STEP 24: Not threaded
            else:
                #   STEP 25: User output
                if (self.bShowOutput):
                    print("Hermione (map-srg) {" + Helga.time() + "} - Starting surrogate mapping")

                #   STEP 26: Create new swarm handler
                sarah = Sarah()

                #   STEP 27: Outsource and return
                return sarah.mapSurrogate(surrogate=kwargs["surrogate"], data=kwargs["data"], optimizer=eOptimizer)
        
        #   STEP 29: Unidentified optimizer - Error handling
        print("Initial error: ", eOptimizer)
        raise Exception("An error occured in Natalie.mapSurrogate() -> Step 29: Unidentified optimizer")

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
        """

        #   STEP 0: Global variables
        global  eUI_event_exit
        global  sUI_str_results

        #   STEP 1: Local variables
        
        #   STEP 2: Check that the ui event is clear
        if (eUI_event_exit.is_set() == True):
            #   STEP 3: Wait for the event to clear
            eUI_event_exit.wait()
            
        #   STEP 4: Get user input
        sUI_str_results = input("")

        #   STEP 5: Check that the event hasn't been reset
        if (eUI_event_exit != None):
            eUI_event_exit.set()

        #   STEP 6: Return
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

                Resets the global variables used by this class' threading
                processes.
        """

        #   STEP 0: GLobal variables
        global  eStopTraining
        global  elTrainingEvents
        global  lTrainingResults

        global  eMap_event_stopMapping
        global  elMap_eventList_threadExit
        global  lMap_list_results

        global  eUI_event_exit
        global  sUI_str_results

        global  rlUO_rlock
        global  slUO_strList_inputStrings
        
        #   STEP 1: Clear globals
        eStopTraining               = None
        elTrainingEvents            = None
        lTrainingResults            = None

        eMap_event_stopMapping      = None
        elMap_eventList_threadExit  = None
        lMap_list_results           = None

        eUI_event_exit              = None
        sUI_str_results             = None

        #rlUO_rlock                  = None
        slUO_strList_inputStrings   = None

        #   STEP 2: Return
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
                    ~ Requried

            |\n

            Returns:

                + dOut  = ( dict ) A dictionary containing the optimized 
                    solution along with its fitness

            |\n

            ToDo:

                + Redo step numbering starting @ 6/7
                + threads can be list instead of tThread0, ...
        """

        #   STEP -1: Global variables
        global  eMap_event_stopMapping
        global  elMap_eventList_threadExit
        global  lMap_list_results

        global  eUI_event_exit
        global  sUI_str_results

        global  rlUO_rlock
        
        #   STEP 0: Local variables
        tThread0                = None
        tThread1                = None
        tThread2                = None
        tThread3                = None

        lResults                = []

        lMapping                = []

        fFittest                = np.inf
        iFittest                = -1

        iThread_ID              = 0
        iThread_Num             = 4

        #   STEP 1: Setup - Local variables

        #   region STEP 2->7: Error checking

        #   STEP 2: Check if data arg passed
        if ("data" not in kwargs):
            #   STEP 3: Error handling
            raise Exception("An error occured in Hermione.__mapSurrogate__() -> Step 2: No data arg passed")

        #   STEP 4: Check if surrogate arg passed
        if ("surrogate" not in kwargs):
            #   STEP 5: Error handling
            raise Exception("An error occured in Hermione.__mapSurrogate__() -> Step 4: No surrogate arg passed")
        
        #   STEP 6: Check if optimizer arg passed
        if ("optimizer" not in kwargs):
            #   STEP 7: Error handling
            raise Exception("An error occured in Hermione.__mapSurrogate__(): No optimizer arg passed")
        
        #
        #   endregion
        
        #   region STEP 6->10: Setup - Global variables

        #   STEP 6: Setup - Stop mapping event
        eMap_event_stopMapping  = mp.Event()
        eMap_event_stopMapping.clear()

        #   STEP 7: Setup - Mapping events
        lTmp    = []
        for _ in range(0, 4):
            lTmp.append(None)

        elMap_eventList_threadExit  = lTmp
        
        #   STEP 8: Setup - Mapping results
        lTmp    = []
        for _ in range(0, 4):
            lTmp.append(None)

        lMap_list_results       = lTmp

        #   STEP 9: Setup - UI variables
        eUI_event_exit          = mp.Event()
        eUI_event_exit.clear()

        sUI_str_results          = ""

        #   STEP 10: Setup - UO lock
        rlUO_rlock              = mp.RLock()

        #
        #   endregion

        #   region STEP 11->12: Setup - Local variables

        #   STEP 11: Setup - UI thread
        tTmp_ThreadUI   = tr.Thread(target=self.__getUI__)
        tTmp_ThreadUI.daemon = True

        tTmp_ThreadUI.start()

        #   STEP 12: Setup - Currently busy mapping list
        for _ in range(0, 4):
            lMapping.append(False)

        #
        #   endregion

        #   region 13->55: Mapping process
        
        #   STEP 13: Loop bish
        while (True):

            #   region STEP 14->36: Thread creation

            #   STEP 14: Loop through mapping events
            for i in range(0, len(elMap_eventList_threadExit)):
                #   STEP 15: Check if no event
                if (elMap_eventList_threadExit[i] == None):
                    #   STEP 16: Create a new event
                    eTmp_Event  = tr.Event()
                    eTmp_Event.clear()

                    #   STEP 17: Push to global
                    elMap_eventList_threadExit[i]  = eTmp_Event

                    #   STEP 18: Create tmp thread dictionary
                    dTmp_Thread = {
                        "surrogate":    cp.deepcopy(kwargs["surrogate"]),
                        "data":         cp.deepcopy(kwargs["data"]),
                        "optimizer":    kwargs["optimizer"],

                        "id":           iThread_ID,
                        "thread":       i
                    }

                    #   STEP 19: Create new thread
                    tTmp_Thread = tr.Thread(target=self.__mapThread__, args=(dTmp_Thread, ))
                    tTmp_Thread.daemon = True

                    #   STEP 20: Set thread var
                    if (i == 0):
                        tThread0    = tTmp_Thread

                    elif (i == 1):
                        tThread1    = tTmp_Thread

                    elif (i == 2):
                        tThread2    = tTmp_Thread

                    else:
                        tThread3    = tTmp_Thread

                    #   STPE 21: Start thread
                    tTmp_Thread.start()

                    #   STEP 22: Set mapping flag and increment thread id
                    iThread_ID      += 1
                    lMapping[i]     = True

                #   STEP 23: Event not None
                else:
                    #   STEP 24: Check if thread has exited
                    if (elMap_eventList_threadExit[i].is_set() == True):
                        #   STEP 25: Clear event
                        elMap_eventList_threadExit[i].clear()

                        #   STEP 26: Clear training flag
                        lMapping[i]         = False

                        #   STEP 27: Append data
                        lResults.append(lMap_list_results[i])

                        #   STEP 28: Clear results
                        lMap_list_results[i]  = None

                        #   STEP 29: Check if max thread reached
                        if (iThread_ID < iThread_Num):
                            #   STEP 30: Create tmp thread dictionary
                            dTmp_Thread = {
                                "surrogate":    cp.deepcopy(kwargs["surrogate"]),
                                "data":         cp.deepcopy(kwargs["data"]),
                                "optimizer":    kwargs["optimizer"],

                                "id":           iThread_ID,
                                "thread":       i
                            }

                            #   STEP 31: Create new thread
                            tTmp_Thread = tr.Thread(target=self.__mapThread__, args=(dTmp_Thread, ))
                            tTmp_Thread.daemon = True

                            #   STEP 32: Set thread var
                            if (i == 0):
                                tThread0    = tTmp_Thread

                            elif (i == 1):
                                tThread1    = tTmp_Thread

                            elif (i == 2):
                                tThread2    = tTmp_Thread

                            else:
                                tThread3    = tTmp_Thread

                            #   STEP 33: Start thread
                            tTmp_Thread.start()

                            #   STEP 34: Set training flag and increment thread id
                            iThread_ID      += 1
                            lMapping[i]     = True

            #   STEP 35: Check if max threads reached
            if (len(lResults) == iThread_ID):
                #   STEP 36: Exit loop
                break

            #
            #   endregion

            #   region STEP 39->55: UI supposrt

            #   STEP 39: Check if ui event occured
            if (eUI_event_exit.is_set() == True):
                #   STEP 40: Clear event
                eUI_event_exit.clear()

                #   STEP 41: Check if ui results == "exit"
                if (sUI_str_results == "exit"):
                    #   STEP 42: Set thread joining event
                    eMap_event_stopMapping.set()

                    #   STEP 43: Loop through mapping threads
                    for i in range(0, len(lMapping)):
                        #   STEP 44: Check if thread is still mapping
                        if (lMapping[i] == True):
                            #   STEP 45: Find thread and join
                            if (i == 0):
                                #   STEP 46: Join
                                tThread0.join()

                            elif (i == 1):
                                #   STEP 47: Join
                                tThread1.join()

                            elif (i == 2):
                                #   STEP 48: Join
                                tThread2.join()

                            else:
                                #   STEP 49: Join
                                tThread3.join()

                            #   STEP 50: Save results
                            lResults.append(lMap_list_results[i])

                    #   STEP 51: Clear thread join event
                    eMap_event_stopMapping.clear()

                    #   STEP 52: Exit loop
                    break
                
                #   STEP 53: UI input not "exit"
                else:
                    #   STEP 54: Create new ui thread
                    tTmp_ThreadUI = tr.Thread(target=self.__getUI__)
                    tTmp_ThreadUI.daemon = True

                    #   STEP 55: Start thread
                    tTmp_ThreadUI.start()

            #
            #   endregion

        #
        #   endregion

        #   STEP 56: Iterate through results
        for i in range(0, len(lResults)):
            #   STEP 57: Check if fitness less than current best
            if (lResults[i]["fitness"] < fFittest):
                #   STEP 58: Update - Local variables
                fFittest    = lResults[i]["fitness"]
                iFittest    = i

        #   STEP 59: Reset globals
        self.__resetGlobals__()

        """
        #   STEP 60: Check if ui thread alive
        if (tTmp_ThreadUI.is_alive()):
            #   STEP 61: Forcefully terminate
            tTmp_ThreadUI.terminate()
        """
        
        #   STEP 62: Return
        return lResults[iFittest]

    def __mapThread__(self, kwargs) -> dict:
        """
            Description:

                This function outsources the mapping of the surrogate to the
                appropriate optimization handler after picking the optimizer
                to use.

            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:

                + surrogate = ( vars ) The surrogate instance to map
                    ~ Required

                + data  = ( vars ) The data container containing the dataset
                    to be used during the mapping process
                    ~ Required

                + thread    = ( int ) The number of this thread
                    ~ Required

                + id    = ( int ) The ID of this thread
                    ~ Required

                + optimizer = ( enum ) The enum of the optimizer to use
                    ~ Required

            |\n

            Returns:

                + dOut  = ( dict )
                    ~ "result"  = ( list ) The list of surrogate inputs that
                        yielded the best results

                    ~ "fitness" = ( float ) The fitness of the best results
        """
        
        #   STEP -1: Global variables
        global  elMap_eventList_threadExit
        global  lMap_list_results

        #   STEP 0: Local variables
        dResults                = None

        iThread_ID              = Helga.ticks()
        iThread_AppID           = None

        iSwarms_Active          = 0
        iGA_Active              = 0

        iOptimizers_Active      = 0

        #   STEP 1: Setup - Local variables

        #   region STEP 2->11: Error checking

        #   STEP 2: Check if surrogate arg passed
        if ("surrogate" not in kwargs):
            #   STEP 3: Error handling
            raise Exception("An error occured in Natalie.__mapThread__() -> Step 2: No surrogate arg passed")

        #   STEP 4: Check if data arg passed
        if ("data" not in kwargs):
            #   STEP 5: Error handling
            raise Exception("An error occured in Natalie.__mapThread__() -> Step 4: No data arg passed")
        
        #   STEP 6: Check if thread arg passed
        if ("thread" not in kwargs):
            #   STEP 7: Error handglinr
            raise Exception("An error occured in Natalie.__mapThread__() -> Step 6: No thread arg passed")

        #   STEP 8: Check if id arg passed
        if ("id" not in kwargs):
            #   STEP 9: Error handling
            raise Exception("An error occured in Natalie.__mapThread__() -> Step 8: No id arg passed")

        #   STEP 10: Check if optimizer arg passed
        if ("optimizer" not in kwargs):
            #   STPE 11: Error handling
            raise Exception("An error occured in Natalie.__mapThread__() -> Step 10: No optimizer arg passed")
        
        #
        #   endregion
        
        #   STEP 12: Update - Local variables
        iThread_AppID   = kwargs["id"]

        #   region STEP 13->25: Map using provided optimizer

        #   STEP 13: Check if not random optimizer
        if (rn.random() > 0.3):
            #   STEP 14: Check if optimizer is GA
            if (ga.isEnum(kwargs["optimizer"])):
                #   STEP 15: User output
                if (self.bShowOutput):
                    #   STEP 16: Populate strings list for threaded output
                    lsTmp_Strings   = []
                    lsTmp_Strings.append("\t- Assigning SpongeBob to mapping")
                    lsTmp_Strings.append("\t- Optimizer: " + str(kwargs["optimizer"]))
                    lsTmp_Strings.append("\t- Thread ID: " + str(iThread_ID))
                    lsTmp_Strings.append("\t- Application Thread ID: " + str(iThread_AppID) + "\n")

                    #   STEP 17: Outsource output
                    self.__threadUO__(strings=lsTmp_Strings)

                #   STEP 18: Create new mapper
                sb          = SpongeBob()

                #   STEP 19: Outsource mapping
                dResults    = sb.mapSurrogate(surrogate=kwargs["surrogate"], data=kwargs["data"], optimizer=kwargs["optimizer"])

            #   STEP 20: Check if swarm
            if (sw.isEnum(kwargs["optimizer"])):
                #   STEP 21: User output
                if (self.bShowOutput):
                    #   STEP 22: Populate strings list for threaded output
                    lsTmp_Strings = []
                    lsTmp_Strings.append("\t- Assigning Sarah to mapping")
                    lsTmp_Strings.append("\t- Optimizer: " + str(kwargs["optimizer"]))
                    lsTmp_Strings.append("\t- Thread ID: " + str(iThread_ID))
                    lsTmp_Strings.append("\t- Application Thread ID: " + str(iThread_AppID) + "\n")

                    #   STEP 23: Outsoruce output
                    self.__threadUO__(strings=lsTmp_Strings)

                #   STEP 24: Create new mapper
                sh          = Sarah()

                #   STEP 25: Outsource mapping
                dResults    = sh.mapSurrogate(surrogate=kwargs["surrogate"], data=kwargs["data"], optimizer=kwargs["optimizer"])

        #
        #   endregion

        #   region 26->41: Map using random optimizer

        #   STEP 26: Using random optimizer for mapping
        else:
            #   STEP 27: Update - Local variables
            iSwarms_Active      = sw.getNumActiveSwarms()
            iGA_Active          = ga.getNumActiveGAs()

            iOptimizers_Active  = iSwarms_Active + iGA_Active

            #   STEP 28: Choose a random optimizer
            iTmp_Optimizer  = rn.randint(0, iOptimizers_Active - 1)

            #   STEP 29: Check if swarm:
            if (iTmp_Optimizer < iSwarms_Active):
                #   STEP 30: Get optimizer enum
                eTmp_Optimizer  = sw.getActiveSwarms()[iTmp_Optimizer]

                #   STEP 31: User output
                if (self.bShowOutput):
                    #   STEP 32: Populate output strings
                    lsTmp_Strings = []
                    lsTmp_Strings.append("\t- Assigning Sarah to training")
                    lsTmp_Strings.append("\t- Optimizer: " + str(eTmp_Optimizer))
                    lsTmp_Strings.append("\t- Thread ID: " + str(iThread_ID))
                    lsTmp_Strings.append("\t- Application Thread ID: " + str(iThread_AppID) + "\n")

                    #   STEP 33: Outsource output
                    self.__threadUO__(strings=lsTmp_Strings)

                #   STEP 34: Create new mapper
                sh          = Sarah()

                #   STEP 35: Outsource
                dResults    = sh.mapSurrogate(surrogate=kwargs["surrogate"], data=kwargs["data"], optimizer=eTmp_Optimizer)

            #   STEP 36: Then swarm
            else:
                #   STEP 37: Get optimizer enum
                eTmp_Optimizer  = ga.getActiveGAs()[iTmp_Optimizer - iSwarms_Active]

                #   STEP 38: User output
                if (self.bShowOutput):
                    #   STEP 39: Populate output strings
                    lsTmp_Strings   = []
                    lsTmp_Strings.append("\t- Assigning SpongeBob to training")
                    lsTmp_Strings.append("\t- Optimizer: " + str(eTmp_Optimizer))
                    lsTmp_Strings.append("\t- Thread ID: " + str(iThread_ID))
                    lsTmp_Strings.append("\t- Application Thread ID: " + str(iThread_AppID) + "\n")

                #   STEP 40: Create new mapper
                sb          = SpongeBob()

                #   STEP 41: Outsource mapping
                dResults    = sb.mapSurrogate(surrogate=kwargs["surrogate"], data=kwargs["data"], optimizer=eTmp_Optimizer)

        #
        #   endregion
        
        #   Step 42: User output
        if (self.bShowOutput):
            #   STEP 43: Create output strings
            lsTmp_Strings   = []
            lsTmp_Strings.append("\t\t\t\t\t- Thread: " + str(iThread_AppID) +  " - <" + str( round( 100.0 * dResults["fitness"], 3 ) ) + ">\n")

            #   STEP 44: Outsoruce output
            self.__threadUO__(strings=lsTmp_Strings)
        
        #   STEP 45: Set results
        lMap_list_results[iThread_AppID]    = dResults

        #   STEP 46: Set exit event
        elMap_eventList_threadExit[iThread_AppID].set()

        #   STEP 47: Return
        return

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

        global  eUI_event_exit
        global  sUI_str_results

        global  rlUO_rlock

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
        eUI_event_exit = tr.Event()
        eUI_event_exit.clear()

        #       STEP 2.5: Init ui results
        sUI_str_results = ""

        #       STEP 2.6: Init uo event
        rlUO_rlock = tr.RLock()

        #       STEP 2.7: Start ui thread
        tTmp_ThreadUI = tr.Thread(target=self.__getUI__)
        tTmp_ThreadUI.daemon = True

        tTmp_ThreadUI.start()

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
            if (eUI_event_exit.is_set() == True):
                #   STEP 30: Clear event
                eUI_event_exit.clear()

                #   STEP 31: Check if ui output == "stop"
                if (sUI_str_results == "stop"):
                    #   STEP 32: Set thread joining event
                    eUI_event_exit.set()

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
                    lTmp = tr.Thread(target=self.__getUI__)
                    lTmp.daemon = True

                    #   STEP !!: Start new thread
                    lTmp.daemon

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
        global  rlUO_rlock

        #   STEP 4: Check that global isn't None
        if (rlUO_rlock != None):
            #   STEP 5: Acquired the lock
            rlUO_rlock.acquire()
                
            #   STEP 6: Iterate throughs strings
            for i in range(0, len(lStrings)):
                print(lStrings[i])            

            #   STEP 7: Release the lock
            rlUO_rlock.release()

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

#
#endregion