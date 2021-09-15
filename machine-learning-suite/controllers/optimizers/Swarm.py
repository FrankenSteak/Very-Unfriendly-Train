#region Imports
import  numpy                           as np
import  os
import  random                          as rn
import  sys

sys.path.append(os.path.abspath("."))

from static.Enums import Enums as en
from controllers.optimizers.Swarms import Swarms as sw
from models.Particle import UwU
from config.Config import Conny
from helpers.GeneralHelpers import Helga
#endregion

#region Class - Swarm

class SwarmChan:

    #region Init

    """
        Description:

            This class are very kawai :3
        
        |\n
        |\n
        |\n
        |\n
        |\n
        
        Parameters:

            :param _iParticles: = ( int ) The number of particles in the swarm

        Returns:

            :return: >> (None)
    """

    def __init__(self, _iParticles: int) -> None:

        #region STEP 0: Local variables

        self.__enum                 = en.SwarmChan
        self.__cf                   = Conny()
        self.__cf.load(self.__enum.value)

        #endregion

        #region STEP 1: Private variables

        #   region STEP 1.1: Particles

        self.__iParticles           = _iParticles

        #   endregion

        #   region STEP 1.2: Init flags

        self.__bPsoState            = [False, False, False, False]
        self.__bBeeState            = [False, False, False, False]
        self.__bNemState            = [False, False, False, False]

        #   endregion

        #   region STEP 1.3: bools

        self.__bAllowTesting        = self.__cf.data["parameters"]["allow testing"]

        #   endregion
        
        #   region STEP 1.4: Other

        self.__data               = [None]

        #   endregion

        #endregion

        #region STEP 2: Public variables

        #   region STEP 2.1: Paricles

        self.lParticles             = []

        self.lBestSolution          = None
        self.fBestSolution          = np.inf
        self.iBestSolution          = 0
        
        #   endregion
        
        #   region STEP 2.2: PSO

        self.psoPhi1                = 0.0
        self.psoPhi2                = 0.0
        self.psoN                   = 0.0
        self.psoX                   = 0.0

        #   endregion

        #   region STEP 2.3: BEE

            #idk       

        #   endregion

        #   region STEP 2.4: Nelder-Mead

        self.NM_Alpha               = None
        self.NM_Beta                = None
        self.NM_Gamma               = None
        self.NM_Sigma               = None

        self.NM_State               = None
        self.NM_lGetFitness         = None

        #
        #   endregion

        #   region STEP 2.5: Bools

        self.bShowOutPut            = self.__cf.data["parameters"]["show output"]
        
        #   endregion

        #endregion

        #region STEP 3: Setup - Private variables

        #endregion

        #region STEP 4: Setup - Public variables

        #   region STEP 4.1: Particles

        for _ in range(0, _iParticles):
            self.lParticles.append(UwU())
        
        #   endregion

        #endregion

        
        return

    #
    #endregion

    #region Front-End

    #   region Front-End: Sets

    def setParticlePositions(self, _lData: list) -> None:
        """
            - **Description**::

            Sets the current positions of all the particles
            
            |\n
            |\n
            |\n
            |\n
            |\n
            - **Parameters**::

                :param _lData: >> (list) The current position of each particle

            - **Return**::

                :return: >> (None)
        """
        
        #   STEP 1: Check that the data size is correct
        if (len(_lData) != self.__iParticles):
            raise Exception("Error in Swarm.setParticlePositions: Wrong data size for position initialization")

        #   STEP 2: Do the loopdy loop
        for i in range(0, self.__iParticles):
            self.lParticles[i].lCurrPosition = _lData[i]
        
        #   STEP 3: Return
        return

    def setParticleFitness(self, _lData: list) -> None:
        """
            - **Description**::

            Sets the current fitness of all the particles
            
            |\n
            |\n
            |\n
            |\n
            |\n
            - **Parameters**::

                :param _lData: >> (list) The current fitness of each particle

            - **Return**::

                :return: >> (None)
        """

        #   STEP 0: Local variables

        #   STEP 1: Setup - Local variables

        #   STEP 2: Check that the data size is correct
        if (len(_lData) != self.__iParticles):
            #   STEP 3: Error handling
            raise Exception("An error occured in Swarm.setParticleFitness() -> Step 2: Wrong data size for fitness initialization")

        #   STEP 4: Be safe OwO
        try:
            #   STEP 5: Do the loopdy loop
            for i in range(0, self.__iParticles):
                #   STEP 6: Check if fitness is list
                if (type(_lData[i]) == list):
                    #   STEP 7: Setup - Tmp variables
                    fSum    = 0.0

                    #   STEP 8: Loop through list
                    for j in range(0, len( _lData[i] ) ):
                        #   STEP 9: Sum fitness values
                        fSum    += _lData[i][j]

                    #   STEP 10: Set particle fitness
                    self.lParticles[i].setFitness( fSum )

                #   STEP 11: Fitness isn't a list
                else:
                    #   STEP 12: Set particle fitness
                    self.lParticles[i].setFitness(_lData[i])

                #   STEP 13: Check if current particle fitness is new best
                if (self.lParticles[i].fFitness < self.fBestSolution):
                    #   STEP 14: Update - Best variables
                    self.iBestSolution = i
                    self.lBestSolution = self.lParticles[i].lCurrPosition

                    self.fBestSolution = self.lParticles[i].fFitness
            
        #   STEP 15: Oopsie daisie
        except Exception as ex:
            #   STEP 16: Whoopsy daisy
            print("Initial error: ", ex)
            raise Exception("Error in Swarm.setParticleFitness() -> Step 15")

        #   STEP 17: Return
        return    
        
    #
    #   endregion
    
    #   region Front-End: Particle-Swarm-Optimization

    def pso(self) -> None:
        """
			Description:

                This function moves all the swarm particles according to the 
                PSO algorithm. C1 and C2 control the velocity and thus are
                called the accelration constants. Small C values allow the 
                particles to explore further away from gBest whereas larger
                C values encourage particles to search more intensively in
                regions close to gBest. R1 and R2 are the social factors and
                ensure that the algorithm is stochastic. X is the inertial 
                weight factor. A large X value causes the algorithm to search
                for a solution globally whereas a small X value allows the 
                algorithm to search local minima more thoroughly

			|\n
			|\n
			|\n
			|\n
			|\n
		"""
        
        #   STEP 0: Local variables
        #   STEP 1: Setup - Local variables

        #   STEP 2: Check if PSO is initialized
        if (self.__bPsoState[3] != True):
            #   STEP 3: Check if it should be
            if ((self.__bPsoState[0] == True) and (self.__bPsoState[1] == True) and (self.__bPsoState[2] == True)):
                #   STEP 4: Set initialized flag and continue
                self.__bPsoState[3] = True

            else:
                #   STEP 5: Error handling
                raise Exception("An error occured in Swarm.psoSwarm() -> Step 3: PSO algorithm not initialized")

        #   STEP 6: Loop through UwU
        for i in range(0, self.__iParticles):
            #   STEP 7: Get particle positions
            lPCurrTmp   = self.lParticles[i].lCurrPosition
            lPBestTmp   = self.lParticles[i].lBestPosition
            lPVelocity  = self.lParticles[i].lVelocity

            #   STEP 8: Calculate velocity constant
            lAlpha1 = self.psoPhi1 * (np.array(lPBestTmp, dtype="object") - np.array(lPCurrTmp, dtype="object"))
            lAlpha2 = self.psoPhi2 * (np.array(self.lBestSolution, dtype="object") - np.array(lPCurrTmp, dtype="object"))
            lAlphaTmp = lAlpha1 + lAlpha2
            lAlphaTmp = lPVelocity + lAlphaTmp
            lBeta = self.psoX * (lAlphaTmp)
            
            #   STEP 9: Set the particels new velocity and position
            self.lParticles[i].lVelocity = lBeta
            self.lParticles[i].lCurrPosition = np.array(lPCurrTmp, dtype="object") + np.array(lBeta, dtype="object")

        return

    #       region Front-End-(Particle-Swarm-Optimization): Init

    def initPsoPositions(self, _lData: list) -> None:
        """
            - **Description**::

            Sets the current positions of all the particles for the PSO algorithm
            
            |\n
            |\n
            |\n
            |\n
            |\n
            - **Parameters**::

                :param _lData: >> (list) The current position of each particle

            - **Return**::

                :return: >> (None)
        """

        #   STEP 1: Be safe OwO
        try:
            #   STEP 2: Out-source the work =]
            self.setParticlePositions(_lData)

            #   STEP 3: Init Velocities
            for i in range(0, self.__iParticles):
                
                #   STEP 4: Create velocity
                lVel = []
                
                #   STEP 5: Loop through list
                for j in range(0, len(_lData[i])):
                    #   STEP 6: Check if 2D list
                    if (type(_lData[i][j]) == list):
                        #   STEP 7: Append zeros to velocity
                        lVel.append(np.zeros(len(_lData[i][j])))

                    #   STEP 8: Not a list
                    else:
                        #   STEP 9: Append zero to velocity
                        lVel.append(0.0)

                #   STEP 10: Set velocity
                self.lParticles[i].lVelocity = lVel
                
        except Exception as ex:
            #   STEP 11: Whoopsy daisy
            print("Initial error: ", ex)
            raise Exception("Error in Swarm.psoInitParticlePositions()")
        
        #   STEP 12: Set PSO positions flag to True
        self.__bPsoState[0] = True

        #   STEP 13: Return
        return

    def initPsoFitness(self, _lData: list) -> None:
        """
            - **Description**::

            Sets the current fitness of all the particles for the PSO algorithm
            
            |\n
            |\n
            |\n
            |\n
            |\n
            - **Parameters**::

                :param _lData: >> (list) The current fitness of each particle

            - **Return**::

                :return: >> (None)
        """

        #   STEP 1: Be safe OwO
        try:
            #   STEP 2: Out-source the work =]
            self.setParticleFitness(_lData)

        except Exception as ex:
            #   STEP 2.?: Whoopsy daisy
            print("Initial erro: ", ex)
            raise Exception("Error in Swarm.psoInitParticleFitness: Wrong data size for position initialization")

        #   STEP TODO: Set PSO fitness flag to True
        self.__bPsoState[1] = True

        #   STEP TODO + 1: Return
        return

    def initPsoParams(self, _fPhi1: float, _fPhi2: float, _fN: float) -> None:
        """
            - **Description**::

            Sets the parameters for the PSO algorithm
            
            |\n
            |\n
            |\n
            |\n
            |\n
            - **Parameters**::

                :param _fC1: >> (float) Acceleration Constant 1
                :param _fR1: >> (float) Social Factor 1
                :param _fC2: >> (float) Acceleration Constant 2
                :param _fR2: >> (float) Social Factor 2
                :param _fN: >> (float) exploitation co-effiecient

            - **Return**::

                :return: >> (None)
        """

        #   STEP 1: Set the algorithm parameters
        self.psoPhi1    = _fPhi1
        self.psoPhi2    = _fPhi2
        self.psoN       = _fN

        #   STEP 2: Update PSO algorithm parameters
        if (self.updatePsoParams()):

            #   STEP 3: Set PSO parameters flag to True
            self.__bPsoState[2] = True

        #   STEP 4: Return
        return

    def updatePsoParams(self) -> bool:
        """
            - **Description**::

            Updates the parameters for the PSO algorithm
            
            |\n
            |\n
            |\n
            |\n
            |\n
        """

        #   STEP 2: Get total phi
        fPhi = self.psoPhi1 + self.psoPhi2

        #   STEP 3: Return and set X
        if (fPhi > 4.0):
            self.psoX = 2.0 * self.psoN / abs(2.0 - fPhi - np.sqrt(fPhi * (fPhi - 4)))
            return True
        
        else:
            return False

    #
    #       endregion

    #
    #   endregion

    #   region Front-End: Bee-Colony-Optimization

    def bee(self) -> None:
        """
            Description:

                This funciton moves all the bee particles according to my
                revised ABC algorithm.

            |\n
            |\n
            |\n
            |\n
            |\n

            Variables:

                ~ bUseRegionFitness = ( bool ) Whether ot not a worker bee
                    should get the fitness of multiple samples within a 
                    region or not

                ~ bEvaluatorsAsScouts   = ( bool ) Whether or not to use
                    evaluator bees as scouts while the bees they employ are
                    out

                ~ bEvaluatorMemory  = ( bool ) Whether or not the evaluator
                    bees should have decaying memory

                ~ bHiveMovement = ( bool ) Whether or not the hive should be 
                    allowed to move to a more suitable location

                ~ bBirthDeath   = ( bool ) Whether or not the colony should be
                    allowed to grow if conditions are favorable

                ~ bWorkerDistraction    = ( bool ) Whether or not to allow 
                    worker bee distraction

                |\n

                ~ iNum_Workers  = ( int ) The number of worker bees in the
                    colony

                ~ iNum_Scounts  = ( int ) The number of scout bees in the 
                    colony

                ~ iNum_Evaluators   = ( int ) The number of evaluator bees in
                    the colony

                |\n

                ~ fSpeed_Worker = ( float ) The speed at which a worker bee
                    moves in the search space

                ~ fSpeed_Scout  = ( float ) The speed at which a scout bee
                    moves in the search space

                ~ fSpeed_Eval   = ( float ) The speed at which an evaluator
                    bee moves in the search space

                ~ fSpeed_Queen  = ( float ) The speed at which the queen bee
                    moves in the search space

                |\n

                ~ iSamples_Worker   = ( int ) The number of samples a worker
                    bee should collect in a region before returning to the hive

                ~ fRequiredFitness_WorkerDistractionStart   = ( float ) The
                    required minimum fitness of a candidate for a worker bee to
                    become distracted from its current task

                ~ iSamples_WorkerDistraction    = ( int ) A semi-random number
                    of how many samples a worker should take when distracted
                    before resuming its original task

                ~ fRequiredFitness_WorkderDistractionTot    = ( float ) The 
                    total fitness of the distraction region that is required
                    for the distraction to be useful

                |\n

                ~ fRatio_ScoutReturn    = ( float ) The ratio of worker bees
                    that need to have returned before the scout bees are 
                    signalled ot return

                ~ fRequiredFitness_Scout    = ( float ) The minimum viable
                    fitness of a candidate that is required for a scout to
                    return to the hive before being signalled to do so
        """

        #   STEP 0: Local variables
        #   STEP 1: Setup - Local variables

        #   STEP 2: Check if not initialized
        if (self.__bBeeState[3] != True):
            #   STEP 3: Check if should be initialized
            if ((self.__bBeeState[0]) and (self.__bBeeState[1]) and (self.__bBeeState[2])):
                #   STEP 4: Set init flag
                self.__bBeeState[3] = True

                #   STEP 5: Energize
                self.__initBee__()

            else:
                #   STEP 6: Error handling
                raise Exception("An error occured in SwarmChan.bee() -> Step 3: Bee-Colony required paramaters not initialized")

        #   STEP 7: Perform evaluator actions
        self.__beeEvaluators__()

        #   STEP 10: Perform Queen bee actions
        self.__beeQueen__()

        #   STEP 8: Perform worker bee actions
        self.__beeWorkers__()

        #   STEP 9: Perform scout bee actions
        self.__beeScouts__()

        #   STEP ??: Return
        return

    #       region Front-End-(Bee-Colony-Optimization): Init

    def initBeePositions(self, **kwargs) -> None:
        """
            Description:

                Initializes the starting positions for the Bee-Colony-Optimization
                algorithm.

            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:

                + positions = ( list ) List of starting information positions
                    ~ Required
        """

        #   STEP 0: Local variables
        #   STEP 1: Setup - Local variables

        #   STEP 2: Check if swarm type is uninitialized
        if (self.__data[0] == None):
            #   STEP 3: Init swarm to be of type Bee-Colony
            self.__setSwarmType__(type=sw.BEE)

        #   STEP 4: Swarm type is initialized - check if type is Bee-Colony
        elif (self.__data[0] != sw.BEE):
            #   STEP 5: Error handling
            raise Exception("An error occured in SwarmChan.initBeePositions() -> Step 4: Incorrect swarm type")

        #   STEP 6: Check if positions passed
        if ("positions" not in kwargs):
            #   STEP 7: Error handling
            raise Exception("An error occured in SwarmChan.initBeePositions() -> Step 6: No positions argument passed")

        #   STEP 8: Check if starting fitnesses initialized
        if ("starting fitnesses" in self.__data[1]):
            #   STEP 9: Check that the length of the fitness list corresponds to the lenght of the position list
            if (len(kwargs["positions"]) != len(self.__data[1]["starting fitnesses"])):
                #   STEP 10: Error handling
                raise Exception("An error occured in SwarmChan.initBeePositions() -> Step 9: Position list length doesn't match fitness list length")

        #   STEP 11: Set starting to positions
        self.__data[1]["starting positions"] = kwargs["positions"]

        #   STEP 12: Set init flag
        self.__bBeeState[0] = True

        #   STEP 13: Return
        return

    def initBeeFitness(self, **kwargs) -> None:
        """
            Description:

                Initializes the starting fitnesses for the Bee-Colony-Optimization
                algorithm.

            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:

                + fitness   = ( list ) The fitnesses of the starting positions
                    ~ Required
        """

        #   STEP 0: Local variables
        #   STEP 1: Setup - Local variables

        #   STEP 2: Check if swarm type is unintialized
        if (self.__data[0] == None):
            #   STEP 3: Init swarm to be of type Bee-Colony
            self.__setSwarmType__(type=sw.BEE)

        #   STEP 4: Swarm type is initialized - check if type is Bee-Colony
        elif (self.__data[0] != sw.BEE):
            #   STEP 5: Error handling
            raise Exception("An error occured in SwarmChan.initBeeFitness() -> Step 4: Incorrect swarm type")

        #   STEP 6: Check if fitness arg passed
        if ("fitness" not in kwargs):
            #   STEP 7: Error handling
            raise Exception("An error occured in SwarmChan.initBeeFitness() -> Step 6: No fitness argument passed")

        #   STEP 8: Check if starting positions initialized
        if ("starting positions" in self.__data[1]):
            #   STEP 9: Check that length of position list corresponds to length of fitness list
            if (len(kwargs["fitness"]) != len(self.__data[1]["starting positions"])):
                #   STEP 10: Error handling
                raise Exception("An error occured in SwarmChan.initBeeFitness() -> Step 9: Fitness length doesn't match position list length")

        #   STEP 11: Set starting fitnesses
        self.__data[1]["starting fitnesses"] = kwargs["fitness"]

        #   STEP 12: Set init flag
        self.__bBeeState[1] = True

        #   STEP 13: Return
        return

    def initBeeParams(self, **kwargs) -> None:
        """
            Description:

                Saves the swarms parameters until the point that they are used
                during the initialization of the Bee-Colon-Optimization 
                algorithm.

            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:

                + params    = ( dict ) A dictionary containing the parameters
                    for the algorithm
                    ~ Required
        """

        #   STEP 0: Local variables
        #   STEP 1: Setup - Local variables

        #   STEP 2: Check if swarm type is uninitialized
        if (self.__data[0] == None):
            #   STEP 3: Init swarm to be of type Bee-Colony
            self.__setSwarmType__(type=sw.BEE)

        #   STEP 4: Swarm type is initialized - check if type is Bee-Colony
        elif (self.__data[0] != sw.BEE):
            #   STEP 5: Error handling
            raise Exception("An error occured in SwarmChan.initBeeParams() -> Step 4: Incorrect swarm type")

        #   STEP 6: Check if params arg passed
        if ("params" not in kwargs):
            #   STEP 7: Error handling
            raise Exception("An error occured in SwarmChan.initBeeParams() -> Step 6: No pamars argument passed")

        #   STEP 8: Set parameters
        self.__data[1]["parameters"] = kwargs["params"]

        #   STPE 9: Set init flag
        self.__bBeeState[2] = True

        #   STEP 10: Return
        return

    #
    #       endregion

    #
    #   endregion

    #
    #endregion

    #region Back-End

    #   region Back-End: Sets

    def __setSwarmType__(self, **kwargs) -> None:
        """
            Description:

                Sets the type of swarm for this instance. Required for more 
                complicated algorithms.

            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:

                + type  = ( enum ) The type of swarm
                    ~ Required
        """

        #   STEP 0: Local variables
        #   STEP 1: Setup - Local variables

        #   STEP 2: Check if type arg was passed
        if ("type" not in kwargs):
            #   STEP 3: Error handling
            raise Exception("An error occured in SwarmChan.__setSwarmType__() -> Step 2: No type argument passed")

        #   STEP 4: Check if passed type is swarm enum
        if (sw.isEnum(kwargs["type"]) == False):
            #   STEP 5: Error handling
            raise Exception("An error occured in SwarmChan.__setSwarmType__() -> Step 4: Invalid enum passed")

        #   STEP 6: Set class swarm type
        self.__data[0] = kwargs["type"]

        #   STEP 7: Check if BCO
        if (kwargs["type"] == sw.BEE):
            #   STEP 8: Add required dictionaries for BCO
            self.__data.append({})
            self.__data.append({})

        #   STEP 7: Return
        return

    #
    #   endregion

    #   region Back-End: Inits

    def __initBee__(self) -> None:
        """
            Description:

                Initializes the Bee-Colony using the saved algorithm parameters.

            |\n
            |\n
            |\n
            |\n
            |\n

            Pseudo:
            
                generate queen
                generate workers
                generate scouts
                generate evaluators

                split workers evenly between evaluators
                split scouts evenly between evaluators

                split starting information evenly between evaluators
        """

        #   STEP 0: Local variables
        dParams                 = self.__data[1]["parameters"]

        lPositions              = self.__data[1]["starting positions"]
        lFitness                = self.__data[1]["starting fitnesses"]

        lTmp                    = None

        lWorkers                = None
        lScouts                 = None

        #   STEP 1: Setup - Local variables

        #   region STEP 2->4: Generate Queen

        #   STEP 2: Generate queen
        uQueen = UwU()

        #   STEP 3: Populate queen data
        uQueen.lCurrPosition = dParams["hive position"]

        #   STEP 4: Add queen to swarm data
        self.__data[2]["queen"] = uQueen

        #
        #   endregion

        #   region STEP 5->11: Generate workers

        #   STEP 5: Set temp vars
        lTmp    = []

        #   STEP 6: Iterate through num workers
        for _ in range(0, dParams["num workers"]):
            #   STEP 7: Create new worker
            uWorker = UwU()

            #   STEP 8: Set worker starting position
            uWorker.lCurrPosition = dParams["hive position"]

            #   STEP 9: Add requried worker data
            uWorker.data["evaluator"]   = None

            uWorker.data["state"]       = "reporting"

            uWorker.data["destination"] = None

            uWorker.data["distraction threshold"] = dParams["worker"]["disctraction threshold"] + rn.random() * dParams["worker"]["disctraction offset"] * 2.0 - dParams["worker"]["distraction offset"]

            uWorker.data["memRoute"]    = {
                "items":        0,
                "positions":    [],
                "fitness":      [],
            }

            uWorker.data["memRegion"]   = {
                "items":        0,
                "positions":    [],
                "fitness":      []
            }

            uWorker.data["memDistraction"] = {
                "items":        0,
                "positions":    [],
                "fitness":      []
            }

            #   STEP 10: Append to worker list
            lTmp.append(uWorker)

        #   STEP 11: Add workers to swarm data
        self.__data[2]["workers"] = lTmp

        lWorkers = self.__data[2]["workers"]

        #
        #   endregion

        #   region STEP 12->18: Generate scouts

        #   STEP 12: Set tmp variables
        lTmp    = []

        #   STEP 13: Iterate through required scouts
        for _ in range(0, dParams["num scouts"]):
            #   STEP 14: Create new scout
            uScout = UwU()

            #   STEP 15: Set scout starting position
            uScout.lCurrPosition = dParams["hive position"]

            #   STEP 16: Add required scout data
            uScout.data["evaluator"]    = None

            uScout.data["state"]        = "reporting"

            uScout.data["destination"]  = None

            uScout.data["mem"]          = {
                "items":        0,
                "positions":    [],
                "fitness":      []
            }

            #   STEP 17: Append to scout list
            lTmp.append(uScout)

        #   STEP 18: Add scout to swarm data
        self.__data[2]["scouts"] = lTmp
        lScouts = self.__data[2]["scouts"]

        #
        #   endregion

        #   region STEP 19->25: Generate evaluators

        #   STEP 19: Set tmp variable
        lTmp    = []

        #   STEP 20: Iterate through required evaluators
        for _ in range(0, dParams["num evals"]):
            #   STEP 21: Create new evaluator
            uEval = UwU()

            #   STEP 22: Set evaluator starting position
            uEval.lCurrPosition = dParams["hive position"]

            #   STEP 23: Add required eval data
            uEval.data["workers"]       = []

            uEval.data["scouts"]        = []

            uEval.data["memory"]        = {
                "items":        0,
                "positions":    [],
                "fitness":      [],
                "age":          []
            }

            uEval.data["state"]         = "starting"

            uEval.data["destination"]   = None

            uEval.data["mem scout"]     = {
                "itmes":        0,
                "positions":    [],
                "fitness":      [],
            }

            uEval.data["best"]          = {
                "position": None,
                "fitness":  None
            }

            #   STEP 24: Append to evaluator list
            lTmp.append(uEval)

        #   STEP 25: Add evaluator list to swarm data
        self.__data[2]["evaluators"] = lTmp

        #
        #   endregion

        #   region STEP 26->32: Split workers between evaluators

        #   STEP 26: Get max workers per evaluator
        iMaxWorkers = int( 1.1 * dParams["num workers"] / dParams["num evals"] )
        
        #   STEP 27: Iterate through workers
        for i in range(0, dParams["num workers"]):
            #   STEP 28: While true
            while (True):
                #   STEP 29: Pick a random evaluator
                iIndex = rn.randint(0, dParams["num evals"] - 1)

                #   STEP 30: Check that that eval doesn't have too many workers already
                if (len(lTmp[iIndex].data["workers"]) < iMaxWorkers):
                    #   STEP 31: Add connection data
                    lTmp[iIndex].data["workers"].append(i)
                    lWorkers[i].data["evaluator"] = iIndex

                    #   STEP 32: Exit while loop
                    break

        #
        #   endregion

        #   region STEP 33->39:Split scouts between evaluators

        #   STEP 33: Get max scouts per evaluator
        iMaxScouts = int( 1.2 * dParams["num scouts"] / dParams["num evals"] )

        #   STEP 34: Iterate through scouts
        for i in range(0, dParams["num scouts"]):
            #   STEP 35: While loop
            while (True):
                #   STEP 36: Pick a random evaluator
                iIndex = rn.randint(0, dParams["num evals"] - 1)

                #   STEP 37: Check that that eval doesn't have too many scouts already
                if (len(lTmp[iIndex].data["scouts"]) < iMaxScouts):
                    #   STEP 38: Add connection data
                    lTmp[iIndex].data["scouts"].append(i)
                    lScouts[i].data["evaluator"] = iIndex

                    #   STEP 39: Exit while loop
                    break

        #
        #   endregion

        #   region STEP 40->45: Split data between evaluators

        #   STEP 40: Get max info per evaluator
        iMaxInfo = int( 1.2 * len(lPositions) / dParams["num evals"] )

        #   STEP 41: Iterate through info
        for i in range(0, len(lPositions)):
            #   STEP 42: While loop
            while (True):
                #   STEP 43: Pick a random evaluator
                iIndex = rn.randint(0, dParams["num evals"] - 1)

                #   STEP 44: Check that that eval doesn't have too much info already
                if (lTmp[iIndex].data["memory"]["items"] < iMaxInfo):
                    #   STEP 44: Add data
                    dMem = lTmp[iIndex].data["memory"]

                    dMem["positions"].append(lPositions[i])
                    dMem["fitness"].append(lFitness[i])
                    dMem["age"].append(0)

                    dMem["items"] += 1

                    #   STEP 45: Exit while loop
                    break

        #
        #   endregion

        #   STEP 46: Return
        return
        
    #
    #   endregion

    #   region Back-End: Bee-Colony-Optimization

    #       region Back-End-(Bee-Colony-Optimization): Sets

    def __setBeeWorkerDest__(self, **kwargs) -> None:
        """
        """

        #   STEP 0: Local variables
        #   STEP 1: Setup - Local variables

        #   STEP 2: ??

        #   STEP ??: Return
        return

    def __setBeeScoutDest__(self, **kwargs) -> None:
        """
        """

        #   STEP 0: Local variables
        #   STEP 1: Setup - Local variables

        #   STEP 2: ??

        #   STEP ??: Return
        return

    def __setBeeEvalDest__(self) -> None:
        """
        """

        #   STEP 0: Local variables
        #   STEP 1: Setup - Local variables

        #   STEP 2: ??

        #   STEP ??: Return
        return

    #
    #       endregion

    #       region Back-End-(Bee-Colony-Optimization): Gets

    def __getBeeEvalMem__(self, **kwargs) -> None:
        """
        """

        #   STEP 0: Local variables
        #   STEP 1: Setup - Local variables

        #   STEP 2: ??

        #   STEP ??: Return
        return

    def __getBeeEmployeeState__(self, **kwargs) -> bool:
        """
            Description:

                Returns true if all the employees of the specified evaluator
                bee are currently in a "reporting" state.

            |\n
            |\n
            |\n
            |\n
            |\n

            Arguments:

                + evaluator = ( int ) The index of the evaluator whoese
                    employees should be checked
                    ~ Required

            |\n

            Returns:

                + bPresent  = ( bool ) A flag that represents whether or not
                    all this evalutor's employees are currently in a 
                    "reporting" state.
        """

        #   STEP 0: Local variables
        lWorkers                = None
        lScouts                 = None

        uEval                   = None

        #   STEP 1: Setup - Local variables

        #   STEP 2: Check if evaluator arg passed
        if ("evaluator" not in kwargs):
            #   STEP 3: Error handling
            raise Exception("An error occured in SwarmChan.__getBeeEmployeeState__() -> Step 2: No evaluator argument passed")

        else:
            #   STEP 4: Init local vars
            lWorkers    = self.__data[2]["workers"]
            lScouts     = self.__data[2]["scouts"]

            uEval       = self.__data[2]["evaluators"][kwargs["evaluator"]]

        #   STEP 5: Iterate through evaluator's worker bees
        for i in range(0, len(uEval.data["workers"])):
            #   STEP 6: Get worker index
            iWorker = uEval.data["workers"][i]

            #   STEP 7: Check if worker is reporting
            if (lWorkers[iWorker].data["state"] != "reporting"):
                #   STEP 8: Return
                return False

        #   STEP 9: Iterate through evaluator's scout bees
        for i in range(0, len(uEval.data["scouts"])):
            #   STEP 10: Get scout index
            iScout = uEval.data["scouts"][i]

            #   STEP 11: Check if scout is not reporting
            if (lScouts[iScout].data["state"] != "reporting"):
                #   STEP 12: Retur of the jedi
                return False

        #   STEP 13: Return of more jedii
        return True

    #
    #       endregion

    #       region Back-End-(Bee-Colony-Optimization): Moves

    def __moveBeeEval__(self, **kwargs) -> None:
        """
        """

        #   STEP 0: Local variables
        #   STEP 1: Setup - Local variables

        #   STEP 2: ??

        #   STEP ??: Return
        return

    def __moveBeeQueen__(self) -> None:
        """
        """

        #   STEP 0: Local variables
        #   STEP 1: Setup - Local variables

        #   STEP 2: ??

        #   STEP ??: Return
        return

    def __moveBeeScout__(self, **kwargs) -> None:
        """
        """

        #   STEP 0: Local variables
        #   STEP 1: Setup - Local variables

        #   STEP 2: ??

        #   STEP ??: Return
        return

    def __moveBeeWorker__(self, **kwargs) -> None:
        """
        """

        #   STEP 0: Local variables
        #   STEP 1: Setup - Local variables

        #   STEP 2: ??

        #   STEP ??: Return
        return

    #
    #       endregion
    
    #       region Back-End-(Bee-Colony-Optimization): Bees

    def __beeEvaluators__(self) -> None:
        """
            Description:

                Peforms the actions of the evaluator bees for this iteration.

            |\n
            |\n
            |\n
            |\n
            |\n

            Pseudo:

                for all evaluators
                    if evaluator at hive
                        if all employees reporting 
                            mem = get data from employees

                        elif starting
                            mem = self.mem

                        else
                            continue

                        mem best = choose best data from mem
                            if employee distraction data is bad lower distraction threshold for all
                            workers

                        split workers between mem best regions

                        get random point in respective region for each worker
                            reset   worker.memroute
                                worker.memRegion
                                worker.memDistraction

                            set worker.destination
                                worker.state

                        decide on new region for each scout

                        reset scout.mem

                        set scout.state
                            scout.destination

                        save best data

                    else
                        if all employees reporting
                            return to hive

                        else
                            scout self.destination
                            save fitness to self.mem scout                            
        """

        #   STEP 0: Local variables
        lEvaluators             = self.__data[2]["evaluators"]
        
        bPresent                = None

        #   STEP 1: Setup - Local variables

        #   STEP 2: Iterate through evaluators
        for i in range(0, len(lEvaluators)):
            #   STEP 3: Get current evaluator
            uEval = lEvaluators[i]

            #   STEP 4: Check if evaluator at hive
            if ((uEval.data["state"] == "starting") or (uEval.data["state"] == "waiting")):
                #   STEP 5: Set tmp variable
                bPresent = True

                #   STEP 6: Check if waiting
                if (uEval.data["state"] == "waiting"):
                    #   STEP 7: Get employee states
                    bPresent = self.__getBeeEmployeeState__(evaluator=i)

                #   STEP 8: Check if all employees are present
                if (bPresent == True):
                    #   STEP 9: Get evaluator memory
                    self.__getBeeEvalMem__(evaluator=i)

                    #   STEP 10: Set worker destinations
                    self.__setBeeWorkerDest__(evaluator=i)

                    #   STEP 11: Set scout destinations
                    self.__setBeeScoutDest__(evaluator=i)

                else:
                    #   STEP 12: All employees not present, skip this evaluator for now
                    continue

            else:
                #   STEP 13: Check if all employees reporting
                if (self.__getBeeEmployeeState__(evaluator=i) == True):
                    #   STEP 14: Return to base
                    self.__moveBeeEval__(destination="base")
                    
                else:
                    #   STEP 15: Continue scouting
                    self.__moveBeeEval__(destination="scout")

        #   STEP 16: Return
        return

    def __beeQueen__(self) -> None:
        """
            Description:

                Performs the actions of the queen bee for this iteration.

            |\n
            |\n
            |\n
            |\n
            |\n

            Pseudo:

                if evaluators as scouts
                    for all evaluators
                        if evaluator waiting
                            best mem = update mem
                            decide on region near hive to search

                            reset eval.mem scout
                            set eval.state
                                eval.destination

                if birth death
                    if birth
                        generate P new bees
                        assign bees to respective positions

                    if death
                        remove P bees

                if hive movement
                    if good food source far from hive and not moving atm
                        pos = new position that would be better for collecting food

                    elif moving atm
                        moveBeeQueen
        """

        #   STEP 0: Local variables
        dParams                 = self.__data[1]["parameters"]

        #   STEP 1: Setup - Local variables

        #   STEP 2: Check if evaluators need to move
        if (dParams["evals as scouts"] == True):
            #   STEP 3: Outsource eval movement
            self.__setBeeEvalDest__()

        #   STEP 4: Check if birth death process
        if (dParams["birth death"] == True):
            #   STEP 5: Outsource birth death
            self.__beeBirthDeath__()

        #   STEP 6: Check if hive movement
        if (dParams["hive movement"] == True):
            #   STEP 7: Outsource hive movement
            self.__moveBeeQueen__()

        #   STEP 8: Return
        return

    def __beeScouts__(self) -> None:
        """
            Description:

                Performs the actions of the scout bee for this iteration of the
                algorithm.

            |\n
            |\n
            |\n
            |\n
            |\n

            Pseudo:

                for all scouts
                    if scout not reporting
                        __moveBeeScout__(scout)
        """

        #   STEP 0: Local variables
        lScouts                 = self.__data[2]["scouts"]

        #   STEP 1: Setup - Local variables

        #   STEP 2: Iterate through scouts
        for i in range(0, len(lScouts)):
            #   STEP 3: Check that scout not reporting
            if (lScouts[i].data["state"] != "reporting"):
                #   STEP 4: Move scout
                self.__moveBeeScout__(scout=i)

        #   STEP 5: Return
        return

    def __beeWorkers__(self) -> None:
        """
            Description:

                Performs the actions of the worker bee for this iteration.

            |\n
            |\n
            |\n
            |\n
            |\n

            Pseudo:

                for all workers
                    if worker is moving
                        __moveBeeWorker__(worker)
        """

        #   STEP 0: Local variables
        lWorkers                = self.__data[2]["workers"]

        #   STEP 1: Setup - Local variables

        #   STEP 2: Iterate through worker
        for i in range(0, len(lWorkers)):
            #   STEP 3: If worker not reporting
            if (lWorkers[i].data["state"] != "reporting"):
                #   STEP 4: Move worker bee
                self.__moveBeeWorker__(worker=i)

        #   STEP ??: Return
        return

    #
    #       endregion

    #       region Back-End-(Bee-Colony-Optimization): Other

    def __beeBirthDeath__(self) -> None:
        """
        """

        #   STEP 0: Local variables
        #   STEP 1: Setup - Local variables

        #   STEP 2: ??

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

#   region Testing

if (__name__ == "__main__"):
    Helga.nop()

#
#   endregion