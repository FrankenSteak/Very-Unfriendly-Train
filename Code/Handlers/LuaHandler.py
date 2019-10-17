#region Imports

from    enum                            import  Enum

import  copy                            as cp
import  os
import  shutil                          as sh
import  sys

sys.path.append(os.path.abspath("."))

from    Code.Enums.Enums                import  Enums           as en

from    Helpers.Config                  import  Conny
from    Helpers.GeneralHelpers          import  Helga

#endregion

#region Globals

#endregion

#region Class - Lana

class Lana:

    #region Init

    """
        Description:

            This class serves as a wrapper for the lua scripting language used
            in Feko.

            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:

                + name  = ( str ) The new session name

                + dir   = ( str ) The directory for the new session to be saved
                    to after completion

                + units = ( str ) The units to use as defined in the enums
                    class
    """

    def __init__(self, **kwargs) -> None:

        #region STEP 0: Local variables

        self.__enum                 = en.Lana

        self.__config               = Conny()
        self.__config.load(self.__enum.value)

        #
        #endregion

        #region STEP 1; Private variables

        self.__sAppLocation         = None

        self.__dSession             = None
        self.__dAntenna             = None

        #endregion

        #region STEP 2: Public variables

        #
        #endregion

        #region STEP 3: Setup - Private variables

        #   STEP 3.1: Get cadfeko application location
        self.__getAppDir__()

        #   STEP 3.2: Init current session
        self.__setNewSession__(args=kwargs)

        #
        #endregion

        #region STEP 4: Setup - Public variables

        #
        #endregion

        #   STEP 5: Return
        return

    #
    #endregion

    #region Front-End

    #   region Front-End: Import/Export

    def importLana(self, **kwargs) -> None:
        """
        """

        #   STEP 0: Local variables
        #   STEP 1: Setup - Local variables
        #   STEP 2: ??
        #   STEP ??: Return
        return

    def exportLana(self, **kwargs) -> None:
        """
        """

        #   STEP 0: Local variables
        #   STEP 1: Setup - Local variables
        #   STEP 2: ??
        #   STEP ??: Return
        return

    def exportLua(self, **kwargs) -> None:
        """
            Description:

                Exports the current session to a .lua file.

            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:

                + replace   = ( bool ) A flag that indicates that if the
                    current lua file already exists it should be replaced

                + run   = ( bool ) A flag that indicates whether or not the
                    current session should be run after export

                + interactive   = ( bool ) A flag that indidcates if on running
                    the current session cadfeko should be run in interactive
                    mode
                    ~ Required if <run=True>
        """

        #   STEP 0: Local variables
        vFile                   = None

        sPath                   = None
        sEnd                    = "\n"

        bReplace                = True
        bRun                    = False
        bInteractive            = False

        #   STEP 1: Setup - Local variables
        sDir    = self.__dSession["session directory"] + "\\" + self.__dSession["session name"] + "\\"
        sPath   = sDir  + self.__dSession["session name"] + ".lua"

        #   STEP 2: Check if run argument passed
        if ("run" in kwargs):
            #   STEP 3: Check if interactive argument passed
            if ("interactive" not in kwargs):
                #   STEP 4: Error handling
                raise Exception("An error occured in Lana.exportLua() -> Step 3: No interactive argument passed")

            #   STEP 5: Update local variables
            bRun            = kwargs["run"]
            bInteractive    = kwargs["interactive"]

        #   STEP 6: Be safe OwO
        try:
            #   STEP 7: Check if directory exists
            if (os.path.exists(sDir) == False):
                #   STEP 8: Create directory
                os.mkdir(sDir)

            #   STEP 9: Check if file exists
            if ((os.path.exists(sPath)) and (bReplace)):
                #   STEP 10: Remove file
                os.remove(sPath)

            elif (os.path.exists(sPath)):
                #   STEP 11: User output
                print("Lana (export lua) {" + Helga.time() + "} - File already exists and export replace flag not set")
                return

            #   STEP 12: Create file
            vFile = open(sPath, "a")

            #   STEP 13: Close file
            vFile.close()
            vFile = None

            #   STEP 14: Open file
            with open(sPath, "r+") as vFile:
                #   STEP 15: 
                vFile.write("--   STEP 0: Get application" + sEnd)
                vFile.write("   VSes_Application = cf.GetApplication()" + sEnd)
                vFile.write("--\n" + sEnd)

                #   STEP 16: Loop through projects
                for i in range(0, self.__dSession["session projects"]["items"]):
                    #   STEP 17: Get project
                    dProject = self.__dSession["session projects"][str(i)]

                    #   STEP 18: Loop through project output
                    for j in range(0, dProject["project output"]["items"]):
                        #   STEP 19: Write to file
                        vFile.write(dProject["project output"][str(j)] + sEnd)

                #   STEP 20: Close feko
                vFile.write("-- STEP ??: Close file" + sEnd)
                vFile.write("   VSes_Application:CloseAllWindows()" + sEnd)
                vFile.write("   VSes_Application:Close()" + sEnd)
                vFile.write("--" + sEnd)

        except Exception as ex:
            #   STEP 21: Error handling
            print("Initial error: ", ex)
            raise Exception("An error occured in Lana.exportLua() -> Step 21")

        finally:
            #   STEP 22: Check if file closed
            if (vFile != None):
                #   STEP ?23: Close file
                vFile.close()
                vFile = None

        #   STEP 24: Check if file should be run
        if (bRun):
            #   STEp 25: Get current directory
            sTmp_Dir    = os.path.abspath(".")

            #   STEP 26: Change directory
            os.chdir(self.__sAppLocation)

            #   STEP 27: Start command
            sCmd = ".\\cadfeko.exe "

            #   STEP 28: Check if interactive
            if (bInteractive == False):
                #   STEP 29: Add flag to command
                sCmd += " --non-interactive"

            #   STEP 30: Add script command
            sCmd += " --run-script \"" + sPath + "\"" 

            #   STEP 31: Run command
            os.system(sCmd)

            #   STEP 32: Reset directory
            os.chdir(sTmp_Dir)
            sh.rmtree(sDir)

        #   STEP ??: Return
        return

    #
    #   endregion

    #   region Front-End: Sets

    def setUnits(self, **kwargs) -> None:
        """
            Description:

                Sets the units of measurement for this lua session.

            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:

                + units = ( str ) The units of measurement to change to
                    ~ Required

                + update_config = ( bool ) Flag that determines if the change
                    should be saved to the config file 
        """

        #   STEP 0: Local variables
        bConfig                 = False

        #   STEP 1: Setup - Local variables

        #   STEP 2: Check if units argument passed
        if ("units" not in kwargs):
            #   STEP 3: Error handling
            raise Exception("An error occured in Lana.setUnits() -> Step 2: No units argument passed")

        #   STEP 4: Check if update config arguemtn passed
        if ("update_config" in kwargs):
            #   STEP 5: Set local variable
            bConfig = kwargs["update_config"]

        #   STEP 6: Verify passed units
        sTmp = en.getUnit(kwargs["units"])

        #   STEP 7: Set new unit for session
        self.__dSession["session units"] = sTmp

        #   STEP 8: Check if config file should be updated
        if (bConfig):
            #   STEP 9: Update default units
            self.__config.data["parameters"]["default units"]["default"] = sTmp

            #   STEP 10: Up date .json file
            self.__config.update(file=self.__enum.value)

        #   STEP 11: Return
        return

    def setAppDirectory(self, **kwargs) -> None:
        """
            Description:

                Updates the feko directory for this lua session.

            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:

                + dir   = ( str ) The feko directory for this lua sesison
                    ~ Required

                + update_config = ( bool ) Flag that determines if the change
                    should be saved to the config file
        """

        #   STEP 0: Local variables
        bConfig                 = False

        #   STEp 1: Setup - Local variables
        
        #   STEP 2: Check if dir argument passed
        if ("dir" not in kwargs):
            #   STEP 3: Error handling
            raise Exception("An error occured in Lana.setApplicaitonPath() -> Step 2: No dir argument passed")

        #   STEP 4: Check if update_config passed
        if ("update_config" in kwargs):
            #   STEP 5: Set local variable
            bConfig = kwargs["update_config"]

        #   STEP 6: Set new application dir for session
        self.__sAppLocation = kwargs["dir"]

        #   STEP 7: Check if config file should be updated
        if (bConfig):
            #   STEP 8: Outsource
            self.__updateConfig__(app_dir=self.__sAppLocation)

        #   STEP 9: Return
        return
        
    #
    #   endregion

    #   region Front-End: Gets

    def getSession(self, **kwargs) -> dict:
        """
            Description:

                Returns a deep copy of the current lua session.

            |\n
            |\n
            |\n
            |\n
            |\n

            Returns:

                + dSession  = ( dict ) A dictionary containg the data for the
                    current lua session
        """

        #   STEP 0: Local variables
        
        #   STEP 1: Setup - Local variables
        
        #   STEP 2: Return
        return cp.deepcopy(self.__dSession)

    def getAntenna(self, **kwargs) -> vars:
        """
            Description:

                Returns a deep copy of the current antenna.

            |\n
            |\n
            |\n
            |\n
            |\n

            Returns:

                + dAntenna  = ( dict ) A dictionary containing the data for the
                    current antenna
        """

        #   STEP 0: Local variables
        
        #   STEP 1: Setup - Local variables
        
        #   STEP 2: Check if no antenna being worked on atm
        if (self.__dAntenna == None):
            #   STEP 3: Return
            return None

        #   STEP 4: Return
        return cp.deepcopy(self.__dAntenna)
        
    #
    #   endregion

    #   region Front-End: Antenna

    def newAntenna(self, **kwargs) -> None:
        """
            Description:

                Creates a new antenna project.

            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:

                + name  = ( str ) The name for the new antenna project
                    ~ Required
        """

        #   STEP 0: Local variables
        dAntenna                = None

        #   STEP 1: Setup - Local variables
        
        #   STEP 2: Check if name argument passed
        if ("name" not in kwargs):
            #   STEP 3: Error handling
            raise Exception("An error occured in Lana.newAntenna() -> Step 2: No name argument passed")
        
        #   STEP 4: Check that there isn't already an antenna being worked on
        if (self.__dAntenna != None):
            #   STEP 5: Error handling
            raise Exception("An error occured in Lana.newAntenna() -> Step 4: There is stlil an antenna project being worked on. Please close it using Lana.closeAntenna() before creating a new antenna project")

        #   STEP 6: Create new antenna dictionary
        dAntenna = {
            "items":        4,

            "0":            "steps",
            "1":            "faces",
            "2":            "regions",
            "3":            "project name",
            "4":            "project variables",
            "5":            "project output",

            "steps":        3,
            "faces":        0,
            "regions":      0,

            "project name": kwargs["name"],

            "project variables":
            {
                "items":    0
            },

            "project output":
            {
                "items":    7,

                "0":        "-- STEP 1: Make a new project",
                "1":        "   VAnt_Project    = VSes_Application:NewProject()",
                "2":        "   VAnt_Geometry   = VAnt_Project.Geometry",
                "3":        "--\n",
                "4":        "-- STEP 2: Set project unit of measurement",
                "5":        "   VAnt_Project.ModelUnit  = cf.Enums.ModelUnitEnum." + self.__dSession["session units"],
                "6":        "--\n"
            }
        }

        #   STEP 7: Set class antenna file
        self.__dAntenna = dAntenna

        #   STEP 8: Return
        return

    def delAntenna(self, **kwargs) -> None:
        """
            Description:

                Deletes the current antenna.
        """
        
        #   STEP 0: Local variables
        #   STEP 1: Setup - Local variables
        #   STEP 2: Set local variable
        self.__dAntenna = None

        #   STEP 4: Return
        return

    def saveAntenna(self, **kwargs) -> None:
        """
            Description:

                Sets the current antenna project to save to the working
                directory.

            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:

                + dir   = ( srt ) The directory to save the projec to
                    ~ Required
        """

        #   STEP 0: Local variables
        dAnt                    = None

        sDir                    = None
        sPath                   = None

        iSteps                  = None
        iOutput                 = None

        #   STEP 1: Setup - Local variables

        #   STEP 2: Check if there is an antenna project ongoing
        if (self.__dAntenna == None):
            #   STEP 3: Error handling
            raise Exception("An error occured in Lana.saveAntenna() -> Step 2: There is no ongoing antenna project")
        
        #   STEP 4: Check if dir argument passed
        if ("dir" not in kwargs):
            #   STEP 5: Error handling
            raise Exception("An error occured in Lana.saveAntenna() -> Step 4: No dir argument passed")

        #   STEP 6: Update local variables
        dAnt        = self.__dAntenna

        iSteps      = dAnt["steps"]
        iOutput     = dAnt["project output"]["items"]

        sDir        = self.__dSession["session directory"] + "\\" + self.__dSession["session name"] + "_" + kwargs["dir"] + "\\"
        sPath       = sDir + dAnt["project name"] + ".cfx"
        sPath       = sPath.replace("\\", "/")

        #   STEP 6: Be safe OwO
        try:
            #   STEP 7: Check if directory exists
            if (os.path.exists(sDir) == False):
                #   STEP 8: Create directory
                os.mkdir(sDir)
        
        except:
                Helga.nop()

        #   STEP 10: Add the output
        dAnt["project output"][str(iOutput + 0)] =  "-- STEP " + str(iSteps) + ": Save project"
        dAnt["project output"][str(iOutput + 1)] =  "   VSes_Application:SaveAs(\"" + sPath + "\")"
        dAnt["project output"][str(iOutput + 2)] =  "--\n"

        #   STEP 11: Update antenna variables
        dAnt["steps"] += 1
        dAnt["project output"]["items"] += 3

        #   STEP 12: Return
        return

    def simulateAntenna(self, **kwargs) -> None:
        """
            Description:

                Sets the current antenna project to simulate using the provided
                arguments.

            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:

                + parallel  = ( bool ) A flag that sets if parallel
                    solving of the model is used during simulations
        """

        #   STEP 0: Local variables
        dAnt                    = None

        iSteps                  = None
        iOutput                 = None

        bParallel               = True
        
        #   STEP 1: Setup - Local variables
        
        #   STEP 2: Check if parallel argument passed
        if ("parallel" in kwargs):
            #   STEP 3: Set local variable
            bParallel = kwargs["parallel"]

        #   STEP 4: Check if there is an ongoing antenna project
        if (self.__dAntenna == None):
            #   STEP 5: Error handling
            raise Exception("An error occured in Lana.simulateAntenna() -> Step 4: There is no ongoing antenna project")

        #   STEP 6: Set local variables
        dAnt    = self.__dAntenna

        iSteps  = dAnt["steps"]
        iOutput = dAnt["project output"]["items"]

        #   STEP 7: Add the output
        dAnt["project output"][str(iOutput + 0)] =  "-- STEP " + str(iSteps) + ": Run simulation"
        dAnt["project output"][str(iOutput + 1)] =  "   VAnt_Project.Launcher.Settings.FEKO.Parallel.Enabled = " + str(bParallel).lower()
        dAnt["project output"][str(iOutput + 2)] =  "   VAnt_Project.Launcher:RunFEKO()"
        dAnt["project output"][str(iOutput + 3)] =  "--\n"

        #   STEP 8: Update antenna variables
        dAnt["steps"] += 1
        dAnt["project output"]["items"] += 4

        #   STEP 9: Return
        return

    def closeAntenna(self, **kwargs) -> None:
        """
            Description:

                Closes the current antenna project and adds it to the session.
        """
        
        #   STEP 0: Local variables
        dAnt                    = None

        iSteps                  = None
        iOutput                 = None

        #   STEP 1: Setup - Local variables
        
        #   STEP 2: Check if there is an ongoing antenna project
        if (self.__dAntenna == None):
            #   STEP 3: Error handling
            raise Exception("An error occured in Lana.closeAntenna() -> Step 2: There is no ongoing antenna project")

        #   STEP 4: Set local variable
        dAnt        = self.__dAntenna

        iSteps      = dAnt["steps"]
        iOutput     = dAnt["project output"]["items"]

        #   STEP 5: Add output
        dAnt["project output"][str(iOutput + 0)] =  "-- STEP " + str(iSteps) + ": Close project"
        dAnt["project output"][str(iOutput + 1)] =  "   VSes_Application:CloseAllWindows()"
        dAnt["project output"][str(iOutput + 2)] =  "--\n"

        #   STEP 6: Update antenna variables
        dAnt["steps"] += 1
        dAnt["project output"]["items"] += 3

        #   STEP 7: Add to session
        self.__dSession["session projects"][str(self.__dSession["session projects"]["items"])] = dAnt
        self.__dSession["session projects"]["items"] += 1

        #   STEP 8: Reset local variable
        self.__dAntenna = None

        #   STEP 9: Return
        return

    #       region Front-End-(Antenna): Sets

    def setAFrequency(self, **kwargs) -> None:
        """
            Description:

                Sets the current antenna project's simulation frequency.

            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:

                + start = ( float ) The starting frequency
                    ~ Required

                + end   = ( float ) The ending frequency
                    ~ Required

                + range_type =  ( str ) The range type that should be used
                    ~ Required
                    ~ Possibilities:
                        - "Single"
                        - "Linear"

                + samples   = ( int ) The number of discrete samples
                    ~ Required
        """

        #   STEP 0: Local variables
        dAnt                    = None

        iSteps                  = None
        iOutput                 = None

        #   STEP 1: Setup - Local variables
        
        #   region STEP 2->13: Error checking

        #   STEP 2: Check if start argument passed
        if ("start" not in kwargs):
            #   STEP 3: Error handling
            raise Exception("An error occured in Lana.setAFrequency() -> Step 2: No start argument passed")

        #   STEP 4: Check if end argument passed
        if ("end" not in kwargs):
            #   STEP 5: Error handling
            raise Exception("An error occured in Lana.setAFrequency() -> Step 4: No end argument passed")

        #   STEP 6: Check if range type argument passed
        if ("range_type" not in kwargs):
            #   STEP 7: Error handling
            raise Exception("An error occured in Lana.setAFrequency() -> Step 6: No range_type argument passed")

        #   STEP 8: Check if range_type is allowed
        if not ((kwargs["range_type"] == "Single") or (kwargs["range_type"] == "Linear")):
            #   STEP 9: Error handling
            raise Exception("An error occured in Lana.setAFrequency() -> Step 8: Invalid argument for range_type passed")

        #   STEP 10: Check if samples passed
        if ("samples" not in kwargs):
            #   STEP 11: Error handling
            raise Exception("An error occured in Lana.setAFrequency() -> Step 10: No samples argument passed")

        #   STEP 12: Check if there is an ongoing antenna project
        if (self.__dAntenna == None):
            #   STEP 13: Error handling
            raise Exception("An error occured in Lana.setAFrequency() -> Step 12: There is no ongoing antenna project")
        
        #
        #   endregion

        #   STEP 14: Set local variables
        dAnt    = self.__dAntenna

        iSteps  = dAnt["steps"]
        iOutput = dAnt["project output"]["items"]

        #   STEP 15: Check if project config is variable
        if ("VAnt_Config" not in dAnt["project variables"]):
            #   STEP 16: Add output for config file
            dAnt["project output"][str(iOutput + 0)] =  "-- STEP " + str(iSteps) + ": Get config file"
            dAnt["project output"][str(iOutput + 1)] =  "   VAnt_Config = VAnt_Project.SolutionConfigurations[1]"
            dAnt["project output"][str(iOutput + 2)] =  "--\n"

            #   STEP 17: Update anntena variables
            iSteps  += 1
            iOutput += 3

            dAnt["steps"] = iSteps
            dAnt["project output"]["items"] = iOutput

            #   STEP 18: Add variable to variable list
            dAnt["project variables"]["VAnt_Config"] = True
            dAnt["project variables"]["items"] += 1

        #   STEP 19: Add output for the frequency range
        dAnt["project output"][str(iOutput + 0)] =  "-- STEP " + str(iSteps) + ": Set frequency range"
        dAnt["project output"][str(iOutput + 1)] =  "   VAnt_tmp = VAnt_Config.Frequency:GetProperties()"
        dAnt["project output"][str(iOutput + 2)] =  "   VAnt_tmp.Start  = " + str(kwargs["start"])
        dAnt["project output"][str(iOutput + 3)] =  "   VAnt_tmp.End    = " + str(kwargs["end"])

        #   STEP 20: Check if range type is linear
        if (kwargs["range_type"] == "Linear"):
            #   STEP 21: Continue output
            dAnt["project output"][str(iOutput + 4)] =  "   VAnt_tmp.RangeType  = cf.Enums.FrequencyRangeTypeEnum.LinearSpacedDiscrete"
            dAnt["project output"][str(iOutput + 5)] =  "   VAnt_tmp.NumberOfDiscreteValues = " + str(kwargs["samples"])
            dAnt["project output"][str(iOutput + 6)] =  "   VAnt_Config.Frequency:SetProperties(VAnt_tmp)"
            dAnt["project output"][str(iOutput + 7)] =  "--\n"

            #   STEP 22: Update antenna variables
            dAnt["steps"] += 1
            dAnt["project output"]["items"] += 8

        else:
            #   STEP 23: Continue output
            dAnt["project output"][str(iOutput + 4)] =  "   VAnt_Config.Frequency:SetProperties(VAnt_tmp)"
            dAnt["project output"][str(iOutput + 5)] =  "--\n"

            #   STEP 24: Update antenna variables
            dAnt["steps"] += 1
            dAnt["project output"]["items"] += 6

        #   STEP 25: Return
        return

    def setAMesh(self, **kwargs) -> None:
        """
            Description:

                Sets the current antenna project's mesh.

            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:

                + wire_radius   = ( float ) The radius of the mesh wires
                    ~ Requried

                + size  = ( str )
                    ~ Required
                    ~ Possibilities:
                        - "Coarse"
                        - "Standard"
                        - "Fine"
        """

        #   STEP 0: Local variables
        dAnt                    = None

        iSteps                  = None
        iOutput                 = None

        #   Step 1: Setup - Local variables
        
        #   region STEP 2->9: Error checking

        #   STEP 2: Check if wire_radius argument was passed
        if ("wire_radius" not in kwargs):
            #   STEP 3: Error handling
            raise Exception("An error occured in Lana.setAMesh() -> Step 2: No wire_radius argument passed")

        #   STEP 4: Check if size argument was passed
        if ("size" not in kwargs):
            #   STEP 5: Error handling
            raise Exception("An error occured in Lana.setAMesh() -> Step 4: No size argument passed")

        #   STEP 6: Check if size argument is allowed
        if not ((kwargs["size"] == "Coarse") or (kwargs["size"] == "Standard") or (kwargs["size"] == "Fine")):
            #   STEP 7: Error handling
            raise Exception("An error occured in Lana.setAMesh() -> Step 6: Invalid size argument passed")

        #   STEP 8: Check if there is an ongoing antenna project
        if (self.__dAntenna == None):
            #   STEP 9: Error handling
            raise Exception("An error occured in Lana.setAMesh() -> Step 8: There is no ongoing antenna project")

        #
        #   endregion

        #   STEP 10: Set local variables
        dAnt                    = self.__dAntenna

        iSteps                  = dAnt["steps"]
        iOutput                 = dAnt["project output"]["items"]

        #   STEP 11: Add output
        dAnt["project output"][str(iOutput + 0)] =  "-- STEP " + str(iSteps) + ": Mesh the project"
        dAnt["project output"][str(iOutput + 1)] =  "   VAnt_Project.Mesher.Settings.WireRadius = " + str(kwargs["wire_radius"])
        dAnt["project output"][str(iOutput + 2)] =  "   VAnt_Project.Mesher.Settings.MeshSizeOption = cf.Enums.MeshSizeOptionEnum." + kwargs["size"]
        dAnt["project output"][str(iOutput + 3)] =  "   VAnt_Project.Mesher:Mesh()"
        dAnt["project output"][str(iOutput + 4)] =  "--\n"

        #   STEP 12: Update antenna variables
        dAnt["steps"] += 1
        dAnt["project output"]["items"] += 5

        #   STEP 13: Return
        return

    #
    #       endregion
        
    #       region Front-End-(Antenna): Media

    def newAMedium(self, **kwargs) -> str:
        """
            Description:

                Sets the current antenna project to create a new dielectric 
                medium using the specified parameters.

            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:

                + label = ( str ) The name for the new medium
                    ~ Required

                + permitivitty  = ( float ) The relative permitivitty of the
                    new medium
                    ~ Required

                + loss  = ( float ) The loss tangent of the new medium
                    ~ Required

            |\n
            
            Returns:

                + sMedium  = ( str ) The full name for the medium variable
        """

        #   STEP 0: Local variables
        dAnt                    = None

        sMediumName             = None

        iSteps                  = None
        iOutput                 = None

        #   STEP 1: Setup - Local variables

        #   region STEP 2->9: Error checking

        #   STEP 2: Check if label was passed
        if ("label" not in kwargs):
            #   STEP 3: Error handling
            raise Exception("An error occured in Lana.newAMedium() -> Step 2: No label argument passed")
        
        #   STEP 4: Check if permitivitty argument was passed
        if ("permitivitty" not in kwargs):
            #   STEP 5: Error handling
            raise Exception("An error occured in Lana.newAMedium() -> Step 4: No permitivitty argument passed")

        #   STEP 6: Check if loss argument was passed
        if ("loss" not in kwargs):
            #   STEP 7: Error handling
            raise Exception("An error occured in Lana.newAMedium() -> Step 6: No loss argument passed")

        #   STEP 8: Check if ther is an ongoing antenna project
        if (self.__dAntenna == None):
            #   STEP 9: Error handling
            raise Exception("An error occured in Lana.newAMedium() -> Step 8: There is no ongoing antenna project")
        
        #
        #   endregion

        #   STEP 10: Set local variables
        dAnt                    = self.__dAntenna

        iSteps                  = dAnt["steps"]
        iOutput                 = dAnt["project output"]["items"]

        sMediumName = "VAnt_Medium_" + kwargs["label"]

        #   STEP 11: Check if the medium already exists
        if (sMediumName in dAnt["project variables"]):
            #   STEP 12: Error handling
            raise Exception("An error occured in Lana.newAMedium() -> Step 11: The specified medium already exists within the context of this antenna project")

        #   STEP 12: Add output
        dAnt["project output"][str(iOutput + 0)] =  "-- STEP " + str(iSteps) + ": Creating medium"
        dAnt["project output"][str(iOutput + 1)] =  "   " + sMediumName + " = VAnt_Project.Media:AddDielectric()"
        dAnt["project output"][str(iOutput + 2)] =  "   " + sMediumName + ".Label = \"" + kwargs["label"] + "\""
        dAnt["project output"][str(iOutput + 3)] =  "   " + sMediumName + ".DielectricModelling.RelativePermittivity = " + str(kwargs["permitivitty"])
        dAnt["project output"][str(iOutput + 4)] =  "   " + sMediumName + ".DielectricModelling.LossTangent = " + str(kwargs["loss"])
        dAnt["project output"][str(iOutput + 5)] =  "--\n"

        #   STEP 13: Update antenna variables
        dAnt["steps"] += 1
        dAnt["project output"]["items"] += 6

        #   STEP 15: Add medium to antenna variables
        dAnt["project variables"][sMediumName] = kwargs["label"]
        dAnt["project variables"]["items"] += 1

        #   STEP 14: Return
        return sMediumName

    def setAFaceMedium(self, **kwargs) -> None:
        """
            Description:

                Sets the antenna project to update the medium of a face.

                Usually required for faces that aren't part of a rgion after
                using the union command.

            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:

                + medium    = ( str ) The label of the medium that should be
                    used
                    ~ Required

                + face  = ( str ) The label of the face to be changed
                    ~ Required

                + union = ( str ) The label of the union to which the above 
                    face belongs
                    ~ Required

            Elaborations:

                The feko api is trash. When you use the union modification on
                a geometry if there are surfaces that lie on a solid then the
                command deletes those surfaces and simply replaces them with
                new faces on the solid. This in turn means that it becomes 
                extremely difficult to reference those faces that have been
                replaced since we no longer know what their label is or where
                in the list of faces for the geometry they lie.

                However, if for example there were a total af 12 faces in the 
                geometry before the union operation with 3 of the faces lieing
                on the solid then after the union operation those 3 new faces
                will be named "Face13", "Face14", and "Face15". So if during
                the design process we count the amount of faces in total in
                the project and the amount of faces that lie on a solid then
                we will know which labels correspond to the intersecting faces.

                Unfortunately, it is still nigh impossible to tell which face
                is exactly which face. I think they might be ordered back to 
                front from the way they were designed. But this is merely a 
                suspicion.
        """
        
        #   STEP 0: Local variables
        dAnt                    = None

        iSteps                  = None
        iOutput                 = None

        #   STEP 1: Setup - Local variables
        
        #   region STEP 2->9: Error checking
        
        #   STEP 2: Check if medium argument passed
        if ("medium" not in kwargs):
            #   STEP 3: Error handling
            raise Exception("An error occured in Lana.setAFaceMedium() -> Step 2: No medium argument passed")

        #   STEP 4: Check if face argument passed
        if ("face" not in kwargs):
            #   STEP 5: Error handling
            raise Exception("An error occured in Lana.setAFaceMedium() -> Step 4: No face argument passed")

        #   STEP 6: Check if union argument passed
        if ("union" not in kwargs):
            #   STEP 7: Error handling
            raise Exception("An error occured in Lana.setAFaceMedium() -> Step 6: No union argument passed")

        #   STEP 8: Check if there is an ongoing antenna project
        if (self.__dAntenna == None):
            #   STEP 9: Error handling
            raise Exception("An error occured in Lana.setAFaceMedium() -> Step 8: There is no ongoing antenna project")

        #
        #   endregion
        
        #   STEP 10: Setup - Local variables
        dAnt        = self.__dAntenna

        iSteps      = dAnt["steps"]
        iOutput     = dAnt["project output"]["items"]

        #   STEP 11: Add output
        dAnt["project output"][str(iOutput + 0)] =  "-- STEP " + str(iSteps) + ": Changing face medium"
        dAnt["project output"][str(iOutput + 1)] =  "   " + kwargs["union"] + ".Faces:Item(\"" + kwargs["face"] + "\").Medium = VAnt_Project.Media:Item(\"" + kwargs["medium"] + "\")"
        dAnt["project output"][str(iOutput + 2)] =  "--\n"

        #   STEP 12: Update antenna variables
        dAnt["steps"] += 1
        dAnt["project output"]["items"] += 3

        #   STEP 13: Return
        return

    def setASolidMedium(self, **kwargs) -> None:
        """
            Description:

                Sets the antenna project to update the medium of a solid.

            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:

                + medium    = ( str ) The label of the medium to be used
                    ~ Required

                + solid = ( str ) The label of the solid to be changed
                    ~ Required
        """

        #   STEP 0: Local variables
        dAnt                    = None

        iSteps                  = None
        iOutput                 = None

        #   STEP 1: Setup - Local variables
        
        #   region STEP 2->7: Error checking

        #   STEP 2: Check if medium argument passed
        if ("medium" not in kwargs):
            #   STEP 3: Error handling
            raise Exception("An error occured in Lana.setASolidMedium() -> Step 2: No medium argument passed")

        #   STEP 4: Check if solid argument passed
        if ("solid" not in kwargs):
            #   STEP 5: Error handling
            raise Exception("An error occured in Lana.setASolidMedium() -> Step 4: No solid argument passed")

        #   STEP 6: Check if there exists an ongoing antenna project
        if (self.__dAntenna == None):
            #   STEP 7: Error handling
            raise Exception("An error occured in Lana.setASolidMedium() -> Step 6: There is not ongoing antenna project")

        #
        #   endregion

        #   STEP 8: Setup - Localv ariables
        dAnt        = self.__dAntenna

        iSteps      = dAnt["steps"]
        iOutput     = dAnt["project output"]["items"]

        #   STPE 11: Add output
        dAnt["project output"][str(iOutput + 0)] =  "-- STEP " + str(iSteps) + ": Set solid medium"
        dAnt["project output"][str(iOutput + 1)] =  "   " + kwargs["solid"] + ".Regions:Item(1).Medium = VAnt_Project.Media:Item(\"" + kwargs["medium"] + "\")"
        dAnt["project output"][str(iOutput + 2)] =  "--\n"

        #   STEP 12: Update antenna variables
        dAnt["steps"] += 1
        dAnt["project output"]["items"] += 3

        #   STEP 13: Return
        return

    #
    #       endregion
    
    #       region Front-End-(Antenna): Solids

    def newASolid(self, **kwargs) -> str:
        """
            Description:

                Sets the antenna project to create a new solid using the
                provided arguments.

            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:

                + solid = ( str ) The type of solid to create
                    ~ Required
                    ~ Possibilities:
                        - Cuboid

                + corner = ( dict ) A dictionary containing the corner points
                    for the new solid
                    ~ Required

                    ~ "x"   = ( float )
                    ~ "y"   = ( float )
                    ~ "z"   = ( float )

                + dimensions    = ( dict ) A dictionary containing the
                    dimensions for the new solid
                    ~ Required

                    ~ "l"   = ( float )
                    ~ "w"   = ( float )
                    ~ "h"   = ( float )

                + label = ( str ) The label for the new solid
                    ~ Required
        """

        #   STEP 0: Local variables

        #   STEP 1: Setup - Local variables
        
        #   region STEP 2->13: Error checking

        #   STEP 2: Check if solid argument passed
        if ("solid" not in kwargs):
            #   STEP 3: Error handling
            raise Exception("An error occured in Lana.newASolid() -> Step 2: No solid argument passed")

        #   STEP 4: Check if solid argument is valid
        if (kwargs["solid"] != "Cuboid"):
            #   STEP 5: Error handling
            raise Exception("An errror occured in Lana.newASolid() -> Step 4: Invalid solid arguemtn passed")

        #   STEP 6: Check if corner argument passed
        if ("corner" not in kwargs):
            #   STEP 7: Errro handling
            raise Exception("An error occured in Lana.newASolid() -> Step 6: No corner argument passed")

        #   STEP 8: Check if diemensions argument passed
        if ("dimensions" not in kwargs):
            #   STPE 9: Error handling
            raise Exception("An error occured in Lana.newASolid() -> Step 8: No dimensions argument passed")

        #   STEP 10: Check if label argument passed
        if ("label" not in kwargs):
            #   STEP 11: Error handling
            raise Exception("An error occured in Lana.newASolid() -> Step 10: No lable argument passed")

        #   STEP 12: Check if there exists an ongoing antenna project
        if (self.__dAntenna == None):
            #   STEP 13: Error handling
            raise Exception("An error occured in Lana.newASolid() -> Step 10: No ongoing antenna project")
        
        #
        #   endregion

        #   STEP 14: Check if cuboid
        if (kwargs["solid"] == "Cuboid"):
            #   STEP 15: Outsource
            return self.__newASolid_Cuboid__(corner=kwargs["corner"], dimensions=kwargs["dimensions"], label=kwargs["label"])

        #   STEP 16: Should never get her
        raise Exception("An error occured in Lana.newASolid() -> Step 16: Ummm, wtf?")

    #
    #       endregion

    #       region Front-End-(Antenna): Surfaces

    def newASurface(self, **kwargs) -> str:
        """
            Description

                Sets the antenna project to create a new surface using the
                provided arguments.

            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:

                + surface   = ( str ) The type of surface to create
                    ~ Requried

                    ~ Possibilities:
                        - Rectangle
                        - Polygon
                        - Ellipse

                + corner    = ( dict ) A dictionary of corners
                    ~ Required

                + dimensions    = ( dict ) A dictionary containging the
                    dimensions of the surface.
                    ~ Required  - Polygon is exception

                + label = ( str ) The label for the new surface
                    ~ Required
        """

        #   STEP 0: Local variables

        #   STEP 1: Setup - Local variables
        
        #   region STEP 2->13: Error checking

        #   STEP 2: Check if corner argument passed
        if ("corner" not in kwargs):
            #   STEP 3: Error handling
            raise Exception("An errro occured in Lana.newASurface() -> Step 2: No corner argument passed")

        #   STEP 4: Check if surface argument passed
        if ("surface" not in kwargs):
            #   STEP 5: Error handling
            raise Exception("An error occured in Lana.newASurface() -> Step 4: No surface argument passed")

        #   STEP 6: Check if surface argument is valid
        if not ((kwargs["surface"] == "Rectangle") or (kwargs["surface"] == "Polygon") or (kwargs["surface"] == "Ellipse")):
            #   STEP 7: Error handling
            raise Exception("An error occured in Lana.newASurface() -> Step 6: Invalid surface argument passed")

        #   STEP 8: Check if label passed
        if ("label" not in kwargs):
            #   STEP 9: Error handling
            raise Exception("An error occured in Lana.newASurface() -> Step 8: No label argument passed")
        
        #   STEP 10: Check if dimensions argument passed
        if ((kwargs["surface"] != "Polygon") and ("dimensions" not in kwargs)):
            #   STEP 11: Error handling
            raise Exception("An error occured in Lana.newASurface() -> Step 10: No dimensions argument passed")

        #   STEP 12: Check if there is an active antenna project
        if (self.__dAntenna == None):
            #   STEP 13: Error handling
            raise Exception("An error occured in Lana.newASurface() -> Step 12: No ongoing antenna project")

        #
        #   endregion
        
        #   STEP 14: Check if rectangle
        if (kwargs["surface"] == "Rectangle"):
            #   STEP 15: Outsource
            return self.__newASurface_Rectangle__(corner=kwargs["corner"], dimensions=kwargs["dimensions"], label=kwargs["label"])

        #   STEP 16: Check if Polygon
        if (kwargs["surface"] == "Polygon"):
            #   STEP 17: Outsource
            return self.__newASurface_Polygon__(corner=kwargs["corner"], label=kwargs["label"])

        #   STEP 18: Check if Ellipse
        if (kwargs["surface"] == "Ellipse"):
            #   STEP 19: Outsource
            return self.__newASurface_Ellipse__(corner=kwargs["corner"], dimensions=kwargs["dimensions"], label=kwargs["label"])
        
        #   STEP 20: Error handling
        raise Exception("An error occured in Lana.newASurface() -> Step 20: The fuck?")

    #
    #       endregion

    #       region Front-End-(Antenna): Curves

    def newACurve(self, **kwargs) -> str:
        """
            Description:

                Sets the antenna project to create a new curve using the
                provided arguments.

            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:

                + curve = ( str ) The type of curve to create
                    ~ Required

                    ~ Possibilities:
                        - Line
                        - PolyLine

                + corner    = ( dict ) A dictionary containing the co-ordinates
                    for the points of the curve
                    ~ Required

                + label = ( str ) The label for the new surface
                    ~ Required
        """

        #   STEP 0: Local variables

        #   STEP 1: Setup - Local variables
        
        #   region STEP 2->??: Error checking

        #   STEP 2: Check if curve argument passed
        if ("curve" not in kwargs):
            #   STEP 3: Error handling
            raise Exception("An error occured in Lana.newACurve() -> Step 2: No curve argument passed")

        #   STEP 4: Check if corner argument passed
        if ("corner" not in kwargs):
            #   STEP 5: Error handling
            raise Exception("An error occured in Lana.newACurve() -> Step 4: No corner argument passed")

        #   STEP 6: Check if label argument passed
        if ("label" not in kwargs):
            #   STEP 7: Error handling
            raise Exception("An error occured in Lana.newACurve() -> Step 6: No label argument passed")

        #   STEP 8: Check if ongoing antenna project
        if (self.__dAntenna == None):
            #   STEP 9: Error handling
            raise Exception("An error occured in Lana.newACurve() -> Step 8: No ongoing anteann project")
        
        #
        #   endregion

        #   STEP 10: Check if line
        if (kwargs["curve"] == "Line"):
            #   STEP 11: Outsource
            return self.__newACurve_Line__(corner=kwargs["corner"], label=kwargs["label"])

        #   STEP 12: Check if polyline
        if (kwargs["curve"] == "PolyLine"):
            #   STEP 13: Outsource
            return self.__newACurve_PolyLine__(corner=kwargs["corner"], label=kwargs["label"])

        #   STEP 14: Error handling
        raise Exception("An error occured in Lana.newACurve() -> Step 14: The fuck?")

    #
    #       endregion

    #       region Front-End-(Antenna): Modifications

    def newAModification(self, **kwargs) -> None:
        """
            Description:

                Sets the antenna project to create a new modification using the
                provided arguments.

            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:

                + mod   = ( str ) The type of modification to make
                    ~ Requried

                    ~ Possibilities:
                        - Union
                        - Subtract
                        - Intersect
                        - Split
                        - Stitch

                + parts = ( dict ) A dictionary containing all the geometry
                    parts to be used in the modification
                    ~ Required

                + tolerance = ( float ) The tolerance for stitching
                    modification
                    ~ Only Required by <mod="Stitch">

                + label = ( str ) The label of the new modification
                    ~ Required
        """

        #   STEP 0: Local variables

        #   STEP 1: Setup - Local variables
        
        #   region STEP 2->11: Error checking

        #   STEP 2: Check if mod argument passed
        if ("mod" not in kwargs):
            #   STEP 3: Error handling
            raise Exception("An errror occured in Lana.newAModification() -> Step 2: No mod argument passed")

        #   STEP 4: Check if parts argument passed
        if ("parts" not in kwargs):
            #   STEP 5: Error handling
            raise Exception("An error occured in Lana.newAModification() -> Step 4: No parts argument passed")

        #   STEP 6: Check if tolerance argument passed
        if ((kwargs["mod"] == "Stitch") and ("tolerance" not in kwargs)):
            #   STEP 7: Error handling
            raise Exception("An error occured in Lana.newAModification() -> Step 6: No toleracne argument passed")

        #   STEP 8: Check if an active antenna project exts
        if (self.__dAntenna == None):
            #   STEP 9: Error handling
            raise Exception("An error occured in Lana.newAModification() -> Step 8: No ongoing antenna project")
        
        #   STEP 10: Check if label argument passed
        if ("label" not in kwargs):
            #   STEP 11: Error handling
            raise Exception("An error occured in Lana.newAModificaiotn() -> Step 10: No label argument passed")

        #
        #   endregion

        #   STEP 12: Check if union
        if (kwargs["mod"] == "Union"):
            #   STEP 13: Outsource
            return self.__newAMod_Union__(parts=kwargs["parts"], label=kwargs["label"])

        #   STEP 14: Check if subtraction
        if (kwargs["mod"] == "Subtract"):
            #   STEP 15: Outsource
            return self.__newAMod_Subtraction__(parts=kwargs["parts"], label=kwargs["label"])

        #   STEP 16: Check if intersection
        if (kwargs["mod"] == "Intersect"):
            #   STEP 17: Outsource
            return self.__newAMod_Intersection__(parts=kwargs["parts"], label=kwargs["label"])

        #   STEP 18: Check if split
        if (kwargs["mod"] == "Split"):
            #   STEP 19: Outsource
            return self.__newAMod_Split__(parts=kwargs["parts"], label=kwargs["label"])

        #   STEP 20: Check if stitch
        if (kwargs["mod"] == "Stitch"):
            #   STEP 21: Outsource
            return self.__newAMod_Stitch__(parts=kwargs["parts"], tolerance=kwargs["tolerance"], label=kwargs["label"])

        #   STEP 22: Error handling
        raise Exception("An error occured in Lana.newAModification() -> Step 19: The fuck?")

    #
    #       endregion

    #       region Front-End-(Antenna): Sources

    def newASource(self, **kwargs) -> None:
        """
            Description:

                Ses the antenna project to create a new source using the
                provided arguments.

            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:

                + source     = ( str ) The type of source to create
                    ~ Required

                    ~ Possibilities:
                        - Voltage

                + port  = ( str ) The port at which the source will be located
                    ~ Requried

                + label = ( str ) The label of the new source
                    ~ Required

                + impedance = ( float ) The impedance of the source

                + magnitude = ( float ) The magnitude of the source

                + phase = ( float ) The phase of the source
        """

        #   STEP 0: Local variables
        fImpedance              = 50.0
        fMagnitude              = 1.0
        fPhase                  = 0.0

        #   STEP 1: Setup - Local variables

        #   region STEP 2->1: Error checking

        #   STEP 2: Check if source argument passed
        if ("source" not in kwargs):
            #   STEP 3: Error handling
            raise Exception("An error occured in Lana.newASource() -> Step 2: No source argument passed")

        #   STEP 4: Check if source argument is valid
        if (kwargs["source"] != "Voltage"):
            #   STEP 5: Error handling
            raise Exception("An error occured in Lana.newASource() -> Step 4: Invalid source argument passed")

        #   STEP 6: Check if port argument passed
        if ("port" not in kwargs):
            #   STEP 7: Error handling
            raise Exception("An error occured in Lana.newASource() -> Step 6: No port argument passed")

        #   STEP 8: Check if label argument passed
        if ("label" not in kwargs):
            #   STEP 9: Error handling
            raise Exception("An error occured in Lana.newASource() -> Step 8: No lable argument passed")

        #   STEP 10: Check if there is an ongoing antenna project
        if (self.__dAntenna == None):
            #   STEP 11: Error handling
            raise Exception("An error occured in Lana.newASource() -> Step 10: No ongoing antenna project")

        #
        #   endregion
        
        #   STEP 12: Check if impedance passed
        if ("impedance" in kwargs):
            #   STEP 13: Update local var
            fImpeance = kwargs["impedance"]

        #   STEP 14: Cehck if magnitude passed
        if ("magnitude" in kwargs):
            #   STEP 15: Update local var
            fMagnitued = kwargs["magnitude"]

        #   STEP 16: Check if phase passed
        if ("phase" in kwargs):
            #   STEP 17: Update local var
            fPhase = kwargs["phase"]

        #   STEP 18: Check if voltage source
        if (kwargs["source"] == "Voltage"):
            #   STEP 19: Outsource
            return self.__newASource_Voltage__(port=kwargs["port"], impedance=fImpedance, magnitude=fMagnitude, phase=fPhase, label=kwargs["label"])

        #   STEP 20: Error handling
        raise Exception("An error occured in Lana.newASource() -> Step 20: The fuck?")

    #
    #       endregion

    #       region Front-End-(Antenna): Ports

    def newAPort(self, **kwargs) -> None:
        """
            Description:

                Sets the antenna proejct to create a new port using the
                provided arguments.

            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:

                + port  = ( str ) The type of port to create
                    ~ Required

                    ~ Possibilities:
                        - Wire
                        - Edge

                + union = ( str ) The label for the union object
                    ~ Required

                + label = ( str ) The label for the new port
                    ~ Required

                + pos   = ( dict ) A dictionary containing the positivie faces
                    to be used in an edge port
                    ~ Required if <port="Edge">

                + neg   = ( dict ) A dictionary containing the negative faces
                    to be used in an edge port
                    ~ Required if <port="Edge">

                + line  = ( str ) The label of the line to be used in a wire
                    port
                    ~ Required if <port="Wire">
        """

        #   STEP 0: Local variables

        #   STEP 1: Setup - Local variables
        
        #   region STEP 2->19: Error checking

        #   STEP 2: Check if port argument passed
        if ("port" not in kwargs):
            #   STEP 3: Error handling
            raise Exception("An error occured in Lana.newAPort() -> Step 2: No port argument passed")

        #   STEP 4: Check if port argument is valid
        if not ((kwargs["port"] == "Wire") or (kwargs["port"] == "Edge")):
            #   STEP 5: Error handling
            raise Exception("An error occured in Lana.newAPort() -> Step 4: Invalid port argument passed")

        #   STEP 6: Check if union argument passed
        if ("union" not in kwargs):
            #   STEP 7: Error handling
            raise Exception("An error occured in Lana.newAPort() -> Step 6: No union argument passed")

        #   STEP 8: Check if label argument passed
        if ("label" not in kwargs):
            #   STEP 9: Error handling
            raise Exception("An error occured in Lana.newAPort() -> Step 8: No label argument passed")

        #   STEP 10: Check if wire
        if (kwargs["port"] == "Wire"):
            #   STEP 11: Check if line argument passed
            if("line" not in kwargs):
                #   STEP 12: Error handling
                raise Exception("An error occured in Lana.newAPort() -> Step 11: No line argument passed")

        #   STEP 13: Check if edge
        if (kwargs["port"] == "Edge"):
            #   STEP 14: Check if pos argument passed
            if ("pos" not in kwargs):
                #   STEP 15: Error handling
                raise Exception("An error occured in Lana.newAPort() -> Step 14: No pos argument passed")

            #   STEP 16: Check neg argument passed
            if ("neg" not in kwargs):
                #   STEP 17: Error handling
                raise Exception("An error occured in Lana.newAPort() -> Step 16: No neg argument passed")

        #   STEP 18: Check if ongoing antenna proejct
        if (self.__dAntenna == None):
            #   STEP 19: Error handling
            raise Exception("An error occured in Lana.newAPort() -> Step 18: No ongoing antenna project")
        
        #
        #   endregion

        #   STEP 20: Check if wire
        if (kwargs["port"] == "Wire"):
            #   STEP 21: Outsource
            return self.__newAPort_Wire__(union=kwargs["union"], line=kwargs["line"], label=kwargs["label"])

        #   STEP 22: Check if edge
        if (kwargs["port"] == "Edge"):
            #   STEP 23: Outsource
            return self.__newAPort_Edge__(union=kwargs["union"], pos=kwargs["pos"], neg=kwargs["neg"], label=kwargs["label"])

        #   STEP 24: Error handling
        raise Exception("An error occured in Lana.newAPort() -> Step 24: The fuck?")

    #
    #       endregion
    
    #       region Front-End-(Antenna): Requrests

    def newARequest(self, **kwargs) -> None:
        """
            Description:

                Sets the antenna project to create a new request using the
                provided arguments.

            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:

                + request   = ( str ) The type of request that can be made
                    ~ Requried

                    ~ Possibilities:
                        - FarField

                + params    = ( dict ) The dictionary that contains the values
                    to be used in the new request
                    ~ Required
        """

        #   STEP 0: Local variables

        #   STEP 1: Setup - Local variables

        #   region STEP 2->7: Error checking

        #   STEP 2: Check if request arg passed
        if ("request" not in kwargs):
            #   STEP 3: Error handling
            raise Exception("An error occured in Lana.newARequest() -> Step 2: No requeust arg passed")

        #   STPE 4: Check if params arg passed
        if ("params" not in kwargs):
            #   STEP 5: Error handling
            raise Exception("An error occured in Lana.newARequest() -> Step 4: No params arg passed")

        #   STEP 6: Check if ongoing antenna project
        if (self.__dAntenna == None):
            #   STEP 7: Error handling
            raise Exception("An error occured in Lana.newARequest() -> Step 6: No ongoing antenna project")

        #
        #   endregion
        
        #   STEP 8: Check if farfields
        if (kwargs["request"] == "FarField"):
            #   STEP 9: Outsource and return
            return self.__newARequest_FarField__(params=kwargs["params"])

        #   STEP 10: Error handling
        raise Exception("An error occured in Lana.newARequest() -> Step 10: The fuck?")

    #
    #       endregion

    #
    #   endregion

    #
    #endregion

    #region Back-End

    #   region Back-End: Init

    #
    #   endregion

    #   region Back-End: Sets

    def __setNewSession__(self, **kwargs) -> None:
        """
            Description:

                Creates a new .lua session

            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:

                + args  = ( dict ) Arguments passed from initializer
                    ~ name  = ( str ) The new session name
                    ~ dir   = ( str ) The new session working directory
                    ~ units = ( str ) The units to be used during the session
                    
        """

        #   STEP 0: Local variables
        dSession                = None
        dArguments              = None

        sSessionName            = None
        sSessionDir             = None
        sSessionUnits           = None

        #   STEP 1: Setup - Local variables

        #   region STEP 2->13: Variable acquire ment

        #   STEP 2: Check if args argument passed
        if ("args" not in kwargs):
            #   STEP 3: Error handling
            raise Exception("An error occured in Lana.__setNewSession__() -> Step 2: No args argument passed")

        else:
            #   STEP 4: Set local variable
            dArguments = kwargs["args"]

        #   STEP 5: Check if session name passed
        if ("name" not in dArguments):
            #   STEP 6: Outsource
            sSessionName = self.__getSessionName__()

        else:
            #   STEP 7: Set local variable
            sSessionName = dArguments["name"]

        #   STEP 8: Check if directory was specified
        if ("dir" not in dArguments):
            #   STEP 9: Outsource
            sSessionDir = self.__getSessionDir__()

        else:
            #   STEP 10: Set local variable
            sSessionDir = dArguments["dir"]

        #   STEP 11: Check if units were specified
        if ("units" not in dArguments):
            #   STEP 12: Outsource
            sSessionUnits = self.__getSessionUnits__()

        else:
            #   STEP 13: Set local variable
            sSessionUnits = dArguments["units"]

        #   endregion

        #   STEP 14: Set session dictionary
        dSession = {
            "items": 5,

            "0":    "session name",
            "1":    "session directory",
            "2":    "session units",
            "3":    "session variables",
            "4":    "session projects",

            "session name":         sSessionName,
            "session directory":    sSessionDir,
            "session units":        sSessionUnits,

            "session variables":
            {
                "items": 1,

                "0":    "VSes_fC",

                "VSes_fC": 2.99792458e8
            },

            "session projects":
            {
                "items": 0
            }
        }

        #   STEP 15: Set class variable
        self.__dSession = dSession

        #   STEP 16: Return
        return

    #
    #   endregion

    #   region Back-End: Gets

    def __getAppDir__(self) -> None:
        """
            Description:

                Retrieves the location of the CadFeko application from the
                config file. After retrieval the location is checked to
                ensure it is correct.

                If the location has not been set the user will be prompted
                to provide the location, and the validity of the location
                will be ensured afterwards.
        """

        #   STEP 0: Local variables
        vConny                  = Conny()
        
        #   STEP 1: Setup - Local variables
        vConny.getDirectory()

        #   STEP 2: Check if location in config file
        if (vConny.data["feko"] != ""):            
            #   STEP 3: Verify application directory
            if (os.path.exists(vConny.data["feko"])):
                #   STEP 4: Set class variable
                self.__sAppLocation = vConny.data["feko"]

                #   STEP 5: Return
                return

        #   STEP 6: Invalid directory or not set - User output
        print("Lana (Get - App Dir) {" + Helga.time() + "} - The Feko directory has not been set. Please enter it below:")

        #   STEP 7: Loop
        while (True):
            #   STEP 8: User input
            sTmp = input("\t> ")

            #   STEP 9: Clear output
            os.system("cls")

            #   STEP 10: Verify input
            if (os.path.exists(sTmp)):
                #   STEP 11: Outsoruce to front-end function
                self.__sAppLocation = sTmp

                #   STEP 12: Update config file
                self.__updateConfig__(app_dir=sTmp)

                #   STEP ??: Exit loop
                break

            else:
                #   STEP 13: User output
                print("Lana (Get - App Dir) {" + Helga.time() + "} - Invalid input. Please specify the Feko directory below.")

        #   STEP 14: Return
        return

    #       region Back-End-(Gets): Defaults

    def __getDefaultDir__(self) -> str:
        """
            Description:

                Retrieves the defautl working directory for the lua session
                from the config file.

                If the default working directory has not been set the user
                will be prompted to provide one.
        """

        #   STEP 0: Local variables
        sOut                    = None
        
        #   STEP 1: Setup - Local variables

        #   STEP 2: Check if directory in config file
        if (self.__config.data["parameters"]["working directory"]["default"] != ""):
            #   STEP 3: Verify working directory
            if (os.path.exists(self.__config.data["parameters"]["working directory"]["default"])):
                #   STEP 4: Return
                return self.__config.data["parameters"]["working directory"]["default"]

        #   STEP 5: Invalid directory or not set - User output
        print("Lana (get - default dir) {" + Helga.time() + "} - The default working directory has not been set, would you like to set it?")

        #   STEP 6: User input
        sOut = input("\t> ")

        #   STEP 7: CLear output
        os.system("cls")

        #   STEP 8: Verify input
        if ((sOut != "") and (sOut == "y")):
            #   STEP 9: User Output
            print("Lana (get - default dir) {" + Helga.time() + "} - Please enter the default working directory below")

            #   STEP 10: User input
            sOut = input("\t> ")

            #   STEP 11: Clear output
            os.system("cls")

            #   STEP 13: Update config file
            self.__updateConfig__(working_dir=sOut)

        #   STEP 14: Return
        return sOut

    def __getDefaultUnits__(self) -> str:
        """
            Description:
            
                Retrieves the default units of measurement for the lua session
                from the config file.

                If the default unit of measurement hasn't been set then someone
                fucked up :)
        """

        #   STEP 0: local variables
        sDefault                = self.__config.data["parameters"]["default units"]["default"]

        #   STEP 1: Setup - Local variables
        
        #   STEP 2: Check if default in config file
        if (sDefault != ""):
            #   STEP 3: Return
            return sDefault

        else:
            #   STEP 4: Error handling
            raise Exception("An error has occured in Lana.__getDefaultUnits__() -> Step 2: No default unit of measurement set")

        #   STEP ??: Nop
        Helga.nop()

    #
    #       endregion

    #       region Back-End-(Gets): Session

    def __getSessionName__(self) -> str:
        """
            Description:

                Prompts the user for the session name. The session name will be
                used as as the name for the .lua file.
        """

        #   STEP 0: Local variables
        sDefault                = Helga.ticks()
        sOut                    = None

        #   STEP 1: Setup - Local variables
        
        #   STEP 2: Loop
        while (True):
            #   STEP 3: User output
            print("Lana (get - Session Name) {" + Helga.time() + "} - Please specify the sesison name below")
            print("\t- Default ( Enter ): " + sDefault + "\n")

            #   STEP 4: User input
            sOut = input("\t> ")

            #   STEP 5: Clear output
            os.system("cls")

            #   STEP 6: Verify output
            if (sOut == ""):
                #   STEP 7: User ouput
                print("Lana (get - Session Name) {" + Helga.time() + "} - Are you sure you would like to use the default?")

                #   STEP 8: User input
                sTmp = input("\t> ")

                #   STEP ??: Clear output
                os.system("cls")

                #   STEP 9: Verify input
                if ((sTmp == "y") or (sTmp == "yes") or (sTmp == "")):
                    #   STEP 10: Set output
                    sOut = sDefault

                    #   STEP 11: Exit loop
                    break

            else:
                #   STEP 12: Exit loop
                break

        #   STEP 13: Append file extension
        sOut += ".lua"
        
        #   STEP 14: Return
        return sOut

    def __getSessionDir__(self) -> str:
        """
        """

        #   STEP 0: local variables
        sDefault                = self.__getDefaultDir__()
        sOut                    = None

        #   STEP 1: Setup - Local variables

        #   STEP 2: Loop
        while (True):
            #   STEP 3: User output
            print("Lana (get - Session Dir) {" + Helga.time() + "} - Please specify the session directory below")
            print("\t- Default ( Enter ): " + sDefault + "\n")

            #   STEP 4: User input
            sOut = input("\t> ")

            #   STEP 5: Clear output
            os.system("cls")

            #   STEP 6: Verify output
            if (sOut == ""):
                #   STPE 7: User output
                print("Lana (get - Session Name) {" + Helga.time() + "} - Are you sure you would like to use the default?")

                #   STEP 8: User input
                sTmp = input("\t> ")

                #   STEP 9: Clear output
                os.system("cls")

                #   STEP 10: Verify input
                if ((sTmp == "y") or (sTmp == "yes") or (sTmp == "")):
                    #   STEP 11: Set output var
                    sOut = sDefault

                    #   STEP 12: Exit loop
                    break

            else:
                #   STEP 13: Exit loop
                break

        #   STEP 14: Return
        return sOut

    def __getSessionUnits__(self) -> str:
        """
        """

        #   STEP 0: Local variables
        sDefault                = self.__getDefaultUnits__()
        sOut                    = None

        #   STEP 1: Setup - Local variables

        #   STEP 2: User output
        print("Lana (get - Session Units) {" + Helga.time() + "} - Please specify the units of measurement for the session below")
        print("\t- Default ( Enter ): " + sDefault + "\n")

        #   STEP 3: Loop
        while (True):
            #   STEP 4: User input
            sOut = input("\t> ")

            #   STEP 5: Clear output
            os.system("cls")

            #   STEP 6: Verify output
            if (sOut == ""):
                #   STEP 7: User output
                print("Lana (get - Session Name) {" + Helga.time() + "} - Are you sure you would like to use the default?")

                #   STEP 8: User input
                sTmp = input("\t> ")

                #   STEP 9: Clear output
                os.system("cls")

                #   STEP 10: Verify input
                if ((sTmp == "y") or (sTmp == "yes") or (sTmp == "")):
                    #   STEP 11: Set output var
                    sOut = sDefault

                    #   STEP 12: Exit loop
                    break

            elif (en.isUnit(sOut)):
                #   STEP 13: Exit loop
                break

            else:
                #   STEP 14: User output
                print("Lana (get - Session Units) {" + Helga.time() + "} - Invalid unit specified")

        #   STEP 14: Return
        return sOut

    #
    #       endregion

    #
    #   endregion

    #   region Back-End: Updates

    def __updateConfig__(self, **kwargs) -> None:
        """
            Description:

                Updates the config file for the lua wrapper using the provided
                information.
            
            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:

                + app_dir   = ( str ) The new feko application directory to use

                + working_dir   = ( str ) The new working directory to use
        """

        #   STEP 0: Local variables
        
        #   STEP 1: Setup - Local variables

        #   STEP 2: Check if application directory
        if ("app_dir" in kwargs):
            #   STEP 3: Update local config file
            vConny = Conny()
            sTmp_Dir = vConny.getDirectory()

            #   STEP 4: Set new app dir
            vConny.data["feko"] = kwargs["app_dir"]

            #   STEP 5: Update config file
            vConny.update(file=sTmp_Dir)

        #   STEP 4: Check if working directory
        if ("working_dir" in kwargs):
            #   STEP 5: Update working directory
            self.__config.data["parameters"]["working directory"]["default"] = kwargs["working_dir"]

        #   STEP 6: Outsource
        self.__config.update(file=self.__enum.value)

        #   STEP 7: Return
        return

    #
    #   endregion

    #   region Back-End: Antenna

    #       region Back-End-(Antenna): Solids

    def __newASolid_Cuboid__(self, **kwargs) -> str:
        """
            Description:

                Sets the antenna proejct to create a new cuboid using the
                provided arguments.

            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:

                + corner = ( dict ) A dictionary containing the corner points
                    for the new solid
                    ~ Required

                    ~ "x"   = ( float )
                    ~ "y"   = ( float )
                    ~ "z"   = ( float )

                + dimensions    = ( dict ) A dictionary containing the
                    dimensions for the new solid
                    ~ Required

                    ~ "l"   = ( float )
                    ~ "w"   = ( float )
                    ~ "h"   = ( float )

                + label = ( str ) The label for the new solid
        """

        #   STEP 0: Local variables
        dAnt                    = None

        sCuboid                 = None

        iSteps                  = None
        iOutput                 = None

        #   STEP 1: Setup - Local variables
        
        #   region STEP 2->4: Error checking

        #   STEP 2: Check that corner has all the right arguments
        if (("x" not in kwargs["corner"]) or ("y" not in kwargs["corner"]) or ("z" not in kwargs["corner"])):
            #   STEP 3: Error handling
            raise Exception("An error occured in Lana.__newASolid_Cuboid__() -> Step 2: Corner argument does not contain the required fields")

        #   STEP 4: Check that dimensions has all the righ arguments
        if (("l" not in kwargs["dimensions"]) or ("w" not in kwargs["dimensions"]) or ("h" not in kwargs["dimensions"])):
            #   STEP 4: Error handling
            raise Exception("An error occured in Lana.__newASolid_Cuboid__() -> Step 4: Dimesions argument does not contain the required fields.")
            
        #
        #   endregion
        
        #   STEP 5: Setup - Local variables
        dAnt        = self.__dAntenna

        iSteps      = dAnt["steps"]
        iOutput     = dAnt["project output"]["items"]

        sCuboid     = "VAnt_Cuboid_" + kwargs["label"]

        #   STEP 6: Add output
        dAnt["project output"][str(iOutput + 0)] =  "-- STEP " + str(iSteps) + ": Create new solid.cuboid"
        dAnt["project output"][str(iOutput + 1)] =  "   VTmp_Corner = cf.Point(" + str(kwargs["corner"]["x"]) + ", " + str(kwargs["corner"]["y"]) + ", " + str(kwargs["corner"]["z"]) + ")"
        dAnt["project output"][str(iOutput + 2)] =  "   " + sCuboid + " = VAnt_Geometry:AddCuboid(VTmp_Corner, " + str(kwargs["dimensions"]["l"]) + ", " + str(kwargs["dimensions"]["w"]) + ", " + str(kwargs["dimensions"]["h"]) + ")"
        dAnt["project output"][str(iOutput + 3)] =  "   " + sCuboid + ".Label = \"" + kwargs["label"] + "\""
        dAnt["project output"][str(iOutput + 4)] =  "--\n"

        #   STEP 7: Update antenna variables
        dAnt["steps"] += 1
        dAnt["faces"] += 6
        dAnt["regions"] += 1
        
        dAnt["project output"]["items"] += 5

        #   STEP 8: Add variable to project
        dAnt["project variables"][sCuboid] = True

        #   STEP 9: Return
        return sCuboid

    #
    #       endregion

    #       region Back-End-(Antenna): Surfaces

    def __newASurface_Rectangle__(self, **kwargs) -> str:
        """
            Description:

                Sets the antenna project to create a new rectangular surface 
                using the provided arguments
            
            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:

                + corner    = ( dict ) A dictionary containing the co-ordinates
                    of the reference corner
                    ~ Requried

                    ~ "x"   = ( float )
                    ~ "y"   = ( float )
                    ~ "z"   = ( float )

                + dimensions    = ( dict ) The dimensions of the new rectangle
                    ~ Required

                    ~ "l"   = ( float )
                    ~ "w"   = ( float )

                + label = ( str ) The label for the new rectanle
                    ~ Required
        """

        #   STEP 0: Local variables
        dAnt                    = None

        sRectangle              = None

        iSteps                  = None
        iOutput                 = None

        #   STEP 1: Setup - Local variables
        
        #   region STEP 2->5: Error checking

        #   STEP 2: Check that corner has all the required arguments
        if (("x" not in kwargs["corner"]) or ("y" not in kwargs["corner"]) or ("z" not in kwargs["corner"])):
            #   STEP 3: Error handling
            raise Exception("An error occured in Lana.__newASurface_Rectangle__() -> Step 2: Corner argument does not contain the required fields")

        #   STEP 4: Check that dimensions has all the required arguments
        if (("l" not in kwargs["dimensions"]) or ("w" not in kwargs["dimensions"])):
            #   STEP 5: Error handling
            raise Exception("An error occured in Lana.__newASurface_Rectangle__() -> Step 4: Dimensions argument does not contain the required fields")

        #
        #   endregion

        #   STEP 6: Setup - Local variables
        dAnt        = self.__dAntenna

        iSteps      = dAnt["steps"]
        iOutput     = dAnt["project output"]["items"]

        sRectangle  = "VAnt_Rectangle_" + kwargs["label"]

        #   STEP 7: Add output
        dAnt["project output"][str(iOutput + 0)] =  "-- STEP " + str(iSteps) + ": Create new rectangular surface"
        dAnt["project output"][str(iOutput + 1)] =  "   VTmp_Corner = cf.Point(" + str(kwargs["corner"]["x"]) + ", " + str(kwargs["corner"]["y"]) + ", " + str(kwargs["corner"]["z"]) + ")"
        dAnt["project output"][str(iOutput + 2)] =  "   " + sRectangle + " = VAnt_Geometry:AddRectangle(VTmp_Corner, " + str(kwargs["dimensions"]["l"]) + ", " + str(kwargs["dimensions"]["w"]) + ")"
        dAnt["project output"][str(iOutput + 3)] =  "   " + sRectangle + ".Label = \"" + kwargs["label"] + "\""
        dAnt["project output"][str(iOutput + 4)] =  "--\n"
        
        #   STEP 8: Update antenna variables
        dAnt["steps"] += 1
        dAnt["faces"] += 1
        
        dAnt["project output"]["items"] += 5

        #   STEP 9: Add variable
        dAnt["project variables"][sRectangle] = True

        #   STEP 10: Return
        return sRectangle

    def __newASurface_Polygon__(self, **kwargs) -> str:
        """
            Description:

                Sets the antenna project to create a new polygonal surface
                using the provided arguments

            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:

                + corner    = ( dict ) A dictionary containing the co-ordinates
                    of each corner of the polygon
                    ~ Required

                    ~ "items"   = ( int )
                    ~ "( int )" = {"x" = ( float ), "y" = ( float ), "z" = ( float )}

                + label = ( str ) The label for the new polygon
                    ~ Required
        """

        #   STEP 0: Local variables
        dAnt                    = None

        sPolygon                = None

        iSteps                  = None
        iOutput                 = None

        #   STEP 1: Setup - Local variables
        
        #   region STEP 2->3: Error checking
        
        #   STEP 2: Check that corner has items argument
        if ("items" not in kwargs["corner"]):
            #   STEP 3: Error handling
            raise Exception("An error occured in Lana.__newASurfce_Polygon__() -> Step 2: Corner does not contain the required fields")

        #
        #   endregion

        #   STEP 4: Setup - Local variables
        dAnt        = self.__dAntenna

        iSteps      = dAnt["steps"]
        iOutput     = dAnt["project output"]["items"]

        sPolygon    = "VAnt_Polygon_" + kwargs["label"]

        #   STEP 5: Add output
        dAnt["project output"][str(iOutput + 0)] =  "-- STEP " + str(iSteps) + ": Create new polygonal surface"
        dAnt["project output"][str(iOutput + 1)] =  "   VTmp_Points = {}"

        #   STEP 6: Update output 
        iOutput += 2

        #   STEP 7: Loop through points
        for i in range(0, kwargs["corner"]["items"]):
            #   STEP 8: Get corner
            dTmp = kwargs["corner"][str(i)]

            #   STEP 9: Add output
            dAnt["project output"][str(iOutput + i)] =  "   VTmp_Points[" + str(i + 1) + "] = cf.Point(" + str(dTmp["x"]) + ", " + str(dTmp["y"]) + ", " + str(dTmp["z"]) + ")" 

        #   STEP 10: Update ioutput
        iOutput += kwargs["corner"]["items"]

        #   STEP 11: Add output - create poly
        dAnt["project output"][str(iOutput + 0)] =  "   " + sPolygon + " = VAnt_Geometry:AddPolygon(VTmp_Points)"
        dAnt["project output"][str(iOutput + 1)] =  "   " + sPolygon + ".Label = \"" + kwargs["label"] + "\""
        dAnt["project output"][str(iOutput + 2)] =  "--\n"

        #   STEP 12: Update antenna variables
        dAnt["steps"] += 1
        dAnt["faces"] += 1

        dAnt["project output"]["items"] = iOutput + 3

        #   STEP 13: Add variable
        dAnt["project variables"][sPolygon] = True

        #   STEP 14: Return
        return sPolygon

    def __newASurface_Ellipse__(self, **kwargs) -> str:
        """
            Description:

                Sets the antenna project to create a new elliptic surface using
                the provided arguments.

            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:

                + corner    = ( dict ) The center co-ordinates of the new
                    elliptical surface
                    ~ Required

                    ~ "x"   = ( float )
                    ~ "y"   = ( float )
                    ~ "z"   = ( float )

                + dimensions    = ( dict ) The dimensiosof the new elliptical
                    surface
                    ~ Required

                    ~ "l"   = ( float )
                    ~ "w"   = ( float )

                + label = ( str ) The label for the new ellipse
                    ~ Required
        """

        #   STEP 0: Local variables
        dAnt                    = None

        sEllipse                = None

        iSteps                  = None
        iOutput                 = None

        #   STEP 1: Setup - Local variables
        
        #   region STEP 2->5: Error checking

        #   STEP 2: Check that corner has all the required arguments
        if (("x" not in kwargs["corner"]) or ("y" not in kwargs["corner"]) or ("z" not in kwargs["corner"])):
            #   STEP 3: Error handling
            raise Exception("An error occured in Lana.__newASurface_Ellipse__() -> Step 2: Corner argument does not contain the required fields")

        #   STEP 4: Check that dimensions has all the required arguments
        if (("l" not in kwargs["dimensions"]) or ("w" not in kwargs["dimensions"])):
            #   STEP 5: Error handling
            raise Exception("An error occured in Lana.__newASurface_Ellipse__() -> Step 4: Dimensions argument does not contain the required fields")

        #
        #   endregion

        #   STEP 6: Setup - Local variables
        dAnt        = self.__dAntenna

        iSteps      = dAnt["steps"]
        iOutput     = dAnt["project output"]["items"]

        sEllipse    = "VAnt_Ellipse_" + kwargs["label"]

        #   STEP 7: Add output
        dAnt["project output"][str(iOutput + 0)] =  "-- STEP " + str(iSteps) + ": Create new elliptical surface"
        dAnt["project output"][str(iOutput + 1)] =  "   VTmp_Corner = cf.Point(" + str(kwargs["corner"]["x"]) + ", " + str(kwargs["corner"]["y"]) + ", " + str(kwargs["corner"]["z"]) + ")"
        dAnt["project output"][str(iOutput + 2)] =  "   " + sEllipse + " = VAnt_Geometry:AddEllipse(VTmp_Corner, " + str(kwargs["dimensions"]["l"]) + ", " + str(kwargs["dimensions"]["w"]) + ")"
        dAnt["project output"][str(iOutput + 3)] =  "   " + sEllipse + ".Label = \"" + kwargs["label"] + "\""
        dAnt["project output"][str(iOutput + 4)] =  "--\n"

        #   STEP 8: Update antenna variables
        dAnt["steps"] += 1
        dAnt["faces"] += 1

        dAnt["project output"]["items"] += 5

        #   STEP 9: Add variable
        dAnt["project variables"][sEllipse] = True

        #   STEP 10: Return
        return sEllipse

    #
    #       endregion

    #       region Back-End-(Antenna): Curves

    def __newACurve_Line__(self, **kwargs) -> str:
        """
            Description:

                Sets the antenna project to create a new line using the
                provided arguments.

            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:

                + corner    = ( dict ) A dictionary containing the co-ordinates
                    of the start and end point of the line
                    ~ Required

                    ~ "start" = {"x" = ( float ), "y" = ( float ), "z" = ( float )}
                    ~ "end" = {"x" = ( float ), "y" = ( float ), "z" = ( float )}

                + label = ( str ) The label for the new line
        """

        #   STEP 0: Local variables
        dAnt                    = None

        sLine                   = None

        iSteps                  = None
        iOutput                 = None

        #   STEP 1: Setup - Local variables
        
        #   region STEP 2->??: Error checking

        #   STEP 2: Check if corner has all the required arguments
        if (("start" not in kwargs["corner"]) or ("end" not in kwargs["corner"])):
            #   STEP 3: Error handling
            raise Exception("An error occured in Lana.__newACurve_Line__() -> Step 2: Corner does not contain the required fields")
        
        #
        #   endregion

        #   STEP 4: Setup - Local variables
        dAnt        = self.__dAntenna

        iSteps      = dAnt["steps"]
        iOutput     = dAnt["project output"]["items"]

        sLine       = "VAnt_Line_" + kwargs["label"]

        dTmpS       = kwargs["corner"]["start"]
        dTmpE       = kwargs["corner"]["end"]

        #   STEP 5: Add output
        dAnt["project output"][str(iOutput + 0)] =  "-- STEP " + str(iSteps) + ": Create new line"
        dAnt["project output"][str(iOutput + 1)] =  "   VTmp_Start = cf.Point(" + dTmpS["x"] + ", " + dTmpS["y"] + ", " + dTmpS["z"] + ")"
        dAnt["project output"][str(iOutput + 2)] =  "   VTmp_End = cf.Point(" + dTmpE["x"] + ", " + dTmpE["y"] + ", " + dTmpE["z"] + ")"
        dAnt["project output"][str(iOutput + 3)] =  "   " + sLine + " = VAnt_Geometry:AddLine(VTmp_Start, VTmp_End)"
        dAnt["project output"][str(iOutput + 4)] =  "   " + sLine + ".Label = \"" + kwargs["label"] + "\""
        dAnt["project output"][str(iOutput + 5)] =  "--\n"

        #   STEP 6: Update antenna variables
        dAnt["steps"] += 1
        dAnt["project output"]["items"] += 6

        #   STEP 7: Add variables
        dAnt["project variables"][sLine] = True

        #   STEP 8: Return
        return sLine

    def __newACurve_PolyLine__(self, **kwargs) -> str:
        """
            Description:

                Sets the antenna project to create a new polygonal line using
                the provided arguments.

            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments;

                + corner    = ( dict ) A dicationary containing the
                    co-ordinates of each corner of the PolyLine
                    ~ Required

                    ~ "items"   = ( int )
                    ~ "( int )" = {"x" = ( float ), "y" = ( float ), "z" = ( float )}

                + label = ( str ) The label for the new polygon
                    ~ Required
        """

        #   STEP 0: Local variables
        dAnt                    = None

        sPolyLine               = None

        iSteps                  = None
        iOutput                 = None

        #   STEP 1: Setup - Local variables
        
        #   STEP 2: Check if corner has the required arguments
        if ("items" not in kwargs["corner"]):
            #   STEP 3: Error handling
            raise Exception("An error occured in Lana.__newACurve_PolyLine__() -> Step 2: Corner argument does not contain the required fields")

        #   STEP 4: Setup - Local variables
        dAnt        = self.__dAntenna

        iSteps      = dAnt["steps"]
        iOutput     = dAnt["project output"]["items"]

        sPolyLine   = "VAnt_PolyLine_" + kwargs["label"]

        #   STEP 5: Add output
        dAnt["project output"][str(iOutput + 0)] =  "-- STEP " + str(iSteps) + ": Create new PolyLine"
        dAnt["project output"][str(iOutput + 1)] =  "   VTmp_Points = {}"

        #   STEP 6: Update iOutput
        iOutput += 2

        #   STEP 7: Loop through points
        for i in range(0, kwargs["corner"]["items"]):
            #   STEP 8: Get corner
            dTmp = kwargs["corner"][str(i)]

            #   STEP 9: Add output
            dAnt["project output"][str(iOutput + i)] = "   VTmp_Points[" + str(i + 1) + "] = cf.Point(" + dTmp["x"] + ", " + dTmp["y"] + ", " + dTmp["z"] + ")"

        #   STEP 10: Update iOutput
        iOutput += kwargs["corner"]["items"]

        #   STEP 11: Add output - Create polyline
        dAnt["project output"][str(iOutput + 0)] =  "   " + sPolyLine + " = VAnt_Geometry:AddPolyLine(VTmp_Points)"
        dAnt["project output"][str(iOutput + 1)] =  "   " + sPolyLine + ".Label = \"" + kwargs["label"] + "\""
        dAnt["project output"][str(iOutput + 2)] =  "--\n"

        #   STEP 12: Update antenna variables
        dAnt["steps"] += 1
        dAnt["project output"]["items"] = iOutput + 3

        #   STEP 13: Add variable
        dAnt["project variables"][sPolyLine] = True

        #   STEP 14: Return
        return sPolyLine

    #
    #       endregion

    #       region Back-End-(Antenna): Modifications

    def __newAMod_Union__(self, **kwargs) -> str:
        """
            Description:

                Sets the antenna proejct to create a new Union using the 
                specified parts.

            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:
            
                + parts = ( dict ) A dictionary containing all the parts to be
                    used in the union operation
                    ~ Required

                    ~ "items"   = ( int )
                    ~ "( int )" = ( str )

                + label = ( str ) The label for the new union
                    ~ Required
        """

        #   STEP 0: Local varioables
        dAnt                    = None

        sUnion                  = None

        iSteps                  = None
        iOutput                 = None

        #   STEP 1: Setup - Local variables
        
        #   STEP 2: Check if parts has all the required fields
        if ("items" not in kwargs["parts"]):
            #   STEP 3: Error handling
            raise Exception("An error occured in Lana.__newAMod_Union__() -> Step 2: Parts argument does not contain the required fields")
        
        #   STEP 4: Setup - Local variables
        dAnt        = self.__dAntenna

        iSteps      = dAnt["steps"]
        iOutput     = dAnt["project output"]["items"]

        sUnion      = "VAnt_Union_" + kwargs["label"]

        #   STEP 5: Add output
        dAnt["project output"][str(iOutput + 0)] =  "-- STEP " + str(iSteps) + ": Create new union"
        dAnt["project output"][str(iOutput + 1)] =  "   VTmp_Parts = {}"

        #   STEP 6: Update iOutput
        iOutput += 2

        #   STEP 7: Loop
        for i in range(0, kwargs["parts"]["items"]):
            #   STEP 8: Add output
            dAnt["project output"][str(iOutput + i)] =  "   VTmp_Parts[" + str(i + 1) + "] = " + kwargs["parts"][str(i)]

        #   STEP 9: Update iOutput
        iOutput += kwargs["parts"]["items"]

        #   STEP 10: Add output
        dAnt["project output"][str(iOutput + 0)] =  "   " + sUnion + " = VAnt_Geometry:Union(VTmp_Parts)"
        dAnt["project output"][str(iOutput + 1)] =  "   " + sUnion + ".Label = \"" + kwargs["label"] +"\""
        dAnt["project output"][str(iOutput + 2)] =  "--\n"

        #   STEP 11: Update antenna variables
        dAnt["steps"] += 1
        dAnt["project output"]["items"] = iOutput + 3

        #   STEP 12: Add variable
        dAnt["project variables"][sUnion] = True

        #   STEP 14: Return
        return sUnion

    def __newAMod_Subtraction__(self, **kwargs) -> str:
        """
            Description:

                Sets the antenna project to create a new Subtraction using the
                specified parts.

            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:

                + parts = ( dict ) A dictionary containing all the parts to be
                    used in the subtraction operations
                    ~ Required

                    ~ "target"  = ( str )
                    ~ "subs"    = ( dict )
                        - "items"   = ( int )
                        - "( int )" = ( str )

                + label = ( str ) The label for the new subtraction
                    ~ Required
        """

        #   STEP 0: Local variables
        dAnt                    = None

        _target                 = None
        _subs                   = None

        sSubtraction            = None

        iSteps                  = None
        iOutput                 = None

        #   STEP 1: Setup - Local variables
        
        #   STEP 2: Check if parts contains all the required fields
        if (("target" not in kwargs["parts"]) or ("subs" not in kwargs["parts"])):
            #   STEP 3: Error handling
            raise Exception("An error occured in Lana.__newAMod_Subtraction__() -> Step 2: Parts argument does not contain all the required fields")

        #   STEP 4: Setup - Local variables
        dAnt        = self.__dAntenna

        iSteps      = dAnt["steps"]
        iOutput     = dAnt["project output"]["items"]

        sSubtraction    = "VAnt_Subtraction_" + kwargs["label"]

        _target     = kwargs["parts"]["target"]
        _subs       = kwargs["parts"]["subs"]

        #   STEP 5: Add output
        dAnt["project output"][str(iOutput + 0)] =  "-- STEP " + str(iSteps) + ": Create new subtraction"
        dAnt["project output"][str(iOutput + 1)] =  "   VTmp_Subs = {}"

        #   STEP 6: Update iOutput
        iOutput += 2

        #   STEP 7: Loop
        for i in range(0, _subs["items"]):
            #   STEP 8: Add output
            dAnt["project output"][str(iOutput + i)] =  "   VTmp_Subs[" + str(i + 1) + "] = " + _subs[str(i)]

        #   STEP 9: Update iOutput
        iOutput += _subs["items"]

        #   STEP 10: add output
        dAnt["project output"][str(iOutput + 0)] =  "   " + sSubtraction + " = VAnt_Geometry:Subtract(" + _target + ", VTmp_Subs)"
        dAnt["project output"][str(iOutput + 1)] =  "   " + sSubtraction + ".Label = \"" + kwargs["label"] + "\""
        dAnt["project output"][str(iOutput + 2)] =  "--\n"

        #   STEP 11: Update antenna variables
        dAnt["steps"] += 1
        dAnt["project output"]["items"] = iOutput + 3

        #   STEP 12: Add variable
        dAnt["project variables"][sSubtraction] = True

        #   STEP 13: Return
        return sSubtraction

    def __newAMod_Intersection__(self, **kwargs) -> str:
        """
            Description:

                Sets the antenna project to create a new intersection using the
                specified parts.

            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:

                + parts = ( dict ) A dictionary containing all the parts to be
                    used in the intersection operation
                    ~ Required

                    ~ "items"   = ( int )
                    ~ "( int )" = ( str )

                + label = ( str ) The label for the new intersection
                    ~ Requried
        """

        #   STEP 0: Local variables
        dAnt                    = None

        sIntersection           = None

        iSteps                  = None
        iOutput                 = None

        #   STEP 1: Setup - Local variables
        
        #   STEP 2: Check if parts argument contains the required fields
        if ("items" not in kwargs["parts"]):
            #   STEP 3: Error handling
            raise Exception("An error occured in Lana.__newAMod_Intersection__() -> Step 2: Parts argument does not contain required fields")
        
        #   STEP 4: Setup - Local variables
        dAnt        = self.__dAntenna

        iSteps      = dAnt["steps"]
        iOutput     = dAnt["project output"]["items"]

        sIntersection   = "VAnt_Intersection_" + kwargs["label"]

        #   STEP 5: Add output
        dAnt["project output"][str(iOutput + 0)] =  "-- STEP " + str(iSteps) + ": Create new intersection"
        dAnt["project output"][str(iOutput + 1)] =  "   VTmp_Parts = {}"

        #   STEP 6: Update iOutput
        iOutput += 2

        #   STEP 7: Loop
        for i in range(0, kwargs["parts"]["items"]):
            #   STEP 8: Add output
            dAnt["project output"][str(iOutput + i)] =  "   VTmp_Parts[" + str(i + 1) + "] = " + kwargs["parts"][str(i)]

        #   STEP 9: Update iOutput
        iOutput += kwargs["parts"]["items"]

        #   STEP 10: Add output
        dAnt["project output"][str(iOutput + 0)] =  "   " + sIntersection + " = VAnt_Geometry:Intersect(VTmp_Parts)"
        dAnt["project output"][str(iOutput + 1)] =  "   " + sIntersection + ".Label = \"" + kwargs["label"] + "\""
        dAnt["project output"][str(iOutput + 2)] =  "--\n"

        #   STEP 11: Update antenna variables
        dAnt["steps"] += 1
        dAnt["project output"]["items"] = iOutput + 3

        #   STEP 12: Add variable
        dAnt["project variables"][sIntersection] = True

        #   STEP 13: Return
        return sIntersection

    def __newAMod_Split__(self, **kwargs) -> str:
        """
        """

        #   STEP 0: Local variables
        #   STEP 1: Setup - Local variables
        #   STEP 2: ??
        #   STEP ??: Return
        return ""

    def __newAMod_Stitch__(self, **kwargs) -> str:
        """
        """

        #   STEP 0: Local variables
        #   STEP 1: Setup - Local variables
        #   STEP 2: ??
        #   STPE ??: Return
        return ""

    #
    #       endregion

    #       region Back-End-(Antenna): Sources

    def __newASource_Voltage__(self, **kwargs) -> str:
        """
            Description:

                Sets the antenna project to create a new voltage source using
                the provided arguments.

            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:

                + port  = ( str ) The port at which the source will be located
                    ~ Required

                + impedance = ( float ) The impedance of the source
                    ~ Required

                + magnitude = ( float ) The magnitude of the source
                    ~ Required

                + phase = ( float ) The phase of the source
                    ~ Required

                + label = ( str ) The label of the new source
                    ~ Required
        """

        #   STEP 0: Local variables
        dAnt                    = self.__dAntenna

        iSteps                  = dAnt["steps"]
        iOutput                 = dAnt["project output"]["items"]

        sVSource                = "VAnt_VSource_" + kwargs["label"]

        #   STEP 1: Setup - Local variables

        #   STEP 2: Check if config variable exists for this project
        if ("VAnt_Config" not in dAnt["project variables"]):
            #   STEP 3: Add output for config file
            dAnt["project output"][str(iOutput + 0)] =  "-- STEP " + str(iSteps) + ": Get config file"
            dAnt["project output"][str(iOutput + 1)] =  "   VAnt_Config = VAnt_Project.SolutionConfigurations[1]"
            dAnt["project output"][str(iOutput + 2)] =  "--\n"

            #   STEP 4: Update anntena variables
            iSteps  += 1
            iOutput += 3

            dAnt["steps"] = iSteps
            dAnt["project output"]["items"] = iOutput

            #   STEP 5: Add variable to variable list
            dAnt["project variables"]["VAnt_Config"] = True
            dAnt["project variables"]["items"] += 1

        #   STEP 6: Add output
        dAnt["project output"][str(iOutput + 0)] =  "-- STEP " + str(iSteps) + ": Create new voltage source"
        dAnt["project output"][str(iOutput + 1)] =  "   " + sVSource + " = VAnt_Config.Sources:AddVoltageSource(" + kwargs["port"] + ")"
        dAnt["project output"][str(iOutput + 2)] =  "   " + sVSource + ".Impedance = " + str(kwargs["impedance"])
        dAnt["project output"][str(iOutput + 3)] =  "   " + sVSource + ".Magnitude = " + str(kwargs["magnitude"])
        dAnt["project output"][str(iOutput + 4)] =  "   " + sVSource + ".Phase = " + str(kwargs["phase"])
        dAnt["project output"][str(iOutput + 5)] =  "   " + sVSource + ".Label = \"" + kwargs["label"] + "\""
        dAnt["project output"][str(iOutput + 6)] =  "--\n"

        #   STEP 7: Update antenna variables
        dAnt["steps"] += 1
        dAnt["project output"]["items"] = iOutput + 7

        #   STEP 8: Add variable
        dAnt["project variables"][sVSource] = True

        #   STEP 9: Return
        return sVSource

    #
    #       endregion

    #       region Back-End-(Antenna): Ports

    def __newAPort_Wire__(self, **kwargs) -> str:
        """
            Description:

                Sets the antenna project to create a new wire port using the
                provided arguments.

            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:

                + union = ( str ) The union variable to use
                    ~ Required

                + line  = ( str ) The label of the line on which the port
                    should be created
                    ~ Required

                + label = ( str ) The label of the new port
                    ~ Required
        """

        #   STEP 0: Local variables
        dAnt                    = self.__dAntenna

        iSteps                  = dAnt["steps"]
        iOutput                 = dAnt["project output"]["items"]

        sWirePort               = "VAnt_WPort_" + kwargs["label"]

        #   STEP 1: Setup - Local variables

        #   STEP 2: Add output
        dAnt["project output"][str(iOutput + 0)] =  "-- STEP " + str(iSteps) + ": Create new wire port"
        dAnt["project output"][str(iOutput + 1)] =  "   VTmp_Line = " + kwargs["union"] + ".Children[" + kwargs["line"] + "]"
        dAnt["project output"][str(iOutput + 2)] =  "   " + sWirePort + " = VAnt_Project.Ports:AddWirePort(VTmp_Line)"
        dAnt["project output"][str(iOutput + 3)] =  "   " + sWirePort + ".Label = \"" + kwargs["label"] + "\""
        dAnt["project output"][str(iOutput + 4)] =  "--\n"

        #   STEP 3: Update antenna variables
        dAnt["steps"] += 1
        dAnt["project output"]["items"] += 5

        #   STEP 4: Add variable
        dAnt["project variables"][sWirePort] = True

        #   STEP 5: Return
        return sWirePort

    def __newAPort_Edge__(self, **kwargs) -> str:
        """
            Description:

                Sets the antenna project ot create a new edge port using the 
                provided arguments.

            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:

                + union = ( str ) The union variable to use
                    ~ Required

                + pos   = ( dict ) A dictionary containing the positive faces
                    to be used
                    ~ Requried

                    ~ "items"   = ( int )
                    ~ "( int )" = ( str )

                + neg   = ( dict ) A dictionary containing the negative faces
                    to be used
                    ~ Requried

                    ~ "items"   = ( int )
                    ~ "( int )" = ( str )

                + label = ( str ) The label for the new edge port
        """

        #   STEP 0: Local variables
        dAnt                    = None

        iSteps                  = None
        iOutput                 = None

        sEdgePort               = None

        #   STEP 1: Setup - Local variables
        
        #   STEP 2: Check if pos argument contrain all required fields
        if ("items" not in kwargs["pos"]):
            #   STEP 3: Error handling
            raise Exception("An error occured in Lana.__newAPort_Edge__() -> Step 2: Pos argument does not contain all required fields")

        #   STEP 4: Check if neg argument contrains all required fields
        if ("items" not in kwargs["neg"]):
            #   STEP 5: Error handling
            raise Exception("An error occured in Lana.__newAPort_Edge__() -> Step 4: Neg argument does not contain all required fields")

        #   STEP 6: Setup - Local variables
        dAnt        = self.__dAntenna

        iSteps      = dAnt["steps"]
        iOutput     = dAnt["project output"]["items"]

        sEdgePort   = "VAnt_EPort_" + kwargs["label"]

        #   STEP 7: Add output
        dAnt["project output"][str(iOutput + 0)] =  "-- STEP " + str(iSteps) + ": Create new edge port"
        dAnt["project output"][str(iOutput + 1)] =  "   VTmp_Pos = {}"
        dAnt["project output"][str(iOutput + 2)] =  "   VTmp_Neg = {}"

        #   STEP 8: Update iOutput
        iOutput += 3

        #   STEP 9: Loop through positivie faces
        for i in range(0, kwargs["pos"]["items"]):
            #   STEP 10: Add output - add face to pos list
            dAnt["project output"][str(iOutput + i)] =  "   VTmp_Pos[" + str(i + 1) + "] = " + kwargs["union"] + ".Faces:Item(\"" + kwargs["pos"][str(i)] + "\")"

        #   STEP 11: Update iOutput
        iOutput += kwargs["pos"]["items"]

        #   STEP 12: Loop through negative faces
        for i in range(0, kwargs["neg"]["items"]):
            #   STEP 13: Add output - add face to neg list
            dAnt["project output"][str(iOutput + i)] =  "   VTmp_Neg[" + str(i + 1) + "] = " + kwargs["union"] + ".Faces:Item(\"" + kwargs["neg"][str(i)] + "\")"

        #   STEP 14: Update iOutput
        iOutput += kwargs["neg"]["items"]

        #   STEP 15: Add output - create port
        dAnt["project output"][str(iOutput + 0)] =  "   " + sEdgePort + " = VAnt_Project.Ports:AddEdgePort(VTmp_Pos, VTmp_Neg)"
        dAnt["project output"][str(iOutput + 1)] =  "   " + sEdgePort + ".Label = \"" + kwargs["label"] + "\""
        dAnt["project output"][str(iOutput + 2)] =  "--\n"

        #   STEP 16: Update antenna variables
        dAnt["steps"] += 1
        dAnt["project output"]["items"] = iOutput + 3

        #   STEP 17: Add variable
        dAnt["project variables"][sEdgePort] = True

        #   STEP 18: Return
        return sEdgePort

    #
    #       endregion

    #       region Back-End-(Antenna): Requests

    def __newARequest_FarField__(self, **kwargs) -> None:
        """
            Description:

                Sets the antenna project to create a new far field request
                using the provided arguments.

            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:

                + params    = ( dict ) The dictionary that contains the values
                    to be used in the new request
                    ~ Required

                    ~ "theta start":        ( float )
                    ~ "phi start":          ( float )
                    ~ "theta end":          ( float )
                    ~ "phi end":            ( float )
                    ~ "theta increments":    ( float )
                    ~ "phi increments":     ( float )
        """

        #   region STEP 0->1: Error checking

        #   STEP 0: Check if params arg passed
        if ("params" not in kwargs):
            #   STEP 1: Error handling
            raise Exception("An error occured in Lana.__newARequest_FarField__() -> Step 0: No params arg passed")

        #
        #   endregion

        #   STEP 2: Local variables
        dAnt    = self.__dAntenna
        dParams = kwargs["params"]

        iSteps  = dAnt["steps"]
        iOutput = dAnt["project output"]["items"]

        #   STEP 3: Setup - Local variables

        #   STEP 4: Check if project config is variable
        if ("VAnt_Config" not in dAnt["project variables"]):
            #   STEP 5: Add output for config file
            dAnt["project output"][str(iOutput + 0)] =  "-- STEP " + str(iSteps) + ": Get config file"
            dAnt["project output"][str(iOutput + 1)] =  "   VAnt_Config = VAnt_Project.SolutionConfigurations[1]"
            dAnt["project output"][str(iOutput + 2)] =  "--\n"

            #   STEP 6: Update anntena variables
            iSteps                                      += 1
            iOutput                                     += 3

            dAnt["steps"]                               = iSteps
            dAnt["project output"]["items"]             = iOutput

            #   STEP 7: Add variable to variable list
            dAnt["project variables"]["VAnt_Config"]    = True
            dAnt["project variables"]["items"]          += 1

        #   STEP 8: Build string
        sTmp =  "   VAnt_Config.FarFields:Add(" + str( dParams["theta start"] ) + ", "
        sTmp += str( dParams["phi start"] ) + ", "
        sTmp += str( dParams["theta end"] ) + ", "
        sTmp += str( dParams["phi end"] ) + ", "
        sTmp += str( dParams["theta increments"] ) + ", "
        sTmp += str( dParams["phi increments"] ) + ")"

        #   STEP 9: Add output
        dAnt["project output"][str(iOutput + 0)] =  "-- STEP " + str(iSteps) + ": Create new Far-Field request"
        dAnt["project output"][str(iOutput + 1)] =  sTmp
        dAnt["project output"][str(iOutput + 2)] =  "--"

        #   STEP 10: Update antenna variables
        dAnt["steps"]   += 1
        dAnt["project output"]["items"] = iOutput + 3
        
        #   STEP ??: Return
        return

    #
    #       endregion

    #
    #   endregion

    #
    #endregion

#
#endregion

#region Testing

"""
os.system("cls")

sDir    = "C:\\Users\\project\\0. My Work\\1. Repositories\\0. Unfriendly Train\\Code\\Templates\\Tests\\Lua"

lurkhei = Lana(name=Helga.ticks(), dir=sDir, units="Millimeters")

lurkhei.newAntenna(name="subtraction test")




dCorner = {
    "x": 0.0,
    "y": 0.0,
    "z": 0.0,
}

dDimensions = {
    "l": 100.0,
    "w": 100.0
}

x = lurkhei.newASurface(surface="Rectangle", corner=dCorner, dimensions=dDimensions, label="1")


dCorner = {
    "items": 3,
    "0":
    {
        "x": 1.0,
        "y": 1.0,
        "z": 0.0
    },
    "1":
    {
        "x": 26.0,
        "y": 1.0,
        "z": 0.0
    },
    "2":
    {
        "x": 1.0,
        "y": 26.0,
        "z": 0.0
    }
}

y = lurkhei.newASurface(surface="Polygon", corner=dCorner, label="2")

dCorner = {
    "items": 3,
    "0":
    {
        "x": 1.0,
        "y": 25.0,
        "z": 0.0
    },
    "1":
    {
        "x": 1.0,
        "y": 51.0,
        "z": 0.0
    },
    "2":
    {
        "x": 27.0,
        "y": 51.0,
        "z": 0.0
    }
}

a = lurkhei.newASurface(surface="Polygon", corner=dCorner, label="a")

dCorner = {
    "items": 3,
    "0":
    {
        "x": 25.0,
        "y": 51.0,
        "z": 0.0
    },
    "1":
    {
        "x": 51.0,
        "y": 51.0,
        "z": 0.0
    },
    "2":
    {
        "x": 51.0,
        "y": 25.0,
        "z": 0.0
    }
}

b = lurkhei.newASurface(surface="Polygon", corner=dCorner, label="b")

dCorner = {
    "items": 3,
    "0":
    {
        "x": 51.0,
        "y": 27.0,
        "z": 0.0
    },
    "1":
    {
        "x": 25.0,
        "y": 1.0,
        "z": 0.0
    },
    "2":
    {
        "x": 51.0,
        "y": 1.0,
        "z": 0.0
    }
}

c = lurkhei.newASurface(surface="Polygon", corner=dCorner, label="c")

dIdk = {
    "target": x,
    "subs":
    {
        "items": 4,
        "0": y,
        "1": a,
        "2": b,
        "3": c
    }
}

z = lurkhei.newAModification(mod="Subtract", parts=dIdk, label="3")


dCorner = {
    "x": 0.0,
    "y": 0.0,
    "z": 1.6,
}

dDimensions = {
    "l": 100.0,
    "w": 100.0
}

x = lurkhei.newASurface(surface="Rectangle", corner=dCorner, dimensions=dDimensions, label="4")


lurkhei.saveAntenna(dir="test")
lurkhei.closeAntenna()
lurkhei.exportLua(replace=True, run=False, interactive=False)
"""

#
#endregion