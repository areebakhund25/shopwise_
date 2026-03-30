# 🛍️ ShopWise — Affiliate Product Listing Website

A clean, modern affiliate website built with Flask. Display Daraz products and
redirect users via affiliate links. Products are managed manually in code.

---

## 📁 Project Structure

```
shopwise/
├── app.py                   # Flask backend (routes + manual product data)
├── requirements.txt         # Python dependencies
├── static/
│   ├── css/
│   │   └── style.css        # Main website styles
│   ├── js/
│   │   ├── main.js          # Homepage JS (toast, animations)
│   │   └── gallery.js       # Product detail image gallery
│   └── images/              # Uploaded product images (auto-created)
└── templates/
    ├── base.html            # Base layout with navbar + footer
    ├── index.html           # Homepage with product grid
    ├── product_detail.html  # Product detail + image gallery
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

- **Website:** http://127.0.0.1:5001

---

## ⚙️ Managing Products (Manual)

1. Open `app.py`
2. Edit the `PRODUCTS` list near the top of the file
3. Add product objects with:
   - `id` (unique integer)
   - `name`
   - `description`
   - `affiliate_link`
   - `images` (list like `["images/item1.jpg", "images/item2.jpg"]`)
4. Put image files inside `static/images/`
5. Restart Flask (or save with debug mode enabled)

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
4. Add authentication and rate limiting if you later add private routes

---

## 📦 Tech Stack

| Layer    | Technology         |
|----------|--------------------|
| Backend  | Python / Flask     |
| Data     | Manual Python list |
| Frontend | HTML5, CSS3, JS    |
| Fonts    | Playfair + DM Sans |
| Icons    | Font Awesome 6     |

---

## 📝 Notes

- Product images are stored in `static/images/` with unique filenames
- No database is used; products are loaded from `PRODUCTS` in `app.py`
- Search works across product names and descriptions
