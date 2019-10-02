#region Imports

from    enum                            import Enum

import  copy                            as cp
import  numpy                           as np
import  os
import  random                          as rn
import  sys
import  time                            as tm

sys.path.append(os.path.abspath("."))

from    Code.Enums.Enums                import Enums            as en
from    Code.Enums.Swarms               import Swarms           as sw

from    Code.Optimizers.Particle        import UwU
from    Code.Optimizers.Swarm           import SwarmChan

from    Helpers.Config                  import Conny
from    Helpers.GeneralHelpers          import Helga

#endregion

#region Class - Sarah

class Sarah:

    #region Init

    """
    """

    def __init__(self):

        #region STEP 0: Local variables

        self.__enum                 = en.Sarah
        self.__config               = Conny()
        self.__config.load(self.__enum.value)
        
        #endregion

        #region STEP 1: Private variables

        self.__bAllowTesting        = self.__config.data["parameters"]["allow testing"]["default"]

        #endregion

        #region STEP 2: Public variables

        self.bShowOutput            = self.__config.data["parameters"]["show output"]["default"]

        #endregion

        #region STEP 3: Setup - Private variables

        #endregion

        #region STEP 4: Setup - Public variables

        #endregion
        
        return
        
    #
    #endregion

    #region Front-End

    #   region Front-End: Mapping

    def mapSurrogate(self, **kwargs) -> dict:
        """
        """
        
        #   STEP 0: Local variables
        #   STEP 1: Setup - Local variables
        #   STEP 2: ??
        #   STEP ??: Return
        print("zap")
        return {"result": None, "fitness": rn.random()}
        
    #
    #   endregion

    #   region Front-End: Training

    def trainSurrogate(self, **kwargs) -> dict:
        """
            Description:

                Trains the passed surrogate using the specified optimizer.

            |\n
            |\n
            |\n
            |\n
            |\n

            Args:

                + surrogate   = ( vars ) The surrogate instance to be trained
                    ~ Required
                + data        = ( vars ) Data container
                    ~ Required
                + password    = ( int ) The surrogate password
                    ~ Required
                + optimizer   = ( enum ) The optimizer to user during training
                    ~ Required

            |\n

            Returns:

                + dictionary    = ( dict )
                    ~ iterations    = ( int ) Number of training iterations
                    ~ surrogate     = ( vars ) The trained surrogate
                    ~ scalar        = ( float ) The surrogate scalar
        """

        #   STEP 0: Local variables
        #   STEP 1: Setup - Local variables

        #   STEP 2: Check if surrogate passed
        if ("surrogate" not in kwargs):
            #   STEP 3: Error handling
            raise Exception("An error occured in Sarah.trainSurrogate() -> Step 2: No surrogate passed")

        #   STEP 4: Check if data container passed
        if ("data" not in kwargs):
            #   STEP 5: Error handling
            raise Exception("An error occured in Sarah.trainSurrogate() -> Step 4: No data container passed")

        #   STEP 6: Check if surrogate password passed
        if ("password" not in kwargs):
            #   STEP 7: Error handling
            raise Exception("An error occured in Sarah.trainSurrogate() -> Step 6: No surrogate password passed")

        #   STEP 8: Check if optimizer passed
        if ("optimizer" not in kwargs):
            #   STEP 9: Error handling
            raise Exception("An error occured in Sarah.trainSurrogate() -> Step 8: No optimizer passed")


        #   STEP 10: Check if pso
        if (kwargs["optimizer"] == sw.PSO):
            #   STEP 11: User Output
            if (self.bShowOutput):
                print("Sarah (train-srg) -> (train-srg-pso) {" + Helga.time() + "}")

            #   STEP 12: Outsource pso optimization and return
            return self.__surrogatePso__(surrogate=kwargs["surrogate"], data=kwargs["data"], password=kwargs["password"])
            
        else:
            #   STEP ??: Error handling
            raise Exception("An error occured in Sarah.trainSurrogate(): Unimplemented optimizer passed")
            
        #   STEP ??: Return
        return None
        
    #
    #   endregion

    #
    #endregion

    #region Back-End

    #   region Back-End: Gets

    def __getCandidates__(self, **kwargs) -> list:
        """
            Description:

                Returns a list of candidates for the specified algorithm.

            |\n
            |\n
            |\n
            |\n
            |\n

            Args:

                + optimizer     = ( enum ) The optimizer
                    ~ Required
                + params        = ( dict ) The optimizer's parameters
                    ~ Required
                + initial       = ( list ) The initial candidate
                    ~ Required

            |\n

            Returns:

                + list          = ( list ) A list of new candidates

        """

        #   STEP 0: Local variables
        lCandidates             = []
        lShape                  = None

        #   STEP 1: Setup - Local variables
        lShape                  = Helga.getShape(kwargs["initial"])

        #   region STEP 2->??: PSO Candidate generation

        #   STEP 2: Check if PSO
        if (kwargs["optimizer"] == sw.PSO):
            #   STEP 3: Append the initial candidate to the candidate list
            lCandidates.append(kwargs["initial"])

            #   STEP 4: Iterate through remaining required candidates
            for _ in range(1, kwargs["params"]["candidates"]):
                #   STEP 5: Get new empty candidate
                lTmp = cp.deepcopy(lShape)

                #   STEP 6: Iterate through candidate list
                for i in range(0, len(lTmp)):
                    #   STEP 7: Check if single data point
                    if (type(lTmp[i]) == float):
                        #   STEP 8: Set value
                        lTmp[i] = rn.random() * 2.0 * kwargs["params"]["scalar"] - kwargs["params"]["scalar"]

                    else:
                        #   STEP 9: Iterate through list
                        for j in range(0, len(lTmp[i])):
                            #   STEP 10: Set value
                            lTmp[i][j] = rn.random() * 2.0 * kwargs["params"]["scalar"] - kwargs["params"]["scalar"]

                #   STEP 11: Append the candidate to the output list
                lCandidates.append(lTmp)

            #   STEP 12: Return
            return lCandidates

        #   STEP ??: Error handling
        raise Exception("An error occured in Sarah.__getCandidates__(): Unimplemented optimizer passed")

    def __getShape__(self, **kwargs) -> list:
        """
        """

        #   STEP 0: Local variables


    #
    #   endregion

    def __getFitness__(self, **kwargs) -> list:
        """
            Description:

                Returns the fitness of the candidates as a list.
            
            |\n
            |\n
            |\n
            |\n
            |\n

            Args:

                + type              = ( str ) The calling function
                    ~ Required
                + candidates        = ( list ) List of potential candidates
                    ~ Required

                - Surrogate:
                    + surrogate     = ( vars ) The surrogate instance
                        ~ Required
                    + data          = ( vars ) Data container
                        ~ Required
                    + password      = ( int/float ) Class password
                        ~ Required

            |\n

            Returns:

                + list          = ( list )
                    ~ List of floats containing fitness for each candidate
                    
        """

        #   STEP 0: Local variables
        lOut                    = []

        #   STEP 1: Setup - Local variables

        #   STEP 2: Check if type passed
        if ("type" not in kwargs):
            #   STEP 3: Error handling
            raise Exception("An error occured in Sarah.__geFitness__() -> Step 2: No type passed")

        #   STEP 4: Check if candidates passed
        if ("candidates" not in kwargs):
            #   STEP 5: Error handling
            raise Exception("An error occured in Sarah.__getFitness__() -> Step 4: No candidate list passed")

        #   STEP 6: Check type
        if (kwargs["type"] == "surrogate"):
            #   STEP 7: Check if surrogate passed
            if ("surrogate" not in kwargs):
                #   STEP 8: Error handling
                raise Exception("An error occured in Saragh.__getFitness__() -> Step 7: No surrogate passed")

            #   STEP 9: Check data container passed
            if ("data" not in kwargs):
                #   STEP 10: Error handling
                raise Exception("An error occured in Sarah.__getFitness__() -> Step 9: No data container passed")

            #   STEP 11: Check if class password passed
            if ("password" not in kwargs):
                #   STEP 12: Error handling
                raise Exception("An error occured in Sarah.__getFitness__() -> Step 11: NO class password passed")

            #   STEP 13: Get temp variables
            surrogate = kwargs["surrogate"]
            data = kwargs["data"]
            candidates = kwargs["candidates"]
            password = kwargs["password"]

            #   STEP 14: Iterate through candidates
            for i in range(0, len(candidates)):
                #   STEP 15: Set the surrogate weights
                surrogate.setWeights(weights=candidates[i], password=password)
                
                #   STEP 16: Append fitness to output list
                lOut.append(surrogate.getAFitness(data=data))

            #   STEP 17: Return
            return lOut

    def __getParams__(self, **kwargs) -> dict:
        """
            Desciption:

                Returns the specified optimization algorithm's required
                parameters.

            |\n
            |\n
            |\n
            |\n
            |\n

            Args:

                + optimizer     = ( enum ) The optimizatoin algorithm
                    ~ Required

            |\n

            Returns:

                + dict          = ( dict ) The algorithm's parameters
        """

        #   STEP 0: Local variables
        dTmp                    = self.__config.data["parameters"]["algorithms"]

        #   STEP 1: Setup - Local variables

        #   STEP 2: Check if PSO
        if (kwargs["optimizer"] == sw.PSO):
            #   STEP 3: Adjust holder dictionary
            dTmp = dTmp["pso"]

            #   STEP 4: Populate output dictionary
            dOut = {
                "iterations":       dTmp["iterations"]["algorithm"]["default"],
                "iterations-def":   dTmp["iterations"]["back propagation"]["default"],
                "candidates":       dTmp["candidates"]["default"],
                "scalar":           dTmp["candidate scalar"]["default"],
                "check point":      dTmp["acc check point"]["default"],
                "requirement":      dTmp["acc requirement"]["default"],
                "phi1":             dTmp["parameters"]["phi 1"]["default"],
                "phi2":             dTmp["parameters"]["phi 2"]["default"],
                "eta":              dTmp["parameters"]["eta"]["default"]
            }

            #   STEP 5: Return
            return dOut

        #   STEP 6: Error handling
        raise Exception("An erro occured in Sarah.__getParams__() -> Step 6: Unimplemented algorithm passed")

    #
    #   endregion

    #   region Back-End: Training

    def __surrogatePso__(self, **kwargs) -> dict:
        """
            Description:

                Trains the passed surrogate using Particle-Swarm Optimization.

            |\n
            |\n
            |\n
            |\n
            |\n

            Args:
            
                + surrogate     = ( vars ) The surrogate instance to be trained
                    ~ Required
                + data          = ( vars ) Data container
                    ~ Required
                + password      = ( int/float ) The surrogate password
                    ~ Required
            
            |\n

            Returns:

                + dictionary        = ( dict ) A dict instance containing
                    ~ surrogate     = ( vars ) The trained surrogate
                    ~ iterations    = ( int ) The training iterations
                    ~ scalar        = ( float ) The surrogate intstance's scalar

        """

        #   region STEP 0: Local variables

        surrogate               = None
        password                = None

        dPsoParams              = None

        swarm                   = None

        dTrainingData           = None
        dTestingData            = None

        lCandidates             = []
        lFitness                = []

        iCount                  = 0

        #   endregion

        #   region STEP 1: Setup - Local variables

        #                       STEP 1.1: Init algorithm parameters
        dPsoParams              = self.__getParams__(optimizer=sw.PSO)

        #                       STEP 1.2: Init datasets
        dTestingData            = kwargs["data"].splitData()

        dTrainingData           = dTestingData["training"]
        dTestingData            = dTestingData["testing"]

        #               region  STEP 1.3: Setup surrogate
        
        #       STEP 1.3.1: Set surrogate and password variables
        surrogate               = kwargs["surrogate"]
        password                = kwargs["password"]

        #       STEP 1.3.2: Init surrogate activation functions
        surrogate.setAcFunction(password=password, algorithm="pso", scalar=dPsoParams["scalar"])

        #       STEP 1.3.3: Init candidate list
        lCandidates             = self.__getCandidates__(optimizer=sw.PSO, params=dPsoParams, initial=surrogate.getWeights(password=password))

        #       STEP 1.3.4: Init fitness list
        lFitness                = self.__getFitness__(type="surrogate", candidates=lCandidates, surrogate=surrogate, data=dTestingData, password=password) 

        #       endregion

        #                       STEP 1.4: Init swarm
        swarm                   = SwarmChan(dPsoParams["candidates"])

        swarm.initPsoPositions(lCandidates)
        swarm.initPsoFitness(lFitness)
        swarm.initPsoParams(dPsoParams["phi1"], dPsoParams["phi2"], dPsoParams["eta"])

        #   endregion

        #   STEP 2: User Output
        if (self.bShowOutput):
            print("Sarah (train-srg-pso) {" + Helga.time() + "} - Starting Particle-Swarm Optimization\n")

        #   STEP 3: Perform number of iterations
        for i in range(0, dPsoParams["iterations"] + 1):
            #   STEP 4: Reset variables
            lFitness    = []
            lCandidates = []

            #   region STEP 5->14: Training process

            #   STEP 5: Perform swarming
            swarm.pso()

            #   STEP 6: Iterate through all particles
            for j in range(0, dPsoParams["candidates"]):
                #   STEP 7: Append particle to list
                lCandidates.append(swarm.lParticles[j].lCurrPosition)

            #   STEP 8: Get updated fitness values
            lFitness = self.__getFitness__(type="surrogate", candidates=lCandidates, surrogate=surrogate, data=dTestingData, password=password)

            #   STEP 9: Set new particle fitness
            swarm.setParticleFitness(lFitness)

            #   STEP 10: Set surrogate weights to best candidate
            surrogate.setWeights(weights=swarm.lBestSolution, password=password)

            #   STEP 11: Perform default training
            for j in range(0, dPsoParams["iterations-def"]):
                #   STEP 12: Get random data sample
                dDNR = dTrainingData.getRandDNR()

                #   STEP 13: Perform propagation
                surrogate.propagateForward(data=dDNR["in"], password=password)
                surrogate.propagateBackward(data=dDNR["out"], password=password)

            #   STEP 14: Update best candidate
            swarm.lBestSolution = surrogate.getWeights(password=password)

            #
            #   endregion

            #   STEP 15: Check if accuracy check needs to be performed
            if (iCount == dPsoParams["check point"]):
                #   STEP 16: Reset counter
                iCount = 0

                #   STEP 17: Get accuracy as percentage
                dHold = surrogate.getAccuracy(data=kwargs["data"], size=kwargs["data"].getLen())
                iAcc = dHold["accurate samples"]
                fAcc = dHold["percent accuracy"]

                #   STEP 18: Check if accuracy requirement met
                if (fAcc >= dPsoParams["requirement"]):
                    #   STEP 19: User Output
                    if (self.bShowOutput):
                        print("Sarah (train-srg-pso) {" + Helga.time() + "} - Particle-Swarm Optimization succcessful")
                        print("\tTotal iterations: " + str(i))
                        print("\tAccurate Samples: " + str(iAcc))
                        print("\tPercent Accuracy: " + str(round(fAcc * 100.0, 2)) + "%\n")

                    #   STEP 20: Populate output dictionary
                    dOut = {
                        "accuracy":     iAcc,
                        "algorithm":    "pso",
                        "iterations":   i,
                        "scalar":       dPsoParams["scalar"],
                        "surrogate":    surrogate
                    }

                    #   STEP !!: Check that iAcc > 0
                    if (iAcc <= 0):
                        dOut["inverse accuracy"] = np.inf

                    else:
                        dOut["inverse accuracy"] = float(dHold["iterations"] / iAcc)

                    #   STEP 21: Return
                    return dOut

            #   STEP 22: Increment counter
            iCount += 1

        #   STEP 24: Get accuracy as percentage
        dHold = surrogate.getAccuracy(data=kwargs["data"], size=kwargs["data"].getLen())
        iAcc = dHold["accurate samples"]
        fAcc = dHold["percent accuracy"]

        #   STEP 23: User Output
        if (self.bShowOutput):

            #   STEP 25: Print output
            print("\tSarah (train-srg-pso) {" + Helga.time() + "} - Particle-Swarm Optimization Unsuccessful")
            print("\t\tTotal iterations: " + str(i))
            print("\t\tAccurate Samples: " + str(iAcc))
            print("\t\tPercent Accuracy: " + str(round(fAcc * 100.0, 2)) + "%\n")
            
        #   STEP 26: Populate output dictionary
        dOut = {
            "accuracy":     iAcc,
            "algorithm":    "pso",
            "iterations":   -i,
            "scalar":       dPsoParams["scalar"],
            "surrogate":    surrogate
        }
        

        #   STEP 27: Check that iAcc > 0
        if (iAcc <= 0):
            dOut["inverse accuracy"] = np.inf

        else:
            dOut["inverse accuracy"] = float(dHold["iterations"] / iAcc)

        #   STEP 28: Return
        return dOut

    #
    #   endregion

    #
    #endregion

#
#endregion

#region Testing

#
#endregion