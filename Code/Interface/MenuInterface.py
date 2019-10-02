#region Imports

from    enum                            import Enum

import  os
import  sys

sys.path.append(os.path.abspath("."))

from    Code.Enums.Enums                import Enums        as en

from    Helpers.Config                  import Conny
from    Helpers.GeneralHelpers          import Helga

#endregion

#region Class - Rae

class Rae:

    #region Init

    """
    """

    def __init__(self):

        #region STEP 0: Local variables

        self.__enum                 = en.Rae
        self.__cf                   = Conny()
        self.__cf.load(self.__enum.value)

        #endregion

        return

    #
    #endregion

    #region Front-End

    #   region Front-End: Gets

    @classmethod
    def getUserInput(self, _eClass: Enum, **kwargs) -> int:
        """
        """

        #   STEP 0: Local variables
        cfTmp = Conny()

        #   STEP 2: Check if the enum is acceptable
        if (en.isClass(_eClass) == False):
            raise Exception("An error occured in Rae.getUserInput -> Step 2: Invalid enum passed")
        
        #   STEP 1: (DELAYED) Setup - Local variables
        cfTmp.load(_eClass.value)

        #   STEP 3: Get the menu options
        lMenu = cfTmp.getMenu(kwargs)

        #   STEP 4: Outsource Return
        if ("breakOnInvalid" in kwargs):
            return self.__getUI(lMenu, kwargs["breakOnInvalid"])

        else:
            return self.__getUI(lMenu, False)

    #
    #   endregion

    #
    #endregion

    #region Back-End

    #   region Back-End: Gets

    @classmethod
    def __getUI(self, _lMenu: list, _bBreakOnInvalid: bool) -> int:
        """
        """

        #   STEP 0: Local variables
        #   STEP 1: Setup - Local Variables
        #   STEP 2: User Input
        while (True):
            #   STEP 3: Output menu
            for i in range(0, len(_lMenu)):
                print("\t" + str(i) + ": " + _lMenu[i])
                
            print("")
            
            #   STEP ..: Wait for user input
            ui = input("\t>")
            os.system("cls")

            #   STEP 4: Verify input to be type integer
            try:
                #   STEP 5: Try to cast to int
                ui = int(ui)

                #   STEP 6: Check that the int is in range
                if ((ui >= 0) and (ui < len(_lMenu))):
                    #   STEP 7: Return
                    return ui
                
                elif (_bBreakOnInvalid):
                    return -1

                else:
                    #   STEP 8: Not in range
                    print("Rae {" + Helga.time() + "} - Invalid Input")

            except:
                if (_bBreakOnInvalid):
                    break

                print("Rae (Menu-UI) {" + Helga.time() + "} - Invalid Input")

        return -1

    #
    #   endregion

    #
    #endregion

#
#endregion