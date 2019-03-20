import itertools

from garage.tf.core import layers as garage_layers
from garage.tf.core.parameterized import Parameterized


class LayersPowered(Parameterized):
    def __init__(self, output_layers, input_layers=None):
        self._output_layers = output_layers
        self._input_layers = input_layers
        Parameterized.__init__(self)

    def get_params_internal(self, **tags):
        layers = garage_layers.get_all_layers(
            self._output_layers, treat_as_input=self._input_layers)
        params = itertools.chain.from_iterable(
            l.get_params(**tags) for l in layers)
        return garage_layers.unique(params)
