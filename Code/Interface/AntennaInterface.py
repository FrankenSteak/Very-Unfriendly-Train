#region Imports

from    enum                            import Enum

import  os
import  sys

sys.path.append(os.path.abspath("."))

from    Code.Enums.Enums                import Enums            as en

from    Code.Handlers.AntennaOptimizationHandler                import Natalie

from    Code.Interface.MenuInterface    import Rae

from    Helpers.Config                  import Conny
from    Helpers.GeneralHelpers          import Helga

#endregion

#region Class - Irene

class Irene:

    #region Init

    """
    """
    
    def __init__(self):

        #region STEP 0: Local variables

        self.__enum             = en.Irene
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
        #   STEP 1: Setup - local variables
        #   STEP 2: User Output
        print("Irene (Main) {" + Helga.time() + "} - Welcome. How would you like to start the optimization process?")

        #   STEP 3: User Input
        while (True):
            ui = Rae.getUserInput(self.__enum, menu="main")
            os.system("cls")

            if (ui == 0):
                self.__newGeometry()

            elif (ui == 1):
                self.__importGeometry()

            elif (ui == 2):
                print("Irene (C-Editor) {" + Helga.time() + "} - This functionality is not implemented yet")#TODO

            elif (ui == 3):
                self.__helpMain()

            elif (ui == 4):
                print("Irene (Exit) {" + Helga.time() + "} - Bye.")
                break

        return
    
    def configEditor(self):
        """
        """

        #   STEP 0: Local variables
        #   STEP 1: Setup - Local variables
        #   STEP 2: ??

        return
    
    #
    #endregion

    #region Back-End

    #   region Back-End: Gets

    def __getFreq(self) -> list:
        """
        """

        #   STEP 0: Local variables
        cfTmp   = Conny()

        lMenu   = []
        lOut    = []

        #   STEP 1: Setup - Local variables
        cfTmp.load(self.__enum.value)

        lMenu = cfTmp.data["menus"]["frequency"]

        #   STEP 2: Get frequency menu
        for i in range(0, lMenu["items"]):
            #   STEP 3: User output
            print("Irene (NG) {" + Helga.time() + "} - Please define (" + lMenu[str(i)] + ")")

            #   STEP 4: user input
            while (True):
                #   STEP 5: Wait for input
                ui = input("\t>")
                os.system("cls")
                
                #   STEP 6: Verify input
                try:
                    #   STEP 7: Cast to float
                    ui = float(ui)

                    lOut.append(ui)
                    break

                except:
                    print("Irene (NG) {" + Helga.time() + "} - Invalid Input")

        #   STEP 8: Return
        return lOut

    def __getParams(self) -> list:
        """
        """

        #   STEP 0: Local variables
        cfTmp       = Conny()

        lMenu       = []
        lOut        = []

        #   STEP 1: Setup - Local variables
        cfTmp.load(self.__enum.value)

        lMenu = cfTmp.data["menus"]["params"]

        #   STEP 2: Iterate through params
        for i in range(0, lMenu["items"]):
            #   STEP 3: Check if substrate
            if (i == 2):
                lOut.append(self.__getSubstrate())

            elif (i == 3):
                lOut.append(self.__getSubstrateHeight())

            else:
                print("Irene (NG) {" + Helga.time() + "} - Please define (" + lMenu[str(i)] + ") {cm}")

                #   STEP 4: User input
                while (True):
                    #   STEP 5: Wait for input
                    ui = input("\t>")
                    os.system("cls")

                    #   STEP 6: Verify input
                    try:
                        #   STEP 7: Cast to float
                        ui = float(ui)

                        lOut.append(ui)
                        break

                    except:
                        print("Irene (NG) {" + Helga.time() + "} - Invalid Input")
        
        return lOut

    def __getSubstrate(self) -> float:
        """
        """

        #   STEP 0: Local variables
        uiChoice    = None

        #   STEP 1: Setup - Local variables
        #   STEP 2: User Output
        print("Irene (NG) {" + Helga.time() + "} - Would you like to specify the substrate by name per permitivitty?")

        #   STEP 3: User Input
        while (True):
            print("\t0: By Name")
            print("\t1: By permitivitty")
            print("")

            #   STEP 4: Wait for user input
            ui = input("\t>")
            os.system("cls")

            #   STEP 5: Validate input
            try:
                #   STEP 6: Cast to int
                ui = int(ui)

                #   STEP 7: Verify range
                if ((ui == 0) or (ui == 1)):
                    uiChoice = ui
                    break
                
                else:
                    print("Irene (NG) {" + Helga.time() + "} - Invalid Input")

            except:
                print("Irene (NG) {" + Helga.time() + "} - Invalid Input")

        #   STEP 8: If by value
        if (uiChoice == 1):
            #   STEP 9: User output
            print("Irene (NG) {" + Helga.time() + "} - Please choose one of the following default peremitvitties")
            
            #   STEP 10: User input
            while (True):
                #   STEP 11: Output menu
                lTmpMenu = self.__cf.data["menus"]["substrate values"]
                for i in range(0, lTmpMenu["items"]):
                    print("\t" + str(i) + ": " + str(lTmpMenu[str(i)]))
                
                print("")

                #   STEP 12: Wait for user input
                ui = input("\t>")
                os.system("cls")

                #   STEP 13: Verify input
                try:
                    #   STEP 14: Cast to int
                    ui = int(ui)

                    #   STEP 15: Verify range
                    if ((ui >= 0) and (ui < lTmpMenu["items"])):
                        return lTmpMenu[str(ui)]
                        
                    else:
                        print("Irene (NG) {" + Helga.time() + "} - Invalid Input")

                except:
                    print("Irene (NG) {" + Helga.time() + "} - Invalid Input")

        #   STEP 16: By name
        elif (ui == 0):
            #   STEP 16: User Output
            print("Irene (NG) {" + Helga.time() + "} - Please choose on of the following default substrates")

            #   STEP 17: User input
            while (True):
                #   STEP 18: Output menu
                lTmpMenu = self.__cf.data["menus"]["substrate names"]
                for i in range(0, lTmpMenu["items"]):
                    print("\t" + str(i) + ": " + lTmpMenu[str(i)])
                        
                print("")

                #   STEP 19: Wait for user input
                ui = input("\t>")
                os.system("cls")

                #   STEP 20: Verify input
                try:
                    #   STEP 21: Casst to int
                    ui = int(ui)

                    #   STEP 22: Verify range
                    if ((ui >= 0) and (ui < lTmpMenu["items"])):
                        return self.__cf.data["menus"]["substrate values"][str(ui)]
                        
                    else:
                        print("Irene0 (NG) {" + Helga.time() + "} - Invalid Input")

                except:
                    print("Irene1 (NG) {" + Helga.time() + "} - Invalid Input")

        return 0.0

    def __getSubstrateHeight(self) -> float:
        """
        """

        #   STEP 0: Local variables
        lTmpMenu = self.__cf.data["menus"]["substrate heights"]

        #   STEP 1: Setup - Local variables
        #   STEP 2: User Output
        print("Irene (NG) {" + Helga.time() + "} - Please choose one of the following default substrate heights")

        #   STEP 3: User Input
        while (True):
            #   STEP 4: Output menu
            for i in range(0, lTmpMenu["items"]):
                print("\t" + str(i) + ": " + str(lTmpMenu[str(i)]) + " {mm}")
            
            print("")

            #   STEP 5: Wait for input
            ui = input("\t>")
            os.system("cls")

            #   STEP 6: Verify input
            try:
                #   STEP 7: Cast to int
                ui = int(ui)

                #   STEP 8: Verify range
                if ((ui >= 0) and (ui < lTmpMenu["items"])):
                    return lTmpMenu[str(ui)]

                else:
                    print("Irene (NG) {" + Helga.time() + "} - Invalid Input")

            except:
                print("Irene (NG) {" + Helga.time() + "} - Invalid Input")
        
        return 0.0

    #
    #   endregion

    #   region Back-End: Antenna-Setup

    def __newGeometry(self) -> None:
        """
        """

        #   STEP 0: Local variables
        lParams     = None
        fParent     = None

        #   STEP 1: Setup - Local variables
        #   STEP 2: User Output
        print("Irene (NG) {" + Helga.time() + "} - Would you like to specify the frequency range or the parameters of the new antenna?")
        
        #   STEP 3: User Input
        while (True):
            print("\t0: Frequency Range")
            print("\t1: Parameters")
            print("\t2: ~ Help")
            print("\t3: ~ Exit")
            print("")

            #   STEP 4: Wait for user input
            ui = input("\t>")
            os.system("cls")

            #   STEP 5: Verify input
            try:
                #   STEP 6: Cast to int
                ui = int(ui)

                #   STEP 7: Verify range
                if (ui == 0):
                    #   STEP 8: Get frequency range
                    lParams = self.__getFreq()
                    fParent = "frequency"
                    
                    break

                elif (ui == 1):
                    #   STEP 9: Get geometry parameters
                    lParams = self.__getParams()
                    fParent = "params"
                    
                    break

                elif (ui == 2):
                    self.__helpNG()

                elif (ui == 3):
                    print("Irene (Main) {" + Helga.time() + "} - How would you like to continue?")
                    return

                else:
                    print("Irene (NG) {" + Helga.time() + "} - Invalid Input")

            except Exception as ex:
                print(ex)
                print("Irene (NG) {" + Helga.time() + "} - Invalid Input")
              
        #   STEP 10: Energize
        self.__optimize(lParams, parent=fParent)

        #   STEP 10: User Output
        print("Irene (Main) {" + Helga.time() + "} - How would you like to continue?")

        #   STEP 11: Return
        return

    def __importGeometry(self) -> None:
        """
        """

        #   STEP 0: Local variables
        cfTmp           = Conny()
        sPath           = None

        lOut            = []

        #   STEP 1: Setup - Local variables
        #   STEP 2: User Output
        print("Irene (IG) {" + Helga.time() + "} - Please specify the antenna geometry .json file to use.")

        #   STEP 3: User Input
        while (True):
            #   STEP 4: Wait for input
            ui = input("\t>")
            os.system("cls")

            #   STEP ..: Check for import cancel
            if (ui == "cancel"):
                print("Irene (Main) {" + Helga.time() + "} - How would you like to continue?")
                return

            #   STEP ..: Check for help requres
            if (ui == "help"):
                self.__helpIG()

            else:

                #   STEP 5: Check if input contains \\ or /
                if (("\\" in ui) or ("/" in ui)):
                    #   STEP 6: Assume full path - check existence
                    if (os.path.exists(ui)):
                        sPath = ui
                        break

                    else:
                        print("Irene (NG) {" + Helga.time() + "} - Invalid Input")

                else:
                    #   STEP 7: Check in ConfigFiles
                    sTmpPath = os.path.abspath(".") + "\\Data\\ConfigFiles\\" + ui

                    if (os.path.exists(sTmpPath)):
                        sPath = sTmpPath
                        break

                    #   STEP 8: Check Exports
                    sTmpPath = os.path.abspath(".") + "\\Data\\Exports\\Antennas\\" + ui

                    if (os.path.exists(sTmpPath)):
                        sPath = sTmpPath
                        break
                    
                    #   STEP 9: User Output
                    print("Irene (NG) {" + Helga.time() + "} - Invalid Input")

        #   STEP 10: Load the json file
        cfTmp.load(sPath)

        #   STEP 11: Append the data
        lOut.append(cfTmp.data["frequency"]["lower"])
        lOut.append(cfTmp.data["frequency"]["upper"])
        lOut.append(cfTmp.data["params"]["length"])
        lOut.append(cfTmp.data["params"]["width"])
        lOut.append(cfTmp.data["params"]["substrate height"])
        lOut.append(cfTmp.data["params"]["permitivitty"])

        #   STEP 12: Optimize using parameters
        self.__optimize(lOut, parent="import")

        #   STEP 13: User Output
        print("Irene (Main) {" + Helga.time() + "} - How would you like to continue?")

        #   STEP 14: Return
        return

    #
    #   endregion

    #   region Back-End: Antenna-Optimization

    def __optimize(self, _lParams: list, **kwargs) -> None:
        """
        """

        #   STEP 0: Local variables
        fOffset         = None
        bDefault        = None
        
        #   STEP 1: Setup - Local variables
        #   STEP 2: Check if parent was params
        if (kwargs["parent"] == "params"):
            #   STEP 3: User Output
            print("Irene (OP) {" + Helga.time() + "} - Would you like to specify the offset for the band edges from the center frequency?")

            #   STEP 4: User Input
            while (True):
                #   STEP 5: Output menu options
                print("\t0: Yes")
                print("\t1: No")
                print("")

                #   STEP 6: Wait for user input
                ui = input("\t>")
                os.system("cls")

                #   STEP 7: Verify input
                try:
                    #   STEP 8: Cast to int
                    ui = int(ui)

                    #   STEP 9: Verify range
                    if (ui == 0):
                        #   STEP 10: User Output
                        print("Irene (OP) {" + Helga.time() + "} - Please specify the offset in Hz")
                        
                        #   STEP 11: User Input
                        while (True):
                            #   STEP 11: Wait for user input
                            ui = input("\t>")
                            os.system("cls")

                            #   STEP 12: Verify input
                            try:
                                #   STEP 13: Cast to float
                                ui = float(ui)

                                fOffset = ui
                                break

                            except:
                                print("Irene (OP) {" + Helga.time() + "} - Invalid Input")

                        break

                    if (ui == 1):
                        fOffset = 100.0
                        break

                    else:
                        print("Irene (OP) {" + Helga.time() + "} - Invalid Input")

                except:
                    print("Irene (OP) {" + Helga.time() + "} - Invalid Input")

        #   STEP 2: User Output
        print("Irene (OP) {" + Helga.time() + "} - Would you like to use default configurations for this project?")

        #   STEP 3: Get some more user input
        while (True):
            print("\t0: Use Default Configurations")
            print("\t1: Don't Use Default Configurations")
            print("")

            #   STEP 4: Wait for user input
            ui = input("\t>")
            os.system("cls")

            #   STEP 5: Verify input
            try:
                #   STEP 6: Cast to int
                ui = int(ui)

                #   STEP 7: Verify range
                if (ui == 0):
                    bDefault = True
                    break
                
                elif (ui == 1):
                    bDefault = False
                    break

                else:
                    print("Irene (OP) {" + Helga.time() + "} - Invalid Input")

            except:
                print("Irene (OP) {" + Helga.time() + "} - Invalid Input")
        
        #   STEP 8: Init Natalie
        nat = Natalie(_lParams, bDefault, parent=kwargs["parent"], offset=fOffset)
        
        #   STEP 9: User Output
        print("Irene (OP) {" + Helga.time() + "} - How would you like to continue?")
        
        #   STPE 10: User Input
        while (True):
            #   STEP 11: Output menu options
            print("\t0: Start Optimization Process")
            print("\t1: ~ Edit Nat config")
            print("\t2: ~ Help")
            print("\t3: ~ Exit")
            print("")

            #   STEP 12: Wait for user input
            ui = input("\t>")
            os.system("cls")

            #   STEP 13: Verify input
            try:
                #   STEP 14: Cast to int
                ui = int(ui)

                #   STEP 15: Verify range
                if (ui == 0):
                    print("Irene (OP) {" + Helga.time() + "} - Starting Optimization Process, this could take a while.")
                    break
                
                elif (ui == 1):
                    nat.configEditor()
                    print("Irene (OP) {" + Helga.time() + "} - How would you like to continue?")

                elif (ui == 2):
                    self.__helpOP()
                    
                elif (ui == 3):
                    return
                    
                else:
                    print("Irene (OP) + {" + Helga.time() + "} - Invalid Input")

            except:
                print("Irene (OP) + {" + Helga.time() + "} - Invalid Input")                

        nat.optimizeAntenna()

        return
    
    #
    #   endregion

    #   region Back-End: Output

    #       region Back-End-(Output): Help

    def __helpMain(self) -> None:
        """
        """

        #   STEP 0: Local variables
        dMenu                   = {}

        #   STEP 1: Setup - Local variables
        dMenu                   = self.__cf.data["help"]["help main"]

        #   STEP 2: User Output
        print("Irene (H-Main) {" + Helga.time() + "} - The following options exist in the Main menu.")
        for i in range(0, dMenu["items"]):
            print(dMenu[str(i)])
            
        print("")

        #   STEP 3: Wait for user to continue
        input("\t> Continue")
        os.system("cls")

        #   STEP 4: Return
        print("Irene (Main) {" + Helga.time() + "} - How would you like to continue?")
        return

    def __helpIG(self) -> None:
        """
        """

        #   STEP 0: Local variables
        dMenu                   = {}

        #   STEP 1: Setup - Local variables
        dMenu                   = self.__cf.data["help"]["help ig"]

        #   STEP 2: User Output
        print("Irene (H-IG) {" + Helga.time() + "} - The following options exist in the Antenna Import menu.")

        for i in range(0, dMenu["items"]):
            print(dMenu[str(i)])

        print("")

        #   STEP 3: Wait for the user to continue
        input("\t> Continue")
        os.system("cls")

        #   STEP 4: Return
        print("Irene (IG) {" + Helga.time() + "} - How would you like to continue?")
        return
    
    def __helpNG(self) -> None:
        """
        """

        #   STEP 0: Local variables
        dMenu                   = {}

        #   STEP 1: Setup - Local variables
        dMenu                   = self.__cf.data["help"]["help ng"]

        #   STEP 2: User Output
        print("Irene (H-NG) {" + Helga.time() + "} - The following options exist in the Antenna Creation menu.")

        for i in range(0, dMenu["items"]):
            print(dMenu[str(i)])

        print("")

        #   STEP 3: Wait for user to continue
        input("\t> Continue")
        os.system("cls")

        #   STEP 4: Return
        print("Irene (NG) {" + Helga.time() + "} - How would you like to continue?")
        return

    def __helpOP(self) -> None:
        """
        """

        #   STEP 0: Local variables
        dMenu                   = {}

        #   STEP 1: Setup - Local variables
        dMenu                   = self.__cf.data["help"]["help op"]

        #   STEP 2: User Output
        print("Irene (H-OP) {" + Helga.time() + "} - The following options exist in the Antenna Optimization menu.")

        for i in range(0, dMenu["items"]):
            print(dMenu[str(i)])

        print("")

        #   STEP 3: Wait for user to continue
        input("\t> Continue")
        os.system("cls")

        #   STEP 4: Return
        print("Irene (OP) {" + Helga.time() + "} - How would you like to continue?")
        return

    #
    #       endregion

    #
    #   endregion

    #
    #endregion

#
#endregion
