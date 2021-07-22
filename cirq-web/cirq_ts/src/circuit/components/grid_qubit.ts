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

import {Group, Vector3} from 'three';
import {
  QubitLine,
  QubitLabel,
  X3DSymbol,
  BoxGate3DSymbol,
  Control3DSymbol,
  ConnectionLine,
} from './meshes';

/**
 * Class that represents a GridQubit.
 * A GridQubit consists of a three.js line, a sprite
 * with location information, and three.js mesh objects
 * representing the gates, if applicable.
 */
export class GridQubit extends Group {
  readonly row: number;
  readonly col: number;
  readonly moments: number;
  private operationsMap: (X3DSymbol | BoxGate3DSymbol | Control3DSymbol | ConnectionLine)[];
  /**
   * Class constructor.
   * @param row The row of the GridQubit
   * @param col The column of the GridQubit
   * @param moments The number of moments of the entire circuit. This
   * determines the length of the three.js line representing the GridQubit
   */
  constructor(row: number, col: number, moments: number) {
    super();

    this.row = row;
    this.col = col;
    this.moments = moments;
    this.operationsMap = [];
    this.createLine();
    this.addLocationLabel();
  }

  /**
   * Adds a three.js mesh single qubit gate symbol
   * to the group at the designated moment.
   * @param label The label of the gate
   * @param color The color of the gate
   * @param moment The moment at which the gate occurs
   */
  addSingleQubitGate(label: string, color: string, moment: number) {
    if (label === 'X') {
      const mesh = new X3DSymbol(color);
      mesh.position.set(this.row, moment, this.col);
      this.add(mesh);
      this.operationsMap.push(mesh);
      return;
    }

    const mesh = new BoxGate3DSymbol(label, color);
    mesh.position.set(this.row, moment, this.col);
    this.add(mesh);
    this.operationsMap.push(mesh);
  }

  /**
   * Adds a three.js mesh control symbol
   * to the group at the designated moment.
   * @param moment The moment at which the control occurs.
   */
  addControl(moment: number) {
    const mesh = new Control3DSymbol();
    mesh.position.set(this.row, moment, this.col);
    this.add(mesh);
    this.operationsMap.push(mesh);
  }

  /**
   * Adds a three.js line mesh connecting one qubit to another
   * at the designated moment
   * @param row The row of the target qubit
   * @param col The column of the target qubit
   * @param moment The moment where the qubits are connected
   */
  addLineToQubit(row: number, col: number, moment: number) {
    const coords = [
      new Vector3(this.row, moment, this.col),
      new Vector3(row, moment, col),
    ];
    const mesh = new ConnectionLine(coords[0], coords[1])
    this.add(mesh);
    this.operationsMap.push(mesh);
  }

  showAllMoments() {
    this.operationsMap.forEach((value) =>{
      value.show();
    });
  }

  hideMomentsBefore(moment: number){
    this.operationsMap.forEach((value) => {
      if (value.position.y < moment) {
        value.blur();
      }
    });
  }

  hideMomentsAfter(moment: number){
    this.operationsMap.forEach((value) => {
      if (value.position.y > moment) {
        value.blur();
      }
    });
  }

  private createLine() {
    const coords = [
      new Vector3(this.row, 0, this.col),
      new Vector3(this.row, this.moments, this.col),
    ];
    this.add(new QubitLine(coords[0], coords[1]));
  }

  private addLocationLabel() {
    const sprite = new QubitLabel(`(${this.row}, ${this.col})`);
    sprite.position.copy(new Vector3(this.row, -0.6, this.col));
    this.add(sprite);
  }
}
