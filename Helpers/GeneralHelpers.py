#region Imports

import datetime as dt
import math as mt
import  numpy           as np

#endregion

#region Class - Helga

class Helga:

    #region Init

    """
    """

    def __init__(self):
        return
    
    #
    #endregion

    #region Front-End

    #   region Front-End: Gets

    @classmethod
    def getShape(self, _lData: list) -> list:
        """
        """

        #   STEP 0: Local variables
        lOut                    = []

        #   STPE 1: Setup - Local variables

        #   STEP 2: Iterate through list
        for i in range(0, len(_lData)):
            #   STEP 3: Check if single data value
            if (type(_lData[i]) == float):
                lOut.append(0.0)

            #   STEP 4: Append list of zeros
            else:
                lOut.append(np.zeros(len(_lData[i])))

        #   STEP 5: Return
        return lOut
    
    @classmethod
    def getList(self, _lData) -> list:
        """
        """

        #   STEP 0: Local variables
        lOut                    = []

        #   STEP 1: Setup - Local variables

        #   STEP 2: Iterate through _lData
        for i in range(0, len(_lData)):
            #   STEP 3: Append list to output list
            lOut.append(list(_lData[i]))

        #   STEP 4: Return
        return lOut

    @classmethod
    def round(slef, _lData, iRound) -> list:
        """
        """

        #   STEP 0: Local variables
        lOut                    = []

        #   STEP 1: Setup - Local variables

        #   STEP 2: Iterate through input data
        for i in range(0, len(_lData)):
            #   STEP 3: Round value
            lOut.append( round( _lData[i], iRound ) )

        #   STEP ??: Return
        return lOut

    #
    #   endregion

    #   region Front-End: Time

    @classmethod
    def ticks(self) -> str:
        dtTmp = dt.datetime.now() - dt.datetime(1, 1, 1)
        iOut = int(dtTmp.total_seconds()*10000000)

        return str(iOut)

    @classmethod
    def time(self) -> str:
        return dt.datetime.now().strftime("%H:%M:%S")

    #
    #   endregion

    #   region Front-End: Output

    @classmethod
    def print2DArray(self, _arrTmp: list) -> None:
        for i in range(0, len(_arrTmp)):
            for j in range(0, len(_arrTmp[i])):
                print(str(round(_arrTmp[i][j], 2)), "\t", end="")
            print("")

    #
    #   endregion

    #   region Front-End: Other

    @classmethod
    def nop(self) -> None:
        return

    #
    #   endregion

    #
    #endregion

#
#endregion


#region Archive

    """
    
    @classmethod
    def extractData(self, _fFile) -> str:
        sTmp = _fFile.readline()
        sTmp = sTmp.split(":")
        sTmp = sTmp[1]
        sTmp = sTmp.split("\n")
        sTmp = sTmp[0]
        
        return sTmp

    @classmethod
    def extractBool(self, _fFile) -> bool:
        sTmp = self.extractData(_fFile)

        if (sTmp == "True"):
            return True
        else:
            return False

    """

#endregion