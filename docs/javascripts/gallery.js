function setupGallery() {
    console.log("Setting up gallery...");
    
    // Remove any existing lightbox to prevent duplicates
    let existingLightbox = document.querySelector('.lightbox');
    if (existingLightbox) {
        existingLightbox.remove();
    }

    // Create fresh lightbox
    const lightbox = document.createElement('div');
    lightbox.className = 'lightbox';
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

    // Add click handlers to gallery items
    document.querySelectorAll('.gallery-item').forEach(item => {
        // Remove existing click listeners by cloning
        const newItem = item.cloneNode(true);
        item.parentNode.replaceChild(newItem, item);
        
        newItem.addEventListener('click', (e) => {
            e.preventDefault();
            e.stopPropagation();
            
            // Get image data, falling back to img attributes if needed
            const fullImage = newItem.dataset.fullImage || newItem.querySelector('img')?.src;
            const fullCaption = newItem.dataset.fullCaption || newItem.querySelector('img')?.alt;
            
            if (!fullImage) {
                console.error('No image source found for gallery item:', newItem);
                return;
            }
            
            lightboxImage.src = fullImage;
            lightboxCaption.innerHTML = fullCaption || '';
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

function initGallery() {
    // Wait a brief moment to ensure content is loaded
    setTimeout(setupGallery, 100);
}

// Initial page load
document.addEventListener('DOMContentLoaded', initGallery);

// Material for MkDocs specific events
document.addEventListener('DOMContentReady', initGallery);
document.addEventListener('mdx-switch-page', initGallery);

// Handle dynamic content changes and page reloads
window.addEventListener('load', initGallery);

// Watch for any changes to the DOM that might add gallery items
const observer = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
        if (mutation.addedNodes && mutation.addedNodes.length > 0) {
            for (let node of mutation.addedNodes) {
                if (node.classList && 
                    (node.classList.contains('gallery-grid') || 
                     node.classList.contains('gallery-item'))) {
                    initGallery();
                    break;
                }
            }
        }
    });
});

// Start observing the document with the configured parameters
observer.observe(document.body, {
    childList: true,
    subtree: true
});