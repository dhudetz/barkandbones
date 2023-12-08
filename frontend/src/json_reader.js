document.addEventListener('DOMContentLoaded', () => {
    fetch('content/about_us.json')
        .then(response => response.json())
        .then(data => {
            document.getElementById('infoParagraph1').textContent = data.info1;
            document.getElementById('infoParagraph2').textContent = data.info2;
            document.getElementById('infoParagraph3').textContent = data.info3;
        })
        .catch(error => console.error('Error fetching data:', error));
});