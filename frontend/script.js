const grid1 = document.getElementById('grid1');
const grid2 = document.getElementById('grid2');
const resetButton = document.getElementById('reset');
const runButton = document.getElementById('run');

let selectedSquare = null;

function createDropdown(square) {
    const dropdown = document.createElement('div');
    dropdown.className = 'dropdown';
    dropdown.innerHTML = `
        <label>R: <select data-color="r">
            <option value="0">0</option>
            <option value="127">127</option>
            <option value="255">255</option>
        </select></label><br>
        <label>G: <select data-color="g">
            <option value="0">0</option>
            <option value="127">127</option>
            <option value="255">255</option>
        </select></label><br>
        <label>B: <select data-color="b">
            <option value="0">0</option>
            <option value="127">127</option>
            <option value="255">255</option>
        </select></label><br>
    `;

    dropdown.addEventListener('change', () => {
        const r = dropdown.querySelector('[data-color="r"]').value;
        const g = dropdown.querySelector('[data-color="g"]').value;
        const b = dropdown.querySelector('[data-color="b"]').value;
        square.style.backgroundColor = `rgb(${r}, ${g}, ${b})`;
        square.dataset.rgb = `${r},${g},${b}`;
    });

    return dropdown;
}

function createGrid(container, isOutput = false) {
    for (let i = 0; i < 100; i++) {
        const square = document.createElement('div');
        square.className = 'square';

        if (!isOutput) {
            square.addEventListener('click', (e) => {
                e.stopPropagation();

                if (selectedSquare && selectedSquare !== square) {
                    selectedSquare.querySelector('.dropdown').style.display = 'none';
                }

                if (!square.querySelector('.dropdown')) {
                    const dropdown = createDropdown(square);
                    square.appendChild(dropdown);
                }

                square.querySelector('.dropdown').style.display = 'block';
                selectedSquare = square;
            });

            square.dataset.rgb = "255,255,255";
        }

        container.appendChild(square);
    }
}

document.addEventListener('click', (e) => {
    if (selectedSquare && (!selectedSquare.contains(e.target) && !e.target.closest('.dropdown'))) {
        selectedSquare.querySelector('.dropdown').style.display = 'none';
        selectedSquare = null;
    }
});

resetButton.addEventListener('click', () => {
    document.querySelectorAll('#grid1 .square').forEach(square => {
        square.style.backgroundColor = 'white';
        square.dataset.rgb = "255,255,255";
    });
});

runButton.addEventListener('click', async () => {
    const gridValues = Array.from(document.querySelectorAll('#grid1 .square')).map(square => square.dataset.rgb);

    const response = await fetch('/run_algorithm', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ grid: gridValues })
    });

    const result = await response.json();
    const updatedGridValues = result.grid;

    const squares = document.querySelectorAll('#grid2 .square');
    updatedGridValues.forEach((rgb, index) => {
        squares[index].style.backgroundColor = `rgb(${rgb})`;
    });
});

createGrid(grid1);
createGrid(grid2, true);
