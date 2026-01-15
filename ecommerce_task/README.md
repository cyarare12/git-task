# Ecommerce Web Application Task

This folder contains the complete eCommerce web application built with Django, along with research answers for the practical task.

## 📁 Folder Structure

```
ecommerce_task/
├── ecommerce_project/          # Complete Django project
│   ├── ecommerce_project/      # Django project settings
│   ├── ecommerce/              # Django app
│   ├── db.sqlite3              # SQLite database
│   └── manage.py               # Django management script
├── research_answers.md         # Research questions answers
└── README.md                   # This file
```

## 🚀 How to Run the Application

### Prerequisites
- Python 3.8 or higher
- Django 5.2+

### Setup Instructions

1. **Navigate to the project directory:**
   ```bash
   cd ecommerce_task/ecommerce_project
   ```

2. **Run the Django development server:**
   ```bash
   python manage.py runserver
   ```

3. **Open your browser and go to:**
   - **Web App**: http://127.0.0.1:8000/
   - **API Endpoints**: http://127.0.0.1:8000/api/
   - **Zip File**: ecommerce_task.zip (ready to submit)

## 🎯 Features Implemented

### User Management
- User registration as vendors or buyers
- Login/logout functionality
- Role-based access control

### Vendor Features
- Create and manage stores
- Add, edit, and delete products
- View store products

### Buyer Features
- Browse all products
- Add products to shopping cart (session-based)
- Checkout with order creation
- Leave reviews (verified if purchased, unverified otherwise)

### Security & Authentication
- Password reset via email (console backend for testing)
- Session-based cart management
- User permissions and authentication

### Email System
- Invoice emails sent after checkout
- Password reset emails

## 🎨 Design Features

The application includes a modern, colorful design with:
- Gradient backgrounds
- Glassmorphism effects
- Responsive design
- Hover animations
- Professional typography
- Mobile-friendly interface

## 📊 Database Models

- **Profile**: User roles (vendor/buyer)
- **Store**: Vendor-owned stores
- **Product**: Store products with pricing
- **Order/OrderItem**: Purchase tracking
- **Review**: Product reviews (verified/unverified)
- **ResetToken**: Password reset tokens

## 🔍 Research Answers

The `research_answers.md` file contains detailed answers to the research questions about:
1. Python requests module
2. JSON vs XML data formats
3. RESTful APIs

## 🧪 Testing

The application has been tested with:
- User registration and login
- Product browsing and cart functionality
- Checkout process
- Email sending (console output)
- Password reset flow

## 📝 Notes

- Database is pre-populated with migrations
- Email backend is set to console for testing (emails appear in terminal)
- Static files are served automatically in development mode
- The application uses SQLite as the database engine

## 🏆 Task Completion

This submission includes:
- ✅ Complete Django eCommerce application
- ✅ All required features implemented
- ✅ Modern, attractive UI design
- ✅ Research questions answered
- ✅ Organized file structure
- ✅ Ready-to-run application
