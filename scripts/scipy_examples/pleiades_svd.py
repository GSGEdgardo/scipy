#  Copyright (c) 2025.  Departamento de Ingenieria de Sistemas y Computacion
import logging

from matplotlib import pyplot as plt
from scipy.linalg import svd
from skimage import io, color
from typeguard import typechecked

from logger import configure_logging


@typechecked
def main():
    configure_logging(log_level=logging.DEBUG)
    log = logging.getLogger(__name__)
    log.debug("Starting ..")

    # Load the Pleiades image
    pleiades= io.imread(
        "https://upload.wikimedia.org/wikipedia/commons/4/4e/Pleiades_large.jpg"
    )
    log.debug(f"Pleiades image loaded: {pleiades.shape}")

    pleiades_grey = color.rgb2gray(pleiades)
    log.debug(f"Pleiades image converted to grayscale: {pleiades_grey.shape}")

    u, s, vt = svd(pleiades_grey, full_matrices=False)
    log.debug(f"SVD computed: u shape {u.shape}, s shape {s.shape}, vt shape {vt.shape}")

    # Show the original image
    plt.figure(figsize=(10, 5))
    plt.subplot(1,2,1)
    plt.title("The Pleiades image")
    plt.imshow(pleiades)
    plt.axis("off")

    # Show the greyscale image
    plt.subplot(1,2,2)
    plt.title("The Gray Pleiades image")
    plt.imshow(pleiades_grey, cmap="gray")
    plt.axis("off")
    plt.show()



if __name__ == "__main__":
    main()

