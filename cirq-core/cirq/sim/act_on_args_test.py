# Copyright 2021 The Cirq Developers
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
import pytest

import cirq
from cirq.sim import act_on_args


class DummyArgs(cirq.ActOnArgs):
    def __init__(self):
        super().__init__(qubits=cirq.LineQubit.range(2))

    def copy(self):
        pass

    def sample(self, qubits, repetitions=1, seed=None):
        pass

    def _perform_measurement(self, qubits):
        return [5, 3]

    def _act_on_fallback_(self, action, qubits, allow_decompose):
        return True


def test_measurements():
    args = DummyArgs()
    args.measure([cirq.LineQubit(0)], "test", [False])
    assert args.log_of_measurement_results["test"] == [5]


def test_decompose():
    class Composite(cirq.Gate):
        def num_qubits(self) -> int:
            return 1

        def _decompose_(self, qubits):
            yield cirq.X(*qubits)

    args = DummyArgs()
    assert act_on_args.strat_act_on_from_apply_decompose(Composite(), args, [cirq.LineQubit(0)])


def test_mapping():
    args = DummyArgs()
    assert list(iter(args)) == cirq.LineQubit.range(2)
    r1 = args[cirq.LineQubit(0)]
    assert args is r1
    with pytest.raises(IndexError):
        _ = args[cirq.LineQubit(2)]


def test_swap_bad_dimensions():
    q0 = cirq.LineQubit(0)
    q1 = cirq.LineQid(1, 3)
    args = DummyArgs()
    with pytest.raises(ValueError, match='Cannot swap different dimensions'):
        args.swap(q0, q1)


def test_rename_bad_dimensions():
    q0 = cirq.LineQubit(0)
    q1 = cirq.LineQid(1, 3)
    args = DummyArgs()
    with pytest.raises(ValueError, match='Cannot rename to different dimensions'):
        args.rename(q0, q1)
