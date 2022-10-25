import os
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorboard.plugins import projector


class TensorBoardProjector:
    """
    This class is designed to leverage the tensorboard projector plugin. This allows a user to load in high
    dimensionality data and project otno a lower dimensional space with a variety of dimensionality reduction
    techniques (e.g. PCA, TSNE, UMAP or custom). It is natural to analyse labelled outputs (e.g. clustering labels)
    as a user can load labels for each vector and thus analyse in an interactive way using tensorboard.
    """
    def __init__(self, log_dir: str, metadata_path: str, tensor_name: str):
        self.log_dir = log_dir
        self.metadata_path = metadata_path
        self.tensor_name = tensor_name
        self.tensor_filepath = os.path.join(log_dir, tensor_name + ".ckpt")

    @staticmethod
    def register_embedding(log_dir, metadata_path, tensor_name):
        config = projector.ProjectorConfig()
        embedding = config.embeddings.add()
        embedding.tensor_name = tensor_name
        embedding.metadata_path = metadata_path
        projector.visualize_embeddings(log_dir, config)

    @staticmethod
    def save_labels_tsv(log_dir, metadata_path, labels):
        with open(os.path.join(log_dir, metadata_path), "w") as f:
            for label in labels:
                f.write('{}\n'.format(label))

    def run(self, embedding, labels):
        tensor_embeddings = tf.Variable(np.array(embedding), name=self.tensor_name)
        saver = tf.compat.v1.train.Saver([tensor_embeddings])
        saver.save(sess=None, global_step=0, save_path=self.tensor_filepath)
        self.register_embedding(
            log_dir=self.log_dir,
            metadata_path=self.metadata_path,
            tensor_name=self.tensor_name
        )
        self.save_labels_tsv(
            log_dir=self.log_dir,
            metadata_path=self.metadata_path,
            labels=np.array(labels)
        )
        print("Run `tensorboard --logdir={0}` to view result on tensorboard".format(self.log_dir))


embedding = pd.concat([
    pd.DataFrame(np.random.normal(0, 0.5, (1000, 10))),
    pd.DataFrame(np.random.normal(3, 0.5, (1000, 10))),
    pd.DataFrame(np.random.normal(5, 0.5, (1000, 10))),
], axis=0)

labels = np.vstack([
    np.zeros((1000, 1)),
    np.ones((1000, 1)),
    np.add(np.ones((1000, 1)), 1),
]).astype(int)

viz = TensorBoardProjector(log_dir="demo_logs", metadata_path="meta.tsv", tensor_name="embeddings")
viz.run(
    embedding=embedding,
    labels=labels
)
