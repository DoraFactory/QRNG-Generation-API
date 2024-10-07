from flask import Flask, request, jsonify
from IBM_QBraid_DataGeneration import launch_job, get_job_status, get_job_results, get_job_results_uniform_randomness
import json
import os
import waitress

app = Flask(__name__)

API_Keys = os.getenv('API_Keys')

max_shots_allowed = 100*10000

allowed_devices = ['ibm_brisbane', 'ibm_kyiv', 'ibm_sherbrooke']

def check_authorization():
    if 'API-Key' not in request.headers:
        return 'ERROR: Please provide an "API-Key" header in your HTTP request with your API Key to access this endpoint'
    if request.headers['API-Key'] not in API_Keys:
        return 'ERROR: Provided API key is either not authorized to access this endpoint or does not exist. Re-check to see if your key is entered correctly or contact Dora Factory for a valid API key'
    return 'True'


@app.route('/QRNG/SubmitJob', methods=['GET'])
def launchJob():
    auth_message = check_authorization()
    if auth_message != 'True':
        return auth_message
    
    length = request.args.get('length', default=100, type=int)
    number = request.args.get('number', default=1, type=int)
    if not (length > 0 and number > 0):
        return 'ERROR: both the length and number parameters for requested QRNG data must be positive integers'
    if (length % 100)  != 0:
        return 'ERROR: requested QRNG number line length must be a multiple of 100'
    if number * length > max_shots_allowed:
        return f'ERROR: requested data exceeds allowed shot count of {max_shots_allowed}: reduce requested length of random number or number of lines'
    
    QPU = request.args.get('QPU', None)
    if QPU and (QPU not in allowed_devices):
        return f'ERROR: requested quantum device cannot be accessed or does not exist: either do not pass in a QPU as a URL parameter, in which case the least busy IBM quantum computer will be used, or pass in one of the following device tags: {allowed_devices}'

    output = launch_job(length, number, QPU)
    return output

@app.route('/QRNG/JobStatus', methods=['GET'])
def getJobStatus():
    auth_message = check_authorization()
    if auth_message != 'True':
        return auth_message
    
    if 'jobID' not in request.args:
        return 'ERROR: must provide valid Quantum Job ID as URL HTTP parameter with attribute name = "jobID"'
    
    jobID = request.args.get('jobID')
    return get_job_status(jobID)

@app.route('/QRNG/JobResults', methods=['GET'])
def getJobResults():
    auth_message = check_authorization()
    if auth_message != 'True':
        return auth_message
    
    if 'jobID' not in request.args:
        return 'ERROR: must provide valid Quantum Job ID as URL HTTP parameter with attribute name = "jobID"'
    
    jobID = request.args.get('jobID')
    return (get_job_results(jobID))

@app.route('/QRNG/JobResultsUniformRandomness', methods=['GET'])
def getJobResultsToeplitz():
    auth_message = check_authorization()
    if auth_message != 'True':
        return auth_message
    
    if 'jobID' not in request.args:
        return 'ERROR: must provide valid Quantum Job ID as URL HTTP parameter with attribute name = "jobID"'
    
    jobID = request.args.get('jobID')
    return (get_job_results_uniform_randomness(jobID))

if __name__ == '__main__':
    waitress.serve(app, host='0.0.0.0', port=8080)