import requests

#Functional test method for job submission endpoint
def testJobSubmissionEndpoint(length=None, number=None, QPU=None, header='API-Key', apiKey='abcd'):
    url = f'http://127.0.0.1:5000/QRNG/SubmitJob?'
    if length != None:
        url += f'length={length}&'
    if number != None:
        url += f'number={number}&'
    if QPU:
        url += f'QPU={QPU}&'
    url = url[:-1]
    print(url)
    response = requests.get(url, headers={header: apiKey})
    output = 'actual output: ' + response.text
    print(output)


#functional tests for all possible job submission codepath errors
def jobSubmissionFunctionalTests():
    #Testing improper API key configurations

    testJobSubmissionEndpoint(header='APIKey', apiKey='abcd')
    print('expected output: ERROR: Please provide an "API-Key" header in your HTTP request with your API Key to access this endpoint\n')

    testJobSubmissionEndpoint(header='APIKey', apiKey='notinkeydb')
    print('expected output: ERROR: Please provide an "API-Key" header in your HTTP request with your API Key to access this endpoint\n')

    testJobSubmissionEndpoint(header='Api-Key', apiKey='notinkeydb')
    print('expected output: ERROR: Provided API key is either not authorized to access this endpoint or does not exist. Re-check to see if your key is entered correctly or contact Dora Factory for a valid API key\n')

    testJobSubmissionEndpoint(header='API-Key', apiKey='notinkeydb')
    print('expected output: ERROR: Provided API key is either not authorized to access this endpoint or does not exist. Re-check to see if your key is entered correctly or contact Dora Factory for a valid API key\n')

    testJobSubmissionEndpoint(header='API-Key', apiKey='ABCD')
    print('expected output: ERROR: Provided API key is either not authorized to access this endpoint or does not exist. Re-check to see if your key is entered correctly or contact Dora Factory for a valid API key\n')

    print('\n\n\n')


    #Testing error handling for length, number, QPU inputs

    testJobSubmissionEndpoint(number=0, length=0)
    print('expected output: ERROR: both the length and number parameters for requested QRNG data must be positive integers\n')

    testJobSubmissionEndpoint(length=-5)
    print('expected output: ERROR: both the length and number parameters for requested QRNG data must be positive integers\n')

    testJobSubmissionEndpoint(number=0)
    print('expected output: ERROR: both the length and number parameters for requested QRNG data must be positive integers\n')

    testJobSubmissionEndpoint(number=-5)
    print('expected output: ERROR: both the length and number parameters for requested QRNG data must be positive integers\n')

    testJobSubmissionEndpoint(number=1, length=0)
    print('expected output: ERROR: both the length and number parameters for requested QRNG data must be positive integers\n')

    testJobSubmissionEndpoint(length=50)
    print('expected output: ERROR: requested QRNG number line length must be a multiple of 100\n')

    testJobSubmissionEndpoint(length=101)
    print('expected output: ERROR: requested QRNG number line length must be a multiple of 100\n')

    testJobSubmissionEndpoint(length=100*(10000+1))
    print(f'expected output: ERROR: requested data exceeds allowed shot count of {100*10000}: reduce requested length of random number or number of lines\n')

    testJobSubmissionEndpoint(number=100*10000+1)
    print(f'expected output: ERROR: requested data exceeds allowed shot count of {100*10000}: reduce requested length of random number or number of lines\n')

    testJobSubmissionEndpoint(number=10000, length=200)
    print(f'expected output: ERROR: requested data exceeds allowed shot count of {100*10000}: reduce requested length of random number or number of lines\n')

    testJobSubmissionEndpoint(QPU='IBM_Brisbane')
    print(f'expected output: ERROR: requested quantum device cannot be accessed or does not exist: either do not pass in a QPU as a URL parameter, in which case the least busy IBM quantum computer will be used, or pass in one of the following device tags: \n')

    testJobSubmissionEndpoint(QPU='dfhdf')
    print(f'expected output: ERROR: requested quantum device cannot be accessed or does not exist: either do not pass in a QPU as a URL parameter, in which case the least busy IBM quantum computer will be used, or pass in one of the following device tags: \n')

    testJobSubmissionEndpoint(QPU='ibm_fez')
    print(f'expected output: ERROR: requested quantum device cannot be accessed or does not exist: either do not pass in a QPU as a URL parameter, in which case the least busy IBM quantum computer will be used, or pass in one of the following device tags: \n')


    #testing succesul calls

    testJobSubmissionEndpoint(length=200, number=50, QPU='ibm_brisbane')
    print(f'expected output: succesful completion\n')

    testJobSubmissionEndpoint(header='API-Key', apiKey='1234')
    print('expected output: Succesful completion\n')

#jobSubmissionFunctionalTests()


response = requests.get('http://127.0.0.1:5000/QRNG/JobResults?jobID=ctfgam2zhysg008t577g', headers = {'API-Key': 'abcd'})
print(response.text)