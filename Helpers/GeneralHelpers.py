#region Imports

import  datetime        as dt
import  math            as mt
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

    #   region Front-End: List stuff

    @classmethod
    def getCentroid(self, _lCandidates: list) -> list:
        """
            Description:

                Gets the centroid of the list of candidates passed.

            |\n
            |\n
            |\n
            |\n
            |\n

            Parameters:

                :param _lCandidates:    = ( list ) List of candidates

            |\n

            Returns:

                + lOut  = ( list ) 
        """

        #   STEP 0: Local variables
        lOut                    = None

        #   STEP 1: Setup - Local variables
        
        #   STEP 2: Check that candidates is a list
        if (type(_lCandidates) != list):
            #   STEP 3: Error handling
            raise Exception("An error occured in Helga.getCentroid() -> Step 2: Passed parameter must be a list")

        #   STEP 4: Setup - Local variables
        lOut    = Helga.getShape(_lCandidates[0])

        #   STEP 5: Loop through candidates
        for i in range(0, len( _lCandidates )):
            #   STEP 6: Loop through candidate parameters
            for j in range(0, len( _lCandidates[i] )):
                #   STEP 7: Check if param is list
                if ( type( _lCandidates[i][j] ) == list):
                    #   STEP 8: Loop through param list
                    for k in range(0, len( _lCandidates[i][j] )):
                        #   STEP 9: Add to output
                        lOut[j][k] += _lCandidates[i][j][k]

                #   STEP 10: Param not list
                else:
                    #   STEP 11: Add to output
                    lOut[j] += _lCandidates[i][j]

        #   STEP 12: Loop through output params
        for i in range(0, len( lOut )):
            #   STEP 13: Check if param is list
            if ( type( lOut[i] ) == list):
                #   STEP 14: Loop through param list
                for j in range(0, len( lOut[i] )):
                    #   STEP 15: Average output val
                    lOut[i][j] = lOut[i][j] / float( len( _lCandidates ))

            #   STEP 16: Param not list
            else:
                #   STEP 17: Average output val
                lOut[i] = lOut[i] / float ( len( _lCandidates )) 

        #   STEP 18: Return
        return lOut

    @classmethod
    def shiftCandidates(self, _lCentroid: list, _lCandidates: list, _fScalar: float, _iRegion1: int, _iRegion2: int) -> list:
        """
            Description:

                Shifts the candidate list towards or from the passed centroid
                based on the provided arguments.

            |\n
            |\n
            |\n
            |\n
            |\n

            Parameters:

                :param _lCentroid:  = ( list ) The candidate about which the
                    candidate list should be shifted

                :param _lCandidates:    = ( list ) The list of candidates to be
                    shifted about the centroied

                :param _fScalar:    = ( float ) The scalar for the shifting
                    operations

            |\n

            Example:

                + lCandidate_New    = _lCentroid + _fScalar * ( _iRegion1 * _lCentroid + _iRegion2 * _lCandidates[i] )
        """

        #   STEP 0: Local variables
        #   STEP 1: Setup - Local variables
        #   STEP 2: ??
        #   STEP ??: Return
        return []

    @classmethod
    def orderCandidates(self, _lBy: list, _lDependent: list) -> dict:
        """
        """

        #   STEP 0: Local variables
        #   STEP 1: Setup - Local variables
        #   STEP 2: ??
        #   STEP ??: Return
        return {}

    #
    #   endregion

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
            if ((type(_lData[i]) == float) or (type(_lData[i]) == int)):
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
    def getValue(self, _sData: str, _iIndex: int) -> vars:
        """
        """

        #   STEP 0: Local variables
        lData                   = []

        sData                   = ""
        #   STEP 1: Setup - Local variables

        #   STEP 2: Check that input is str
        if (type(_sData) != str):
            #   STEP 3: Error handling
            raise Exception("An error occured in Helga.getValue() -> Step 3: Invalid input")

        #   STEP 4: Loop through input
        for i in range(0, len(_sData)):
            #   STEP 5: Check if current index empty, tab, or newl
            if (( _sData[i] == " " ) or ( _sData[i] == "\t" ) or ( _sData[i] == "\n" )):
                #   STEP 6: Check if there is data to add to the list
                if (sData != ""):
                    #   STEP 7: Be safe OwO
                    try:
                        #   STEP 8: Append to list
                        lData.append( float(sData ) )

                    #   STEP 9: Error shortcut
                    except:
                        #   STEP 10: APpend to list
                        lData.append(sData)

                    #   STEP 11: Reset data str
                    sData   = ""

            #   STEP 12: Not empty, add to data str
            else:
                #   STEP 13: Add to data str
                sData += _sData[i]

        #   STEP 14: Check if index in range
        if (_iIndex < len( lData )):
            #   STEP 15: Return
            return lData[_iIndex]

        #   STEP 16: Return
        return lData

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

if (__name__ == "__main__"):

    ltmp = [[1,1],
            [2,2],
            [3,1],
            [4,0]]

    lTmp = Helga.getCentroid(ltmp)
    Helga.nop()
    print(lTmp)

#endregion
