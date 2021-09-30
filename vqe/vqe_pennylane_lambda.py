import json
import pennylane as qml
from pennylane import numpy as np
from io import StringIO

#{
#    "hamiltonian_matrix": "0, 0, 0, 0\n0, 0, 0, 0\n0, 0, 0, 0\n0, 0, 0, 0",
#    "max_iterations": 10,
#    "stepsize": 0.4
#}
def lambda_handler(event, context):
    matrix_str = event['hamiltonian_matrix']
    matrix = np.genfromtxt(StringIO(matrix_str), delimiter=",")
    print(matrix)
    obs = qml.Hermitian(matrix, wires=[0, 1])
    h = qml.Hamiltonian((0.8, ), (obs, ))

    max_iterations = event['max_iterations']
    stepsize = event['stepsize']

    qubits = 4
    dev = qml.device('default.qubit', wires=qubits)

    ## IBM Quantum
    #dev = qml.device('qiskit.ibmq', wires=qubits, backend='ibmq_qasm_simulator', ibmqx_token=event["IBMQ_TOKEN"])

    ## AWS Braket
    #s3 = ("my-bucket", "my-prefix")
    #remote_device = qml.device("braket.aws.qubit", device_arn="arn:aws:braket:::device/quantum-simulator/amazon/sv1", s3_destination_folder=s3, wires=2)

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

    print('Final value of the ground-state energy = {:.8f} Ha'.format(energy))

    return {
        'statusCode': 200,
        'body': json.dumps('Final value of the ground-state energy = {:.8f} Ha'.format(energy))
    }
