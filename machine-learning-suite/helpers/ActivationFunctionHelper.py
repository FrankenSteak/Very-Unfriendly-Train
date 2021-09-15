#region --- Imports ---
import  math                        as mt
import  numpy                       as np
import  os
import  sys

sys.path.append(os.path.abspath("."))

from config.Config import Conny
#endregion

class ActivationFunctionHelper:    
    #region --- Init ---
    """
        - Description::

            Contains various activation functions along witht their derivatives.
    """

    def __init__(self):
        #   --- Setup ---
        self._config = Conny()
        self._config.load("ActivationFunctions.json")
        #   --- Linear ---
        self.linear_c = self._config.data["linear"]["c"]["default"]
        self.linear_m = self._config.data["linear"]["m"]["default"]
        #   --- Logistic ---
        self.logistic_c = self._config.data["logistic"]["c"]["default"]
        self.logistic_k = self._config.data["logistic"]["k"]["default"]
        self.logistic_max = self._config.data["logistic"]["max"]["default"]
        #   --- tanh ---
        self.tanh_c = self._config.data["tanh"]["c"]["default"]
        self.tanh_k = self._config.data["tanh"]["k"]["default"]
        self.tanh_m = self._config.data["tanh"]["m"]["default"]
        #   --- relU ---
        self.relu_boundary = self._config.data["relu"]["boundary"]["default"]
        self.relu_lower_c = self._config.data["relu"]["lower_c"]["default"]
        self.relu_lower_m = self._config.data["relu"]["lower_m"]["default"]
        self.relu_upper_c = self._config.data["relu"]["upper_c"]["default"]
        self.relu_upper_m = self._config.data["relu"]["upper_m"]["default"]
        #   --- elU ---
        self.elu_boundary = self._config.data["elu"]["boundary"]["default"]
        self.elu_linear_c = self._config.data["elu"]["linear_c"]["default"]
        self.elu_linear_m = self._config.data["elu"]["linear_m"]["default"]
        self.elu_exponential_c = self._config.data["elu"]["exponential_c"]["default"]
        self.elu_exponential_k = self._config.data["elu"]["exponential_k"]["default"]
        self.elu_exponential_m = self._config.data["elu"]["exponential_m"]["default"]
        #   --- srelU ---
        self.srelu_lower_boundary = self._config.data["srelu"]["lower_boundary"]["default"]
        self.srelu_upper_boundary = self._config.data["srelu"]["upper_boundary"]["default"]
        self.srelu_lower_c = self._config.data["srelu"]["lower_c"]["default"]
        self.srelu_lower_m = self._config.data["srelu"]["lower_m"]["default"]
        self.srelu_central_c = self._config.data["srelu"]["central_c"]["default"]
        self.srelu_central_m = self._config.data["srelu"]["central_m"]["default"]
        self.srelu_upper_c = self._config.data["srelu"]["upper_c"]["default"]
        self.srelu_upper_m = self._config.data["srelu"]["upper_m"]["default"]
        #   --- Response ---
        return

    #
    #endregion

    #region --- FE: Activation Functions ---
    def activation_function(self, activation_function: int, x: float) -> float:
        """
            ToDo
        """
        
        if (activation_function == 0):
            return self.linear(x)
        elif (activation_function == 1):
            return self.logistic(x)
        elif (activation_function == 2):
            return self.tanh(x)
        elif (activation_function == 3):
            return self.relu(x)
        elif (activation_function == 5):
            return self.elu(x)
        elif (activation_function == 6):
            return self.srelu(x)
        else:
            raise Exception("An error occured in ActivationFunctionHelper.activation_function(): Invalid activation function passed")

    def activation_function_derivative(self, activation_function: int, x: float) -> float:
        """
            ToDo
        """
        
        if (activation_function == 0):
            return self.linear_derivative()
        elif (activation_function == 1):
            return self.logistic_derivative(x)
        elif (activation_function == 2):
            return self.tanh_derivative(x)
        elif (activation_function == 3):
            return self.relu_derivative(x)
        elif (activation_function == 5):
            return self.elu_derivative(x)
        elif (activation_function == 6):
            return self.srelu_derivative(x)
        else:
            raise Exception("An error occured in ActivationFunctionHelper.activation_function_derivative(): Invalid activation function passed")
    
    #
    #endregion

    #region --- FE: Linear ---
    def linear(self, x: float) -> float:
        return self.linear_m * x + self.linear_c

    def linear_derivative(self) -> float:
        return self.linear_m

    #
    #endregion

    #region --- FE: Logistic ---
    def logistic(self, x: float) -> float:
        return 1.0 / (1.0 + mt.exp(-1.0 * self.logistic_c * x))

    def logistic_derivative(self, x: float) -> float:
        fOut = self.logistic(x)
        return fOut * (1.0 - fOut)

    #
    #endregion

    #region --- FE: tanh ---
    def tanh(self, x: float) -> float:
        return self.tanh_k * np.tanh(self.tanh_m * x + self.tanh_c)

    def tanh_derivative(self, x: float) -> float:
        fOut = self.tanh(x)
        return self.tanh_m * self.tanh_k * (1.0 - fOut * fOut)
    
    #
    #endregion

    #region --- FE: relu ---
    def relu(self, x: float) -> float:
        if (x > self.relu_boundary): return (self.relu_upper_m * x + self.relu_upper_c)
        return (self.relu_lower_m * x + self.relu_lower_c)

    def relu_derivative(self, x: float) -> float:
        if (x > self.relu_boundary): return self.relu_upper_m
        return self.relu_lower_m
    
    #
    #endregion

    #region --- FE: elu ---
    def elu(self, x: float) -> float:
        if (x > self.elu_boundary): return (self.elu_linear_m * x + self.elu_linear_c)
        return (self.elu_exponential_k * (mt.exp(self.elu_exponential_m * x + self.elu_exponential_c) - 1))

    def elu_derivative(self, x: float) -> float:
        if (x > self.elu_boundary): return self.elu_linear_c
        return (self.elu_exponential_m * self.elu(x))
    
    #
    #endregion

    #region --- FE: srelu ---
    def srelu(self, x: float) -> float:
        if (x <= self.srelu_lower_boundary): return (self.srelu_lower_m * x + self.srelu_lower_c)
        elif (x >= self.srelu_upper_boundary): return (self.srelu_upper_m * x + self.srelu_upper_c)
        return (self.srelu_center_c * x)

    def srelu_derivative(self, x: float) -> float:
        if (x <= self.srelu_lower_boundary):
            #   STEP 3: If under lower boundary
            return self.srelu_lower_c

        elif (x >= self.srelu_upper_boundary):
            #   STEP 4: If above upper boundary
            return self.srelu_upper_c

        else:
            #   STEP 5: If center
            return self.srelu_center_c

    # 
    #endregion
