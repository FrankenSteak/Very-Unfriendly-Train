#region Imports

from    enum                        import Enum

import  os
import  sys

sys.path.append(os.path.abspath("."))

from    Code.Surrogates.ArtificialNeuralNetwork             import Annie

from    Helpers.Config              import Conny

#endregion

#region Class - Surrogates (Enum)

class Surrogates(Enum):

    #region Enums

    Annie               = [0,   True,   "Annie.json"]
    Viktor              = [1,   False,  "Viktor.json"]
    King                = [2,   False,  "King.json"]

    #
    #endregion

    #region Init

    """
    """

    #
    #endregion

    #region Front-End

    #   region Front-End: Is-type-statements

    @classmethod
    def isEnum(self, _eSurrogateType: Enum) -> bool:
        """
        """

        #   STEP 0: Local variables
        lTmp                    = None

        #   STEP 1: Setup - Local variables
        lTmp                    = self.getSurrogates()

        #   STEP 2: Iterate through surrogates
        for i in range(0, len(lTmp)):
            if (_eSurrogateType == lTmp[i]):
                return True

        #   STEP 3: Return
        return False

    @classmethod
    def isValue(self, _iSurrogateType: int) -> bool:
        """
        """

        #   STEP 0: Local variables
        lTmp                    = None

        #   STEP 1: Setup - Local variables
        lTmp                    = self.getSurrogates()

        #   STEP 2: Iterate through surrogates
        for i in range(0, len(lTmp)):
            if (_iSurrogateType == lTmp[i].value[0]):
                return True

        #   STEP 3: Return
        return False

    #
    #   endregion

    #   region Front-End: Gets

    @classmethod
    def getNewSurrogate(self, **kwargs) -> vars:
        """
        """

        #   STEP 0: Local variables
        #   STEP 1: Setup - Local variables

        #   STEP 2: be safe
        try:
            #   STEP 3: Check if annie
            if (kwargs["surrogate"] == self.Annie):
                return Annie(params=kwargs["params"])

            else:
                #   STEP 4: Not active surrogate
                raise Exception("An error occured in Surrogates.getNewSurrogate -> Step 4: Specified surrogate either does not exist or is currently inactive")

        except Exception as ex:
            print("Initial Exception: ", ex)
            raise Exception("An error occured in Surrogates.getNewSurrogate")

        #   STEP ??: Return
        return

    @classmethod
    def getNumSurrogates(self) -> int:
        """
        """

        #   STEP 0: Local variables
        lTmp                    = None

        #   STEP 1: Setup - Local variables
        lTmp                    = self.getSurrogates()

        #   STEP 2: Return
        return len(lTmp)

    @classmethod
    def getSurrogates(self) -> list:
        """
        """

        #   STEP 0: Local variables
        lOut = []

        #   STEP 1: Setup - Local variables
        #   STEP 2: Populate output list
        lOut.append(self.Annie)
        lOut.append(self.Viktor)
        lOut.append(self.King)

        #   STEP 3: Return
        return lOut

    @classmethod
    def getNumActiveSurrogates(self) -> int:
        """
        """

        #   STEP 0: Local variables
        lTmp                    = None

        iCount                  = 0

        #   STEP 1: Setup - Local variables
        lTmp                    = self.getSurrogates()

        #   STEP 2: Iterate through surrogates
        for i in range(0, len(lTmp)):
            if (lTmp[i].value[1] == True):
                iCount += 1
        
        #   STEP 3: Return
        return iCount

    @classmethod
    def getActiveSurrogates(self) -> list:
        """
        """

        #   STEP 0: Local variables
        lOut                    = []
        lTmp                    = None

        #   STEP 1: Setup - Local variables
        lTmp                    = self.getSurrogates()

        #   STEP 2: Iterate through surrogates
        for i in range(0, len(lTmp)):
            if (lTmp[i].value[1] == True):
                lOut.append(lTmp[i])
                
        #   STEP 3: Return
        return lOut

    @classmethod
    def getActiveParameters(self) -> list:
        """
        """

        #   STEP 0: Local variables
        lOut                    = []
        lTmp                    = None

        #   STEP 1: Setup - local variables
        lTmp                    = self.getSurrogates()

        #   STPE 2: Iterate through surrogates
        for i in range(0, len(lTmp)):
            #   STEP 3: If active
            if (lTmp[i].value[1] == True):
                #   STEP 4: Get config files
                cfTmp = Conny()
                cfTmp.load(lTmp[i].value[2])

                #   STEP 5: Append to output
                lOut.append(cfTmp.data["parameters"])

        #   STEP 6: Return
        return lOut

    @classmethod
    def getActiveScalars(self) -> list:
        """
        """

        #   STEP 0: Local variables
        lOut                    = []
        lTmp                    = None

        #   STEP 1: Setup - Local variables
        lTmp                    = self.getSurrogates()

        #   STEP 2: Iterate through surrogates
        for i in range(0, len(lTmp)):
            #   STEP 3: If active
            if (lTmp[i].value[1] == True):
                #   STEP 4: Get config file
                cfTmp = Conny()
                cfTmp.load(lTmp[i].value[2])
                
                #   STEP 5: Append to output
                lOut.append(cfTmp.data["scalars"])

        #   STEP 6: Return
        return lOut
    
    @classmethod
    def getParameters(self) -> list:
        """
        """

        #   STEP 0: Local variables
        lOut                    = []
        lTmp                    = None

        #   STEP 1: Setup - Local variables
        lTmp                    = self.getSurrogates()

        #   STEP 2: Iterate through surrogates
        for i in range(0, len(lTmp)):
            #   STEP 3: Get config file
            cfTmp   = Conny()
            cfTmp.load(lTmp[i].value[2])
            
            #   STEP 4: Append to output list
            lOut.append(cfTmp.data["parameters"])

        #   STEP 5: Return
        return lOut

    @classmethod
    def getScalars(self) -> list:
        """
        """

        #   STEP 0: Local variables
        lOut                    = []
        lTmp                    = None

        #   STEP 1: Setup - Local variables
        lTmp                    = self.getSurrogates()

        #   STEP 2: Iterate through surrogates
        for i in range(0, len(lTmp)):
            #   STEP 3: Get config file
            cfTmp   = Conny()
            cfTmp.load(lTmp[i].value[2])

            #   STEP 4: Append to output list
            lOut.append(cfTmp.data["scalars"])

        #   STEP 5: Return
        return lOut

    #
    #   endregion

    #
    #endregion

#
#endregion