from datetime import datetime

import tensorflow as tf
import tensorflow_datasets as tfds


def normalize_img(image, label):
    """Normalizes images: `uint8` -> `float32`."""
    return tf.cast(image, tf.float32) / 255., label


if __name__ == "__main__":
    (ds_train, ds_test), ds_info = tfds.load(
        'mnist',
        split=['train', 'test'],
        shuffle_files=True,
        as_supervised=True,
        with_info=True,
    )

    ds_train = ds_train.map(normalize_img)
    ds_train = ds_train.batch(128)

    ds_test = ds_test.map(normalize_img)
    ds_test = ds_test.batch(128)

    model = tf.keras.models.Sequential([
      tf.keras.layers.Flatten(input_shape=(28, 28, 1)),
      tf.keras.layers.Dense(128, activation='relu'),
      tf.keras.layers.Dense(10, activation='softmax')
    ])
    model.compile(
        loss='sparse_categorical_crossentropy',
        optimizer=tf.keras.optimizers.Adam(0.001),
        metrics=['accuracy']
    )

    # Create a TensorBoard callback
    logs = "profile_logs/" + datetime.now().strftime("%Y%m%d-%H%M%S")

    tb_callback = tf.keras.callbacks.TensorBoard(
        log_dir=logs,
        histogram_freq=1,
        profile_batch='500,520'
    )

    model.fit(
        ds_train,
        epochs=10,
        validation_data=ds_test,
        callbacks=[tb_callback]
    )