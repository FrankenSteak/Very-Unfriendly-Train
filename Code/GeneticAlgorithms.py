#region Imports

from    enum                    import Enum

import  os
import  sys

sys.path.append(os.path.abspath("."))

from    Config                  import Conny

#endregion

#region Class - GeneticAlgorithms

class GeneticAlgorithms(Enum):

    #region Enums

    TRO         = [0, True, "GA\\TRO.json"]

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
    def isEnum(self, _eGaType: Enum) -> bool:
        """
        """

        #   STEP 0: Local variables
        lTmp                    = None

        #   STEP 1: Setup - Local variables
        lTmp                    = self.getGAs()

        #   STEP 2: Iterate through algorithms
        for i in range(0, len(lTmp)):
            if (_eGaType == lTmp[i]):
                return True
        
        #   STEP 3: Return
        return False

    @classmethod
    def isValue(self, _iGaType: int) -> bool:
        """
        """

        #   STEP 0: Local variables
        lTmp                    = None

        #   STEP 1: Setup - Local variables
        lTmp                    = self.getGAs()
        
        #   STEP 2: Iterate through algorithms
        for i in range(0, len(lTmp)):
            if (_iGaType == lTmp[i].value[0]):
                return True
            
        #   STEP 3: Return
        return False
    
    #
    #   endregion

    #   region Front-End: Gets

    @classmethod
    def getNumGAs(self) -> int:
        """
        """

        #   STEP 0: Local variables
        lTmp                    = None

        #   STEP 1: Setup - Local variables
        lTmp                    = self.getGAs()

        #   STEP 2: Return
        return len(lTmp)
    
    @classmethod
    def getGAs(self) -> list:
        """
        """

        #   STEP 0: Local variables
        lOut                    = []
        #   STEP 1: Setup - Local variables
        #   STEP 2: Populate output list
        lOut.append(self.TRO)

        #   STEP 3: Return
        return lOut

    @classmethod
    def getNumActiveGAs(self) -> int:
        """
        """

        #   STEP 0: Local variables
        lTmp                    = None

        iCount                  = 0

        #   STEP 1: Setup - Local variables
        lTmp                    = self.getGAs()

        #   STEP 2: Iterate through gas
        for i in range(0, len(lTmp)):
            if (lTmp[i].value[1] == True):
                iCount += 1

        #   STEP 3: Return
        return iCount

    @classmethod
    def getActiveGAs(self) -> list:
        """
        """

        #   STEP 0: Local variables
        lTmp                    = None
        lOut                    = []

        #   STEP 1: Setup - Local variables
        lTmp                    = self.getGAs()

        #   STEP 2: Iterate through algorithms
        for i in range(0, len(lTmp)):
            if (lTmp[i].value[1] == True):
                lOut.append(lTmp[i])

        #   STEP 3: Return
        return lOut

    @classmethod
    def getParameters(self) -> list:
        """
        """

        #   STEP 0: Local variables
        lOut                    = []
        lTmp                    = None

        #   STEP 1: Setup - Local variables
        lTmp                    = self.getGAs()

        #   STEP 2: Itreate through algorithms
        for i in range(0, len(lTmp)):
            #   STEP 3: Get config file
            cfTmp   = Conny()
            cfTmp.load(lTmp[i].value[2], isGA=True)

            #   STEP 4: Append parameters dictionary
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
        lTmp                    = self.getGAs()

        #   STEP 2: Iterate through algorithms
        for i in range(0, len(lTmp)):
            #   STEP 3: Get config file
            cfTmp   = Conny()
            cfTmp.load(lTmp[i].value[2], isGA=True)

            #   STEP 4: append scalars dictionary
            lOut.append(cfTmp.data["scalars"])

        #   STEP 5: Return
        return lOut
    
    #
    #   endregion

    #
    #endregion

#
#endregion