import pandas
from pathlib import Path
from pandas import read_csv

def readcsv_fromFile(filePath):
    dataPath = Path(filePath)
    return read_csv(dataPath)