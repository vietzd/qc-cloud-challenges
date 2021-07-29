import json
import boto3

def lambda_handler(event, context):

    braket = boto3.client('braket')


    # Create parameters to pass into create_quantum_task()
    kwargs = {
        # Create a Bell pair
        'action': '{"braketSchemaHeader": {"name": "braket.ir.jaqcd.program", "version": "1"}, "results": [], "basis_rotation_instructions": [], "instructions": [{"type": "h", "target": 0}, {"type": "cnot", "control": 0, "target": 1}]}',
        # Specify the SV1 Device ARN
        'deviceArn': 'arn:aws:braket:::device/quantum-simulator/amazon/sv1',
        # Specify 2 qubits for the Bell pair
        'deviceParameters': '{"braketSchemaHeader": {"name": "braket.device_schema.simulators.gate_model_simulator_device_parameters", "version": "1"}, "paradigmParameters": {"braketSchemaHeader": {"name": "braket.device_schema.gate_model_parameters", "version": "1"}, "qubitCount": 2}}',
        # Specify where results should be placed when the quantum task completes.
        #  You must ensure the S3 Bucket exists before calling create_quantum_task()
        'outputS3Bucket': 'amazon-braket-6ca17c5fc378',
        'outputS3KeyPrefix': 'boto-examples',
        # Specify number of shots for the quantum task
        'shots': 1
    }

    # Send the request and capture the response
    response = braket.create_quantum_task(**kwargs)

    print(f"Quantum task {response['quantumTaskArn']} created")


    # TODO implement
    return {
        'statusCode': 200,
        'response': response
    }
