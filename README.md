# 🛍️ ShopWise — Affiliate Product Listing Website

A clean, modern affiliate website built with Flask. Display Daraz products and
redirect users via affiliate links. Manage everything from a hidden admin panel.

---

## 📁 Project Structure

```
shopwise/
├── app.py                   # Flask backend (all routes + DB logic)
├── database.db              # SQLite database (auto-created on first run)
├── requirements.txt         # Python dependencies
├── static/
│   ├── css/
│   │   ├── style.css        # Main website styles
│   │   └── admin.css        # Admin panel styles
│   ├── js/
│   │   ├── main.js          # Homepage JS (toast, animations)
│   │   ├── gallery.js       # Product detail image gallery
│   │   └── admin.js         # Admin panel JS (CRUD operations)
│   └── images/              # Uploaded product images (auto-created)
└── templates/
    ├── base.html            # Base layout with navbar + footer
    ├── index.html           # Homepage with product grid
    ├── product_detail.html  # Product detail + image gallery
    ├── admin.html           # Hidden admin panel
    └── 404.html             # 404 error page
```

---

## 🚀 Quick Start

### 1. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the website

```bash
python app.py
```

### 3. Open in your browser

- **Website:** http://127.0.0.1:5000
- **Admin Panel:** http://127.0.0.1:5000/admin-1351954

---

## ⚙️ Admin Panel Usage

Visit: `http://127.0.0.1:5000/admin-1351954`

### Adding a Product
1. Click **"Add New Product"** in the sidebar
2. Fill in: Product Name, Description, Daraz Affiliate Link
3. Upload one or more product images
4. Click **"Save Product"**

### Editing a Product
1. Click **"Edit"** on any product card
2. Update any field or add new images
3. Click ⭐ on an image to set it as the primary (thumbnail) image
4. Click 🗑 on an image to delete it
5. Click **"Update Product"**

### Deleting a Product
1. Click **"Delete"** on a product card
2. Confirm in the popup dialog
3. The product and all its images are permanently removed

---

## 🔧 Configuration

Edit the top of `app.py` to customize:

```python
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Change in production
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Max file upload: 16MB
```

---

## 🌐 Deploying to Production

For production use, consider:

1. **Change the secret key** in `app.py`
2. **Use a production WSGI server:**
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:8000 app:app
   ```
3. **Add Nginx** as a reverse proxy for static files
4. **Add authentication** to `/admin-1351954` if needed

---

## 📦 Tech Stack

| Layer    | Technology         |
|----------|--------------------|
| Backend  | Python / Flask     |
| Database | SQLite             |
| Frontend | HTML5, CSS3, JS    |
| Fonts    | Playfair + DM Sans |
| Icons    | Font Awesome 6     |

---

## 📝 Notes

- The admin panel at `/admin-1351954` is intentionally not linked anywhere on the public site
- Product images are stored in `static/images/` with unique filenames
- The SQLite database is auto-created at first run — no setup needed
- Search works across product names and descriptions
