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
      - /helpers/ActivationFunctions.py
         - Ensure math functions work as expected
      - /helpers/GeneralHelpers.py
         - Renamed to `ApplicationHelper.py`

# Documentation
   - /config/Config.py
   - /static/Enums.py
      - Been removed so that files` code is more centralized to those files