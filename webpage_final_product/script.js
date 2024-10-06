// Array of video objects
const videos = [
    {
        src: 'https://drive.google.com/file/d/1Kca0AoCyfqSz_EL2CGjdeAeqxOmfcIjw/view?usp=drive_link',
        title: 'Nebula',
        description: 'This is a purple neblua (we'll change the caption based on the NASA website's information.'
    },
    {
        src: 'https://drive.google.com/file/d/1aoa1VW96dsn7dETOU5XDJMH0lqMxeZwB/view?usp=drive_link',
        title: 'Video Title 2',
        description: 'Description of the second video.'
    },
    {
        src: 'https://drive.google.com/file/d/1Ldj8sRJf5AAN5DPhN4w5pBCMbrnFS4Ua/view?usp=drive_link',
        title: 'Video Title 3',
        description: 'Description of the third video.'
    }
];

// Current video index
let currentIndex = 0;

// Function to update the video player
function updateVideo() {
    const videoPlayer = document.getElementById('video-player');
    const videoTitle = document.getElementById('video-title');
    const videoDescription = document.getElementById('video-description');

    // Update video source and reload
    videoPlayer.src = videos[currentIndex].src;
    videoTitle.textContent = videos[currentIndex].title;
    videoDescription.textContent = videos[currentIndex].description;
    videoPlayer.load();
}

// Event listeners for buttons
document.getElementById('prev-btn').addEventListener('click', () => {
    currentIndex = (currentIndex > 0) ? currentIndex - 1 : videos.length - 1;
    updateVideo();
});

document.getElementById('next-btn').addEventListener('click', () => {
    currentIndex = (currentIndex < videos.length - 1) ? currentIndex + 1 : 0;
    updateVideo();
});

// Initial video load
updateVideo();
