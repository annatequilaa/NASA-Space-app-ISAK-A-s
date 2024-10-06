// Array of video objects
const videos = [
    {
        src: 'video1.mp4',
        title: 'Video Title 1',
        description: 'Description of the first video.'
    },
    {
        src: 'video2.mp4',
        title: 'Video Title 2',
        description: 'Description of the second video.'
    },
    {
        src: 'video3.mp4',
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
