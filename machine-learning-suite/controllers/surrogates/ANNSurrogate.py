#region	--- Imports ---
import copy as cp
import datetime as dt
import json as js
import numpy as np
import os
import random as rn
import sys

sys.path.append(os.path.abspath("."))

from config.Config import Conny
from controllers.handlers.OptimizationHandler import Hermione
from controllers.optimizers.Swarms import Swarms as swarms
from controllers.optimizers.GeneticAlgorithms import GeneticAlgorithms as genetic_algorithm
from helpers.ActivationFunctionHelper import ActivationFunctionHelper
from helpers.ApplicationHelper import ApplicationHelper
from helpers.ArrayHelper import ArrayHelper
from helpers.MathHelper import MathHelper
from models.DataContainer import Data
#endregion

class Annie:
    #region	--- Init ---
    def __init__(self, **kwargs) -> None:
        #   --- Setup ---
        self.__config = Conny()
        self.__config.load("ArtificialNeuralNetwork.json")
        self.__password			= rn.random() * 111754552.83191288 			#  ToDo change to uuid

        rn.seed(dt.datetime.now())
        #
        self.secondary_neural_nets = None
        self.__iIterationsChildGen = None
        self.classifier_neural_net = None        
        #	STEP 1.1: Layout
        self.weights = None
        self.weights_momentum = None
        #
        self.nodes = None
        self.pre_activation_nodes = None
        self.node_averages = None
        #
        self.input_width = None
        self.output_width = None
        self.hidden_layers_width = None
        self.number_of_hidden_layers = None
        #
        self.__dHiddenDetails = None
        #
        self.weight_range = None
        #	STEP 1.3: Activation functions
        self.activation_functions = ActivationFunctionHelper()
        self.current_activation_function = None
        #	STEP 1.4: Learning Rate
        self.learning_rate = None
        #	STEP 1.5: Momentum
        self.use_momentum = None
        #
        self.momentum = None		
        #	STEP 1.6: Default training variables
        self.accuracy_requirement = None
        #
        self.number_of_epochs = None
        self.batch_size = None
        #	STEP 1.7: Other
        self.accuracy_test_sample_size = None
        self.fitness_test_sample_size = None
        #	STEP 1.9: Bools
        self.__bAllowTesting		= None
        #	STEP 1.10: Bias
        self.bias_array				= None
        #
        self.bias				= None       
        #	STEP 1.11: Dropout
        self.drop_out_array				= None
        self.input_nodes_drop_out_percent		= None
        self.hidden_nodes_drop_out_percent		= None        
        #	STEP 1.12: Regularizations
        self.weight_decay			= None
        self.l1_regularization			= None
        self.l2_regularization			= None
        #	STEP 2.1: Chlidren
        self.is_primary				= None
        self.is_classifier			= None
        self.is_secondary				= None        
        #	STEP 2.2: Other
        self.show_output			= None
        #	STEP 2.3: Drop out
        self.use_drop_out			= False
        #	STEP 2.4: Regularization
        self.use_noise_injection	= True
        self.use_weight_decay		= False
        self.use_l1_regularization				= False
        self.use_l2_regularization				= False
        #	STEP 3.1: Check if parameters in kwargs
        if ("params" in kwargs):
            #	STEP 3.2: Init params using passed params
            self.__initParams__(kwargs["params"])
        else:
            #	STEP 3.3: Init params using default params
            self.__initParams__(self.__config.data["parameters"])

        #	STEP 3.4: Check if geometry is in kwargs
        if ("geometry" in kwargs):
            #	STEP 3.5: Init geometry using passed geometry
            self.__initGeometry__(kwargs["geometry"])

        #	STEP 4: Return
        return

    #
    #endregion

    #region --- FE: imports/exports ---
    def importAnnie(self, **kwargs) -> None:
        """
            - Description::

                Imports an Annie instance from the specified file.

            |\n
            |\n
            |\n
            |\n
            |\n

            - Arguments::

                :arg file: >> [required][str] The file path from which the Annie instance
                    should be imported

                :arg is_full_path: >> [bool] Specifies if the full path was provided
                    in the <file> argument

                :arg is_extension_appended: >> [bool] Specifies if the file extension has been
                    appended to the <file> argument
                    ~ False = appends .json to the end of the path
        """

        file_path = ""
        json_file = None
        json_data = None

        try:
            #   --- Check if full path
            if ("is_full_path" in kwargs):
                if (kwargs["is_full_path"] == True):
                    file_path = kwargs["file"]

            #   --- Check if not full path
            if (file_path == None):
                file_path = os.path.abspath(".") + "/static/data/exports/surrogates/" + kwargs["file"]
                if ("is_extension_appended" in kwargs):
                    if (kwargs["is_extension_appended"] == False):
                        file_path = file_path + ".json"

            #   --- Open json
            with open(file_path, "r+") as jsFile:
                json_data = js.load(jsFile)

            #	STEP 12: Child variables
            self.__iIterationsChildGen	= json_data["child iterations"]

            self.is_primary				= json_data["is fertile"]
            self.is_classifier			= json_data["is classifier"]
            self.is_secondary				= json_data["is child"]

            #	STEP 13: Check if this instance has a child net
            if (json_data["child"] != None):
                #	STEP 14: Init child net
                self.secondary_neural_nets = Annie()
                self.secondary_neural_nets.importAnnie(file=json_data["child"])

            #	STEP 15: Layout variables
            self.weights 			= json_data["weights"]
            self.weights_momentum	= json_data["momentum weights"]

            self.nodes				= json_data["nodes"]
            self.pre_activation_nodes	= json_data["pre activation nodes"]
            self.node_averages		= json_data["average nodes"]

            self.input_width			= json_data["input width"]
            self.output_width			= json_data["output width"]
            self.hidden_layers_width			= json_data["hidden width"]
            self.number_of_hidden_layers		= json_data["hidden length"]

            self.__dHiddenDetails		= json_data["hidden layer details"]

            self.weight_range			= json_data["weight range"]

            #	STEP 16: Activation Function variables
            self.current_activation_function			= json_data["activation function"]

            #	STEP 17: Learning Rate variables
            self.learning_rate		= json_data["learning rate"]
            
            #	STEP 18: Momentum variables
            self.use_momentum		= json_data["momentum active"]

            self.momentum			= json_data["momentum"]			

            #	STEP 19: Training variables
            self.accuracy_requirement		= json_data["accuracy requirement"]

            self.number_of_epochs				= json_data["epochs"]
            self.batch_size			= json_data["batch size"]

            #	STEP 20: Accuracy Test sample size
            self.accuracy_test_sample_size		= json_data["accuracy sample size"]
            self.fitness_test_sample_size		= json_data["fitness sample size"]

            #	STEP 21: Other
            self.__bAllowTesting		= json_data["allow testing"]
            self.show_output			= json_data["show output"]

            #	STEP 22: Bias variables
            self.__bUseBias				= json_data["use bias"]
            self.__bClearBias			= json_data["clear bias"]
            self.bias				= json_data["bias value"]

        except Exception as ex:
            #	STEP 22: Error handling
            print("Initial error: ", ex)
            raise Exception("An error occured in Annie.importAnnie()")

        #	STEP 23: Return
        return

    def exportAnnie(self, **kwargs) -> None:
        """
            Description:

                Exports this instance of Annie to the specified file location.

            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:

                + file	= ( str ) The file path this instance should be
                    exported
                    ~ Required

                + full_path	= ( bool ) Specifies if the full path was provided
                    in the <file> argument

                + extension	= ( bool ) Specifies if the file extension has been
                    appended to the <file> argument
                    ~ False = appends .json to the end of the path
        """

        #	STEP 0: Local variables
        json_data					= None

        file_path				= None

        jsFile					= None

        #	STEP 1: Setup - Local variables

        #	STEP 2: Be safe
        try:
            #	STEP 3: Populate dictionary
            json_data = {
                #	STEP 4: Child variables
                "child iterations":		self.__iIterationsChildGen,

                "is fertile":			self.is_primary,
                "is classifier":		self.is_classifier,
                "is child":				self.is_secondary,

                #	STEP 5: Layoutvariables
                "weights":				ArrayHelper.getList(self.weights),
                "momentum weights":		ArrayHelper.getList(self.weights_momentum),
                "nodes":				ArrayHelper.getList(self.nodes),
                "pre activation nodes":	ArrayHelper.getList(self.pre_activation_nodes),
                "average nodes":		ArrayHelper.getList(self.node_averages),

                "input width":			self.input_width,
                "output width":			self.output_width,
                "hidden width":			self.hidden_layers_width,
                "hidden length":		self.number_of_hidden_layers,

                "hidden layer details":	self.__dHiddenDetails,

                "weight range":			self.weight_range,

                #	STEP 6: Activation Function variables
                "activation function":	self.current_activation_function,

                #	STEP 7: Learning Rate variables
                "learning rate":		self.learning_rate,

                #	STEP 8: Momentum variables
                "momentum active":		self.use_momentum,

                "momentum":				self.momentum,

                #	STEP 9: Training variables
                "accuracy requirement":	self.accuracy_requirement,

                "epochs":				self.number_of_epochs,
                "batch size":			self.batch_size,

                #	STEP 10: Acc Test sample size
                "accuracy sample size":	self.accuracy_test_sample_size,
                "fitness sample size":	self.fitness_test_sample_size,

                #	STEP 11: Other variables
                "allow testing":		self.__bAllowTesting,
                "show output":			self.show_output,

                #	STEP 12: Bias variables
                "use bias":				self.__bUseBias,
                "clear bias":			self.__bClearBias,
                "bias value":			self.bias
            }

            #	STEP 12: Check if this instance has a child net
            if (self.secondary_neural_nets == None):
                #	STEP 13: No set child var = None
                json_data["child"] = None

            else:
                #	STEP 14: Yes, create child net export name
                json_data["child"] = kwargs["file"] + "_child"

                #	STEP 15: Export child net
                self.secondary_neural_nets.exportAnnie(file=json_data["child"], extension=False)

            #	STEP 16: Check if full path in kwargs
            if ("full_path" in kwargs):
                #	STEP 17: If specified file is full path
                if (kwargs["full_path"] == True):
                    #	STEP 18: Set file path
                    file_path = kwargs["file"]

            #	STEP 19: If file path not set
            if (file_path == None):
                #	STEP 20: Get full path
                file_path = os.path.abspath(".") + "\\Data\\Exports\\Surrogates\\" + kwargs["file"]

                #	STEP 21: Check if file extension specified
                if ("extension" in kwargs):
                    #	STEP 22: If file extension not added
                    if (kwargs["extension"] == False):
                        #	STEP 23: If file exntension not added
                        file_path = file_path + ".json"

            #	STEP 24: Create the file
            jsFile = open(file_path, "a")

            #	STEP 25: Close file
            jsFile.close()
            jsFile = None

            #	STEP 26: Open file
            with open(file_path, "r+") as jsFile:
                #	STEP 27: Dump json data to file
                js.dump(json_data, jsFile, indent=4, separators=(", ", " : "))

        except Exception as ex:
            #	STEP 28: Error handling
            print("Initial error: ", ex)
            raise Exception("An error occured in Annie.exportAnnie()")

        #	STEP 29: Return
        return

    #
    #endregion

    #region Front-End: Is-type-statements

    def isAccurate(self, _lfExpectedOutput: list, **kwargs) -> bool:
        """
            Description:

                Checks if the current output of the layer is accurate compared
                to the provided expected output.

            |\n
            |\n
            |\n
            |\n
            |\n

            Returns:

                + bAccurate	= ( bool )

                + RMSD	= ( bool ) Flag to indicate if the RMSD should be used
                    ~ Default	= False
        """

        #	STEP 0: Local variables
        lOutputs				= self.getOutput()

        bRMSD					= False

        #	STEP 1: Check if RMSD arg passed
        if ("RMSD" in kwargs):
            #	STEP 2: Update - Local variables
            bRMSD	= True

        #region STEP 3->11: Not RMSD

        #	STEP 3: Check if not RMSD
        if (bRMSD == False):
            #	STEP 4: Setup - Tmp variables
            fTmp_Margin					= self.__config.data["parameters"]["accuracy margin"]

            iTmp_Correct				= 0

            #	STEP 5: Loop through outputs
            for i in range(0, len( lOutputs ) ):
                #	STEP 6: Get difference between output and actual
                fTmp_Error = lOutputs[i] - _lfExpectedOutput[i]

                #	STEP 7: If within margin
                if ((fTmp_Error <= fTmp_Margin) and (fTmp_Error >= -1.0 * fTmp_Margin)):
                    #	STEP 8: Increment number of correct outputs
                    iTmp_Correct += 1
                
            #	STEP 9: If all outputs were accurate
            if (iTmp_Correct == len( lOutputs ) ):
                #	STEP 10: Return
                return True
            
            #	STEP 11: Return not correct
            return False

        #
        #endregion

        #region STEP 12->??: RMSD

        #	STEP 12: Then RMSD
        else:
            #	STEP 13: Setup - Tmp variables
            fTmp_Sum	= 0.0

            #	STEP 14: Loop through outputs
            for i in range(0, len( lOutputs ) ):
                #	STEP 15: Get MSE
                fTmp_MSE	= np.power( _lfExpectedOutput[i] - lOutputs[i], 2)

                #	STEP 16: Add MSE to sum
                fTmp_Sum	+= fTmp_MSE

            #	STEP 17: Average MSE sum
            fTmp_Avg	= fTmp_Sum / float( len( lOutputs ) )

            #	STEP 18: Sqrt MSE average
            fTmp_RMSD	= np.sqrt( fTmp_Avg )

            #	STEP 19: Calculate the error margin
            fTmp_Margin	= self.__config.data["parameters"]["accuracy margin"]
            
            #	STEP 20: Check if RMSD within error
            if (fTmp_RMSD <= fTmp_Margin):
                #	STEP 21: Return correct
                return True

            #	STEP 22: Return incorrect
            return False
        
        #
        #endregion

    #
    #endregion

    #region Front-End: Gets

    def getAccuracy(self, **kwargs) -> dict:
        """
            Description:

                Gets the accuracy of this instance using the provided dataset.

            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:

                + data 	= ( vars ) Data container
                    ~ Required

                + size	= ( int ) The number of data samples to use for the
                    accuracy test
                    ~ Required
                    ~ If greater than 150, limited to 150

                + full_set	= ( bool ) Boolean to indicate if the full dataset
                    should be tested. If used overrides size limit of 150

                + split	= ( bool ) Boolean to indicate if the set should be
                    split between correct and incorrect results
            
            |\n

            Returns:

                + dDetails	= ( dict ) Dictionary containing the following
                    ~ child dataset = ( vars ) Child dataset that was created
                        using samples that tested inaccurate
                    ~ percent accuracy	= ( float ) The accuracy of this 
                        instance as a percentage
                    ~ iterations 	= ( int ) The number of samples used for
                        the test
                    ~ accurate samples	= ( int ) The amount of accurat samples
        """

        #region STEP 0->1: Init

        #	STEP 0: Local variables
        dData					= None
        dChild					= None

        iIterations				= None

        iAccurate				= 0

        bSplit					= False

        #	STEP 1: Setup - Local variables

        #
        #endregion

        #region STEP 2->18: Error checking

        #	STEP 2: Check if data passed
        if ("data" not in kwargs):
            #	STEP 3: Error handling
            raise Exception("An error occured in Annie.getAccuracy() -> Step 2: No data argument passed")

        else:
            #	STEP 4: Set data var
            dData = kwargs["data"]

        #	STEP 5: Check if size passed
        if ("size" not in kwargs):
            #	STEP 6: Use default
            iIterations = self.accuracy_test_sample_size

        else:
            #	STEP 7: If size greater than limit
            if (kwargs["size"] > self.accuracy_test_sample_size):
                #	STEP 8: Limit size
                iIterations = self.accuracy_test_sample_size

            else:
                #	STEP 9: Not larger, used passed arg
                iIterations = kwargs["size"]

        #	STEP 10: Shortcut
        try:
            #	STEP 11: Check if full_set is true
            if (kwargs["full_set"] == True):
                #	STEP 12: Set iterations
                iIterations = dData.getLen()

        except:
            #	STEP 13: Do nothing
            ApplicationHelper.nop()

        #	STEP 14: Shortcut
        try:
            #	STEP 15: Set split flag
            bSplit = kwargs["split"]

            #	STEP 16: Use copy of data set instead
            dData = cp.deepcopy(kwargs["data"])

            #	STEP 17: Create child data set
            dChild = Data()

        except:
            #	STEP 18: YEET
            ApplicationHelper.nop()

        #
        #endregion

        #region STEP 19->24: Accuracy test

        #	STEP 19: Reset data set
        dData.reset()

        #	STEP 20: Iterate through dataset
        for _ in range(0, iIterations):
            #	STEP 21: Get random data sample
            dDNR = dData.getRandDNR()

            #	STEP 21: Propagate forward
            self.__propagateForward__(dDNR["in"])

            #	STEP 22: Get accuracy
            if (self.isAccurate(dDNR["out"], RMSD=True)):
                iAccurate += 1

            else:
                #	STEP 23: Check if data set should be split
                if (bSplit):
                    #	STEP 24: Pop and lock
                    dChild.insert(data=dData.pop(last_seen=True))

        #
        #endregion

        #	STEP 25: Populate output dictionary
        dOut = {
            "child dataset":		dChild,

            "percent accuracy":		float(iAccurate) / iIterations,
            "iterations": 			iIterations,

            "accurate samples":		iAccurate
        }

        #	STEP 26: Return
        return dOut

    def getAFitness(self, **kwargs) -> float:
        """
            Description:

                Returns the sum of the fitness of a number of samples in the
                provided dataset.

            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:

                + data	= ( vars ) The dataset to use for testing
                    ~ Required

                + debug	= ( bool ) Flag that specifies if the dataset stats
                    should be printed
        """

        #	STEP 0: Local variables
        dData					= None
        iIterations				= None

        fOut					= 0.0

        #	STEP 1: Setup - Local variables

        #region STEP 2->11: Argument error checking

        #	STEP 2: Check if data passed
        if ("data" not in kwargs):
            #	STEP 3: Error handling
            raise Exception("An error occured in Annie.getAFitness() -> Step 2: No data argument passed")

        else:
            #	STEP 4: Set local variable
            dData = kwargs["data"]

            #	STEP 5: Reset dataset for accurate sampling
            dData.reset()

        #	STEP 6: Check length of dataset passed
        if (dData.getLen() > self.fitness_test_sample_size):
            #	STEP 7: Limit iterations
            iIterations = self.fitness_test_sample_size

        else:
            #	STPE 8: Set local variable
            iIterations = dData.getLen()

        #	STEP 9: Check if debug arg passed
        if ("debug" in kwargs):
            #	STEP 10: If debug arg is true
            if (kwargs["debug"] == True):
                #	STEP 11: Print dataset statistics
                dData.stats()

        #
        #endregion

        #region STEP 12->15: Fitness test

        #	STEP 12: Iterate through dataset
        for _ in range(0, iIterations):
            #	STEP 13: Get random data sample from dataset
            dDNR = dData.getRandDNR()

            #	STEP 14: Propagate forward
            self.__propagateForward__(dDNR["in"])

            #	STEP 15: Sum fitness
            fOut += self.getFitness(dDNR["out"])

        #
        #endregion

        #	STEP 16: Return
        return fOut

    def getError(self, _lfExpectedOutput: list) -> list:
        """
        """
        
        #	STEP 0: Local variables
        lOut					= []
        lTmp					= None

        #	STEP 1: Setup - Local variables
        lTmp					= self.getOutput()

        #	STEP 2: Iterate through outputs
        for i in range(0, len(_lfExpectedOutput)):
            #	STEP 3: Append E = expected - actual
            lOut.append(_lfExpectedOutput[i] - lTmp[i])

        #	STEP 4: Return
        return lOut

    def getFitness(self, _lfExpectedOutput: list) -> float:
        """
        """

        #	STEP 0: Local variables
        fOut				= 0.0
        lTmp				= None

        #	STEP 1: Setup - Local variables
        lTmp 				= self.getError(_lfExpectedOutput)

        #	STEP 2: Get the fitness of the sample
        for i in range(0, len(lTmp)):
            fOut = fOut + abs(lTmp[i])
        
        #	STEP 3: Return
        return fOut

    def getOutput(self, **kwargs) -> list:
        """
            Description:

                Returns the rounded output of this instance.

            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:

                + round	= ( bool ) Flag for if rounding should be used in the return

            Returns:

                + lOut	= ( list ) The output layer of this instance
        """

        #	STEP 0: Local variables
        lOut				= None
        
        #	STEP 1: Setup - local variables
        lOut				= self.nodes[self.number_of_hidden_layers + 1]

        #	STEP 2: Check if rounding specified
        if ("round" in kwargs):
            #	STEP 3: If rounding required
            if (kwargs["round"] == True):
                #	STEP 4: Iterate through the list
                for i in range(0, len(lOut)):
                    #	STEP 5: Round the list value
                    lOut[i] = round(lOut[i], 5)

        #	STEP 6: Return
        return lOut

    def getPointOutput(self, _lData: list) -> vars:
        """
        """
        
        #	STEP 0: Local variables
        lOut				= None

        #	STEP 1: Setup - Local variables

        #	STEP 2: Propagate forward
        self.__propagateForward__(_lData)

        #	STEP 3: Get the output to return
        lOut = np.ndarray.tolist(cp.deepcopy(self.getOutput()))

        #	STEP 4: Reset the network
        self.__resetNodes__()

        #	STEP 5: Check if only single output
        if (len(lOut) == 1):
            #	STEP 6: Return only that output
            return lOut[0]

        #	STEP 7: Return normally
        return lOut

    #
    #endregion

    #region Front-End: Training

    def trainSet(self, _dData: Data, **kwargs) -> dict:
        """
            - Description::

                Trains this instance of Annie using the data set provided as
                well as the parameters in kwargs.

            |\n
            |\n
            |\n
            |\n
            |\n
            - Parameters::

                :param _dData: >> ( vars ) -- The data container containing the
                    data set to train with

                :arg acc: >> ( bool ) Check accuracy flag for default training
                    ~ default	= True

                :arg compare: >> ( bool ) Show comparison flag
                    ~ default 	= False

                :arg advanced_training: >> ( bool ) Flag for the use of optimizers during training
                    ~ default	= False

                :arg advanced_algorithm: >> ( int ) The optimizer to user for training if advanced_training = true
                    ~ default 	= randint(0, 3)

            |\n

            Returns:

                + dResults		= ( dict ) Dictionary containing
                    ~ result	= ( int ) Number of iterations training took
                    ~ check accuracy	= ( bool ) Accuracy check flag
                    ~ show comparison	= ( bool ) Show comparison flag
                    ~ use optimization	= ( bool ) Advanced training flag
                    ~ optimization algorithm	= ( int ) Optimizer used for
                        advanced training 

        """

        #	STEP 0: Local variables
        dOut							= None

        iAlgorithm						= rn.randint(0, 1)

        bCheckAcc						= True
        bComparison						= False
        bOptimization					= False

        #	STEP 1: Setup - Local variables
        _dData.reset()

        #region STEP 2->11: Argument check

        #	STEP 2: Check if acc flag passed
        if ("acc" in kwargs):
            #	STEP 3: Update - Local variables
            bCheckAcc = kwargs["acc"]

        #	STEP 4: Check if compare flag passed
        if ("compare" in kwargs):
            #	STPE 5: Update - Local variable
            bComparison = kwargs["compare"]

        #	STEP 6: Check if advanced training flag passed
        if ("advanced_training" in kwargs):
            #	STEP 7: Update - Local variable
            bOptimization = kwargs["advanced_training"]

        #	STEP 10: Check if advanced algorithm passed
        if ("advanced_algorithm" in kwargs):
            #	STEP 11: Update - Local variable
            iAlgorithm = kwargs["advanced_algorithm"]

        #
        #endregion

        #region STEP 12->14: Check if class fully initialized

        #	STEP 12: Check if weights initialized
        if (self.weights == None):
            #	STEP 13: Get geometry from data
            dGeo = self.__getGeometry__(_dData)

            #	STEP 14: Init geometry
            self.__initGeometry__(dGeo)

        #
        #endregion

        #region STEP 15->17: Default training

        #	STEP 5: Check if DEF training
        if (bOptimization == False):
            #	STEP 6: User Output
            if (self.show_output):
                print("Annie (train-set) {" + ApplicationHelper.time() + "} - Training via Default Training")
                input("\n> Start:")

            #	STEP 7: Outsource default training
            json_data_Out	= self.__trainDef__(_dData, bCheckAcc)

        #
        #endregion

        #region STEP 18->21: Trust-Region Optimization training

        #	STEP 18: Check if TRO assisted DEF training
        elif ((bOptimization == True) and (iAlgorithm == 0)):
            #	STEP 19: User Output
            if (self.show_output):
                print("Annie (train-set) {" + ApplicationHelper.time() + "} - Training via Trust-Region Optimization assisted Default training")
                input("\n> Start:")

            #	STEP 20: Outsource tro training
            self.__trainTro__(_dData)

            #	STEP 21: Outsoruce def training
            json_data_Out	= self.__trainDef__(_dData, bCheckAcc)

        #
        #endregion
        
        #region STEP 22->25: Particle-Swarm Optimization training

        #	STEP 22: Chec if PSO assisted DEF training
        elif ((bOptimization == True) and (iAlgorithm == 1)):
            #	STEP 23: User Output
            if (self.show_output):
                print("Annie (train-set) {" + ApplicationHelper.time() + "} - Training via Particle-Swarm Optimization assisted Default training")
                input("\n> Start:")

            #	STEP 24: Outsource pso training
            self.__trainPso__(_dData)

            #	STEP 25: Outsource def training
            json_data_Out 	= self.__trainDef__(_dData, bCheckAcc)

        #
        #endregion

        #	STEP 26: Check if comparison results should be shown
        if (bComparison):
            #	STEP 27: Perform data comparison
            self.showComparison(_dData)

        #	STEP 28: Populate output dictionary
        dOut = {
            "fitness":					json_data_Out["fitness"],
            "iterations":				json_data_Out["iterations"],

            "check accuracy": 			bCheckAcc,
            "show comparison": 			bComparison,
            "use optimization": 		bOptimization,
            "optimization algorithm": 	iAlgorithm
        }

        #	STEP 29: Return
        return dOut

    #
    #endregion

    #region Front-End: Testing

    def test(self, _dDict: dict) -> vars:
        """
        """

        #	STEP 0: Local variables
        #	STEP 1: Setup - local variables

        #	STEP 2: Check if testing allowed
        if (self.__bAllowTesting):
            print("YEET! This bitch empty!")

        else:
            raise Exception("An error occured in Annie.test() -> Step 2: Testing is not allowed in this class")

        #	STEP ??: Return
        return

    #
    #endregion

    #region Mid-End: Gets

    def getWeights(self, **kwargs) -> list:
        """
            Description:

                Returns this class isntance's weight list if the provided password
                matches this instance's password.

            |\n
            |\n
            |\n
            |\n
            |\n

            Args:

                + password		= ( int/float ) This class' password
                    ~ Required

            |\n

            Returns:

                + list			= ( list )
                    ~ A deep copy of this class' weights
        """

        #	STEP 0: Local variables
        #	STEP 1: Setup - local variables

        #	STEP 2: Check if password provided
        if ("password" not in kwargs):
            #	STEP 3: Error handling
            raise Exception("An error occured in Annie.getWeights() -> Step 2: No password provided")

        #	STEP 4: Check if password matches class password
        if (kwargs["password"] != self.__password):
            #	STEP 5: Error handling
            raise Exception("An error occured in Annie.getWeights() -> Step 4: The provided password doesn't match this class' password")

        #	STEP 6: Return
        return cp.deepcopy(self.weights)

    #
    #endregion

    #region Mid-End: Sets

    def setAcFunction(self, **kwargs) -> None:
        """
            Description

                Sets the activation function for the class to match the range
                of weights that will be used and updates the learning rate
                accordingly

            |\n
            |\n
            |\n
            |\n
            |\n

            Args:

                + password		= ( int/float ) This class' password
                    ~ Required
                + algorithm		= ( str ) Name of the algorithm being used
                    ~ Required
                + scalar		= ( float ) The scalar to use
                    ~ Required

        """

        #	STEP 0: Local variables
        #	STEP 1: Setup - Local variables

        #	STEP 2: Check if password passed
        if ("password" not in kwargs):
            #	STEP 3: Error handling
            raise Exception("An error occured in Annie.setAcFunction() -> Step 2: No password passed")

        #	STEP 4: Check if password matches class password
        if (kwargs["password"] != self.__password):
            #	STEP 5: Error handling
            raise Exception("An error occured in Annie.setAcFunction() -> Step 3: Passed password does not match this class' password")

        #	STEP 5: Outsource
        self.__setAcFunction__(algorithm=kwargs["algorithm"], scalar=kwargs["scalar"])

        #	STEP 6: Return
        return

    def setWeights(self, **kwargs) -> None:
        """
            Description:

                Sets this class' weights to be the provided weights.

            |\n
            |\n
            |\n
            |\n
            |\n

            Args:

                + password		= ( int/float ) This class' password
                    ~ Required
                + weights 		= ( list ) The weights to update to
                    ~ Required
                    
        """

        #	STEP 0: Local variables
        #	STEP 1: Setup - Local variables

        #	STEP 2: Check if password passed
        if ("password" not in kwargs):
            #	STEP 3: Error handling
            raise Exception("An error occured in Annie.SetWeights() -> Step 2: No password provided")

        #	STEP 4: Check if password matches class password
        if (kwargs["password"] != self.__password):
            #	STEP 5: Error handling
            raise Exception("An error occured in Annie.setWeights() -> Step 4: The provided password doesn't match this class' password")

        #	STEP 6: Check if new weights provided
        if ("weights" not in kwargs):
            #	STEP 7: Error handling
            raise Exception("An error occured in Annie.setWeights() -> Step 6: No weights provided to update to")

        #	STEP 8: Set the weights
        self.weights = kwargs["weights"]

        #	STEP 9: Return
        return

    def setParameters(self, _dParams: dict) -> None:
        """
        """

        #	STEP 0: Local variables
        #	STEP 1: Setup - Local variables

        #	STEP 2: Check if testing is allowed
        if (self.__bAllowTesting):
            #	STEP 3: Outsource
            self.__initParams__(_dParams)

        #	STEP 4: Return
        return

    #
    #endregion

    #region Mid-End: Propagation

    def propagateForward(self, **kwargs) -> None:
        """
            Description:

                Performs forward propagation using the provided input.

            |\n
            |\n
            |\n
            |\n
            |\n

            Args:

                + data			= ( list ) Data point
                    ~ Required
                + password		= ( int/float ) This class' password
                    ~ Required

        """

        #	STEP 0: Local variables
        #	STEP 1: Setup - Local variables

        #	STEP 2: check if password passed
        if ("password" not in kwargs):
            #	STEP 3: Error handling
            raise Exception("An error occured in Annie.propagateForward() -> Step 2: No password passed")

        #	STEP 4: Check if password matches class' password
        if (kwargs["password"] != self.__password):
            #	STEP 5: Error handling
            raise Exception("An error occured in Annie.propagateForward() -> Step 4: Passed password does not match this class' password")

        #	STEP 6: Check if data passed
        if ("data" not in kwargs):
            #	STEP 7: Error handling
            raise Exception("An error occured in Annie.propagateForward() -> Step 6: No data point passed")

        #	STEP 7: Outsource
        self.__propagateForward__(kwargs["data"])

        #	STEP 8: Return
        return

    def propagateBackward(self, **kwargs) -> None:
        """
            Description

                Perform back propagation using the provided output.

            |\n
            |\n
            |\n
            |\n
            |\n

            Args:

                + data			= ( list ) Data point
                    ~ Required
                + password		= ( int/float ) This class' password
                    ~ Required

        """

        #	STEP 0: Local variables
        #	STEP 1: Setup - Local variables

        #	STEP 2: check if password passed
        if ("password" not in kwargs):
            #	STEP 3: Error handling
            raise Exception("An error occured in Annie.propagateForward() -> Step 2: No password passed")

        #	STEP 4: Check if password matches class' password
        if (kwargs["password"] != self.__password):
            #	STEP 5: Error handling
            raise Exception("An error occured in Annie.propagateForward() -> Step 4: Passed password does not match this class' password")

        #	STEP 6: Check if data passed
        if ("data" not in kwargs):
            #	STEP 7: Error handling
            raise Exception("An error occured in Annie.propagateForward() -> Step 6: No data point passed")

        #	STEP 7: Outsource
        self.__propagateBackward__(kwargs["data"])

        #	STEP 8: Return
        return

    #
    #endregion

    #region Back-End: Init

    def __initGeometry__(self, _dGeometry: dict) -> None:
        """
            Description:

                Initializes this instance's gemoetry variables; weights and
                nodes are then initialized.
            
            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:

                + in width	= ( int ) The input data width
                    ~ Required

                + out width = ( int ) The output data width
                    ~ Required

                + hidden width	= ( int ) The hidden layer width
                    ~ Required

                + hidden legnth = ( int ) The number of hidden layers
                    ~ Required
        """

        #	STEP 0: Local variables
        #	STEP 1: Setup - Local variables

        #	STEP 2: Initialize lists
        self.input_width 		= _dGeometry["in width"]
        self.output_width		= _dGeometry["out width"]
        self.hidden_layers_width		= _dGeometry["hidden width"]
        self.number_of_hidden_layers	= _dGeometry["hidden length"]

        #	STEP 3: Initialize weights and momentumWeights
        self.__initNodes__()
        self.__initWeights__()

        #	STEP 4: Return
        return

    def __initParams__(self, _dParams: dict) -> None:
        """
        """

        #	STEP 0: Local variables

        #	STEP 1: Setup - Local variables
        self.__bAllowTesting		= _dParams["allow testing"]
        self.show_output			= _dParams["show output"]
        self.current_activation_function			= _dParams["activation function"]
        self.weight_range			= _dParams["weight range"]
        self.learning_rate		= _dParams["learning"]
        self.accuracy_test_sample_size		= _dParams["accuracy sample size"]
        self.fitness_test_sample_size		= _dParams["fitness sample size"]
        

        self.__dHiddenDetails		= _dParams["hidden details"]
        self.current_activation_function_Output	= _dParams["output details"]["default"]

        # self.activation_functions.setFunction(function=self.current_activation_function_Output, c=_dParams["output details"]["c"], boundary=_dParams["output details"]["boundary"])
        
        self.momentum			= _dParams["momentum"]["momentum scalar"]
        self.use_momentum		= _dParams["momentum"]["is active"]

        self.bias				= _dParams["bias"]["bias value"]

        self.__bUseBias				= _dParams["bias"]["use bias"]
        self.__bClearBias			= _dParams["bias"]["clear bias"]
        self.number_of_epochs				= _dParams["training methods"]["def"]["epochs"]
        self.batch_size			= _dParams["training methods"]["def"]["batch size"]
        self.accuracy_requirement		= _dParams["training methods"]["def"]["acc requirement"]

        self.hidden_nodes_drop_out_percent		= _dParams["training methods"]["def"]["drop out"]["hidden drop out"]
        self.input_nodes_drop_out_percent		= _dParams["training methods"]["def"]["drop out"]["input drop out"]

        self.weight_decay			= _dParams["training methods"]["def"]["weight decay"]
        self.l1_regularization			= _dParams["training methods"]["def"]["lambda1"]
        self.l2_regularization			= _dParams["training methods"]["def"]["lambda2"]

        self.is_primary				= _dParams["children"]["is fertile"]
        self.is_classifier			= _dParams["children"]["is classifier"]

        self.is_secondary				= _dParams["children"]["is child"]
        self.__iIterationsChildGen	= _dParams["children"]["generation iterations"]

        #	STEP 2: Return
        return

    def __initWeights__(self) -> None:
        """
        """

        #	STEP 0: Local variables
        self.weights 		= []
        self.weights_momentum 	= []

        #	STEP 1: Setup - Local variables

        #	STEP 2: Iterate through nodes
        for i in range(0, len(self.nodes) - 1):
            #	STEP 3: Append weight list
            self.weights.append(np.zeros( len(self.nodes[i]) * len(self.nodes[i + 1]) ))

        #	STEP 4: Create momentum weights
        self.weights_momentum = cp.deepcopy(self.weights)

        #	STEP 5: Iterate through weights
        for i in range(0, len(self.weights)):
            for j in range(0, len(self.weights[i])):
                #	STEP 6: Get random value for weight
                self.weights[i][j] = rn.gauss(0.0, self.weight_range)

        #	STEP 7: Return
        return

    def __initNodes__(self) -> None:
        """
        """

        #	STEP 0: Local variables
        dWidth						= self.__dHiddenDetails["width"]

        self.nodes 				= []
        self.pre_activation_nodes	= []
        self.node_averages		= []

        iInWidth					= self.input_width
        iOutWidth					= self.output_width
        iHiddenWidth				= self.hidden_layers_width
        iHiddenLength				= self.number_of_hidden_layers

        #	STEP 1: Setup - local variables
        
        #region STEP 1.1: Bias nodes - check if using bias

        if (self.__bUseBias):
            #	STEP 1.2: Adjust hidden width
            iHiddenWidth 	+= 1
            iInWidth		+= 1
            
        #
        #endregion

        #	STEP 2: Init first row of nodes
        self.nodes.append(np.zeros(iInWidth))

        #	STEP 3: Iterate through hidden nodes
        for _ in range(0, iHiddenLength):
            #	STEP 4: Get random number
            rand = rn.random()

            #	STEP 5: Check if no width change
            if ((rand <= dWidth["decrease"]) and (iHiddenWidth > self.output_width) and (iHiddenWidth > self.input_width)):
                #	STEP 6: Check if decrease
                iHiddenWidth -= 1

            #	STEP 7: Check if increase
            elif (rand <= dWidth["decrease"] + dWidth["increase"]):
                iHiddenWidth += 1

            #	STEP 4: Append hidden layer nodes
            self.nodes.append(np.zeros(iHiddenWidth))

        #	STEP 5: Append output layer nodes
        self.nodes.append(np.zeros(iOutWidth))

        #	STEP 6: Copy zeroes to pre activation list
        self.pre_activation_nodes = cp.deepcopy(self.nodes)
        self.node_averages		= cp.deepcopy(self.nodes)

        #	STEP 7: Init bias matrix
        self.bias_array				= np.zeros(iHiddenLength + 1)

        #	STEP 8: Set bias values
        self.__setBiasValues__()

        #	STEP 9: Return
        return

    #
    #endregion

    #region Back-End: Sets

    def __setAcFunction__(self, **kwargs) -> None:
        """
            Description:

                Sets the activation function for the class to match the range
                of weights that will be used and updates the learning rate
                accordingly

            |\n
            |\n
            |\n
            |\n
            |\n

            Args:
            
                + algorithm		= ( str ) Name of the algorithm that's updating
                    ~ Required
                + scalar		= ( float ) The scalar to use
                    ~ Required

        """
        
        #	STEP 0: Local variables
        fTmp					= 0.0

        #	STEP 1: Setup - Local variables
        
        #	STEP 2: Be safe
        try:
            #	STEP 3: Check if algorithm passed
            if ("algorithm" not in kwargs):
                #	STEP 4: Error handling
                raise Exception("An error occured in Annie.__setAcFunction__() -> Step 3: No algorithm passed")

            #	STEP 5: Check if scalar passed
            if ("scalar" not in kwargs):
                #	STEP 5: Error handling
                raise Exception("An error occured in Annie.__setAcFunction__() -> Step 5: No scalar passed")

            #	STEP 7: Check if normal propagation
            if (kwargs["algorithm"] == "def"):
                #	STEP 8: Return
                return

            #	STEP 9: Check if tro
            if (kwargs["algorithm"] == "tro"):
                #	STEP 10: Get scalar range
                fTmp = float( 6.5 * kwargs["scalar"] )

                #	STEP 11: update activation functions
                self.activation_functions.setFunction(function=self.current_activation_function, c=float( 2.0 / fTmp ))

                #	STEP 12: Update class learning rate
                self.learning_rate = self.learning_rate * ( fTmp / 2.0 )

                #	STEP 13: Return of the jedi
                return

            #	STEP 14: Check if pso
            if (kwargs["algorithm"] == "pso"):
                #	STEP 15: Get scalar range
                fTmp = kwargs["scalar"]

                #	STEP 16: Update activation function
                self.activation_functions.setFunction(function=self.current_activation_function, c=float( 2.0 / fTmp ))

                #	STEP 17: Update class learning rate
                self.learning_rate = self.learning_rate * float ( fTmp / 2.5 )

                #	STEP 18: Return of the jedi
                return

            #	STEP 19: Error handing
            raise Exception("An error occured in Annie.__setAcFunction__() -> Step 19: Unimplemented algorithm passed")

        except Exception as ex:
            #	STEP ??: Error handling
            print("Initial Error: ", ex)
            raise Exception("An error occured in Annie.__setAcFunction__()")

        #	STEP ??: Return
        return

    def __setBiasValues__(self) -> None:
        """
        """

        #	STEP 0: Local variables

        #	STEP 1: Setup - Local variables

        #	STEP 2: Check if bias is being used
        if (self.__bUseBias):
            #	STEP 3: Iterate through bias list
            for i in range(0, len(self.bias_array)):
                #	STEP 4: Set bias node value
                self.bias_array[i] = self.bias

        #	STEP 5: Return
        return
        
    def __setWeights(self, _lWeights: list) -> None:
        """
        """

        #	STEP 0: Local variables
        #	STEP 1: Setup - local variables

        #	STEP 2: Set class weights
        self.weights = _lWeights

        #	STEP 3: Return
        return

    #
    #endregion

    #region Back-End: Gets

    def __getClassificationDataset__(self, **kwargs) -> dict:
        """
            Description:

                Creates a new dataset using the provided dataset. The new
                dataset groups the data that is correctly classified by this
                parent instance and the data that is incorrectly classified
                into unique classes:

            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:

                + data	= ( vars ) The dataset to adjust
                    ~ Required
        """

        #	STEP 0: Local variables
        dNewData				= None
        dOldData				= None

        dOut					= {}

        #	STEP 1: Setup - Local variables

        #	STEP 2: Check if data arg passed
        if ("data" not in kwargs):
            #	STEP 3: Error handling
            raise Exception("An error occured in Annie.__getClassificationDataset__() -> Step 2: No data argument passed")

        else:
            #	STEP 4: Set local variable
            dOldData = kwargs["data"]
            dOldData.reset()

        #	STEP 5: Create new dataset
        dNewData = Data()

        #	STEP 6: Iterate through old dataset
        for _ in range(0, dOldData.getLen()):
            #	STEP 7: Get random data sample
            dDNR = dOldData.getRandDNR()

            #	STEP 8: Propagate forward
            self.__propagateForward__(dDNR["in"])

            #	STEP 9: Check if accurate
            if (self.isAccurate(dDNR["out"], RMSD=True)):
                #	STEP 10: Create temp dictionary
                json_data = {
                    "in": dDNR["in"],
                    "out": [1.0, -1.0]
                }

                #	STEP 11: Insert into new dataset
                dNewData.insert(data=json_data)

            else:
                #	STEP 12: Create temp dictionary
                json_data = {
                    "in": dDNR["in"],
                    "out": [-1.0, 1.0]
                }

                #	STEP 13: Insert into new dataset
                dNewData.insert(data=json_data)

        #	STEP 14: Populate output dictionary
        dOut = {
            "new set": dNewData
        }

        #	STEP 15: Return
        return dOut

    def __getGeometry__(self, _dData: Data) -> dict:
        """
        """

        #	STEP 0: Local variables
        dOut					= None

        iWidth_Input			= None
        iWidth_Output			= None
        iWidth_Hidden			= None
        iLength_Hidden			= None

        #	STEP 1: Setup - Local variables
        iWidth_Input	= _dData.getInputWidth()
        iWidth_Output	= _dData.getOutputWidth()

        iWidth_Hidden 	= iWidth_Input + int(rn.random() * iWidth_Input)

        #	STEP 2: Check if geometry is shallow
        if (( self.__dHiddenDetails["is shallow"] ) and ( rn.uniform(0.0, 1.0) < 0.95 ) and ( self.use_drop_out == False ) ):
            #	STEP 3: Get length probabilities
            dProbabilities	= self.__dHiddenDetails["probabilities"] 

            #	STEP 4: Get random number
            fTmp = rn.uniform(0.0, 1.0)

            #	STEP 5: Check if 2 length
            if (fTmp < dProbabilities["2"]):
                iLength_Hidden = 2

            #	STEP 6: Check if 3 lenght
            elif (fTmp < dProbabilities["2"] + dProbabilities["3"]):
                iLength_Hidden = 3

            #	STEP 7: Then must be 1 length
            else:
                iLength_Hidden = 1

        #	STEP 8: Not shallow
        else:
            #	STEP 9
            iTmp_Len1	= iWidth_Input + int(rn.random() * iWidth_Input)
            iTmp_Len2	= rn.randint(4, 7)

            iLength_Hidden	= min(iTmp_Len1, iTmp_Len2)

            #	STEP 10: User output
            if (self.show_output):
                print("Annie (get-geo) {" + ApplicationHelper.time() + "} - Initializing deep net")
                print("\t~ Depth: " + str(iLength_Hidden), end="\n\n")

        #	STEP 2: Populate output dictionary
        dOut = {
            "in width": 		iWidth_Input,
            "out width": 		iWidth_Output,
            "hidden width":		iWidth_Hidden,
            "hidden length":	iLength_Hidden
        }

        #	STEP 3: Return
        return dOut

    def __getShape_Weights(self) -> list:
        """
        """

        #	STEP 0: Local variables
        lOut = []

        #	STEP 1: Setup - Local variables

        #	STEP 2: Iterate thrgouh weight layers
        for i in range(0, len(self.weights)):
            #	STEP 3: Append zeros for layer
            lOut.append(np.zeros(len(self.weights[i])))
        
        #	STEP 4: Return
        return lOut

    def __getShape_Nodes(self) -> list:
        """
        """

        #	STEP 0: Local variables
        lOut = []

        #	STEP 1: Setup - Local variables

        #	STEP 2: Iterate through node layers
        for i in range(0, len(self.nodes)):
            #	STEP 3: Append zeros for node layer
            lOut.append(np.zeros(len(self.nodes[i])))
        
        #	STEP 6: Return
        return lOut

    #
    #endregion

    #region Back-End: Resets

    def __resetAverages__(self) -> None:
        """
        """

        #	STEP 0: Local variables

        #	STEP 1: Setup - Local variables

        #	STEP 2: Iterate through layers
        for i in range(0, len(self.node_averages)):
            #	STEP 3: Iterate through nodes in layer
            for j in range(0, len(self.node_averages[i])):
                #	STEP 4: Reset node
                self.node_averages[i][j] = 0.0

        #	STEP 5: Return
        return

    def __resetNodes__(self) -> None:
        """
        """
        
        #	STEP 0: Local variables
        #	STEP 1: Setup - Local vairalbes

        #	STEP 2: Iterate through node layers
        for i in range(0, len(self.nodes)):
            #	STEP 3: Iterate through nodes in layer
            for j in range(0, len(self.nodes[i])):
                #	STEP 4: Reset ndoe
                self.nodes[i][j] 				= 0.0
                self.pre_activation_nodes[i][j] 	= 0.0

        #	STEP 5: Return
        return

    def __resetPassword__(self) -> int:
        """
            Description:

                Resets the password for this class

            |\n
            |\n
            |\n
            |\n
            |\n

            Returns:

                + int			= ( int )
                    ~ The new password for this class

        """

        #	STEP 0: Local variables
        #	STEP 1: Setup - Local variables

        #	STEP 2: Generate new password
        self.__password = rn.random() * 111754552.83191288

        #	STEP 3: Return
        return self.__password

    #
    #endregion

    #region Back-End: Training

    #		region Back-End-(Training): Default

    def __trainDef__(self, _dData: Data, _bCheckAcc: bool) -> int:
        """
            Description:

                Performs default forward and backward propagation training
                using the provided dataset.

            |\n
            |\n
            |\n
            |\n
            |\n

            Params:
            
                :param _dData: = ( vars ) -- Data container
                :param _bCheckAcc: = ( bool ) -- Check accuracy flag

            |\n

            Returns:

                + dOut	= ( dict )
                    ~ iterations	= ( int ) The amount of iterations used
                        during training

                    ~ child set	= ( vars ) The child data set created from the
                        incorrecy data samples

            |\n

            ToDo:

                + Recount steps
        """

        #	STEP 0: Local variables
        dData_Testing		= None
        dData_Training		= None

        lBest_Set			= self.getWeights(password=self.__password)
        fBest_Fitness		= np.inf

        fScalar_Train		= 30.0
        fScalar_Test		= 70.0

        iBatch_Iterations	= None
        iBatch_Size			= self.batch_size

        iEpochs				= self.number_of_epochs

        #region STEP 1->6: Setup - Localv variables

        #	STEP 1: Setup - Local variables
        dData_Training		= _dData.splitData()

        dData_Testing		= dData_Training["testing"]
        dData_Training		= dData_Training["training"]
        
        iBatch_Iterations	= int( np.ceil( dData_Training.getLen() / iBatch_Size ) )

        #	STEP 2: Check for small dataset
        if ( dData_Training.getLen() < iBatch_Size ):
            fScalar_Train	= 80.0
            fScalar_Test	= 20.0

        if (self.use_drop_out):
            iEpochs	= int(iEpochs * 0.65)

        #
        #endregion

        #	STEP 7: User Output
        if (self.show_output):
            print("Annie (def-training) {" + ApplicationHelper.time() + "} - Starting default training")
            print("\t~ Epochs:\t\t"				+ str(iEpochs))
            print("\t~ Batches per Epoch:\t"	+ str(iBatch_Iterations))
            print("\t~ Batch size:\t\t"			+ str(iBatch_Size))
            print("\t~ Dataset size:\t\t"		+ str(dData_Training.getLen()) + "\n")

            print("\t~ Node Drop Out:\t\t" 			+ str(self.use_drop_out))
            print("\t~ Gaussian Noise Injection:\t"	+ str(self.use_noise_injection))
            print("\t~ Weight Decay:\t\t\t"			+ str(self.use_weight_decay))
            print("\t~ L1 Regularization:\t\t" 		+ str(self.use_l1_regularization))
            print("\t~ L2 Regularization:\t\t"		+ str(self.use_l2_regularization) + "\n")
        
        #	STEP 8: Iterate for epochs
        for i in range(0, iEpochs):
            #	STEP 9: Iterate for batch iterations
            for j in range(0, iBatch_Iterations):

                #region STEP 10->16: Train

                #	STEP 10: Iterate for batch size
                for _ in range(0, iBatch_Size):
                    #	STEP 11: Get data point
                    dDNR = dData_Training.getRandDNR(noise=self.use_noise_injection)

                    #	STEP 12: Check - Drop Out status
                    if (self.use_drop_out):
                        #	STEP 13: Set dropout flag
                        self.__propagateForward__(dDNR["in"], training=True)

                    #	STEP 14: No dropout
                    else:
                        #	STEP 15: Propagate forwared
                        self.__propagateForward__(dDNR["in"])
                    
                    #	STEP 16: Outsource - Back Prop
                    self.__propagateBackward__(dDNR["out"])

                #
                #endregion

                #region STEP 17->24: Accuracy check point

                #	STEP 17: Get accuracy
                json_data_AccTest	= self.getAccuracy(data=dData_Testing, 	size=dData_Testing.getLen())
                json_data_AccTrain	= self.getAccuracy(data=dData_Training, size=dData_Training.getLen())

                #	STEP 18: Get fitness
                fTmp_Fitness	= 100.0 * ( 1.0 - json_data_AccTest["percent accuracy"] ) * ( 1.01 - json_data_AccTrain["percent accuracy"] ) + fScalar_Test * ( 1.0 - json_data_AccTest["percent accuracy"] ) + fScalar_Train * ( 1.01 - json_data_AccTrain["percent accuracy"] )

                #	STEP 19: Check if best fitness
                if (fTmp_Fitness < fBest_Fitness):
                    #	STEP 20: Update - Best
                    lBest_Set		= self.getWeights(password=self.__password)
                    fBest_Fitness	= fTmp_Fitness

                    #	STEP 21: User output
                    if (self.show_output):
                        print("\t{" + ApplicationHelper.time() + "} -", "Fitness: " + str( round( fBest_Fitness, 2 ) ) + "\t", "Test: " + str( round( json_data_AccTest["percent accuracy"], 2) ), "Train: " + str( round( json_data_AccTrain["percent accuracy"], 2) ), "Index: " + str(i) + "-" + str(j), sep="\t")

                #	STEP 22: If temp fitness not converging
                elif ( fTmp_Fitness > 5.0 * fBest_Fitness ):
                    #	STEP 23: User output
                    if (self.show_output):
                        print("\t{" + ApplicationHelper.time() + "} - \tEnding epoch " + str(i) + " early by " + str( iBatch_Iterations - j ) + " batch iterations")
                    
                    #	STEP 24: End epoch
                    break
                
                #
                #endregion

        #region STEP 25->31: Post training evaluations

        #	STEP 25: Get total iterations
        iTmp = self.number_of_epochs * (iBatch_Iterations * iBatch_Size)

        #	STEP 26: Update weights to fittest set
        self.setWeights(password=self.__password, weights=lBest_Set)

        #	STEP 27: Get dataset accuracy
        json_data_AccTrain = self.getAccuracy(data=_dData, size=0, full_set=True)

        #	STEP 28: User output
        if (self.show_output):
            #	STEP 29: Get accuracy as percentage
            iAccTmp = json_data_AccTrain["accurate samples"]
            fAccTmp = json_data_AccTrain["percent accuracy"]

            #	STEP 30: Print output
            print("")
            print("\t- Iterations: " + str(iTmp))
            print("\t- Accurate Samples: " + str(iAccTmp))
            print("\t- Percentage Accuracy: " + str(round(fAccTmp * 100.0, 2)) + "%\n")						
        
        #
        #endregion

        #	STEP 32: Populate output dictionary
        dOut = {
            "iterations":	iTmp,
            "fitness":		fBest_Fitness,
            "child set":	json_data_AccTrain["child dataset"]
        }

        #	STEP 33: Return		
        return dOut

    def __propagateForward__(self, _dataPoint: list, **kwargs) -> None:
        """
        """

        #	STEP 0: Local variables

        #	STEP 1: Setup - Local variables
        self.__resetNodes__()

        #	STEP 2: Check - Data width
        if (len(_dataPoint) != self.input_width):
            #	STEP 3: Error handling
            raise Exception("An error occured in Annie.__propagateForward() -> Step 2: Data input width mismatch")		

        #	STEP 5: Update - Drop out list
        self.drop_out_array	= ArrayHelper.getShape(self.nodes)
            
        #	STEP 6: Iterate through inputs
        for i in range(0, len(_dataPoint)):
            #	STEP 7: Check if drop out
            if ((self.use_drop_out) and (rn.uniform(0.0, 1.0) < self.input_nodes_drop_out_percent) and ("training" in kwargs)):
                #	STEP 8: Set node as dropout
                self.nodes[0][i]		= 0.0
                self.drop_out_array[0][i]	= True

            #	STEP 9: Not dropout
            else:
                #	STEP 10: Update - Node
                self.nodes[0][i] 	= _dataPoint[i]
                self.drop_out_array[0][i]	= False

        #	STEP 11: Check if using bias
        if (self.__bUseBias):
            #	STEP 12: Update - Bias nodes
            self.nodes[0][len(self.nodes[0]) - 1] = self.bias_array[0]
        
        #	STEP 13: Propagate each layer foward
        for i in range(1, len(self.nodes)):
            #	STEP 14: Get the length of the layer
            iTmp 			= len(self.nodes[i])
            iTmp_Iterations	= iTmp

            #	STEP 15: Check if bias is being used and not output layer
            if ((self.__bUseBias) and (i != len(self.nodes) - 1)):
                #	STEP 16: Set pre activation bias node
                self.pre_activation_nodes[i][iTmp - 1] 	= self.bias_array[i]

                #	STEP 17: Set bias node
                self.nodes[i][iTmp - 1] 					= self.activation_functions.activation_function(self.current_activation_function, self.bias_array[i])

                #	STEP 18: Adjust layer length
                iTmp_Iterations 							-= 1

            #	STEP 19: Iterate through the nodes in the layer
            for j in range(0, iTmp_Iterations):
                #	STEP 20: Check - Dropout status
                if ((self.use_drop_out) and (rn.uniform(0.0, 1.0) < self.hidden_nodes_drop_out_percent) and (i != len(self.nodes) - 1) and ("training" in kwargs)):
                    #	STEP 21: Set node as dropout
                    self.nodes[i][j]					= 0.0
                    self.pre_activation_nodes[i][j]	= 0.0
                    self.drop_out_array[i][j]				= True

                #	STEP 22: Not dropout
                else:
                    #	STEP 23: Setup - Temp variables
                    fTmp = 0.0

                    #	STEP 24: Get the sum of all the inputs - iterate through relevant weights
                    for k in range(0, len(self.nodes[i - 1])):
                        #	STEP 25: Sum input
                        ln = self.nodes[i - 1][k]
                        lw = self.weights[i - 1][k * iTmp + j]
                        
                        #	STPE 26: Update sum
                        fTmp = fTmp + ln * lw

                    #	STEP 27: Save pre-activation function values
                    self.pre_activation_nodes[i][j]	= fTmp

                    #	STEP 28: Update node values
                    self.nodes[i][j] 				= self.activation_functions.activation_function(self.current_activation_function, fTmp)
            
        #	STEP 29: Return
        return

    def __propagateBackward__(self, _lfExpectedOutput: list) -> None:
        """
        """
        
        #	STEP 0: local variables
        lNodeSig				= None
        lNodeErr				= None
        lWeightErr				= None

        lTmpError				= None

        #	STEP 1: Setup - Local variables
        lNodeSig 	= self.__getShape_Nodes()
        lNodeErr 	= self.__getShape_Nodes()
        lWeightErr 	= self.__getShape_Weights()

        lTmpError	= self.getError(_lfExpectedOutput)

        #	STEP 2: Get sigmas for all node layers - iterate through layers
        lNodeSig    = self.__pbSigma__(lNodeSig)

        #	STEP 3: Get node errors
        lNodeErr    = self.__pbNodeError__(lTmpError, lNodeSig, lNodeErr)

        #	STEP 4: Get weight errors
        lWeightErr  = self.__pbWeightError__(lNodeSig, lNodeErr, lWeightErr)

        #	STEP 5: Update weights
        self.__pbUpdateWeights__(lWeightErr)

        #	STEP 6: Return
        return

    #		region Back-End-(Default): Back-Propagation

    def __pbSigma__(self, _lNodeSig: list) -> list:
        """
            Description:

                Gets the sigma values ( activation function derivatives ) of
                the current node values in this Annie.

            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:

                + _lNodeSig	= ( list ) A list to be populated with the sigma
                    values. Has the same shape as the nodes for this class.
        """

        #	STEP 0: Local variables

        #	STEP 1: Setup - Local variables

        #	STEP 2: Iterate through node layers
        for i in range(1, len(_lNodeSig)):
            #	 STPE 8: Iterate through nodes in layer
            for j in range(0, len(_lNodeSig[i])):
                #   STEP 9: Check - Dropout status
                if ((self.use_drop_out) and (self.drop_out_array[i][j] == True)):
                    #   STEP 10: Set as dropout node
                    _lNodeSig[i][j] = 0.0

                #   STEP 11: Not dropout
                else:
                    #	STEP 12: Get pre-activation value
                    fTmp_preActivation	= self.pre_activation_nodes[i][j]

                    #	STEP 13: Get normal activation function
                    _lNodeSig[i][j]	= self.activation_functions.activation_function_derivative(self.current_activation_function, fTmp_preActivation)

        #	STEP 14: Return
        return _lNodeSig

    def __pbNodeError__(self, _lError: list, _lNodeSig: list, _lNodeErr: list) -> list:
        """
        """

        #	STEP 0: Local variables
        iLastRow				= None

        #	STEP 1: Setup - local variables
        iLastRow 				= len(_lNodeErr) - 1
        
        #	STEP 2: Iterate through the node layers from back to front
        for i in range(iLastRow, 0, -1):
            #	STEP 3: If not last row
            if (i < iLastRow):
                #	STEP 4: Get temp vars
                iTmpLen 	= len(_lNodeErr[i + 1])
                iIterations	= iTmpLen

                #	STEP 4: Check if using bias and layer <= iLastRow -2
                if ((self.__bUseBias) and (i <= iLastRow - 2)):
                    #	STEP 5: Adjust iterations
                    iIterations -= 1

            #	STEP 6: Iterate through the nodes in the layer
            for j in range(0, len(_lNodeErr[i])):
                #	STEP 7: Check if currently on last row
                if (i == iLastRow):
                    #	STEP 8: Set error for the node -> dE/da = -E
                    _lNodeErr[i][j] = -1.0 * _lError[j]

                #   STPE 9: Check - Dropout status
                elif ((self.use_drop_out) and (self.drop_out_array[i][j] == True)):
                    #   STEP 10: Set as dropout node
                    _lNodeErr[i][j] = 0.0

                #   STEP 11: Not dropout
                else:
                    #	STEP 12: Reset temp vars
                    fTmp	= 0.0

                    #	STEP 13: Iterate through the layer above thisone
                    for k in range(0, iIterations):
                        #	STEP 14: Sum the error from iterable node to current node
                        fTmp = fTmp + self.weights[i][j * iTmpLen + k] * _lNodeSig[i + 1][k] * _lNodeErr[i + 1][k]

                    #	STEP 15: Set current node error
                    _lNodeErr[i][j] = fTmp

        #	STEP 16: Return
        return _lNodeErr

    def __pbWeightError__(self, _lNodeSig: list, _lNodeErr: list, _lWeightErr: list) -> list:
        """
        """

        #	STEP 0: local variables

        #	STEP 1: Setup - Local variables

        #	STEP 2: Iterate through weight layers
        for i in range(0, len(_lWeightErr)):
            #	STEP 3: Get length of node layer
            iTmpLen     = len(_lNodeErr[i + 1])
            iIterations	= iTmpLen
            
            if ((self.__bUseBias) and (i < len(_lWeightErr) - 1)):
                iIterations -= 1

            #	STEP 4: Iterate through nodes in layer
            for j in range(0, len(_lNodeErr[i])):
                #	STEP 5: Iterate through attached weights
                for k in range(0, iIterations):
                    #	STEP 6: Set the weight error
                    _lWeightErr[i][j * iTmpLen + k] = round(self.nodes[i][j] * _lNodeSig[i+1][k] * _lNodeErr[i+1][k], 6)

        #	STEP 7: Return
        return _lWeightErr

    def __pbUpdateWeights__(self, _lWeightErr: list) -> None:
        """
        """

        #	STEP 0: Local variables
        
        #	STEP 1: Setup - Local variables

        #	STEP 2: Check - Momentum status
        if (self.use_momentum == False):
            #	STEP 3: Iterate through weight layers
            for i in range(0, len(_lWeightErr)):
                #	STEP 4: Iterate through weights in layer
                for j in range(0, len(_lWeightErr[i])):
                    #	STEP 5: Calculate delta = -error
                    fDelta = -1.0 * _lWeightErr[i][j]

                    #	STEP 6: Save new weight
                    self.weights[i][j] = round(self.weights[i][j] + fDelta, 6)

            #	STEP 7: Return
            return

        #	STEP 8: Iterate through weight layers
        for i in range(0, len(_lWeightErr)):
            #	STEP 9: Iterate through weights in layer
            for j in range(0, len(_lWeightErr[i])):
                #	STEP 10: Calculate delta = -learning * error + momentum * previous weights
                fDelta = -1.0 * self.learning_rate * _lWeightErr[i][j] + self.momentum * self.weights_momentum[i][j]

                #	STEP 11: Check - L1 status
                if (self.use_l1_regularization):
                    #	STEP 12: Check if weight is positive
                    if (self.weights[i][j] > 0):
                        #	STEP 13: Update - Delta
                        fDelta -= self.learning_rate * self.l1_regularization

                    #	STEP 14: Check if weight is negative
                    elif (self.weights[i][j] < 0):
                        #	STEP 15: Update - Detla
                        fDelta += self.learning_rate * self.l1_regularization

                #	STEP 16: Check - L2 status
                if (self.use_l2_regularization):
                    #	STEP 17: Update - Delta
                    fDelta -= 2.0 * self.learning_rate * self.l2_regularization * self.weights[i][j]
                    
                #	STEP 23: Set new weight
                self.weights[i][j] = round(self.weights[i][j] + fDelta, 6)
        
        #	STEP 24: Save momentum weight
        self.weights_momentum = cp.copy(self.weights)

        #	STEP 13: Check - Weight Decay status
        if (self.use_weight_decay):
            #	STEP 14: Iterate through weight layers
            for i in range(0, len( self.weights )):
                #	STEP 15: Iterate through weights in layer
                for j in range(0, len( self.weights[i] )):
                    #	STEP 16: Update weight
                    self.weights[i][j]	*= (1.0 - self.weight_decay )


        #	STEP 17: Return
        return

    #
    #		endregion

    #
    #		endregion

    #		region Back-End-(Training): Child

    def	__trainChild__(self, **kwargs) -> None:
        """
            Description:

                If possible trains a child network for this instance.

            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:

                + data	= ( vars ) New data set to use for child
                    ~ Required

                + original_data	= ( vars ) Original data set if new data set
                    needs to be expanded upon

                    ~ Required

                + show_comparison	= ( bool ) Flag that specifies whether or
                    not the comparison of the child net should be displayed
                    after generation

                    ~ Default	= False

                + chlid_output	= ( bool ) Flag that specifies whether or not
                    the child should show output

                    ~ Default 	= self.show_output
        """

        #	STEP 0: Local variables
        dNew					= None
        dOrg					= None

        lOutputs_New			= None
        lOutputs_Org			= None

        bShowComparison			= False
        bChildOutput			= self.show_output

        #	STEP 1: Setup - Local variables

        #	STEP 2: Check if not fertile or already a child
        if (self.is_secondary == True):
            #	STEP 3: Exit function
            return

        elif not ((self.is_primary) or (self.is_classifier)):
            return

        #	STEP 4: Check if data passed
        if ("data" not in kwargs):
            #	STEP 5: Error handling
            raise Exception("An error occured in Annie.__trainChild__() -> Step 4: No data argument passed")

        #	STEP 6: Check if original data passed
        if ("original_data" not in kwargs):
            #	STEP 7: Error handling
            raise Exception("An error occured in Annie.__trainChild__() -> Step 6: No original_data argument passed")
            
        #	STEP 8: Check if acc_check arg passed
        if ("show_comparison" in kwargs):
            #	STEP 9: Set variable
            bShowComparison = kwargs["show_comparison"]

        #	STEP ??: Check if child_output arg passed
        if ("child_output" in kwargs):
            #	STEP ??: Set variable
            bChildOutput	= kwargs["child_output"]

        #	STEP 9: User Output
        if (self.show_output):
            print("Annie (child-train) {" + ApplicationHelper.time() + "} - Training child network to meet 100 percent accuracy requirement")

        #	STEP 10: Get outputs for both datasets
        dNew	= kwargs["data"]
        dOrg	= kwargs["original_data"]

        lOutputs_New = dNew.getUniqueOutputs()
        lOutputs_Org = dOrg.getUniqueOutputs()

        #	STEP 11: Check if num outputs is same
        iRequired	= len(lOutputs_Org) - len(lOutputs_New)

        #region STEP 12->23: Data set expansion

        if (iRequired > 0):
            #	STEP 12: User Output
            if (self.show_output):
                print("Annie (child-train) {" + ApplicationHelper.time() + "} - Expanding dataset to avoid single class dataset")

            #	STEP 13: Get the output\s that isn't in the new dataset
            lOutputs = []

            #	STEP 14: Loop till done
            while (len(lOutputs) < iRequired):
                #	STEP 15: Get random data sample
                dDNR = dOrg.getRandDNR()

                #	STEP 16: Check if not in new required outputs or current outputs
                if ((dDNR["out"] not in lOutputs) and (dDNR["out"] not in lOutputs_New)):
                    #	STEP 17: Append new output
                    lOutputs.append(dDNR["out"])

            #	STEP 18: Get the size of the new data to append
            iNewSize	= rn.randint(5, 10) / 10.0
            iNewSize	= int( iNewSize * iRequired * dNew.getLen() )

            #	STEP 19: Loop till new set acquired
            i = 0

            while (i < iNewSize):
                #	STEP 20: Get random data sample
                dDNR = dOrg.getRandDNR()

                #	STEP 21: Check if sample is of the required outputs
                if (dDNR["out"] in lOutputs):
                    #	STEP 22: Append new data sample
                    dNew.insert(data=dOrg.copy(last_seen=True))

                    #	STEP 23: Increment counter
                    i += 1

        #
        #endregion

        #	STEP 24: User Output
        if (self.show_output):
            print("Annie (child-train) {" + ApplicationHelper.time() + "} - Starting training process")

        if (bChildOutput):
            print("")

        #region STEP 25->37: Child generations and testing

        #	STEP 25: Set temp vars
        vChild	= None
        fAcc	= 0

        #	STEP 26: Loop through iterations
        for _ in range(0, self.__iIterationsChildGen):
            #	STEP 27: Create child
            vTmpChild = Annie()
            vTmpChild.is_secondary = True

            if (self.show_output):
                vTmpChild.show_output = bChildOutput

            #	STEP 28: Train child
            vTmpChild.trainSet(dNew, advanced_training=False)

            #	STEP 29: Get accuracy
            json_data	= vTmpChild.getAccuracy(data=dNew, size=0, full_set=True)
            fTmp	= json_data["percent accuracy"]

            #	STEP 30: Check if accuracy better than current
            if (fTmp > fAcc):
                #	STEP 31: Check if accuracy == 100%
                if (fTmp == 1.0):
                    #	STEP 32: Set as child for this instance
                    self.secondary_neural_nets = vTmpChild

                    #	STEP 33: User output
                    if (self.show_output):
                        print("Annie (child-train) {" + ApplicationHelper.time() + "} - Child net successfully trained")

                    if (bShowComparison):
                        print("\n***\n")

                        self.secondary_neural_nets.showComparison(dNew)

                        print("\n***\n")

                    #	STEP 34: Exit function
                    return

                else:
                    #	STEP 35: Set as best curr candidate
                    vChild 	= vTmpChild
                    fAcc	= fTmp

        #	STEP 36: Set child as best candidate
        self.secondary_neural_nets = vChild

        #	STEP 37: User output
        if (self.show_output):
            print("Annie (child-train) {" + ApplicationHelper.time() + "} - Child net successfully trained")
            print("\t> Required accuracy not achieved")

        if (bShowComparison):
            print("\n***\n")

            self.secondary_neural_nets.showComparison(dNew)

            print("\n***\n")

        #
        #endregion

        #	STEP 38: Return
        return

    #
    #		endregion

    #		region Back-End-(Training): Classifier

    def __trainClassifier__(self, **kwargs) -> None:
        """
            Description:

                If possible trains a dataset classifier for this instance.

            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:

                + data	= ( vars ) Dataset to train the classifier for this
                    instance

                    ~ Required

                + show_comparison	= ( bool ) Flag that specifies whether or
                    not the comparison of the classification network should be
                    displayed after training

                    ~ Default	= False

                + show_output	= ( bool ) Flag that specifies whether or not
                    the classification network should show output

                    ~ Default	= self.show_output
        """

        #	STEP 0: Local variables
        dData					= None

        bShowComparison			= False
        show_output				= self.show_output

        #	STEP 1: Setup - Local variables

        #	STEP 2: Check if data arg was passed
        if ("data" not in kwargs):
            #	STEP 3: Error handling
            raise Exception("An error occured in Annie.__trainClassifier__() -> Step 2: No data argument passed")

        else:
            #	STEP 4: Set local variable
            dData = kwargs["data"]

        #	STEP 5: Check if show_comparison passed
        if ("show_comparison" in kwargs):
            #	STEP 6: Set local variable
            bShowComparison = kwargs["show_comparison"]

        #	STEP 7: Check if show_output passed
        if ("show_output" in kwargs):
            #	STEP 8: Set local variable
            show_output = kwargs["show_output"]

        #	STEP 9: Check if classifier is allowed for this instance
        if ((self.is_primary == True) and (self.is_secondary == False) and (self.is_classifier == False)):
            #	STEP 10: User output
            if (self.show_output):
                print("\nAnnie (train-classifier) {" + ApplicationHelper.time() + "} - Creating classifier")
            
            #	STEP 11: Create classifier
            self.classifier_neural_net = Annie()

            #	STEP 12: Set as classifier and set output
            self.classifier_neural_net.is_classifier = True
            self.classifier_neural_net.show_output = show_output

            #	STEP 13: User output
            if (self.show_output):
                print("Annie (train-classifier) {" + ApplicationHelper.time() + "} - Training classifier\n")

            #	STEP 14: Train classifier
            self.classifier_neural_net.trainSet(dData, compare=bShowComparison)

        #	STEP 15: Return
        return

    #
    #		endregion

    #		region Back-End-(Training): Trust-Region-Optimization

    def __trainTro__(self, _dData: Data) -> int:
        """
            Description

                Pergorms training of this class through Hermione

            |\n
            |\n
            |\n
            |\n
            |\n

            Params:
            
                :param _dData:	= ( Data ) -- Data Container
                    ~ Required

            |\n

            Returns:

                + iterations	= ( int ) The number of iterations the training
                    process took
        """

        #	STEP 0: Local variables
        vOptimzier				= Hermione()

        dResults				= None

        iPassword				= None

        #	STEP 1: Setup - Local variables
        vOptimzier.show_output	= self.show_output

        iPassword				= self.__resetPassword__()

        #	STEP 2: User Output
        if (self.show_output):
            print("\t- Outsourcing Trust-Region Optimization training to Hermione\n")

        #	STEP 3: Perform training
        dResults = vOptimzier.trainSurrogate(surrogate=cp.deepcopy(self), data=_dData, password=iPassword, optimizer=genetic_algorithm.TRO, threading=True)
        
        #	STEP 4: Set new weights
        self.__setWeights(dResults["surrogate"].getWeights(password=self.__password))

        #	STEP 6: Update password
        self.__resetPassword__()

        #	STEP 7: Return
        return dResults["iterations"]

    #
    #		endregion

    #		region Back-End-(Training): Particle Swarm Optimization

    def __trainPso__(self, _dData: Data) -> int:
        """
            Description:

                Performs training of this class through Hermione.

            |\n
            |\n
            |\n
            |\n
            |\n

            Params:

                :param _dData: 	= ( Data ) -- Data container
                    ~ Required

            |\n

            Returns:
            
                + iterations	= ( int ) The number of iterations the training
                    process took

        """

        #	STEP 0: Local variables
        vOptimizer				= Hermione()

        dResults				= None

        iPassword				= None

        #	STEP 1: Setup - Local variables
        vOptimizer.show_output = self.show_output

        iPassword				= self.__resetPassword__()

        #	STEP 2: User Output
        if (self.show_output):
            print("\t- Outsourcing Particle-Swarm Optimization training to Hermione\n")

        #	STEP 3: Perform training
        dResults = vOptimizer.trainSurrogate(surrogate=cp.deepcopy(self), data=_dData, password=iPassword, optimzier=swarms.PSO, threading=True)

        #	STEP 4: Set new weights
        self.__setWeights(dResults["surrogate"].getWeights(password=self.__password))
        
        #	STEP 6: Update password
        self.__resetPassword__()

        #	STEP 7: Return
        return dResults["iterations"]

    #
    #		endregion

    #
    #endregion

    #region Back-End: Other

    def showComparison(self, _dData: Data) -> None:
        """
        """

        #	STEP 0: Local variables

        #	STEP 1: Setup - Local variables
        _dData.reset()

        #	STEP 2: Print Output
        print("-----------------------------", "\t\tStats\t\t", "-----------------------------")
        print("Learning Rate: ", 	self.learning_rate)
        print("Momentum: ", 		self.momentum)

        print("\n-----------------------------", "\tResult Comparison\t", "-----------------------------")
        for _ in range(0, min(10, _dData.getLen())):
            dDNR = _dData.getRandDNR()

            self.__propagateForward__(dDNR["in"])
            print( MathHelper.round( dDNR["out"], 1) , MathHelper.round( self.getOutput(), 1), sep="\t")

        print("\n-----------------------------", "\tClassification\t\t", "-----------------------------\n")
        
        _dData.reset()
        dHold = self.getAccuracy(data=_dData, size=_dData.getLen(), full_set=True)

        print("Dataset Size: ", 	str( _dData.getLen() ))
        print("Correct Classifications: " + str(dHold["accurate samples"]))

        #	STEP 3: Return
        return

    #
    #endregion

#region	Testing - Training
if (__name__ == "__main__"):
	dat = Data()
	dat.importData(file="4x - Banknote/banknote_0.json")

	x = ""

	while (True):
		x = input("> Continue (Y): ")
		if (x == "exit" or x == "N" or x == "n"):
			break

		os.system("clear")

		fire = Annie()
		
		fire.show_output 	= True
		fire.use_l1_regularization		= False
		fire.use_l2_regularization		= True

		y = fire.trainSet(cp.deepcopy(dat), advanced_training=True, compare=True)

		print("---", "---", sep="\n", end="\n\n")


#endregion
