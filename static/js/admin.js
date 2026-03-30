/**
 * ShopWise — Admin Panel JavaScript
 * Handles: section switching, add/edit/delete products, image management
 */

// ── Section Navigation ──────────────────────────────────────────────────────

/**
 * Show a specific admin section and hide others.
 * @param {string} name - 'products' | 'add' | 'edit'
 */
function showSection(name) {
    // Hide all sections
    document.querySelectorAll('.admin-section').forEach(s => s.classList.remove('active'));

    // Show target section
    const section = document.getElementById(`section-${name}`);
    if (section) section.classList.add('active');

    // Update sidebar active state
    document.querySelectorAll('.sidebar-link').forEach(link => {
        link.classList.remove('active');
    });

    // Update page title
    const titles = { products: 'All Products', add: 'Add New Product', edit: 'Edit Product' };
    const titleEl = document.getElementById('sectionTitle');
    if (titleEl) titleEl.textContent = titles[name] || '';
}

// ── Toast Notification ──────────────────────────────────────────────────────

function showAdminToast(message, type = 'info') {
    const toast = document.getElementById('adminToast');
    if (!toast) return;
    toast.textContent = message;
    toast.className = `admin-toast show ${type}`;
    clearTimeout(toast._timer);
    toast._timer = setTimeout(() => toast.classList.remove('show'), 3500);
}

// ── Image Preview (for upload inputs) ──────────────────────────────────────

/**
 * Preview selected images in a grid below the upload zone.
 * @param {HTMLInputElement} input - File input element
 * @param {string} previewId - ID of the preview container
 */
function previewImages(input, previewId) {
    const container = document.getElementById(previewId);
    if (!container) return;
    container.innerHTML = '';

    Array.from(input.files).forEach((file, index) => {
        if (!file.type.startsWith('image/')) return;

        const reader = new FileReader();
        reader.onload = (e) => {
            const div = document.createElement('div');
            div.className = 'preview-item';
            div.innerHTML = `
                <img src="${e.target.result}" alt="Preview ${index + 1}">
                <button class="preview-remove" type="button" title="Remove" onclick="this.parentElement.remove()">✕</button>
            `;
            container.appendChild(div);
        };
        reader.readAsDataURL(file);
    });
}

// ── Add Product ─────────────────────────────────────────────────────────────

document.getElementById('addProductForm')?.addEventListener('submit', async function(e) {
    e.preventDefault();

    const btn = this.querySelector('[type="submit"]');
    btn.disabled = true;
    btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Saving...';

    const formData = new FormData(this);

    try {
        const res = await fetch('/admin-secret/add', { method: 'POST', body: formData });
        const data = await res.json();

        if (data.success) {
            showAdminToast('✅ Product added successfully!', 'success');
            this.reset();
            document.getElementById('addPreview').innerHTML = '';
            // Reload page to refresh product list
            setTimeout(() => location.reload(), 1200);
        } else {
            showAdminToast('❌ Error: ' + data.error, 'error');
        }
    } catch (err) {
        showAdminToast('❌ Network error. Please try again.', 'error');
    } finally {
        btn.disabled = false;
        btn.innerHTML = '<i class="fas fa-save"></i> Save Product';
    }
});

// ── Load Edit Product ───────────────────────────────────────────────────────

async function loadEditProduct(productId) {
    showSection('edit');

    try {
        const res = await fetch(`/admin-secret/edit/${productId}`);
        const data = await res.json();

        document.getElementById('edit-product-id').value = data.id;
        document.getElementById('edit-name').value = data.name;
        document.getElementById('edit-desc').value = data.description;
        document.getElementById('edit-link').value = data.affiliate_link;

        // Render existing images
        const grid = document.getElementById('existingImagesGrid');
        grid.innerHTML = '';
        data.images.forEach(img => {
            const div = document.createElement('div');
            div.className = `existing-img-item ${img.primary ? 'primary' : ''}`;
            div.id = `existing-${img.id}`;
            div.innerHTML = `
                <img src="/static/${img.path}" alt="Product image">
                <div class="img-actions">
                    <button class="set-primary" title="Set as primary" onclick="setPrimaryImage(${img.id})">⭐</button>
                    <button class="del-img" title="Delete image" onclick="deleteImage(${img.id})">🗑</button>
                </div>
                ${img.primary ? '<div class="primary-badge">PRIMARY</div>' : ''}
            `;
            grid.appendChild(div);
        });

        // Clear new image previews
        document.getElementById('editPreview').innerHTML = '';

    } catch (err) {
        showAdminToast('❌ Failed to load product data.', 'error');
    }
}

// ── Edit Product Submit ─────────────────────────────────────────────────────

document.getElementById('editProductForm')?.addEventListener('submit', async function(e) {
    e.preventDefault();

    const productId = document.getElementById('edit-product-id').value;
    const btn = this.querySelector('[type="submit"]');
    btn.disabled = true;
    btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Updating...';

    const formData = new FormData(this);

    try {
        const res = await fetch(`/admin-secret/edit/${productId}`, { method: 'POST', body: formData });
        const data = await res.json();

        if (data.success) {
            showAdminToast('✅ Product updated successfully!', 'success');
            setTimeout(() => location.reload(), 1200);
        } else {
            showAdminToast('❌ Error: ' + data.error, 'error');
        }
    } catch (err) {
        showAdminToast('❌ Network error. Please try again.', 'error');
    } finally {
        btn.disabled = false;
        btn.innerHTML = '<i class="fas fa-save"></i> Update Product';
    }
});

// ── Set Primary Image ───────────────────────────────────────────────────────

async function setPrimaryImage(imageId) {
    try {
        const res = await fetch(`/admin-secret/set-primary/${imageId}`, { method: 'POST' });
        const data = await res.json();

        if (data.success) {
            showAdminToast('⭐ Primary image updated!', 'success');
            // Update UI — remove old primary badges
            document.querySelectorAll('.existing-img-item').forEach(el => {
                el.classList.remove('primary');
                const badge = el.querySelector('.primary-badge');
                if (badge) badge.remove();
            });
            // Mark new primary
            const newPrimary = document.getElementById(`existing-${imageId}`);
            if (newPrimary) {
                newPrimary.classList.add('primary');
                newPrimary.insertAdjacentHTML('beforeend', '<div class="primary-badge">PRIMARY</div>');
            }
        }
    } catch (err) {
        showAdminToast('❌ Failed to update primary image.', 'error');
    }
}

// ── Delete Single Image ─────────────────────────────────────────────────────

async function deleteImage(imageId) {
    if (!confirm('Delete this image?')) return;

    try {
        const res = await fetch(`/admin-secret/delete-image/${imageId}`, { method: 'DELETE' });
        const data = await res.json();

        if (data.success) {
            const el = document.getElementById(`existing-${imageId}`);
            if (el) el.remove();
            showAdminToast('🗑 Image deleted.', 'info');
        }
    } catch (err) {
        showAdminToast('❌ Failed to delete image.', 'error');
    }
}

// ── Delete Product ──────────────────────────────────────────────────────────

let _pendingDeleteId = null;

function deleteProduct(productId, productName) {
    _pendingDeleteId = productId;
    document.getElementById('modalTitle').textContent = 'Delete Product?';
    document.getElementById('modalMessage').textContent = `"${productName}" and all its images will be permanently deleted.`;
    document.getElementById('confirmModal').style.display = 'flex';

    document.getElementById('modalConfirmBtn').onclick = async () => {
        closeModal();
        try {
            const res = await fetch(`/admin-secret/delete/${productId}`, { method: 'DELETE' });
            const data = await res.json();

            if (data.success) {
                showAdminToast('🗑 Product deleted.', 'info');
                const card = document.getElementById(`card-${productId}`);
                if (card) {
                    card.style.transition = 'opacity 0.3s, transform 0.3s';
                    card.style.opacity = '0';
                    card.style.transform = 'scale(0.9)';
                    setTimeout(() => card.remove(), 300);
                }
            } else {
                showAdminToast('❌ Failed to delete product.', 'error');
            }
        } catch (err) {
            showAdminToast('❌ Network error.', 'error');
        }
    };
}

function closeModal() {
    document.getElementById('confirmModal').style.display = 'none';
    _pendingDeleteId = null;
}

// Close modal on overlay click
document.getElementById('confirmModal')?.addEventListener('click', function(e) {
    if (e.target === this) closeModal();
});

// ── Drag & Drop Upload Zones ────────────────────────────────────────────────

function initDragDrop(zoneId, inputId) {
    const zone = document.getElementById(zoneId);
    if (!zone) return;

    zone.addEventListener('dragover', (e) => {
        e.preventDefault();
        zone.style.borderColor = 'var(--orange)';
        zone.style.background = 'var(--orange-light)';
    });

    zone.addEventListener('dragleave', () => {
        zone.style.borderColor = '';
        zone.style.background = '';
    });

    zone.addEventListener('drop', (e) => {
        e.preventDefault();
        zone.style.borderColor = '';
        zone.style.background = '';
        const input = document.getElementById(inputId);
        if (input && e.dataTransfer.files.length) {
            input.files = e.dataTransfer.files;
            const previewId = inputId === 'add-images' ? 'addPreview' : 'editPreview';
            previewImages(input, previewId);
        }
    });
}

// ── Init ───────────────────────────────────────────────────────────────────

document.addEventListener('DOMContentLoaded', () => {
    initDragDrop('addUploadZone', 'add-images');
    initDragDrop('editUploadZone', 'edit-images');
});
