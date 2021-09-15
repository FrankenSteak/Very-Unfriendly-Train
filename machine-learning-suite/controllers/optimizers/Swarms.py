#region Imports

from    enum                            import Enum

import  os
import  sys

sys.path.append(os.path.abspath("."))

#endregion

#region Class - Swarms (Enum)

class Swarms(Enum):

    #region Enums

    PSO                 = [0, True, "Swarm\\PSO.json"]
    BEE                 = [1, False, ""]

    #
    #endregion

    #region Init

    """
    """

    #
    #endregion

    #region Front-End

    #   region  Front-End: Is-type-statements

    @classmethod
    def isEnum(self, _eSwarmType: Enum) -> bool:
        """
        """

        #   STEP 0: Local variables
        lTmp                    = None

        #   STEP 1: Setup - Local variables
        lTmp                    = self.getSwarms()

        #   STEP 2: Iterate through swarms
        for i in range(0, len(lTmp)):
            if (_eSwarmType == lTmp[i]):
                return True
        
        #   STEP 3: Return
        return False

    @classmethod
    def isValue(self, _iSwarmType: int) -> bool:
        """
        """

        #   STEP 0: Local variables
        lTmp                    = None

        #   STEP 1: Setup - Local variables
        lTmp                    = self.getSwarms()
        
        #   STEP 2: Iterate through swarms
        for i in range(0, len(lTmp)):
            if (_iSwarmType == lTmp[i].value[0]):
                return True

        #   STEP 3: Return
        return False

    #
    #   endregion

    #   region  Front-End: Gets

    @classmethod
    def getNumSwarms(self) -> int:
        """
        """

        #   STEP 0: Local variables
        lTmp                    = None

        #   STEP 1: Setup - Local variables
        lTmp                    = self.getSwarms()

        #   STEP 2: Return
        return len(lTmp)
    
    @classmethod
    def getSwarms(self) -> list:
        """
        """

        #   STEP 0: Local variables
        lOut = []

        #   STEP 1: Setup - Local variables
        
        #   STEP 2: Populate output list
        lOut.append(self.PSO)
        lOut.append(self.BEE)

        #   STEP 3: Return
        return lOut
        
    @classmethod
    def getNumActiveSwarms(self) -> int:
        """
        """

        #   STEP 0: Local variables
        lTmp                    = None

        iCount                  = 0
        #   STEP 1: Setup - Local variables
        lTmp                    = self.getSwarms()

        #   STEP 2: Count active swarms
        for i in range(0, len(lTmp)):
            if (lTmp[i].value[1] == True):
                iCount += 1
            
        #   STEP 3: Return
        return iCount

    @classmethod
    def getActiveSwarms(self) -> list:
        """
        """

        #   STEP 0: Local variables
        lTmp                    = None
        lOut                    = []

        #   STEP 1: Setup - Local variables
        lTmp                    = self.getSwarms()

        #   STEP 2: Iterate through swarms
        for i in range(0, len(lTmp)):
            if (lTmp[i].value[1] == True):
                lOut.append(lTmp[i])
        
        #   STEP 3: Return
        return lOut


    #
    #   endregion

    #
    #endregion

#
#endregion