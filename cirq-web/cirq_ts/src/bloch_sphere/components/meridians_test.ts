// Copyright 2021 The Cirq Developers
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      https://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

import {expect} from 'chai';
import {
  createHorizontalChordMeridians,
  createVerticalMeridians,
  createHorizontalCircleMeridians,
} from './meridians';

describe('Meridians methods', () => {
  const DEFAULT_RADIUS = 5;

  it('createHorizontalChordMeridians() returns an array of Line objects', () => {
    const meridians = createHorizontalChordMeridians(DEFAULT_RADIUS);
    for (const meridian of meridians) {
      expect(meridian.type).to.equal('Line');
    }
  });

  it('createHorizontalCircleMeridians() returns an array of Line objects', () => {
    const meridians = createHorizontalCircleMeridians(DEFAULT_RADIUS);
    for (const meridian of meridians) {
      expect(meridian.type).to.equal('Line');
    }
  });

  it('createVerticalMeridians() returns an array of Line objects', () => {
    const meridians = createVerticalMeridians(DEFAULT_RADIUS);
    for (const meridian of meridians) {
      expect(meridian.type).to.equal('Line');
    }
  });
});
