# Refactor ToDo
   - /config
      - Check all config files
   - /controllers/handlers/GeneticaAlgorithmsHandler.py
   - /controllers/handlers/SurrogateHandler.py
   - /controllers/handlers/SwarmHander.py
   - /controllers/optimizers/GeneticAlgorithm.py
   - /controllers/optimizers/Swarm.py
   - /controllers/surrogates/Kriging.py
   - /controllers/surrogates/SupportVectorMachine.py
   - /controllers/surrogates/Surrogates.py
      - What even does this do?
   - /helpers/SurrogateHandler.py
   - /interface/MenuInterface.py
   - /interface/UserInterface.py
   - /models/Particle.py
   - /models/DataContainer.py

# In Progress
   - /controllers/surrogates/ArtificialNeuralNetwork.py
      - /controllers/handlers/OptimizationHandler.py
      - /controllers/optimizers/Swarms.py
      - /controllers/optimizers/GeneticAlgorithms.py

# Refactoring Completed
   - /config/Config.py
   - /static/Enums.py
      - Been removed so that files` code is more centralized to those files
   - /helpers/ActivationFunctions.py
      - Ensure math functions work as expected
   - /helpers/GeneralHelpers.py
      - Renamed to `ApplicationHelper.py`
      - Expaned to `ApplicationHelper.py`,  `ArrayHelper.py`,  and `MathHelper.py`

# Optimizers
   - https://en.wikipedia.org/wiki/List_of_metaphor-based_metaheuristics