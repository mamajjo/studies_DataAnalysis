from app.configuration.config import Config
import numpy
import statistics
from collections import Counter

class Data(object):
    def __init__(self, dataset, cfg:Config):
        self.datasetName = cfg.dataSourceUrl[7:-4]
        self.dataset = dataset
        self.hasQualitativeFeatures = cfg.hasQualitativeFeatures
        if self.hasQualitativeFeatures:
            if cfg.numberedFirstColumn > 0:
                self.fQualitativeColumn = 0
                self.lQualitativeColumn = cfg.numberedFirstColumn
            elif cfg.numberedFirstColumn == 0:
                self.fQualitativeColumn = cfg.numberedLastColumn+1
                self.lQualitativeColumn = dataset.shape[1]
            self.fQuantitativeColumn = cfg.numberedFirstColumn
            self.lQuantitativeColumn = cfg.numberedLastColumn+1
            self.QualitativeColumns = self.dataset.columns.values[self.fQualitativeColumn:self.lQualitativeColumn]
            print(self.QualitativeColumns)
        else:
            self.fQuantitativeColumn = cfg.numberedFirstColumn
            self.lQuantitativeColumn = cfg.numberedLastColumn + 1
        self.QuantitiveColumns = self.dataset.columns.values[self.fQuantitativeColumn:self.lQuantitativeColumn]
        print(self.QuantitiveColumns)
        self.classColumn = cfg.classColumn
    
    def __str__(self):
        if self.hasQualitativeFeatures:
            return f"Choosen data set is {self.datasetName} and quntitative cells are: {self.fQuantitativeColumn} : {self.lQuantitativeColumn} and Qualitative cells are: {self.fQualitativeColumn} : {self.lQualitativeColumn}"
        else:
            return f"Choosen data set is {self.datasetName} and quntitative cells are: {self.fQuantitativeColumn} : {self.lQuantitativeColumn}"
    
    def printQuantitativeColumns(self):
        print(f"--------QUANTITATIVE COLUMNS OF {self.datasetName} --------")
        columnsLabels = self.dataset.columns.values
        for columnLabel in columnsLabels:
            if isinstance(self.dataset[columnLabel][0],  numpy.float64) or isinstance(self.dataset[columnLabel][0], numpy.int64) or isinstance(self.dataset[columnLabel][0], numpy.int32):
                print(columnLabel)
                print(self.dataset[columnLabel])

    def printQualitativeColumns(self):
        print(f"--------Qualitative COLUMNS OF {self.datasetName} --------")
        if self.hasQualitativeFeatures:
            columnsLabels = self.dataset.columns.values
            for columnLabel in columnsLabels:
                if isinstance(self.dataset[columnLabel][0],  str):
                    print(columnLabel)
                    print(self.dataset[columnLabel])
        else:
            print("No Qualitative columns")

    def getMedians(self):
        dict = {}
        for quantitativeLabel in self.QuantitiveColumns:
            dict[quantitativeLabel] = statistics.median(self.dataset[quantitativeLabel])
        return dict

    def getMaximum(self):
        dict = {}
        for quantitativeLabel in self.QuantitiveColumns:
            dict[quantitativeLabel] = max(self.dataset[quantitativeLabel])
        return dict

    def getMinimum(self):
        dict = {}
        for quantitativeLabel in self.QuantitiveColumns:
            dict[quantitativeLabel] = min(self.dataset[quantitativeLabel])
        return dict

    def getDominant(self):
        if self.hasQualitativeFeatures:
            dict = {}
            for label in self.QualitativeColumns:
                dict[label] = Counter(self.dataset[label]).most_common(1)
            return dict
        else:
            return "No Qualitative columns"