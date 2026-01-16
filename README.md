# 🎓 Student Management System

A professional, deployment-ready Django web application for managing student information and generating QR-coded ID cards.

![Python](https://img.shields.io/badge/python-3.10-blue)
![Django](https://img.shields.io/badge/django-4.2-green)
![Docker](https://img.shields.io/badge/docker-ready-blue)

## ✨ Features

### 🔐 Core Functionality
- **Student CRUD Operations** - Create, Read, Update, Delete student records
- **QR Code Generation** - Automatic QR code creation for each student
- **Client-Side Camera Scanner** - Browser-based QR scanning (works on mobile!)
- **User Authentication** - Secure login/logout system
- **Search & Filtering** - Quick student lookup

### 📊 Professional Features
- **Dashboard with Analytics** - Visual charts showing student distribution
- **CSV Export** - Download student data for offline processing
- **REST API** - JSON endpoints for external integrations
- **Responsive Design** - Mobile-friendly, modern UI
- **Docker Support** - Production-ready containerization

## 🚀 Quick Start

### Option 1: Local Development

```bash
# Clone the repository
git clone <your-repo-url>
cd Studentmanagement

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your SECRET_KEY

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

Visit `http://localhost:8000/`

### Option 2: Docker (Recommended for Production)

```bash
# Build and run with Docker Compose
docker-compose up --build

# The app will be available at http://localhost:8000
```

## 📁 Project Structure

```
Studentmanagement/
├── main/                   # Main application
│   ├── models.py          # Student model with QR generation
│   ├── views.py           # Views + CSV export + dashboard
│   ├── api.py             # REST API endpoints
│   ├── tests.py           # Unit tests
│   └── templates/         # HTML templates
├── static/
│   └── css/
│       └── styles.css     # Modern design system
├── Dockerfile             # Container definition
├── docker-compose.yml     # Docker orchestration
├── requirements.txt       # Python dependencies
└── .env                   # Environment variables
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
SECRET_KEY=your-secret-key-here
DEBUG=False  # Set to True for development
```

### Database

- **Development**: SQLite (included)
- **Production**: Configure PostgreSQL/MySQL in `settings.py`

## 🧪 Testing

Run the comprehensive test suite:

```bash
python manage.py test
```

**Test Coverage:**
- Model creation and QR generation
- CRUD operations
- QR scanning API
- Authentication

## 📡 API Documentation

### REST Endpoints

#### List/Create Students
```
GET  /api/students/
POST /api/students/
```

#### Retrieve/Update/Delete Student
```
GET    /api/students/{id}/
PUT    /api/students/{id}/
DELETE /api/students/{id}/
```

#### Statistics
```
GET /api/stats/
```

#### QR Processing
```
POST /process_qr/
Body: {"qr_data": "ROLL_NUMBER"}
```

## 🎨 Tech Stack

- **Backend**: Django 4.2, Django REST Framework
- **Frontend**: HTML5, CSS3, JavaScript
- **QR Scanner**: html5-qrcode library
- **Database**: SQLite (default), PostgreSQL ready
- **Deployment**: Docker, Docker Compose

## 📸 Screenshots

### Dashboard
![Dashboard](docs/dashboard.png)

### QR Scanner
![Scanner](docs/scanner.png)

## 🛡️ Security Features

- ✅ Environment-based secrets
- ✅ CSRF protection
- ✅ Login required decorators
- ✅ Password validation
- ✅ SQL injection protection (Django ORM)

## 🚢 Deployment

### Heroku
```bash
heroku create your-app-name
git push heroku main
heroku run python manage.py migrate
```

### Railway
```bash
railway init
railway up
```

### AWS/GCP
Use the provided `Dockerfile` for containerized deployment.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 🌐 Live Demo

**[View Live Application](https://web-production-750fc.up.railway.app/)**

## 👤 Author

**Zain**
- Live Demo: [Student Management System](https://web-production-750fc.up.railway.app/)
- LinkedIn: [dev-zain](https://www.linkedin.com/in/dev-zain/)
- GitHub: [@dev-zain](https://github.com/dev-zain)

## 🙏 Acknowledgments

- Django community
- html5-qrcode library
- Modern web design inspiration from Tailwind CSS

---

**⭐ If you found this project helpful, please give it a star!**
