document.addEventListener('DOMContentLoaded', () => {
    fetch('content/about_us.json')
        .then(response => response.json())
        .then(data => {
            document.getElementById('home1').textContent = data.home;
            document.getElementById('aboutUs1').textContent = data.aboutUs1;
            document.getElementById('aboutUs2').textContent = data.aboutUs2;
        })
        .catch(error => console.error('Error fetching data:', error));
});