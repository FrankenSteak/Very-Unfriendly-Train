#region Imports

from    enum                            import Enum

import  os
import  sys

sys.path.append(os.path.abspath("."))

from    Enums                import Enums        as en

from    MenuInterface    import Rae
from    AntennaInterface import Irene

from    Config                  import Conny
from    GeneralHelpers          import Helga

#endregion

#region Class - Heimi

class Heimi:

    #region Init

    """
    """

    def __init__(self):

        #region STEP 0: Local variables

        self.__enum             = en.Heimi
        self.__cf               = Conny()
        self.__cf.load(self.__enum.value)

        #endregion

        #region STEP 1: Private variables

        #endregion

        #region STEP 2: Public variables
            
        #endregion

        #region STEP 3: Setup - Private variables

        #endregion

        #region STEP 4: Setup - Public variables

        #endregion

        return

    #
    #endregion

    #region Front-End

    def main(self):
        """
        """

        #   STEP 0: Local variables
        #   STEP 1: Setup - Local variables

        #   STEP 2: User Output
        print("Heimi (Main) {" + Helga.time() + "} - Hi. What program would you like to run?")

        #   STEP 3: User Input
        while (True):
            ui = Rae.getUserInput(self.__enum, menu="main")
            os.system("cls")

            if (ui == 0):
                #   STEP 4: If OMA then send to Irene
                print("Heimi (Main.OMA) + {" + Helga.time() + "} - Transferring control to Irene. See you soon.")

                irene   = Irene()
                irene.main()

                print("Hiemi (Main.OMA) + {" + Helga.time() + "} - Welcome back.")

            elif (ui == 1):
                #   STEP 5: Ha, jokes on you. There is no help for you
                print("Heimi (Main.Help) {" + Helga.time() + "} - Ummmm, really? Lol")

            elif (ui == 2):
                #   STEP 6: Exit program
                print("Heimi (Main.Exit) {" + Helga.time() + "} - Exiting program.")
                break


        #   STEP 7: Return
        return
    
    def configEditor(self) -> None:
        """
        """

        #   STEP 0: Local variables5
        #   STEP 1: Setup - Local variables

        #   STEP 2: ??

        return

    #
    #endregion

    #region Back-End

    #
    #endregion

#
#endregion

ily = Heimi()

ily.main()