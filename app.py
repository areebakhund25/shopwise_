"""
ShopWise.com - Affiliate Product Listing Website
Flask Backend - app.py
"""

import os
from flask import Flask, render_template, request

app = Flask(__name__)
app.config['SECRET_KEY'] = 'shopwise-secret-key-2024'
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'images')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Manual product source.
# Add/edit/remove products directly in this list.
PRODUCTS = [
    {
        'id': 1,
        'name': 'Redmi 15 - 6.9',
        'description': (
            '✓ Display: 6.9" FHD+ DotDisplay\n'
            '✓ Resolution: 2340 x 1080\n'
            '✓ Refresh rate: Up to 144Hz\n'
            '✓ Processor: Snapdragon 685 Mobile Platform (6nm, octa-core)\n'
            '✓ CPU: Qualcomm Kryo, up to 2.8GHz | GPU: Qualcomm Adreno\n'
            '✓ Rear camera: 50MP main | 5P lens | f/1.8 | Auxiliary lens\n'
            '✓ Front camera: 8MP | f/2 | HDR | Portrait | Time-lapse\n'
            '✓ Battery and charging: 7000mAh (typ) | 33W fast charging\n'
            '✓ Security: Side fingerprint sensor | AI face unlock\n'
            '✓ Connectivity: SIM1 + Hybrid (SIM or microSD)\n'
            '✓ Wi-Fi: 2.4GHz and 5GHz | Bluetooth 5.0\n'
            '✓ Water and dust resistance: IP64\n'
            '✓ Navigation: GPS | Glonass | Galileo | Beidou\n'
            '✓ Audio: Hi-Res Audio | Dolby Atmos\n'
            '✓ Sensors: Proximity | Ambient light | Accelerometer | Compass | IR blaster\n'
            '✓ OS: Xiaomi HyperOS 2\n'
            '✓ Dimensions: 169.48 x 80.45 x 8.40 mm | Weight: 214g'
        ),
        'affiliate_link': 'https://www.daraz.pk/products/15-69-fhd-8gb-128gb-50mp-7000mah-33-pta-1-i938794413-s3997126131.html?c=&channelLpJumpArgs=&clickTrackInfo=query%253Aredmi%252B12c%253Bnid%253A938794413%253Bsrc%253ALazadaMainSrp%253Brn%253A178894a63738e1d9882d3f0fa6294cf8%253Bregion%253Apk%253Bsku%253A938794413_PK%253Bprice%253A48980%253Bclient%253Adesktop%253Bsupplier_id%253A1096030%253Bsession_id%253A%253Bbiz_source%253Ah5_external%253Bslot%253A0%253Butlog_bucket_id%253A470687%253Basc_category_id%253A3%253Bitem_id%253A938794413%253Bsku_id%253A3997126131%253Bshop_id%253A206899%253BtemplateInfo%253A&freeshipping=0&fs_ab=1&fuse_fs=&lang=en&location=Punjab&price=4.898E%204&priceCompare=skuId%3A3997126131%3Bsource%3Alazada-search-voucher%3Bsn%3A178894a63738e1d9882d3f0fa6294cf8%3BoriginPrice%3A4898000%3BdisplayPrice%3A4898000%3BsinglePromotionId%3A-1%3BsingleToolCode%3AmockedSalePrice%3BvoucherPricePlugin%3A0%3Btimestamp%3A1774896333836&qSellingPoint=p--12c___b--redmi&ratingscore=&request_id=178894a63738e1d9882d3f0fa6294cf8&review=&sale=1&search=1&source=search&spm=a2a0e.searchlist.list.0&stock=1',
        'images': ['images/p2.png'],
    },
    {
        'id': 2,
        'name': '3 in 1 Hair Dryer',
        'description': (
            '✓ 3-in-1 styling tool — hair dryer, straightener, and curler in one device\n'
            '✓ 1100W hot air brush for fast drying with less heat damage\n'
            '✓ Volumizing oval design — lifts roots, reduces frizz and flyaways\n'
            '✓ Three modes: Low, Medium, High — suits different hair types\n'
            '✓ Ergonomic and lightweight — comfortable for longer styling sessions\n'
            '✓ Ionic technology — less static, smoother, shinier hair\n'
            '✓ Ceramic coated barrel — even heat, fewer hot spots\n'
            '✓ 360° swivel cord — flexible movement without tangles'
        ),
        'affiliate_link': 'https://www.daraz.pk/products/1-3-i912065115-s3954005089.html?pvid=547efb89-f77e-4313-9ce4-f8a0a791c11b&search=jfy&scm=1007.51705.413671.0&spm=a2a0e.tm80335142.just4u.d_912065115',
        'images': ['images/p3.png'],
    }
]


def get_all_products(search_query=''):
    """Return all products (filtered by optional search query)."""
    query = search_query.lower().strip()
    items = PRODUCTS
    if query:
        items = [
            p for p in PRODUCTS
            if query in p['name'].lower() or query in p['description'].lower()
        ]

    return [
        {
            'id': p['id'],
            'name': p['name'],
            'description': p['description'],
            'affiliate_link': p['affiliate_link'],
            'primary_image': p['images'][0] if p.get('images') else None,
        }
        for p in items
    ]


def get_product_with_images(product_id):
    """Return one product and image objects for detail page."""
    for product in PRODUCTS:
        if product['id'] == product_id:
            images = [{'image_path': img} for img in product.get('images', [])]
            return product, images
    return None, []

# ─── Public Routes ─────────────────────────────────────────────────────────────

@app.route('/')
def index():
    """Homepage: show all products in a grid (manual data source)."""
    search_query = request.args.get('q', '').strip()
    products = get_all_products(search_query)
    return render_template('index.html', products=products, search_query=search_query)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    """Product detail page with image gallery."""
    product, images = get_product_with_images(product_id)
    if not product:
        return render_template('404.html'), 404
    return render_template('product_detail.html', product=product, images=images)

# ─── Error Handlers ────────────────────────────────────────────────────────────

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# ─── Entry Point ───────────────────────────────────────────────────────────────

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    print("ShopWise.com is running at http://127.0.0.1:5001")
    app.run(debug=True, host='0.0.0.0', port=5001)
