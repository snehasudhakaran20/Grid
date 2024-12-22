document.getElementById('mathForm').addEventListener('submit', async (event) => {
  event.preventDefault();
  const inputData = document.getElementById('inputData').value;
  const inputDataGrid = document.getElementById('inputData').value;

  try {
    const response = await fetch('https://demosaicing-math.onrender.com/api/calculate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ input: inputData })
    });

    try {
    const response1 = await fetch('https://demosaicing-math.onrender.com/api/fillmissingcolours', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ input: inputData })
    });
      
    const result = await response.json();
    document.getElementById('result').innerText = `Result: ${result.output}`;
  } catch (error) {
    console.error('Error:', error);
    document.getElementById('result').innerText = 'An error occurred.';
  }
});
