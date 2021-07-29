import json
import boto3
from braket.aws import AwsDevice
from braket.devices import LocalSimulator
from braket.circuits import Circuit

def lambda_handler(event, context):
    number = event["number"]
    max_number = 10
    howmanytimes = int(number/max_number)
    last_circuit_size = number%max_number
    result = ''
    for i in range(howmanytimes):
        result += random_bitstring(max_number)
    if (last_circuit_size > 0):
        result += random_bitstring(last_circuit_size)
    print(result)

    return {
        'statusCode': 200,
        'body': result
    }

def random_bitstring(number):
    # Circuit
    circ = Circuit()
    for i in range(number):
        circ.h(i)

    device = LocalSimulator()
    #device = AwsDevice("arn:aws:braket:::device/quantum-simulator/amazon/sv1")
    #s3_folder = ("amazon-braket-Your-Bucket-Name", "folder-name")

    # run the circuit
    result = device.run(circ, shots=1).result()
    #task = device.run(bell, s3_folder, shots=1)
    counts = result.measurement_counts
    res = next(iter(counts))
    return res