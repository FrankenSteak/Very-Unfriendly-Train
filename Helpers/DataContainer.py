#region Imports

from    enum                            import Enum

import  copy                            as cp
import  json                            as js
import  numpy                           as np
import  os
import  random                          as rn
import  sys

sys.path.append(os.path.abspath("."))

from    Code.Enums.Enums                import Enums        as en

from    Helpers.Config                  import Conny
from    Helpers.GeneralHelpers          import Helga

#endregion

#region Class - Data Container

class Data:

    #region Init

    """
        Description:

            This class contains all the data required by a surrogate model for
            training and testing.
    """

    def __init__(self):

        #region STEP 0: Local variables

        self.__enum             = en.Data
        self.__cf               = Conny()
        self.__cf.load(self.__enum.value)

        #endregion

        #region STEP 1: Private variables

        #   region STEP 1.1: Data Range

        self.__fLower           = self.__cf.data["parameters"]["data range"]["lower"]
        self.__fUpper           = self.__cf.data["parameters"]["data range"]["upper"]
        self.__fCenter          = self.__cf.data["parameters"]["data range"]["center"]

        #   endregion

        #   region STEP 1.2: Data

        self.__iLen                 = 0

        self.__iUniqueOutputs       = None

        self.__iRequests            = 0

        self.__lInput               = None
        self.__lOutput              = None
        self.__lClass               = None

        self.__lUsedInput           = None
        self.__lUsedOutput          = None
        self.__lUsedClass           = None

        self.__lMap_Input           = None
        self.__lMap_Output          = None

        #   endregion

        #   region STEP 1.3: Bools

        self.__bAllowTesting        = self.__cf.data["parameters"]["allow testing"]

        #   endregion

        #endregion

        #region STEP 2: Public variables

        self.bShowOutput    = self.__cf.data["parameters"]["show output"]

        #endregion

        #   STEP 3: Return
        return

    #
    #endregion

    #region Front-End
    
    #   region Front-End: Import-Export

    def importData(self, **kwargs) -> None:
        """
            Description:

                Imports a Data() instance from a previous .json export.

            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:

                + file  = ( str ) The file to import
                    ~ Required

                + full_path = ( bool ) Flag for if the full path was used

                + extension = ( bool ) Flag for if the file extension was added
                    to the <file> variable
        """

        #   STEP 0: Local variables
        cfTmp                   = Conny()

        sFilePath               = None

        #   STEP 1: Setup - Local variables

        #   region STEP 2->3: Argument checking
        
        #   STEP 2: Check if file was passed
        if ("file" not in kwargs):
            #   STEP 3: Error handling
            raise Exception("An error occured in Data.exportData() -> Step 2: No file argument passed")

        #
        #   endregion
        
        #   STEP 4: Safety first
        try:
            #   STEP 5: Check if full path in kwargs
            if ("full_path" in kwargs):
                #   STEP 6: Check if full path
                if (kwargs["full_path"] == True):
                    #   STEP 7: Set path
                    sFilePath = kwargs["file"]

            #   STEP 8: Check if file not set
            if (sFilePath == None):
                #   STEP 9: Get full path
                sFilePath = os.path.abspath(".") + "\\Data\\DataSets\\" + kwargs["file"]

                #   STEP 10: Check if extension in kwargs
                if ("extension" in kwargs):
                    #   STEP 11: Check if extension not set
                    if (kwargs["extension"] == False):
                        #   STEP 12: Add extension to file path
                        sFilePath = sFilePath + ".json"

            #   STEP 13: Import config file
            cfTmp.load(sFilePath)

            #   STEP 14: Populate data
            self.__fLower           = cfTmp.data["data"]["lower"]
            self.__fUpper           = cfTmp.data["data"]["upper"]
            self.__fCenter          = cfTmp.data["data"]["center"]
            self.__iLen             = cfTmp.data["data"]["len"]
            self.__iRequests        = cfTmp.data["data"]["requests"]
    
            self.__lUsedInput       = cfTmp.data["input"]["used"]
            self.__lUsedOutput      = cfTmp.data["output"]["used"]
            self.__lUsedClass       = cfTmp.data["class"]["used"]
    
            self.__lInput           = cfTmp.data["input"]["unused"]
            self.__lOutput          = cfTmp.data["output"]["unused"]
            self.__lClass           = cfTmp.data["class"]["unused"]    
    
            self.bShowOutput        = cfTmp.data["show output"]

            #   STEP 15: Check used input lists not None
            if (self.__lUsedInput == None):
                self.__lUsedInput = []

            if (self.__lUsedOutput == None):
                self.__lUsedOutput = []

            if (self.__lUsedClass == None):
                self.__lUsedClass = []

        except Exception as ex:
            #   STEP 16: Error handling
            print("Initial Error: ", ex)
            raise Exception("An error occured in Data.importData() -> Step 14")

        #   STEP 17: Return
        return

    def txtImportData(self, **kwargs) -> None:
        """
            Description:

                Imports data from a text file.

            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:

                + file  = ( str ) The name of the file to import the data from
                    ~ Required

                + output_range  = ( list/str ) The indexes in the txt file for
                    the output data
                    ~ Ex: "first", "last", [2,4]
                    ~ Required

                + separator = ( str ) Data delimiting value
                    ~ Default = ","

                + expand_output = ( bool ) Flag to indicate if data should be
                    expanded
                    ~ Default = True

                + full_path = ( bool ) Flag to specify if full path was used in
                    <file> variable

                + extension = ( str ) The file extension, in the case that it
                    was not append to the <file> variable

                + automap   = ( bool ) Flag to indiciate whether or not auto
                    mapping of data should occur after import
        """

        #   STEP 0: Local variables
        sFilePath               = None

        sSep                    = ","
        bExpandOutput           = True

        #   STEP 1: Setup - Local variables

        #   region  STEP 2->9: Arguments checks

        #   STEP 2: Check if file passed
        if ("file" not in kwargs):
            #   STEP 3: Error handling
            raise Exception("An error occured in Data.txtImportData() -> Step 2: No file passed")

        #   STEP 4: Check if output range passed
        if ("output_range" not in kwargs):
            #   STEP 5: Error handling
            raise Exception("An error occured in Data.txtImportData() -> Step 5: No output range specified")

        #   STEP 6: Check if separator passed
        if ("separator" in kwargs):
            #   STEP 7: Update separator variable
            sSep = kwargs["separator"]

        #   STEP 8: Check if expand_output passed
        if ("expand_output" in kwargs):
            #   STEP 9: Update bExpandOutput
            bExpandOutput = kwargs["expand_output"]

        #
        #   endregion

        #   region STEP 10->24: Import

        #   STEP 10: Be safe OwO
        try:
            #   STEP 11: Check if full path specified
            if ("full_path" in kwargs):
                #   STEP 12: Check if full path
                if (kwargs["full_path"] == True):
                    #   STEP 13: Set file path
                    sFilePath = kwargs["file"]

            #   STEP 14: If not full path
            if (sFilePath == None):
                #   STEP 15: Set full file path
                sFilePath = os.path.abspath(".") + "\\Data\\DataSets\\" + kwargs["file"]

                #   STEP 16: Check if extension has been added
                if ("extension" in kwargs):
                    #   STEP 17: Append extension to file path
                    sFilePath = sFilePath + kwargs["extension"]

            #   STEP 18: Populate temp dictionary
            dTmp = {
                "path":     sFilePath,
                "sep":      sSep,
                "oRange":   kwargs["output_range"],
                "expand":   bExpandOutput
            }

            #   STEP 19: Outsource importing
            self.__importFromTxt__(dTmp)

            #   STEP 20: Check if auto mapping specified
            if ("automap" in kwargs):
                #   STEP 21: Check if should auto map
                if (kwargs["automap"] == True):
                    #   STEP 22: Outsource auto mapping
                    self.autoMapData()

            #   STEP 23: Set data length
            self.__iLen = len(self.__lInput)

        except Exception as ex:
            #   STEP 24: Error handling
            print("Initial error:", ex)
            raise Exception("An error occured in Data.txtImportData() -> Step 24")

        #
        #   endregion

        #   STEP 25: Return
        return

    def exportData(self, **kwargs) -> None:
        """
            Description:

                Exports this data container instance to file.

            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:

                + file  = ( str ) The file path to export to
                    ~ Required

                + full_path = ( bool ) Flag for if the full file path was
                    provided

                + extension = ( str ) The file extension in the scenario that
                    the <file> variable doesn't have it included
        """

        #   STEP 0: Local variables
        dTmp                    = {}

        jsFile                  = None

        sFilePath               = None

        #   STEP 1: Setup - Local variables

        #   region STEP 2->3: Argument checking
        
        #   STEP 2: Check if file was passed
        if ("file" not in kwargs):
            #   STEP 3: Error handling
            raise Exception("An error occured in Data.exportData() -> Step 2: No file argument passed")

        #
        #   endregion
        
        #   STEP 3: Safety first
        try:
            #   STEP 4 Check if full path in kwargs
            if ("full_path" in kwargs):
                #   STEP 5: Check if full path
                if (kwargs["full_path"] == True):
                    #   STEP 6: Set path
                    sFilePath = kwargs["file"]

            #   STEP 7: Check if file not set
            if (sFilePath == None):
                #   STEP 8: Get full path
                sFilePath = os.path.abspath(".") + "\\Data\\DataSets\\" + kwargs["file"]

                #   STEP 9: Check if extension in kwargs
                if ("extension" in kwargs):
                    #   STEP 10: Add extension to file path
                    sFilePath = sFilePath + kwargs["extension"]

            #   STEP 11: Check if file exists
            if (os.path.exists(sFilePath) == True):
                #   STEP 12: Error handling
                raise Exception("An error occured in Data.exportData -> Step 3: A file with that name already exists")

            #   STEP 13: Populate the temp dictionary
            dTmp["data"] = {
                "lower":    self.__fLower,
                "upper":    self.__fUpper,
                "center":   self.__fCenter,
                "len":      self.__iLen,
                "requests": self.__iRequests
            }

            dTmp["input"] = {
                "used":     self.__lUsedInput,
                "unused":   self.__lInput
            }

            dTmp["output"] = {
                "used":     self.__lUsedOutput,
                "unused":   self.__lOutput
            }

            dTmp["class"] = {
                "used":     self.__lUsedClass,
                "unused":   self.__lClass
            }

            dTmp["show output"] = self.bShowOutput

            #   STEP 14: Create the file
            jsFile = open(sFilePath, "a")
            jsFile.close()
            jsFile = None

            #   STEP 15: Open the file
            with open(sFilePath, "r+") as jsFile:
                #   STEP 16: Dump the data to the file
                js.dump(dTmp, jsFile, indent=4, separators=(", ", " : "))

        except Exception as ex:
            #   STEP 17: Error handling
            print("Initial Error: ", ex)
            raise Exception("An error occured in Data.exportData")
        
        #   STEP 18: Return
        return

    #
    #   endregion

    #   region Front-End: Sets

    def setData(self, **kwargs) -> None:
        """
            Description:

                Sets the data for this class to the provided data

            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:

                + data  = ( dict ) Dictionary containing the new data for this
                    class
                    ~ Required

                + automap   = ( bool ) Flag to indicate if automapping should
                    occur after setting class data lists

                + transpose = ( bool ) Flag to indicate if the dataset shoul be
                    transposed after initialization
        """

        #   STEP 0: Local variables

        #   STEP 1: Setup - Local variables

        #   STEP 2: Check if data arg passed
        if ("data" not in kwargs):
            #   STEP 3: Error handling
            raise Exception("An error occured in Data.setData() -> Step 2: No data arugment passed")

        #   STEP 5: Outsource - Ensure all data points are lists
        self.__setDataLists__(data=kwargs["data"])
        
        #   STEP 6: Update - Class variables
        self.__lInput       = kwargs["data"]["in"]
        self.__lOutput      = kwargs["data"]["out"]
        self.__lClass       = []

        self.__lUsedInput   = []
        self.__lUsedOutput  = []
        self.__lUsedClass   = []

        #   STEP 10: Check if trnapose arg passed
        if ("transpose" in kwargs):
            #   STEP 11: Check if tranpose
            if (kwargs["transpose"]):
                #   STEP 12: Transpose data
                self.__lInput   = np.ndarray.tolist(np.transpose(self.__lInput))
                self.__lOutput  = np.ndarray.tolist(np.transpose(self.__lOutput))
        
        #   STEP 7: Check if automap argument passed
        if ("automap" in kwargs):
            #   STEP 8: Check if automap set
            if (kwargs["automap"] == True):
                #   STEP 9: Outsource automapping
                self.autoMapData()

        #   STEP 13: Set data length
        self.__iLen = len(self.__lInput)

        #   STEP 14: Return
        return

    def setLength(self, **kwargs) -> None:
        """
            Description:

                Limits the length of the data in the class to the specified
                value.

            |\n
            |\n
            |\n
            |\n
            |\n
            
            Arguments:

                + length    = ( int ) The length to which the data should be
                    limited
                    ~ Required
        """

        #   STEP 0: Local variables
        #   STEP 1: Setup - Local variables

        #   STEP 2: Check if length argument passed
        if ("length" not in kwargs):
            #   STEP 3: Error handling
            raise Exception("An error occured in Data.setLength() -> Step 2: No length argument passed")

        #   STEP 4: reset data to ensure the random values popped aren't biased
        self.__resetData__()

        #   STEP 5: Check if length less than current length
        if (kwargs["length"] < self.__iLen):
            #   STEP 6: Pop current len - specified len number of samples randomly
            for _ in range(0, self.__iLen - kwargs["length"]):
                #   STEP 7: Pop
                self.getRandDNR()

            #   STEP 8: Clear the used lists
            self.__lUsedInput   = []
            self.__lUsedOutput  = []
            self.__lUsedClass   = []

            #   STEP 9: Reset the class length
            self.__iLen = kwargs["length"]

        #   STEP 10: Return
        return
    
    def setNumUniqueOutputs(self) -> None:
        """
            Description:

                Updates this instance's number of unique outputs.
        """

        #   STEP 0: Local variables
        #   STEP 1: Setup - Local variables

        #   STEP 2: Do the thing
        self.__iUniqueOutputs = len(self.getUniqueOutputs())

        #   STEP 3: Return
        return
        
    #
    #   endregion

    #   region Front-End: Gets

    #       region Front-End-(Gets): Data width and length

    def getLen(self) ->  int:
        """
            Description:

                Returns the length of the data used by this Data instance.

            |\n
            |\n
            |\n
            |\n
            |\n
            
            Returns:

                + iLength   = ( int ) The length of the data used by this Data
                    instance
        """

        #   STEP 0: Local variables
        #   STEP 1: Setup - Local variables

        #   STEP 2: Check that class has been initialized
        if (self.__lInput == None):
            #   STEP 3: Error handling
            raise Exception("An error occured in Data.getLen() -> Step 2: Data instance has not been initialized")

        #   STEP 4: Return
        return self.__iLen

    def getCurrLen(self) -> int:
        """
            Description:

                Returns the current length of the data used by this Data
                instance.

            |\n
            |\n
            |\n
            |\n
            |\n

            Returns:

                + iLength   = ( int ) The current length of the data used by
                    this Data instance
        """

        #   STEP 0: Local variables
        #   STEP 1: Setup - Local variables

        #   STEP 2: Check that class has been initialized
        if (self.__lInput == None):
            #   STEP 3: Error handling
            raise Exception("An error occured in Data.getCurrLen() -> Step 2: Data instance has not been initialized")

        #   STEP 4: Return
        return len(self.__lInput)
    
    def getInputWidth(self) -> int:
        """
            Description:

                Returns the width of the input data in this Data instance.

            |\n
            |\n
            |\n
            |\n
            |\n

            Returns:

                + iWidth    = ( int ) The width of the input data in this Data
                    instance
        """

        #   STEP 0: Local variables

        #   STEP 1: Setup - Local variables

        #   STEP 2: Check that class is initialized
        if (self.__lInput == None):
            #   STEP 3: Error handling
            raise Exception("An error occured in Data.getInputWidth -> Step 2: Input data not initialized")
        
        #   STEP 4: Check if all input data not in used
        if ((len(self.__lInput) == 0) and (len(self.__lUsedInput) > 0)):
            #   STEP 5: Reset data
            self.__resetData__()

        #   STEP 6: Check that used and unused aren't empty
        elif ((len(self.__lInput) == 0) and (len(self.__lUsedInput) == 0)):
            #   STEP 7: Error handling
            raise Exception("An error occured in Data.getInputWidth() -> Step 6: All input lists empty")

        #   STEP 8: Be safe
        try:
            #   STEP 9: Return
            return len(self.__lInput[0])

        except Exception as ex:
            #   STEP 10: Error handling
            print("Initial error: ", ex)
            print("\tAttemptint to rectify error")

            #   STEP 11: Outsource - Turn data points into single balue lists
            self.__setDataLists__(isSelf=True)

        #   STEP 12: Return
        return 1

    def getOutputWidth(self) -> int:
        """
            Description:

                Returns the width of the output data in this Data instance.

            |\n
            |\n
            |\n
            |\n
            |\n

            Returns:

                + iWidth    = ( int ) The width of the output data in this Data
                    instance
        """

        #   STEP 0: Local variables
        #   STEP 1: Setup - Local variables

        #   STEP 2: Check if class initialized
        if (self.__lOutput == None):
            #   STEP 3: Error handling
            raise Exception("An error occured in data.getOutputWidth -> Step 2: Output data not initialized")
        
        #   STEP 4: Be safe
        try:
            #   STEP 5: Return
            return len(self.__lOutput[0])

        except:
            #   STEP 6: Outsource - Turn data points into single value lists
            self.__setDataLists__(isSelf=True)

            #   STEP 7: Return
            return 1

    #
    #       endregion

    #       region Front-End-(Gets): Data maps

    def getDataRange(self) -> dict:
        """
            Description:

                Returns the data range of this Data instance as a dictionary.

            |\n
            |\n
            |\n
            |\n
            |\n

            Returns:

                + dRange        = ( dict ) The data range of this Data instance
                    ~ lower     = ( float ) The lower bound
                    ~ center    = ( float ) The center point
                    ~ upper     = ( float ) The upper bound
        """

        #   STEP 0: Local variables
        dOut                    = {}

        #   STEP 1: Setup - Local variables

        #   STEP 2: Populate output dictionary
        dOut["lower"]   = self.__fLower
        dOut["upper"]   = self.__fUpper
        dOut["center"]  = self.__fCenter

        #   STEP 3: Return
        return dOut
    
    def getInputMap(self) -> vars:
        """
            Description:

                If the input data for this dataset has been mapped then the
                mapping data will be returned.
        """

        #   STEP 0: Local variables

        #   STEP 1: Setup - Local variables

        #   STEP 2: Check if map doesn't exist
        if (self.__lMap_Input == None):
            #   STEP 3: Return nothing
            return None

        #   STEP 4: Return map
        return self.__lMap_Input

    def getOutputMap(self) -> vars:
        """
            Description:

                If the output data for this dataset has been mapped then the
                mapping data will be returned.
        """

        #   STEP 0: Local variables

        #   STEP 1: Setup - Local variables

        #   STEP 2: Check if map doesn't exist
        if (self.__lMap_Output == None):
            #   STEP 3: Return nothing
            return None

        #   STEP 4: Return map
        return self.__lMap_Output

    def getOutputMin(self, index: int) -> float:
        """
            Description:

                Iterates through the output data to find the smalles output
                data sample.

            |\n
            |\n
            |\n
            |\n
            |\n
            
            Parameters:

                + index = ( int ) The index in the output of the minimum that
                    is being searched for
        """

        #   STEP 0: Local variables
        fOut                    = np.inf

        #   STEP 1: Setup - Local variables

        #   STEP 2: Loop through outputs
        for i in range(0, len( self.__lOutput )):
            #   STEP 3: Check if smaller than current minimum
            if (self.__lOutput[i][index] < fOut):
                #   STEP 4: Update output
                fOut    = self.__lOutput[i][index]

        #   STEP 5: Loop through used outputs
        for i in range(0, len( self.__lUsedOutput )):
            #   STEP 6: Check if smaller than current minimum
            if (self.__lUsedOutput[i][index] < fOut):
                #   STEP 7: Update output
                fOut    = self.__lUsedOutput[i][index]

        #   STEP 8: Return
        return fOut

    def getInputDistance(self, index: int) -> list:
        """
            Description:

                Gets the euclidian distance of each input from the specified
                input given that the input is in range.
        """

        #   STEP 0: Local variables
        lOut                    = []

        lInput                  = None

        #   STEP 1: Setup - Local variables
        self.reset()

        #   region STEP 2->6: Error checking

        #   STEP 2: Check that there is data in input
        if ( len( self.__lInput ) > 0):
            #   STEP 3: Check index in range
            if ( index >= len( self.__lInput )):
                #   STEP 4: Error handling
                raise Exception("An error occured in Data.getInputDistance() -> Step 3: Index out of range")
        
        #   STEP 5: No input list
        else:
            #   STEP 6: Error handling
            raise Exception("An error occured in Data.getInputDistance() -> Step 5: No input list for dataset")

        #
        #   endregion

        #   STEP 7: Update - Local variables
        lInput  = self.__lInput[index]

        #   STEP 8: Loop through inputs
        for i in range(0, len(self.__lInput)):
            #   STEP 9: Setup - Scope variables
            fTmp_Sum    = 0.0

            #   STEP 10: Check input isn't reference index
            if (i != index):
                #   STEP 11: Loop through input
                for j in range(0, len(lInput)):
                    #   STEP 12: Check inputs not none
                    if ((lInput[j] != None) and (self.__lInput[i][j] != None)):
                        #   STEP 13: Get distance of point
                        fTmp_Point  = np.square(lInput[j] - self.__lInput[i][j])

                        #   STEP 14: Add to sum
                        fTmp_Sum    += fTmp_Point

            #   STEP 15: Root the sum
            fTmp_Sum    = round( np.sqrt(fTmp_Sum), 4 )

            #   STEP 16: Append to list
            lOut.append(fTmp_Sum)
            
        #   STEP 17: Return
        return lOut
        
    #
    #       endregion    
    
    #       region Front-End-(Gets): Data samples

    def getDNR(self, **kwargs) -> dict:
        """
            Description:

                Returns the data input and output values of the specified
                index.

            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:
            
                + index = ( int ) The index of the data to be returned
                    ~ Required

            |\n

            Returns:

                + dData = ( dict ) The specified data
                    ~ in    = ( list ) The specified input data
                    ~ out   = ( list ) The specified output data
                    ~ class = ( list ) The specified class data
        """

        #   STEP 0: Local variables
        dOut                    = None

        lTmpIn                  = None
        lTmpOut                 = None
        lTmpClass               = None

        #   STEP 1: Setup - Local variables

        #   STEP 2: Check if index arg passed
        if ("index" not in kwargs):
            #   STEP 3: Error handling
            raise Exception("An error occured in Data.getDNR() -> Step 2: No index argument passed")

        #   STEP 4: Check if data needs to be reset
        if (len(self.__lInput) == 0):
            self.__resetData__()

        #   STEP 5: Check if index in range
        if (kwargs["index"] < len(self.__lInput)):

            #   region STEP 6->14: Get data

            #   STEP 6: Be safe
            try:
                #   STEP 7: Get input data
                lTmpIn = self.__lInput.pop(kwargs["index"])
            
            except Exception as ex:
                #   STEP 8: Error handling
                print("Initial Error: ", ex)
                raise Exception("An error occured in Data.getDNR() -> Step 6")

            #   STEP 9: Be safe
            try:
                #   STEP 10: Get output data
                lTmpOut = self.__lOutput.pop(kwargs["index"])

            except Exception as ex:
                #   STEP 11: Error handling
                print("Initial Error: ", ex)
                raise Exception("An error occured in Data.getDNR() -> Step 9")

            #   STEP 12: Be safe
            try:
                #   STEP 13: Get class data
                lTmpClass = self.__lClass.pop(kwargs["index"])

            except Exception as ex:
                #   STEP 14: Error handling
                #ToDo
                #print("Initial Error: ", ex)
                #raise Exception("An error occured in Data.getDNR() -> Step 12")
                Helga.nop()
            
            #
            #   endregion

            #   STEP 15: Add data to used lists
            self.__lUsedInput.append(lTmpIn)
            self.__lUsedOutput.append(lTmpOut)
            self.__lUsedClass.append(lTmpClass)

            #   STEP 16: Increment request counter
            self.__iRequests += 1

            #   STEP 17: Populate output dictionary
            dOut = {
                "in":       lTmpIn,
                "out":      lTmpOut,
                "class":    lTmpClass
            }

            #   STEP 18: Return
            return dOut

        else:
            #   STEP 19: Error handling
            raise Exception("An error occured in Data.getDNR() -> Step 5: Data index out of bounds")

    def getRandDNR(self) -> dict:
        """
            Description:

                Returns the input and output data of a random index in this
                Data instance's data lists.

            |\n
            |\n
            |\n
            |\n
            |\n
                        
            Returns:

                + dData = ( dict ) The specified data  
                    ~ in    = ( list ) The specified input data  
                    ~ out   = ( list ) The specified output data  
                    ~ class = ( list ) The specified class data  
        """

        #   STEP 0: Local variables
        iIndex                  = None

        #   STEP 1: Setup - Local variables

        #   STEP 2: Check if reset required
        if ((len(self.__lInput) == 0) and (len(self.__lUsedInput) > 0)):
            #   STEP 3: Reset data
            self.__resetData__()

        #   STEP 4: Check if class not initialized
        elif ((len(self.__lInput) == 0) and (len(self.__lUsedInput) == 0)):
            #   STEP 5: Error Handling
            raise Exception("An error occured in Data.getRandDNR() -> Step 4: Class not initialized")

        #   STEP 6: Get a random index
        iIndex = rn.randint(0, len(self.__lInput) - 1)

        #   STEP 7: Outsource - Return
        return self.getDNR(index=iIndex)

    #
    #   endregion

    #       region Front-End-(Gets): Unique outputs

    def getUniqueOutputs(self) -> list:
        """
            Description:

                Returns a list containing all the unque outpus in this dataset.

            |\n
            |\n
            |\n
            |\n
            |\n

            Returns:

                + lOut  = ( list ) A list containing all the unique outputs?
        """

        #   STEP 0: Local variables
        lOut                    = []

        #   STEP 1: Setup - Local variables

        #   STEP 2: Iterate through unused list
        for i in range(0, len(self.__lOutput)):
            #   STEP 3: Check if in not in list
            if (self.__lOutput[i] not in lOut):
                #   STEP 4: Append
                lOut.append(self.__lOutput[i])

        #   STEP 5: Iterate through used list
        for i in range(0, len(self.__lUsedOutput)):
            #   STEP 6: Check if not in list
            if (self.__lUsedOutput[i] not in lOut):
                #   STEP 7: Append to output
                lOut.append(self.__lUsedOutput[i])

        #   STEP 8: Return
        return lOut

    def getNumUniqueOutputs(self) -> int:
        """
            Description:
            
                Returns the number of unique outputs in this dataset.

            |\n
            |\n
            |\n
            |\n
            |\n

            Returns:

                iOut    = ( int )
        """

        #   STEP 0: Local variables
        #   STEP 1: Setup - Local variables

        #   STEP 2: Check if private class var not set
        if (self.__iUniqueOutputs == None):
            #   STEP 3: Init var
            self.__iUniqueOutputs = len(self.getUniqueOutputs())

        #   STEP 4: Return
        return self.__iUniqueOutputs
    
    #
    #       endregion
    
    #
    #   endregion

    #   region Front-End: Resets

    def reset(self) -> None:
        """
            Description:

                Resets this Data instance's data lists while keeping the data.
        """

        #   STEP 0: Local variables
        #   STEP 1: Setup - Local variables

        #   STEP 2: Outsource
        self.__resetData__()

        #   STEP 3: Return
        return
    
    #
    #   endregion

    #   region Front-End: Data-Manipulation

    def autoMapData(self) -> None:
        """
            Description:

                Maps the data of the input and output data lists of this Data
                instance to fall between [-1, 1] with a center value of 0.
        """

        #   STEP 0: Local variables
        dRange                  = None

        dMap                    = None

        #   STEP 1: Setup - Local variables
        dMap                    = self.__getDefaultMap__(isSelf=True, inValue=0, outValue=0)

        #   STEP 2: Populate temp dictionary
        dRange = {
            "lower": -1.0,
            "center": 0.0,
            "upper": 1.0
        }

        #   STEP 3: Outsource
        self.mapData(range=dRange, map=dMap)

        #   STEP 4: Return
        return
    
    def mapData(self, **kwargs) -> None:
        """
            Description:

                Maps the data in this class to the specified range using the
                provided data map.

            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:

                + mapRange  = ( dict ) Dictionary containing the ranges to 
                    which this Data instance's data lists should be mapped
                    ~ Required

                    ~ lower     = ( float ) The lower bound of the data
                    ~ center    = ( float ) The center point of the data
                    ~ upper     = ( float ) The upper bound of the data

                + mapSets   = ( dict ) Dictionary containing the mappings for 
                    the input and output data of this class
                    ~ Required

                    ~ in    = ( list ) Input data mapping
                    ~ out   = ( list ) Output data mapping

                + input = ( bool ) A flag that indicates whether or not the
                    input data in this class should be mapped
                    ~ Default: False

                + output    = ( bool ) A flag that indicates whether or not the
                    output data in this class should be mapped
                    ~ Default: False

                + min   = ( dict ) The list of minimums for the data
                    ~ Note: If not provided the min will be the current minimum
                        of the dataset

                    ~ "input":
                        {
                            "( int )":  ( list ),
                        }
                    ~ "output":
                        {
                            "( int )":  ( list ),
                        }

                + max   = ( dict ) The list of maximums for the data
                    ~ Note: If not provided the max will be the current maximum
                        of the dataset

                    ~ "input":
                        {
                            "( int )":  ( list ),
                        }
                    ~ "output":
                        {
                            "( int )":  ( list ),
                        }
        """

        #   STEP 0: Local variables
        dMin_Input              = None
        dMin_Output             = None

        dMax_Input              = None
        dMax_Output             = None

        lRange_Input            = []
        lRange_Output           = []

        lMap_Input              = None
        lMap_Output             = None

        bInput                  = False
        bOutput                 = False

        #   STEP 1: Setup - Local variables

        #   region STEP 2->7: Error checking

        #   STEP 2: Check if class initialized
        if ((self.__lInput == None) or (self.__lOutput == None)):
            #   STEP 3: Error handling
            raise Exception("An error occured in Data.mapData() -> Step 2: Class not initialized")

        #   STEP 4: Check if range passed
        if ("mapRange" not in kwargs):
            #   STEP 5: Error handling
            raise Exception("An error occured in Data.mapData() -> Step 4: No mapRange argument passed")

        #   STEP 6: Check if map passed
        if ("mapSets" not in kwargs):
            #   STEP 7: Error handling
            raise Exception("An error occured in Data.mapData() -> Step 6: No mapSets argument passed")
        
        #
        #   endregion

        #   region STEP 8->13: Update flags

        #   STEP 8: Check if input arg passed
        if ("input" in kwargs):
            #   STEP 9: Check if input
            if (kwargs["input"] == True):
                #   STEP 10: Update - Local variables
                bInput = True

        #   STEP 11: Check if output arg passed
        if ("output" in kwargs):
            #   STEP 12: Check if output
            if (kwargs["output"] == True):
                #   STEP 13: Update - Local variables
                bOutput = True

        #
        #   endregion
        
        #   region STEP 14->29: Map input data

        #   STEP 14: Check if input
        if (bInput):

            #   region STEP 15->19: Variable update

            #   STEP 15: Update - Local variables
            lMap_Input   = kwargs["mapSets"]["in"]

            #   STEP 16: Check if min arg passed
            if ("min" in kwargs):
                #   STEP 17: Update - Input min var
                dMin_Input = kwargs["min"]["input"]

            #   STEP 18: Check if max arg passed
            if ("max" in kwargs):
                #   STEP 19: Update - Input max var
                dMax_Input = kwargs["max"]["input"]

            #
            #   endregion

            #   region STEP 20->26: Build input data ranges list

            #   STEP 20: Set global input data range
            lRange_Input.append([np.inf, -1.0 * np.inf, 0.0, 0])

            #   STEP 21: Iterate through inputs
            for i in range(0, len(lMap_Input)):
                #   STEP 22: Be safe
                try:
                    #   STEP 23: Checc if input value is not global
                    if (lMap_Input[i] != 0):
                        #   STEP 24: Check if input range matches range
                        if (lMap_Input[i] >= len(lRange_Input)):
                            #   STEP 24: Loop
                            while (len(lRange_Input) <= lMap_Input[i]):
                                #   STEP 25: Append empty mapping spot to input range
                                lRange_Input.append([np.inf, -1.0 * np.inf, 0.0, 0])

                except:
                    #   STEP 26: Assume global - append value to map
                    lMap_Input.append(0)

            #
            #   endregion

            #   region STEP 27->29: Map data

            #   STEP 27: Outsource input ranges
            lRange_Input        = self.__getDataRange__(data=self.__lInput, map=lMap_Input, range=lRange_Input, min=dMin_Input, max=dMax_Input)

            #   STEP 28: Oursource input center and width 
            lRange_Input        = self.__getDataParameters__(range=lRange_Input)

            #   STEP 29: Outsoruce input mapping
            dTmp_Data           = self.__getData__(dataRange=kwargs["mapRange"], data=self.__lInput, map=lMap_Input, range=lRange_Input)
            
            self.__lInput       = dTmp_Data["data"]
            self.__lMap_Input   = dTmp_Data["map"]

            #
            #   endregion

        #
        #   endregion

        #   region STEP 30->46: Map output data

        #   STEP 30: Check if output
        if (bOutput):

            #   region STEp 31->35: Variable update

            #   STEP 31: Update - Local variables
            lMap_Output = kwargs["mapSets"]["out"]

            #   STEP 32: Check if min arg passed
            if ("min" in kwargs):
                #   STEP 33: Update - Output min var
                dMin_Output = kwargs["min"]["output"]

            #   STEP 34: Check if max arg passed
            if ("max" in kwargs):
                #   STEP 35: Update - Output max var
                dMax_Output = kwargs["max"]["output"]
                
            #
            #   endregion
        
            #   region STEP 36->43: Build output data ranges list

            #   STEP 36: Set global output data range
            lRange_Output.append([np.inf, -1.0 * np.inf, 0.0, 0])

            #   STEP 37: Iterate through outputs
            for i in range(0, len(lMap_Output)):
                #   STEP 38: Be safe
                try:
                    #   STEP 39: Check if output is not global
                    if (lMap_Output[i] != 0):
                        #   STEP 40: Check if output range matches range
                        if (lMap_Output[i] >= len(lRange_Output)):
                            #   STEP 41: Loop
                            while ( len(lRange_Output) <= lMap_Output[i] ):
                                #   STEP 42: Append new mapping to output range
                                lRange_Output.append([np.inf, -1.0 * np.inf, 0.0, 0])

                except:
                    #   STEP 43: Assume global - append value to map
                    lMap_Output.append(0)
                    
                #
                #   endregion

            #   region STEP 44->46: Map data

            #   STEP 44: Outsource output ranges
            lRange_Output       = self.__getDataRange__(data=self.__lOutput, map=lMap_Output, range=lRange_Output, min=dMin_Output, max=dMax_Output)

            #   STEP 45: Outsource output center and width
            lRange_Output       = self.__getDataParameters__(range=lRange_Output)

            #   STEP 46: Outsource output mapping
            dTmp_Data           = self.__getData__(dataRange=kwargs["mapRange"], data=self.__lOutput, map=lMap_Output, range=lRange_Output)

            self.__lOutput      = dTmp_Data["data"]
            self.__lMap_Output  = dTmp_Data["map"]

            #
            #   endregion
        
        #
        #   endregion

        #   STEP 47: Set data range
        self.__fLower   = kwargs["mapRange"]["lower"]
        self.__fCenter  = kwargs["mapRange"]["center"]
        self.__fUpper   = kwargs["mapRange"]["upper"]
        
        #   STEP 48: Return
        return

    def remap(self, **kwargs) -> list:
        """
            Desciption:

                This function remaps a provided input to be similar to the
                input dataset before normalization.

            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:

                + candidate = ( list ) A list of inputs of the same length as
                    the current inputs for this dataset
                    ~ Required
        """

        #   STEP 0: Local variables
        lOut                    = []
        
        #   STEP 1: Setup - Local variables
        
        #   region STEP 2->7: Error checking

        #   STEP 2: Check if candidate arg passed
        if ("candidate" not in kwargs):
            #   STEP 3: Error handling
            raise Exception("An error occured in Data.remap() -> Step 2: No candidate arg passed")

        #   STEP 4: Check if candidate same length as current input
        if (len(kwargs["candidate"]) != self.getInputWidth()):
            #   STEP 5: Error handling
            raise Exception("An error occured in Data.remap() -> Step 4: The provided input is not the same length as the input length of the dataset")

        #   STEP 6: Check input map exists
        if (self.__lMap_Input == None):
            #   STEP 7: Error handling
            raise Exception("An error occured in Data.remap() -> Step 6: No input mapping for this dataset exists")

        #
        #   endregion

        #   STEP 8: Loop through input
        for i in range(0, self.getInputWidth()):
            #   STEP 9: Get new value
            fTmp    = self.__lMap_Input[i][4] + ( ( self.__lMap_Input[i][5] / 2.0 ) * kwargs["candidate"][i] )

            #   STEP 10: Append to output
            lOut.append(fTmp)

        #   STEP 11: Return
        return lOut

    def splitData(self, **kwargs) -> dict:
        """
            Description:

                Splits the data in this class into testing and training
                datasets.

            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:

                + size  = ( int ) The size of the training set.

                + percent   = ( float ) The percent of this instance's data to
                    use for the training set
                    ~ Ex: 0.1, 0.5, ...

            |\n

            Returns:

                + dData = ( dict ) Dictionary containing new Data instances
                    with split data
                    ~ training  = ( vars ) Training Data instance
                    ~ testing   = ( vars ) Testing Data instance
        """

        #   STEP 0: Local variables
        dOut                    = {}
        dTmp                    = {}

        dTrain                  = Data()
        dTest                   = Data()

        iLen                    = None

        #   STEP 1: Setup - Local variables
        self.__resetData__()

        #   STEP 2: Check if size argument passed
        if ("size" in kwargs):
            #   STEP 3: Check if size is smaller than data length
            if ((kwargs["size"] < self.__iLen) and (kwargs["size"] > 0)):
                #   STEP 4: Set length of data
                iLen = kwargs["size"]

            else:
                #   STEP 5: Error handling
                raise Exception("An error occured in Data.splitData() -> Step 3: Invalid size argument passed")

        #   STEP 6: Check if percent argument passed
        elif ("percent" in kwargs):
            #   STEP 6: Check that percent less than 1
            if ((kwargs["percent"] < 1) and (kwargs["percent"] > 0)):
                #   STEP 7: Set length of data
                iLen = int( len(self.__lInput) * kwargs["percent"] )

            else:
                #   STEP 8: Error handling
                raise Exception("An error occured in Data.splitData() -> Step 6: Invalid percent argument passed")

        else:
            #   STEP 9: Use default percent
            iLen = int( len(self.__lInput) * 0.75)

        #   STEP 10: Pop iLen data samples
        for _ in range(0, iLen):
            #   STEP 11: Pop goes the data sample
            self.getRandDNR()

        #   STEP 12: Set testing dictionary
        dTmp = {
            "in": cp.deepcopy(self.__lInput),
            "out": cp.deepcopy(self.__lOutput)
        }

        #   STEP 13: Set testing data container's data
        dTest.setData(data=dTmp)

        #   STPE 14: Set training dictionary
        dTmp = {
            "in": cp.deepcopy(self.__lUsedInput),
            "out": cp.deepcopy(self.__lUsedOutput)
        }

        #   STEP 15: Set training data container's data
        dTrain.setData(data=dTmp)

        #   STEP 16: Populate output dict
        dOut = {
            "training": dTrain,
            "testing":  dTest
        }

        #   STEP 17: Return
        return dOut

    #
    #   endregion

    #   region Front-End: Set-Manipulation

    def pop(self, **kwargs) -> dict:
        """
            Description:

                Removes the specified entry from this dataset and returns it.
                The class length is adjusted appropriately.

            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:

                + used  = ( bool ) A flag to indicate if the entry to be
                    removed is in the used data lists
                    ~ Required

                + index = ( int ) The index of entry to return
                    ~ Required

                + last_seen = ( bool ) Indicates if the entry to remove
                    was the last used entry.
                    ~ Overrides the requirements for the <used> and <index>
                    arguments

            |\n

            Returns:

                + dEntry    = ( dict ) Dictionary containing the specified data
                    entry
        """

        #   STEP 0: Local variables
        dOut                    = None

        lData                   = []

        #   STEP 1: Setup - Local variables

        #   STEP 2: Check if used was passed
        if ("used" in kwargs):
            #   STEP 3: Add to data list
            lData.append(kwargs["used"])

        #   STEP 4: Check if index was passed
        if ("index" in kwargs):
            #   STEP 5: Add to data list
            lData.append(kwargs["index"])

        #   STEP 6: Check if all necessarry data was passed
        if (len(lData) != 2):
            #   STEP 7: Check if last_seen was passed
            if ("last_seen" not in kwargs):
                #   STEP 8: Error handling
                raise Exception("An error occured in Data.pop() -> Step 7: No last_seen argument passed")

            else:
                #   STEP 9: Set data list
                lData = [True, len(self.__lUsedInput) - 1]

        #   STEP 10: Check if used
        if (lData[0] == True):
            #   STEP 11: Check index in range
            if ((lData[1] >= 0) and (lData[1] < len(self.__lUsedInput))):
                #   STEP 12: Populate output dictionary
                dOut = {
                    "in": self.__lUsedInput.pop(lData[1]),
                    "out": self.__lUsedOutput.pop(lData[1])
                }

                self.__lUsedClass.pop(lData[1])

        else:
            #   STEP 13: Unused list - check index in range
            if ((lData[1] >= 0) and (lData[1] < len(self.__lInput))):
                #   STEP 14: Populate output dictionary
                dOut = {
                    "in": self.__lInput.pop(lData[1]),
                    "out": self.__lOutput.pop(lData[1])
                }

                self.__lClass.pop(lData[1])

        #   STEP 15: Adjust class length
        self.__iLen -= 1

        #   STEP 17: Return
        return dOut

    def copy(self, **kwargs) -> dict:
        """
            Description:

                Copies the specified entry from this dataset and returns it.

            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:

                + used  = ( bool ) A flag to indicate if the entry to be
                    removed is in the used data lists
                    ~ Required

                + index = ( int ) The index of entry to return
                    ~ Required

                + last_seen = ( bool ) Indicates if the entry to remove
                    was the last used entry.
                    ~ Overrides the requirements for the <used> and <index>
                    arguments

            |\n

            Returns:

                + dEntry    = ( dict ) Dictionary containing the specified data
                    entry
        """

        #   STEP 0: Local variables
        dOut                    = None

        lData                   = []

        #   STEP 1: Setup - Local variables

        #   STEP 2: Check if used was passed
        if ("used" in kwargs):
            #   STEP 3: Add to data list
            lData.append(kwargs["used"])

        #   STEP 4: Check if index was passed
        if ("index" in kwargs):
            #   STEP 5: Add to data list
            lData.append(kwargs["index"])

        #   STEP 6: Check if all nec data was passed
        if (len(lData) != 2):
            #   STEP 7: Check if last_seen was passed
            if ("last_seen" not in kwargs):
                #   STEP 8: Error handling
                raise Exception("An error occured in Data.copy() -> Step 7: No last_seen argument passed")

            else:
                #   STEP 9: Set data list
                lData = [True, len(self.__lUsedInput) - 1]

        #   STEP 10: Chck if used
        if (lData[0] == True):
            #   STEP 11: Check index in range
            if ((lData[1] >= 0) and (lData[1] < len(self.__lUsedInput))):
                #   STEP 12: Populate output dictionary
                dOut = {
                    "in": cp.deepcopy(self.__lUsedInput[lData[1]]),
                    "out": cp.deepcopy(self.__lUsedOutput[lData[1]])
                }

        else:
            #   STEP 13: Unused list - check index in range
            if ((lData[1] >= 0) and (lData[1] < len(self.__lInput))):
                #   STEP 14: Populate output dictionary
                dOut = {
                    "in": cp.deepcopy(self.__lInput[lData[1]]),
                    "out": cp.deepcopy(self.__lOutput[lData[1]])
                }

        #   STEP 15: Return
        return dOut

    def insert(self, **kwargs) -> None:
        """
            Description:

                Appends the provided to the unused lists of this instance and
                adjusts the instance length appropriately

            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:

                + data  = ( dict ) The data to append
                    ~ in    = ( list ) The input data
                    ~ out   = ( list ) The output data

                    ~ Required
        """

        #   STEP 0: Local variables
        #   STEP 1: Setup - Local variables

        #   STEP 2: Check if data passed
        if ("data" not in kwargs):
            #   STEP 3: Error handling
            raise Exception("An error occured in Data.insert() -> Step 2: No data argument passed")

        #   STEP 4: Check if lists haven't been initialized
        if (self.__lInput == None):
            #   STEP 5: Init
            self.__lInput   = []
            self.__lOutput  = []
            self.__lClass   = []

            self.__lUsedInput   = []
            self.__lUsedOutput  = []
            self.__lUsedClass   = []

        #   STEP 6: Append the data
        self.__lInput.append(kwargs["data"]["in"])
        self.__lOutput.append(kwargs["data"]["out"])
        self.__lClass.append(None)

        #   STEP 7: Adjust the class length
        self.__iLen += 1

        #   STEP 8: Return
        return

    #
    #   endregion

    #   region Front-End: User Output

    def stats(self, **kwargs) -> None:
        """
        """

        #   STEP 0: Local variables
        #   STEP 1: Setup - Local variables

        #   STEP 2: ??

        if ("i" in kwargs):
            print(kwargs["i"], "\t|\t", "max:" + str(self.__iLen) + "\t", "curr:" + str(len(self.__lInput)), "used:" + str(len(self.__lUsedInput)), sep="\t")
        else:
            print("max:" + str(self.__iLen + "\t"), "curr:" + str(len(self.__lInput)), "used:" + str(len(self.__lUsedInput)), sep="\t")

        #   STEP ??: Return
        return
    #
    #   endregion

    #
    #endregion

    #region Back-End
    
    #   region Back-End: Clear
    
    def __clearClass__(self) -> None:
        """
        """

        #   STEP 0: Local variables
        #   STEP 1: Setup - Local variables

        #   STEP 2: Reset all data
        self.__fLower           = self.__cf.data["data"]["lower"]
        self.__fUpper           = self.__cf.data["data"]["upper"]
        self.__fCenter          = self.__cf.data["data"]["center"]

        self.__iLen             = 0
        self.__iRequests        = 0

        self.__lInput           = None
        self.__lOutput          = None
        self.__lClass           = None

        self.__lUsedInput       = None
        self.__lUsedOutput      = None
        self.__lUsedClass       = None

        #   STEP 3: Return
        return

    #
    #   endregion

    #   region Back-End: Resets

    def __resetData__(self) -> None:
        """
            Description:

                Resets this Data instance's data lists while keeping the data.
        """

        #   STEP 0: local variables
        #   STEP 1: Setup - Local variables

        #   STEP 2: Check that input lists initialized
        if ((self.__lInput != None) and (self.__lUsedInput != None)):
            #   STEP 3: Reset input lists
            self.__lInput.extend(self.__lUsedInput)

        #   STEP 4: Check that output lists are initialized
        if ((self.__lOutput != None) and (self.__lUsedOutput != None)):
            #   STEP 5: Reset output lists        
            self.__lOutput.extend(self.__lUsedOutput)
                
        #   STEP 6: Check that class lists are initialized
        if ((self.__lClass != None) and (self.__lUsedClass != None)):
            #   STEP 7: Reset class lists
            self.__lClass.extend(self.__lUsedClass)

        #   STEP 8: Reset used data
        self.__lUsedInput = []
        self.__lUsedOutput = []
        self.__lUsedClass = []

        #   STEP 9: Return
        return

    #
    #   endregion

    #   region Back-End: Sets

    def __setClass__(self, _lClass: list) -> None:
        """
        """

        #   STEP 0: Local variables
        #   STEP 1: Setup - Local variables

        #   STEP 2: ??

        #   STEP ??: Return
        return

    def __setDataLists__(self, **kwargs) -> dict:
        """
            Description:

                Checks to see if the data lists passed contain single value
                data points. If they do then the single data points are added
                to lists to aid data manipulation.

            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:

                + data  = ( dict ) A dictionary containing the input and output
                    data lists
                    ~ Required

                    ~ ( + isSelf )  = True bypasses this requirement
        """

        #   STEP 0: Local variables
        dOut                    = {}

        lInput                  = None
        lOutput                 = None

        #   STEP 1: Setup - Local variables

        #   STEP 2: Check if data arg passed
        if ("data" not in kwargs):            
            #   STEP 3: Check if self arg passed
            if ("isSelf" not in kwargs):
                #   STEP 4: Error handling
                raise Exception("An error occured in Data.__setDataLists() -> Step 2 & Step 3: No data or self arguments passed")

            #   STEP 5: If self set
            elif (kwargs["isSelf"] == True):
                #   STPE 6: Set variables
                lInput = self.__lInput
                lOutput = self.__lOutput

            else:
                #   STEP 7: Error handling
                raise Exception("An error occured in Data.__setDataLists() -> Step 2 & Step 3: No data or self arguments passed")

        else:
            #   STEP 8: Set variables
            lInput  = kwargs["data"]["in"]
            lOutput = kwargs["data"]["out"]

        #   STEP 9: Check if input data contains only single data point
        if (type(lInput[0]) == float):
            #   STEP 10: Iterate through input data
            for i in range(0, len(lInput)):
                #   STEP 11: Set as array
                lInput[i] = [lInput[i]]

        #   STEP 12: Check if output data contains only single data point
        if (type(lOutput[0]) == float):
            #   STEP 13: Iterate through output data
            for i in range(0, len(lOutput)):
                #   STEP 14: Set as array
                lOutput[i] = [lOutput[i]]

        #   STEP 15: Populate output dictionary
        dOut = {
            "in": lInput,
            "out": lOutput,
            "class": {}
        }

        #   STEP 16: Return
        return dOut

    #
    #   endregion

    #   region Back-End: Gets

    def __getDefaultMap__(self, **kwargs) -> dict:
        """
            Description:

                Returns the default mapping for the values provided.

            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:

                + data  = ( dict ) Dictionary containing input and output data
                    lists
                    
                    ~ Required

                    ~ in    = ( list ) Input data list
                    ~ out   = ( list ) Output data list

                    ~ ( + isSelf )  = True bypasses this requirement

                + inValue   = ( int ) The value to be used for the input map
                    ~ Default   = 0

                + outValue  = ( int ) The value to be used for the output map
                    ~ Default   = 0

            |\n

            Returns:

                + dData = ( dict ) Dictionary containing converted input and
                    output data

                    ~ in    = ( list ) Converted input data list
                    ~ out   = ( )
        """

        #   STEP 0: Local variables
        dOut                    = None

        lInputData              = None
        lOutputData             = None

        lInput                  = []
        lOutput                 = []

        iInput                  = 0
        iOutput                 = 0

        #   STEP 1: Setup - Local variables

        #   STEP 2: Check if data passed
        if ("data" not in kwargs):
            #   STEP 3: Check if isSelf was passed
            if ("isSelf" not in kwargs):
                #   STEP 4: Error handling
                raise Exception("An error occured in Data._getDefaultmap__() -> Step 2: No data or isSelf argurment passed")

            #   STEP 5: Check if isSelf is set
            elif (kwargs["isSelf"] == True):
                #   STEP 6: Set data lists
                lInputData = self.__lInput
                lOutputData = self.__lOutput

            else:
                #   STEP 7: Error handling
                raise Exception("An error occured in Data._getDefaultmap__() -> Step 7: Invalid data or isSelf argurment passed")

        else:
            #   STEP 8: Set data lists
            lInputData  = kwargs["data"]["in"]
            lOutputData = kwargs["data"]["out"]

        #   STEP 9: Check if input data is single value
        if ((type(lInputData[0]) != list) or (type(lOutputData[0]) != list)):
            #   STEP 10: Populate temp dictionary
            dTmp = {
                "in":   lInputData,
                "out":  lOutputData
            }

            #   STEP 11: Outsource - Convert data points to lists
            dTmp = self.__setDataLists__(data=dTmp)

            #   STEP 12: Set new data
            lInputData  = dTmp["in"]
            lOutputData = dTmp["out"]

        #   STEP 13: check if input value was specified
        if ("inValue" in kwargs):
            #   STEP 14: Set input value
            iInput = kwargs["inValue"]

        #   STEP 15: Check if output value was specified
        if ("outValue" in kwargs):
            #   STEP 16: Set output value
            iOutput = kwargs["outValue"]

        #   STEP 17: Iterate through input width
        for _ in range(0, len(lInputData)):
            lInput.append(iInput)

        #   STEP 18: Iterate through output width
        for _ in range(0, len(lOutputData)):
            lOutput.append(iOutput)

        #   STEP 19: Populate output dict
        dOut = {
            "in":   lInput,
            "out":  lOutput
        }

        #   STEP 20: Return
        return dOut

    def __getDataRange__(self, **kwargs) -> list:
        """
            Description:

                Finds the minimum and maximum range of the specified data list.

            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:

                + data  = ( list ) The data list
                    ~ Required

                + map   = ( list ) The mapping for the data
                    ~ Required

                + range = ( list ) The current range values for the data
                    ~ Required

                + min   = ( dict ) A dictionary that contains the minimums for
                    the current dataset
                    ~ Required, but can be None

                + max   = ( dict ) A dictionary that contains the maximums for
                    the current dataset
                    ~ Required, but can be None

            |\n

            Returns:

                + lRange    = ( list ) The minimum and maximum ranges of the
                    input data
        """

        #   STEP 0: Local variables
        dMin                    = {}
        dMax                    = {}

        lData                   = None
        lMap                    = None
        lRange                  = None

        #   STEP 1: Setup - Local variables

        #   region STEP 2->11: Error checking

        #   STEP 2: Check if data was passed
        if ("data" not in kwargs):
            #   STEP 3: Error handling
            raise Exception("An error occured in Data.__getDataRange__() -> Step 2: No data argument passed")

        #   STEP 4: Check if map was passed
        if ("map" not in kwargs):
            #   STEP 5: Error handling
            raise Exception("An error occured in Data.__getDataRange__() -> Step 5: No map argument passed")

        #   STEP 6: Check if range was passed
        if ("range" not in kwargs):
            #   STEP 7: Error handling
            raise Exception("An error occured in Data.__getDataRange__() -> Step 6: No range argument passed")
        
        #   STPE 8: Check if min arg passed
        if ("min" not in kwargs):
            #   STEP 9: Error handling
            raise Exception("An error occured in Data.__getDataRange__() -> Step 8: No min arg passed")

        #   STEP 10: Check if max arg passed
        if ("max" not in kwargs):
            #   STEP 11: Error handling
            raise Exception("An error occured in Data.__getDataRange__() -> Step 10: No max arg passed")

        #
        #   endregion
        
        #   region STEP 12->15: Update min/max
        
        #   STEP 12: Check if min is not None
        if (kwargs["min"] != None):
            #   STEP 13: Update - Local variables
            dMin = kwargs["min"]

        #   STEP 14: Check if max is not None
        if (kwargs["max"] != None):
            #   STEP 15: Update - Local variables
            dMax = kwargs["max"]

        #
        #   endregion
        
        #   STEP 16: Update - Local variables
        lRange  = kwargs["range"]
        lData   = kwargs["data"]
        lMap    = kwargs["map"]

        #   STEP 17: Iterate through data list
        for i in range(0, len(lData)):
            #   STEP 18: Update - Local and tmp vars
            lTmp_Data   = lData[i]

            #   STEP 18: Iterate through data points in data sample
            for j in range(0, len(lTmp_Data)):
                #   STEP 19: Check data value isn't None
                if (lTmp_Data[j] != None):
                    #   STEP 20: Get map point
                    iIndex = lMap[j]

                    #   STEP 21: Check if smaller than lower range
                    if (lTmp_Data[j] < lRange[iIndex][0]):
                        #   STEP 22: Set lower range
                        lRange[iIndex][0] = lTmp_Data[j]

                    #   STEP 23: Check if larger than upper range
                    if (lTmp_Data[j] > lRange[iIndex][1]):
                        lRange[iIndex][1] = lTmp_Data[j]

                    #   STEP ??: Add to mean and count
                    lRange[iIndex][2] += lTmp_Data[j]
                    lRange[iIndex][3] += 1

            #   STEP 24: Check if data parameter has min
            if (str(i) in dMin):
                #   STEP 25: Get min list
                lTmp_Min = dMin[str(i)]

                #   STEP 26: Iterate through min list
                for j in range(0, len(lTmp_Min)):
                    #   STEP 27: Check if more than min
                    if (lRange[iIndex][0] > lTmp_Min[j]):
                        #   STEP 28: Set new min
                        lRange[iIndex][0] = lTmp_Min[j]

                        #   STEP 29: Exit for loop
                        break

            #   STEP 30: Check if data parameters has max
            if (str(i) in dMax):
                #   STEP 31: Get max list
                lTmp_Max = dMax[str(i)]

                #   STEP 32: Iterate through max list
                for j in range(0, len(lTmp_Max)):
                    #   STEP 33: Check if less than max
                    if (lRange[iIndex][1] < lTmp_Max[j]):
                        #   STEP 34: Set new max
                        lRange[iIndex][1] = lTmp_Max[j]

                        #   STEP 35: Exit for loop
                        break

        #   STEP 36: Return
        return lRange

    def __getDataParameters__(self, **kwargs) -> list:
        """
            Description:

                Expands on the passed data parameter list.

            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:

                + range = ( list ) Current data minimums and maximums

            |\n

            Returns:

                + lRange    = ( list ) List containing data parameters
                    ~ min       = ( float ) Data minimum
                    ~ max       = ( float ) Data maximum
                    ~ center    = ( float ) Data center
                    ~ range     = ( float ) Range from center to either min or
                        max point
        """

        #   STEP 0: Local variables
        lRange                  = None

        #   STEP 1: Setup - Local variables

        #   STEP 2: Check if range was passed
        if ("range" not in kwargs):
            #   STEP 3: Error handling
            raise Exception("An error occured in Data.__getDataParameters__() -> Step 2: No range argument passed")

        else:
            #   STEP 4: Init local range variable
            lRange = kwargs["range"]

        #   STEP 5: Iterate through data ranges
        for i in range(0, len(lRange)):
            #   STEP 6: Get Center and range
            fRange = lRange[i][1] - lRange[i][0]
            fRange = fRange / 2.0

            fCenter = lRange[i][0] + fRange

            #   STEP 7: Append to data
            lRange[i].append(fCenter)
            lRange[i].append(fRange)

        #   STEP 8: Return
        return lRange

    def __getData__(self, **kwargs) -> dict:
        """
            Description:

                Converts the passed data to fall into the specified range.

            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:

                + dataRange = ( list ) The required range for the passed data
                    ~ Required

                    ~ lower     = ( float ) The lower bound of the data
                    ~ cetner    = ( float ) The center point for the data
                    ~ upper     = ( float ) The upper bound of the data
                
                + data  = ( list ) The data list
                    ~ Required

                + map   = ( list ) The mapping for the data list
                    ~ Required

                + range = ( list ) The current range for the data list
                    ~ Required

            Returns:

                + lData = ( list ) List of mapped data values
        """

        #   STEP 0: Local variables
        lData                   = None
        lMap                    = None
        lRange                  = None

        fCenter                 = None
        fRange                  = None

        fRangeUpper             = None
        fRangeLower             = None

        iDataWidth              = None

        lMap_Out                = []

        #   STEP 1: Setup - Local variables

        #   region STEP 2->9: Error checking

        #   STEP 2: Check if dataRange passed
        if ("dataRange" not in kwargs):
            #   STEP 3: Error handling
            raise Exception("An error occured in Data.__getData__() -> Step 2: No dataRange argument passed")

        #   STEP 5: Check if data passed
        if ("data" not in kwargs):
            #   STEP 5: Error handling
            raise Exception("An error occured in Data.__getData__() -> Step 5: No data argument passed")

        #   STEP 6: Check if map was passed
        if ("map" not in kwargs):
            #   STEP 7: Error handling
            raise Exception("An error occured in Data.__getData__() -> Step 8: No map argument passed")

        #   STEP 8: Check if range was passed
        if ("range" not in kwargs):
            #   STEP 9: Error handling
            raise Exception("An error occured in Data.__getData__() -> Step 11: No range argument passed")

        #
        #   endregion

        #   STEP 10: Setup - Class variables

        #   STEP 11: Setup - Local variables
        lData       = kwargs["data"]
        lMap        = kwargs["map"]
        lRange      = kwargs["range"]
        
        fRangeUpper = float( kwargs["dataRange"]["upper"] - kwargs["dataRange"]["center"] )
        fRangeLower = float( kwargs["dataRange"]["center"] - kwargs["dataRange"]["lower"] )
        
        iDataWidth  = len(lData[0])

        #   STEP 12: Iterate through data
        for i in range(0, len(lData)):
            #   STEP 13: Iterate through values in data point
            for j in range(0, iDataWidth):
                #   STEP 14: Check that entry is not None
                if (lData[i][j] != None):
                    #   STEP 15: Get range and center
                    lTmp_Map    = lRange[lMap[j]]

                    fCenter     = lTmp_Map[4]
                    fRange      = lTmp_Map[5]

                    #   STEP 16: Get offset
                    fOffset = lData[i][j] - fCenter

                    #   STEP 17: Check if class map not set
                    if (len(lMap_Out) == j):
                        #   STEP 18: Append current map
                        lMap_Out.append(lTmp_Map)

                    #   STEP 19: Check that range > 0
                    if (fRange == 0):
                        #   STEP 20: Set to center
                        lData[i][j] = kwargs["dataRange"]["center"]

                        continue

                    #   STEP 21: Get percentage offset
                    fOffset = fOffset / fRange

                    #   STEP 22: Scale percent offset
                    if (fOffset > 0):
                        #   STEP 23: Scale by upper data range
                        fOffset = fOffset * fRangeUpper

                    else:
                        #   STEP 24: Scale by lower data range
                        fOffset = fOffset * fRangeLower

                    #   STEP 25: Center the offset - set new data point
                    lData[i][j] = fOffset + kwargs["dataRange"]["center"]

                else:
                    #   STEP 26: Check if class map not set
                    if (len(lMap_Out) == j):
                        #   STEP 27: Get map
                        lTmp_Map    = lRange[lMap[j]]

                        #   STEP 28: Append current map
                        lMap_Out.append(lTmp_Map)

                    #   STEP 29: Set data point to center 
                    lData[i][j] = 0.0

        #   STEP 30: Populate output dict
        dOut    = {
            "data": lData,
            "map":  lMap_Out
        }

        #   STEP 31: Return
        return dOut

    #
    #   endregion

    #   region Back-End: Import
    
    def __importFromTxt__(self, _d: dict) -> None:
        """
        """

        #   STEP 0: Local variables
        fileTmp                 = None

        lData                   = None
        lInput                  = []
        lOutput                 = []

        lOutputRange            = []

        iDataWidth              = 1

        #   STEP 1: Setup - Local variables

        #   STEP 2: Be safe
        try:
            #   STEP 3: Open the file
            with open(_d["path"], "r+") as fileTmp:
                #   STEP 4: Get data
                lData = fileTmp.readlines()

            #   STEP 5: Check data length
            if (len(lData) > 1):
                #   STEP 6: Get data width
                for i in range(0, len(lData[0])):
                    if (lData[0][i] == _d["sep"]):
                        iDataWidth += 1

            else:
                #   STEP 7: Error handling
                raise Exception("An error occured in Data.__importFromTxt__() -> Step 7: Data range too small")

            #   STEP 8: Check data width
            if (iDataWidth > 2):
                #   STEP 9: Get Output range
                if (type(_d["oRange"]) != list):
                    if (_d["oRange"] == "last"):
                        lOutputRange.append(iDataWidth - 1)

                    else:
                        lOutputRange.append(0)

                else:
                    lOutputRange = _d["oRange"]

                #   STEP 10: Split data
                iOutputLower = lOutputRange[0]
                iOutputUpper = lOutputRange[len(lOutputRange) - 1]

                for i in range(0, len(lData)):
                    lTmpI = []
                    lTmpO = []
                    sData = lData[i]
                    sHold = ""
                    iCount = 0

                    #   STEP 11: Loop through characters in string
                    for j in range(0, len(sData)):
                        #   STEP 12: Check if separator
                        if (sData[j] == _d["sep"]):
                            #   STEP 13: Check if in output range
                            if ((iCount >= iOutputLower) and (iCount <= iOutputUpper)):
                                #   STEP 14: Append to output list
                                lTmpO.append(sHold)
                                sHold = ""

                            else:
                                lTmpI.append(sHold)
                                sHold = ""

                            #   STEP 13: Increment count
                            iCount += 1

                        else:
                            #   STEP 14 Add to temp string
                            sHold = sHold + sData[j]
                        
                    #   STEP 15: If last field needs to be processed
                    if (sHold != ""):
                        if ((iCount >= iOutputLower) and (iCount <= iOutputUpper)):
                            lTmpO.append(sHold)

                        else:
                            lTmpI.append(sHold)

                    #   STEP 16: Append to data lists
                    lInput.append(lTmpI)
                    lOutput.append(lTmpO)

                #   STEP 17: Outsource turning the data to float values
                lOutput = self.__txtToFloat__(lOutput, expand=_d["expand"])
                lInput = self.__txtToFloat__(lInput, expand=False)

                #   STEP 18: Set class input and output lists
                self.__lInput   = lInput
                self.__lOutput  = lOutput
                self.__lClass   = []

                self.__lUsedInput   = []
                self.__lUsedOutput  = []
                self.__lUsedClass   = []

            else:
                #   STEP 19: Error handling
                raise Exception("An error occured in Data.__importFromTxt__() -> Step 19 Data width too small")

        except Exception as ex:
            #   STEP 20: Error handling
            print("Initial Error:", ex)
            raise Exception("An error occured in Data.__importFromTxt__()")
        
        finally:
            #   STEP 21: Check file was closed
            if (fileTmp != None):
                fileTmp.close()
                fileTmp = None

        #   STEP 22: Return
        return

    def __getUnitOutput__(self, _iIndex: int, _iLen: list) -> list:
        """
        """

        #   STEP 0: Local variables
        lOut                    = []

        #   STEP 1: Setup - Local variables

        #   STEP 2: Get output list
        for i in range(0, _iLen):
            if (i == _iIndex):
                lOut.append(1.0)

            else:
                lOut.append(0.0)

        #   STEP 3: Return
        return lOut

    def __txtToFloat__(self, _lData: list, **kwargs) -> []:
        """
        """

        #   STEP 0: Local variables
        lOut                    = []
        lHold                   = None

        lDataValues             = []
        lDataTypes              = []

        bAllFloat               = True

        #   region STEP 1: Setup - Local variables

        #   STEP 1: Setup - Local variables
        lHold = self.__stripData__(_lData,value="\n")

        #       STEP 1.1: Check if data point is single
        if (type(lHold[0]) != list):
            #   STEP 1.2: Add single data value to list
            lDataTypes.append(None)

        else:
            #   STEP 1.3: Iterate through first data point and add "j" values to list
            for _ in range(0, len(lHold[0])):
                lDataTypes.append(None)

        #   endregion

        #   region STEP 2->15: Get data types

        #   STEP 2: Iterate through data list
        for i in range(0, len(lHold)):
            #   STEP 3: Check if data point is single value
            if (len(lDataValues) == 1):
                #   STEP 4: Be safe OwO
                try:
                    #   STEP 5: Cast to float
                    float(lHold[i])

                    #   STEP 6: Set data type to float
                    lDataTypes[0] = "f"

                except:
                    #   STEP 7: Not float - set data type to string
                    lDataTypes[0] = "s"

                    #   STEP 8: Exit loop and set all float flag
                    bAllFloat = False
                    break

            else:
                #   STEP 9: Iterate through data point
                for j in range(0, len(lHold[i])):
                    #   STEP 10: Check that data type isn't already "s"
                    if (lDataTypes[j] != "s"):
                        #   STEP 11: Be safe UwU
                        try:
                            #   STEP 12: Cast to float
                            float(lHold[i][j])

                            #   STEP 13: Set data type to float
                            lDataTypes[j] = "f"

                        except:
                            #   STEP 14: Not float - set data type to string
                            lDataTypes[j] = "s"

                            #   STEP 15: Clear all float flag
                            bAllFloat = False

        #   endregion

        #   STEP 2: Loop through data - get data values
        if ((bAllFloat) and (kwargs["expand"] == False)):
            #   STEP 3: If all the values are already float compatible
            for i in range(0, len(lHold)):
                lPoint = lHold[i]
                lTmp = []

                #   STEP 4: Loop through data point
                for j in range(0, len(lPoint)):
                    lTmp.append(float(lPoint[j]))

                #   STEP 5: Append to output
                lOut.append(lTmp)

        else:
            #   STEP 6: Loop through data get values
            for i in range(0, len(lHold)):
                lPoint = lHold[i]

                #   STEP 7: Loop through data point
                for j in range(0, len(lPoint)):
                    if ((lDataTypes[j] == "s") or (kwargs["expand"] == True)):
                        if (lPoint[j] not in lDataValues):
                            lDataValues.append(lPoint[j])

            #   STEP 8: Loop through data again
            iLenData = len(lDataValues)

            for i in range(0, len(lHold)):
                lPoint = lHold[i]
                lTmp = []

                #   STEP 9: Loop through point data
                for j in range(0, len(lPoint)):
                    #   STEP 10: If string
                    if (lDataTypes[j] == "s"):
                        #   STEP 11: IF expand
                        if (kwargs["expand"]):
                            lTmp.append(self.__getUnitOutput__(lDataValues.index(lPoint[j]), iLenData))

                        else:
                            lTmp.append(lDataValues.index(lPoint[j]))

                    #   STEP 12: If float
                    elif (lDataTypes[j] == "f"):
                        #   STEP 13: If expand
                        if (kwargs["expand"]):
                            lTmp.append(self.__getUnitOutput__(lDataValues.index(lPoint[j]), iLenData))

                        else:
                            lTmp.append(float(lPoint[j]))
                            
                if (len(lTmp) == 1):
                    lOut.append(lTmp[0])
                else:
                    lOut.append(lTmp)

        #   STEP ??: Return
        return lOut

    def __stripData__(self, _lData: list, **kwargs) -> []:
        """
        """

        #   STEP 0: Local variables
        lOut                    = []

        #   STEP 1: Setup - Local variables
        
        #   STEP 2: Loop through data
        for i in range(0, len(_lData)):
            lTmp = []
            lTmpData = _lData[i]

            #   STEP 3: Loop through values
            for j in range(0, len(lTmpData)):
                lTmp.append(lTmpData[j].strip(kwargs["value"]))

            #   STEP 4: Append to output list
            lOut.append(lTmp)

        #   STEP ??: Return
        return lOut

    #
    #   endregion

    #
    #endregion

#
#endregion
