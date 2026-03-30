/**
 * ShopWise — Main JavaScript
 * Toast notifications, click tracking, misc utilities
 */

// ── Toast Notification ──────────────────────────────────────────────────────

/**
 * Show a toast message at the bottom-right of the screen.
 * @param {string} message - Text to display
 * @param {string} type - 'success' | 'error' | 'info'
 * @param {number} duration - Milliseconds to show (default 3000)
 */
function showToast(message, type = 'info', duration = 3000) {
    const toast = document.getElementById('toast');
    if (!toast) return;
    toast.textContent = message;
    toast.className = `toast show ${type}`;
    clearTimeout(toast._timer);
    toast._timer = setTimeout(() => {
        toast.classList.remove('show');
    }, duration);
}

// ── Click Tracking ──────────────────────────────────────────────────────────

/**
 * Track affiliate link clicks (basic logging).
 * Can be extended with analytics later.
 */
function trackClick(productId) {
    console.log(`[ShopWise] Affiliate click → Product ID: ${productId}`);
    // Example: send to analytics endpoint
    // fetch(`/api/track-click/${productId}`, { method: 'POST' });
}

// ── Lazy Load Images ────────────────────────────────────────────────────────

/**
 * Observe images with loading="lazy" and animate them in
 * when they enter the viewport.
 */
function initLazyImageAnimations() {
    if (!('IntersectionObserver' in window)) return;

    const images = document.querySelectorAll('img[loading="lazy"]');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });

    images.forEach(img => {
        img.style.opacity = '0';
        img.style.transition = 'opacity 0.5s ease';
        img.addEventListener('load', () => { img.style.opacity = '1'; });
        observer.observe(img);
    });
}

// ── Card Scroll Animation ───────────────────────────────────────────────────

function initCardAnimations() {
    if (!('IntersectionObserver' in window)) return;

    const cards = document.querySelectorAll('.product-card');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry, i) => {
            if (entry.isIntersecting) {
                entry.target.style.animationPlayState = 'running';
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });

    cards.forEach(card => {
        card.style.animationPlayState = 'paused';
        observer.observe(card);
    });
}

// ── Init ───────────────────────────────────────────────────────────────────

document.addEventListener('DOMContentLoaded', () => {
    initLazyImageAnimations();
    initCardAnimations();
});
