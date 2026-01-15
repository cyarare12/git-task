# 📰 NewsHub - Django News Application

A modern, full-featured news platform built with Django that connects readers with independent journalists and curated publications.

## 📋 Table of Contents
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Configuration](#configuration)
- [Database Setup](#database-setup)
- [Running the Application](#running-the-application)
- [Admin Access](#admin-access)
- [User Roles & Permissions](#user-roles--permissions)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Deployment](#deployment)
- [Contributing](#contributing)

## ✨ Features

### 🎯 Core Functionality
- **User Authentication**: Registration and login system with role-based access
- **Article Management**: Create, read, update, and approve articles
- **Newsletter System**: Create and manage newsletters
- **Publisher Management**: Organize content by publications
- **Search & Filtering**: Advanced search functionality
- **Responsive Design**: Mobile-first, modern UI

### 👥 User Roles
- **Readers**: Access articles and newsletters, subscribe to journalists/publications
- **Journalists**: Create articles and newsletters, build audience
- **Editors**: Review and approve content, maintain quality standards

### 🎨 Modern UI/UX
- **Colorful Design**: Gradient backgrounds and modern styling
- **Interactive Elements**: Hover effects, animations, and transitions
- **Dark Mode**: Toggle between light and dark themes
- **Responsive Layout**: Optimized for all device sizes

## 🛠 Technology Stack

- **Backend**: Django 5.2.8
- **Database**: MariaDB (configured) / SQLite (development)
- **Frontend**: Bootstrap 5.3, HTML5, CSS3, JavaScript
- **API**: Django REST Framework
- **Authentication**: Django's built-in auth system
- **Email**: Django's email system (console backend for development)
- **File Uploads**: Django's media handling

## 📦 Installation

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- MariaDB (for production) or SQLite (for development)
- Git

### Clone the Repository
```bash
git clone <repository-url>
cd capstone_news_app
```

### Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

## ⚙️ Configuration

### Environment Variables
Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=mysql://user:password@localhost:3306/news_app_db
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
X_API_POST_URL=https://api.x.com/2/tweets
X_API_BEARER=your-twitter-bearer-token
```

### Django Settings
The application is configured with:
- Custom user model (`news.CustomUser`)
- REST Framework for API
- Media files handling
- Email configuration
- Social media integration (Twitter/X)

## 🗄️ Database Setup

### Development (SQLite)
```bash
python manage.py migrate
```

### Production (MariaDB)
1. Install MariaDB and create database:
```sql
CREATE DATABASE news_app_db;
CREATE USER 'newsuser'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON news_app_db.* TO 'newsuser'@'localhost';
FLUSH PRIVILEGES;
```

2. Update `settings.py` database configuration
3. Run migrations:
```bash
python manage.py migrate
```

### Create Groups and Permissions
```bash
python manage.py create_roles
```

## 🚀 Running the Application

### Development Server
```bash
python manage.py runserver
```

Access the application at: `http://127.0.0.1:8000/`

### Create Superuser (Admin)
```bash
python manage.py createsuperuser
```

## 👑 Admin Access

### Default Admin Credentials
```
Username: admin
Email: admin@example.com
Password: admin123
```

### Access Admin Panel
1. Go to: `http://127.0.0.1:8000/admin/`
2. Enter the credentials above
3. Click "Log in"

### Admin Capabilities
- **Users & Groups**: Create and manage user accounts with different roles
- **Articles**: Approve/reject articles, manage content
- **Categories**: Create and organize article categories
- **Publishers**: Manage publication entities
- **Newsletters**: View and manage newsletter content

## 👥 User Roles & Permissions

### Creating Test Users via Admin
1. Go to Authentication and Authorization > Users
2. Click "Add User +"
3. Fill in username, password, and email
4. Save the user
5. Edit the user to set their role (Reader/Journalist/Editor)
6. The system automatically assigns them to the correct group

### User Registration
For regular users (not admin), they can register through the main application:

1. Go to `http://127.0.0.1:8000/register/`
2. Fill out the registration form
3. Select their role during registration (Reader, Journalist, Editor)

### Role Permissions

#### Reader
- View articles and newsletters
- Subscribe to publishers and journalists
- Comment on articles

#### Journalist
- Create, view, update, and delete articles
- Create, view, update, and delete newsletters
- Build personal audience
- Access analytics

#### Editor
- View, update, and delete articles
- View, update, and delete newsletters
- Approve/reject article submissions
- Maintain content quality standards

## 🔌 API Documentation

### Authentication
The API uses token-based authentication. Include the Authorization header:
```
Authorization: Token <your-token>
```

### Endpoints

#### Articles API
- **GET** `/api/articles/` - Retrieve articles (filtered by user subscriptions)
- **Query Parameters**:
  - `publisher`: Filter by publisher ID
  - `author`: Filter by author ID

#### Authentication Required
All API endpoints require authentication. Only authenticated users can access articles from their subscribed publishers and journalists.

### Example API Usage
```bash
# Get articles for authenticated user
curl -H "Authorization: Token <token>" http://127.0.0.1:8000/api/articles/

# Get articles by specific publisher
curl -H "Authorization: Token <token>" "http://127.0.0.1:8000/api/articles/?publisher=1"
```

## 🧪 Testing

### Run Tests
```bash
python manage.py test
```

### Test Coverage
- User authentication and authorization
- Article CRUD operations
- API endpoints and permissions
- Newsletter functionality
- Search and pagination

## 🚀 Deployment

### Production Checklist
- [ ] Set `DEBUG = False`
- [ ] Configure production database (MariaDB/PostgreSQL)
- [ ] Set up proper email backend
- [ ] Configure static files serving
- [ ] Set up HTTPS
- [ ] Configure environment variables
- [ ] Set up monitoring and logging

### Example Production Setup
```bash
# Install production requirements
pip install gunicorn psycopg2-binary

# Collect static files
python manage.py collectstatic

# Run with Gunicorn
gunicorn news_app.wsgi:application --bind 0.0.0.0:8000
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and add tests
4. Run tests: `python manage.py test`
5. Commit your changes: `git commit -am 'Add feature'`
6. Push to the branch: `git push origin feature-name`
7. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For support and questions:
- Create an issue in the repository
- Contact the development team

## 🎯 Future Enhancements

- [ ] User profiles and avatars
- [ ] Social media sharing
- [ ] Comment system
- [ ] Article bookmarking
- [ ] Advanced analytics dashboard
- [ ] Mobile app development
- [ ] Multi-language support
- [ ] Advanced search filters

---

**Built with ❤️ using Django**