#region --- Imports ---
import json as js
import os
import shutil as sh
import sys

sys.path.append(os.path.abspath("."))

from helpers.GeneralHelpers import Helga
#endregion

class Conny:
    #region --- Init ---
    def __init__(self):
        self.data = None

        return

    #
    #endregion

    #region --- Setup ---
    def load(self, _sFileName: str, **kwargs) -> None:
        """
            - Description::

                Imports the data form the provided .json file

            |\n
            |\n
            |\n
            |\n
            |\n
            - Parameters::

                :param _sFileName: >> (str) The .json file to import
                :param full_path: >> (bool) Whether or not the path provided is the full file path

            - Return::

                :returns: (None)
        """

        #   STEP 0: Local variables
        jsFile      = None
        sFilePath   = ""

        #   STEP 1: Get full file path
        if (("full_path" in kwargs) and (kwargs["full_path"])):
            sFilePath = _sFileName
        else:
            sFilePath = os.path.abspath(".") + "/config/" + _sFileName
            
        #   STEP 2: Try-catch
        try:
            #   STEP 3: Open .json file
            with open(sFilePath) as jsFile:
                #   STEP 4: Import data
                self.data = js.load(jsFile)

        except Exception as ex:
            #   STEP 5: Exception handling
            print("An error occured in Config.importData: " + str(ex))

        finally:
            #   STEP 6: Check .json file was closed
            if (jsFile != None):
                jsFile.close()
                jsFile = None

        return
    
    #
    #endregion

    #region  --- FE: Is-type Statements ---
    def hasMenu(self) -> bool:
        """
        """

        #   STEP 0: local vars
        #   STEP 1: Setup - local vars
        #   STEP 2: Check that data has been loaded
        if (self.data == None):
            raise Exception("An error occured in Conny.hasMenu() -> Step 2: No data loaded for class")

        #   STEP 3: Check if the loaded json file has a menu
        if (self.data["menus"]["items"] > 0):
            return True

        return False
    
    #
    #endregion

    #region  --- FE: Gets ---
    def getMenu(self, kwargs: dict) -> list:
        """
        """

        #   STEP 0: Local variables
        lOut                = []
        dTmp                = None

        #   STEP 1: Setup - Local variables

        #   STEP 2: Check if self containes menus
        try:
            if (self.hasMenu() == False):
                raise Exception("An error occured in Conny.getMenu -> Step 2: Config file does not contain menu")

            #   STEP 3: Check kwargs
            if (kwargs["menu"] not in self.data["menus"]):
                try:
                    #   STEP 4: Temporary variables
                    bFound  = False

                    #   STEP 5: Loop through base levels
                    for i in range(0, self.data["menus"]["items"]):
                        #   STEP 6: IF in list
                        sTmp = self.data["menus"][str(i)]

                        if (kwargs["menu"] in self.data["menus"][sTmp]):
                            #   STEP 7: Set temp list and break
                            dTmp = self.data["menus"][sTmp][kwargs["menu"]]
                            bFound = True
                            break

                    #   STEP 8: Could not find menu
                    if (bFound == False):
                        raise Exception("An error occured in Conny.getMenu -> Step 12: Could not find specified menu")

                except:
                    #   STEP 9: Error handling
                    raise Exception("An error occured in Conny.getMenu -> Step 13: Could not find specified menu")

            else:
                dTmp = self.data["menus"][kwargs["menu"]]

            #   STEP 6: Populate output list
            for i in range(0, dTmp["items"]):
                #   STEP 7: Append each menu item to the output list
                lOut.append(dTmp[str(i)])

        except Exception as ex:
            #   STEP 8: Error handling
            print(str(ex))
            raise Exception("An error occured in Conny.getMenu -> (General)")

        #   STEP 9: Return
        return lOut
    
    #
    #endregion

    #region  --- FE: Other ---
    def update(self, **kwargs) -> None:
        """
            Description:

                Updates the .json config file provided with the current data
                in this class.

            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:

                + file  = ( str ) The file to update
        """

        #   STEP 0: Local variables
        jsFile                  = None

        sPath                   = os.path.abspath(".") + "\\Data\\ConfigFiles\\"

        #   STEP 1: Setup - Local variables

        #   STEP 2: Check if file argurment was passed
        if ("file" not in kwargs):
            #   STEP 3: Error handling
            raise Exception("An error occured in Conny.update() -> Step 2: No file argument passed")

        #   STEP 4: Get full path
        sPath += kwargs["file"]

        #   STEP 5: Be safe OwO
        try:
            #   STEP 6: Check if file exists
            if (os.path.exists(sPath)):
                #   STEP 7: Delete file
                os.remove(sPath)

            #   STEP 8: Create new file
            jsFile = open(sPath, "a")

            #   STEP 9: Close file
            jsFile.close()
            jsFile = None

            #   STEP 10: Open file
            with open(sPath, "r+") as jsFile:
                #   STEP 11: Dump json data to file
                js.dump(self.data, jsFile, indent=4, separators=(", ", " : "))

        except Exception as ex:
            #   STEP 12: Error handling
            print("Initial error: ", ex)
            raise Exception("An error occured in Conny.update()")

        finally:
            #   STEP 13: Check if file not close
            if (jsFile != None):
                #   STEP 14: Close file
                jsFile.close()
                jsFile = None

        #   STEP 15: Return
        return

    #
    #endregion

#region --- Testing ---

a = Conny()
Helga.nop()

#endregion