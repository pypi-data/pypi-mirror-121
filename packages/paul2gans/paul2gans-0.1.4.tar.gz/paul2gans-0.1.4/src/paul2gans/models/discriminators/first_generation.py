from typing import Tuple

import tensorflow as tf


def discriminator_network(
    image_dimension: Tuple[int, int, int], prior_dimension: int, kernel_size: int
) -> tf.keras.Model:
    image_tensor = tf.keras.layers.Input(shape=image_dimension)
    x = tf.keras.layers.Conv2D(filters=3, kernel_size=kernel_size, strides=(2, 2))(
        image_tensor
    )
    x = tf.keras.layers.LeakyReLU(alpha=0.2)(x)
    x = tf.keras.layers.Conv2D(filters=8, kernel_size=kernel_size, strides=(2, 2))(x)
    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.LeakyReLU(alpha=0.2)(x)
    x = tf.keras.layers.Conv2D(filters=16, kernel_size=kernel_size, strides=(2, 2))(x)
    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.LeakyReLU(alpha=0.2)(x)
    x = tf.keras.layers.Conv2D(filters=32, kernel_size=kernel_size, strides=(2, 2))(x)
    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.LeakyReLU(alpha=0.2)(x)
    x = tf.keras.layers.Conv2D(filters=64, kernel_size=kernel_size, strides=(2, 2))(x)
    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.LeakyReLU(alpha=0.2)(x)
    x = tf.keras.layers.Flatten()(x)
    output = tf.keras.layers.Dense(1, activation="sigmoid")(x)
    return tf.keras.models.Model(image_tensor, output)
