
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

@app.route('/api/calculate', methods=['POST'])
def calculate():
    data = request.json
    input_value = int(data.get('input', 0))
    # Example algorithm: square the input
    result = input_value ** 2
    return jsonify({'output': result})

if __name__ == '__main__':
    app.run(debug=True)
