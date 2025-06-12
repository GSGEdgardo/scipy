#  Copyright (c) 2025.  Departamento de Ingenieria de Sistemas y Computacion
import logging

import pandas as pd
from matplotlib import pyplot as plt
from prophet import Prophet

from benchmark import benchmark
from logger import configure_logging


def main():
    log = logging.getLogger(__name__)
    log.info("Starting ...")
    log.info("Done.")

    # Load the data
    df = pd.read_csv(
        "https://raw.githubusercontent.com/facebook/prophet/main/examples/example_wp_log_peyton_manning.csv"
    )

    log.debug(f"DataFrame shape: {df.shape}")
    log.debug(f"Data: \n{df.head()}")

    # the model
    model = Prophet(
        changepoints=["2011-01-01", "2013-01-01"],
    )
    with benchmark("Fitting Prophet model", log):
        model.fit(df)

    # Create the future dataframe
    future = model.make_future_dataframe(periods=365)

    #predict the future
    forecast = model.predict(future)
    model.plot(forecast)

    model.plot_components(forecast)
    plt.show()

    plt.show()

if __name__ == "__main__":
    configure_logging(log_level="DEBUG")
    main()