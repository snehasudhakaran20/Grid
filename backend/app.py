
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


@app.route('/api/process-grid', methods=['POST'])
def process_grid():
    data = request.json
    grid = data['grid']

    # Process the grid using the previously provided algorithm
    filled_grid = fill_missing_colors(grid)  # Call your grid processing function

    return jsonify({"grid": filled_grid})




if __name__ == '__main__':
    app.run(debug=True)

def fill_missing_colors(grid):
    # Helper function to find the average of non-zero neighbors in opposite directions
    def average_neighbors(grid, x, y, color):
        values = []
        
        # Search left and right
        for dx in [-1, 1]:
            nx = x + dx
            while 0 <= nx < 10:
                if grid[nx][y][color] is not None:
                    values.append(grid[nx][y][color])
                    break
                nx += dx
        
        # Search up and down
        for dy in [-1, 1]:
            ny = y + dy
            while 0 <= ny < 10:
                if grid[x][ny][color] is not None:
                    values.append(grid[x][ny][color])
                    break
                ny += dy
        
        # Return the average if values are found, else None
        return sum(values) / len(values) if values else None

    # Iterate through each cell in the grid
    for x in range(10):
        for y in range(10):
            cell = grid[x][y]
            # Fill red if missing
            if cell['red'] is None:
                cell['red'] = average_neighbors(grid, x, y, 'red')
            # Fill green if missing
            if cell['green'] is None:
                cell['green'] = average_neighbors(grid, x, y, 'green')
            # Fill blue if missing
            if cell['blue'] is None:
                cell['blue'] = average_neighbors(grid, x, y, 'blue')
    
    return grid

# Example Usage
# Initialize a 10x10 grid with some missing values
grid = [
    [{'red': None, 'green': 50, 'blue': None} for _ in range(10)]
    for _ in range(10)
]
# Set some non-zero values
grid[0][0]['red'] = 100
grid[1][1]['blue'] = 200
grid[2][2]['green'] = 150
grid[9][9]['red'] = 50

# Fill missing colors
filled_grid = fill_missing_colors(grid)

# Print the result
for row in filled_grid:
    print(row)
