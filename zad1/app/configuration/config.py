from pathlib import Path
from pandas import read_json

class Config(object):
    def __init__(self, dataSourceUrl, numberedFirstColumn, numberedLastColumn, testDataSize,hasQualitativeFeatures, classColumn):
        self.dataSourceUrl = dataSourceUrl
        self.numberedFirstColumn = numberedFirstColumn
        self.numberedLastColumn = numberedLastColumn
        self.testDataSize = testDataSize
        self.hasQualitativeFeatures = hasQualitativeFeatures
        self.classColumn = classColumn

def read_config(json_config):
    dataSetName = json_config['chosenDataSet'][0]
    return Config(
        dataSourceUrl=json_config[dataSetName]['dataSourceUrl'],
        numberedFirstColumn=json_config[dataSetName]['numberedFirstColumn'],
        numberedLastColumn=json_config[dataSetName]['numberedLastColumn'],
        testDataSize=json_config[dataSetName]['testDataSize']
        ,
        hasQualitativeFeatures=json_config[dataSetName]['quantityFactors'],
        classColumn=json_config[dataSetName]['classColumn']
        )

cfgJson = read_json("./configuration.json")
config = read_config(cfgJson)
        