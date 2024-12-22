// Function to initialize a 10x10 grid with empty values
function initializeGrid() {
    const grid = [];
    for (let i = 0; i < 10; i++) {
        const row = [];
        for (let j = 0; j < 10; j++) {
            row.push({ red: null, green: null, blue: null }); // Empty values
        }
        grid.push(row);
    }
    return grid;
}

// Render the grid in the table on the webpage
function renderGrid(grid) {
    const table = document.getElementById('gridTable');
    table.innerHTML = ''; // Clear existing content

    grid.forEach((row, rowIndex) => {
        const tr = document.createElement('tr');
        row.forEach((cell, colIndex) => {
            const td = document.createElement('td');
            td.classList.add('grid-cell');
            td.setAttribute('data-row', rowIndex);
            td.setAttribute('data-col', colIndex);
            td.innerHTML = `
                <input type="number" placeholder="R" data-color="red" value="${cell.red ?? ''}">
                <input type="number" placeholder="G" data-color="green" value="${cell.green ?? ''}">
                <input type="number" placeholder="B" data-color="blue" value="${cell.blue ?? ''}">
            `;
            tr.appendChild(td);
        });
        table.appendChild(tr);
    });
}

// Collect grid values from the inputs
function getGridFromInputs() {
    const grid = [];
    const rows = document.querySelectorAll('#gridTable tr');
    rows.forEach((row, rowIndex) => {
        const cells = row.querySelectorAll('td');
        const gridRow = [];
        cells.forEach(cell => {
            const red = cell.querySelector('[data-color="red"]').value || null;
            const green = cell.querySelector('[data-color="green"]').value || null;
            const blue = cell.querySelector('[data-color="blue"]').value || null;
            gridRow.push({
                red: red ? parseInt(red) : null,
                green: green ? parseInt(green) : null,
                blue: blue ? parseInt(blue) : null
            });
        });
        grid.push(gridRow);
    });
    return grid;
}

// Send grid to Python API and update the table with new values
async function processGrid() {
    const grid = getGridFromInputs();
    try {
        const response = await fetch('https://demosaicing-math.onrender.com/api/process-grid', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ grid })
        });
        const result = await response.json();
        renderGrid(result.grid); // Update the grid with new values
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to process grid. Please try again.');
    }
}

// Initialize the grid on page load
document.addEventListener('DOMContentLoaded', () => {
    const grid = initializeGrid();
    renderGrid(grid);

    // Set up the process button
    const processButton = document.getElementById('processButton');
    processButton.addEventListener('click', processGrid);
});
