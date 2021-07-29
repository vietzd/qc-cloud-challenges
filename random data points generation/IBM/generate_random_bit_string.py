from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, IBMQ, assemble, transpile, execute

def main(dict):
    number = dict["number_of_bits"]
    ibmq_token = dict["ibmq_token"]
    print('Generate', number, 'Bit random number...')

    # Set IBMQ_TOKEN
    try:
        provider = IBMQ.enable_account(ibmq_token)
        print('IBMQ_TOKEN activated')
    except:
        IBMQ.disable_account()
        provider = IBMQ.enable_account(ibmq_token)
        print('Disabled old and activated new IBMQ_TOKEN')

    # Execution (Max 32 bits at once)
    howmanytimes = int(number/32)
    last_circuit_size = number%32
    result = ''
    for i in range(howmanytimes):
        result += random_bitstring(32, provider)
    if (last_circuit_size > 0):
        result += random_bitstring(last_circuit_size, provider)

    try:
        IBMQ.disable_account()
        print('IBMQ_TOKEN disabled')
    except:
        print('No IBMQ_TOKEN to disable')

    return ({"random_bitstring": result})
    # TODO: call assemble_and_store_random_data_points.py directly



def random_bitstring(number, provider):
    # Circuit
    qr = QuantumRegister(number, 'qr')
    cr = ClassicalRegister(number, 'cr')
    circuit = QuantumCircuit(qr, cr)
    circuit.h(qr[0:number])
    circuit.measure(qr, cr)

    # # Execute Job at IBMQ Backend
    backend = provider.backends.ibmq_qasm_simulator
    qobj = assemble(transpile(circuit, backend=backend), backend=backend, shots=1)
    print('Send job to IBMQ backend')
    job = backend.run(qobj)
    retrieved_job = backend.retrieve_job(job.job_id())
    result = retrieved_job.result().get_counts().most_frequent()
    return result