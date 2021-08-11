# Copyright 2019 The Cirq Developers
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

import functools
from typing import Dict

from cirq.protocols.json_serialization import ObjectFactory


@functools.lru_cache()
def _class_resolver_dictionary() -> Dict[str, ObjectFactory]:
    import cirq_google
    from cirq_google.devices.known_devices import _NamedConstantXmonDevice

    return {
        '_NamedConstantXmonDevice': _NamedConstantXmonDevice,
        'Calibration': cirq_google.Calibration,
        'CalibrationTag': cirq_google.CalibrationTag,
        'CalibrationLayer': cirq_google.CalibrationLayer,
        'CalibrationResult': cirq_google.CalibrationResult,
        'CouplerPulse': cirq_google.experimental.CouplerPulse,
        'SycamoreGate': cirq_google.SycamoreGate,
        'GateTabulation': cirq_google.GateTabulation,
        'PhysicalZTag': cirq_google.PhysicalZTag,
        'FloquetPhasedFSimCalibrationOptions': cirq_google.FloquetPhasedFSimCalibrationOptions,
        'FloquetPhasedFSimCalibrationRequest': cirq_google.FloquetPhasedFSimCalibrationRequest,
        'PhasedFSimCalibrationResult': cirq_google.PhasedFSimCalibrationResult,
        'PhasedFSimCharacterization': cirq_google.PhasedFSimCharacterization,
        'XEBPhasedFSimCalibrationOptions': cirq_google.XEBPhasedFSimCalibrationOptions,
        'XEBPhasedFSimCalibrationRequest': cirq_google.XEBPhasedFSimCalibrationRequest,
        'LocalXEBPhasedFSimCalibrationOptions': cirq_google.LocalXEBPhasedFSimCalibrationOptions,
        'LocalXEBPhasedFSimCalibrationRequest': cirq_google.LocalXEBPhasedFSimCalibrationRequest,
    }
