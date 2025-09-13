# Academic Travelogue

A chronicle of academic journeys, conferences, research visits, and collaborative endeavors across the globe.

<div class="gallery-grid">
    <div class="gallery-item" 
         data-full-image="assets/travelogue/full/PXL_20250913_142859898.jpg"
         data-full-caption="Presenting our latest findings on human-AI collaborative workflows at the AGI-25 conference. This talk highlighted the emerging patterns in how humans and language models cooperatively solve complex problems.">
        <img class="gallery-thumbnail" src="assets/travelogue/thumbnails/PXL_20250913_142859898.jpg" alt="Speaking at AGI-25 conference podium">
        <div class="gallery-caption">Conference presentation at AGI-25</div>
    </div>
</div>

<!-- Script to debug image loading -->
<script>
document.addEventListener('DOMContentLoaded', function() {
    const img = document.querySelector('.gallery-thumbnail');
    console.log('Thumbnail src:', img.src);
    console.log('Thumbnail complete:', img.complete);
    img.addEventListener('load', () => console.log('Thumbnail loaded successfully'));
    img.addEventListener('error', () => console.log('Thumbnail failed to load'));
});
</script>