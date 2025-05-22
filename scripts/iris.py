#  Copyright (c) 2025.  Departamento de Ingenieria de Sistemas y Computacion
import logging

import pandas as pd
from matplotlib import pyplot as plt
from pandas.plotting import scatter_matrix
from ydata_profiling import ProfileReport

from benchmark import benchmark
from logger import configure_logging


def main():
    # Configure the logging
    configure_logging(log_level=logging.DEBUG)

    # Get the logger
    log = logging.getLogger(__name__)
    log.debug("Starting main...")

    # Import data
    with benchmark(
        operation_name="read iris",
        log=log
    ):
        df = pd.read_csv('../data/iris.csv')
        log.debug(f"Data readed: \n{df}")

    log.debug(f"Describe: \n {df.describe()}")
    log.debug(f"Correlation: \n {df.corr}")
    #scatter_matrix(df[df["variety"] == "Iris-setosa"], label="Iris-setosa")
    #plt.show()

    profile = ProfileReport(df, title="Profiling Report", explorative=True)
    profile.to_file("../output/iris_report.html")

    # Finish the program
    log.debug("Done")
    pass

if __name__ == "__main__":
    main()