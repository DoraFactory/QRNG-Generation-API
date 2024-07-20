from flask import Flask, request, jsonify
from IBM_QBraid_DataGeneration import launch_job, get_job_status, get_job_results
import json

app = Flask(__name__)

#***TO-DO: implement error handling

@app.route('/QRNG/SubmitJob', methods=['GET'])
def launchJob():
    length = request.args.get('length', '100')
    number = request.args.get('number', '1')
    QPU = request.args.get('QPU', None)
    msg = number + ' bitstring(s) of length ' + length + ' on quantum computer ' + QPU
    print(msg)
    output = launch_job(int(length), int(number), QPU)
    return output

@app.route('/QRNG/JobStatus/<jobID>', methods=['GET'])
def getJobStatus(jobID):
    return get_job_status(jobID)

@app.route('/QRNG/JobResults/<jobID>', methods=['GET'])
def getJobResults(jobID):
    return jsonify({'data': get_job_results(jobID)})

@app.route('/test', methods=['GET'])
def test():
    return jsonify({'test': 'test'})

if __name__ == '__main__':
    app.run(debug=True)