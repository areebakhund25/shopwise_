/**
 * ShopWise — Product Image Gallery
 * Handles main image switching, keyboard navigation, thumbnails
 */

let currentIndex = 0;

/**
 * Switch to a specific image by index.
 */
function selectImage(index) {
    if (!galleryImages || galleryImages.length === 0) return;

    // Clamp index
    currentIndex = (index + galleryImages.length) % galleryImages.length;

    // Update main image with fade
    const mainImg = document.getElementById('mainImage');
    if (mainImg) {
        mainImg.style.opacity = '0.4';
        mainImg.src = galleryImages[currentIndex];
        mainImg.onload = () => { mainImg.style.opacity = '1'; };
    }

    // Update counter
    const counter = document.getElementById('imageCounter');
    if (counter) counter.textContent = `${currentIndex + 1} / ${galleryImages.length}`;

    // Update thumbnail active state
    document.querySelectorAll('.thumb-wrap').forEach((t, i) => {
        t.classList.toggle('active', i === currentIndex);
    });

    // Scroll active thumb into view
    const activeThumb = document.getElementById(`thumb-${currentIndex}`);
    if (activeThumb) {
        activeThumb.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });
    }
}

/**
 * Navigate forward or back by a step.
 */
function changeImage(step) {
    selectImage(currentIndex + step);
}

/**
 * Keyboard navigation support.
 */
document.addEventListener('keydown', (e) => {
    if (!galleryImages || galleryImages.length <= 1) return;
    if (e.key === 'ArrowLeft') changeImage(-1);
    if (e.key === 'ArrowRight') changeImage(1);
});

/**
 * Touch swipe support for mobile.
 */
(function initSwipe() {
    const main = document.querySelector('.gallery-main');
    if (!main) return;

    let startX = 0;
    main.addEventListener('touchstart', e => { startX = e.touches[0].clientX; }, { passive: true });
    main.addEventListener('touchend', e => {
        const diff = startX - e.changedTouches[0].clientX;
        if (Math.abs(diff) > 40) changeImage(diff > 0 ? 1 : -1);
    }, { passive: true });
})();

// Show/hide nav buttons based on image count
document.addEventListener('DOMContentLoaded', () => {
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    if (prevBtn && nextBtn) {
        const hasMultiple = galleryImages && galleryImages.length > 1;
        prevBtn.style.display = hasMultiple ? 'flex' : 'none';
        nextBtn.style.display = hasMultiple ? 'flex' : 'none';
    }
});
