#region --- Imports ---
import json
import os

from helpers.GeneralHelpers import Helga
#endregion

class Conny:
    #region --- Private ---
    def __init__(self):
        self.data = None
        return

    #
    #endregion

    #region --- Public ---
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

        # --- Variables ---
        json_file = None
        file_path = ""

        # --- Setup ---
        if (("full_path" in kwargs) and (kwargs["full_path"])):
            file_path = _sFileName
        else:
            file_path = os.path.abspath(".") + "/config/" + _sFileName
            
        # --- Do ---
        try:
            with open(file_path) as json_file:
                self.data = json.load(json_file)

        except Exception as ex:
            print("An error occured in Config.importData: " + str(ex))

        finally:
            if (json_file != None):
                json_file.close()
                json_file = None

        return
    
    #
    #endregion