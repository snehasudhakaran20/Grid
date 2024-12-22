
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests


@app.route('/api/run_algorithm1', methods=['POST'])
def run_algorithm1():
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



def amaze(grid):
    # 
    return [{0,0,0} for r, g, b in (rgb.split(",") for rgb in grid)]

def ppg(grid):
      return [{0,0,255} for r, g, b in (rgb.split(",") for rgb in grid)] 
   # return [f"{int(r)*2%256},{int(0)*2%256},{int(b)*2%256}" for r, g, b in (rgb.split(",") for rgb in grid)]

def vng(grid):
    return [{0,255,0} for r, g, b in (rgb.split(",") for rgb in grid)]

    #return [f"{255-int(r)},{int(g)},{int(0)}" for r, g, b in (rgb.split(",") for rgb in grid)]

def edge_detect(grid):
    return [{255,0,0} for r, g, b in (rgb.split(",") for rgb in grid)]

    #return [f"{max(0, int(0)-50)},{max(0, int(0)-50)},{max(0, int(0)-50)}" for r, g, b in (rgb.split(",") for rgb in grid)]

def gaussian_blur(grid):
    sigma=1
    kernel=gaussian_kernel(10,sigma)
    updated_grid=apply_gaussian_blur(grid,kernel)
    
    return jsonify({'grid': updated_grid})

@app.route('/run_algorithm', methods=['POST'])
def run_algorithm():
    data = request.json
    grid = data.get('grid', [])
    algorithm = data.get('algorithm')

    if not grid or not algorithm:
        return jsonify({'error': 'Invalid input data'}), 400

    # Select and execute the appropriate algorithm
    if algorithm == "gaussian_blur":
        updated_grid = gaussian_blur(grid)
    elif algorithm == "amaze":
        updated_grid = amaze(grid)
    elif algorithm == "ppg":
        updated_grid = ppg(grid)
    elif algorithm == "vng":
        updated_grid = vng(grid)
    elif algorithm == "edge_detect":
        updated_grid = edge_detect(grid)
    else:
        return jsonify({'error': 'Unknown algorithm'}), 400

    return jsonify({'grid': updated_grid})   

if __name__ == '__main__':
    app.run(debug=True)
