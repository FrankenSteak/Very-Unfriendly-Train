import helpers.ArrayHelper as ArrayHelper

class MathHelper:
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
    def transpose(self, _lData: list) -> list:
        """
            Description:
            
                Tronsposes the passed data list.
        """

        #   STEP 0: Local variables
        lOut                    = []

        #   STEP 1: Check if 1D
        if ( type(_lData[0]) == float):
            #   STEP 2: Loop through parameters
            for i in range(0, len( _lData ) ):
                #   STEP 3: Populate output list
                lOut.append( [ _lData[i] ] )

        #   STEP 4: Then 2D
        else:
            #   STEP 5: Loop through candidates
            for i in range(0, len( _lData[0] ) ):
                #   STEP 6: Setup - Tmp variable
                lTmp_Candidate  = []

                #   STEP 7: Loop through parameters
                for j in range(0, len( _lData ) ):
                    #   STEP 8: Add to candidate list
                    lTmp_Candidate.append( _lData[j][i] )

                #   STEP 9: Append to output list
                lOut.append(lTmp_Candidate)

        #   STEP 10: Return
        return lOut

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
            raise Exception("An error occured in MathHelper.getCentroid() -> Step 2: Passed parameter must be a list")

        #   STEP 4: Setup - Local variables
        lOut    = ArrayHelper.getShape(_lCandidates[0])

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
