
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests


@app.route('/api/run_algorithm', methods=['POST'])
def run_algorithm():
    data = request.json
    grid = data.get('grid', [])
    
    if not grid:
        return jsonify({'error': 'Invalid grid data'}), 400
    
    # Example processing: Compute new grid values by inverting RGB
    updated_grid = []
    for rgb in grid:
        r, g, b = map(int, rgb.split(','))
        {updated_r,updated_g,updated_b} = same_values(r,g,b)
        updated_grid.append(f"{updated_r},{updated_g},{updated_b}")
    
    return jsonify({'grid': updated_grid})

def same_values(r,g,b):
    r1=r
    b1=b
    g1=g
    return r1,b1,g1

def gaussian_blur():
    

if __name__ == '__main__':
    app.run(debug=True)
