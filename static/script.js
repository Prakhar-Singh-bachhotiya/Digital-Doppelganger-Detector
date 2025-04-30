// JavaScript to handle form submission and display results
const userForm = document.getElementById('userForm');
const resultDiv = document.getElementById('result');

userForm.addEventListener('submit', async (event) => {
    event.preventDefault(); // Prevent the form from refreshing the page

    // Collect input data
    const formData = new FormData(userForm);
    const data = {};
    formData.forEach((value, key) => {
        data[key] = value;
    });

    // Send data to the server
    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });

        if (!response.ok) {
            throw new Error('Failed to fetch');
        }

        const result = await response.json();
        if (result.error) {
            resultDiv.innerHTML = `<div class="alert alert-danger">${result.error}</div>`;
        } else {
            const prediction = result.prediction === 1 ? "Fake Account" : "Real Account";
            resultDiv.innerHTML = `<div class="alert alert-success">Prediction: ${prediction}</div>`;
        }
    } catch (error) {
        resultDiv.innerHTML = `<div class="alert alert-danger">Error: ${error.message}</div>`;
    }
});