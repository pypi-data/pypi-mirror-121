import tensorflow as tf

# tf.data.experimental.enable_debug_mode()

@tf.function
def train_step(
    generator: tf.keras.Model,
    discriminator: tf.keras.Model,
    generator_optimizer: tf.keras.optimizers.Optimizer,
    discriminator_optimizer: tf.keras.optimizers.Optimizer,
    batch_real_images: tf.Tensor,
    batch_prior: tf.Tensor,
    step: tf.Tensor
) -> None:
    # persistent is set to True because the tape is used more than
    # once to calculate the gradients.
    with tf.GradientTape(persistent=True) as tape:

        fake_images = generator(batch_prior, training=True)
        disc_real_images = discriminator(
            tf.divide(batch_real_images - tf.constant(127.5), tf.constant(127.5)),
            training=True,
        )
        disc_fake_images = discriminator(fake_images, training=True)

        # calculate the loss
        gen_loss = -tf.reduce_mean(disc_fake_images)
        disc_loss = tf.reduce_mean(disc_fake_images) - tf.reduce_mean(disc_real_images)

        #gen_loss = tf.reduce_mean(
        #    tf.keras.losses.binary_crossentropy(
        #        tf.ones_like(disc_fake_images), disc_fake_images
        #    )
        #)
        #disc_loss = tf.reduce_mean(
        #    tf.keras.losses.binary_crossentropy(
        #        tf.ones_like(disc_real_images), disc_real_images
        #    )
        #) + tf.reduce_mean(
        #    tf.keras.losses.binary_crossentropy(
        #        tf.zeros_like(disc_fake_images), disc_fake_images
        #    )
        #)

    # Calculate the gradients for generator and discriminator
    generator_gradients = tape.gradient(gen_loss, generator.trainable_variables)

    # Apply the gradients to the optimizer
    if step % 5 == 0:

        capped_gen_gvs = [
            (tf.clip_by_value(grad, -1e-2, 1e-2), var)
            for grad, var in zip(generator_gradients, generator.trainable_variables)
        ]
        #
        generator_optimizer.apply_gradients(capped_gen_gvs)

    discriminator_gradients = tape.gradient(
        disc_loss, discriminator.trainable_variables
    )

    capped_disc_gvs = [
        (tf.clip_by_value(grad, -1e-2, 1e-2), var)
        for grad, var in zip(discriminator_gradients, discriminator.trainable_variables)
    ]
    #
    discriminator_optimizer.apply_gradients(capped_disc_gvs)
