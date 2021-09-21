#region	--- Imports ---
import copy as cp
import datetime as dt
import json as js
import math as mt
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
    #region	--- init ---
    def __init__(self, **kwargs) -> None:
        #   --- General ---
        self.__config = Conny()
        self.__config.load("ArtificialNeuralNetwork.json")
        self.__password = rn.random() * 111754552.83191288  #  ToDo change to uuid

        rn.seed(dt.datetime.now())
        #   --- Application ---
        self.show_output = None
        self.__bAllowTesting = None
        self.__dHiddenDetails = None
        #   --- Secondary Neural Nets ---
        self.secondary_neural_net_iterations = None
        self.secondary_neural_nets = None
        self.classifier_neural_net = None
        self.is_primary = None
        self.is_classifier = None
        self.is_secondary = None
        #   --- Weights ---
        self.weights = None
        self.weight_range = None
        self.weights_momentum = None
        #   --- Nodes ---
        self.input_width = None
        self.output_width = None
        self.hidden_layers_width = None
        self.number_of_hidden_layers = None
        self.bias_array = None
        self.nodes = None
        self.pre_activation_nodes = None
        self.node_averages = None
        #   --- Activation Functions ---
        self.activation_functions = ActivationFunctionHelper()
        self.current_activation_function = None
        #   --- Training Variables ---
        self.learning_rate = None
        self.use_momentum = None
        self.momentum = None
        self.number_of_epochs = None
        self.batch_size = None
        self.use_bias = None
        self.bias = None
        #   --- Fitness Function ---
        self.accuracy_requirement = None
        self.accuracy_test_sample_size = None
        self.fitness_test_sample_size = None
        #   --- Regularization---
        self.use_drop_out = False
        self.drop_out_array = None
        self.input_nodes_drop_out_rate = None
        self.hidden_nodes_drop_out_rate = None
        self.use_weight_decay = False
        self.weight_decay = None
        self.use_l1_regularization = False
        self.l1_regularization = None
        self.use_l2_regularization = False
        self.l2_regularization = None
        self.use_noise_injection = True
        
        #   --- Setup ---
        if ("params" in kwargs):
            self.__setup_params__(kwargs["params"])
        else:
            self.__setup_params__(self.__config.data["parameters"])

        if ("geometry" in kwargs):
            self.__setup_geometry__(kwargs["geometry"])

        #   --- Response ---
        return

    def __setup_geometry__(self, _dGeometry: dict) -> None:
        """
            - Description:

                Initializes this instance's gemoetry variables; weights and
                nodes are then initialized.
            
            |\n
            |\n
            |\n
            |\n
            |\n
            - Refactoring: ToDo
            - Arguments:

                + in width	= ( int ) The input data width
                    ~ Required

                + out width = ( int ) The output data width
                    ~ Required

                + hidden width	= ( int ) The hidden layer width
                    ~ Required

                + hidden legnth = ( int ) The number of hidden layers
                    ~ Required
        """

        #	STEP 2: Initialize lists
        self.input_width = _dGeometry["in width"]
        self.output_width = _dGeometry["out width"]
        self.hidden_layers_width= _dGeometry["hidden width"]
        self.number_of_hidden_layers = _dGeometry["hidden length"]

        #	STEP 3: Initialize weights and momentumWeights
        self.__setup_nodes__()
        self.__setup_weights__()

        #	STEP 4: Return
        return

    def __setup_params__(self, _dParams: dict) -> None:
        """
            - Description:
            
            |\n
            |\n
            |\n
            |\n
            |\n
            - Refactoring: ToDo
            - Arguments:
        """

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

        self.use_bias				= _dParams["bias"]["use bias"]
        self.number_of_epochs				= _dParams["training methods"]["def"]["epochs"]
        self.batch_size			= _dParams["training methods"]["def"]["batch size"]
        self.accuracy_requirement		= _dParams["training methods"]["def"]["acc requirement"]

        self.hidden_nodes_drop_out_rate		= _dParams["training methods"]["def"]["drop out"]["hidden drop out"]
        self.input_nodes_drop_out_rate		= _dParams["training methods"]["def"]["drop out"]["input drop out"]

        self.weight_decay			= _dParams["training methods"]["def"]["weight decay"]
        self.l1_regularization			= _dParams["training methods"]["def"]["lambda1"]
        self.l2_regularization			= _dParams["training methods"]["def"]["lambda2"]

        self.is_primary				= _dParams["children"]["is fertile"]
        self.is_classifier			= _dParams["children"]["is classifier"]

        self.is_secondary				= _dParams["children"]["is child"]
        self.secondary_neural_net_iterations	= _dParams["children"]["generation iterations"]

        #	STEP 2: Return
        return

    def __setup_weights__(self) -> None:
        """
            - Description:
            
            |\n
            |\n
            |\n
            |\n
            |\n
            - Refactoring: ToDo
            - Arguments:
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

    def __setup_nodes__(self) -> None:
        """
            - Description:
            
            |\n
            |\n
            |\n
            |\n
            |\n
            - Refactoring: ToDo
            - Arguments:
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

        if (self.use_bias):
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
        self.__set_bias_values__()

        #	STEP 9: Return
        return

    #
    #endregion

    #region --- imports/exports ---
    def import_ann(self, **kwargs) -> None:
        """
            - Description:

                Imports an Annie instance from the specified file.
            
            |\n
            |\n
            |\n
            |\n
            |\n
            - Refacroting: ToDo
            - Arguments:

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
            with open(file_path, "r+") as json_file:
                json_data = js.load(json_file)

            #	STEP 12: Child variables
            self.secondary_neural_net_iterations	= json_data["child iterations"]

            self.is_primary				= json_data["is fertile"]
            self.is_classifier			= json_data["is classifier"]
            self.is_secondary				= json_data["is child"]

            #	STEP 13: Check if this instance has a child net
            if (json_data["child"] != None):
                #	STEP 14: Init child net
                self.secondary_neural_nets = Annie()
                self.secondary_neural_nets.import_ann(file=json_data["child"])

            #	STEP 15: Layout variables
            self.weights = json_data["weights"]
            self.weights_momentum = json_data["momentum weights"]
            self.nodes = json_data["nodes"]
            self.pre_activation_nodes = json_data["pre activation nodes"]
            self.node_averages = json_data["average nodes"]
            self.input_width = json_data["input width"]
            self.output_width = json_data["output width"]
            self.hidden_layers_width = json_data["hidden width"]
            self.number_of_hidden_layers = json_data["hidden length"]
            self.weight_range = json_data["weight range"]
            self.current_activation_function = json_data["activation function"]
            self.learning_rate = json_data["learning rate"]
            self.use_momentum = json_data["momentum active"]
            self.momentum = json_data["momentum"]
            self.accuracy_requirement = json_data["accuracy requirement"]
            self.number_of_epochs = json_data["epochs"]
            self.batch_size = json_data["batch size"]
            self.accuracy_test_sample_size = json_data["accuracy sample size"]
            self.fitness_test_sample_size = json_data["fitness sample size"]
            self.show_output = json_data["show output"]
            self.use_bias = json_data["use bias"]
            self.bias = json_data["bias value"]
            self.__bAllowTesting = json_data["allow testing"]
            self.__dHiddenDetails = json_data["hidden layer details"]

        except Exception as ex:
            print("Initial error: ", ex)
            raise Exception("An error occured in Annie.import_ann()")

        #   --- Response ---
        return

    def export_ann(self, **kwargs) -> None:
        """
            - Description:

                Exports this instance of Annie to the specified file location.

            |\n
            |\n
            |\n
            |\n
            |\n
            - Refactoring: ToDo
            - Arguments:

                :arg file: >> [required][str] The file path this instance should be
                    exported
                    ~ Required

                :arg full_path: >> [bool] Specifies if the full path was provided
                    in the <file> argument

                :arg extension: >> [bool] Specifies if the file extension has been
                    appended to the <file> argument
                    ~ False = appends .json to the end of the path
        """

        json_data = None
        file_path = None
        json_file = None

        try:
            json_data = {
                "child iterations": self.secondary_neural_net_iterations,
                "is fertile": self.is_primary,
                "is classifier": self.is_classifier,
                "is child": self.is_secondary,
                "weights": ArrayHelper.getList(self.weights),
                "momentum weights": ArrayHelper.getList(self.weights_momentum),
                "nodes": ArrayHelper.getList(self.nodes),
                "pre activation nodes": ArrayHelper.getList(self.pre_activation_nodes),
                "average nodes": ArrayHelper.getList(self.node_averages),
                "input width": self.input_width,
                "output width": self.output_width,
                "hidden width": self.hidden_layers_width,
                "hidden length": self.number_of_hidden_layers,
                "hidden layer details": self.__dHiddenDetails,
                "weight range": self.weight_range,
                "activation function": self.current_activation_function,
                "learning rate": self.learning_rate,
                "momentum active": self.use_momentum,
                "momentum": self.momentum,
                "accuracy requirement": self.accuracy_requirement,
                "epochs": self.number_of_epochs,
                "batch size": self.batch_size,
                "accuracy sample size": self.accuracy_test_sample_size,
                "fitness sample size": self.fitness_test_sample_size,
                "allow testing": self.__bAllowTesting,
                "show output": self.show_output,
                "use bias": self.use_bias,
                "bias value": self.bias,
                "child": ""
            }

            #   --- Export Secondary ANN ---
            if (self.secondary_neural_nets != None):
                json_data["child"] = kwargs["file"] + "_child"
                self.secondary_neural_nets.export_ann(file=json_data["child"], extension=False)

            #   --- Check if full file path ---
            if ("full_path" in kwargs):
                if (kwargs["full_path"] == True):
                    file_path = kwargs["file"]

            #   --- Check if not full file path ---
            if (file_path == None):
                file_path = os.path.abspath(".") + "\\Data\\Exports\\Surrogates\\" + kwargs["file"]
                if ("extension" in kwargs):
                    if (kwargs["extension"] == False):
                        file_path = file_path + ".json"

            #   --- Export file ---
            json_file = open(file_path, "a")
            json_file.close()
            with open(file_path, "r+") as json_file:
                js.dump(json_data, json_file, indent=4, separators=(", ", " : "))

        except Exception as ex:
            print("Initial error: ", ex)
            raise Exception("An error occured in Annie.export_ann()")

        #   --- Response ---
        return

    #
    #endregion

    #region --- is-type statements ---
    def is_accurate(self, expected_output_values: list, **kwargs) -> bool:
        """
            - Description:
                Checks if the current output of the layer is accurate compared
                to the provided expected output.

            |\n
            |\n
            |\n
            |\n
            |\n
            - Refactoring: Done
            - Response:

                + bAccurate	= ( bool )

                + RMSD	= ( bool ) Flag to indicate if the RMSD should be used
                    ~ Default	= False
        """
        #   --- variables --
        ann_outputs = self.get_ann_output()
        use_rmsd = False

        #   --- setup ---
        if ("RMSD" in kwargs):
            use_rmsd = kwargs["RMSD"]

        #   --- functionality (probz-bad) ---
        if (use_rmsd == False):
            accuracy_deviation_margin = self.__config.data["parameters"]["accuracy margin"]
            number_of_correct_nodes = 0

            for i in range(0, len( ann_outputs ) ):
                if (mt.fabs(ann_outputs[i] - expected_output_values[i]) <= accuracy_deviation_margin):
                    number_of_correct_nodes += 1
                
            if (number_of_correct_nodes == len( ann_outputs ) ): return True            
            return False
        
        #   --- functionality (RMSD) ---
        else:
            deviation_sum = 0.0

            for i in range(0, len( ann_outputs ) ):
                deviation_sum += np.power( expected_output_values[i] - ann_outputs[i], 2)

            rmsd = np.sqrt( deviation_sum / float( len( ann_outputs ) ) )
            
            #   ToDo : this should return the actual rmsd as the fitness of this node, shouldn't it? xD
            if (rmsd <= self.__config.data["parameters"]["accuracy margin"]): return True
            return False

    #
    #endregion

    #region --- gets ---
    def get_accuracy(self, **kwargs) -> dict:
        """
            - Description:

                Gets the accuracy of this instance using the provided dataset.

            |\n
            |\n
            |\n
            |\n
            |\n
            - Refactoring: Done
            - Arguments:

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
            - Response:

                + dDetails	= ( dict ) Dictionary containing the following
                    ~ child dataset = ( vars ) Child dataset that was created
                        using samples that tested inaccurate
                    ~ percent accuracy	= ( float ) The accuracy of this 
                        instance as a percentage
                    ~ iterations 	= ( int ) The number of samples used for
                        the test
                    ~ accurate samples	= ( int ) The amount of accurat samples
        """
        
        #   --- Variables ---
        accurate_data_point = 0
        child_dataset = Data()
        should_split_data = False
        test_data = None
        test_iterations = 1
        
        #   --- Setup (data) ---
        if ("data" not in kwargs):
            raise Exception("An error occured in Annie.get_accuracy(): No 'data' argument passed")
        else:
            test_data = cp.deepcopy(kwargs["data"])
            test_data.reset()

        #   --- Setup (Test Size) ---
        if (("full_set" in kwargs) and (kwargs["full_set"] == True)): test_iterations = test_data.getLen()
        elif ("size" not in kwargs): test_iterations = self.accuracy_test_sample_size
        elif (kwargs["size"] > self.accuracy_test_sample_size): test_iterations = self.accuracy_test_sample_size
        else: test_iterations = max(kwargs["size"], 1)

        #   --- Setup (Data Split) ---
        if ("split" in kwargs): should_split_data = kwargs["split"]

        #   --- Functionality ---
        for _ in range(0, test_iterations):
            data_point = test_data.getRandDNR()
            
            self.__propagate_forward__(data_point["in"])

            if (self.is_accurate(data_point["out"], RMSD=True)): accurate_data_point += 1
            elif (should_split_data): child_dataset.insert(data=test_data.pop(last_seen=True))

        #   --- Response ---
        return {
            "accurate samples": accurate_data_point,
            "child dataset": child_dataset,
            "iterations": test_iterations,
            "percent accuracy": float(accurate_data_point) / test_iterations,
        }

    def get_fitness_of_array(self, **kwargs) -> float:
        """
            - Description:

                Returns the sum of the fitness of a number of samples in the
                provided dataset.

            |\n
            |\n
            |\n
            |\n
            |\n
            - Refactoring: Done
            - Arguments:
            
                + data = ( vars ) The dataset to use for testing
                    ~ Required

                + debug = ( bool ) Flag that specifies if the dataset stats
                    should be printed
            
            |\n
            - Response: ToDo
        """
        
        #   --- Variables ---
        data_set = None
        iterations = self.fitness_test_sample_size
        response = 0.0
        
        #   --- Setup (Data Set) ---
        if ("data" not in kwargs):
            raise Exception("An error occured in Annie.get_fitness_of_array() -> Step 2: No data argument passed")
        else:
            data_set = kwargs["data"]
            data_set.reset()
            
        #   --- Setup (Iterations) ---
        if (data_set.getLen() < self.fitness_test_sample_size): iterations = data_set.getLen()

        #   --- Setup (Debug) ---
        if (("debug" in kwargs) and (kwargs["debug"] == True)): data_set.stats()

        #   --- Functionality ---
        for _ in range(0, iterations):
            data_point = data_set.getRandDNR()
            self.__propagate_forward__(data_point["in"])
            response += self.get_ann_fitness(data_point["out"])

        #   --- Response ---
        return response

    def get_ann_error(self, expected_output_values: list) -> list:
        """
            - Description:
            
            |\n
            |\n
            |\n
            |\n
            |\n
            - Refactoring: Done
            - Arguments:
            - Response:
        """
        
        #   --- Variables ---
        response = []
        ann_output = self.get_ann_output()

        #   --- Functionality ---
        for i in range(0, len(expected_output_values)):
            response.append(expected_output_values[i] - ann_output[i])

        #   --- Response ---
        return response

    def get_ann_fitness(self, expected_output_values: list) -> float:
        """
            - Description:
            
            |\n
            |\n
            |\n
            |\n
            |\n
            - Refactoring: Done
            - Arguments:
            - Response
        """

        #   --- Variables ---
        response = 0.0
        lTmp = self.get_ann_error(expected_output_values)

        #   --- Functionality ---
        for i in range(0, len(lTmp)):
            response += abs(lTmp[i])
        
        #   --- Response ---
        return response

    def get_ann_output(self, **kwargs) -> list:
        """
            - Description:

                Returns the rounded output of this instance.

            |\n
            |\n
            |\n
            |\n
            |\n
            - Refactoring: Done
            - Arguments:

                + round = ( bool ) Flag for if rounding should be used in the return

            - Response:

                + response = ( list ) The output layer of this instance
        """
        
        #   --- Variables ---
        response = self.nodes[self.number_of_hidden_layers + 1]

        #   --- Functionality ---
        if (("round" in kwargs) and (kwargs["round"] == True)):
            for i in range(0, len(response)):
                response[i] = round(response[i], 5)

        #   --- Response ---
        return response

    def get_ann_output_and_reset(self, input_data: list) -> vars:
        """
            - Description:
            
            |\n
            |\n
            |\n
            |\n
            |\n
            - Refactoring: Done
            - Arguments: 
            - Response:
        """

        #   --- Propagate ---
        self.__propagate_forward__(input_data)
        response = np.ndarray.tolist(cp.deepcopy(self.get_ann_output()))

        #   --- Reset ---
        self.__reset_nodes__()

        #   --- Response ---
        if (len(response) == 1): return response[0]
        return response

    def get_weights(self, **kwargs) -> list:
        """
            - Description:

                Returns this class isntance's weight list if the provided password
                matches this instance's password.

            |\n
            |\n
            |\n
            |\n
            |\n
            - Refactoring: Done
            - Arguments:

                + password = ( int/float ) This class' password
                    ~ Required

            |\n
            - Response:

                + list = ( list )
                    ~ A deep copy of this class' weights
        """
        #   --- Protection ---
        if (("password" not in kwargs) or (kwargs["password"] != self.__password)):
            raise Exception("An error occured in Annie.get_weights(): The provided password doesn't match this class' password")

        #   --- Response ---
        return cp.deepcopy(self.weights)

    def __get_classification_set__(self, **kwargs) -> dict:
        """
            - Description:

                Creates a new dataset using the provided dataset. The new
                dataset groups the data that is correctly classified by this
                parent instance and the data that is incorrectly classified
                into unique classes:

            |\n
            |\n
            |\n
            |\n
            |\n
            - Refactoring: Done
            - Arguments:

                + data	= ( vars ) The dataset to adjust
                    ~ Required
                    
            |\n
            - Response: ToDo
        """

        #   --- Variables ---
        new_data_set = Data()
        old_data_set = None

        #   --- Setup ---
        if ("data" not in kwargs):
            raise Exception("An error occured in Annie.__get_classification_set__() -> Step 2: No data argument passed")
        else:
            old_data_set = kwargs["data"]
            old_data_set.reset()

        #   --- Functionality ---
        for _ in range(0, old_data_set.getLen()):
            data_point = old_data_set.getRandDNR()
            self.__propagate_forward__(data_point["in"])

            if (self.is_accurate(data_point["out"], RMSD=True)):
                new_data_set.insert(data={
                    "in": data_point["in"],
                    "out": [1.0, -1.0]
                })

            else:
                new_data_set.insert(data={
                    "in": data_point["in"],
                    "out": [-1.0, 1.0]
                })

        #   --- Response ---
        return {
            "new set": new_data_set
        }

    def __get_geometry__(self, data_set: Data) -> dict:
        """
            - Description:
            
            |\n
            |\n
            |\n
            |\n
            |\n
            - Refactoring: Done
            - Arguments:
            - Response:
        """
        
        #   --- Variables ---
        hidden_layers_length = 1
        input_width = data_set.getInputWidth()
        output_width = data_set.getOutputWidth()
        hidden_layer_width = input_width + int(rn.random() * input_width)

        #   --- Functionality ---
        if (( self.__dHiddenDetails["is shallow"] ) and ( rn.uniform(0.0, 1.0) < 0.95 ) and ( self.use_drop_out == False ) ):
            temp_float = rn.uniform(0.0, 1.0)
            probability_config	= self.__dHiddenDetails["probabilities"] 

            if (temp_float < probability_config["2"]): hidden_layers_length = 2
            elif (temp_float < probability_config["2"] + probability_config["3"]): hidden_layers_length = 3

        else:
            hidden_layers_length = min(input_width + int(rn.random() * input_width), rn.randint(4, 7))
            if (self.show_output):
                print("Annie (get-geo) {" + ApplicationHelper.time() + "} - Initializing deep net")
                print("\t~ Depth: " + str(hidden_layers_length), end="\n\n")

        #   --- Response ---
        return {
            "in width": 		input_width,
            "out width": 		output_width,
            "hidden width":		hidden_layer_width,
            "hidden length":	hidden_layers_length
        }

    def __get_wheights_shape__(self) -> list:
        """
            - Description:
            
            |\n
            |\n
            |\n
            |\n
            |\n
            - Refactoring: Done
            - Arguments:
            - Response:
        """

        #   --- Variables ---
        response = []

        #   --- Functionality ---
        for i in range(0, len(self.weights)):
            response.append(np.zeros(len(self.weights[i])))
        
        #   --- Response ---
        return response

    def __get_nodes_shape__(self) -> list:
        """
            - Description:
            
            |\n
            |\n
            |\n
            |\n
            |\n
            - Refactoring: Done
            - Arguments:
            - Response:
        """

        #   --- Variables ---
        response = []

        #   --- Functionality ---
        for i in range(0, len(self.nodes)):
            response.append(np.zeros(len(self.nodes[i])))
        
        #   --- Response ---
        return response

    #
    #endregion

    #region --- sets ---
    def set_activation_function(self, **kwargs) -> None:
        """
            - Description:

                Sets the activation function for the class to match the range
                of weights that will be used and updates the learning rate
                accordingly

            |\n
            |\n
            |\n
            |\n
            |\n
            - Refactoring: Done
            - Arguments:

                + password		= ( int/float ) This class' password
                    ~ Required
                + algorithm		= ( str ) Name of the algorithm being used
                    ~ Required
                + scalar		= ( float ) The scalar to use
                    ~ Required
                    
            - Response:
        """
        
        #   --- Protection ---
        if (("password" not in kwargs) and (kwargs["password"] != self.__password)):
            raise Exception("An error occured in Annie.set_activation_function(): Passed password does not match this class' password")

        #   --- Outsource ---
        self.__set_activation_function__(algorithm=kwargs["algorithm"], scalar=kwargs["scalar"])

        #   --- Response ---
        return

    def set_weights(self, **kwargs) -> None:
        """
            - Description:

                Sets this class' weights to be the provided weights.

            |\n
            |\n
            |\n
            |\n
            |\n
            - Refactoring: Done
            - Arguments:

                + password		= ( int/float ) This class' password
                    ~ Required
                + weights 		= ( list ) The weights to update to
                    ~ Required
            
            - Response:
        """
        
        #   --- Protection ---
        if (("password" not in kwargs) and (kwargs["password"] != self.__password)):
            raise Exception("An error occured in Annie.set_weights(): The provided password doesn't match this class' password")

        #   --- Requirements ---
        if ("weights" not in kwargs):
            raise Exception("An error occured in Annie.set_weights() -> Step 6: No weights provided to update to")

        #   --- Functionality ---
        self.weights = kwargs["weights"]

        #	--- Response ---
        return

    def __set_activation_function__(self, **kwargs) -> None:
        """
            - Description:

                Sets the activation function for the class to match the range
                of weights that will be used and updates the learning rate
                accordingly

            |\n
            |\n
            |\n
            |\n
            |\n
            - Refactoring: Done
            - Arguments:
            
                + algorithm		= ( str ) Name of the algorithm that's updating
                    ~ Required
                + scalar		= ( float ) The scalar to use
                    ~ Required

            - Response:
        """
        
        try:
            #   --- Safety First ---
            if ("algorithm" not in kwargs):
                raise Exception("An error occured in Annie.__set_activation_function__() -> Step 3: No algorithm passed")

            if ("scalar" not in kwargs):
                raise Exception("An error occured in Annie.__set_activation_function__() -> Step 5: No scalar passed")

            if (kwargs["algorithm"] == "def"):
                return

            #   --- TRO ---
            if (kwargs["algorithm"] == "tro"):
                random_value = float( 6.5 * kwargs["scalar"] )
                self.activation_functions.setFunction(function=self.current_activation_function, c=float( 2.0 / random_value ))
                self.learning_rate = self.learning_rate * ( random_value / 2.0 )

            #	--- PSO ---
            if (kwargs["algorithm"] == "pso"):
                scalar = kwargs["scalar"]
                self.activation_functions.setFunction(function=self.current_activation_function, c=float( 2.0 / scalar ))
                self.learning_rate = self.learning_rate * float ( scalar / 2.5 )

            #	--- Error Handling ---
            raise Exception("An error occured in Annie.__set_activation_function__() -> Step 19: Unimplemented algorithm passed")

        except Exception as ex:
            #	--- Error Handling ---
            print("Initial Error: ", ex)
            raise Exception("An error occured in Annie.__set_activation_function__()")

        #	--- Response ---
        return

    def __set_bias_values__(self) -> None:
        """
            - Description:
            
            |\n
            |\n
            |\n
            |\n
            |\n
            - Refactoring: Done
            - Arguments:
            - Response:
        """

        #   --- Functionality ---
        if (self.use_bias):
            for i in range(0, len(self.bias_array)):
                self.bias_array[i] = self.bias
        
        #   --- Response ---
        return

    #
    #endregion

    #region --- training ---
    def train_set(self, data_set: Data, **kwargs) -> dict:
        """
            - Description:

                Trains this instance of Annie using the data set provided as
                well as the parameters in kwargs.

            |\n
            |\n
            |\n
            |\n
            |\n
            - Refactoring: Done
            - Parameters:

                :param data_set: >> ( vars ) -- The data container containing the
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
            - Response:

                + dResults		= ( dict ) Dictionary containing
                    ~ result	= ( int ) Number of iterations training took
                    ~ check accuracy	= ( bool ) Accuracy check flag
                    ~ show comparison	= ( bool ) Show comparison flag
                    ~ use optimization	= ( bool ) Advanced training flag
                    ~ optimization algorithm	= ( int ) Optimizer used for
                        advanced training 

        """

        #   --- Variables ---
        advanced_algorithm = rn.randint(0, 1)
        check_accuracy = True
        compare_results = False
        advanced_training = False
        training_results = None

        #   --- Setup ---
        data_set.reset()

        if ("acc" in kwargs): check_accuracy = kwargs["acc"]
        if ("compare" in kwargs): compare_results = kwargs["compare"]
        if ("advanced_training" in kwargs): advanced_training = kwargs["advanced_training"]
        if ("advanced_algorithm" in kwargs): advanced_algorithm = kwargs["advanced_algorithm"]
        if (self.weights == None): self.__setup_geometry__(self.__get_geometry__(data_set))

        #   --- DEF ---
        if (advanced_training == False):
            if (self.show_output):
                print("Annie (train-set) {" + ApplicationHelper.time() + "} - Training via Default Training")

            training_results = self.__perform_default_training__(data_set, check_accuracy)

        #   --- TRO and DEF ---
        elif ((advanced_training == True) and (advanced_algorithm == 0)):
            if (self.show_output):
                print("Annie (train-set) {" + ApplicationHelper.time() + "} - Training via Trust-Region Optimization assisted Default training")

            self.__perform_tro_training__(data_set)
            training_results = self.__perform_default_training__(data_set, check_accuracy)

        #   --- PSO and DEF ---
        elif ((advanced_training == True) and (advanced_algorithm == 1)):
            if (self.show_output):
                print("Annie (train-set) {" + ApplicationHelper.time() + "} - Training via Particle-Swarm Optimization assisted Default training")

            self.__preform_pso_training__(data_set)
            training_results = self.__perform_default_training__(data_set, check_accuracy)


        #	--- Compare Results? ---
        if (compare_results):
            self.show_comparison(data_set)

        #   --- Response ---
        return {
            "fitness":					training_results["fitness"],
            "iterations":				training_results["iterations"],
            "check accuracy": 			check_accuracy,
            "show comparison": 			compare_results,
            "use optimization": 		advanced_training,
            "optimization algorithm": 	advanced_algorithm
        }

    def propagate_forward(self, inputs: list, **kwargs) -> None:
        """
            - Description:

                Performs forward propagation using the provided input.

            |\n
            |\n
            |\n
            |\n
            |\n
            - Refactoring: Done
            - Arguments:

                + inputs = ( list ) Data point
                    ~ Required
                + password = ( int/float ) This class' password
                    ~ Required
            
            - Response:
        """
        
        #   --- Protection ---
        if (("password" not in kwargs) and (kwargs["password"] != self.__password)):
            raise Exception("An error occured in Annie.propagate_forward(): Passed password does not match this class' password")

        #   --- Functionality ---
        self.__propagate_forward__(inputs)

        #   --- Response ---
        return

    def propagate_backward(self, outputs: list, **kwargs) -> None:
        """
            - Description:

                Perform back propagation using the provided output.

            |\n
            |\n
            |\n
            |\n
            |\n
            - Refactoring: Done
            - Arguments:

                + outputs = ( list ) Data point
                    ~ Required
                + password = ( int/float ) This class' password
                    ~ Required
            
            - Response:
        """
        
        #   --- Protection ---
        if (("password" not in kwargs) and (kwargs["password"] != self.__password)):
            raise Exception("An error occured in Annie.propagate_forward(): Passed password does not match this class' password")

        #   --- Functionality ---
        self.__propagate_backward__(outputs)

        #   --- Response ---
        return

    def __perform_default_training__(self, _dData: Data, _bCheckAcc: bool) -> int:
        """
            - Description:

                Performs default forward and backward propagation training
                using the provided dataset.

            |\n
            |\n
            |\n
            |\n
            |\n
            - Refactoring: Done
            - Parameters:
            
                :param _dData: = ( vars ) -- Data container
                :param _bCheckAcc: = ( bool ) -- Check accuracy flag

            |\n
            - Response:

                + dOut	= ( dict )
                    ~ iterations	= ( int ) The amount of iterations used
                        during training

                    ~ child set	= ( vars ) The child data set created from the
                        incorrecy data samples
        """

        #   --- Variables ---
        best_training_result_weights = self.get_weights(password=self.__password)
        best_training_result_fitness = np.inf
        training_set_fitness_scalar = 30.0
        testing_set_fitness_scalar = 70.0
        batch_size = self.batch_size
        number_of_epochs = self.number_of_epochs
        dData_Training = _dData.splitData()
        dData_Testing = dData_Training["testing"]
        dData_Training = dData_Training["training"]        
        number_of_batches = int( np.ceil( dData_Training.getLen() / batch_size ) )

        #   --- Setup ---        
        if (self.use_drop_out):
            number_of_epochs	= int(number_of_epochs * 0.65)

        if ( dData_Training.getLen() < batch_size ):
            training_set_fitness_scalar = 80.0
            testing_set_fitness_scalar = 20.0

        #   --- Output ---
        if (self.show_output):
            print("Annie (def-training) {" + ApplicationHelper.time() + "} - Starting default training")
            print("\t~ Epochs:\t\t"				+ str(number_of_epochs))
            print("\t~ Batches per Epoch:\t"	+ str(number_of_batches))
            print("\t~ Batch size:\t\t"			+ str(batch_size))
            print("\t~ Dataset size:\t\t"		+ str(dData_Training.getLen()) + "\n")

            print("\t~ Node Drop Out:\t\t" 			+ str(self.use_drop_out))
            print("\t~ Gaussian Noise Injection:\t"	+ str(self.use_noise_injection))
            print("\t~ Weight Decay:\t\t\t"			+ str(self.use_weight_decay))
            print("\t~ L1 Regularization:\t\t" 		+ str(self.use_l1_regularization))
            print("\t~ L2 Regularization:\t\t"		+ str(self.use_l2_regularization) + "\n")
        
        #   --- Functionality ---
        for i in range(0, number_of_epochs):
            for j in range(0, number_of_batches):
                #   --- Propagation ---
                for _ in range(0, batch_size):
                    data_point = dData_Training.getRandDNR(noise=self.use_noise_injection)
                    if (self.use_drop_out): self.__propagate_forward__(data_point["in"], training=True)
                    else: self.__propagate_forward__(data_point["in"])
                    self.__propagate_backward__(data_point["out"])

                #   --- Fitness Test ---
                testing_set_acc_test = self.get_accuracy(data=dData_Testing, size=dData_Testing.getLen())
                training_set_acc_test = self.get_accuracy(data=dData_Training, size=dData_Training.getLen())
                batch_fitness = 100.0 * ( 1.0 - testing_set_acc_test["percent accuracy"] ) * ( 1.01 - training_set_acc_test["percent accuracy"] ) + testing_set_fitness_scalar * ( 1.0 - testing_set_acc_test["percent accuracy"] ) + training_set_fitness_scalar * ( 1.01 - training_set_acc_test["percent accuracy"] )

                if (batch_fitness < best_training_result_fitness):
                    best_training_result_weights = self.get_weights(password=self.__password)
                    best_training_result_fitness = batch_fitness

                    #   --- Output ---
                    if (self.show_output):
                        print("\t{" + ApplicationHelper.time() + "} -", "Fitness: " + str( round( best_training_result_fitness, 2 ) ) + "\t", "Test: " + str( round( testing_set_acc_test["percent accuracy"], 2) ), "Train: " + str( round( training_set_acc_test["percent accuracy"], 2) ), "Index: " + str(i) + "-" + str(j), sep="\t")

                #	--- Not Converging ---
                elif ( batch_fitness > 5.0 * best_training_result_fitness ):
                    #   --- Output ---
                    if (self.show_output):
                        print("\t{" + ApplicationHelper.time() + "} - \tEnding epoch " + str(i) + " early by " + str( number_of_batches - j ) + " batch iterations")
                        
                    break

        #   --- Finish Up ---
        self.weights = best_training_result_weights
        training_set_acc_test = self.get_accuracy(data=_dData, full_set=True)
        total_training_iterations = self.number_of_epochs * (number_of_batches * batch_size)

        #   --- Output ---
        if (self.show_output):
            accuracy_samples = training_set_acc_test["accurate samples"]
            percent_accuracy = training_set_acc_test["percent accuracy"]

            print("")
            print("\t- Iterations: " + str(total_training_iterations))
            print("\t- Accurate Samples: " + str(accuracy_samples))
            print("\t- Percentage Accuracy: " + str(round(percent_accuracy * 100.0, 2)) + "%\n")
        
        #   --- Response ---	
        return {
            "iterations":	total_training_iterations,
            "fitness":		best_training_result_fitness,
            "child set":	training_set_acc_test["child dataset"]
        }

    def __perform_tro_training__(self, _dData: Data) -> int:
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

        iPassword				= self.__reset_password__()

        #	STEP 2: User Output
        if (self.show_output):
            print("\t- Outsourcing Trust-Region Optimization training to Hermione\n")

        #	STEP 3: Perform training
        dResults = vOptimzier.trainSurrogate(surrogate=cp.deepcopy(self), data=_dData, password=iPassword, optimizer=genetic_algorithm.TRO, threading=True)
        
        #	STEP 4: Set new weights
        self.weights = dResults["surrogate"].get_weights(password=self.__password)

        #	STEP 6: Update password
        self.__reset_password__()

        #	STEP 7: Return
        return dResults["iterations"]

    def __preform_pso_training__(self, _dData: Data) -> int:
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

        iPassword				= self.__reset_password__()

        #	STEP 2: User Output
        if (self.show_output):
            print("\t- Outsourcing Particle-Swarm Optimization training to Hermione\n")

        #	STEP 3: Perform training
        dResults = vOptimizer.trainSurrogate(surrogate=cp.deepcopy(self), data=_dData, password=iPassword, optimzier=swarms.PSO, threading=True)

        #	STEP 4: Set new weights
        self.weights = dResults["surrogate"].get_weights(password=self.__password)
        
        #	STEP 6: Update password
        self.__reset_password__()

        #	STEP 7: Return
        return dResults["iterations"]

    def __propagate_forward__(self, _dataPoint: list, **kwargs) -> None:
        """
        """

        #	STEP 0: Local variables

        #	STEP 1: Setup - Local variables
        self.__reset_nodes__()

        #	STEP 2: Check - Data width
        if (len(_dataPoint) != self.input_width):
            #	STEP 3: Error handling
            raise Exception("An error occured in Annie.__propagate_forward() -> Step 2: Data input width mismatch")		

        #	STEP 5: Update - Drop out list
        self.drop_out_array	= ArrayHelper.getShape(self.nodes)
            
        #	STEP 6: Iterate through inputs
        for i in range(0, len(_dataPoint)):
            #	STEP 7: Check if drop out
            if ((self.use_drop_out) and (rn.uniform(0.0, 1.0) < self.input_nodes_drop_out_rate) and ("training" in kwargs)):
                #	STEP 8: Set node as dropout
                self.nodes[0][i]		= 0.0
                self.drop_out_array[0][i]	= True

            #	STEP 9: Not dropout
            else:
                #	STEP 10: Update - Node
                self.nodes[0][i] 	= _dataPoint[i]
                self.drop_out_array[0][i]	= False

        #	STEP 11: Check if using bias
        if (self.use_bias):
            #	STEP 12: Update - Bias nodes
            self.nodes[0][len(self.nodes[0]) - 1] = self.bias_array[0]
        
        #	STEP 13: Propagate each layer foward
        for i in range(1, len(self.nodes)):
            #	STEP 14: Get the length of the layer
            iTmp 			= len(self.nodes[i])
            iTmp_Iterations	= iTmp

            #	STEP 15: Check if bias is being used and not output layer
            if ((self.use_bias) and (i != len(self.nodes) - 1)):
                #	STEP 16: Set pre activation bias node
                self.pre_activation_nodes[i][iTmp - 1] 	= self.bias_array[i]

                #	STEP 17: Set bias node
                self.nodes[i][iTmp - 1] 					= self.activation_functions.activation_function(self.current_activation_function, self.bias_array[i])

                #	STEP 18: Adjust layer length
                iTmp_Iterations 							-= 1

            #	STEP 19: Iterate through the nodes in the layer
            for j in range(0, iTmp_Iterations):
                #	STEP 20: Check - Dropout status
                if ((self.use_drop_out) and (rn.uniform(0.0, 1.0) < self.hidden_nodes_drop_out_rate) and (i != len(self.nodes) - 1) and ("training" in kwargs)):
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

    def __propagate_backward__(self, expected_output_values: list) -> None:
        """
        """
        
        #	STEP 0: local variables
        lNodeSig				= None
        lNodeErr				= None
        lWeightErr				= None

        lTmpError				= None

        #	STEP 1: Setup - Local variables
        lNodeSig 	= self.__get_nodes_shape__()
        lNodeErr 	= self.__get_nodes_shape__()
        lWeightErr 	= self.__get_wheights_shape__()

        lTmpError	= self.get_ann_error(expected_output_values)

        #	STEP 2: Get sigmas for all node layers - iterate through layers
        lNodeSig    = self.__get_ann_sigmas__(lNodeSig)

        #	STEP 3: Get node errors
        lNodeErr    = self.__get_node_errors__(lTmpError, lNodeSig, lNodeErr)

        #	STEP 4: Get weight errors
        lWeightErr  = self.__get_weight_errors__(lNodeSig, lNodeErr, lWeightErr)

        #	STEP 5: Update weights
        self.__update_weights__(lWeightErr)

        #	STEP 6: Return
        return

    def __get_ann_sigmas__(self, _lNodeSig: list) -> list:
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

    def __get_node_errors__(self, _lError: list, _lNodeSig: list, _lNodeErr: list) -> list:
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
                if ((self.use_bias) and (i <= iLastRow - 2)):
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

    def __get_weight_errors__(self, _lNodeSig: list, _lNodeErr: list, _lWeightErr: list) -> list:
        """
        """

        #	STEP 0: local variables

        #	STEP 1: Setup - Local variables

        #	STEP 2: Iterate through weight layers
        for i in range(0, len(_lWeightErr)):
            #	STEP 3: Get length of node layer
            iTmpLen     = len(_lNodeErr[i + 1])
            iIterations	= iTmpLen
            
            if ((self.use_bias) and (i < len(_lWeightErr) - 1)):
                iIterations -= 1

            #	STEP 4: Iterate through nodes in layer
            for j in range(0, len(_lNodeErr[i])):
                #	STEP 5: Iterate through attached weights
                for k in range(0, iIterations):
                    #	STEP 6: Set the weight error
                    _lWeightErr[i][j * iTmpLen + k] = round(self.nodes[i][j] * _lNodeSig[i+1][k] * _lNodeErr[i+1][k], 6)

        #	STEP 7: Return
        return _lWeightErr

    def __update_weights__(self, _lWeightErr: list) -> None:
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

    def	__train_secondary_ann__(self, **kwargs) -> None:
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

        ann_outputs_New			= None
        ann_outputs_Org			= None

        bshow_comparison			= False
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
            raise Exception("An error occured in Annie.__train_secondary_ann__() -> Step 4: No data argument passed")

        #	STEP 6: Check if original data passed
        if ("original_data" not in kwargs):
            #	STEP 7: Error handling
            raise Exception("An error occured in Annie.__train_secondary_ann__() -> Step 6: No original_data argument passed")
            
        #	STEP 8: Check if acc_check arg passed
        if ("show_comparison" in kwargs):
            #	STEP 9: Set variable
            bshow_comparison = kwargs["show_comparison"]

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

        ann_outputs_New = dNew.getUniqueOutputs()
        ann_outputs_Org = dOrg.getUniqueOutputs()

        #	STEP 11: Check if num outputs is same
        iRequired	= len(ann_outputs_Org) - len(ann_outputs_New)

        #region STEP 12->23: Data set expansion

        if (iRequired > 0):
            #	STEP 12: User Output
            if (self.show_output):
                print("Annie (child-train) {" + ApplicationHelper.time() + "} - Expanding dataset to avoid single class dataset")

            #	STEP 13: Get the output\s that isn't in the new dataset
            ann_outputs = []

            #	STEP 14: Loop till done
            while (len(ann_outputs) < iRequired):
                #	STEP 15: Get random data sample
                dDNR = dOrg.getRandDNR()

                #	STEP 16: Check if not in new required outputs or current outputs
                if ((dDNR["out"] not in ann_outputs) and (dDNR["out"] not in ann_outputs_New)):
                    #	STEP 17: Append new output
                    ann_outputs.append(dDNR["out"])

            #	STEP 18: Get the size of the new data to append
            iNewSize	= rn.randint(5, 10) / 10.0
            iNewSize	= int( iNewSize * iRequired * dNew.getLen() )

            #	STEP 19: Loop till new set acquired
            i = 0

            while (i < iNewSize):
                #	STEP 20: Get random data sample
                dDNR = dOrg.getRandDNR()

                #	STEP 21: Check if sample is of the required outputs
                if (dDNR["out"] in ann_outputs):
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
        for _ in range(0, self.secondary_neural_net_iterations):
            #	STEP 27: Create child
            vTmpChild = Annie()
            vTmpChild.is_secondary = True

            if (self.show_output):
                vTmpChild.show_output = bChildOutput

            #	STEP 28: Train child
            vTmpChild.train_set(dNew, advanced_training=False)

            #	STEP 29: Get accuracy
            json_data	= vTmpChild.get_accuracy(data=dNew, size=0, full_set=True)
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

                    if (bshow_comparison):
                        print("\n***\n")

                        self.secondary_neural_nets.show_comparison(dNew)

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

        if (bshow_comparison):
            print("\n***\n")

            self.secondary_neural_nets.show_comparison(dNew)

            print("\n***\n")

        #
        #endregion

        #	STEP 38: Return
        return

    def __train_classifier__(self, **kwargs) -> None:
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

        bshow_comparison			= False
        show_output				= self.show_output

        #	STEP 1: Setup - Local variables

        #	STEP 2: Check if data arg was passed
        if ("data" not in kwargs):
            #	STEP 3: Error handling
            raise Exception("An error occured in Annie.__train_classifier__() -> Step 2: No data argument passed")

        else:
            #	STEP 4: Set local variable
            dData = kwargs["data"]

        #	STEP 5: Check if show_comparison passed
        if ("show_comparison" in kwargs):
            #	STEP 6: Set local variable
            bshow_comparison = kwargs["show_comparison"]

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
            self.classifier_neural_net.train_set(dData, compare=bshow_comparison)

        #	STEP 15: Return
        return

    #
    #endregion

    #region --- resets ---
    def __reset_nodes__(self) -> None:
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

    def __reset_password__(self) -> int:
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
    
    #region --- other ---    
    def show_comparison(self, _dData: Data) -> None:
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

            self.__propagate_forward__(dDNR["in"])
            print( MathHelper.round( dDNR["out"], 1) , MathHelper.round( self.get_ann_output(), 1), sep="\t")

        print("\n-----------------------------", "\tClassification\t\t", "-----------------------------\n")
        
        _dData.reset()
        dHold = self.get_accuracy(data=_dData, size=_dData.getLen(), full_set=True)

        print("Dataset Size: ", 	str( _dData.getLen() ))
        print("Correct Classifications: " + str(dHold["accurate samples"]))

        #	STEP 3: Return
        return

    #
    #endregion

#region	Testing - Training
if (__name__ == "__main__"):
    dat = Data()
    dat.importData(file="4x - Iris/iris_0.json")

    x = ""

    while (True):
        print("")
        x = input("> Continue? ")
        if (x == "exit" or x == "N" or x == "n"):
            break

        os.system("clear")

        fire = Annie()
        fire.show_output = True
        fire.use_l1_regularization = False
        fire.use_l2_regularization = True
        fire.train_set(cp.deepcopy(dat), advanced_training=True, compare=True)

        print("--------------------------------------------------------------------------------------")


#endregion
