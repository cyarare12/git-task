# South African eCommerce Platform 🛍️🇿🇦

A comprehensive Django-based eCommerce web application featuring vendor and buyer functionality, with South African Rand pricing, dynamic product images, and a complete REST API. Includes social media integration and modern responsive design.

## 🌟 Features

### 👥 User Management
- **User Registration & Authentication** - Register as vendor or buyer
- **Role-based Access Control** - Different permissions for vendors and buyers
- **Password Reset** - Email-based password recovery with secure tokens

### 🏪 Vendor Features
- **Store Management** - Create, edit, and delete stores
- **Product Management** - Add, edit, and remove products from stores
- **Dashboard** - Overview of vendor's stores and products

### 🛒 Buyer Features
- **Product Browsing** - View products from all stores
- **Shopping Cart** - Session-based cart functionality
- **Checkout Process** - Complete orders with invoice generation
- **Product Reviews** - Leave verified/unverified reviews

### 💰 South African Currency
- **Rand Pricing** - All prices displayed in South African Rand (R)
- **Realistic Pricing** - Authentic local market prices
- **Currency Conversion** - Proper formatting and display

### 🖼️ Product Images
- **Dynamic Images** - Product-specific images from Unsplash API
- **Smart Categorization** - Images match product types (phones, clothing, furniture, etc.)
- **Fallback System** - Automatic image selection based on product names
- **Responsive Design** - Images adapt to all screen sizes with hover effects

### 🐦 Social Media Integration
- **Twitter/X Integration** - Automatic tweets for store and product creation
- **Real-time Updates** - Social media notifications for new business activities
- **Marketing Automation** - Automated social media presence for vendors

###  REST API
- **Complete API** - Full RESTful API for all functionality
- **Authentication** - Token-based API access
- **CRUD Operations** - Create, read, update, delete for all resources
- **Browsable Interface** - Interactive API documentation

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Django 5.2+
- Pillow (for image handling)
- Django REST Framework

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ecommerce_project
   ```

2. **Install dependencies**
   ```bash
   pip install django djangorestframework pillow
   ```

3. **Run migrations**
   ```bash
   python manage.py migrate
   ```

4. **Create sample data**
   ```bash
   python manage.py populate_sample_data
   ```

5. **Start the development server**
   ```bash
   python manage.py runserver
   ```

6. **Access the application**
   - Web interface: `http://127.0.0.1:8000/`
   - API interface: `http://127.0.0.1:8000/api/`

## 📊 Sample Data

The application comes pre-loaded with:
- **4 Vendors** with different store types
- **4 Stores** (Tech, Fashion, Home, Sports)
- **20 Products** with realistic South African pricing
- **Sample users** for testing

### Store Categories
- **TechZone Electronics** - Smartphones, laptops, headphones
- **Fashion Forward** - Clothing, shoes, accessories
- **Home & Living** - Furniture, decor, kitchenware
- **Sports Central** - Fitness equipment, sports gear

## 🛠️ API Endpoints

### Authentication Required Endpoints
- `POST /api/stores/` - Create store (vendors only)
- `POST /api/products/` - Create product (vendors only)
- `POST /api/reviews/` - Create review (authenticated users)

### Public Endpoints
- `GET /api/stores/` - List all stores
- `GET /api/products/` - List all products
- `GET /api/reviews/` - List all reviews

### Detailed Endpoints
- `GET/PUT/PATCH/DELETE /api/stores/<id>/` - Store details
- `GET/PUT/PATCH/DELETE /api/products/<id>/` - Product details
- `GET/PUT/PATCH/DELETE /api/reviews/<id>/` - Review details

## 🎨 Design Features

### Modern UI/UX
- **Responsive Design** - Works on all devices
- **Gradient Backgrounds** - Beautiful color schemes
- **Hover Effects** - Interactive elements
- **Card-based Layout** - Clean product displays

### South African Theming
- **Rand Currency** - R symbol throughout
- **Local Pricing** - Authentic SA market values
- **Cultural Relevance** - South African context

## 🔒 Security Features

- **User Authentication** - Django's built-in auth system
- **Role-based Permissions** - Vendor/buyer access control
- **CSRF Protection** - Cross-site request forgery prevention
- **Secure Password Reset** - Token-based recovery
- **API Authentication** - Token-based API access

## 📁 Project Structure

```
ecommerce_project/
├── ecommerce_project/          # Main Django project
│   ├── settings.py            # Django settings
│   ├── urls.py                # Main URL configuration
│   └── wsgi.py                # WSGI configuration
├── ecommerce/                 # Main app
│   ├── models.py              # Database models
│   ├── views.py               # View functions
│   ├── urls.py                # App URL patterns
│   ├── urls_api.py            # API URL patterns
│   ├── api_views.py           # API view classes
│   ├── serializers.py         # API serializers
│   ├── forms.py               # Django forms
│   ├── signals.py             # Django signals
│   ├── management/commands/   # Custom management commands
│   ├── static/ecommerce/css/  # CSS stylesheets
│   └── templates/ecommerce/   # HTML templates
├── media/                     # Uploaded media files
├── db.sqlite3                 # SQLite database
└── manage.py                  # Django management script
```

## 🧪 Testing

### Web Interface Testing
1. Visit `http://127.0.0.1:8000/`
2. Register as a vendor or buyer
3. Test store/product management (vendors)
4. Test browsing and purchasing (buyers)

### API Testing
1. Visit `http://127.0.0.1:8000/api/`
2. Use the browsable API interface
3. Test CRUD operations on all endpoints

## 🆕 Latest Updates

### Version 2.0 Features
- **🐦 Social Media Integration** - Automatic Twitter/X posts for new stores and products
- **🖼️ Smart Product Images** - Category-specific images from Unsplash API
- **🎨 Modern UI/UX** - Beautiful gradients, animations, and responsive design
- **💰 South African Rand** - Authentic local currency with realistic pricing
- **🔌 Enhanced API** - Complete REST API with browsable interface
- **📱 Mobile Optimization** - Fully responsive design for all devices

### Technical Improvements
- **Image Upload Support** - Django ImageField with media file handling
- **API Root Endpoint** - Interactive API documentation at `/api/`
- **Email Integration** - Console backend for development, SMTP ready for production
- **Security Enhancements** - CSRF protection, authentication, and permissions
- **Database Optimization** - Proper relationships and indexing

## 📈 Complete Features Overview

| Feature Category | Feature | Status | Description |
|------------------|---------|--------|-------------|
| **👥 User Management** | User Registration | ✅ | Role-based registration (vendor/buyer) |
| | Authentication | ✅ | Django auth with login/logout |
| | Password Reset | ✅ | Email-based secure recovery |
| | Profile Management | ✅ | User roles and preferences |
| **🏪 Vendor Features** | Store Management | ✅ | Full CRUD operations |
| | Product Management | ✅ | Add/edit/delete products with images |
| | Dashboard | ✅ | Vendor overview and analytics |
| | Social Media | ✅ | Automatic Twitter/X integration |
| **🛒 Buyer Features** | Product Browsing | ✅ | View all products with images |
| | Shopping Cart | ✅ | Session-based cart functionality |
| | Checkout Process | ✅ | Order completion with invoices |
| | Product Reviews | ✅ | Verified/unverified review system |
| **💰 Commerce** | South African Rand | ✅ | Local currency with realistic pricing |
| | Order Management | ✅ | Complete order lifecycle |
| | Invoice Generation | ✅ | Email delivery of order invoices |
| **🖼️ Visual Design** | Product Images | ✅ | Dynamic category-based images |
| | Responsive Design | ✅ | Mobile-friendly interface |
| | Modern UI/UX | ✅ | Beautiful gradients and animations |
| | Card-based Layout | ✅ | Clean product display |
| **🔌 API & Integration** | REST API | ✅ | Complete API with authentication |
| | API Documentation | ✅ | Browsable API interface |
| | Social Media API | ✅ | Twitter/X integration |
| | Email Integration | ✅ | SMTP ready for production |
| **🔒 Security** | Authentication | ✅ | Token-based API access |
| | Permissions | ✅ | Role-based access control |
| | CSRF Protection | ✅ | Cross-site request forgery prevention |
| | Secure Passwords | ✅ | Django's password validation |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Django Framework
- Django REST Framework
- Unsplash (for product images)
- Bootstrap (for responsive design)
- South African eCommerce inspiration

---

**Built with ❤️ for South African entrepreneurs and shoppers**