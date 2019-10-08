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
    
    print(q.get())

    q.put(["u a hoe"])

    return


if (__name__ == "__main__"):

    while (True):
        a = sys.stdin.read(1)
        print(a)
        
    eGlobal = mp.Event()
    eGlobal.clear()

    eUI     = mp.Event()
    eUI.clear()

    q       = mp.Queue()
    q.put(["sup bitch"])

    pY  = mp.Process(target=y, args=(q, eGlobal, eUI, None))

    pY.start()

    pY.join()

    b = q.get()

    print("")
    print("")
    print("")