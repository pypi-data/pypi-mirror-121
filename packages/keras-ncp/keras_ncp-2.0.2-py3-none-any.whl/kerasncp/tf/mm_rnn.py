# Copyright 2020-2021 Mathias Lechner
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import numpy as np
from packaging.version import parse

try:
    import tensorflow as tf
except:
    raise ImportWarning(
        "It seems like the Tensorflow package is not installed\n"
        "Please run"
        "`$ pip install tensorflow`. \n",
    )

if parse(tf.__version__) < parse("2.0.0"):
    raise ImportError(
        "The Tensorflow package version needs to be at least 2.0.0 \n"
        "for keras-ncp to run. Currently, your TensorFlow version is \n"
        "{version}. Please upgrade with \n"
        "`$ pip install --upgrade tensorflow`. \n"
        "You can use `pip freeze` to check afterwards that everything is "
        "ok.".format(version=tf.__version__)
    )


@tf.keras.utils.register_keras_serializable(package="Custom", name="MixedMemoryRNN")
class MixedMemoryRNN(tf.keras.layers.AbstractRNNCell):
    def __init__(self, rnn_cell, forget_gate_bias=1.0, **kwargs):
        self.rnn_cell = rnn_cell
        self.forget_gate_bias = forget_gate_bias
        super(MixedMemoryRNN, self).__init__(**kwargs)

    @property
    def state_size(self):
        return [self.rnn_cell.state_size, self.rnn_cell.state_size]

    @property
    def flat_size(self):
        if isinstance(self.rnn_cell.state_size, int):
            return self.rnn_cell.state_size
        return sum(self.rnn_cell.state_size)

    def build(self, input_shape):
        input_dim = input_shape[-1]
        if isinstance(input_shape[0], tuple):
            # Nested tuple
            input_dim = input_shape[0][-1]

        self.rnn_cell.build(input_shape)
        self.input_kernel = self.add_weight(
            shape=(input_dim, 4 * self.flat_size),
            initializer=self.initializer,
            name="input_kernel",
        )
        self.recurrent_kernel = self.add_weight(
            shape=(self.flat_size, 4 * self.flat_size),
            initializer=self.recurrent_initializer,
            name="recurrent_kernel",
        )
        self.bias = self.add_weight(
            shape=(4 * self.flat_size),
            initializer=tf.keras.initializers.Zeros(),
            name="bias",
        )

        self.built = True

    def call(self, inputs, states, **kwargs):
        memory_state, ct_state = states

        z = (
            tf.matmul(inputs, self.input_kernel)
            + tf.matmul(ct_state, self.recurrent_kernel)
            + self.bias
        )
        i, ig, fg, og = tf.split(z, 4, axis=-1)

        input_activation = tf.nn.tanh(i)
        input_gate = tf.nn.sigmoid(ig)
        forget_gate = tf.nn.sigmoid(fg + self.forget_gate_bias)
        output_gate = tf.nn.sigmoid(og)

        new_memory_state = memory_state * forget_gate + input_activation * input_gate
        ct_input = tf.nn.tanh(new_memory_state) * output_gate  # LSTM output = ODE input

        if (isinstance(inputs, tuple) or isinstance(inputs, list)) and len(inputs) > 1:
            # Input is a tuple -> Ct cell input should also be a tuple
            ct_input = (ct_input,) + inputs[1:]

        # Implementation choice on how to parametrize ODE component
        ct_output, new_ct_state = self.cfc(ct_input, [ct_state])

        return ct_output, [new_memory_state, new_ct_state[0]]

    def get_config(self):
        serialized = {
            "rnn_cell": self.rnn_cell.get_config(),
            "forget_gate_bias": self.forget_gate_bias,
        }
        return serialized

    @classmethod
    def from_config(cls, config):
        rnn_cell = tf.keras.layers.deserialize(config["rnn_cell"])
        return cls(rnn_cell=rnn_cell, **config)