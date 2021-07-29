# implementation based on https://www.qmunity.tech/tutorials/the-variational-quantum-eigensolver

import pennylane as qml
from pennylane import numpy as np
from io import StringIO

def main(dict):
    matrix_str = dict["hamiltonian_matrix"]
    # matrix = "0, 0, 0, 0\n0, 0, 0, 0\n0, 0, 0, 0\n0, 0, 0, 0"
    matrix = np.genfromtxt(StringIO(matrix_str), delimiter=",")
    print(matrix)
    obs = qml.Hermitian(matrix, wires=[0, 1])
    h = qml.Hamiltonian((0.8, ), (obs, ))

    max_iterations = dict["max_iterations"]
    stepsize = dict["stepsize"]

    qubits = 4
    dev = qml.device('default.qubit', wires=qubits)

    def circuit(params, wires):
        qml.BasisState(np.array([1, 1, 0, 0], requires_grad=False), wires=wires)
        for i in wires:
            qml.Rot(*params[i], wires=i)
        qml.CNOT(wires=[2, 3])
        qml.CNOT(wires=[2, 0])
        qml.CNOT(wires=[3, 1])


    cost_function = qml.ExpvalCost(circuit, h, dev)

    opt = qml.GradientDescentOptimizer(stepsize=stepsize)
    np.random.seed(0)
    params = np.random.normal(0, np.pi, (qubits, 3))


    conv_tol = 1e-06
    for n in range(max_iterations):
        params, prev_energy = opt.step_and_cost(cost_function, params)
        energy = cost_function(params)
        conv = np.abs(energy - prev_energy)

        if n % 20 == 0:
            print('Iteration = {:},  Energy = {:.8f} Ha'.format(n, energy))

        if conv <= conv_tol:
            break
    print()
    print('Final value of the ground-state energy = {:.8f} Ha'.format(energy))