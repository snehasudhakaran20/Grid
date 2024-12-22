document.getElementById('mathForm').addEventListener('submit', async (event) => {
  event.preventDefault();
  const inputData = document.getElementById('inputData').value;

  try {
    const response = await fetch('http://127.0.0.1:5000/api/calculate', {
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
