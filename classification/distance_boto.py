import json
import math
from math import pi
import boto3

braket = boto3.client('braket')

def get_theta(d):
    x = d[0]
    y = d[1]
    theta = 2*math.acos((x+y)/2.0)
    return theta

def lambda_handler(event, context):
    x = event['x']
    y = event['y']
    theta_1 = get_theta(x)
    theta_2 = get_theta(y)

    print("theta1: " + str(theta_1))
    print("theta2: " + str(theta_2))

    instructions = '['
    instructions += '{"type": "h", "target": 0},'
    instructions += '{"type": "rx", "target": 1, "angle": '+str(theta_1)+'},'
    instructions += '{"type": "rx", "target": 2, "angle": '+str(theta_2)+'},'
    #instructions += '{"type": "cswap", "control": 0, "targets": [0, 1]},'
    instructions += '{"type": "h", "target": 0}'
    instructions += ']'


    # Create parameters to pass into create_quantum_task()
    kwargs = {
        # Create a Bell pair
        'action': '{"braketSchemaHeader": {"name": "braket.ir.jaqcd.program", "version": "1"}, "results": [], "basis_rotation_instructions": [], "instructions": '+instructions+'}',
        # Specify the SV1 Device ARN
        'deviceArn': 'arn:aws:braket:::device/quantum-simulator/amazon/sv1',
        # Specify 2 qubits for the Bell pair
        'deviceParameters': '{"braketSchemaHeader": {"name": "braket.device_schema.simulators.gate_model_simulator_device_parameters", "version": "1"}, "paradigmParameters": {"braketSchemaHeader": {"name": "braket.device_schema.gate_model_parameters", "version": "1"}, "qubitCount": 3}}',
        # Specify where results should be placed when the quantum task completes.
        #  You must ensure the S3 Bucket exists before calling create_quantum_task()
        'outputS3Bucket': 'amazon-braket-6ca17c5fc378',
        'outputS3KeyPrefix': 'boto-examples',
        # Specify number of shots for the quantum task
        'shots': 1
    }

    # Send the request and capture the response
    response = braket.create_quantum_task(**kwargs)

    return {
        'statusCode': 200,
        'instructions': instructions,
        'braket-response': response
    }