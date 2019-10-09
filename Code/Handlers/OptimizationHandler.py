#region Imports

from    enum                                import  Enum

import  copy                                as      cp
import  multiprocessing                     as      mp
import  numpy                               as      np
import  os
import  random                              as      rn
import  sys
import  threading                           as      tr
import  time                                as      t

sys.path.append(os.path.abspath("."))

from    Code.Enums.Enums                    import  Enums                   as  en
from    Code.Enums.GeneticAlgorithms        import  GeneticAlgorithms       as  ga
from    Code.Enums.Swarms                   import  Swarms                  as  sw

from    Code.Handlers.GAHandler             import  SpongeBob
from    Code.Handlers.SwarmHandler          import  Sarah

from    Helpers.Config                      import  Conny
from    Helpers.GeneralHelpers              import  Helga

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
                    ~ Default = PSO

                + threading   = ( bool ) Multi-treading flag
                    ~ Default = False

            |\n

            Returns:

                surrogate   = ( vars ) The trained surrogate

        """

        #   STEP 0: Local variables
        eOptimizer              = sw.PSO
        bThreading              = False

        #   STEP 1: Setup - Local variables

        #   region STEP 2->7: Error checking

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

        #
        #   endregion
        
        #   region STEP 8->12: Setup - Local variables

        #   STEP 8: Check if threading was specified
        if ("threading" in kwargs):
            #   STEP 9: Check if threading enabled
            if (kwargs["threading"] == True):
                #   STEP 10: Update - Local variables
                bThreading  = True

        #   STEP 11: Check if optimizer was specified
        if ("optimizer" in kwargs):
            #   STEP 12: Set optimizer
            eOptimizer = kwargs["optimizer"]

        #
        #   endregion

        #   STEP 13: Check if optimizer is GA
        if (ga.isEnum(eOptimizer)):
            #   STEP 14: Check - Threading status
            if (bThreading):
                #   STEP 15: User output
                if (self.bShowOutput):
                    print("Hermione (train-srg) {" + Helga.time() + "} - Starting threaded surrogate training")

                #   STEP 16: Outsource and return
                return self.__trainSurrogate__(surrogate=kwargs["surrogate"], data=kwargs["data"], password=kwargs["password"], optimizer=eOptimizer)

            #   STEP 17: Not threaded
            else:
                #   STEP 18: User output
                if (self.bShowOutput):
                    print("Hermione (train-srg) {" + Helga.time() + "} - Starting surrogate training")

                #   STEP 19: Create new optimizer
                sb      = SpongeBob()

                #   STEP 20: Outsource and return
                return sb.trainSurrogate(surrogate=kwargs["surrogate"], data=kwargs["data"], password=kwargs["password"], optimizer=eOptimizer)

        #   STEP 21: Check if optimizer is swarm
        if (sw.isEnum(eOptimizer)):
            #   STEP 22: Check - Threading status
            if (bThreading):
                #   STEP 23: User output
                if (self.bShowOutput):
                    print("Hermione (train-srg) {" + Helga.time() + "} - Starting threaded surrogate training")

                #   STEP 24: Outsouce and return
                return self.__trainSurrogate__(surrogate=kwargs["surrogate"], data=kwargs["data"], password=kwargs["password"], optimizer=eOptimizer)

            #   STEP 25: Not threaded
            else:
                #   STEP 26: User output
                if (self.bShowOutput):
                    print("Hermione (train-srg) {" + Helga.time() + "} - Starting surrogate training")

                #   STEP 27: Create new optimizer
                sarah       = Sarah()

                #   STEP 28: Outsource and return
                return sarah.trainSurrogate(surrogate=kwargs["surrogate"], data=kwargs["data"], password=kwargs["optimizer"], optimizer=eOptimizer)

        #   STEP 29: Unidentified optimizer - Error handling
        print("Initial error: ", eOptimizer)
        raise Exception("An error occured in Natalie.trainSurrogate() -> Step 29: Unidentified optimizer")

    #
    #   endregion

    #
    #endregion

    #region Back-End

    #   region Back-End: Gets

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
            t.sleep(0.35)

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

    #
    #   endregion

    #   region Back-End: Sets
    
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
        
        #   STEP 0: Local variables
        eGlobal                 = None
        eGlobal_Exit            = None

        eUI_Event               = None
        qUI_Queue               = None
        tUI_Thread              = None

        lUO_Lock                = None

        lThread_Data            = []
        lThread_Results         = []
        iThread                 = 8
        iThread_ID              = 0

        fFittest                = np.inf
        iFittest                = 0

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
        
        #   region STEP 8->10: Setup - Local variables

        #   STEP 8: Setup - Global variables
        eGlobal                 = mp.Event()
        eGlobal.clear()

        eGlobal_Exit            = mp.Event()
        eGlobal_Exit.clear()

        #   STEP 9: Setup - UI thread
        eUI_Event               = mp.Event()
        qUI_Queue               = mp.Queue()

        tUI_Thread              = tr.Thread(target=self.__threadUI__, args=(eGlobal_Exit, eGlobal, eUI_Event, qUI_Queue, ))
        tUI_Thread.daemon       = True
        #tUI_Thread.start()

        lUO_Lock                = mp.RLock()

        #   STEP 10: Setup - Thread data list
        for _ in range(0, 4):
            lThread_Data.append(None)

        #
        #   endregion

        #   region 11->55: Mapping process
        
        #   STEP 11: Loop bish
        while (True):

            #   region STEP 12->31: Thread creation

            #   STEP 12: Loop through mapping events
            for i in range(0, len(lThread_Data)):
                #   STEP 13: Check if no event
                if (lThread_Data[i] == None):
                    #   STEP 14: Create a new event
                    eTmp_Event          = mp.Event()
                    eTmp_Event.clear()

                    #   STEP 15: Create tmp thread dictionary
                    dTmp_Thread = {
                        "surrogate":    cp.deepcopy(kwargs["surrogate"]),
                        "data":         cp.deepcopy(kwargs["data"]),
                        "optimizer":    kwargs["optimizer"],

                        "id":           iThread_ID,
                        "thread":       i
                    }

                    #   STEP 16: Create a new queue
                    qTmp_Queue          = mp.Queue()
                    qTmp_Queue.put([dTmp_Thread])

                    #   STEP 17: Create new process
                    tTmp_Thread         = mp.Process(target=self.__threadMap__, args=(eGlobal_Exit, eTmp_Event, qTmp_Queue, lUO_Lock, ) )
                    tTmp_Thread.daemon  = True
                    tTmp_Thread.start()

                    #   STEP 18: Set thread var
                    lThread_Data[i] = [tTmp_Thread, eTmp_Event, qTmp_Queue]

                    #   STEP 19: Increment thread id
                    iThread_ID      += 1

                #   STEP 20: Event not None
                else:
                    #   STEP 21: Check if thread has exited
                    if (lThread_Data[i][1].is_set() == True):
                        #   STEP 22: Clear event
                        lThread_Data[i][1].clear()

                        #   STEP 23: Append data
                        lThread_Results.append( lThread_Data[i][2].get()[0] )

                        #   STEP 24: Check if max thread reached
                        if (iThread_ID < iThread):
                            #   STEP 25: Create tmp thread dictionary
                            dTmp_Thread = {
                                "surrogate":    cp.deepcopy(kwargs["surrogate"]),
                                "data":         cp.deepcopy(kwargs["data"]),
                                "optimizer":    kwargs["optimizer"],

                                "id":           iThread_ID,
                                "thread":       i
                            }

                            #   STEP 26: Update input queue
                            lThread_Data[i][2].put( [dTmp_Thread] )

                            #   STEP 27: Create new thread
                            tTmp_Thread         = mp.Process(target=self.__threadMap__, args=(eGlobal_Exit, lThread_Data[i][1], lThread_Data[i][2], lUO_Lock ) )
                            tTmp_Thread.daemon  = True
                            tTmp_Thread.start()

                            #   STEP 28: Set thread var
                            lThread_Data[i][0]  = tTmp_Thread

                            #   STEP 29: Set training flag and increment thread id
                            iThread_ID      += 1

            #   STEP 30: Check if max threads reached
            if ( len( lThread_Results ) == iThread ):
                #   STEP 31: Exit loop
                break

            #
            #   endregion

            #   region STEP 32->41: UI supposrt

            #   STEP 32: Check if ui event occured
            if (eUI_Event.is_set() == True):
                #   STEP 33: Clear event
                eUI_Event.clear()

                #   STEP 34: Check if ui results == "exit"
                if (qUI_Queue.get()[0] == "exit"):
                    #   STEP 35: Set thread joining event
                    eGlobal_Exit.set()
                    #tUI_Thread.join()

                    #   STEP 36: Loop through mapping threads
                    for i in range(0, len(lThread_Data)):
                        #   STEP 37: Check if thread is still mapping
                        if (lThread_Data[i][0].is_alive() == True):
                            #   STEP 38: Find thread and join
                            lThread_Data[i][0].join()

                            #   STEP 39: Save results
                            lThread_Results.append( lThread_Data[i][2].get()[0] )

                    #   STEP 40: Clear thread join event
                    eGlobal_Exit.clear()

                    #   STEP 41: Exit loop
                    break

            #
            #   endregion

        #
        #   endregion

        #   STEP 42: Iterate through results
        for i in range(0, len(lThread_Results)):
            #   STEP 43: Check if fitness less than current best
            if (lThread_Results[i]["fitness"] < fFittest):
                #   STEP 44: Update - Local variables
                fFittest    = lThread_Results[i]["fitness"]
                iFittest    = i
        
        #   STEP 45: Return
        return lThread_Results[iFittest]

    def __threadMap__(self, _eExit, _eTr, _qTr, _lUO) -> None:
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

            Parameters:

                + _eGlobal_Exit  = ( mp.Event() ) Event signalling global exit
                    for threads and processes

                + _eTr      = ( mp.Event() ) Event signalling process
                    completion

                + _qTr      = ( mp.Queue() ) The queue onto which the process
                    results should be returned

                + _lUO      = ( mp.RLock() ) The lock for commong user output

            |\n

            Returns:

                + dOut  = ( dict )
                    ~ "result"  = ( list ) The list of surrogate inputs that
                        yielded the best results

                    ~ "fitness" = ( float ) The fitness of the best results
        """
        
        #   STEP 0: Local variables
        dArgs                   = _qTr.get()[0]
        dResults                = None

        iThread_ID              = Helga.ticks()
        iThread_AppID           = dArgs["thread"]

        iSwarms_Active          = 0
        iGA_Active              = 0

        iOptimizers_Active      = 0

        #   region STEP 1->15: Map using provided optimizer

        #   STEP 1: Check if not random optimizer
        if (rn.uniform(0.0, 1.0) > 0.3):
            #   STEP 2: Check if optimizer is GA
            if (ga.isEnum(dArgs["optimizer"])):
                #   STEP 3: User output
                if (self.bShowOutput):
                    #   STEP 4: Get lock
                    _lUO.acquire()

                    #   STEP 5: Populate strings list for threaded output
                    print("\t- Assigning SpongeBob to mapping")
                    print("\t- Optimizer: " + str(dArgs["optimizer"]))
                    print("\t- Thread ID: " + str(iThread_ID))
                    print("\t- Application Thread ID: " + str(iThread_AppID))
                    print("\t- Time: " + Helga.time() + "\n")

                    #   STEP 6: Release lock
                    _lUO.release()

                #   STEP 7: Create new mapper
                sb          = SpongeBob()

                #   STEP 8: Outsource mapping
                dResults    = sb.mapSurrogate(surrogate=dArgs["surrogate"], data=dArgs["data"], optimizer=dArgs["optimizer"])

            #   STEP 9: Check if swarm
            if (sw.isEnum(dArgs["optimizer"])):
                #   STEP 10: User output
                if (self.bShowOutput):
                    #   STEP 11: Get lock
                    _lUO.acquire()

                    #   STEP 12: Populate strings list for threaded output
                    print("\t- Assigning Sarah to mapping")
                    print("\t- Optimizer: " + str(dArgs["optimizer"]))
                    print("\t- Thread ID: " + str(iThread_ID))
                    print("\t- Application Thread ID: " + str(iThread_AppID))
                    print("\t- Time: " + Helga.time() + "\n")

                    #   STEP 13: Release lock
                    _lUO.release()

                #   STEP 14: Create new mapper
                sh          = Sarah()

                #   STEP 15: Outsource mapping
                dResults    = sh.mapSurrogate(surrogate=dArgs["surrogate"], data=dArgs["data"], optimizer=dArgs["optimizer"])

        #
        #   endregion

        #   region STEP 16->34: Map using random optimizer

        #   STEP 16: Using random optimizer for mapping
        else:
            #   STEP 17: Update - Local variables
            iSwarms_Active      = sw.getNumActiveSwarms()
            iGA_Active          = ga.getNumActiveGAs()

            iOptimizers_Active  = iSwarms_Active + iGA_Active

            #   STEP 18: Choose a random optimizer
            iTmp_Optimizer  = rn.randint(0, iOptimizers_Active - 1)

            #   STEP 19: Check if swarm:
            if (iTmp_Optimizer < iSwarms_Active):
                #   STEP 20: Get optimizer enum
                eTmp_Optimizer  = sw.getActiveSwarms()[iTmp_Optimizer]

                #   STEP 21: User output
                if (self.bShowOutput):
                    #   STPE 22: Acquire lock
                    _lUO.acquire()

                    #   STEP 23: Populate output strings
                    print("\t- Assigning Sarah to training")
                    print("\t- Optimizer: " + str(eTmp_Optimizer))
                    print("\t- Thread ID: " + str(iThread_ID))
                    print("\t- Application Thread ID: " + str(iThread_AppID))
                    print("\t- Time: " + Helga.time() + "\n")

                    #   STEP 24: Release lock
                    _lUO.release()

                #   STEP 25: Create new mapper
                sh          = Sarah()

                #   STEP 26: Outsource
                dResults    = sh.mapSurrogate(surrogate=dArgs["surrogate"], data=dArgs["data"], optimizer=eTmp_Optimizer)

            #   STEP 27: Then ga
            else:
                #   STEP 28: Get optimizer enum
                eTmp_Optimizer  = ga.getActiveGAs()[iTmp_Optimizer - iSwarms_Active]

                #   STEP 29: User output
                if (self.bShowOutput):
                    #   STEP 30: Acquired lock
                    _lUO.acquire()

                    #   STEP 31: Populate output strings
                    print("\t- Assigning SpongeBob to training")
                    print("\t- Optimizer: " + str(eTmp_Optimizer))
                    print("\t- Thread ID: " + str(iThread_ID))
                    print("\t- Application Thread ID: " + str(iThread_AppID))
                    print("\t- Time: " + Helga.time() + "\n")

                    #   STEP 32: Release lock
                    _lUO.release()

                #   STEP 33: Create new mapper
                sb          = SpongeBob()

                #   STEP 34: Outsource mapping
                dResults    = sb.mapSurrogate(surrogate=dArgs["surrogate"], data=dArgs["data"], optimizer=eTmp_Optimizer)

        #
        #   endregion
        
        #   Step 35: User output
        if (self.bShowOutput):
            #   STEP 36: Get lock
            _lUO.acquire()

            #   STEP 37: Create output strings
            print("\t\t\t\t\t- Thread: " + str(iThread_AppID) +  " - <" + str( round( 100.0 * dResults["fitness"], 3 ) ) + ">\n")

            #   STEP 38: Release lock
            _lUO.release()
        
        #   STEP 39: Set results
        _qTr.put([dResults])
        
        #   STEP 40: Set exit event
        _eTr.set()

        #   STEP 41: Return
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
        
        #   STEP 0: Local variables
        eGlobal                 = None
        eGlobal_Exit            = None

        eUI_Event               = None
        qUI_Queue               = None
        tUI_Thread              = None

        lUO_Lock                = None

        lThread_Data            = []
        lThread_Results         = []
        iThread                 = 8
        iThread_ID              = 0

        fFittest                = np.inf
        iFittest                = 0

        #   STEP 1: Setup - Local variables

        #   region STEP 2->9: Error checking

        #   STEP 2: Check if data arg passed
        if ("data" not in kwargs):
            #   STEP 3: Error handling
            raise Exception("An error occured in Hermione.__trainSurrogate__() -> Step 2: No data arg passed")

        #   STEP 4: Check if surrogate arg passed
        if ("surrogate" not in kwargs):
            #   STEP 5: Error handling
            raise Exception("An error occured in Hermione.__trainSurrogate__() -> Step 4: No surrogate arg passed")
        
        #   STEP 6: Check if optimizer arg passed
        if ("optimizer" not in kwargs):
            #   STEP 7: Error handling
            raise Exception("An error occured in Hermione.__trainSurrogate__() -> Step 6: No optimizer arg passed")
        
        #   STEP 8: Check if password arg passed
        if ("password" not in kwargs):
            #   STEP 9: Error handling
            raise Exception("An error occured in Hermione.__trainSurrogate__() -> Step 8: No password arg passed")
        
        #
        #   endregion

        #   region STEP 10->12: Setup - Global variables

        #   STEP 10: Setup - Global variables
        eGlobal                 = mp.Event()
        eGlobal.clear()

        eGlobal_Exit            = mp.Event()
        eGlobal_Exit.clear()

        #   STEP 11: Setup - UI Thread
        eUI_Event               = mp.Event()
        qUI_Queue               = mp.Queue()

        tUI_Thread              = tr.Thread(target=self.__threadUI__, args=(eGlobal_Exit, eGlobal, eUI_Event, qUI_Queue, ))
        tUI_Thread.daemon       = True
        #tUI_Thread.start()

        lUO_Lock                = mp.RLock()

        #   STEP 12: Setup - Thread data list
        for _ in range(0, 4):
            lThread_Data.append(None)

        #
        #   endregion

        #   STEP 13: User output
        if (self.bShowOutput):
            #   STEP 14: Acquire lock
            lUO_Lock.acquire()

            #   STEP 15: print
            print("Hermione (train-thread) {" + Helga.time() + "} - Starting threaded surrogate training.\n")

            #   STEP 16: Release
            lUO_Lock.release()

        #   region STEP 17->46: Training process

        #   STEP 17: Loop bish
        while (True):

            #   region STEP 18->36: Thread creation

            #   STEP 18: Iterate through training events
            for i in range(0, len(lThread_Data)):
                #   STEP 19: Check if event is currently None
                if (lThread_Data[i] == None):
                    #   STEP 20: Create a new event
                    eTmp_Event          = mp.Event()
                    eTmp_Event.clear()

                    #   STEP 21: Create new thread dictionary
                    dTmp_Thread = {
                        "surrogate":    cp.deepcopy(kwargs["surrogate"]),
                        "data":         cp.deepcopy(kwargs["data"]),
                        "optimizer":    kwargs["optimizer"],

                        "id":           iThread_ID,
                        "password":     kwargs["password"],
                        "thread":       i
                    }

                    #   STEP 22: Create a new queue
                    qTmp_Queue          = mp.Queue()
                    qTmp_Queue.put([dTmp_Thread])
                    
                    #   STEP 23: Create new thread
                    tTmp_Thread         = mp.Process(target=self.__threadTrain__, args=(eGlobal_Exit, eTmp_Event, qTmp_Queue, lUO_Lock, ))
                    tTmp_Thread.daemon  = True
                    tTmp_Thread.start()
                    
                    #   STEP 24: Set thread variable
                    lThread_Data[i]     = [tTmp_Thread, eTmp_Event, qTmp_Queue]

                    #   STEP 25: Set training flag and icnrement thread id
                    iThread_ID          += 1

                #   STEP 26: Event not None
                else:
                    #   STEP 27: Check if thread has exited
                    if (lThread_Data[i][1].is_set() == True):
                        #   STEP 28: Clear event
                        lThread_Data[i][1].clear()

                        #   STEP 29: Append data
                        lThread_Results.append( lThread_Data[i][2].get()[0] )

                        #   STEP 30: Check if max threads not reached
                        if (iThread_ID < iThread):
                            #   STEP 31: Create new thread dictionary
                            dTmp_Thread = {
                                "surrogate":    cp.deepcopy(kwargs["surrogate"]),
                                "data":         cp.deepcopy(kwargs["data"]),
                                "optimizer":    kwargs["optimizer"],

                                "id":           iThread_ID,
                                "password":     kwargs["password"],
                                "thread":       i
                            }

                            lThread_Data[i][2].put( [dTmp_Thread] )

                            #   STEP 32: Create a new thread
                            tTmp_Thread         = mp.Process(target=self.__threadTrain__, args=(eGlobal_Exit, lThread_Data[i][1], lThread_Data[i][2], lUO_Lock, ))
                            tTmp_Thread.daemon  = True
                            tTmp_Thread.start()

                            #   STEP 33: Set thread var
                            lThread_Data[i][0]  = tTmp_Thread
                            
                            #   STEP 34: Increment thread id
                            iThread_ID          += 1

            #   STEP 35: Check if 16 threads reached
            if ( len( lThread_Results ) == iThread):
                #   STEP 36: Exit loop
                break

            #
            #   endregion

            #   region STEP 37->46: Ui support

            #   STEP 37: Check if ui thread is set
            if (eUI_Event.is_set() == True):
                #   STEP 38: Clear event
                eUI_Event.clear()

                #   STEP 39: Check if ui output == "stop"
                if (qUI_Queue.get()[0] == "exit"):
                    #   STEP 40: Set thread joining event
                    eGlobal_Exit.set()
                    #tUI_Thread.join()

                    #   STEP 41: Loop through training threads
                    for i in range(0, len( lThread_Data )):
                        #   STEP 42: Check if thread is still training
                        if (lThread_Data[i][0].is_alive() == True):
                            #   STEP 43: Join thread
                            lThread_Data[i][0].join()

                            #   STEP 44: Save results
                            lThread_Results.append( lThread_Data[i][2].get()[0] )

                    #   STEP 45: Reset thread joining event
                    eGlobal_Exit.clear()

                    #   STEP 46: Exit loop
                    break

            #
            #   endregion

        #
        #   endregion

        #   STEP 47: Iterate through results
        for i in range(0, len( lThread_Results )):
            #   STEP 48: Check if fitter than current best
            if (lThread_Results[i]["fitness"] < fFittest):
                #   STEP 49: Set new best candidate
                fFittest    = lThread_Results[i]["fitness"]
                iFittest    = i

        #   STEP 50: Return
        return lThread_Results[iFittest]

    def __threadTrain__(self, _eExit, _eTr, _qTr, _lUO) -> None:
        """
            Description:
            
                This fucntion outsources the training of the surrogate to the appropriate
                optimization handler after finding the optimizer to use.

            |\n
            |\n
            |\n
            |\n
            |\n

            Parameters:

                + _eGlobal_Exit  = ( mp.Event() ) Event signalling global exit
                    for threads and processes

                + _eTr      = ( mp.Event() ) Event signalling process
                    completion

                + _qTr      = ( mp.Queue() ) The queue onto which the process
                    results should be returned

                + _lUO      = ( mp.RLock() ) The lock for commong user output

            |\n

            Returns:

                + dict        = ( dict )
                    ~ surrogate   = ( vars ) The trained surrogate
                    ~ fitness     = ( float ) The overall fitness of the trained surrogate
        """

        #   STEP 0: Local variables
        dArgs                   = _qTr.get()[0]
        dResults                = None

        iThread_ID              = Helga.ticks()
        iThread_AppID           = dArgs["thread"]

        iSwarms_Active          = 0
        iGA_Active              = 0

        iOptimizers_Active      = 0

        #   region STEP 1->15: Train using provided optimizer

        #   STEP 1: Check if not random optimizer
        if (rn.uniform(0.0, 1.0) > 0.3):
            #   STEP 2: Check if optimizer is GA
            if (ga.isEnum(dArgs["optimizer"])):
                #   STEP 3: User output
                if (self.bShowOutput):
                    #   STEP 4: Get lock
                    _lUO.acquire()

                    #   STEP 5: Print output
                    print("\t- Assigning SpongeBob to training")
                    print("\t- Optimizer: " + str(dArgs["optimizer"]))
                    print("\t- Thread ID: " + str(iThread_ID))
                    print("\t- Application Thread ID: " + str(iThread_AppID))
                    print("\t- Time: " + Helga.time() + "\n")

                    #   STEP 6: Release lock
                    _lUO.release()

                #   STEP 7: Create new optimizer
                sb = SpongeBob()

                #   STEP 8: Outsoruce training
                dResults = sb.trainSurrogate(surrogate=dArgs["surrogate"], data=dArgs["data"], password=dArgs["password"], optimizer=dArgs["optimizer"])

            #   STEP 9: Check if swarm
            elif (sw.isEnum( dArgs["optimizer"] )):
                #   STEP 10: User Output
                if (self.bShowOutput):
                    #   STEP 11: Get lock
                    _lUO.acquire()

                    #   STEP 12: Print strings
                    print("\t- Assigning Sarah to training")
                    print("\t- Optimizer: " + str(dArgs["optimizer"]))
                    print("\t- Thread ID: " + str(iThread_ID))
                    print("\t- Application Thread ID: " + str(iThread_AppID))
                    print("\t- Time: " + Helga.time() + "\n")

                    #   STEP 13: Release lock
                    _lUO.release()

                #   STEP 14: Create new optimizer
                sarah = Sarah()

                #   STEP 15: Outsource training
                dResults = sarah.trainSurrogate(surrogate=dArgs["surrogate"], data=dArgs["data"], password=dArgs["password"], optimizer=dArgs["optimizer"])

        #
        #   endregion

        #   region STEP 16->34: Random training

        #   STEP 16: Use random
        else:
            #   STEP 17: Update - Local variables
            iSwarms_Active      = sw.getNumActiveSwarms()
            iGA_Active          = ga.getNumActiveGAs()

            iOptimizers_Active  = iSwarms_Active + iGA_Active

            #   STEP 18: Random a handler
            iTmp_Optimizer      = rn.randint(0, iOptimizers_Active - 1)

            #   STEP 19: if swarm
            if (iTmp_Optimizer < iSwarms_Active):
                #   STEP 20: Get new swarm enum
                eTmp_Optimzier  = sw.getActiveSwarms()[iTmp_Optimizer]

                #   STEP 21: User Output
                if (self.bShowOutput):
                    #   STEP 22: Get lock
                    _lUO.acquire()

                    #   STEP 23: Print output
                    print("\t- Assigning Sarah to training")
                    print("\t- Optimizer: " + str(eTmp_Optimzier))
                    print("\t- Thread ID: " + str(iThread_ID))
                    print("\t- Application Thread ID: " + str(iThread_AppID))
                    print("\t- Time: " + Helga.time() + "\n")

                    #   STEP 24: Release lock
                    _lUO.release()

                #   STEP 25: Create new optimizer
                sarah       = Sarah()

                #   STEP 26: Outsource training
                dResults    = sarah.trainSurrogate(surrogate=dArgs["surrogate"], data=dArgs["data"], password=dArgs["password"], optimizer=eTmp_Optimzier)

            #   STEP 27: Then ga
            else:
                #   STEP 28: Get new ga enum
                eTmp_Optimizer = ga.getActiveGAs()[iTmp_Optimizer - iSwarms_Active]

                #   STEP 29: User Output
                if (self.bShowOutput):
                    #   STEP 30: Acquire lock
                    _lUO.acquire()

                    #   STEP 31: Print output
                    print("\t- Assigning SpongeBob to training")
                    print("\t- Optimizer: " + str(eTmp_Optimizer))
                    print("\t- Thread ID: " + str(iThread_ID))
                    print("\t- Application Thread ID: " + str(iThread_AppID))
                    print("\t- Time: " + Helga.time() + "\n")

                    #   STEP 32: Release lock
                    _lUO.release()

                #   STEP 33: Create new optimizer
                sb          = SpongeBob()

                #   STEP 34: Outsource training
                dResults    = sb.trainSurrogate(surrogate=dArgs["surrogate"], data=dArgs["data"], password=dArgs["password"], optimizer=eTmp_Optimizer)
        
        #
        #   endregion

        #   STEP 35: Get surrogate fitness
        fTmpFitness = dResults["surrogate"].getAFitness(data=dArgs["data"])
        fTmpFitness = fTmpFitness * dResults["inverse accuracy"]
        
        #   STEP 36: User Output
        if (self.bShowOutput):
            #   STEP 37: Get lock
            _lUO.acquire()

            #   STEP 38: Print output
            print("\t\t\t\t\t- Thread: " + str(iThread_AppID) +  " - <" + str(dResults["accuracy"]) + "  :  " + str(round(fTmpFitness, 2)) + ">")
            print("\t\t\t\t\t- Time: " + Helga.time() + "\n")

            #   STEP 39: release lock
            _lUO.release()

        #   STEP 40: Populate output dictionary
        dOut = {
            "accuracy":     dResults["accuracy"],
            "algorithm":    dResults["algorithm"],
            "fitness":      fTmpFitness,
            "iterations":   dResults["iterations"],
            "inverse accuracy": dResults["inverse accuracy"],
            "scalar":       dResults["scalar"],
            "surrogate":    dResults["surrogate"]
        }

        #   STEP 41: Set training results
        _qTr.put([dOut])

        #   STEP 42: Set training finished result
        _eTr.set()

        #   STEP 43: Return
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