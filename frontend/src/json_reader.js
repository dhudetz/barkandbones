document.addEventListener('DOMContentLoaded', () => {
    fetch('content/content.json')
        .then(response => response.json())
        .then(data => {
            // Select all <p> elements with the 'json' class
            document.querySelectorAll('p.json').forEach(p => {
                // Use the id of the <p> element to get the corresponding data
                const content = data[p.id];
                if (content) {
                    p.textContent = content;
                }
            });
        })
        .catch(error => console.error('Error fetching data:', error));
});