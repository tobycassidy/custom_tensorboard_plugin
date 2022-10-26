from pathlib import Path

import tensorflow as tf


@tf.function
def init_model(model_to_init: tf.keras.models.Model, data_to_init_model: tf.Tensor):
    """Function to initialise model with data utilising the autograph decorator @tf.function."""
    model_to_init(data_to_init_model)


def write_graph_summaries(log_dir: str,
                          model_to_init: tf.keras.models.Model,
                          data_to_init_model: tf.Tensor):
    """Function to write summaries and visualise tensorflow models using the GRAPHS plugin."""
    log_path = Path(log_dir)

    if not log_path.exists():
        print("Creating Directory....")
        log_path.mkdir()
    else:
        print("Directory already exists")

    writer = tf.summary.create_file_writer(log_dir)
    tf.summary.trace_on(graph=True)
    init_model(model_to_init, data_to_init_model)

    with writer.as_default():
        tf.summary.trace_export("Model Architecture", step=0)


if __name__ == "__main__":
    log_dir = "demo_logs"
    inputs = tf.keras.Input(shape=(3, 1), name="input")
    flatten = tf.keras.layers.Flatten(name="flatten")(inputs)
    dense1 = tf.keras.layers.Dense(32, name="dense1")(flatten)
    dense2 = tf.keras.layers.Dense(32, name="dense2")(dense1)
    output = tf.keras.layers.Dense(1, activation="sigmoid", name="sigmoid")(dense2)

    model = tf.keras.Model(
        inputs=inputs,
        outputs=output
    )
    data = tf.random.normal(
        mean=1.0,
        stddev=0.1,
        shape=(100, 3, 1)
    )

    # RUN
    write_graph_summaries(
        log_dir=log_dir,
        model_to_init=model,
        data_to_init_model=data
    )
