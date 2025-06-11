#  Copyright (c) 2025.  Departamento de Ingenieria de Sistemas y Computacion
import logging
import pickle

import sys
import os
from pathlib import Path

import pandas as pd
from matplotlib import pyplot as plt

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'libs')))

import streamlit
from sklearn.ensemble import RandomForestClassifier

from logger import configure_logging

@streamlit.cache_data
def load_iris_model() -> RandomForestClassifier:
    model_path = Path(__file__).resolve().parent.parent / "output" / "iris_randomforest.pkl"
    with model_path.open("rb") as model_file:
        return pickle.load(model_file)

def main():
    log = logging.getLogger(__name__)
    log.info("Starting web service for Iris model...")

    # Load the model
    model = load_iris_model()

    # the webpage
    streamlit.title("Iris Flower Classification")
    streamlit.markdown(
        "This is a simple web service to classify Iris flowers using a Random Forest model."
    )
    streamlit.header("Iris Flower Features")
    col_1, col_2 = streamlit.columns(2)

    with col_1:
        streamlit.text("Sepal Length (cm):")
        sepal_length = streamlit.slider(
            "select sepal length",
            min_value=4.0,
            max_value=8.0,
            value=5.0,
            step=0.1,
        )
        log.debug(f"Sepal Length (cm): {sepal_length} cm")

        streamlit.text("Sepal Width (cm):")
        sepal_width = streamlit.slider(
            "select sepal width",
            min_value=4.0,
            max_value=8.0,
            value=5.0,
            step=0.1,
        )
        log.debug(f"Sepal Length (cm): {sepal_width} cm")


    with col_2:
        streamlit.text("Petal Length (cm):")
        petal_length = streamlit.slider(
            "select petal length",
            min_value=4.0,
            max_value=8.0,
            value=5.0,
            step=0.1,
        )
        log.debug(f"Petal Length (cm): {petal_length} cm")

        streamlit.text("Petal Width (cm):")
        petal_width = streamlit.slider(
            "select petal Width",
            min_value=4.0,
            max_value=8.0,
            value=5.0,
            step=0.1,
        )
        log.debug(f"Petal Width (cm): {petal_width} cm")

    features= pd.DataFrame(
        [[sepal_length, sepal_width, petal_length, petal_width]],
        columns=["sepal.length", "sepal.width", "petal.length", "petal.width"],
    )

    predict = model.predict(features)[0]
    streamlit.write(f"The predicted variety is: **{predict}**")

    # predict probabilities
    probabilities = model.predict_proba(features)[0]

    probabilities_df = pd.DataFrame(
        probabilities,
        index=model.classes_,
        columns=["Probability"]
    )

    # draw the probabilities
    plt.figure(figsize=(8, 4))

    plt.title("Predicted probabilities for iris flower varieties")
    probabilities_df.plot(kind="bar", legend=False, ax=plt.gca())
    plt.tight_layout()

    streamlit.pyplot(plt)

    log.info("Done..")

if __name__ == "__main__":
    configure_logging(log_level="DEBUG")
    main()