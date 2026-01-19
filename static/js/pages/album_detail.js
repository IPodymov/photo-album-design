function copyLink() {
  var copyText = document.getElementById('shareLink');
  copyText.select();
  copyText.setSelectionRange(0, 99999);
  navigator.clipboard.writeText(copyText.value);
  alert('Ссылка скопирована в буфер обмена!');
}

// Lightbox functionality
let currentPhotoIndex = 0;
let photoImages = [];

// Initialize photo images array
document.addEventListener('DOMContentLoaded', function() {
  const photoImgs = document.querySelectorAll('.photo-img');
  photoImages = Array.from(photoImgs).map(img => img.src);
});

function openLightbox(index) {
  currentPhotoIndex = index;
  const lightbox = document.getElementById('lightbox');
  const lightboxImg = document.getElementById('lightbox-img');
  const counter = document.getElementById('lightbox-counter');
  
  lightboxImg.src = photoImages[currentPhotoIndex];
  counter.textContent = `${currentPhotoIndex + 1} / ${photoImages.length}`;
  lightbox.style.display = 'flex';
  document.body.style.overflow = 'hidden'; // Prevent scrolling
}

function closeLightbox() {
  const lightbox = document.getElementById('lightbox');
  lightbox.style.display = 'none';
  document.body.style.overflow = 'auto'; // Restore scrolling
}

function changePhoto(direction) {
  currentPhotoIndex += direction;
  
  // Loop around
  if (currentPhotoIndex < 0) {
    currentPhotoIndex = photoImages.length - 1;
  } else if (currentPhotoIndex >= photoImages.length) {
    currentPhotoIndex = 0;
  }
  
  const lightboxImg = document.getElementById('lightbox-img');
  const counter = document.getElementById('lightbox-counter');
  
  lightboxImg.src = photoImages[currentPhotoIndex];
  counter.textContent = `${currentPhotoIndex + 1} / ${photoImages.length}`;
}

// Keyboard navigation
document.addEventListener('keydown', function(event) {
  const lightbox = document.getElementById('lightbox');
  if (lightbox && lightbox.style.display === 'flex') {
    if (event.key === 'ArrowLeft') {
      changePhoto(-1);
    } else if (event.key === 'ArrowRight') {
      changePhoto(1);
    } else if (event.key === 'Escape') {
      closeLightbox();
    }
  }
});
