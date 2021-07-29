from qiskit import QuantumRegister, ClassicalRegister
from qiskit import QuantumCircuit
from qiskit import Aer, execute
from numpy import pi

def main(dict):
    x_p = dict['point']['x']
    y_p = dict['point']['y']
    centroids = dict['centroids']
    x_list = [x_p]
    y_list = [y_p]
    for centroid in centroids:
        x_list.append(centroid['x'])
        y_list.append(centroid['y'])

    phi_list = [((x + 1) * pi / 2) for x in x_list]
    print("Phi-list (first is new point):", phi_list)
    theta_list = [((x + 1) * pi / 2) for x in y_list]
    print("Theta-list (first is new point):", theta_list)

    qreg = QuantumRegister(3, 'qreg')
    creg = ClassicalRegister(1, 'creg')
    qc = QuantumCircuit(qreg, creg, name='qc')
    backend = Aer.get_backend('qasm_simulator')

    centroid_distances = []
    for i in range(1, len(centroids)+1):
        qc.h(qreg[2])
        # Encode new point and centroid
        qc.u(theta_list[0], phi_list[0], 0, qreg[0])
        qc.u(theta_list[i], phi_list[i], 0, qreg[1])
        # Controlled Swap
        qc.cswap(qreg[2], qreg[0], qreg[1])
        qc.h(qreg[2])
        qc.measure(qreg[2], creg[0])
        qc.reset(qreg)

        job = execute(qc, backend=backend, shots=1024)
        result = job.result().get_counts(qc)
        centroid_distances.append(result['1'])

    print("(Quantum) Distances:", centroid_distances)
    closest = centroid_distances.index(min(centroid_distances))
    return {'Message': "The new point is closest to centroid" + str(closest)}

dict = {
    'point': {'x': 0.5, 'y': 0.5},
    'centroids': [
        {'x': -0.265, 'y': -0.265},
        {'x': 0.3733125, 'y': 0.3733125},
        {'x': 0.03875, 'y': 0.03875}
    ]
}
print(main(dict))