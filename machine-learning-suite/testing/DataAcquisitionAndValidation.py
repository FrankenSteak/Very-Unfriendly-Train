#region Imports
import  os
import  sys
import  threading                        as thread
import  time                             as t

sys.path.append(os.path.abspath("."))

from    Config                  import Conny
from    DataContainer           import Data
from    GeneralHelpers          import ApplicationHelper

#endregion

#region DAVID

#   region GLOBALS - Eeeeeeeew

teUInputEvent    = thread.Event()
sUserInput      = ""
tTest = None

#   endregion

#   region Class - David

class DAVID:

    #   region Init

    """
    ToDo "This bitch empty! YEEEET"
    """

    def __init__(self) -> None:
        
        #region STEP 0: Local variables
        self.__cf = Conny()
        self.__cf.load("David.json")

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
    #   endregion

    #   region Front-End

    def main(self, _iIterations: int, _iWaitPeriod):
        """
        """
        #   STEP -1: Global variables
        global teUInputEvent
        global tTest

        #   STEP 0: Local variables
        sFileName   = ApplicationHelper.ticks()
        lData       = []
        iCount      = 0

        #   STEP 1: Setup - Global variables
        tTest = thread.Thread(target=self.__userInput)
        tTest.daemon = True
        tTest.start()

        #   STEP ..: Setup - local variables
        
        #   STEP 2: We out here looping
        while (True):
            #   STEP 3: Perform the result acquisition
            print("\tDAVID - Gathering data (" + str(iCount + 1) + " / " + str(_iIterations) + ")")
            lData = self.__theTHING(lData, sFileName)
            iCount = iCount + 1

            #   STEP 4: Check for user input
            if (teUInputEvent.isSet() == True):
                #   STEP 4.1: Get global varialbes
                global sUserInput

                #   STEP 4.2: Check if input was to stop
                if (sUserInput == "stop"):
                    #   STEP 4.2.1: Clear variables and end loop
                    sUserInput = ""
                    teUInputEvent.clear()

                    break
                
                else:
                    #   STEP 4.2.2: Clear variables and restart thread (no additional commands atm)
                    sUserInput = ""
                    teUInputEvent.clear()

                    tTest.run()

            #   STEP 5: Check if iterations have been reached

            if ((_iIterations > 0) and (iCount >= _iIterations)):
                #   STEP 5.1: iteration condition achieved
                break

            #   STEP 6: Wait the set amount of time
            if ((_iWaitPeriod > 0) and (_iWaitPeriod <= 10)):
                t.sleep(_iWaitPeriod)


        #   STEP 7: Average data
        #lData = self.__averageData(lData, iCount)

        #   STEP 8: Write the data to file and ???
        self.__saveData(lData, sFileName, iCount)

        #   STEP 9: GTFO
        return
    
    #
    #   endregion

    #   region Back-End

    def __theTHING(self, _lData: list, _sFileName: str) -> list:
        #   values chosen arbitrarily
        #
        #   a = Swarm Size              = [10, 20 {, 5}]
        #   b = Swarm Iterations        = [15, 40 {, 5}]
        #   c = Def Iterations          = [400, 1000 {, 100}]

        #   STEP 0: Local vars
        global teUInputEvent

        fFile = None

        sFileName   = ""
        iCount      = 0
        bFirst      = False
        
        #   STEP 1: Define if necesarry
        if (len(_lData) <= 0):
            bFirst = True
            sFileName = os.path.abspath(".") + "\\Helpers\\Testing\\" + _sFileName + "_parm.txt"
            
            fileTmp = open(sFileName, "a")
            fileTmp.close()
            fileTmp = None

            fFile = open(sFileName, "r+")
            fFile.write("Params=[Swarm Size, Swarm Iterations, Def Iterations]\n")
        
        #   STEP 0: Other variables
        dIris = Data()
        dIris.importData(os.path.abspath(".") + "\\Data\\DataSets\\Iris\\iris.data")
        
        #   STEP 2: Swarm Size
        for a in range(10, 21, 5):
            #   STEP 3: Swarm Iterations
            for b in range(15, 41, 5):
                #   STEP 4: Def Iterations
                for c in range(400, 1001, 100):
                    #   STEP 6: Create annie
                    """
                        fire = Annie(4, 3, 5, 5, -1)
                        fire.bShowOutput    = True
                        
                        #   STEP 6.1 Set activation function variables
                        fire.setTanH(0.2, 1.0)
                        fire.fLearningRate  = fire.fLearningRate * 5.0
                        
                        #   STEP 6.2: Set candidate and algorithm iterations
                        fire.iOptCandidates = a + 1
                        fire.iOptIterations = b + 1
                        fire.iMaxIterations = c + 1

                        fire.iAccCheckPoint = 25

                        #	STEP 7: Local variables
                        bFailed     = 0
                        iTime       = dt.datetime.now()
                        iAccuracy   = 0
                        iIterations = 0

                        try:
                            #   STEP 8: Run
                            iIterations = fire.train_set(dIris, True, False, True, 3)
                            iAccuracy = fire.getAccuracy(dIris)

                        except Exception as ex:
                            #   STEP 2.7: bombed out
                            print("\tDAVID (The THING) {" + ApplicationHelper().time() + "} - Bombed out:")
                            print("\t\tSwarm Size: " + str(a))
                            print("\t\tSwarm Iterations: " + str(b))
                            print("\t\tDef Iterations: " + str(c))
                            print("\t\tException: " + ex)
                            

                        #   STEP 2.8: If first iteration of test then add data
                        if (bFirst):
                            lTmp = []
                            lTmp.append(0)                              #0 - Count
                            lTmp.append(0)                              #1 - Time
                            lTmp.append(0)                              #2 - Iterations
                            lTmp.append(0)                              #3 - Accuracy

                            _lData.append(lTmp)

                            sTmp = ":" + str(a) + ":"
                            sTmp += str(b) + ":"
                            sTmp += str(c) + ":\n"
                            fFile.write(sTmp)

                        if (iIterations >= 0):
                            #   STEP 2.9: If training failed say so
                            _lData[iCount][0] += 1
                            
                            dTmp = dt.datetime.now() - iTime
                            dTmp = int(dTmp.total_seconds()*10000000)

                            _lData[iCount][1] += dTmp
                            _lData[iCount][2] += iIterations
                            _lData[iCount][3] += iAccuracy

                        #   STEP 21: Increase counter
                    """
                    iCount = iCount + 1

        if (fFile != None):
            fFile.close()
            fFile = None

        return _lData

    def __averageData(self, _lData: list, _iIterations: int) -> list:
        if (len(_lData) > 0):
            print("\tDAVID - Averaging Data")
            for i in range(0, len(_lData)):
                for j in range(1, len(_lData[i])):
                    _lData[i][j] = float(_lData[i][j]) / _iIterations

                    if (_lData[i][j] > 0):
                        _lData[i][j] = int(_lData[i][j])

                _lData[i][0] = int(_lData[i][0])

        return _lData

    def __userInput(self) -> None:
        global teUInputEvent

        if (teUInputEvent.is_set() == True):
            print("waiting")
            teUInputEvent.wait()

        global sUserInput

        sUserInput = input("")
        teUInputEvent.set()
        print("\tDAVID - Input received. Please wait while the data acquisition finishes")

    def __saveData(self, _lData: list, _sFileName: str, _iIterations: int) -> None:
        if (len(_lData) > 0):
            print("\tDAVID - Saving Data")

            #   STEP 0: Local variables
            fFileOut = None
            
            try:
                #   STEP 0.1: Some more variables
                sFile = os.path.abspath(".") + "\\Helpers\\Testing\\" + _sFileName + "_data.txt"
                sTmp = ""

                #   STEP 1: Create file
                fFileOut = open(sFile, "a")
                fFileOut.close()
                fFileOut = None

                #   STEP 2: Write to file
                fFileOut = open(sFile, "r+")

                #   STEP 3: Loop through the list and write it to the file
                sTmp = "Iterations=" + str(_iIterations) +"|Params=[Failures, Time, Iterations, Accuracy]\n"
                fFileOut.write(sTmp)

                for i in range(0, len(_lData)):
                    sTmp = ":"
                    if (len(_lData[i]) > 1):
                        for j in range(0, len(_lData[i])):
                            sTmp = sTmp + str(_lData[i][j]) + ":"
                    
                    else:
                        sTmp = sTmp + str(_lData[i]) + ":"

                    fFileOut.write(sTmp + "\n")

            except:
                print("An error occured in Helpers.DAVID->savData()")

            finally:
                if (fFileOut != None):
                    fFileOut.close()
                    fFileOut = None

                print("\tDAVID - Data Acquisition completed\n")
                return

    #
    #   endregion

#
#   endregion

#
#endregion

if (__name__ == "__main__"):
    d = DAVID()

    print("DAVID - Starting Data Acquisition")

    teUInputEvent.clear()

    d.main(0, 0)

    print("DAVID - Data Acquisition Successul")