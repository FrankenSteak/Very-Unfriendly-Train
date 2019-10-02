#region Imports

from    enum                import Enum

#endregion

#region Class - Enums

class Enums(Enum):

    #region Enums

    #   region Enums: File-Types
        
    json        = [0, "File-Type"]
    txt         = [1, "File-Type"]

    #
    #   endregion

    #   region Enums: Antenna

    #       region Enums-(Antenna): Feeds

    temp        = [0, "Antenna-Feed"]

    #
    #       endregion

    #       region Enums-(Antenna): Sim-Roughness

    veryFine    = [0, "Sim-Roughness"]
    fine        = [1, "Sim-Roughness"]
    medium      = [2, "Sim-Roughness"]
    coarse      = [3, "Sim-Roughness"]
    veryCoarse  = [4, "Sim-Roughness"]

    #
    #       endregion

    #
    #   endregion

    #   region Enums: Classes

    #       region Enums-(Classes): Handlers

    Golem       = "Golem.json"
    Hermione    = "Hermione.json"
    Lana        = "Lana.json"
    Mathew      = "Mathew.json"
    Natalie     = "Natalie.json"
    Sarah       = "Sarah.json"
    SpongeBob   = "SpongeBob.json"

    #
    #       endregion

    #       region Enums-(Classes): Interface

    Heimi       = "Heimi.json"
    Irene       = "Irene.json"
    Rae         = "Rae.json"

    #
    #       endregion

    #       region Enums-(Classes): Optimizers
    
    Garry       = "Garry.json"
    SwarmChan   = "SwarmChan.json"
    UwU         = "UwU.json"

    #
    #       endregion

    #       region Enums-(Classes): Surrogates

    Annie   = "Annie.json"
    Viktor  = "Viktor.json"
    King    = "King.json"
    
    #
    #       endregion

    #       region Enums-(Classes): Helpers

    Antonio = "Antonio.json"
    Data    = "Data.json"
    David   = "David.json"
    
    #
    #       endregion

    #
    #   endregion

    #   region Enums: Lua

    Millimetres = [0, "mm", "millimeters", "Millimetres"]

    #
    #   endregion

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
    def isClass(self, _eClass: Enum) -> bool:
        if (_eClass == self.Golem):
            return True

        if (_eClass == self.Hermione):
            return True

        if (_eClass == self.Mathew):
            return True

        if (_eClass == self.Natalie):
            return True

        if (_eClass == self.Sarah):
            return True

        if (_eClass == self.SpongeBob):
            return True

        if (_eClass == self.Heimi):
            return True

        if (_eClass == self.Irene):
            return True

        if (_eClass == self.Rae):
            return True

        if (_eClass == self.Garry):
            return True

        if (_eClass == self.SwarmChan):
            return True

        if (_eClass == self.UwU):
            return True

        if (_eClass == self.Annie):
            return True

        if (_eClass == self.Viktor):
            return True

        if (_eClass == self.King):
            return True

        return False

    @classmethod
    def isUnit(self, _sUnit: str) -> bool:
        """
        """

        #   STEP 0: Local variables
        lUnits                  = self.getUnits()

        #   STEP 1: Setup - Local variables
        
        #   STEP 2: Iterate through units
        for i in range(0, len(lUnits)):
            #   STEP 3: Check if this unit
            if ((lUnits[i].value[1] == _sUnit) or (lUnits[i].value[2] == _sUnit)):
                #   STEP 4: Return
                return True

        #   STEP 5: Return
        return False

    #
    #   endregion

    #   region Front-End: Gets

    #       region Front-End-(Gets): Feed

    @classmethod
    def getNumFeeds(self) -> int:
        """
        """

        #   STEP 0: Local variables
        #   STEP 1: Setup - Local variables
        #   STEP 2: ??

        return 1

    @classmethod
    def getFeeds(self) -> list:
        """
        """

        #   STEP 0: Local variables
        lOut        = []

        #   STEP 1: Setup - Local variables
        #   STEP 2: ??
        lOut.append(self.temp)

        #   STEP 3: Return
        return lOut

    #
    #       endregion

    #       region Front-End-(Gets): Lua

    @classmethod
    def getUnits(self) -> list:
        """
            Description:

                Returns a list of all the valid units of measurement for the
                lua wrapper.

            |\n
            |\n
            |\n
            |\n
            |\n

            Returns:

                + lOut  = ( list ) A list of all the valid units of measurement
                    for the lua wrapper
        """

        #   STEP 0: Local variables
        lOut                    = []

        #   STEP 1: Setup - Local variables

        #   STEP 2: Populate outputlist
        lOut.append(self.Millimetres)

        #   STEP 3: Return
        return lOut

    @classmethod
    def getNumUnits(self) -> int:
        """
            Description:

                Return the number of vali units of measurement for the lua
                wrapper.

            |\n
            |\n
            |\n
            |\n
            |\n

            Returns:

                + iOut  = ( int ) The number of valid units of measurement for
                the lua wrapper
        """

        #   STEP 0: Local variables
        
        #   STEP 1: Setup - Local variables

        #   STEP 2: Return
        return len(self.getUnits())

    @classmethod
    def getUnit(self, _sUnit: str) -> str:
        """
            Description:

                Returns the keyword for the specified unit of emasurement.

            |\n
            |\n
            |\n
            |\n
            |\n

            Parameters:

                + _sUnit    = ( str ) The unit of measurement

            Reutnrs:

                + sOut  = ( str ) The keyworkd for the specified unit of
                    measurement
        """

        #   STEP 0: Local variables
        lUnits                  = self.getUnits()

        #   STEP 1: Setup - Local variables

        #   STEP 2: Verify unit
        if (self.isUnit(_sUnit) == False):
            #   STEP 3: Error handling
            raise Exception("An error occured in Enums.getUnit() -> Step 2: Passed unit of measurement is not an enum")

        #   STEP 4: Loop
        for i in range(0, len(lUnits)):
            #   STEP 5: Check if this unit
            if ((lUnits[i].value[1] == _sUnit) or (lUnits[i].value[2] == _sUnit)):
                #   STEP 6: Return
                return lUnits[i].value[3]

        #
        
    #
    #       endregion

    #
    #   endregion

    #
    #endregion

#
#endregion

