import multiprocessing  as mp
import queue            as qu
import sys


def x(eUI):

    print("x1")
    if (eUI.is_set() == False):
        eUI.wait()

    print("bitch don't kill my vibe")

    eUI.clear()
    
    print("x2")

    return

def y(q, eGlobal, eUI, stdin):

    a = stdin.read(1)

    eGlobal.set()
    eUI.set()

    q.put(a)

    return


if (__name__ == "__main__"):

    eGlobal = mp.Event()
    eGlobal.clear()

    eUI     = mp.Event()
    eUI.clear()

    q       = mp.Queue()

    pY  = mp.Process(target=y, args=(q, eGlobal, eUI, sys.stdin))

    pY.start()

    pY.join()

    b = q.get()

    print("")
    print("")
    print("")