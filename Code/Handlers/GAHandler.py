#region Imports

from    enum                                import Enum

import  copy                                as cp
import  numpy                               as np
import  os
import  random                              as rn
import  sys
import  time                                as tm

sys.path.append(os.path.abspath("."))

from    Code.Enums.Enums                    import Enums                as en
from    Code.Enums.GeneticAlgorithms        import GeneticAlgorithms    as ga

from    Code.Optimizers.Particle            import UwU
from    Code.Optimizers.GeneticAlgorithm    import Garry

from    Helpers.Config                      import Conny
from    Helpers.GeneralHelpers              import Helga

#endregion

#region Class - SpongeBob

class SpongeBob:

    #region Init

    """
    """

    def __init__(self):

        #region STEP 0: Local variables

        self.__enum                 = en.SpongeBob
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
            Description:

                Maps the passed surrogate using the specified optimizer.

            |\n
            |\n
            |\n
            |\n
            |\n
            
            Arguments:

                + surrogate = ( vars ) The surrogate that requires mapping
                    ~ Required

                + data  = ( vars ) A Data container that contains the data
                    for the mapping process
                    ~ Required

                + optimizer = ( enum ) The optimizer to be used during the
                    mapping process
                    ~ Required
        """

        #   STEP 0: Local variables

        #   STEP 1: Setup - Local variables
        
        #   region STEP 2->7: Error checking

        #   STEP 2: Check if surrogate arg passed
        if ("surrogate" not in kwargs):
            #   STEP 3: Error handling
            raise Exception("An error occured in SpongeBob.mapSurrogate() -> Step 2: No surrogate arg passed")

        #   STEP 4: Check if data arg passed
        if ("data" not in kwargs):
            #   STEP 5: Error handling
            raise Exception("An error occured in SpongeBob.mapSurrogate() -> Step 4: No data arg passed")

        #   STEP 6: Check if optimizer arg passed
        if ("optimizer" not in kwargs):
            #   STEP 7: Error handling
            raise Exception("An error occured in SpongeBob.mapSurrogate() -> Step 6: No optimizer arg passed")
        
        #
        #   endregion
        
        #   STEP 8: Check if TRO
        if (kwargs["optimizer"] == ga.TRO):
            #   STEP 10: User output
            if (self.bShowOutput):
                print("SpongeBob (map-srg) -> (map-srg-TRO) {" + Helga.time() + "}")

            #   STEP 11: Outsource to tro and return
            return self.__troMapping__(surrogate=kwargs["surrogate"], data=kwargs["data"])

        #   STEP 12: Unrecognized optimizer - Error handling
        raise Exception("An error occured in SpongeBob.mapSurrogate() -> Step 12: Unrecognized optimizer")
        
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
            raise Exception("An error occured in SpongeBob.trainSurrogate() -> Step 2: No surrogate passed")

        #   STEP 4: Check if data container passed
        if ("data" not in kwargs):
            #   STEP 5: Error handling
            raise Exception("An error occured in SpongeBob.trainSurrogate() -> Step 4: No data container passed")

        #   STEP 6: Check if surrogate password passed
        if ("password" not in kwargs):
            #   STEP 7: Error handling
            raise Exception("An error occured in SpongeBob.trainSurrogate() -> Step 6: No surrogate password passed")

        #   STEP 8: Check if optimizer passed
        if ("optimizer" not in kwargs):
            #   STEP 9: Error handlign
            raise Exception("An error occured in SpongeBob.trainSurrogate() -> Step 8: No optimizer passed")
            
        #   STEP 10: Check if tro
        if (kwargs["optimizer"] == ga.TRO):
            #   STEP 11: User Output
            if (self.bShowOutput):
                print("SpongeBob (train-srg) -> (train-srg-tro) {" + Helga.time() + "}")

            #   STEP 12: Outsource tro optimization and return
            return self.__troTraining__(surrogate=kwargs["surrogate"], data=kwargs["data"], password=kwargs["password"])

        else:
            #   STEP ??: Error handling
            raise Exception("An error occured in SpongeBob.trainSurrogate(): Unimplemented optimizer passed")

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

                + optimizer = ( enum ) The optimzier
                    ~ Required

                + params    = ( dict ) The optimizer's parameters
                    ~ Required

                + initial   = ( list ) The initial candidate

                + region    = ( float ) The algorithm's current region
                    ~ Required if <optimizer="tro">

            |\n

            Returns

                + list      = ( list ) A list of new candidates
        """

        #   STEP 0: Local variables
        lCandidates             = []

        #   STEP 1: Setup - Local variables

        #   STEP 2: Check if optimizer passed
        if ("optimizer" not in kwargs):
            #   STEP 3: Error handling
            raise Exception("An error occured in SpongeBob.__getCandidates__() -> Step 2: No optimizer passed")

        #   STEP 4: Check optimizer parameters passed
        if ("params" not in kwargs):
            #   STEP 5: Error handling
            raise Exception("An error occured in SpongeBob.__getCandidates__() -> Step 4: No optimizer parameters passed")

        #   STEP 6: Check if initial candidate passed
        if ("initial" not in kwargs):
            #   STEP 7: Error handling
            raise Exception("An error occured in SpongeBob.__getCandidates__() -> Step 6: No initial candidate passed")

        #   STEP 8: Check if optimizer is tro
        if (kwargs["optimizer"] == ga.TRO):
            #   STEP 9: Check if region passed
            if ("region" not in kwargs):
                #   STEP 10: Error handling
                raise Exception("An error occured in SpongeBob.__getCandidates__() -> Step 9: No region passed")

            #   STEP 11: Iterate through the required number of candidates
            for _ in range(0, kwargs["params"]["candidates"]):
                #   STEP 12: Get temporary candidate
                lTmp = Helga.getShape(kwargs["initial"])

                #   STEP 13: Iterate through candidate
                for i in range(0, len(lTmp)):
                    #   STEP 14: Check if single point
                    if (type(lTmp[i]) == float):
                        #   STEP 15: Get random value in range [-1, 1]
                        fTmp = (rn.random() * 2.0) - 1.0

                        #   STEP 16: Modify value using region and scalar
                        fTmp = kwargs["params"]["scalar"] * kwargs["region"] * fTmp

                        #   STEP 17: Set new weight
                        lTmp[i] = kwargs["initial"][i] + fTmp

                    else:
                        #   STEP 18: Iterate through list
                        for j in range(0, len(lTmp[i])):
                            #   STEP 19: Get random value in range [1, 1]
                            fTmp = rn.random() * 2.0 - 1.0

                            #   STEP 20: Modify using region and scalar
                            fTmp = kwargs["params"]["scalar"] * kwargs["region"] * fTmp

                            #   STEP 21: Set new candidate value
                            lTmp[i][j] = kwargs["initial"][i][j] + fTmp

                #   STEP 22: Append new candidate to output list
                lCandidates.append(lTmp)

            #   STEP 23: Return
            return lCandidates

        #   STEP ??: Error handling
        raise Exception("An error occured in SpongeBob.__getCandidates__(): Unimplemented optimizer passed")

    def __getFitness__(self, **kwargs) -> list:
        """
            Description:

                Returns the fitness of the candidates as a list

            |\n
            |\n
            |\n
            |\n
            |\n

            Args:

                + type          = ( str ) The calling function
                    ~ Required
                + candidates    = ( list ) List of potential candidates
                    ~ Required

                - Type = Surrogate:
                    + surrogate = ( vars ) The surrogate instance
                        ~ Required
                    + data      = ( vars ) Data container
                        ~ Required
                    + password  = ( int / float ) Class password
                        ~ Required
        """

        #   STEP 0: Local variables
        lOut                    = []
        #   STEP 1: Setup - Local variables

        #   STEP 2: Check that candidates were passed
        if ("candidates" not in kwargs):
            #   STEP 3: Error handling
            raise Exception("An error occured in SpongeBob.__getFitness__() -> Step 2: No candidate list passed")

        #   STEP 4: Check if type specified
        if ("type" not in kwargs):
            #   STEP 5: Error handling
            raise Exception("An error occured in SpongeBob.__getFitness__() -> Step 4: No type specified")
        
        #   STEP 6: If surrogate
        if (kwargs["type"] == "surrogate"):
            #   STEP 7: Check if surrogate passed
            if ("surrogate" not in kwargs):
                #   STEP 8: Error handling
                raise Exception("An error occured in SpongeBob.__getFitness__() -> Step 7: No surrogate passed")

            #   STEP 9: Check if data container passed
            if ("data" not in kwargs):
                #   STEP 10: Error handling
                raise Exception("An error occured in SpongeBob.__getFitness__() -> Step 9: No data passed")

            #   STEP 11: Check if class password passed
            if ("password" not in kwargs):
                #   STEP 12: Error handling
                raise Exception("An error occured in SpongeBob.__getFitness__() -> Step 11: No class password passed")

            #   STEP 13: Get temp variables
            surrogate   = kwargs["surrogate"]
            data        = kwargs["data"]
            candidates  = kwargs["candidates"]
            password    = kwargs["password"]

            #   STEP 14: Iterate through candidates
            for i in range(0, len(candidates)):
                #   STEP 15: Set the surrogate weights
                surrogate.setWeights(weights=candidates[i], password=password)

                #   STEP 16: Append fitness to output list
                lOut.append(surrogate.getAFitness(data=data))

            #   STEP 17: Return
            return lOut

        else:
            #   STEP ??: Error handling
            raise Exception("An error occured in SpongeBob.__getFitness__() -> Step 6: Unimplemented functionality")
        
    def __getParams__(self, **kwargs) -> dict:
        """
            Description:

                Returns the specified optimization algorithm's required
                parameters.

            |\n
            |\n
            |\n
            |\n
            |\n

            Args:

                + optimizer     = ( enum ) The optimization algorithm

            |\n

            Returns:

                + dictionary    = ( dict ) Contains the following
                    ~ scalar    = ( float ) Algorithm weight scalar
                    ~ candidates    = ( int ) Number of candidates
                    ~ region        = ( int ) Initial region
                    ~ iterations    = ( int ) Algorithm iterations
                    ~ iterations-def    = ( int ) Algorithm default training
                        iterations

        """

        #   STEP 0: Local variables
        dTmp                    = self.__config.data["parameters"]["algorithms"]

        #   STEP 1: Setup - Local variables

        #   STEP 2: Check if TRO
        if (kwargs["optimizer"] == ga.TRO):
            #   STEP 3: Adjust holder dictionary
            dTmp = dTmp["tro"]

            #   STEP 4: Populate output dictionary
            dOut = {
                "iterations":       dTmp["training"]["iterations"]["algorithm"]["default"],
                "iterations-def":   dTmp["training"]["iterations"]["back propagation"]["default"],
                "candidates":       dTmp["training"]["candidates"]["default"],
                "scalar":           dTmp["training"]["candidate scalar"]["default"],
                "check point":      dTmp["training"]["acc check point"]["default"],
                "requirement":      dTmp["training"]["acc requirement"]["default"],
                "region":           dTmp["training"]["region"]["default"],

                "mapping":          dTmp["mapping"]
            }

            #   STEP 5: Return
            return dOut

        #   STEP ??: Error handling
        raise Exception("An error occured in SpongeBob.__getParams__(): Unimplemented optimizer passed")

    #
    #   endregion

    #   region Back-End: Training

    def __troTraining__(self, **kwargs) -> dict:
        """
            Description:

                Trains the passed surrogate using Trust-Region Optimization.

            |\n
            |\n
            |\n
            |\n
            |\n

            Args:
            
                + surrogate = ( vars ) The surrogate instance to be trained
                    ~ Required

                + data      = ( vars ) Data container
                    ~ Required

                + password  = ( int / float ) The surrogate instance's password
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

        dTroParams              = None

        garry                   = None

        dTrainingData           = None
        dTestingData            = None

        lCandidates             = []
        lFitness                = []

        iCount                  = 0
        
        #   endregion

        #   region STEP 1: Setup - Local variables

        #                       STEP 1.1: Init algorithm parameters
        dTroParams              = self.__getParams__(optimizer=ga.TRO)

        #                       STEP 1.2: Init datasets
        dTestingData            = kwargs["data"].splitData()
        
        dTrainingData           = dTestingData["training"]
        dTestingData            = dTestingData["testing"]
        
        #                       STEP 1.3: Setup surrogate
        
        #       STEP 1.3.1: Init surrogate and password variables
        surrogate               = kwargs["surrogate"]
        password                = kwargs["password"]

        #       STEP 1.3.2: Init surrogate activation funcitons
        surrogate.setAcFunction(password=password, algorithm="tro", scalar=dTroParams["scalar"])
        
        #       STEP 1.3.3: Init candidate list
        lCandidates.append(surrogate.getWeights(password=password))

        #       STEP 1.3.4: Init fitness list
        lFitness                = self.__getFitness__(type="surrogate", candidates=lCandidates, surrogate=surrogate, data=dTestingData, password=password)
        
        #                       STEP 1.4: Init genetic algorithm
        garry                   = Garry(dTroParams["candidates"])

        garry.initTroParticles(candidates=lCandidates)
        garry.initTroFitness(fitness=lFitness)
        garry.initTroParams(region=dTroParams["region"])

        #   endregion

        #   STEP 2: User Output
        if (self.bShowOutput):
            print("SpongeBob (train-srg-tro) {" + Helga.time() + "} - Starting Trust-Region Optimization\n")

        #   STEP 3: Perform specified number of iterations
        for i in range(0, dTroParams["iterations"] + 1):
            #   STEP 4: Clear necesarry variables
            lCandidates     = []
            lFitness        = []

            #   STEP 5: Populate candidate list
            lCandidates = self.__getCandidates__(optimizer=ga.TRO, params=dTroParams, initial=garry.lTroBest[0].lCurrPosition, region=float(garry.iTroRegion / dTroParams["region"]))

            #   STEP 6: Get candidate list fitness
            for j in range(0, len(lCandidates)):
                #   STEP 7: Set surrogate weights
                surrogate.setWeights(weights=lCandidates[j], password=password)

                #   STEP 8: Append candidate fitness
                lFitness.append(surrogate.getAFitness(data=dTestingData))

            #   STEP 9: Update garry
            garry.setPopulation(candidates=lCandidates)
            garry.setFitness(fitness=lFitness)

            #   STEP 10: Set surrogate weight to best candidate
            surrogate.setWeights(weights=garry.vBestSolution.lCurrPosition, password=password)

            #   STEP 11: Perform default training
            for j in range(0, dTroParams["iterations-def"]):
                #   STEP 12: Get random data sample
                dDNR = dTrainingData.getRandDNR()

                #   STEP 13: Perform propagation
                surrogate.propagateForward(data=dDNR["in"], password=password)
                surrogate.propagateBackward(data=dDNR["out"], password=password)

            #   STEP 14: Update garry
            garry.vBestSolution.lCurrPosition = surrogate.getWeights(password=password)
            garry.fBestSolution = surrogate.getAFitness(data=dTestingData)

            #   STEP 15: Perform trust-region optimization
            garry.tro()

            #   STEP 16: Check if region is still okay
            if (garry.iTroRegion <= 1):
                #   STEP 17: Exit loop
                break

            #   STEP 18: Check if accucacy check needs to be performed
            if (iCount == dTroParams["check point"]):
                #   STEP 19: Reset counter
                iCount = 0

                #   STEP 20: Get accuracy as percentage
                dHold = surrogate.getAccuracy(data=kwargs["data"], size=kwargs["data"].getLen())
                iAcc = dHold["accurate samples"]
                fAcc = dHold["percent accuracy"]

                #   STEP 21: Check if accuracy requirement met
                if (fAcc >= dTroParams["requirement"]):
                    #   STEP 22: User Output
                    if (self.bShowOutput):
                        print("SpongeBob (train-srg-tro) {" + Helga.time() + "} - Trust-Region Optimization successful")
                        print("\tTotal Iterations: " + str(i))
                        print("\tAccurate Samples: " + str(iAcc))
                        print("\tPercent Accuracy: " + str(round(fAcc * 100.0, 2)) + "%\n")

                    #   STEP 23: Populate output dictionary
                    dOut = {
                        "accuracy":     iAcc,
                        "algorithm":    "tro",
                        "iterations":   i,
                        "scalar":       dTroParams["scalar"],
                        "surrogate":    surrogate
                    }

                    #   STEP !!: Check that iAcc > 0
                    if (iAcc <= 0):
                        dOut["inverse accuracy"] = np.inf

                    else:
                        dOut["inverse accuracy"] = float(dHold["iterations"] / iAcc)

                    #   STEP 24: Return
                    return dOut

            #   STEP 25: Increment counter
            iCount += 1

        #   STEP 26: Get accuracy as percentage
        dHold = surrogate.getAccuracy(data=kwargs["data"], size=kwargs["data"].getLen())
        iAcc = dHold["accurate samples"]
        fAcc = dHold["percent accuracy"]

        #   STEP 27: User Output
        if (self.bShowOutput):
            #   STEP 28: Print output
            if (fAcc >= dTroParams["requirement"]):
                print("SpongeBob (train-srg-tro) {" + Helga.time() + "} - Trust-Region Optimization successful")
                print("\tTotal Iterations: " + str(i))
                print("\tAccurate Samples: " + str(iAcc))
                print("\tPercent Accuracy: " + str(round(fAcc * 100.0, 2)) + "%\n")

            else:
                print("\tSpongeBob (train-srg-tro) {" + Helga.time() + "} - Trust-Region Optimization Unsuccessful")
                print("\t\tTotal iterations: " + str(i))
                print("\t\tAccurate Samples: " + str(iAcc))
                print("\t\tPercent Accuracy: " + str(round(fAcc * 100.0, 2)) + "%\n")

        #   STEP 29: Populate output dictionary
        dOut = {
            "accuracy":     iAcc,
            "algorithm":    "tro",
            "iterations":   -i,
            "scalar":       dTroParams["scalar"],
            "surrogate":    surrogate
        }


        #   STEP 31: Check that iAcc > 0
        if (iAcc <= 0):
            dOut["inverse accuracy"] = np.inf

        else:
            dOut["inverse accuracy"] = float(dHold["iterations"] / iAcc)

        #   STEP 30: Return
        return dOut

    #
    #   endregion

    #   region Back-End: Mapping

    def __troMapping__(self, **kwargs) -> dict:
        """
            Description:

                Maps the passed surrogate using Trust-Region Optimization.

            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:

                + surrogate = ( vars ) The surrogate instance to be mapped
                    ~ Required

                + data  = ( vars ) A Data container that contains the dataset
                    to be used during the mapping process
        """

        #   STEP 0: Local variables
        vData                   = None
        vGarry                  = None
        vSRG                    = None

        dTRO_Params             = None

        lCandidates             = []
        lFitness                = []
        
        #   STEP 1: Setup - Local variables

        #   region STEP 2->5: Error checking

        #   STEP 2: Check if surrogate arg passed
        if ("surrogate" not in kwargs):
            #   STEP 3: Error handling
            raise Exception("An error occured in SpongeBob.__troMapping__() -> Step 2: No surrogate arg passed")

        #   STEP 4: CHeck if data arg passed
        if ("data" not in kwargs):
            #   STEP 5: Error handling
            raise Exception("An error occured in SpongeBob.__troMapping__() -> Step 4: No data arg passed")
        
        #
        #   endregion
        
        #   region STEP 6->10: Setup - Local variabls
        
        #   STEP 6: Update - Local variables
        vData   = kwargs["data"]
        vSRG    = kwargs["surrogate"]

        #   STEP 7: Get initial candidate
        iTmp_Candidate  = vData.getInputWidth()
        lTmp_Candidate  = []
        
        for _ in range(0, iTmp_Candidate):
            lTmp_Candidate.append(0.0)

        lCandidates.append(lTmp_Candidate)

        #   STEP 8: Get initial fitness
        lFitness.append(vSRG.getPointOutput(lTmp_Candidate))

        #   STEP 9: Get TRO params
        dTRO_Params = self.__getParams__(optimizer=ga.TRO)["mapping"]

        #   STEP 10: Setup - Garry
        vGarry       = Garry(dTRO_Params["candidates"])

        vGarry.initTroParticles(candidates=lCandidates)
        vGarry.initTroFitness(fitness=lFitness)
        vGarry.initTroParams(region=dTRO_Params["region"])

        #
        #   endregion
        
        #   STEP 11: User output
        if (self.bShowOutput):
            print("SpongeBob (map-srg-TRO) {" + Helga.time() +"} - Starting Trust-Region Optimization mapping")

        #   STEP 12: Loop for max iterations
        for i in range(0, dTRO_Params["iterations"] + 1):
            #   STEP 13: Clear required variables
            lFitness    = []

            #   STEP 14: Populate candidate list
            lCandidates = self.__getCandidates__(optimizer=ga.TRO, params=dTRO_Params, initial=vGarry.lTroBest[0].lCurrPosition, region=float(vGarry.iTroRegion / dTRO_Params["region"]))

            #   STEP 15: Loop through candidates
            for j in range(0, len(lCandidates)):
                #   STEP 16: Get candidate fitness
                lFitness.append(vSRG.getPointOutput(lCandidates[j]))

            #   STEP 17: Update garry
            vGarry.setPopulation(candidates=lCandidates)
            vGarry.setFitness(fitness=lFitness)

            #   STEP 18: Perform trust-region optimization
            vGarry.tro()

            #   STEP 19: Check if region too small
            if (vGarry.iTroRegion <= 1):
                #   STEP 20: Exit loop
                break

        #   STEP 27: User output
        if (self.bShowOutput):
            print("SpongeBob (map-srg-TRO) {" + Helga.time() + "} - Trust-Region Optimizaion mapping completed")
            print("\tTotal Iterations: " + str(i))

        #   STEP 28: Populate output dictionary
        dOut    = {
            "result":       vGarry.lTroBest[0].lCurrPosition,
            "fitness":      vGarry.lTroBest[1],
            "iterations":   i
        }

        #   STEP ??: Return
        return dOut

    #
    #   endregion

    #
    #endregion
    
#
#endregion