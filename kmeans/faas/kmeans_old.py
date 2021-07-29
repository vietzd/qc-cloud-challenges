#
# Source: https://github.com/smit14/Quantum-K-means-algorithm/blob/master/k_means_quantum.ipynb
#
import numpy as np
import math
from math import pi
from qiskit import Aer, IBMQ, execute
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
import random


def get_theta(d):
    x = d[0]
    y = d[1]
    theta = 2*math.acos((x+y)/2.0)
    return theta


def get_Distance(x,y):
    theta_x = get_theta(x)
    theta_y = get_theta(y)

    qr = QuantumRegister(3, name="qr")
    cr = ClassicalRegister(3, name="cr")
    qc = QuantumCircuit(qr, cr, name="k_means")
    qc.h(qr[0])
    qc.h(qr[1])
    qc.h(qr[2])
    qc.u(theta_x, pi, pi, qr[1])
    qc.u(theta_y, pi, pi, qr[2])
    qc.cswap(qr[0], qr[1], qr[2])
    qc.h(qr[0])
    qc.measure(qr[0], cr[0])
    qc.reset(qr)

    backend = Aer.get_backend('qasm_simulator')
    job = execute(qc,backend=backend, shots=1024)
    data = job.result().get_counts(qc)

    if len(data)==1:
        return 0.0
    else:
        return data['001']/1024.0


def find_nearest_neighbour(points,centroids):
    n = len(points)
    k = len(centroids)
    centers = np.zeros(n)
    for i in range(n):
        min_dis = 10000
        ind = 0
        for j in range(k):
            temp_dis = get_Distance(points[i],centroids[j])
            if temp_dis < min_dis:
                min_dis = temp_dis
                ind = j
        centers[i] = ind
    return centers


def find_centroids(points,centers,k):
    n = len(points)
    centroids = [[0,0],[0,0],[0,0]]
    for i in range(k):
        sum_x = 0.0
        sum_y = 0.0
        count = 0
        for j in range(n):
            if(centers[j] == i):
                sum_x += points[j][0]
                sum_y += points[j][1]
                count += 1
        if (count == 0):
            centroids[i] = [0,0]
        else:
            centroids[i] = [sum_x/count, sum_y/count]
    return centroids


# Normalize
def preprocess(points):
    n = len(points)
    x = 30.0*np.sqrt(2)
    for i in points:
        i[0]+=15
        i[0]/=x
        i[1]+=15
        i[1]/=x
    return points

def initialize_centers_randomly(k):
    result = [[0,0],[0,0],[0,0]]
    for i in range(k):
        result[i] = [random.uniform(0,1), random.uniform(0,1)]
    return result


def main(dict):
    k = dict['k']
    iterations = dict['iterations']
    points = [[2.83074041, -3.40417462], [-1.88863985, 7.40552553], [1.31045817, -6.57269896], [-11.07281298, -5.93492344], [-2.42570216, 7.76584962]]
    points = preprocess(points)
    centroids = initialize_centers_randomly(k)

    # run k-means algorithm
    for i in range(iterations):
        centers = find_nearest_neighbour(points,centroids)       # find nearest centers
        print(centers)
        centroids = find_centroids(points,centers, k)               # find centroids
        print(centroids)
    return centroids

#main({'k': 3, 'iterations': 10})
