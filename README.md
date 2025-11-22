# CR Reviews 🎓

A comprehensive web platform for university students to review and discover Class Representatives (CRs) across different universities and departments in Bangladesh. This platform helps students make informed decisions by reading authentic reviews and ratings from their peers.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.2-green.svg)](https://www.djangoproject.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🌟 Features

### For Students
- **Browse CRs**: Search and filter CRs by university, department, batch, and ratings
- **Submit Reviews**: Write detailed reviews with 1-5 star ratings
- **Anonymous Reviews**: Option to submit anonymous reviews (requires admin approval)
- **Save Favorites**: Bookmark CRs for quick access
- **View Statistics**: Access comprehensive rating distributions and analytics
- **User Dashboard**: Manage your profile, reviews, and saved CRs

### For CR Representatives
- **Create Profile**: Build detailed profiles with bio, contact info, and social links
- **Track Reviews**: Monitor reviews and ratings
- **Profile Management**: Update information, photos, and status (Present/Former CR)
- **Social Integration**: Link Facebook, Instagram, and LinkedIn profiles

### For Administrators
- **Comprehensive Dashboard**: Monitor all platform activities
- **Review Moderation**: Approve/reject anonymous reviews
- **User Management**: Manage users, CRs, and reviews
- **Content Management**: Add/edit universities, departments
- **Notice System**: Post important announcements
- **Contact Messages**: Handle user inquiries
- **Developer Profiles**: Showcase team members
- **Analytics**: View monthly statistics and trends

## 🚀 Technology Stack

### Backend
- **Framework**: Django 5.2
- **Database**: SQLite (Development) / PostgreSQL (Production)
- **Authentication**: Django Auth + Google OAuth2
- **Image Storage**: Cloudinary
- **Email Service**: SendGrid via Anymail

### Frontend
- **Template Engine**: Django Templates
- **Styling**: Custom CSS with responsive design
- **JavaScript**: Vanilla JS for interactive features

### Deployment
- **Platform**: Render
- **Static Files**: WhiteNoise
- **Environment**: Python-decouple for config management

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)
- PostgreSQL (for production)
- Cloudinary account (for image storage)
- SendGrid account (for email services)

## 🔧 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/MNR-Tushar/crreviews.git
cd crreviews
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
Create a `.env` file in the root directory:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True

# Database (Production)
DATABASE_URL=your-postgresql-url

# Cloudinary Configuration
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret

# Email Configuration
EMAIL_BACKEND=anymail.backends.sendgrid.EmailBackend
DEFAULT_FROM_EMAIL=your-email@example.com
SERVER_EMAIL=your-email@example.com
SENDGRID_API_KEY=your-sendgrid-api-key

# Google OAuth2
GOOGLE_OAUTH2_CLIENT_ID=your-client-id
GOOGLE_OAUTH2_CLIENT_SECRET=your-client-secret
```

### 5. Database Setup
```bash
# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Load initial data (optional)
python manage.py loaddata fixtures/universities.json
python manage.py loaddata fixtures/departments.json
```

### 6. Collect Static Files
```bash
python manage.py collectstatic --noinput
```

### 7. Run Development Server
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` to access the application.

## 📁 Project Structure

```
crreviews/
├── admin_dashboard/       # Admin panel functionality
│   ├── models.py         # Notice, Contact, Developer models
│   ├── views.py          # Admin dashboard views
│   └── forms.py          # Admin forms
├── cr/                    # CR profiles and reviews
│   ├── models.py         # University, Department, CrProfile, Review
│   └── views.py          # CR-related views
├── userprofile/          # User authentication and profiles
│   ├── models.py         # Custom User model
│   ├── views.py          # Auth and profile views
│   ├── manager.py        # Custom user manager
│   └── pipeline.py       # Social auth pipeline
├── footer/               # Footer pages (About, Contact, etc.)
├── templates/            # HTML templates
├── static/               # Static files (CSS, JS, images)
├── media/                # User-uploaded files
└── crreviews/            # Project settings
    ├── settings.py       # Main configuration
    ├── urls.py           # URL routing
    └── wsgi.py           # WSGI configuration
```

## 🎯 Key Models

### User Model
Extended Django User with:
- University and Department relations
- Profile picture (Cloudinary)
- Student ID, batch, section
- Social media links
- Email verification system
- Password reset functionality

### CrProfile Model
- One-to-One with User
- University and Department
- CR status (Present/Former)
- Contact information
- Average rating calculation
- Social media integration

### Review Model
- User and CrProfile relations
- 1-5 star rating system
- Anonymous review support
- Admin approval workflow
- Unique constraint (one review per user per CR)

## 🔐 Authentication Features

- Email/Password registration
- Email verification system
- Password reset via email
- Google OAuth2 integration
- Session management
- Staff/Admin role separation

## 📧 Email System

- **Verification Emails**: Sent upon registration
- **Password Reset**: Secure token-based reset
- **Templates**: Professional HTML email templates
- **Provider**: SendGrid via Anymail

## 🖼️ Image Management

- **Storage**: Cloudinary CDN
- **Features**: 
  - Automatic resizing (500x500)
  - Face detection cropping
  - Format optimization
  - Quality compression
- **Default Images**: Fallback avatars for users without uploads

## 🔍 Search & Filter

- **Search**: Name, Student ID, Email, Batch, Section
- **Filters**: 
  - University
  - Department
  - Rating ranges (1-5 stars)
- **Pagination**: Efficient data loading
- **Sorting**: By date, rating, popularity

## 📊 Admin Dashboard Features

- **Statistics Overview**:
  - Total users, CRs, reviews
  - University/Department counts
  - Review approval status
  - Monthly growth charts

- **Management Panels**:
  - Users (view, edit, delete)
  - CRs (CRUD operations)
  - Reviews (moderation)
  - Universities & Departments
  - Notices & Messages

- **Approval System**: Anonymous review moderation

## 🌐 Deployment (Render)

### Prerequisites
1. Create Render account
2. Create PostgreSQL database
3. Configure Cloudinary
4. Set up SendGrid

### Steps
1. Push code to GitHub
2. Create new Web Service on Render
3. Configure environment variables
4. Set build command: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
5. Set start command: `gunicorn crreviews.wsgi:application`
6. Deploy!

## 🛡️ Security Features

- CSRF protection
- Password validation
- SQL injection prevention
- XSS protection
- Secure password hashing
- Token-based email verification
- Session security (production)
- Environment variable protection

## 🧪 Testing

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test cr
python manage.py test userprofile

# Generate coverage report
coverage run --source='.' manage.py test
coverage report
```

## 📝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🐛 Known Issues

- None currently reported

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **Md Naimur Rahman** - *Initial work* - [GitHub Profile](https://github.com/MNR-Tushar)

## 🙏 Acknowledgments

- Django Documentation
- Cloudinary for image hosting
- SendGrid for email services
- Bootstrap for UI components
- All contributors and testers

## 📞 Contact

- **GitHub**: [@MNR-Tushar](https://github.com/MNR-Tushar)
- **Project Link**: [https://github.com/MNR-Tushar/crreviews](https://github.com/MNR-Tushar/crreviews)
- **Live Demo**: [https://crreviews.onrender.com](https://crreviews.onrender.com)

## 🚀 Future Enhancements

- [ ] Mobile application (React Native)
- [ ] Real-time notifications
- [ ] Advanced analytics dashboard
- [ ] Multi-language support
- [ ] API for third-party integrations
- [ ] Machine learning for review sentiment analysis
- [ ] Chat system between students and CRs
- [ ] Events and announcements calendar

---

**Made with ❤️ for university students in Bangladesh**