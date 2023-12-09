function createBone() {
    const bone = document.createElement('div');
    bone.classList.add('bone');
    bone.style.left = (Math.random() * 100 - 5) + 'vw';
    bone.style.animationDuration = Math.random() * 0.3 + 0.9 + 's';

    // Array of pre-rotated bone image URLs
    const boneImages = [
        'images/bone_graphics/bone-graphic-0.png',
        'images/bone_graphics/bone-graphic-45.png',
        'images/bone_graphics/bone-graphic-90.png',
        'images/bone_graphics/bone-graphic-135.png',
    ];

    // Randomly select a rotated image
    const selectedImage = boneImages[Math.floor(Math.random() * boneImages.length)];
    bone.style.backgroundImage = `url('${selectedImage}')`;

    document.getElementById('animation-container').appendChild(bone);

    setTimeout(() => {
        bone.remove();
    }, 2000);
}



function rainBones() {
    // Start creating bones
    const intervalId = setInterval(createBone, 60);

    // Stop creating bones after 3 seconds
    setTimeout(() => {
        clearInterval(intervalId);
    }, 1500);
}
