function setupGallery() {
    console.log("Setting up gallery...");
    
    // Create lightbox element if it doesn't exist
    let lightbox = document.querySelector('.lightbox');
    if (!lightbox) {
        lightbox = document.createElement('div');
        lightbox.className = 'lightbox';
        lightbox.innerHTML = `
            <div class="lightbox-content">
                <img class="lightbox-image" src="" alt="">
                <div class="lightbox-caption"></div>
                <button class="lightbox-close" aria-label="Close">✕</button>
            </div>
        `;
        document.body.appendChild(lightbox);
    }

    // Get lightbox elements
    const lightboxImage = lightbox.querySelector('.lightbox-image');
    const lightboxCaption = lightbox.querySelector('.lightbox-caption');
    const closeButton = lightbox.querySelector('.lightbox-close');

    // Add click handlers to gallery items
    document.querySelectorAll('.gallery-item').forEach(item => {
        item.addEventListener('click', () => {
            const fullImage = item.dataset.fullImage;
            const fullCaption = item.dataset.fullCaption;
            
            lightboxImage.src = fullImage;
            lightboxCaption.innerHTML = fullCaption;
            lightbox.classList.add('active');
            document.body.style.overflow = 'hidden';
        });
    });

    // Close lightbox on button click
    closeButton.addEventListener('click', closeLightbox);

    // Close lightbox on background click
    lightbox.addEventListener('click', e => {
        if (e.target === lightbox) {
            closeLightbox();
        }
    });

    // Close lightbox on escape key
    document.addEventListener('keydown', e => {
        if (e.key === 'Escape' && lightbox.classList.contains('active')) {
            closeLightbox();
        }
    });

    function closeLightbox() {
        lightbox.classList.remove('active');
        document.body.style.overflow = '';
        setTimeout(() => {
            lightboxImage.src = '';
            lightboxCaption.innerHTML = '';
        }, 300);
    }
}

// Setup gallery when DOM is ready and when page changes (for Material's instant loading)
document.addEventListener('DOMContentLoaded', setupGallery);
document.addEventListener('DOMContentReady', setupGallery);
document.addEventListener('mdx-switch-page', setupGallery);