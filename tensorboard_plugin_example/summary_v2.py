"""Creating the summaries for the custom plugin."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow.compat.v2 as tf
from tensorboard.compat.proto import summary_pb2

from tensorboard_plugin_example import metadata


def greeting(name, guest, step=None, description=None):
    """Write a "greeting" summary."""
    with tf.summary.experimental.summary_scope(
        name, "greeeting_summary", values=[guest, step],
    ) as (tag, _):
        return tf.summary.write(
            tag=tag,
            tensor=tf.strings.join(["Hello, ", guest, "!"]),
            step=step,
            metadata=_create_summary_metadata(description)
        )


def _create_summary_metadata(description):
    return summary_pb2.SummaryMetadata(
        summary_description=description,
        plugin_data=summary_pb2.SummaryMetadata.PluginData(
            plugin_name=metadata.PLUGIN_NAME,
            content=b"",  # no need for summary-specific metadata
        ),
        data_class=summary_pb2.DATA_CLASS_TENSOR,
    )
