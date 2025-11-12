# CR Reviews Platform

A comprehensive platform for students to review and rate their Class Representatives (CRs) in educational institutions.

## 🚀 Technologies Used

### Backend
<img src="https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white"/>
<img src="https://img.shields.io/badge/Django-092E20?style=flat&logo=django&logoColor=white"/>
<img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=flat&logo=postgresql&logoColor=white"/>

### Frontend
<img src="https://img.shields.io/badge/HTML5-E34F26?style=flat&logo=html5&logoColor=white"/>
<img src="https://img.shields.io/badge/CSS3-1572B6?style=flat&logo=css3&logoColor=white"/>
<img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=flat&logo=javascript&logoColor=black"/>
<img src="https://img.shields.io/badge/Bootstrap-563D7C?style=flat&logo=bootstrap&logoColor=white"/>

### Services
<img src="https://img.shields.io/badge/Cloudinary-3448C5?style=flat&logo=cloudinary&logoColor=white"/>
<img src="https://img.shields.io/badge/SendGrid-1A82E2?style=flat&logo=sendgrid&logoColor=white"/>
<img src="https://img.shields.io/badge/Render-46E3B7?style=flat&logo=render&logoColor=white"/>

## 📋 Features

- **User Authentication** - Secure login/signup system
- **CR Profiles** - Detailed profiles for Class Representatives
- **Review System** - Rate and review CRs with optional anonymity
- **Admin Dashboard** - Manage users, CRs, and reviews
- **Responsive Design** - Works on all devices
- **Image Upload** - Cloudinary integration for profile pictures
- **Email Notifications** - SendGrid integration for email communications

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone [your-repository-url]
   cd crreviews
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the project root and add:
   ```
   DEBUG=True
   SECRET_KEY=your-secret-key-here
   DATABASE_URL=sqlite:///db.sqlite3
   CLOUDINARY_URL=your-cloudinary-url
   SENDGRID_API_KEY=your-sendgrid-key
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

## 📂 Project Structure

```
crreviews/
├── admin_dashboard/      # Admin interface customizations
├── cr/                   # Main application (CR profiles, reviews)
├── crreviews/            # Project configuration
├── footer/               # Reusable footer component
├── static/               # Static files (CSS, JS, images)
├── templates/            # HTML templates
├── userprofile/          # User authentication and profiles
├── .env                  # Environment variables
├── .gitignore
├── manage.py
├── Procfile              # Deployment configuration
├── requirements.txt      # Python dependencies
└── README.md
```

## 🌐 Deployment

The application is configured for deployment on Render. The `Procfile` includes the necessary configuration for Gunicorn and static file handling.

1. Push your code to a Git repository
2. Create a new Web Service on Render and connect your repository
3. Add your environment variables in the Render dashboard
4. Deploy!

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Django for the awesome web framework
- Bootstrap for the responsive design
- Cloudinary for media storage
- SendGrid for email services
