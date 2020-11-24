#region Imports

from    enum                            import Enum

import 	numpy as np
import 	os
import 	sys

sys.path.append(os.path.abspath("."))

from    Enums                import Enums        as en

from 	Config 				    import Conny

#endregion

#region Class - UwU

class UwU:

	#region Init

    """
        - **Description**::

        EEEEK! Oni-Swarm don't touch me there!
        
        |\n
        |\n
        |\n
        |\n
        |\n
    """

    def __init__(self):

        #region STEP 0: Local variables

        self.__enum                 = en.UwU

        #endregion

        #region STEP 1: Private variables

        #   region STEP 1.1: Bools

        self.__bAllowTesting        = False

        #   endregion

        #endregion

        #region STEP 2: Public variables

        #   region STEP 2.1: Params

        self.lCurrPosition  = []
        self.lBestPosition  = []

        self.lVelocity      = []

        self.fFitness       = np.inf

        #   endregion

        #   region STEP 2.2: Bools

        self.bShowOutput        = False #self.__cf.data["parameters"]["show output"]

        #   endregion

        #   region STEP 2.3: Other

        self.data               = {}

        #   endregion

        #endregion
        
        #   STEP 3: Return
        return
    
    #
    #endregion

    #region Sets

    def setFitness(self, _fFit: float) -> None:
        """
			- **Description**::

			Sets the fitness of this particle

			|\n
			|\n
			|\n
			|\n
			|\n
			- **Parameters**::

				:param _fFit: >> (float) The new fitness for this particle

			- **Return**::

				:return: >> None
		"""

        #   STEP 1: Check if this fitness is an improvement
        if (_fFit < self.fFitness):
            #   STEP 2: Set the new best position for this
            self.lBestPosition = self.lCurrPosition
        
        #   STEP 3: Set the fitness
        self.fFitness = _fFit

        #   STEP 4: Return
        return

    #
    #endregion

#
#endregion