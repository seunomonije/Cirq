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

from typing import Dict, Optional, Tuple

import dataclasses

MEASUREMENT_KEY_SEPARATOR = ':'


@dataclasses.dataclass(frozen=True)
class MeasurementKey:
    """A class representing a Measurement Key.

    Wraps a string key. If you just want the string measurement key, simply call `str()` on this.

    Args:
        name: The string representation of the key.
        path: The path to this key in a circuit. In a multi-level circuit (one with repeated or
            nested subcircuits), we need to differentiate the keys that occur multiple times. The
            path is used to create such fully qualified unique measurement key based on where it
            occurs in the circuit. The path is outside-to-in, the outermost subcircuit identifier
            appears first in the tuple.
    """

    _hash: Optional[int] = dataclasses.field(default=None, init=False)
    _str: Optional[str] = dataclasses.field(default=None, init=False)

    name: str
    path: Tuple[str, ...] = dataclasses.field(default_factory=tuple)

    def __post_init__(self):
        if not self.name:
            raise ValueError("Measurement key name cannot be empty")
        if MEASUREMENT_KEY_SEPARATOR in self.name:
            raise ValueError(
                f'Invalid key name: {self.name}\n{MEASUREMENT_KEY_SEPARATOR} is not allowed in '
                'MeasurementKey. If this is a nested key string, use '
                '`MeasurementKey.parse_serialized` for correct behavior.'
            )

    def replace(self, **changes) -> 'MeasurementKey':
        """Returns a copy of this MeasurementKey with the specified changes."""
        return dataclasses.replace(self, **changes)

    def __eq__(self, other) -> bool:
        if isinstance(other, (MeasurementKey, str)):
            return str(self) == str(other)
        return NotImplemented

    def __repr__(self):
        if self.path:
            return f'cirq.MeasurementKey(path={self.path}, name={self.name})'
        else:
            return f'cirq.MeasurementKey(name={self.name})'

    def __str__(self):
        if self._str is None:
            object.__setattr__(
                self, '_str', MEASUREMENT_KEY_SEPARATOR.join(self.path + (self.name,))
            )
        return self._str

    def __hash__(self):
        if self._hash is None:
            object.__setattr__(self, '_hash', hash(str(self)))
        return self._hash

    def _json_dict_(self):
        return {
            'cirq_type': 'MeasurementKey',
            'name': self.name,
            'path': self.path,
        }

    @classmethod
    def _from_json_dict_(
        cls,
        name,
        path,
        **kwargs,
    ):
        return cls(name=name, path=tuple(path))

    @classmethod
    def parse_serialized(cls, key_str: str):
        """Parses the serialized string representation of `Measurementkey` into a `MeasurementKey`.

        This is the only way to construct a `MeasurementKey` from a nested string representation
        (where the path is joined to the key name by the `MEASUREMENT_KEY_SEPARATOR`)"""
        components = key_str.split(MEASUREMENT_KEY_SEPARATOR)
        return MeasurementKey(name=components[-1], path=tuple(components[:-1]))

    def _with_key_path_(self, path: Tuple[str, ...]):
        return self.replace(path=path)

    def with_key_path_prefix(self, path_component: str):
        """Adds the input path component to the start of the path.

        Useful when constructing the path from inside to out (in case of nested subcircuits),
        recursively.
        """
        return self._with_key_path_((path_component,) + self.path)

    def _with_measurement_key_mapping_(self, key_map: Dict[str, str]):
        if self.name not in key_map:
            return self
        return self.replace(name=key_map[self.name])
