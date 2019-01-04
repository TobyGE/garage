"""
This script creates a unittest that tests Gaussian policies in
garage.tf.policies.
"""
from unittest import mock

import numpy as np
import tensorflow as tf

from garage.misc.overrides import overrides
from garage.spaces import Box
from garage.spaces import Discrete
from garage.tf.core.mlp import mlp
from garage.tf.policies import QfDerivedPolicy
from tests.fixtures import TfGraphTestCase


class TestQfDerivedPolicy(TfGraphTestCase):
    @overrides
    def setUp(self):
        self.observation_shape = (4, )
        self.action_shape = 2
        self.env = mock.Mock()
        env_spec = mock.Mock()
        env_spec.observation_space = Box(
            low=0, high=1, shape=self.observation_shape)
        env_spec.action_space = Discrete(self.action_shape)
        self.env.env_spec = env_spec
        self.env.reset.return_value = np.zeros(self.observation_shape)
        self.env.step.side_effect = self._step

        super().setUp()

    def _step(self, action):
        return np.random.uniform(0., 1.,
                                 self.observation_shape), 0, False, dict()

    def test_qf_derived_policy(self):
        obs_ph = tf.placeholder(tf.float32, shape=(None, 4))
        qf = mlp(
            input_var=obs_ph,
            output_dim=2,
            hidden_sizes=(32, 32),
            hidden_nonlinearity=tf.nn.relu,
            name="mlp")
        policy = QfDerivedPolicy(
            env_spec=self.env.env_spec, qf=qf, obs_ph=obs_ph)

        self.sess.run(tf.global_variables_initializer())

        obs, _, _, _ = self.env.step(1)
        policy.get_action(obs, self.sess)
        policy.get_actions([obs], self.sess)
