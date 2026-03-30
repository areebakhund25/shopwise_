"""
ShopWise.com - Affiliate Product Listing Website
Flask Backend - app.py
"""

import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, jsonify, g
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = 'shopwise-secret-key-2024'
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'images')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload
app.config['DATABASE'] = 'database.db'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

# ─── Database Helpers ──────────────────────────────────────────────────────────

def get_db():
    """Get database connection (one per request)."""
    if 'db' not in g:
        g.db = sqlite3.connect(app.config['DATABASE'])
        g.db.row_factory = sqlite3.Row  # Access columns by name
    return g.db

@app.teardown_appcontext
def close_db(error):
    """Close database connection after each request."""
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    """Initialize database tables."""
    db = sqlite3.connect(app.config['DATABASE'])
    db.executescript('''
        CREATE TABLE IF NOT EXISTS products (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT NOT NULL,
            description TEXT NOT NULL,
            affiliate_link TEXT NOT NULL,
            created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS product_images (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id  INTEGER NOT NULL,
            image_path  TEXT NOT NULL,
            is_primary  INTEGER DEFAULT 0,
            FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
        );
    ''')
    db.commit()
    db.close()
    print("✅ Database initialized successfully.")

def allowed_file(filename):
    """Check if uploaded file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_product_with_images(product_id):
    """Fetch a single product along with all its images."""
    db = get_db()
    product = db.execute('SELECT * FROM products WHERE id = ?', (product_id,)).fetchone()
    if not product:
        return None, []
    images = db.execute(
        'SELECT * FROM product_images WHERE product_id = ? ORDER BY is_primary DESC',
        (product_id,)
    ).fetchall()
    return product, images

def get_all_products():
    """Fetch all products with their primary image."""
    db = get_db()
    products = db.execute('SELECT * FROM products ORDER BY created_at DESC').fetchall()
    result = []
    for p in products:
        img = db.execute(
            'SELECT image_path FROM product_images WHERE product_id = ? AND is_primary = 1 LIMIT 1',
            (p['id'],)
        ).fetchone()
        if not img:
            img = db.execute(
                'SELECT image_path FROM product_images WHERE product_id = ? LIMIT 1',
                (p['id'],)
            ).fetchone()
        result.append({
            'id': p['id'],
            'name': p['name'],
            'description': p['description'],
            'affiliate_link': p['affiliate_link'],
            'primary_image': img['image_path'] if img else None
        })
    return result

# ─── Public Routes ─────────────────────────────────────────────────────────────

@app.route('/')
def index():
    """Homepage: show all products in a grid."""
    search_query = request.args.get('q', '').strip()
    db = get_db()

    if search_query:
        products_raw = db.execute(
            "SELECT * FROM products WHERE name LIKE ? OR description LIKE ? ORDER BY created_at DESC",
            (f'%{search_query}%', f'%{search_query}%')
        ).fetchall()
    else:
        products_raw = db.execute('SELECT * FROM products ORDER BY created_at DESC').fetchall()

    products = []
    for p in products_raw:
        img = db.execute(
            'SELECT image_path FROM product_images WHERE product_id = ? AND is_primary = 1 LIMIT 1',
            (p['id'],)
        ).fetchone()
        if not img:
            img = db.execute(
                'SELECT image_path FROM product_images WHERE product_id = ? LIMIT 1',
                (p['id'],)
            ).fetchone()
        products.append({
            'id': p['id'],
            'name': p['name'],
            'description': p['description'],
            'affiliate_link': p['affiliate_link'],
            'primary_image': img['image_path'] if img else None
        })

    return render_template('index.html', products=products, search_query=search_query)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    """Product detail page with image gallery."""
    product, images = get_product_with_images(product_id)
    if not product:
        return render_template('404.html'), 404
    return render_template('product_detail.html', product=product, images=images)

# ─── Admin Routes ──────────────────────────────────────────────────────────────

@app.route('/admin-1351954')
def admin():
    """Hidden admin panel to manage products."""
    products = get_all_products()
    return render_template('admin.html', products=products)

@app.route('/admin-1351954/add', methods=['POST'])
def admin_add_product():
    """Add a new product with images."""
    name = request.form.get('name', '').strip()
    description = request.form.get('description', '').strip()
    affiliate_link = request.form.get('affiliate_link', '').strip()

    if not name or not description or not affiliate_link:
        return jsonify({'success': False, 'error': 'All fields are required.'}), 400

    db = get_db()
    cursor = db.execute(
        'INSERT INTO products (name, description, affiliate_link) VALUES (?, ?, ?)',
        (name, description, affiliate_link)
    )
    product_id = cursor.lastrowid

    # Handle image uploads
    images = request.files.getlist('images')
    is_first = True
    for image in images:
        if image and image.filename and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            # Make filename unique with product_id prefix
            unique_filename = f"product_{product_id}_{filename}"
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            image.save(save_path)
            db_path = f"images/{unique_filename}"
            db.execute(
                'INSERT INTO product_images (product_id, image_path, is_primary) VALUES (?, ?, ?)',
                (product_id, db_path, 1 if is_first else 0)
            )
            is_first = False

    db.commit()
    return jsonify({'success': True, 'product_id': product_id})

@app.route('/admin-1351954/edit/<int:product_id>', methods=['GET', 'POST'])
def admin_edit_product(product_id):
    """Edit existing product details and images."""
    db = get_db()
    product, images = get_product_with_images(product_id)
    if not product:
        return jsonify({'success': False, 'error': 'Product not found.'}), 404

    if request.method == 'GET':
        return jsonify({
            'id': product['id'],
            'name': product['name'],
            'description': product['description'],
            'affiliate_link': product['affiliate_link'],
            'images': [{'id': img['id'], 'path': img['image_path'], 'primary': img['is_primary']} for img in images]
        })

    # POST: update product fields
    name = request.form.get('name', '').strip()
    description = request.form.get('description', '').strip()
    affiliate_link = request.form.get('affiliate_link', '').strip()

    if not name or not description or not affiliate_link:
        return jsonify({'success': False, 'error': 'All fields are required.'}), 400

    db.execute(
        'UPDATE products SET name=?, description=?, affiliate_link=? WHERE id=?',
        (name, description, affiliate_link, product_id)
    )

    # Handle new image uploads
    new_images = request.files.getlist('images')
    existing_count = db.execute(
        'SELECT COUNT(*) FROM product_images WHERE product_id=?', (product_id,)
    ).fetchone()[0]
    is_first = existing_count == 0

    for image in new_images:
        if image and image.filename and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            unique_filename = f"product_{product_id}_{filename}"
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            image.save(save_path)
            db_path = f"images/{unique_filename}"
            db.execute(
                'INSERT INTO product_images (product_id, image_path, is_primary) VALUES (?, ?, ?)',
                (product_id, db_path, 1 if is_first else 0)
            )
            is_first = False

    db.commit()
    return jsonify({'success': True})

@app.route('/admin-1351954/delete-image/<int:image_id>', methods=['DELETE'])
def admin_delete_image(image_id):
    """Delete a single product image."""
    db = get_db()
    img = db.execute('SELECT * FROM product_images WHERE id=?', (image_id,)).fetchone()
    if not img:
        return jsonify({'success': False, 'error': 'Image not found.'}), 404

    # Delete file from disk
    file_path = os.path.join('static', img['image_path'])
    if os.path.exists(file_path):
        os.remove(file_path)

    # If deleted image was primary, make the next one primary
    was_primary = img['is_primary']
    product_id = img['product_id']
    db.execute('DELETE FROM product_images WHERE id=?', (image_id,))

    if was_primary:
        next_img = db.execute(
            'SELECT id FROM product_images WHERE product_id=? LIMIT 1', (product_id,)
        ).fetchone()
        if next_img:
            db.execute('UPDATE product_images SET is_primary=1 WHERE id=?', (next_img['id'],))

    db.commit()
    return jsonify({'success': True})

@app.route('/admin-1351954/delete/<int:product_id>', methods=['DELETE'])
def admin_delete_product(product_id):
    """Delete a product and all its images."""
    db = get_db()
    product = db.execute('SELECT * FROM products WHERE id=?', (product_id,)).fetchone()
    if not product:
        return jsonify({'success': False, 'error': 'Product not found.'}), 404

    # Delete image files from disk
    images = db.execute('SELECT image_path FROM product_images WHERE product_id=?', (product_id,)).fetchall()
    for img in images:
        file_path = os.path.join('static', img['image_path'])
        if os.path.exists(file_path):
            os.remove(file_path)

    db.execute('DELETE FROM product_images WHERE product_id=?', (product_id,))
    db.execute('DELETE FROM products WHERE id=?', (product_id,))
    db.commit()
    return jsonify({'success': True})

@app.route('/admin-1351954/set-primary/<int:image_id>', methods=['POST'])
def admin_set_primary_image(image_id):
    """Set an image as the primary image for its product."""
    db = get_db()
    img = db.execute('SELECT * FROM product_images WHERE id=?', (image_id,)).fetchone()
    if not img:
        return jsonify({'success': False, 'error': 'Image not found.'}), 404

    db.execute('UPDATE product_images SET is_primary=0 WHERE product_id=?', (img['product_id'],))
    db.execute('UPDATE product_images SET is_primary=1 WHERE id=?', (image_id,))
    db.commit()
    return jsonify({'success': True})

# ─── Error Handlers ────────────────────────────────────────────────────────────

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# ─── Entry Point ───────────────────────────────────────────────────────────────

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    init_db()
    print("🚀 ShopWise.com is running at http://127.0.0.1:5000")
    print("🔧 Admin panel: http://127.0.0.1:5000/admin-1351954")
    app.run(debug=True, host='0.0.0.0', port=5000)
