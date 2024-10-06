const videoPlayer = document.getElementById("video-player");
const videoTitle = document.getElementById("video-title");
const videoDescription = document.getElementById("video-description");

const videos = [
  {
    src: "video1.mp4",
    title: "Video Title 1",
    description: "Description of the first video."
  },
  {
    src: "video2.mp4",
    title: "Video Title 2",
    description: "Description of the second video."
  },
  {
    src: "video3.mp4",
    title: "Video Title 3",
    description: "Description of the third video."
  }
];

let currentIndex = 0;

function updateVideo(index) {
  videoPlayer.src = videos[index].src;
  videoTitle.textContent = videos[index].title;
  videoDescription.textContent = videos[index].description;
}

document.getElementById("prev-btn").addEventListener("click", () => {
  currentIndex = currentIndex > 0 ? currentIndex - 1 : videos.length - 1;
  updateVideo(currentIndex);
});

document.getElementById("next-btn").addEventListener("click", () => {
  currentIndex = currentIndex < videos.length - 1 ? currentIndex + 1 : 0;
  updateVideo(currentIndex);
});

// Handle image upload
const uploadInput = document.getElementById("upload-input");
const uploadedImage = document.getElementById("uploaded-image");

uploadInput.addEventListener("change", function () {
  const file = this.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = function (e) {
      uploadedImage.src = e.target.result;
      uploadedImage.classList.remove("hidden");
    };
    reader.readAsDataURL(file);
  }
});
