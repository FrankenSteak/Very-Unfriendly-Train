#region Imports
import  math                        as mt
import  numpy                       as np
import  os
import  sys

sys.path.append(os.path.abspath("."))

from static.Enums import Enums as en
from config.Config import Conny
#endregion

#region Class - Antonio

class Antonio:
    
    #region Init

    """
        Description:

            Contains various activation functions along witht their derivatives.
    """

    def __init__(self):

        #region STEP 0: Local variables

        self.__enum                 = en.Antonio
        self.__cf                   = Conny()
        self.__cf.load(self.__enum.value)

        #endregion

        #region STEP 1: Private variables

        #   region Linear
        
        self.__fC_linear            = self.__cf.data["parameters"]["linear"]["c"]["default"]

        #   endregion

        #   region Logistic
        
        self.__fC_logisitic         = self.__cf.data["parameters"]["logistic"]["c"]["default"]

        #   endregion

        #   region TanH

        self.__fC_tanh              = self.__cf.data["parameters"]["tanh"]["c"]["default"]
        self.__fM_tanh              = self.__cf.data["parameters"]["tanh"]["magnitude"]["default"]

        #   endregion

        #   region Relu
        
        self.__fC_relu              = self.__cf.data["parameters"]["relu"]["c"]["default"]

        #   endregion

        #   region Leaky-Relu
        
        self.__fC_lRelu_Pos         = self.__cf.data["parameters"]["leaky relu"]["c"]["positive"]["default"]
        self.__fC_lRelu_Neg         = self.__cf.data["parameters"]["leaky relu"]["c"]["negative"]["default"]

        #   endregion

        #   region Elu
        
        self.__fC_elu_lin           = self.__cf.data["parameters"]["elu"]["c"]["linear"]["default"]
        self.__fC_elu_exp           = self.__cf.data["parameters"]["elu"]["c"]["exponential"]["default"]

        #   endregion

        #   region Srelu
        
        self.__fC_srelu_lower       = self.__cf.data["parameters"]["srelu"]["c"]["lower"]["default"]
        self.__fC_srelu_center      = self.__cf.data["parameters"]["srelu"]["c"]["center"]["default"]
        self.__fC_srelu_upper       = self.__cf.data["parameters"]["srelu"]["c"]["upper"]["default"]

        self.__fBoundary_srelu_lower    = self.__cf.data["parameters"]["srelu"]["boundary"]["lower"]["default"]
        self.__fBoundary_srelu_upper    = self.__cf.data["parameters"]["srelu"]["boundary"]["upper"]["default"]

        #   endregion

        #   region Gaussian
        
        self.__fC_gaussian          = self.__cf.data["parameters"]["gaussian"]["c"]["default"]

        #   endregion

        #endregion

        #   STEP 2: Return
        return

    #
    #endregion

    #region Front-End

    #   region Front-End: Gets

    def getActivation(self, _iIn: int, _fIn: float) -> float:
        """
        """

        #   STEP 0: Local variables
        #   STEP 1: Setup - Local variables

        #   STEP 2: Check activation functions - Essentially a switch case
        if (_iIn == 0):
            return self.linear(_fIn)
        elif (_iIn == 1):
            return self.logistic(_fIn)
        elif (_iIn == 2):
            return self.tanH(_fIn)
        elif (_iIn == 3):
            return self.relu(_fIn)
        elif (_iIn == 4):
            return self.leakyRelu(_fIn)
        elif (_iIn == 5):
            return self.elu(_fIn)
        elif (_iIn == 6):
            return self.srelu(_fIn)
        else:
            #   STEP 3: Error handling
            raise Exception("An error occured in Antonio.getActivation() - > Step 2: Invalid activation function passed")

    def getActivationD(self, _iIn: int, _fIn: float) -> float:
        """
        """

        #   STEP 0: Local variables
        #   STEP 1: Setup - Local variables

        #   STEP 2: Check activation functions
        if (_iIn == 0):
            return self.linearD()
        elif (_iIn == 1):
            return self.logisticD(_fIn)
        elif (_iIn == 2):
            return self.tanHD(_fIn)
        elif (_iIn == 3):
            return self.reluD(_fIn)
        elif (_iIn == 4):
            return self.leakyReluD(_fIn)
        elif (_iIn == 5):
            return self.eluD(_fIn)
        elif (_iIn == 6):
            return self.sreluD(_fIn)
        else:
            #   STEP 3: Error handling
            raise Exception("An error occured in Antonio.getActivationD() -> Step 2: Invalid activation function passed")
    
    #
    #   endregion
    
    #   region Front-End: Sets

    def setFunction(self, **kwargs) -> None:
        """
        """

        #   STEP 0: Local variables
        #   STEP 1: Setup - Local variables

        #   STEP 2: Be safe
        try:
            #   STEP 3: Check if function = linear
            if (kwargs["function"] == 0):
                #   STEP 4: Outsource
                self.__setLinear(kwargs)

            #   STEP 5: Check if function = logistic
            elif (kwargs["function"] == 1):
                #   STEP 6: Outsource
                self.__setLogistic(kwargs)

            #   STEP 7: Check if function = tanh
            elif (kwargs["function"] == 2):
                #   STEP 8: Outsource
                self.__setTanh(kwargs)

            #   STEP 9: Check if srelu
            elif (kwargs["function"] == 6):
                #   STEP 10: Outsource
                self.__setSrelu__(kwargs)

            #   STEP 11: Function not implemented
            else:
                #   STEP 12: Error handling
                raise Exception("An error occured in Antonio.setFunction() -> Step 9: That activation function isn't fully implemented yet")

        except Exception as ex:
            #   STEP 13: Error handling
            print("Initial Error: ", ex)
            raise Exception("An error occured in Antonio.setFunction()")
            
        #   STEP 14: Return
        return
    
    #
    #   endregion

    #   region Front-End: Linear

    def linear(self, _fIn: float) -> float:
        """
        """

        #   STEP 0: Local variables
        #   STEP 1: Setup - Local variables

        #   STEP 2: Return
        return _fIn * self.__fC_linear

    def linearD(self) -> float:
        """
        """

        #   STEP 0: Local variables
        #   STEP 1: Setup - Local variables

        #   STEP 2: Return
        return self.__fC_linear

    #
    #   endregion

    #   region Front-End: Logistic

    def logistic(self, _fIn: float) -> float:
        """
        """

        #   STEP 0: Local variables
        #   STEP 1: Setup - Local variables
        fOut = 1.0 / (1.0 + mt.exp(-1.0 * self.__fC_logisitic * _fIn))
        
        #   STEP 2: Return
        return fOut

    def logisticD(self, _fIn: float) -> float:
        """
        """

        #   STEP 0: Local variables
        fOut = 0.0

        #   STEP 1: Setup - Local variables
        fOut = self.logistic(_fIn)

        #   STEP 2: Compute derivative
        fOut = fOut * (1.0 - fOut)
        fOut = self.__fC_logisitic * fOut

        #   STEP 3: Return
        return fOut

    #
    #   endregion

    #   region Front-End: TanH

    def tanH(self, _fIn: float) -> float:
        """
        """

        #   STEP 0: Local variables
        #   STEP 1: Setup - Local variables

        #   STEP 2: Return
        return (self.__fM_tanh * np.tanh(self.__fC_tanh * _fIn))

    def tanHD(self, _fIn: float) -> float:
        """
        """

        #   STEP 0: Local variables
        fOut = 0.0

        #   STEP 1: Setup - Local variables
        fOut = self.tanH(_fIn)
        
        #   STEP 2: Compute derivative
        fOut = self.__fM_tanh * self.__fC_tanh * (1.0 - fOut * fOut)
        
        #   STEP 3: Return
        return fOut
    
    #
    #   endregion

    #   region Front-End: Relu

    def relu(self, _fIn: float) -> float:
        """
        """

        #   STEP 0: Local variables
        #   STEP 1: Setup - Local variables

        #   STEP 2: Check relu condition
        if (_fIn > 0):
            #   STEP 3: Return
            return (self.__fC_relu * _fIn)
        
        else:
            #   STEP 4: Return of the Return
            return 0.0

    def reluD(self, _fIn: float) -> float:
        """
        """

        #   STEP 0: Local variables
        #   STEP 1: Setup - Local variables

        #   STEP 2: Check relu condition
        if (_fIn > 0):
            #   STEP 3: Return
            return self.__fC_relu

        else:
            #   STEP 4: Return of the Return
            return 0.0
    
    #
    #   endregion
    
    #   region Front-End: Leaky-Relu
    
    def leakyRelu(self, _fIn: float) -> float:
        """
        """

        #   STEP 0: Local variables
        #   STEP 1: Setup - Local variables

        #   STEP 2: Check Leaky Relu condition
        if (_fIn > 0):
            #   STEP 3: Return
            return self.__fC_lRelu_Pos * _fIn
        
        else:
            #   STEP 4: Return of the Return
            return self.__fC_lRelu_Neg * _fIn

    def leakyReluD(self, _fIn: float) -> float:
        """
        """

        #   STEP 0: Local variables
        #   STEP 1: Setup - Local variables

        #   STEP 2: Check Leaky Relu condition
        if (_fIn > 0):
            #   STEP 3: Return
            return self.__fC_lRelu_Pos

        else:
            #   STEP 4: Return of the Return
            return self.__fC_lRelu_Neg

    #
    #   endregion

    #   region Front-End: Elu

    def elu(self, _fIn: float) -> float:
        """
        """

        #   STEP 0: Local variables
        #   STEP 1: Setup - Local variables

        #   STEP 2: Check elu condition
        if (_fIn > 0):
            #   STEP 3: Return
            return self.__fC_elu_lin * _fIn

        else:
            #   STEP 4: Return of the Return
            return (self.__fC_elu_exp * (mt.exp(_fIn) - 1))

    def eluD(self, _fIn: float) -> float:
        """
        """

        #   STEP 0: Local variables
        #   STEP 1: Setup - Local variables

        #   STEP 2: Check elu condition
        if (_fIn > 0):
            #   STEP 3: Return
            return self.__fC_elu_lin

        else:
            #   STEP 4: Return of the Return
            return (self.elu(_fIn) - self.__fC_elu_exp)
    
    #
    #   endregion

    #   region Front-End: Srelu

    def srelu(self, _fIn: float) -> float:
        """
        """

        #   STEP 0: Local variables
        fOut = 0.0

        #   STEP 1: Setup - Local variables

        #   STEP 2: Check srelu condition
        if (_fIn <= self.__fBoundary_srelu_lower):
            #   STEP 3: If under lower boundary
            fOut = self.__fBoundary_srelu_lower
            fOut = fOut + self.__fC_srelu_lower * (_fIn - fOut)

        elif (_fIn >= self.__fBoundary_srelu_upper):
            #   STEP 4: If above upper boundary
            fOut = self.__fBoundary_srelu_upper
            fOut = fOut + self.__fC_srelu_upper * (_fIn - fOut)

        else:
            #   STEP 5: If center
            fOut = self.__fC_srelu_center * _fIn

        #   STEP 6: Return
        return fOut

    def sreluD(self, _fIn: float) -> float:
        """
        """

        #   STEP 0: Local variables
        #   STEP 1: Setup - Local variables

        #   STEP 2: Check srelu condition
        if (_fIn <= self.__fBoundary_srelu_lower):
            #   STEP 3: If under lower boundary
            return self.__fC_srelu_lower

        elif (_fIn >= self.__fBoundary_srelu_upper):
            #   STEP 4: If above upper boundary
            return self.__fC_srelu_upper

        else:
            #   STEP 5: If center
            return self.__fC_srelu_center

    # 
    #   endregion

    #
    #endregion

    #region Back-End

    def __setLinear(self, _dData: dict) -> None:
        """
        """

        #   STEP 0: Local variables
        #   STEP 1: Setup - Local variables

        #   STEP 2: Check if c is specified
        if ("c" in _dData):
            #   STEP 3: Set c
            self.__fC_linear = _dData["c"]

        #   STEP 4: Return
        return

    def __setLogistic(self, _dData: dict) -> None:
        """
        """

        #   STEP 0: Local variables
        #   STEP 1: Setup - Local variables

        #   STEP 2: check if c is specified
        if ("c" in _dData):
            #   STEP 3: Set c
            self.__fC_logisitic = _dData["c"]

        #   STEP 4: Return
        return

    def __setTanh(self, _dData: dict) -> None:
        """
        """

        #   STEP 0: Local variables
        #   STEP 1: Setup - Local variables

        #   STEP 2: Check if c is specified
        if ("c" in _dData):
            #   STEP 3: Set c
            self.__fC_tanh = _dData["c"]

        #   STEP 4: Check if m is specified
        if ("m" in _dData):
            #   STEP 5: Set m
            self.__fM_tanh = _dData["m"]

        #   STEP 6: Return
        return

    def __setSrelu__(self, kwargs: dict) -> None:
        """
            Description:

                Sets the variables for the srelu activation function.

            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:

                + c = ( dict ) A dictionary containing the gradient functions
                    for the lower, center, and upper regions of the srelu
                    activation function
                    ~ Required

                    ~ "lower":  ( float )
                    ~ "center": ( float )
                    ~ "upper":  ( float )

                + boundary  = ( dict ) A dictionary containing the boundaries
                    for the srelu activation function
                    ~ Required

                    ~ "lower":  ( float )
                    ~ "upper":  ( float )


        """

        #   STEP 0: Local variables
        #   STEP 1: Setup - Local variables
        
        #   region STEP 2->??: Error checking

        #   STEP 2: CHeck if c arg passed
        if ("c" not in kwargs):
            #   STEP 3: Error handling
            raise Exception("An error occured in Antonio.__setSrelu__() -> Step 2: No c arg passed")

        #   STEP 4: Check if boundary arg passed
        if ("boundary" not in kwargs):
            #   STEP 5: Error handling
            raise Exception("An error occured in Antonio.__setSrelu__() -> Step 4: No boundary arg passed")

        #
        #   endregion

        #   STEP 6: Update - Class variables
        self.__fC_srelu_lower           = kwargs["c"]["lower"]
        self.__fC_srelu_center          = kwargs["c"]["center"]
        self.__fC_srelu_upper           = kwargs["c"]["upper"]

        self.__fBoundary_srelu_lower    = kwargs["boundary"]["lower"]
        self.__fBoundary_srelu_upper    = kwargs["boundary"]["upper"]

        #   STEP 7: Return
        return

    #
    #   endregion

#
#endregion

#region Testing

if (__name__ == "__main__"):
    av = Antonio()

    print(av.tanH(0.0))
    print(av.tanHD(0.0))
#
#   endregion
