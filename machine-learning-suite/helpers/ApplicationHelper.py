#region --- Imports ---
import  datetime        as dt
#endregion

class ApplicationHelper:
    #region --- Init ---
    """
    """

    def __init__(self):
        return
    
    #
    #endregion

    #region --- Functionality ---
    @classmethod
    def ticks(self) -> str:
        dtTmp = dt.datetime.now() - dt.datetime(1, 1, 1)
        return str(int(dtTmp.total_seconds()*10000000))

    @classmethod
    def time(self) -> str:
        return dt.datetime.now().strftime("%H:%M:%S")

    @classmethod
    def nop(self) -> None:
        return

    #
    #endregion
