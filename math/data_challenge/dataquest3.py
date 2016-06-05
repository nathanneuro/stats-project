import numpy as np
import itertools
np.set_printoptions(precision=9)
import math
import timeit
import pandas as pd

# stream of numbers, last N and max N
# gonna need math.random.randint for sure (low, high+1) (1,11)
def numberStream(streamT, N, trials):
  MminusL = []

  for i in range(trials-1):
    T = np.random.randint(1,11, size = streamT)
    L = T[-2] * T[-1]
    Tsort = np.sort(T)
    M = Tsort[-2] * Tsort[-1] # sort T for largest two and multiply them
    MminusL.append(M - L)
    # if debug == True:
      # print("T", T, "L", L, "M", M, "M - L =", MminusL[i])

  return (np.mean(MminusL), np.std(MminusL, ddof=1))

def precisionLoop(streamT, N, trials, precision):
  meanList = []
  SDlist = []
  meanFinal = 0
  SDfinal = 0
  for i in range(100000):
    mean, SD = numberStream(streamT, N, trials)
    meanList.append(mean)
    SDlist.append(SD)
    if debug == True:
      print("Current M-L mean: ", mean, "SD: ", SD, "Running mean:", round(np.mean(meanList), precision), "SD:", round(np.mean(SDlist), precision), end = '\r')
    if i >= 2:
      if (round(meanList[i], precision) == round(np.mean(meanList), precision)) and (round(meanList[i], precision) == round(meanList[i-1], precision)):
        meanFinal = round(np.mean(meanList), precision)
        print("\nSuccess finding mean:", meanFinal)
      if (round(SDlist[i], precision) == round(np.mean(SDlist), precision)) and (round(SDlist[i], precision) == round(SDlist[i-1], precision)):
        SDfinal = round(np.mean(SDlist), precision)
        print("\nSuccess finding SD:", SDfinal)
    if (meanFinal != 0) and (SDfinal != 0):
      print("\nBoth mean and SD successful. Final mean:", meanFinal, "Final SD:", SDfinal)
      break
    
  return (meanFinal, SDfinal)

def main():
  streamT = 8
  N = 2
  trials = 1000
  precision = 9
  global debug
  debug = False
  mean, SD = precisionLoop(streamT, N, trials, precision)
  df = pd.DataFrame()
  df['mean'] = mean
  df['SD'] = SD
  df.to_csv('calcResults.csv')

  return


if __name__ == '__main__':
   main()

