from flask import Flask, request, jsonify
from IBM_QBraid_DataGeneration import generate_data
import json

app = Flask(__name__)

@app.route('/generateQRNGData', methods=['GET'])
def generate_QRNG_Data():
    length = request.args.get('length', '100')
    number = request.args.get('number', '1')
    QPU = request.args.get('QPU', None)
    msg = number + ' bitstring(s) of length ' + length + ' on quantum computer ' + QPU
    print(msg)
    bitstrings = generate_data(int(length), int(number), QPU)
    return jsonify({'Requested QRNG Data': bitstrings})

if __name__ == '__main__':
    app.run(debug=True)