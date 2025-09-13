function setupGallery() {
    console.log("Setting up gallery...");
    
    // Remove any existing lightbox
    const existingLightbox = document.querySelector('.lightbox');
    if (existingLightbox) {
        existingLightbox.remove();
    }

    // Create fresh lightbox
    const lightbox = document.createElement('div');
    lightbox.className = 'lightbox';
    lightbox.style.display = 'none';
    lightbox.innerHTML = `
        <div class="lightbox-content">
            <img class="lightbox-image" src="" alt="">
            <div class="lightbox-caption"></div>
            <button class="lightbox-close" aria-label="Close">✕</button>
        </div>
    `;
    document.body.appendChild(lightbox);

    // Get lightbox elements
    const lightboxImage = lightbox.querySelector('.lightbox-image');
    const lightboxCaption = lightbox.querySelector('.lightbox-caption');
    const closeButton = lightbox.querySelector('.lightbox-close');

    // Function to open lightbox
    function openLightbox(fullImage, fullCaption) {
        lightboxImage.src = fullImage;
        lightboxCaption.innerHTML = fullCaption || '';
        lightbox.style.display = 'flex';
        requestAnimationFrame(() => {
            lightbox.classList.add('active');
            document.body.style.overflow = 'hidden';
        });
    }

    // Function to close lightbox
    function closeLightbox() {
        lightbox.classList.remove('active');
        document.body.style.overflow = '';
        setTimeout(() => {
            lightbox.style.display = 'none';
            lightboxImage.src = '';
            lightboxCaption.innerHTML = '';
        }, 300);
    }

    // Add click handlers to gallery items
    document.querySelectorAll('.gallery-item').forEach(item => {
        item.onclick = (e) => {
            e.preventDefault();
            e.stopPropagation();
            
            const fullImage = item.dataset.fullImage || item.querySelector('img')?.src;
            const fullCaption = item.dataset.fullCaption || item.querySelector('img')?.alt;
            
            if (!fullImage) {
                console.error('No image source found for gallery item:', item);
                return;
            }
            
            openLightbox(fullImage, fullCaption);
        };
    });

    // Close button click
    closeButton.onclick = (e) => {
        e.preventDefault();
        closeLightbox();
    };

    // Background click
    lightbox.onclick = (e) => {
        if (e.target === lightbox) {
            closeLightbox();
        }
    };

    // Escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && lightbox.classList.contains('active')) {
            closeLightbox();
        }
    });
}

// Initialize gallery
function initGallery() {
    setupGallery();
}

// Setup on initial load
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initGallery);
} else {
    initGallery();
}

// Handle MkDocs navigation
document.addEventListener('DOMContentReady', initGallery);
document.addEventListener('mdx-switch-page', () => {
    setTimeout(initGallery, 100);
});
