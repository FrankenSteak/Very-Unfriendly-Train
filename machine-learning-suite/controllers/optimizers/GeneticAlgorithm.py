#region Imports
import  numpy                           as np
import  os
import  sys

sys.path.append(os.path.abspath("."))

from config.Config import Conny
from models.Particle import UwU
#endregion

#region Class - Garry

class Garry:

    #region Init

    """
    """

    def __init__(self, _iPopSize: int) -> None:

        #region STEP 0: Local variables
        self.__cf = Conny()
        self.__cf.load("GeneticAlgorithms.json")

        #endregion

        #region STEP 1: Private variables

        #   region STEP 1.1: Pop size

        self.__iPopSize             = _iPopSize

        #   endregion

        #   region STEP 1.2: Init flags

        self.__bTroState            = [False, False, False]

        #   endregion

        #   region STEP 1.3: Bools

        self.__bAllowTesting        = self.__cf.data["parameters"]["allow testing"]

        #   endregion

        #endregion

        #region STEP 2: Public variables

        #   region STEP 2.1: Population

        self.lPopulation            = []

        self.vBestSolution          = None
        self.fBestSolution          = np.inf
        self.iBestSolution          = 0

        #   endregion

        #   region STEP 2.2: TRO

        self.iTroRegion             = None
        self.lTroBest               = None

        #   endregion

        #   region STEP 2.3: Bools

        self.bShowOutput            = self.__cf.data["parameters"]["show output"]

        #   endregion

        #endregion

        #region STEP 3: Setup - Private variables

        #endregion

        #region STEP 4: Setup - Public variables

        #endregion

        return

    #
    #endregion

    #region Front-End

    #   region Front-End: Sets

    def setPopulation(self, **kwargs) -> None:
        """
            Description:

                Initializes the population using the provided list of candidate
                positions

            |\n
            |\n
            |\n
            |\n
            |\n

            Args:
            
                + candidates    = ( list ) List of candidate positions
                    ~ Required

        """

        #   STEP 0: Local variables
        candidates              = None

        #   STEP 1: Setup - Local variables

        #   STEP 2: Check if candidate
        if ("candidates" not in kwargs):
            #   STEP 3: Error handling
            raise Exception("An error occured in Garry.setPopulation() -> Step 2: No candidate list passed")
        
        #   STEP 4: Check that candidate list is right length
        if (len(kwargs["candidates"]) != self.__iPopSize):
            #   STEP 5: Error handling
            raise Exception("An error occured in Garry.setPopulation() -> STEp 4: Incorrect candidate list length passed")

        #   STEP 6: Set the class population
        if (len(self.lPopulation) > 0):
            #   STEP 7: Reset class candidate list
            self.lPopulation = []

        #   STEP 8: Init temp variable
        candidates = kwargs["candidates"]

        #   STEP 9: Iterate through candidates
        for i in range(0, len(candidates)):
            #   STEP 10: Create new candidate
            candy = UwU()

            #   STEP 11: Populat new candidate data
            candy.lCurrPosition = candidates[i]

            #   STEP 12: Append new candidate to population list
            self.lPopulation.append(candy)

        #   STEP 13: Return
        return

    def setFitness(self, **kwargs) -> None:
        """
            Description:

                Sets the fitness for the current population.

            |\n
            |\n
            |\n
            |\n
            |\n

            Args:

                + fitness   = ( list ) Fitness values for the population
                    ~ Required

        """

        #   STEP 0: Local variables
        fitness                 = None

        #   STEP 1: Setup - Local variables

        #   STEP 2: Check if fitness passed
        if ("fitness" not in kwargs):
            #   STEP 3: Error handling
            raise Exception("An error occured in Garry.setFitness() -> Step 2: No fitness list passed")

        #   STEP 4: Check fitness list length
        if not ((len(kwargs["fitness"]) == len(self.lPopulation)) and (len(self.lPopulation) == self.__iPopSize)):
            #   STEP 5: Error handling
            raise Exception("An error occured in Garry.setFitness() -> Step 4: List length mismatch")

        #   STEP 5: Set local variable
        fitness = kwargs["fitness"]

        #   STEP 6: Iterate through fitness list
        for i in range(0, len(fitness)):
            #   STEP 7: Check if fitness is list
            if (type(fitness[i]) == list):
                #   STPE 8: Setup - Temp vars
                fTmp_TotalFitness   = 0.0

                #   STEP 9: Iterate through list
                for j in range(0, len(fitness[i])):
                    #   STEP 10: Sum
                    fTmp_TotalFitness += fitness[i][j]

                #   STEP 11: Set pop fitness
                self.lPopulation[i].fFitness = fTmp_TotalFitness

            #   STEP 12: Not list
            else:
                #   STEP 13: Set pop fitness
                self.lPopulation[i].fFitness = fitness[i]

            #   STEP 14: Check if new best fitness
            if (self.lPopulation[i].fFitness < self.fBestSolution):
                #   STEP 15: Set best candidate variables
                self.fBestSolution = self.lPopulation[i].fFitness
                self.vBestSolution = self.lPopulation[i]
                self.iBestSolution = i

        #   STEP 16: Return
        return

    #
    #   endregion

    #   region Front-End: Trust-Region-Optimization

    def tro(self) -> list:
        """
        """

        #   STEP 0: Local variables
        #   STEP 1: Setup - Local variables

        #   STEP 2: Check if initialized
        if not (self.__bTroState[2]):
            #   STEP 3: Check if should be initialized
            if ((self.__bTroState[0]) and (self.__bTroState[1])):
                #   STEP 4: Set initialized flag
                self.__bTroState[2] = True

            else:
                #   STEP 5: Error handling
                raise Exception("An error occured in Garry.tro() -> Step 3: Trust-region optimization algorithm not initialized")

        #   STEP 6: Check if new fittest solution is better than previous solution
        if (self.fBestSolution < self.lTroBest[1]):
            #   STEP 7: Adjust tro best candidate
            self.lTroBest[0] = self.vBestSolution
            self.lTroBest[1] = self.fBestSolution

            #   STEP 8: Increase trust region
            self.iTroRegion += 1

        else:
            #   STEP 9: Decrease trust region
            self.iTroRegion -= 1

        #   STEP 10: Clear irrelevant data
        self.lPopulation    = []
        self.vBestSolution  = None
        self.fBestSolution  = np.inf
        self.iBestSolution  = 0

        #   STEP 11: Return
        return

    #       region Front-End-(Trust-Region-Optimization): Init

    def initTroParticles(self, **kwargs) -> None:
        """
            Description:

                Initializes the initial candidates for the trust-region
                optimization process.

            |\n
            |\n
            |\n
            |\n
            |\n

            Args:
            
                + candidates    = ( list ) List of candidates

        """

        #   STEP 0: Local variables
        #   STEP 1: Setup - Local variables

        #   STEP 2: Check if candidates passed
        if ("candidates" not in kwargs):
            #   STEP 3: Error handling
            raise Exception("An error occured in Garry.initTroParticles() -> Step 2: No candidate list")

        #   STEP 4: Check that candidates is greater than zero
        if (len(kwargs["candidates"]) != 1):
            #   STEP 5: Error handling
            raise Exception("An error occured in Garry.initTroParticles() -> Step 4: Invalid candidate list passed")

        #   STEP 8: Create new candidate
        pop = UwU()

        #   STEP 9: Set candidate data
        pop.lCurrPosition =  kwargs["candidates"][0]

        #   STEP 10: Append to class population list
        self.lPopulation.append(pop)

        #   STEP 11: Set best solution
        self.vBestSolution = self.lPopulation[0]
        self.iBestSolution = 0

        #   STEP 12: Init tro best variables
        if (self.lTroBest == None):
            self.lTroBest = [None, None]

        self.lTroBest[0] = self.vBestSolution

        #   STEP 13: Set init flag
        self.__bTroState[0] = True

        #   STEP 14: Return
        return

    def initTroFitness(self, **kwargs) -> None:
        """
            Description:

                Sets the fitness of the starting population

            |\n
            |\n
            |\n
            |\n
            |\n

            Args:

                + fitness   = ( list ) List of fitness values for population
                    ~ Requried

        """

        #   STEP 0: Local variables
        #   STEP 1: Setup - Local variables

        #   STEP 2: Check if fitness passed
        if ("fitness" not in kwargs):
            #   STEP 3: Error handling
            raise Exception("An error occured in Garry.initTroFitness() -> Step 2: No fitness list passed")

        #   STEP 4: Check fitness length
        if (len(kwargs["fitness"]) != 1):
            #   STEP 5: Error handling
            raise Exception("An error occured in Garry.initTroFitness() -> Step 4: Invalid fitness list passed")
        
        #   STEP 6: Check if fitness is a list
        if (type(kwargs["fitness"][0]) == list):
            #   STEP 8: Setup - Temp vars
            fTmp_Fitness    = 0.0
            lFitness        = kwargs["fitness"][0]

            #   STPE 9: Iterate through list
            for i in range(0, len(lFitness)):
                #   STEP 10: Sum
                fTmp_Fitness    += lFitness[i]

            #   STEP 11: Set initial best fitness
            self.fBestSolution = fTmp_Fitness

        #   STEP 12: Input fitness not a list
        else:
            #   STEP 13: Set initial candidate fitness
            self.fBestSolution = kwargs["fitness"][0]

        #   STEP 14: Init tro best variable
        if (self.lTroBest == None):
            self.lTroBest = [None, None]

        self.lTroBest[1] = self.fBestSolution

        #   STEP 15: Set init flag
        self.__bTroState[1] = True

        #   STEP 16: Return
        return

    def initTroParams(self, **kwargs) -> None:
        """
            Description:

                Initializes the trust-region optimization process' parameters.

            |\n
            |\n
            |\n
            |\n
            |\n

            Args:

                + region    = ( int / float ) The algorithm's initial region

        """

        #   STEP 0: Local variables
        #   STEP 1: Setup - Local variables

        #   STEP 2: Check if region passed
        if ("region" not in kwargs):
            #   STEP 3: Error handling
            raise Exception("An error occured in Garry.initTroParams() -> Step 2: No region passed")

        #   STEP 4: Set the initial region
        self.iTroRegion = kwargs["region"]

        #   STEP 5: Set init flag
        self.__bTroState[1] = True

        #   STEP 6: return
        return

    #
    #       endregion

    #
    #   endregion

    #
    #endregion

    #region Back-End

    #   region Back-End: Trust-Region-Optimization

    def __troStats(self) -> None:
        """
        """

        #   STEP 0: Local variables
        #   STEP 1: Setup - Local variables

        #   STEP 2: ??


        return

    #
    #   endregion

    #
    #endregion

#
#endregion