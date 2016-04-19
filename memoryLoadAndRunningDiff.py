import os, sys, time

def main():
  fileA = sys.argv[1]
  fileB = sys.argv[2]
  doComp(fileA, fileB)

def getValues(fileName):
  with open(fileName, "r") as f:
    lines = f.readlines()
    values = map(lambda x: int(x.split(",")[1]), lines)
    return values

def getTimestamp(fileName):
  with open(fileName, "r") as f:
    lines = f.readlines()
    return lines[-1].split(",")[0]

def getArrayAverage(array):
  runningDiff = 0.0
  for i in xrange(len(array)-1):
    runningDiff += array[i+1] - array[i]
  return runningDiff/len(array)


def doComp(fileA, fileB):
  while True:
    fileAValues = getValues(fileA)
    fileBValues = getValues(fileB)
    timestamp = getTimestamp(fileA)
    runningMemoryLoad = getArrayAverage(fileAValues)
    print "%s: Memory load: %.2f%%, Running Diff: %f" % (timestamp, (fileAValues[-1] / float(fileBValues[-1]))*100.0, (runningMemoryLoad/fileBValues[-1])*100.0)
    time.sleep(0.25)

if __name__ == "__main__":
  main()
