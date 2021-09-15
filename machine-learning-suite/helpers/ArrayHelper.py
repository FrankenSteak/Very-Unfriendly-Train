#region --- Imports ---
import numpy as np
#endregion

class ArrayHelper:
    @classmethod
    def getShape(self, input: list) -> list:
        #   --- Variables ---
        output = []

        #   --- Functionality ---
        for i in range(0, len(input)):
            if ((type(input[i]) == float) or (type(input[i]) == int)):
                output.append(0.0)
            else:
                output.append(np.zeros(len(input[i])))

        #   --- Response ---
        return output
    
    @classmethod
    def getList(self, input: list) -> list:
        #   --- Variables ---
        output = []

        #   --- Functionality ---
        for i in range(0, len(input)):
            output.append(list(input[i]))

        #   --- Response ---
        return output

    @classmethod
    def print2DArray(self, _arrTmp: list) -> None:
        for i in range(0, len(_arrTmp)):
            for j in range(0, len(_arrTmp[i])):
                print(str(round(_arrTmp[i][j], 2)), "\t", end="")
            print("")
