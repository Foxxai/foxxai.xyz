console.log('Gallery script loading...');

window.addEventListener('load', function() {
    console.log('Window loaded, initializing gallery...');
    setupGallery();
});

document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM ready, initializing gallery...');
    setupGallery();
});

function setupGallery() {
    console.log('Setting up gallery...');
    
    // First, check if we have gallery items
    const galleryItems = document.querySelectorAll('.gallery-item');
    console.log('Found gallery items:', galleryItems.length);
    
    if (galleryItems.length === 0) {
        console.log('No gallery items found, exiting setup');
        return;
    }

    // Create or get lightbox
    let lightbox = document.querySelector('.lightbox');
    if (!lightbox) {
        console.log('Creating new lightbox');
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

    const lightboxImage = lightbox.querySelector('.lightbox-image');
    const lightboxCaption = lightbox.querySelector('.lightbox-caption');
    const closeButton = lightbox.querySelector('.lightbox-close');

    // Add click handlers to gallery items
    galleryItems.forEach(item => {
        item.addEventListener('click', function() {
            console.log('Gallery item clicked');
            const fullImage = this.dataset.fullImage;
            const fullCaption = this.dataset.fullCaption;
            console.log('Opening image:', fullImage);
            
            lightboxImage.src = fullImage;
            lightboxCaption.innerHTML = fullCaption;
            lightbox.classList.add('active');
            document.body.style.overflow = 'hidden';
        });
    });

    // Close lightbox on button click
    closeButton.addEventListener('click', closeLightbox);

    // Close lightbox on background click
    lightbox.addEventListener('click', function(e) {
        if (e.target === this) {
            closeLightbox();
        }
    });

    // Close lightbox on escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && lightbox.classList.contains('active')) {
            closeLightbox();
        }
    });

    function closeLightbox() {
        console.log('Closing lightbox');
        lightbox.classList.remove('active');
        document.body.style.overflow = '';
        setTimeout(() => {
            lightboxImage.src = '';
            lightboxCaption.innerHTML = '';
        }, 300);
    }
}

// Also try to handle Material theme's instant loading
document.addEventListener('DOMContentReady', setupGallery);
document.addEventListener('mdx-switch-page', function() {
    console.log('Page switched, reinitializing gallery...');
    setupGallery();
});