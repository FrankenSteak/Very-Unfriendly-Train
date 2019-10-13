
	def __propagateBackward__(self, _lfExpectedOutput: list) -> None:
		"""
		"""
		
		#	STEP 0: local variables
		lNodeSig				= None
		lNodeErr				= None
		lWeightErr				= None

		lTmpError				= None

		#	STEP 1: Setup - Local variables
		lNodeSig 	= self.__getShape_Nodes()
		lNodeErr 	= self.__getShape_Nodes()
		lWeightErr 	= self.__getShape_Weights()

		lTmpError	= self.getError(_lfExpectedOutput)

		#	STEP 2: Get sigmas for all node layers - iterate through layers
		lNodeSig    = self.__pbSigma__(lNodeSig)

		#	STEP 3: Get node errors
		lNodeErr    = self.__pbNodeError__(lTmpError, lNodeSig, lNodeErr)

		#	STEP 4: Get weight errors
		lWeightErr  = self.__pbWeightError__(lNodeSig, lNodeErr, lWeightErr)

		#	STEP 5: Update weights
		self.__pbUpdateWeights__(lWeightErr)

		#	STEP 6: Return
		return

	#		region Back-End-(Default): Back-Propagation

	def __pbSigma__(self, _lNodeSig: list) -> list:
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
                if ((self.bUseDropout) and (self.__lDropOut[i][j] == True)):
                    #   STEP 10: Set as dropout node
                    _lNodeSig[i][j] = 0.0

                #   STEP 11: Not dropout
                else:
                    #	STEP 12: Get pre-activation value
                    fTmp_preActivation	= self.__lNodes_PreActivation[i][j]

                    #	STEP 13: Get normal activation function
                    _lNodeSig[i][j]	= self.__acFunctions.getActivationD(self.__iAcFunction, fTmp_preActivation)

		#	STEP 14: Return
		return _lNodeSig

	def __pbNodeError__(self, _lError: list, _lNodeSig: list, _lNodeErr: list) -> list:
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
				if ((self.__bUseBias) and (i <= iLastRow - 2)):
					#	STEP 5: Adjust iterations
					iIterations -= 1

			#	STEP 6: Iterate through the nodes in the layer
			for j in range(0, len(_lNodeErr[i])):
				#	STEP 7: Check if currently on last row
				if (i == iLastRow):
					#	STEP 8: Set error for the node -> dE/da = -E
					_lNodeErr[i][j] = -1.0 * _lError[j]

                #   STPE 9: Check - Dropout status
				elif ((self.bUseDropout) and (self.__lDropOut[i][j] == True)):
                    #   STEP 10: Set as dropout node
                    _lNodeErr[i][j] = 0.0

                #   STEP 11: Not dropout
                else:
					#	STEP 12: Reset temp vars
					fTmp	= 0.0

					#	STEP 13: Iterate through the layer above thisone
					for k in range(0, iIterations):
						#	STEP 14: Sum the error from iterable node to current node
						fTmp = fTmp + self.__lWeights[i][j * iTmpLen + k] * _lNodeSig[i + 1][k] * _lNodeErr[i + 1][k]

					#	STEP 15: Set current node error
					_lNodeErr[i][j] = fTmp

		#	STEP 16: Return
		return _lNodeErr

	def __pbWeightError__(self, _lNodeSig: list, _lNodeErr: list, _lWeightErr: list) -> list:
		"""
		"""

		#	STEP 0: local variables

		#	STEP 1: Setup - Local variables

		#	STEP 2: Iterate through weight layers
		for i in range(0, len(_lWeightErr)):
			#	STEP 3: Get length of node layer
			iTmpLen     = len(_lNodeErr[i + 1])
			iIterations	= iTmpLen
			
			if ((self.__bUseBias) and (i < len(_lWeightErr) - 1)):
				iIterations -= 1

			#	STEP 4: Iterate through nodes in layer
			for j in range(0, len(_lNodeErr[i])):
				#	STEP 5: Iterate through attached weights
				for k in range(0, iIterations):
					#	STEP 6: Set the weight error
					_lWeightErr[i][j * iTmpLen + k] = round(self.__lNodes[i][j] * _lNodeSig[i+1][k] * _lNodeErr[i+1][k], 6)

		#	STEP 7: Return
		return _lWeightErr

	def __pbUpdateWeights__(self, _lWeightErr: list) -> None:
		"""
		"""

		#	STEP 0: Local variables
        
		#	STEP 1: Setup - Local variables

		#	STEP 2: Check if momentum should be taken into account
		if (self.__bMomentumActive):
			#	STEP 3: Iterate through weight layers
			for i in range(0, len(_lWeightErr)):
				#	STEP 4: Iterate through weights in layer
				for j in range(0, len(_lWeightErr[i])):
					if (_lWeightErr[i][j] != 0):
						#	STEP 5: Calculate delta = -learning * error + momentum * previous weights
						fDelta = -1.0 * self.__fLearningRate * _lWeightErr[i][j] + self.__fMomentum * self.__lWeights_Momentum[i][j]

						#	STEP 6: Set new weight
						self.__lWeights[i][j] = round(self.__lWeights[i][j] + fDelta, 6)
			
			#	STEP 7: Save momentum weight
			self.__lWeights_Momentum = cp.copy(self.__lWeights)

		#	STEP 8: No momentum
		else:
			#	STEP 9: Iterate through weight layers
			for i in range(0, len(_lWeightErr)):
				#	STEP 10: Iterate through weights in layer
				for j in range(0, len(_lWeightErr[i])):
					#	STEP 11: Calculate delta = -error
					fDelta = -1.0 * _lWeightErr[i][j]

					#	STEP 12: Save new weight
					self.__lWeights[i][j] = round(self.__lWeights[i][j] + fDelta, 6)

		#	STEP 13: Return
		return

	#
	#		endregion
