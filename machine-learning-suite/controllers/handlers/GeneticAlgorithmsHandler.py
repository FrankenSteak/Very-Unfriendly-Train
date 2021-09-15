#region --- Imports ---
import  numpy                               as np
import  os
import  random                              as rn
import  sys

sys.path.append(os.path.abspath("."))

from config.Config import Conny
from controllers.optimizers.GeneticAlgorithms import GeneticAlgorithms as ga
from controllers.optimizers.GeneticAlgorithm import Garry
from helpers.GeneralHelpers import Helga
#endregion

class SpongeBob:
    #region --- Private ---
    def __init__(self):
        #   --- Setup ---
        self.__config = Conny()
        self.__config.load("SpongeBob.json")
        #   --- Private ---
        self.__bAllowTesting = self.__config.data["parameters"]["allow testing"]["default"]
        #   --- Public ---
        self.bShowOutput = self.__config.data["parameters"]["show output"]["default"]
        #   --- Response ---
        return

    #
    #endregion

    #region --- Public: FE ---
    def map_surrogate(self, **kwargs) -> dict:
        """
            - Description::

                Maps the passed surrogate using the specified optimizer.

            |\n
            |\n
            |\n
            |\n
            |\n
            - Parameters::

                :param surrogate: >> ( vars ) The surrogate that requires mapping
                    ~ Required

                + data  = ( vars ) A Data container that contains the data
                    for the mapping process
                    ~ Required

                + optimizer = ( enum ) The optimizer to be used during the
                    mapping process
                    ~ Required
        """

        #   STEP 2: Check if surrogate arg passed
        if ("surrogate" not in kwargs):
            #   STEP 3: Error handling
            raise Exception("An error occured in SpongeBob.map_surrogate() -> Step 2: No surrogate arg passed")

        #   STEP 4: Check if data arg passed
        if ("data" not in kwargs):
            #   STEP 5: Error handling
            raise Exception("An error occured in SpongeBob.map_surrogate() -> Step 4: No data arg passed")

        #   STEP 6: Check if optimizer arg passed
        if ("optimizer" not in kwargs):
            #   STEP 7: Error handling
            raise Exception("An error occured in SpongeBob.map_surrogate() -> Step 6: No optimizer arg passed")
        
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
        raise Exception("An error occured in SpongeBob.map_surrogate() -> Step 12: Unrecognized optimizer")

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

    #region --- Private: BE ---
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
                        #   STEP 16: Modify value using region and scalar
                        lTmp[i] = rn.gauss(kwargs["initial"][i], kwargs["params"]["scalar"] * kwargs["region"])

                        #   STEP 17: Check if value above upper limit
                        if (lTmp[i] > 1.0):
                            #   STEP 18: Limit value
                            lTmp[i] = 1.0

                        #   STEP 19: Check if value below lower limit
                        if (lTmp[i] < -1.0):
                            #   STEP 20: Limit value
                            lTmp[i] = -1.0

                    else:
                        #   STEP 21: Iterate through list
                        for j in range(0, len(lTmp[i])):
                            #   STEP 22: Modify value using region and sacalar
                            lTmp[i][j] = rn.gauss(kwargs["initial"][i][j], kwargs["params"]["scalar"] * kwargs["region"])
                            
                            #   STEP 23: Check if value above upper limit
                            if (lTmp[i][j] > 1.0):
                                #   STEP 24: Limit value
                                lTmp[i][j] = 1.0

                            #   STEP 25: Check if value below lower limit
                            if (lTmp[i][j] < -1.0):
                                #   STEP 26: Limit value
                                lTmp[i][j] = -1.0


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

        #   STEP 0: Local variables
        surrogate               = None
        password                = None

        dTroParams              = None

        garry                   = None

        dTestingData            = None

        lCandidates             = []
        lFitness                = []
        
        #   region STEP 1->6: Error checking

        #   STEP 1: Check if surrogate arg passed
        if ("surrogate" not in kwargs):
            #   STEP 2: Error handling
            raise Exception("An error occured in SpongeBob.__troTraining__() -> Step 1: NO surrogate arg passed")

        #   STEP 3: Check if data arg passed
        if ("data" not in kwargs):
            #   STEP 4: Error handling
            raise Exception("An error occured in SpongeBob.__troTraining__() -> Step 3: No data arg passed")

        #   STEP 5: Check if password arg passed
        if ("password" not in kwargs):
            #   STEP 6: Error handling
            raise Exception("An error occured in SpongeBob.__troTraining__() -> Step 5: No password arg passed")

        #
        #   endregion
        
        #   region STEP 7->13: Setup - Local variables

        #   STEP 7: Init algorithm parameters
        dTroParams      = self.__getParams__(optimizer=ga.TRO)

        #   STEP 8: Init datasets
        dTestingData    = kwargs["data"].splitData()
        
        dData_Train     = dTestingData["training"]
        dData_Test      = dTestingData["testing"]
        
        #   STEP 9: Init surrogate and password variables
        surrogate       = kwargs["surrogate"]
        password        = kwargs["password"]

        #   STEP 10: Init surrogate activation funcitons
        
        #   STEP 11: Init candidate list
        lCandidates.append(surrogate.getWeights(password=password))

        #   STEP 12: Init fitness list
        lFitness        = self.__getFitness__(type="surrogate", candidates=lCandidates, surrogate=surrogate, data=dData_Test, password=password)
        
        #   STEP 13: Init genetic algorithm
        garry           = Garry(dTroParams["candidates"])

        garry.initTroParticles(candidates=lCandidates)
        garry.initTroFitness(fitness=lFitness)
        garry.initTroParams(region=dTroParams["region"])

        #   STPE 14: Check if L1
        fTmp    = rn.uniform(0.0, 1.0)

        #   STEP 15: Check if L1
        if (fTmp < 0.65):
            #   STEP 16: Set - L1
            surrogate.bUse_L1   = True

        #   STEP 17: Check if L2
        elif (fTmp < 0.85):
            #   STEP 18: Set - L2
            surrogate.bUse_L2   = True

        #
        #   endregion

        #   STEP 14: User Output
        if (self.bShowOutput):
            print("SpongeBob (train-srg-tro) {" + Helga.time() + "} - Starting Trust-Region Optimization\n")

        #   STEP 15: Perform specified number of iterations
        for i in range(0, dTroParams["iterations"] + 1):
            #   STEP 16: Clear necesarry variables
            lCandidates     = []
            lFitness        = []

            #   STEP 5: Populate candidate list
            lCandidates = self.__getCandidates__(optimizer=ga.TRO, params=dTroParams, initial=garry.lTroBest[0].lCurrPosition, region=float(garry.iTroRegion / dTroParams["region"]))

            #   STEP 6: Get candidate list fitness
            for j in range(0, len(lCandidates)):
                #   STEP 7: Set surrogate weights
                surrogate.setWeights(weights=lCandidates[j], password=password)

                #   STEP 8: Append candidate fitness
                lFitness.append(surrogate.getAFitness(data=dData_Test))

            #   STEP 9: Update garry
            garry.setPopulation(candidates=lCandidates)
            garry.setFitness(fitness=lFitness)

            #   STEP 10: Set surrogate weight to best candidate
            surrogate.setWeights(weights=garry.vBestSolution.lCurrPosition, password=password)

            #   STEP 11: Perform default training
            for j in range(0, dTroParams["iterations-def"]):
                #   STEP 12: Get random data sample
                dDNR = dData_Train.getRandDNR(noise=True)

                #   STEP 13: Perform propagation
                surrogate.propagateForward( data=dDNR["in"], password=password)
                surrogate.propagateBackward( data=dDNR["out"], password=password)

            #   STEP 14: Update garry
            garry.vBestSolution.lCurrPosition   = surrogate.getWeights(password=password)
            garry.fBestSolution                 = surrogate.getAFitness(data=dData_Test)

            #   STEP 15: Perform trust-region optimization
            garry.tro()

            #   STEP 16: Check if region is still okay
            if (garry.iTroRegion <= 1):
                #   STEP 17: Exit loop
                break

        #   STEP 26: Get accuracy as percentage
        dHold = surrogate.getAccuracy(data=kwargs["data"], size=kwargs["data"].getLen(), full_set=True)
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

    def __limit_candidate_to_trust_region__(self, **kwargs) -> list:
        """
            Description:

                Limits the provided candidate to the range of -1 and 1.

            |\n
            |\n
            |\n
            |\n
            |\n

            Args:
            
                + candidate     = ( list ) The candidate to be adjusted
                    ~ Required
            
            |\n

            Returns:

                + dictionary        = ( dict ) A dict instance containing
                    ~ surrogate     = ( vars ) The trained surrogate
                    ~ iterations    = ( int ) The training iterations
                    ~ scalar        = ( float ) The surrogate intstance's scalar
        """

        #   region STEP 0->1: Error handling

        #   STEP 0: Check if candidate arg passed
        if ("candidate" not in kwargs):
            #   STEP 1: Error handling
            raise Exception("An error occured in Sarah.__limit_candidate_to_trust_region__() -> Step 0: No candidate arg passed")

        #
        #   endregion
        
        #   STEP 2: Local variables
        lCandidate                  = kwargs["candidate"]

        #   STEP 3: Loop through candidate
        for i in range(0, len(lCandidate)):
            #   STEP 4: Check if single data point
            if (type(lCandidate[i]) == float):
                #   STEP 5: Check if value over limit
                if (lCandidate[i] > 1.0):
                    #   STEP 6: Limit value
                    lCandidate[i] = 1.0
                
                #   STEP 7: Check if value below lower limit
                elif (lCandidate[i] < -1.0):
                    #   STEP 8: Limit value
                    lCandidate[i] = -1.0

            else:
                #   STEP 9: Loop through data point
                for j in range(0, len(lCandidate[i])):
                    #   STEP 10: Check if value over upper limit
                    if (lCandidate[i][j] > 1.0):
                        #   STEP 11: Limit value
                        lCandidate[i][j] = 1.0
                    
                    #   STEP 12: Check if value below lower limit
                    elif (lCandidate[i][j] < -1.0):
                        #   STEP 13: Limit value
                        lCandidate[i][j] = -1.0

        #   STEP 14: Return
        return lCandidate

    #
    #   endregion
