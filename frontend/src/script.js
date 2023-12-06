document.addEventListener('DOMContentLoaded', (event) => {
    funtime();
    setupEventSource();
});

function funtime() {
    const h1 = document.querySelector('h1');
    const img = document.querySelector('img');

    const minWidth = 250; // Minimum width
    const maxWidth = 300; // Maximum width
    const amplitude = (maxWidth - minWidth) / 2; // Amplitude of the sine wave
    const midWidth = minWidth + amplitude; // Middle width value
    let angle = 0; // Angle for the sine wave

    setInterval(() => {
        // Generate a random color
        const randomColor = '#' + ('000000' + Math.floor(Math.random() * 16777215).toString(16)).slice(-6);
        h1.style.color = randomColor;
    }, 200);

    setInterval(() => {
        // Calculate the new width using sine wave
        img.style.width = (midWidth + amplitude * Math.sin(angle)) + "px";

        angle += 0.05; // Increment the angle for the next frame
    }, 10);
}

function setupEventSource() {
    const h1 = document.querySelector('h1');
    const eventSource = new EventSource(`${config.API_BASE_URL}/api`);

    eventSource.onmessage = (event) => {
        const parsedData = JSON.parse(event.data);
        h1.textContent += parsedData.message;
    };

    eventSource.onerror = (error) => {
        console.error('EventSource failed:', error);
        eventSource.close();
    };
}
