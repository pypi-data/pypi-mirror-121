import click
import tensorflow as tf
from paul2gans.images.generation import generate_images
from paul2gans.models.discriminators import discriminator_network
from paul2gans.models.generators import generator_network
from paul2gans.models.training_procedure import train_step
from paul2gans.pipelines import GANParams
from paul2gans.pipelines.main import training

tf.config.run_functions_eagerly(True)  # to delete
tf.data.experimental.enable_debug_mode()


@training.command()
@click.option("--prior-dimension", default=5, type=int)
@click.option("--kernel-dimension", default=5, type=int)
@click.pass_context
def wgan(ctx: click.Context, prior_dimension: int, kernel_dimension: int):
    gan_params: GANParams = ctx.obj
    dataset = tf.keras.preprocessing.image_dataset_from_directory(
        gan_params.data_source,
        label_mode=None,
        batch_size=gan_params.batch_size,
        image_size=gan_params.image_resolution,
        shuffle=True,
    )

    # NETWORK
    fixed_samples = tf.random.normal((9, prior_dimension))

    generator = generator_network(prior_dimension, kernel_dimension)
    discriminator = discriminator_network(
        (*gan_params.image_resolution, 3), prior_dimension, kernel_dimension
    )
    generator_optimizer = tf.keras.optimizers.Adam(
        learning_rate=5e-3, beta_1=.5
    )
    discriminator_optimizer = tf.keras.optimizers.Adam(
        learning_rate=5e-3, beta_1=.5
    )

    step = 0
    for batch_real_images in dataset.repeat(200):
        step += 1
        batch_prior = tf.random.normal((gan_params.batch_size, prior_dimension))
        train_step(
            generator,
            discriminator,
            generator_optimizer,
            discriminator_optimizer,
            batch_real_images,
            batch_prior,
            step
        )

        if step % 30 == 0:
            figure_filepath = f"{gan_params.output_directory}step_{step}_over_{gan_params.n_iters}.jpg"
            generate_images(generator, fixed_samples, figure_filepath)

    generator.save('/home/paul/perso/aiposters/generator.h5')


@training.command()
@click.option("--prior-dimension", default=5, type=int)
@click.option("--kernel-dimension", default=5, type=int)
@click.pass_context
def wgan2(ctx: click.Context, prior_dimension: int, kernel_dimension: int):
    gan_params: GANParams = ctx.obj

    import os
    import pathlib

    import numpy as np
    import tensorflow as tf

    global_dir = pathlib.Path(gan_params.data_source)
    class_names = np.array(sorted([item.name for item in global_dir.glob('*') if item.name != "LICENSE.txt"]))
    print(class_names)

    def get_label(file_path):
        # convert the path to a list of path components
        parts = tf.strings.split(file_path, os.path.sep)
        # The second to last is the class-directory
        one_hot = parts[-2] == class_names
        # Integer encode the label
        return tf.argmax(one_hot)

    def decode_img(img):
        # convert the compressed string to a 3D uint8 tensor
        img = tf.image.decode_jpeg(img, channels=3)
        # resize the image to the desired size
        return tf.image.resize(img, gan_params.image_resolution)

    def process_image(class_names):
        def process_path(file_path):
            parts = tf.strings.split(file_path, os.path.sep)
            # The second to last is the class-directory
            one_hot = parts[-2] == class_names
            # Integer encode the label
            label = tf.argmax(one_hot)
            # load the raw data from the file as a string
            img = tf.io.read_file(file_path)
            img = decode_img(img)
            return img, label

        return process_path


    def create_atomic_dataset(data_dir: str, class_names: np.array):
        list_ds = tf.data.Dataset.list_files(str(f'{data_dir}/*.jpg'), shuffle=False)
        list_ds = list_ds.shuffle(len(list_ds), reshuffle_each_iteration=False)
        return list_ds.map(process_image(class_names), num_parallel_calls=tf.data.AUTOTUNE)

    datasets = []
    for ppath in global_dir.glob('*'):
        ds = create_atomic_dataset(str(ppath), class_names)
        ds = ds.repeat(-1)
        datasets.append(ds)
    dataset = tf.data.experimental.sample_from_datasets(datasets)
    dataset = dataset.batch(gan_params.batch_size)


    #dataset = tf.keras.preprocessing.image_dataset_from_directory(
    #    gan_params.data_source,
    #    label_mode=None,
    #    batch_size=gan_params.batch_size,
    #    image_size=gan_params.image_resolution,
    #    shuffle=True,
    #)

    # NETWORK
    fixed_samples = tf.random.normal((9, prior_dimension))

    generator = generator_network(prior_dimension, kernel_dimension)
    discriminator = discriminator_network(
        (*gan_params.image_resolution, 3), prior_dimension, kernel_dimension
    )
    generator_optimizer = tf.keras.optimizers.Adam(
        learning_rate=5e-3, beta_1=.5
    )
    discriminator_optimizer = tf.keras.optimizers.Adam(
        learning_rate=5e-3, beta_1=.5
    )

    keras = tf.keras
    class GAN(keras.Model):
        def __init__(self, discriminator, generator, latent_dim):
            super(GAN, self).__init__()
            self.discriminator = discriminator
            self.generator = generator
            self.latent_dim = latent_dim

        def compile(self, d_optimizer, g_optimizer, loss_fn):
            super(GAN, self).compile()
            self.d_optimizer = d_optimizer
            self.g_optimizer = g_optimizer
            self.loss_fn = loss_fn

        def train_step(self, real_images):
            if isinstance(real_images, tuple):
                real_images = real_images[0]
            # Sample random points in the latent space
            batch_size = tf.shape(real_images)[0]
            random_latent_vectors = tf.random.normal(shape=(batch_size, self.latent_dim))

            # Decode them to fake images
            generated_images = self.generator(random_latent_vectors)

            # Combine them with real images
            combined_images = tf.concat([generated_images, real_images], axis=0)

            # Assemble labels discriminating real from fake images
            labels = tf.concat(
                [tf.ones((batch_size, 1)), tf.zeros((batch_size, 1))], axis=0
            )
            # Add random noise to the labels - important trick!
            labels += 0.05 * tf.random.uniform(tf.shape(labels))

            # Train the discriminator
            with tf.GradientTape() as tape:
                predictions = self.discriminator(combined_images)
                d_loss = self.loss_fn(labels, predictions)
            grads = tape.gradient(d_loss, self.discriminator.trainable_weights)
            self.d_optimizer.apply_gradients(
                zip(grads, self.discriminator.trainable_weights)
            )

            # Sample random points in the latent space
            random_latent_vectors = tf.random.normal(shape=(batch_size, self.latent_dim))

            # Assemble labels that say "all real images"
            misleading_labels = tf.zeros((batch_size, 1))

            # Train the generator (note that we should *not* update the weights
            # of the discriminator)!
            with tf.GradientTape() as tape:
                predictions = self.discriminator(self.generator(random_latent_vectors))
                g_loss = tf.reduce_mean(predictions)
            grads = tape.gradient(g_loss, self.generator.trainable_weights)
            self.g_optimizer.apply_gradients(zip(grads, self.generator.trainable_weights))
            return {"d_loss": d_loss, "g_loss": g_loss}

    gan = GAN(discriminator=discriminator, generator=generator, latent_dim=10)
    gan.compile(
        d_optimizer=keras.optimizers.Adam(learning_rate=0.0003),
        g_optimizer=keras.optimizers.Adam(learning_rate=0.0003),
        loss_fn=keras.losses.BinaryCrossentropy(from_logits=False),
    )

    tb_callback = tf.keras.callbacks.TensorBoard(log_dir='/home/paul/perso/aiposters/tb/')
    #tf.profiler.experimental.start('/home/paul/perso/aiposters/tb/')
    # To limit the execution time, we only train on 100 batches. You can train on
    # the entire dataset. You will need about 20 epochs to get nice results.
    gan.fit(dataset, epochs=10, steps_per_epoch=100, callbacks=[tb_callback])