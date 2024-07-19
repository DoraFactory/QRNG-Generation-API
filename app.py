from flask import Flask, request, jsonify
from IBM_QBraid_DataGeneration import generate_data
import json

app = Flask(__name__)

@app.route('/QRNG/SubmitJob', methods=['GET'])
def generate_QRNG_Data():
    length = request.args.get('length', '100')
    number = request.args.get('number', '1')
    QPU = request.args.get('QPU', None)
    msg = number + ' bitstring(s) of length ' + length + ' on quantum computer ' + QPU
    print(msg)
    bitstrings = generate_data(int(length), int(number), QPU)
    return jsonify({'Requested QRNG Data': bitstrings})

@app.route('/QRNG/JobStatus/<jobID>', methods=['GET'])
def getJobStatus(jobID):
    print(jobID)
    return jsonify(str(jobID))

@app.route('/QRNG/JobResults/<jobID>', methods=['GET'])

@app.route('/test', methods=['GET'])
def test():
    return jsonify({'test': 'test'})

if __name__ == '__main__':
    app.run(debug=True)