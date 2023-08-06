import matplotlib.pyplot as plt
import tensorflow as tf


def generate_images(
    model: tf.keras.Model, prior_values: tf.Tensor, figure_filepath: str
) -> None:
    prediction = model(prior_values)

    fig, ax = plt.subplots(nrows=3, ncols=3, figsize=(36, 36))
    for i in range(9):
        ax[i // 3][i % 3].imshow((prediction[i].numpy() + 1) / 2.0)
    plt.savefig(figure_filepath)
    plt.close(fig)
