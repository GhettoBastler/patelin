const apiURL = 'api/';
const townNameElement = document.getElementById('townName');
const generateButtonElement = document.getElementById('generateButton');

function generateName(){
    generateButtonElement.setAttribute('value', '...');
    generateButtonElement.setAttribute('disabled', '');
    fetch(apiURL)
        .then(response => {
            if (!response.ok) {
                throw new Error('API response was not OK');
            }
            return response.json();
        })
        .then(data => {
            townNameElement.innerHTML = data['name'];
            generateButtonElement.setAttribute('value', 'Generate');
            generateButtonElement.removeAttribute('disabled');
        })
        .catch(error => {
            console.error('Error:', error);
        });
};

generateButtonElement.onclick = generateName;
window.onload = generateName;
