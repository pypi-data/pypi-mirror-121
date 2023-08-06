from GitMarco.tf import utils, metrics
import tensorflow as tf


def r_squared(y, prediction):
    """
    :param y: True values
    :param prediction: Predictions
    :return: R squared

    Determination Coefficient Metric For Tensorflow
    """
    unexplained_error = tf.reduce_sum(tf.square(tf.sub(y, prediction)))
    total_error = tf.reduce_sum(tf.square(tf.sub(y, tf.reduce_mean(y))))
    return tf.sub(1, tf.div(unexplained_error, total_error))
