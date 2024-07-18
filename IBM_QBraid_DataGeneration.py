from qbraid.runtime.qiskit import QiskitRuntimeProvider

from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit.circuit.library import QuantumVolume
from qiskit.visualization.counts_visualization import plot_histogram
from qiskit import QuantumCircuit

import numpy as np

import os
from dotenv import load_dotenv

allowed_devices = ['ibm_brisbane', 'ibm_kyoto', 'ibm_sherbrooke', 'ibm_osaka']

def generate_data(length, numLines, machine=None):
    load_dotenv()
    API_KEY = os.getenv('IBM_APIKEY')
    provider = QiskitRuntimeProvider(API_KEY)
    
    HGate_circ = QuantumCircuit(4)
    HGate_circ.h(0)
    HGate_circ.h(1)
    HGate_circ.h(2)
    HGate_circ.h(3)
    HGate_circ.measure_all()

    if not machine:
        #implement finding qpu with lowest job_count and/or wait_time
        pass
    else:
        device = provider.get_device(machine)
        print('device obtained')

        pm = generate_preset_pass_manager(optimization_level=1, target=device._backend.target)
        transpiled_circuit = pm.run(HGate_circ)
        shot_count = (length*numLines)/4
        job = device.run(transpiled_circuit, shots=shot_count, memory=True)
        print('job running')

        result = job.result()
        rawData = result.measurements()
        print('job completed')

        unbrokenData = []
        for shot in rawData:
            for meas in shot:
                unbrokenData.append(meas)

        results = []
        for i in range(0, len(unbrokenData), length):
            results.append(''.join(map(str, unbrokenData[i:i+length])))

        print(results)

        return results