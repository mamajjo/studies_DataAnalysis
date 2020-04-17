import numpy as np
from math import sqrt
from app.configuration.config import config
from app.io.fileReader import readcsv_fromFile
from app.dataobject.dataobject import Data
import matplotlib.pyplot as plot
from scipy import stats
import yaml

class App():
    def run(self):
        dataset = readcsv_fromFile(config.dataSourceUrl)
        CurrentDataSet = Data(dataset, config)
        print("-----Medians for quantitative features----")
        print(yaml.dump(CurrentDataSet.getMedians(), default_flow_style=False))
        print("-----Maximum for quantitative features----")
        print(yaml.dump(CurrentDataSet.getMaximum(), default_flow_style=False))
        print("-----Minimum for quantitative features----")
        print(yaml.dump(CurrentDataSet.getMinimum(), default_flow_style=False))
        print("-----Dominant for qualitative features----")
        print(CurrentDataSet.getDominant())

        print("-----Correlation matrix for quantitative features----")
        print(CurrentDataSet.dataset[CurrentDataSet.QuantitiveColumns].corr())
        corr_matrix = CurrentDataSet.dataset[CurrentDataSet.QuantitiveColumns].corr().abs()
        bestCorr = (corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(np.bool))
                 .stack()
                 .sort_values(ascending=False))
        bestCorrStr = str(bestCorr.head(1))
        a = bestCorrStr.split(" ")
        firstCorrelationColumn = a[0]
        secondCorrelationColumn = a[2]

        plot.subplot(1,2,1)
        plot.hist(CurrentDataSet.dataset[firstCorrelationColumn], bins=20, label=firstCorrelationColumn)
        plot.title(firstCorrelationColumn)
        plot.ylabel("Liczba wystąpień")
        plot.xlabel(firstCorrelationColumn)
        plot.subplot(1,2,2)
        plot.hist(CurrentDataSet.dataset[secondCorrelationColumn], bins=20, label=secondCorrelationColumn)
        plot.title(secondCorrelationColumn)
        plot.ylabel("Liczba wystąpień")
        plot.xlabel(secondCorrelationColumn)
        plot.tight_layout()
        plot.show()

        input("press enter to continue")
        if config.dataSourceUrl == "./data/quakes.csv":
            hypothesis = 300
            alpha = 0.05
            meanD = np.average(CurrentDataSet.dataset["depth"])
            print("Średnia obliczona ze wszystkich głębokości wystąpienia: " + str(meanD))
            stdD = np.std(CurrentDataSet.dataset["depth"])
            print("Odchylenie standardowe głebokości wystąpienia: " + str(stdD))
            t = stats.t.ppf(1 - alpha/2, CurrentDataSet.dataset["depth"].count()-1)
            print(f"Wartość krytyczna zbioru quakes w kolumnie depth: {t}")
            left_crit_boundary = meanD + t*stdD/(sqrt(CurrentDataSet.dataset["depth"].count()))
            right_crit_boundary = meanD - t*stdD/(sqrt(CurrentDataSet.dataset["depth"].count()))
            print(left_crit_boundary)
            print(right_crit_boundary)
            if hypothesis > right_crit_boundary and hypothesis < left_crit_boundary:
                print("Hipoteza potwierdzona")
            else:
                print("hipotera zostaje odrzucona")
            fig = plot.figure()
            ax = fig.add_subplot(1,1,1)
            ax.set_title("depth histogram")
            CurrentDataSet.dataset.hist(column=["depth"], ax=ax)
            plot.axvline(x=right_crit_boundary, linestyle='--', color='orange')
            plot.axvline(x=left_crit_boundary, linestyle='--', color='orange')
            lin = plot.axvline(x=hypothesis, linestyle='--', color='black')
            plot.show()
            
        



if __name__ == "__main__":
    App().run()