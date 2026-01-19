document.addEventListener('DOMContentLoaded', function() {
    // Shared functionality
    const copyBtn = document.querySelector('.btn-copy');
    if (copyBtn) {
        copyBtn.addEventListener('click', copyLink);
    }
    
    const fileInput = document.getElementById('file-upload');
    if (fileInput) {
        fileInput.addEventListener('change', function() {
            this.form.submit();
        });
    }

    const deleteBtn = document.getElementById('btn-delete-album');
    if (deleteBtn) {
        deleteBtn.addEventListener('click', function(e) {
            e.preventDefault();
            if (confirm('Вы уверены, что хотите удалить этот альбом? Это действие нельзя отменить.')) {
                document.getElementById('delete-album-form').submit();
            }
        });
    }

    // Lightbox functionality
    let currentPhotoIndex = 0;
    let photoImages = [];
    const photoImgs = document.querySelectorAll('.photo-img');
    photoImages = Array.from(photoImgs).map(img => img.src);
    
    const lightbox = document.getElementById('lightbox');
    const lightboxImg = document.getElementById('lightbox-img');
    const counter = document.getElementById('lightbox-counter');
    const closeBtn = document.querySelector('.lightbox-close');
    const prevBtn = document.querySelector('.lightbox-prev');
    const nextBtn = document.querySelector('.lightbox-next');

    if (lightbox) {
        photoImgs.forEach((img, index) => {
            img.style.cursor = 'pointer'; // Ensure pointer cursor
            img.addEventListener('click', () => openLightbox(index));
        });

        if (closeBtn) closeBtn.addEventListener('click', closeLightbox);
        
        if (prevBtn) prevBtn.addEventListener('click', () => changePhoto(-1));
        
        if (nextBtn) nextBtn.addEventListener('click', () => changePhoto(1));

        // Close on background click
        lightbox.addEventListener('click', function(e) {
            if (e.target === lightbox) {
                closeLightbox();
            }
        });

        // Keyboard navigation
        document.addEventListener('keydown', function(e) {
            if (lightbox.style.display === 'flex') {
                if (e.key === 'Escape') closeLightbox();
                if (e.key === 'ArrowLeft') changePhoto(-1);
                if (e.key === 'ArrowRight') changePhoto(1);
            }
        });
    }

    function openLightbox(index) {
        currentPhotoIndex = index;
        updateLightbox();
        lightbox.style.display = 'flex';
        document.body.style.overflow = 'hidden';
    }

    function closeLightbox() {
        lightbox.style.display = 'none';
        document.body.style.overflow = 'auto';
    }

    function changePhoto(direction) {
        currentPhotoIndex += direction;
        
        if (currentPhotoIndex < 0) {
            currentPhotoIndex = photoImages.length - 1;
        } else if (currentPhotoIndex >= photoImages.length) {
            currentPhotoIndex = 0;
        }
        
        updateLightbox();
    }

    function updateLightbox() {
        lightboxImg.src = photoImages[currentPhotoIndex];
        counter.textContent = `${currentPhotoIndex + 1} / ${photoImages.length}`;
    }

    function copyLink() {
        var copyText = document.getElementById('shareLink');
        copyText.select();
        copyText.setSelectionRange(0, 99999);
        navigator.clipboard.writeText(copyText.value)
            .then(() => alert('Ссылка скопирована в буфер обмена!'))
            .catch(err => console.error('Ошибка копирования:', err));
    }
});
