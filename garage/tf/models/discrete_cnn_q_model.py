"""Discrete MLP Model."""
import tensorflow as tf

from garage.tf.core.cnn import cnn
from garage.tf.models.base import Model


class DiscreteCNNQModel(Model):
    """
    Discrete CNN Q Model.

    Args:
        filter_dims: Dimension of the filters.
        num_filters: Number of filters.
        strides: The stride of the sliding window.
        name: Variable scope of the cnn.
        padding: The type of padding algorithm to use, from "SAME", "VALID".
    """

    def __init__(self,
                 filter_dims,
                 num_filters,
                 strides,
                 name,
                 out_model,
                 padding="VALID"):
        super().__init__(name)
        self._filter_dims = filter_dims
        self._num_filters = num_filters
        self._strides = strides
        self._padding = padding
        self._out_model = out_model

    def _build(self, state_input):
        network = cnn(
            input_var=state_input,
            filter_dims=self._filter_dims,
            num_filters=self._num_filters,
            strides=self._strides,
            padding=self._padding,
            name="cnn")

        return self._out_model.build(network)
