#region Imports

from    enum                            import Enum

import  os
import  sys

sys.path.append(os.path.abspath("."))

from    Code.Enums.Enums                import Enums            as en

from    Helpers.Config                  import Conny

#endregion

#region Class - Viktor

class Viktor:

    #region Init

    """
    """

    def __init__(self):

        #region STEP 0: Local variables

        self.__enum                 = en.Viktor
        self.__cf                   = Conny()
        self.__cf.load(self.__enum.value)

        #endregion

        #region STEP 1: Private variables

        #   region STEP 1.??: Bools

        self.__bAllowTesting        = self.__cf.data["parameters"]["allow testing"]

        #   endregion

        #endregion

        #region STEP 2: Public variables

        #   region STEP 2.??: Bools

        self.bShowOutput            = self.__cf.data["parameters"]["show output"]

        #   endregion
        
        #endregion

        #region STEP 3: Setup - Private variables

        #endregion

        #region STEP 4: Setup - Public variables

        #endregion

        return

    #
    #endregion

    #region Front-End

    #
    #endregion

    #region Back-End

    #
    #endregion

#
#endregion