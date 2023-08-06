import tensorflow as tf


def generator_network(prior_dimension: int, kernel_size: int) -> tf.keras.Model:
    init = tf.keras.initializers.RandomNormal(stddev=0.02)
    input_tensor = tf.keras.layers.Input(shape=(prior_dimension,))
    x = tf.keras.layers.Dense(units=4 * 4 * 128, kernel_initializer=init)(input_tensor)
    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.ReLU()(x)
    x = tf.keras.layers.Reshape(target_shape=(4, 4, 128))(x)
    x = tf.keras.layers.Conv2DTranspose(
        filters=64,
        kernel_size=kernel_size,
        strides=2,
        padding="same",
        kernel_initializer=init
    )(x)
    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.ReLU()(x)
    x = tf.keras.layers.Conv2DTranspose(
        filters=32,
        kernel_size=kernel_size,
        strides=2,
        padding="same",
        kernel_initializer=init,
    )(x)
    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.ReLU()(x)
    x = tf.keras.layers.Conv2DTranspose(
        filters=16,
        kernel_size=kernel_size,
        strides=2,
        padding="same",
        kernel_initializer=init,
    )(x)
    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.ReLU()(x)
    x = tf.keras.layers.Conv2DTranspose(
        filters=8,
        kernel_size=kernel_size,
        strides=2,
        padding="same",
        kernel_initializer=init,
    )(x)
    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.ReLU()(x)
    # No activation
    image = tf.keras.layers.Conv2DTranspose(
        filters=3,
        kernel_size=kernel_size,
        strides=2,
        padding="same",
        kernel_initializer=init,
        activation="tanh",
    )(x)

    return tf.keras.models.Model(input_tensor, image)
