document.addEventListener('DOMContentLoaded', (event) => {
    funtime();
});

function funtime() {
    const h1 = document.querySelector('h1');
    const img = document.querySelector('img');

    const minWidth = 200;
    var i = minWidth; // Start with the initial width
    const maxWidth = 300; // Maximum width for the image
    var direction = true;

    setInterval(() => {
        // Generate a random color
        const randomColor = '#' + ('000000' + Math.floor(Math.random() * 16777215).toString(16)).slice(-6);
        h1.style.color = randomColor;
    }, 200);

    setInterval(() => {
        // Increase image width and reset if it exceeds maxWidth
        img.style.width = i + "px";
        if (direction)
            i += 5;
        else
            i -= 3;

        if (i > maxWidth) {
            direction = false; // Reset to initial width
        }
        else if (i < minWidth) {
            direction = true;
        }
    }, 10);
}